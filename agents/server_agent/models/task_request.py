from pydantic import BaseModel, Field
from typing import Literal, Optional
from enum import Enum

class ResourceType(str, Enum):
    SERVER = "server"
    BMC = "bmc"
    SENSOR = "sensor"
    FIRMWARE = "firmware"
    EVENT_LOG = "event_log"

class Action(str, Enum):
    FETCH_METRICS = "fetch_metrics"
    EXECUTE_ACTION = "execute_action"
    HEALTH_CHECK = "health_check"
    DISCOVER_INVENTORY = "discover_inventory"
    FETCH_EVENT_LOG = "fetch_event_log"
    SYNC_CMDB = "sync_cmdb"

class Provider(str, Enum):
    REDFISH = "redfish"
    IPMI = "ipmi"
    ILO = "ilo"
    DEFAULT = "default"

class TaskRequest(BaseModel):
    task_id: str
    task_type: str
    agent_type: Literal["server"] = "server"
    resource_type: ResourceType
    resource_id: str
    region: Optional[str] = None
    provider: str = "default"
    action: Action
    parameters: dict = Field(default_factory=dict)
    credentials_ref: Optional[str] = "mock"
