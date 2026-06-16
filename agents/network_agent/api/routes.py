"""Network Agent API routes."""

from __future__ import annotations
import logging
from fastapi import APIRouter, HTTPException
from models.task_models import NetworkTaskRequest, NetworkTaskResponse
from core.execution_engine import NetworkExecutionEngine
from core.adapter_manager import NetworkAdapterManager

logger = logging.getLogger(__name__)
router = APIRouter()
_engine = NetworkExecutionEngine()


@router.post("/execute-task", response_model=NetworkTaskResponse, summary="Execute a network task")
async def execute_task(request: NetworkTaskRequest) -> NetworkTaskResponse:
    logger.info("Task '%s' | action='%s' | protocol='%s' | device='%s'",
                request.task_id, request.action, request.protocol, request.resource_id)
    try:
        response = _engine.execute(request)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    return response


@router.get("/health", summary="Agent health check")
async def health() -> dict:
    return {"status": "ok", "agent": "network-agent", "protocols": NetworkAdapterManager.registered_protocols()}


@router.get("/protocols", summary="List registered protocols")
async def list_protocols() -> dict:
    return {"protocols": NetworkAdapterManager.registered_protocols()}
