"""
Route Mapper — Dynamic OneView/COMS Endpoint Routing
======================================================
Maps ResourceType enums to REST API endpoint templates.

Architecture:
- Routes are APPLICATION LOGIC (stored in code, not database)
- Supports OneView v1+ APIs with 18 resource types
- Supports COMS v1/v1beta APIs with 28 resource types
- Dynamic endpoint generation without hardcoded URLs
- Extensible for future resource types

Philosophy:
Routes are APPLICATION LOGIC, not infrastructure data.
They belong in code, not the database.
The database only stores: UUID, ResourceType, host, credentials.

Endpoint Generation Pattern:
    base_url + route_template.format(uuid=resource_uuid)
    
Example:
    base_url = "https://oneview.example.com"
    route_template = "/rest/v1/server-hardware/{uuid}"
    uuid = "abc123def456"
    →
    "https://oneview.example.com/rest/v1/server-hardware/abc123def456"

COMS APIs Supported:
- v1beta1: ahs-files, activation-keys, activation-tokens, activities,
           energy metrics, external-services, groups, reports, filters,
           async-operations
- v1beta2: appliances, approval-policy, approval-request, activities,
           job-templates, servers, tasks, jobs, events, alerts,
           webhooks, subscriptions, compliance, power, telemetry
- v1:      settings, appliance-firmware-bundles, async-operations
"""

from __future__ import annotations

import logging
from typing import Optional

from enums import ResourceType, Protocol

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# OneView REST API v1+ Route Templates
# Organized by domain for maintainability and extensibility
# ─────────────────────────────────────────────────────────────────────────────

