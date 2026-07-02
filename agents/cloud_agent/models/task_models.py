"""Cloud Agent - Pydantic Models: TaskRequest and TaskResponse."""

from __future__ import annotations
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class TaskRequest(BaseModel):
    """Unified task request consumed by all cloud adapters."""

    task_id: str = Field(..., description="Unique task identifier from the orchestrator.")
    task_type: str = Field(..., description="Type of task: 'monitoring' | 'control' | 'discovery' | 'health_check' | 'anomaly'.")
    agent_type: str = Field(default="cloud", description="Always 'cloud' for this agent.")
    resource_type: str = Field(..., description="Logical resource type: 'vm' | 'container' | 'function' | 'cluster_node' | etc.")
    resource_id: str = Field(..., description="Provider-agnostic resource identifier.")
    region: Optional[str] = Field(default=None, description="Cloud region or availability zone. Optional for on-prem.")
    provider: str = Field(..., description="Cloud provider identifier: 'aws' | 'gcp' | 'mock' | any custom label.")
    action: str = Field(
        ...,
        description=(
            "Action to execute: 'fetch_metrics' | 'execute_action' | 'health_check' "
            "| 'discover_resources' | 'detect_anomaly'"
        ),
    )
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Action-specific parameters.")
    credentials_ref: Optional[str] = Field(
        default=None,
        description="Opaque reference to the Credential Vault secret. Agent fetches creds at runtime.",
    )


class TaskResponse(BaseModel):
    """Unified task response emitted by all cloud adapters — normalized to this schema."""

    task_id: str
    status: str = Field(..., description="'success' | 'failed' | 'partial'")
    agent_type: str = "cloud"
    resource_type: str
    resource_id: str
    region: Optional[str] = None
    provider: str
    metrics: Dict[str, Any] = Field(default_factory=dict, description="Normalized metric KVs.")
    actions_taken: List[str] = Field(default_factory=list, description="Human-readable log of steps executed.")
    status_level: str = Field(default="healthy", description="'healthy' | 'warning' | 'critical'")
    insights: List[str] = Field(default_factory=list, description="Anomaly insights or recommendations.")
    errors: List[str] = Field(default_factory=list, description="Error messages if any step failed.")
