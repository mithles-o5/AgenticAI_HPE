from pydantic import BaseModel, Field
from typing import Literal, Optional, List, Dict, Any
from enum import Enum

class StatusLevel(str, Enum):
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"

class SensorReading(BaseModel):
    name: str
    reading: float
    units: str
    status: str   # OK/Warning/Critical/Unknown

class ServerMetrics(BaseModel):
    # CPU / Memory
    cpu_utilization: float = 0.0          # %
    memory_utilization: float = 0.0       # %
    cpu_count: int = 0
    memory_total_gb: float = 0.0

    # Power & thermal
    power_consumed_watts: float = 0.0
    power_capacity_watts: float = 0.0
    power_utilization_pct: float = 0.0    # computed
    inlet_temperature_celsius: float = 0.0
    cpu_temperature_celsius: float = 0.0

    # Component health rollups
    overall_health: str = "Unknown"       # OK/Warning/Critical/Unknown
    power_supply_status: str = "Unknown"
    fan_status: str = "Unknown"
    storage_status: str = "Unknown"
    network_status: str = "Unknown"

    # Sensors (populated on fetch_metrics for resource_type=sensor)
    sensors: List[SensorReading] = Field(default_factory=list)

    # Power state
    power_state: str = "Unknown"          # On/Off/PoweringOn/PoweringOff

    # Event log (populated on fetch_event_log)
    event_count: int = 0
    critical_event_count: int = 0
    recent_events: List[Dict[str, Any]] = Field(default_factory=list)

    # Predictive failure
    predictive_failure_count: int = 0

    # Inventory (populated on discover_inventory)
    inventory: Optional[List[Dict[str, Any]]] = None

class TaskResponse(BaseModel):
    task_id: str
    status: Literal["success", "failed", "partial"]
    agent_type: Literal["server"] = "server"
    resource_type: str
    resource_id: str
    region: Optional[str] = None
    metrics: ServerMetrics = Field(default_factory=ServerMetrics)
    actions_taken: List[str] = Field(default_factory=list)
    status_level: StatusLevel = StatusLevel.HEALTHY
    insights: List[str] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list)