ONEVIEW_ROUTES: dict[ResourceType, str] = {
    # ─────────────────────────────────────────────────────────────────────────
    # Server Hardware & Provisioning
    # ─────────────────────────────────────────────────────────────────────────
    ResourceType.SERVER_HARDWARE: "/rest/v1/server-hardware/{uuid}",
    ResourceType.SERVER_PROFILE: "/rest/v1/server-profiles/{uuid}",
    ResourceType.SERVER_PROFILE_TEMPLATE: "/rest/v1/server-profile-templates/{uuid}",
    ResourceType.RACK_MANAGER: "/rest/v1/rack-managers/{uuid}",
    
    # ─────────────────────────────────────────────────────────────────────────
    # Networking
    # ─────────────────────────────────────────────────────────────────────────
    ResourceType.ETHERNET_NETWORK: "/rest/v1/ethernet-networks/{uuid}",
    ResourceType.FC_NETWORK: "/rest/v1/fc-networks/{uuid}",
    ResourceType.NETWORK_SET: "/rest/v1/network-sets/{uuid}",
    ResourceType.INTERCONNECT: "/rest/v1/interconnects/{uuid}",
    ResourceType.INTERCONNECT_TYPE: "/rest/v1/interconnect-types/{uuid}",
    ResourceType.UPLINK_SET: "/rest/v1/uplink-sets/{uuid}",
    ResourceType.LOGICAL_INTERCONNECT: "/rest/v1/logical-interconnects/{uuid}",
    ResourceType.LOGICAL_INTERCONNECT_GROUP: "/rest/v1/logical-interconnect-groups/{uuid}",
    ResourceType.INTERNAL_NETWORK: "/rest/v1/internal-networks/{uuid}",
    
    # ─────────────────────────────────────────────────────────────────────────
    # Storage
    # ─────────────────────────────────────────────────────────────────────────
    ResourceType.STORAGE_SYSTEM: "/rest/v1/storage-systems/{uuid}",
    ResourceType.STORAGE_POOL: "/rest/v1/storage-pools/{uuid}",
    ResourceType.VOLUME: "/rest/v1/volumes/{uuid}",
    ResourceType.VOLUME_TEMPLATE: "/rest/v1/volume-templates/{uuid}",
    ResourceType.VOLUME_SNAPSHOT: "/rest/v1/volume-snapshots/{uuid}",
    ResourceType.DRIVE_ENCLOSURE: "/rest/v1/drive-enclosures/{uuid}",
    
    # ─────────────────────────────────────────────────────────────────────────
    # Enclosures & Facilities
    # ─────────────────────────────────────────────────────────────────────────
    ResourceType.ENCLOSURE: "/rest/v1/enclosures/{uuid}",
    ResourceType.ENCLOSURE_GROUP: "/rest/v1/enclosure-groups/{uuid}",
    ResourceType.RACK: "/rest/v1/racks/{uuid}",
    ResourceType.DATACENTER: "/rest/v1/datacenters/{uuid}",
    
    # ─────────────────────────────────────────────────────────────────────────
    # Firmware & Updates
    # ─────────────────────────────────────────────────────────────────────────
    ResourceType.FIRMWARE_DRIVER: "/rest/v1/firmware-drivers/{uuid}",
    ResourceType.FIRMWARE_BUNDLE: "/rest/v1/firmware-bundles/{uuid}",
    
    # ─────────────────────────────────────────────────────────────────────────
    # Tasks, Events & Monitoring
    # ─────────────────────────────────────────────────────────────────────────
    ResourceType.TASK: "/rest/v1/tasks/{uuid}",
    ResourceType.ALERT: "/rest/v1/alerts/{uuid}",
    ResourceType.EVENT: "/rest/v1/events/{uuid}",
    ResourceType.AUDIT_LOG: "/rest/v1/audit-logs/{uuid}",
    
    # ─────────────────────────────────────────────────────────────────────────
    # Security & Authentication
    # ─────────────────────────────────────────────────────────────────────────
    ResourceType.CERTIFICATE: "/rest/v1/certificates/{uuid}",
    ResourceType.USER: "/rest/v1/users/{uuid}",
    ResourceType.ROLE: "/rest/v1/roles/{uuid}",
    ResourceType.LDAP: "/rest/v1/ldap/{uuid}",
    ResourceType.ACTIVE_DIRECTORY: "/rest/v1/active-directory/{uuid}",
    ResourceType.SESSION: "/rest/v1/sessions/{uuid}",
    
    # ─────────────────────────────────────────────────────────────────────────
    # Settings & Configuration
    # ─────────────────────────────────────────────────────────────────────────
    ResourceType.SCOPE: "/rest/v1/scopes/{uuid}",
    ResourceType.SETTING: "/rest/v1/settings/{uuid}",
    ResourceType.VERSION: "/rest/v1/version",
    ResourceType.HEALTH_STATUS: "/rest/v1/health-status",
    
    # ─────────────────────────────────────────────────────────────────────────
    # Appliance Management
    # ─────────────────────────────────────────────────────────────────────────
    ResourceType.APPLIANCE_INFO: "/rest/v1/appliance",
    ResourceType.APPLIANCE_NETWORK: "/rest/v1/appliance/network-interfaces",
    ResourceType.APPLIANCE_LICENSES: "/rest/v1/appliance/licenses",
    ResourceType.APPLIANCE_BACKUP: "/rest/v1/appliance/backup",
    ResourceType.APPLIANCE_RESTART: "/rest/v1/appliance/restart",
    
    # ─────────────────────────────────────────────────────────────────────────
    # Remote Support & Telemetry
    # ─────────────────────────────────────────────────────────────────────────
    ResourceType.REMOTE_SUPPORT: "/rest/v1/remote-support",
    ResourceType.REMOTE_SUPPORT_CONTACTS: "/rest/v1/remote-support/contacts/{uuid}",
    ResourceType.TELEMETRY_STREAMING: "/rest/v1/telemetry-streaming/{uuid}",
    ResourceType.SUPPORT_DUMP: "/rest/v1/support-dump",
    
    # ─────────────────────────────────────────────────────────────────────────
    # Hypervisors
    # ─────────────────────────────────────────────────────────────────────────
    ResourceType.HYPERVISOR_MANAGER: "/rest/v1/hypervisor-managers/{uuid}",
    ResourceType.HYPERVISOR_PROFILE: "/rest/v1/hypervisor-profiles/{uuid}",
    
    # ─────────────────────────────────────────────────────────────────────────
    # Search & Indexing
    # ─────────────────────────────────────────────────────────────────────────
    ResourceType.SEARCH: "/rest/v1/search",
    ResourceType.RESOURCE_INDEX: "/rest/v1/resource-index",
    
    # ─────────────────────────────────────────────────────────────────────────
    # Metrics & Performance
    # ─────────────────────────────────────────────────────────────────────────
    ResourceType.METRICS: "/rest/v1/metrics/{uuid}",
    ResourceType.PERFORMANCE_COUNTERS: "/rest/v1/performance-counters/{uuid}",
    
    # ─────────────────────────────────────────────────────────────────────────
    # Licensing
    # ─────────────────────────────────────────────────────────────────────────
    ResourceType.LICENSE: "/rest/v1/licenses/{uuid}",
    ResourceType.LICENSE_POOL: "/rest/v1/license-pools/{uuid}",
}


