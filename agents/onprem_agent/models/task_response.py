from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List

class TaskResponse(BaseModel):
    task_id: str
    status: str  # success, failed, partial
    agent_type: str = "onprem"
    resource_type: Optional[str] = None
    resource_id: Optional[str] = None
    region: Optional[str] = None
    metrics: Dict[str, Any] = Field(default_factory=dict)
    actions_taken: List[str] = Field(default_factory=list)
    status_level: str  # healthy, warning, critical
    insights: List[Dict[str, Any]] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list)
