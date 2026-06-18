import os
import json
import logging
import httpx
from fastapi import FastAPI
from api.routes import router
from config.settings import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("onprem_agent.main")

app = FastAPI(
    title="HPE On-Prem Agent Microservice",
    description="OASF-compliant agent service for managing HPE physical/composable infrastructure",
    version="1.0.0"
)

# Attach routes
app.include_router(router)

@app.get("/health")
def health():
    """Service health check endpoint."""
    return {"status": "healthy", "service": "onprem-agent"}

@app.on_event("startup")
async def register_with_capability_registry():
    """
    On startup, POST oasf_record.json to CAPABILITY_REGISTRY_URL
    to publish agent capability registration in the OASF ecosystem.
    """
    registry_url = settings.CAPABILITY_REGISTRY_URL
    if not registry_url or registry_url.startswith("mock") or "localhost:8003" in registry_url:
        logger.warning("CAPABILITY_REGISTRY_URL missing or matches dev URL. Skipping capability registration.")
        return

    record_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "oasf_record.json")
    if not os.path.exists(record_path):
        logger.error(f"Cannot register capability: oasf_record.json not found at {record_path}")
        return

    try:
        with open(record_path, "r", encoding="utf-8") as f:
            record = json.load(f)
            
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{registry_url}/agents",
                json=record,
                timeout=10.0
            )
            response.raise_for_status()
            logger.info(f"Successfully published OASF manifest to registry at: {registry_url}")
    except Exception as e:
        logger.error(f"Failed to publish OASF record to capability registry: {e}")
        # We do not raise the error here to ensure the microservice startup is resilient 
        # to external registration dependencies failing.

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)

