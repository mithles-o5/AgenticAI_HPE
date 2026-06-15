"""Cloud Agent task handler — FastAPI router wiring TaskRequest → ExecutionEngine → TaskResponse."""

from __future__ import annotations
import logging

from fastapi import APIRouter, HTTPException

from models.task_models import TaskRequest, TaskResponse
from core.execution_engine import CloudExecutionEngine
from core.adapter_manager import AdapterManager

logger = logging.getLogger(__name__)
router = APIRouter()
_engine = CloudExecutionEngine()


@router.post("/execute-task", response_model=TaskResponse, summary="Execute a cloud task")
async def execute_task(request: TaskRequest) -> TaskResponse:
    """
    Primary task endpoint consumed by the MCP Execution Engine.

    Accepts a TaskRequest, routes it to the correct cloud adapter, and
    returns a normalized TaskResponse with metrics, anomaly insights, and errors.
    """
    logger.info(
        "Received task '%s' | action='%s' | provider='%s' | resource='%s/%s'",
        request.task_id, request.action, request.provider,
        request.resource_type, request.resource_id,
    )
    try:
        response = _engine.execute(request)
    except Exception as exc:
        logger.exception("Unhandled error processing task '%s'", request.task_id)
        raise HTTPException(status_code=500, detail=str(exc))

    logger.info(
        "Task '%s' completed | status='%s' | level='%s'",
        response.task_id, response.status, response.status_level,
    )
    return response


@router.get("/health", summary="Agent health check")
async def health() -> dict:
    """Liveness probe for orchestrator and load-balancer health checks."""
    return {
        "status":    "ok",
        "agent":     "cloud-agent",
        "providers": AdapterManager.registered_providers(),
    }


@router.get("/providers", summary="List registered cloud providers")
async def list_providers() -> dict:
    """Return all registered cloud adapter provider labels."""
    return {"providers": AdapterManager.registered_providers()}
