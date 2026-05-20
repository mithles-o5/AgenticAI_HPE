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


class ResourceType(str, Enum):
    """
    OneView & COMS resource types.
    Maps to REST API endpoints and resource schemas.
    """
    # ─────────────────────────────────────────────────────────────────────────
    # OneView Resource Types (Comprehensive)
    # ─────────────────────────────────────────────────────────────────────────
    
    # Server Hardware & Provisioning
    SERVER_HARDWARE            = "ServerHardware"
    SERVER_PROFILE             = "ServerProfile"
    SERVER_PROFILE_TEMPLATE    = "ServerProfileTemplate"
    RACK_MANAGER               = "RackManager"
    
    # Networking
    ETHERNET_NETWORK           = "EthernetNetwork"
    FC_NETWORK                 = "FcNetwork"
    NETWORK_SET                = "NetworkSet"
    INTERCONNECT               = "Interconnect"
    INTERCONNECT_TYPE          = "InterconnectType"
    UPLINK_SET                 = "UplinkSet"
    LOGICAL_INTERCONNECT       = "LogicalInterconnect"
    LOGICAL_INTERCONNECT_GROUP = "LogicalInterconnectGroup"
    INTERNAL_NETWORK           = "InternalNetwork"
    
    # Storage
    STORAGE_SYSTEM             = "StorageSystem"
    STORAGE_POOL               = "StoragePool"
    VOLUME                     = "Volume"
    VOLUME_TEMPLATE            = "VolumeTemplate"
    VOLUME_SNAPSHOT            = "VolumeSnapshot"
    DRIVE_ENCLOSURE            = "DriveEnclosure"
    
    # Enclosures & Facilities
    ENCLOSURE                  = "Enclosure"
    ENCLOSURE_GROUP            = "EnclosureGroup"
    RACK                       = "Rack"
    DATACENTER                 = "Datacenter"
    
    # Firmware & Updates
    FIRMWARE_DRIVER            = "FirmwareDriver"
    FIRMWARE_BUNDLE            = "FirmwareBundle"
    
    # Tasks, Events & Monitoring
    TASK                       = "Task"
    ALERT                      = "Alert"
    EVENT                      = "Event"
    AUDIT_LOG                  = "AuditLog"
    
    # Security & Authentication
    CERTIFICATE                = "Certificate"
    USER                       = "User"
    ROLE                       = "Role"
    LDAP                       = "LDAP"
    ACTIVE_DIRECTORY           = "ActiveDirectory"
    SESSION                    = "Session"
    
    # Settings & Configuration
    SCOPE                      = "Scope"
    SETTING                    = "Setting"
    VERSION                    = "Version"
    HEALTH_STATUS              = "HealthStatus"
    
    # Appliance Management
    APPLIANCE_INFO             = "ApplianceInfo"
    APPLIANCE_NETWORK          = "ApplianceNetwork"
    APPLIANCE_LICENSES         = "ApplianceLicenses"
    APPLIANCE_BACKUP           = "ApplianceBackup"
    APPLIANCE_RESTART          = "ApplianceRestart"
    
    # Remote Support & Telemetry
    REMOTE_SUPPORT             = "RemoteSupport"
    REMOTE_SUPPORT_CONTACTS    = "RemoteSupportContacts"
    TELEMETRY_STREAMING        = "TelemetryStreaming"
    SUPPORT_DUMP               = "SupportDump"
    
    # Hypervisors
    HYPERVISOR_MANAGER         = "HypervisorManager"
    HYPERVISOR_PROFILE         = "HypervisorProfile"
    
    # Search & Indexing
    SEARCH                     = "Search"
    RESOURCE_INDEX             = "ResourceIndex"
    
    # Metrics & Performance
    METRICS                    = "Metrics"
    PERFORMANCE_COUNTERS       = "PerformanceCounters"
    
    # Licensing
    LICENSE                    = "License"
    LICENSE_POOL               = "LicensePool"
    
    # ─────────────────────────────────────────────────────────────────────────
    # COMS (HPE Compute Ops Management) Resource Types
    # ─────────────────────────────────────────────────────────────────────────
    
    # Server Resources
    SERVER                     = "Server"
    
    # Infrastructure & Configuration
    COMS_AHS_FILES             = "AhsFiles"
    COMS_APPLIANCES            = "Appliances"
    COMS_ACTIVATION_KEYS       = "ActivationKeys"
    COMS_ACTIVATION_TOKENS     = "ActivationTokens"
    COMS_ACTIVITIES            = "Activities"
    COMS_FIRMWARE_BUNDLES      = "FirmwareBundles"
    COMS_APPROVAL_POLICY       = "ApprovalPolicy"
    COMS_APPROVAL_REQUEST      = "ApprovalRequest"
    COMS_EXTERNAL_SERVICES     = "ExternalServices"
    
    # Async Operations & Jobs
    COMS_ASYNC_OPS_V1          = "AsyncOpsV1"
    COMS_ASYNC_OPS_V1BETA      = "AsyncOpsV1Beta"
    COMS_JOB_TEMPLATES         = "JobTemplates"
    COMS_JOBS                  = "Jobs"
    COMS_TASKS                 = "ComsTask"
    
    # Groups & Organization
    COMS_GROUPS                = "Groups"
    
    # Reporting & Analytics
    COMS_REPORTS               = "Reports"
    COMS_FILTERS               = "Filters"
    COMS_ENERGY_OVER_TIME      = "EnergyOverTime"
    COMS_ENERGY_BY_ENTITY      = "EnergyByEntity"
    COMS_TELEMETRY             = "Telemetry"
    
    # Policies & Compliance
    COMS_POLICIES              = "Policies"
    COMS_COMPLIANCE            = "Compliance"
    
    # Events & Alerts
    COMS_EVENTS                = "ComsEvent"
    COMS_ALERTS                = "ComsAlert"
    COMS_WEBHOOKS              = "Webhooks"
    COMS_SUBSCRIPTIONS         = "Subscriptions"
    
    # Power & Control
    COMS_POWER                 = "ComsPower"
    
    # Settings & Configuration
    COMS_SETTINGS              = "Settings"
    COMS_APPLIANCE_FIRMWARE    = "ApplianceFirmware"