# ─────────────────────────────────────────────────────────────────────────────
# COMS (HPE Compute Ops Management) REST API Route Templates
# 
# Note: Routes are ENDPOINT ONLY (no base URL or hostname).
# Note: {uuid} placeholder is used; can be omitted for collection endpoints.
# Full URLs are built by combining: base_url + route_template
# ─────────────────────────────────────────────────────────────────────────────

COMS_ROUTES: dict[ResourceType, str] = {
    # ─────────────────────────────────────────────────────────────────────────
    # Server Resources
    # ─────────────────────────────────────────────────────────────────────────
    ResourceType.SERVER: "/compute-ops-mgmt/v1beta2/servers/{uuid}",
    ResourceType.SERVER_HARDWARE: "/compute-ops-mgmt/v1beta2/servers/{uuid}",  # Fallback
    
    # ─────────────────────────────────────────────────────────────────────────
    # Infrastructure & Appliance Management
    # ─────────────────────────────────────────────────────────────────────────
    ResourceType.COMS_AHS_FILES: "/compute-ops-mgmt/v1beta1/ahs-files/{uuid}",
    ResourceType.COMS_APPLIANCES: "/compute-ops-mgmt/v1beta2/appliances/{uuid}",
    ResourceType.COMS_APPLIANCE_FIRMWARE: "/compute-ops-mgmt/v1/appliance-firmware-bundles/{uuid}",
    ResourceType.COMS_EXTERNAL_SERVICES: "/compute-ops-mgmt/v1beta1/external-services/{uuid}",
    
    # ─────────────────────────────────────────────────────────────────────────
    # Activation & License Management
    # ─────────────────────────────────────────────────────────────────────────
    ResourceType.COMS_ACTIVATION_KEYS: "/compute-ops-mgmt/v1beta1/activation-keys/{uuid}",
    ResourceType.COMS_ACTIVATION_TOKENS: "/compute-ops-mgmt/v1beta1/activation-tokens/{uuid}",
    
    # ─────────────────────────────────────────────────────────────────────────
    # Activities & Audit
    # ─────────────────────────────────────────────────────────────────────────
    ResourceType.COMS_ACTIVITIES: "/compute-ops-mgmt/v1beta2/activities/{uuid}",
    
    # ─────────────────────────────────────────────────────────────────────────
    # Firmware Management
    # ─────────────────────────────────────────────────────────────────────────
    ResourceType.COMS_FIRMWARE_BUNDLES: "/compute-ops-mgmt/v1beta2/firmware-bundles/{uuid}",
    
    # ─────────────────────────────────────────────────────────────────────────
    # Approval & Policies
    # ─────────────────────────────────────────────────────────────────────────
    ResourceType.COMS_APPROVAL_POLICY: "/compute-ops-mgmt/v1beta2/approval-policy/{uuid}",
    ResourceType.COMS_APPROVAL_REQUEST: "/compute-ops-mgmt/v1beta2/approval-request/{uuid}",
    ResourceType.COMS_POLICIES: "/compute-ops-mgmt/v1beta2/policies/{uuid}",
    
    # ─────────────────────────────────────────────────────────────────────────
    # Async Operations & Jobs
    # ─────────────────────────────────────────────────────────────────────────
    ResourceType.COMS_ASYNC_OPS_V1: "/compute-ops-mgmt/v1/async-operations/{uuid}",
    ResourceType.COMS_ASYNC_OPS_V1BETA: "/compute-ops-mgmt/v1beta1/async-operations/{uuid}",
    ResourceType.COMS_JOB_TEMPLATES: "/compute-ops-mgmt/v1beta2/job-templates/{uuid}",
    ResourceType.COMS_JOBS: "/compute-ops-mgmt/v1beta2/jobs/{uuid}",
    
    # ─────────────────────────────────────────────────────────────────────────
    # Groups & Organization
    # ─────────────────────────────────────────────────────────────────────────
    ResourceType.COMS_GROUPS: "/compute-ops-mgmt/v1beta1/groups/{uuid}",
    
    # ─────────────────────────────────────────────────────────────────────────
    # Reporting & Analytics
    # ─────────────────────────────────────────────────────────────────────────
    ResourceType.COMS_REPORTS: "/compute-ops-mgmt/v1beta1/reports/{uuid}",
    ResourceType.COMS_FILTERS: "/compute-ops-mgmt/v1beta1/filters/{uuid}",
    ResourceType.COMS_ENERGY_OVER_TIME: "/compute-ops-mgmt/v1beta1/energy-over-time/{uuid}",
    ResourceType.COMS_ENERGY_BY_ENTITY: "/compute-ops-mgmt/v1beta1/energy-by-entity/{uuid}",
    ResourceType.COMS_TELEMETRY: "/compute-ops-mgmt/v1beta2/telemetry/{uuid}",
    
    # ─────────────────────────────────────────────────────────────────────────
    # Tasks, Events & Alerts
    # ─────────────────────────────────────────────────────────────────────────
    ResourceType.COMS_TASKS: "/compute-ops-mgmt/v1beta2/tasks/{uuid}",
    ResourceType.COMS_EVENTS: "/compute-ops-mgmt/v1beta2/events/{uuid}",
    ResourceType.COMS_ALERTS: "/compute-ops-mgmt/v1beta2/alerts/{uuid}",
    
    # ─────────────────────────────────────────────────────────────────────────
    # Webhooks & Subscriptions
    # ─────────────────────────────────────────────────────────────────────────
    ResourceType.COMS_WEBHOOKS: "/compute-ops-mgmt/v1beta2/webhooks/{uuid}",
    ResourceType.COMS_SUBSCRIPTIONS: "/compute-ops-mgmt/v1beta2/subscriptions/{uuid}",
    
    # ─────────────────────────────────────────────────────────────────────────
    # Compliance & Power Control
    # ─────────────────────────────────────────────────────────────────────────
    ResourceType.COMS_COMPLIANCE: "/compute-ops-mgmt/v1beta2/compliance/{uuid}",
    ResourceType.COMS_POWER: "/compute-ops-mgmt/v1beta2/power/{uuid}",
    
    # ─────────────────────────────────────────────────────────────────────────
    # Settings & Configuration
    # ─────────────────────────────────────────────────────────────────────────
    ResourceType.COMS_SETTINGS: "/compute-ops-mgmt/v1/settings/{uuid}",
}


