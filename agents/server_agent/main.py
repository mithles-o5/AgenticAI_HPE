import os
import sys
import json
import time
import httpx
import structlog
import uuid
import re
from fastapi import FastAPI, Request, Response, HTTPException
from contextlib import asynccontextmanager

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from api.routes import router
from config.settings import settings
from core.poll_handler import ServerPollHandler

# Configure structlog JSON logging
structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ]
)

logger = structlog.get_logger()
poll_handler = ServerPollHandler()

async def register_with_capability_registry():
    try:
        record_path = os.path.join(_HERE, "oasf_record.json")
        with open(record_path, "r") as f:
            record = json.load(f)
            
        cap_url = os.getenv("CAPABILITY_REGISTRY_URL", settings.CAPABILITY_REGISTRY_URL)
        logger.info("Registering capabilities with registry", registry_url=cap_url)
        
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{cap_url}/agents",
                json=record,
                timeout=10.0
            )
            resp.raise_for_status()
            logger.info("Registered successfully with Capability Registry")
    except Exception as e:
        logger.warning("Capability Registry registration failed (ignoring for local mode)", error=str(e))

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup actions
    await register_with_capability_registry()
    poll_handler.start()
    yield
    # Shutdown actions
    poll_handler.stop()

app = FastAPI(
    title="Server Agent",
    description="Physical/bare-metal server management microservice via Redfish, IPMI, and iLO",
    version="1.0.0",
    lifespan=lifespan
)

# Middleware: Request ID and execution time
@app.middleware("http")
async def add_process_time_and_request_id(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(request_id=request_id)
    
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    response.headers["X-Request-ID"] = request_id
    
    logger.info(
        "Request processed",
        method=request.method,
        path=request.url.path,
        status_code=response.status_code,
        duration_s=process_time
    )
    return response

# Mount routes
app.include_router(router, prefix="/server-agent", tags=["Server Agent"])

# Proxy handler to forward server-related requests to the mock API servers
async def handle_proxy(request: Request, target_base: str, is_oneview: bool):
    full_path = request.url.path
    path_clean = full_path
    if path_clean.startswith("/server-agent"):
        path_clean = path_clean[len("/server-agent"):]
        
    if is_oneview:
        # OneView category checking
        if path_clean.startswith("/rest/"):
            parts = [p for p in path_clean.split("/") if p]
            if len(parts) >= 2:
                category = parts[1]
                if category not in {"server-hardware", "custom-servers", "rack-managers", "updates", "certificates", "login-sessions"}:
                    raise HTTPException(
                        status_code=403,
                        detail="Access denied: Only server-related APIs are accessible through the Server Agent."
                    )
    else:
        # Compute Ops category checking
        if path_clean.startswith("/compute-ops-mgmt/") or path_clean.startswith("/compute-ops/"):
            parts = [p for p in path_clean.split("/") if p]
            if len(parts) >= 2:
                if re.match(r"^v\d", parts[1]):
                    category_idx = 2
                else:
                    category_idx = 1
                
                if len(parts) > category_idx:
                    category = parts[category_idx]
                    if category in {"storage", "switches", "networks"}:
                        raise HTTPException(
                            status_code=403,
                            detail="Access denied: Only server-related APIs are accessible through the Server Agent."
                        )
            
    # Rewrite legacy /compute-ops/ prefix → /compute-ops-mgmt/ (the mock only exposes /compute-ops-mgmt/)
    if not is_oneview and path_clean.startswith("/compute-ops/"):
        path_clean = "/compute-ops-mgmt/" + path_clean[len("/compute-ops/"):]

    target_url = f"{target_base}{path_clean}"
    if request.url.query:
        target_url += f"?{request.url.query}"
        
    async with httpx.AsyncClient() as client:
        body = await request.body()
        headers = dict(request.headers)
        headers.pop("host", None)
        try:
            resp = await client.request(
                method=request.method,
                url=target_url,
                headers=headers,
                content=body,
                timeout=30.0
            )
            return Response(
                content=resp.content,
                status_code=resp.status_code,
                headers=dict(resp.headers)
            )
        except Exception as e:
            raise HTTPException(status_code=502, detail=f"Proxy request failed: {str(e)}")

@app.api_route("/rest/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
@app.api_route("/server-agent/rest/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_oneview(request: Request, path: str):
    return await handle_proxy(request, settings.ONEVIEW_URL, is_oneview=True)

@app.api_route("/compute-ops-mgmt/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
@app.api_route("/server-agent/compute-ops-mgmt/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
@app.api_route("/compute-ops/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
@app.api_route("/server-agent/compute-ops/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_compute_ops(request: Request, path: str):
    return await handle_proxy(request, settings.COMPUTE_OPS_URL, is_oneview=False)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=settings.PORT, reload=True)
