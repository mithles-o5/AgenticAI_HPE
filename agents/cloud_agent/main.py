"""Cloud Agent — FastAPI application entry point.

On startup:
  • Registers OASF capability record with the Capability Registry.
  • Mounts all API routes.

Run locally:
  uvicorn main:app --host 0.0.0.0 --port 8005 --reload
"""

from __future__ import annotations
import json
import logging
import os
import sys

# ── Ensure the agent package root is on sys.path (for direct uvicorn invocation)
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import httpx
from fastapi import FastAPI
from contextlib import asynccontextmanager

from api.routes import router
from config.settings import settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
)
logger = logging.getLogger("cloud-agent")


# ── Lifespan: startup + shutdown ───────────────────────────────────────────────
@asynccontextmanager
async def lifespan(application: FastAPI):
    # ── Startup ───────────────────────────────────────────────────────────────
    logger.info("Cloud Agent starting on port %d …", settings.SERVICE_PORT)
    _record_path = os.path.join(_HERE, "oasf_record.json")
    try:
        with open(_record_path) as f:
            record = json.load(f)
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.post(
                f"{settings.CAPABILITY_REGISTRY_URL}/agents",
                json=record,
            )
            if resp.is_success:
                logger.info("Registered with Capability Registry ✓")
            else:
                logger.warning(
                    "Capability Registry returned %d — continuing without registration.",
                    resp.status_code,
                )
    except Exception as exc:
        logger.warning("Could not reach Capability Registry: %s — continuing.", exc)

    yield

    # ── Shutdown ──────────────────────────────────────────────────────────────
    logger.info("Cloud Agent shutting down.")


# ── Application factory ────────────────────────────────────────────────────────
app = FastAPI(
    title="Cloud Agent",
    description=(
        "Universal cloud observability, control-plane execution, and anomaly "
        "detection microservice. Supports any cloud provider via pluggable adapters."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(router, prefix="/cloud-agent", tags=["Cloud Agent"])


# ── Module-level entry point (python main.py) ──────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=settings.SERVICE_PORT, reload=True)