# ─────────────────────────────────────────────────────────────────────────────
# Default Resource Types per Protocol
# ─────────────────────────────────────────────────────────────────────────────

DEFAULT_RESOURCE_TYPES: dict[Protocol, ResourceType] = {
    Protocol.ONEVIEW: ResourceType.SERVER_HARDWARE,  # Default to server hardware
    Protocol.COMS: ResourceType.SERVER,              # Default to server (COMS)
}


# ─────────────────────────────────────────────────────────────────────────────
# API Versions
# ─────────────────────────────────────────────────────────────────────────────

API_VERSIONS = {
    Protocol.ONEVIEW: {
        "current": 4600,
        "minimum": 2800,
        "header": "X-API-Version",
    },
    Protocol.COMS: {
        "current": 1,
        "minimum": 1,
        "header": "X-COMS-API-Version",
    },
}


# ─────────────────────────────────────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────────────────────────────────────

def get_route_template(resource_type: ResourceType, protocol: Protocol) -> Optional[str]:
    """
    Get the route template for a resource type and protocol.
    
    Parameters
    ----------
    resource_type : ResourceType
        The resource type (e.g., SERVER_HARDWARE, ETHERNET_NETWORK)
    protocol : Protocol
        The protocol (ONEVIEW or COMS)
    
    Returns
    -------
    str or None
        Route template with {uuid} placeholder, or None if not supported
    
    Example:
        >>> get_route_template(ResourceType.SERVER_HARDWARE, Protocol.ONEVIEW)
        "/rest/v1/server-hardware/{uuid}"
    """
    if protocol == Protocol.ONEVIEW:
        route = ONEVIEW_ROUTES.get(resource_type)
        if route:
            logger.debug(f"[RouteMapper] OneView route: {resource_type.value} → {route}")
            return route
        logger.warning(
            f"[RouteMapper] No OneView route for {resource_type.value}"
        )
        return None
    
    if protocol == Protocol.COMS:
        route = COMS_ROUTES.get(resource_type)
        if route:
            logger.debug(f"[RouteMapper] COMS route: {resource_type.value} → {route}")
            return route
        logger.warning(
            f"[RouteMapper] No COMS route for {resource_type.value}"
        )
        return None
    
    raise ValueError(f"Unknown protocol: {protocol}")


def get_default_resource_type(protocol: Protocol) -> ResourceType:
    """
    Get the default resource type for a protocol.
    
    Used when resource type is not explicitly specified.
    """
    return DEFAULT_RESOURCE_TYPES.get(protocol, ResourceType.SERVER_HARDWARE)


