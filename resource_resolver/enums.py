from enum import Enum


class Vendor(str, Enum):
    HPE = "HPE"


class DeploymentType(str, Enum):
    CLOUD   = "Cloud"          # Compute Ops API (cloud-hosted)
    ON_PREM = "On-Premises"    # OneView API (on-premises)


class Protocol(str, Enum):
    ONEVIEW = "OneView"        # HPE OneView API (on-premises)
    COMS    = "COMS"           # HPE Compute Ops API (cloud)


class ActionCategory(str, Enum):
    PROVISIONING = "Provisioning"   # Create / Allocate
    OPERATIONAL  = "Operational"    # Power, Reboot, Status, etc.


class PowerAction(str, Enum):
    ON     = "On"
    OFF    = "Off"
    RESET  = "Reset"
    COLD   = "ColdBoot"
    STATUS = "Status"


class ProvisionAction(str, Enum):
    CREATE     = "Create"
    ALLOCATE   = "Allocate"
    DEALLOCATE = "Deallocate"
    DELETE     = "Delete"


class ResourceHealth(str, Enum):
    OK       = "OK"
    WARNING  = "Warning"
    CRITICAL = "Critical"
    UNKNOWN  = "Unknown"


class CacheStatus(str, Enum):
    HIT  = "hit"
    MISS = "miss"
