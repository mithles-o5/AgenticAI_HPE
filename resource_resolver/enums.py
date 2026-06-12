"""Enums used by the resource resolver routing pipeline."""

from enum import Enum


class IdentifierType(str, Enum):
    IP = "ip"
    SERIAL_NUMBER = "sn"
    FQDN = "fqdn"


class CacheStatus(str, Enum):
    HIT = "hit"
    MISS = "miss"


class ManagementSource(str, Enum):
    ONEVIEW = "oneview"
    COMS = "coms"


class ActionCategory(str, Enum):
    OPERATIONAL = "Operational"
    PROVISIONING = "Provisioning"


class ActionType(str, Enum):
    ON = "ON"
    OFF = "OFF"
    RESET = "RESET"
    COLD_BOOT = "COLD_BOOT"
    STATUS = "STATUS"
    CREATE = "CREATE"
    ALLOCATE = "ALLOCATE"
    DEALLOCATE = "DEALLOCATE"
    DELETE = "DELETE"
    RELOAD = "RELOAD"
    FAILOVER = "FAILOVER"
    POLICY_SYNC = "POLICY_SYNC"
    RESCAN = "RESCAN"




