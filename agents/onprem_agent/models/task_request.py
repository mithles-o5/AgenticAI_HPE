from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class TaskRequest(BaseModel):
    task_id: str
    task_type: str
    agent_type: str = "onprem"
    resource_type: Optional[str] = None
    resource_id: Optional[str] = None
    region: Optional[str] = None
    provider: str = "default"  # oneview, com, default
    action: str  # fetch_metrics, execute_action, health_check, discover_inventory, fetch_alerts, sync_cmdb
    parameters: Dict[str, Any] = Field(default_factory=dict)
    credentials_ref: Optional[str] = None
