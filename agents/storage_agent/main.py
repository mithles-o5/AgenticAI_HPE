"""Storage Agent — FastAPI application entry point. Port 8007."""

from __future__ import annotations
import json, logging, os, sys

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import httpx
from fastapi import FastAPI
from contextlib import asynccontextmanager
from api.routes import router
from config.settings import settings
from core.poll_handler import StoragePollHandler

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s — %(message)s")
logger = logging.getLogger("storage-agent")

# Global poll handler — started/stopped in lifespan
_poll_handler = StoragePollHandler()


@asynccontextmanager
async def lifespan(application: FastAPI):
    logger.info("Storage Agent starting on port %d …", settings.SERVICE_PORT)

    # Register with Capability Registry
    try:
        with open(os.path.join(_HERE, "oasf_record.json")) as f:
            record = json.load(f)
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.post(f"{settings.CAPABILITY_REGISTRY_URL}/agents", json=record)
            if resp.is_success:
                logger.info("Registered with Capability Registry ✓")
            else:
                logger.warning("Registry returned %d", resp.status_code)
    except Exception as exc:
        logger.warning("Could not reach Capability Registry: %s", exc)

    # Start poll scheduler
    _poll_handler.start()

    yield

    # Shutdown
    _poll_handler.stop()
    logger.info("Storage Agent shutting down.")


app = FastAPI(
    title="Storage Agent",
    description=(
        "Storage capacity monitoring, volume management, SAN/NAS/S3 health checks, "
        "anomaly detection, and GreenLake DSCC integration."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(router, prefix="/storage-agent", tags=["Storage Agent"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=settings.SERVICE_PORT, reload=True)
