"""Storage Agent API routes."""

from __future__ import annotations
import logging
from fastapi import APIRouter, HTTPException
from models.task_models import StorageTaskRequest, StorageTaskResponse
from core.execution_engine import StorageExecutionEngine
from core.adapter_manager import StorageAdapterManager

logger = logging.getLogger(__name__)
router = APIRouter()
_engine = StorageExecutionEngine()


@router.post("/execute-task", response_model=StorageTaskResponse, summary="Execute a storage task")
async def execute_task(request: StorageTaskRequest) -> StorageTaskResponse:
    logger.info("Task '%s' | action='%s' | provider='%s' | resource='%s/%s'",
                request.task_id, request.action, request.provider,
                request.resource_type, request.resource_id)
    try:
        response = _engine.execute(request)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    return response


@router.get("/health", summary="Agent health check")
async def health() -> dict:
    return {"status": "ok", "agent": "storage-agent", "providers": StorageAdapterManager.registered_providers()}


@router.get("/providers", summary="List registered storage providers")
async def list_providers() -> dict:
    return {"providers": StorageAdapterManager.registered_providers()}
