from fastapi import APIRouter, HTTPException, Query, status
from models.task_request import TaskRequest
from models.task_response import TaskResponse
from core.task_handler import TaskHandler
from core.poll_handler import ServerPollHandler
from core.adapter_manager import get_adapter

router = APIRouter()
task_handler = TaskHandler()
poll_handler = ServerPollHandler()

@router.post("/execute-task", response_model=TaskResponse, status_code=status.HTTP_200_OK)
async def execute_task(request: TaskRequest):
    """
    Accepts OASF TaskRequest and routes it to the corresponding adapter via Execution Engine.
    """
    return await task_handler.handle(request)

@router.get("/health")
def health():
    """
    Liveness and readiness health check endpoint.
    """
    return {"status": "healthy", "agent": "server-agent", "version": "1.0.0"}

@router.get("/inventory/{resource_id}")
def get_inventory(
    resource_id: str,
    provider: str = Query("redfish", description="Bmc provider name"),
    credentials_ref: str = Query("mock", description="Vault credentials pointer")
):
    """
    Fetch and discover hardware inventory details from the target server BMC.
    """
    try:
        adapter = get_adapter(provider, credentials_ref)
        raw_inv = adapter.discover_inventory({"resource_id": resource_id})
        
        if not raw_inv:
            return {"cpus": [], "memory": [], "storage": [], "nics": [], "firmware": []}
            
        inv_item = raw_inv[0]
        return {
            "cpus": inv_item.get("cpus", []),
            "memory": inv_item.get("memory", []),
            "storage": inv_item.get("storage", []),
            "nics": inv_item.get("nics", []),
            "firmware": inv_item.get("firmware", [])
        }
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to discover inventory: {str(exc)}"
        )

@router.post("/poll/trigger")
def trigger_poll():
    """
    Manual trigger to force a sync of metrics/sensors to CMDB.
    """
    summary = poll_handler.run_poll_cycle()
    return summary