def build_endpoint(
    base_url: str,
    resource_type: ResourceType,
    uuid: str,
    protocol: Protocol,
) -> str:
    """
    Build full endpoint URL from base URL, resource type, and UUID.
    
    Parameters
    ----------
    base_url : str
        Base URL (e.g., "https://oneview.example.com" or "http://localhost:8080")
    resource_type : ResourceType
        The resource type
    uuid : str
        The resource UUID. Empty/None for collection endpoints.
    protocol : Protocol
        The protocol (ONEVIEW or COMS)
    
    Returns
    -------
    str
        Full endpoint URL
    
    Example:
        >>> build_endpoint(
        ...     "https://oneview.example.com",
        ...     ResourceType.SERVER_HARDWARE,
        ...     "abc123",
        ...     Protocol.ONEVIEW
        ... )
        "https://oneview.example.com/rest/v1/server-hardware/abc123"
        
    Example (collection):
        >>> build_endpoint(
        ...     "https://coms.example.com",
        ...     ResourceType.SERVER,
        ...     "",  # Empty for collection
        ...     Protocol.COMS
        ... )
        "https://coms.example.com/compute-ops-mgmt/v1beta2/servers"
    """
    # Get route template
    route_template = get_route_template(resource_type, protocol)
    
    if not route_template:
        logger.error(
            f"[RouteMapper] No route template for {resource_type.value} / {protocol.value}"
        )
        # Fallback: use base URL + UUID
        return f"{base_url}/{uuid}" if uuid else base_url
    
    # Build endpoint
    if uuid and uuid.strip():
        # Resource endpoint: replace {uuid} placeholder
        route = route_template.format(uuid=uuid)
    else:
        # Collection endpoint: remove /{uuid} placeholder
        route = route_template.replace("/{uuid}", "")
    
    endpoint = f"{base_url}{route}"
    
    logger.debug(
        f"[RouteMapper] Generated endpoint: {resource_type.value} → {endpoint}"
    )
    
    return endpoint


def get_api_version_header(protocol: Protocol) -> tuple[str, int]:
    """
    Get API version header name and current version for a protocol.
    
    Returns
    -------
    tuple[str, int]
        (header_name, version)
    
    Example:
        >>> get_api_version_header(Protocol.ONEVIEW)
        ("X-API-Version", 4600)
    """
    info = API_VERSIONS.get(protocol)
    if info:
        return info["header"], info["current"]
    return "X-API-Version", 1


def supports_resource_type(
    resource_type: ResourceType,
    protocol: Protocol,
) -> bool:
    """
    Check if a resource type is supported by a protocol.
    
    Parameters
    ----------
    resource_type : ResourceType
    protocol : Protocol
    
    Returns
    -------
    bool
        True if supported, False otherwise
    """
    if protocol == Protocol.ONEVIEW:
        return resource_type in ONEVIEW_ROUTES
    elif protocol == Protocol.COMS:
        return resource_type in COMS_ROUTES
    return False


def list_supported_types(protocol: Protocol) -> list[ResourceType]:
    """
    List all resource types supported by a protocol.
    
    Parameters
    ----------
    protocol : Protocol
    
    Returns
    -------
    list[ResourceType]
    """
    if protocol == Protocol.ONEVIEW:
        return list(ONEVIEW_ROUTES.keys())
    elif protocol == Protocol.COMS:
        return list(COMS_ROUTES.keys())
    return []


def infer_resource_type_from_endpoint(endpoint: str) -> Optional[ResourceType]:
    """
    Infer resource type from endpoint string (for diagnostics).
    
    Not intended for routing — only for analysis/logging.
    """
    endpoint_lower = endpoint.lower()
    
    for resource_type, route in ONEVIEW_ROUTES.items():
        # Extract path component from route template
        path = route.split("/{uuid}")[0]
        if path in endpoint_lower:
            return resource_type
    
    for resource_type, route in COMS_ROUTES.items():
        path = route.split("/{uuid}")[0]
        if path in endpoint_lower:
            return resource_type
    
    return None


def get_protocol_info(protocol: Protocol) -> dict:
    """
    Get protocol metadata (versions, header, etc).
    """
    info = API_VERSIONS.get(protocol, {})
    return {
        "protocol": protocol.value,
        "header": info.get("header", "X-API-Version"),
        "current_version": info.get("current", 1),
        "minimum_version": info.get("minimum", 1),
        "supported_resources": len(list_supported_types(protocol)),
    }
