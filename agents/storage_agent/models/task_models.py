"""Storage Agent — Pydantic models."""

from __future__ import annotations
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class StorageTaskRequest(BaseModel):
    task_id: str
    task_type: str = Field(..., description="'monitoring' | 'control' | 'discovery' | 'health_check' | 'poll'")
    agent_type: str = "storage"
    resource_type: str = Field(..., description="'volume' | 'array' | 'pool' | 'lun' | 'share' | 'bucket' | 'snapshot'")
    resource_id: str
    region: Optional[str] = None
    provider: str = Field(..., description="'dscc' | 'nas' | 's3' | 'mock'")
    action: str = Field(
        ...,
        description=(
            "'fetch_capacity' | 'fetch_performance' | 'execute_action' "
            "| 'discover_arrays' | 'health_check' | 'poll'"
        ),
    )
    parameters: Dict[str, Any] = Field(default_factory=dict)
    credentials_ref: Optional[str] = None


class StorageTaskResponse(BaseModel):
    task_id: str
    status: str = Field(..., description="'success' | 'failed' | 'partial'")
    agent_type: str = "storage"
    resource_type: str
    resource_id: str
    region: Optional[str] = None
    provider: str
    metrics: Dict[str, Any] = Field(default_factory=dict)
    actions_taken: List[str] = Field(default_factory=list)
    status_level: str = "healthy"
    insights: List[str] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list)
