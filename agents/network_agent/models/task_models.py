"""Network Agent — Pydantic models for unified request/response contracts."""

from __future__ import annotations
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class NetworkTaskRequest(BaseModel):
    task_id: str
    task_type: str = Field(..., description="'monitoring' | 'config_push' | 'discovery' | 'fault_detection'")
    agent_type: str = "network"
    resource_type: str = Field(..., description="'switch' | 'router' | 'interface' | 'vlan' | 'bgp_session'")
    resource_id: str
    region: Optional[str] = None
    protocol: str = Field(..., description="'snmp' | 'netconf' | 'rest' | 'mock'")
    action: str = Field(
        ...,
        description=(
            "'fetch_metrics' | 'execute_config_push' | 'discover_topology' "
            "| 'detect_fault' | 'health_check'"
        ),
    )
    parameters: Dict[str, Any] = Field(default_factory=dict)
    credentials_ref: Optional[str] = None


class InterfaceMetrics(BaseModel):
    name: str
    status: str = "unknown"
    in_octets_per_sec: float = 0.0
    out_octets_per_sec: float = 0.0
    in_errors: int = 0
    out_errors: int = 0
    utilization_pct: float = 0.0


class TopologyNode(BaseModel):
    node_id: str
    hostname: str
    device_type: str
    interfaces: List[str] = Field(default_factory=list)
    neighbors: List[str] = Field(default_factory=list)


class NetworkTaskResponse(BaseModel):
    task_id: str
    status: str = Field(..., description="'success' | 'failed' | 'partial'")
    agent_type: str = "network"
    resource_type: str
    resource_id: str
    region: Optional[str] = None
    protocol: str
    metrics: Dict[str, Any] = Field(default_factory=dict)
    topology: List[TopologyNode] = Field(default_factory=list)
    actions_taken: List[str] = Field(default_factory=list)
    status_level: str = "healthy"
    insights: List[str] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list)
