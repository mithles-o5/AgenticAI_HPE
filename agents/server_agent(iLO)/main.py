import os
import sys
import json
import time
import httpx
import structlog
import uuid
from fastapi import FastAPI, Request
from contextlib import asynccontextmanager

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from api.routes import router
from config.settings import settings
from core.poll_handler import ServerPollHandler

import logging
structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
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
    description="Physical/bare-metal server management microservice via Redfish and iLO",
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=settings.PORT, reload=True)
