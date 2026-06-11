import logging
from fastapi import APIRouter, HTTPException
from models.task_request import TaskRequest
from models.task_response import TaskResponse
from core.task_handler import TaskHandler

logger = logging.getLogger("onprem_agent.api.routes")
router = APIRouter()
task_handler = TaskHandler()

@router.post("/tasks", response_model=TaskResponse)
async def execute_task(request: TaskRequest):
    """
    Executes a specific skill/action against HPE infrastructure.
    Delegates parsing and execution to the TaskHandler.
    """
    try:
        response = await task_handler.handle_task(request)
        return response
    except Exception as e:
        logger.error(f"Task routing failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal handler failed to process task: {str(e)}"
        )
