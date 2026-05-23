"""
Protocol Selector
==================
Steps 3, 4, and 5 of the resolver spec.

Step 3 — Vendor & Capability Detection
  Reads the resource's vendor field and deployment_type.
  (HPE only)

Step 4 — Action Classification
  Maps the NL query intent to:
    • ActionCategory.OPERATIONAL   (Power / Reboot / Status / …)

Step 5 — Protocol Selection Decision Logic
  Cloud Deployment       → COMS  (HPE Compute Ops API)
  On-Premises Deployment → OneView  (HPE OneView REST API)

Endpoint Generation:
  Uses route_mapper to dynamically construct API endpoints based on:
  - Base host (management_host or ip_address)
  - Resource type (default: SERVER_HARDWARE)
  - UUID
  - Protocol
"""

from __future__ import annotations

import logging
from typing import Optional

from records import (
    Vendor, Protocol, ActionCategory,
    PowerAction, ResourceRecord, DeploymentType,
)
from enums import ResourceType
import route_mapper
from route_mapper import get_default_resource_type
from errors import ActionClassificationError
from protocol_discovery import discover_protocol_for_resource

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# Intent → Action mapping tables
# ─────────────────────────────────────────────────────────────────────────────

_OPERATIONAL_PHRASES: dict[str, PowerAction] = {
    "turn on":   PowerAction.ON,
    "power on":  PowerAction.ON,
    "start":     PowerAction.ON,
    "boot":      PowerAction.ON,
    "bring up":  PowerAction.ON,
    "enable":    PowerAction.ON,
    "turn off":  PowerAction.OFF,
    "power off": PowerAction.OFF,
    "shutdown":  PowerAction.OFF,
    "shut down": PowerAction.OFF,
    "stop":      PowerAction.OFF,
    "halt":      PowerAction.OFF,
    "reboot":    PowerAction.RESET,
    "restart":   PowerAction.RESET,
    "reset":     PowerAction.RESET,
    "cold boot": PowerAction.COLD,
    "cold":      PowerAction.COLD,
    "status":    PowerAction.STATUS,
    "check":     PowerAction.STATUS,
    "ping":      PowerAction.STATUS,
    "state":     PowerAction.STATUS,
}


# ─────────────────────────────────────────────────────────────────────────────
# Public helpers
# ─────────────────────────────────────────────────────────────────────────────

def classify_action(
    query: str,
) -> tuple[ActionCategory, PowerAction]:
    """
    Step 4 — Classify query as Operational and return the specific action.
    Raises ActionClassificationError if unrecognised.
    """
    q = query.lower()

    for phrase, action in sorted(
        _OPERATIONAL_PHRASES.items(),
        key=lambda item: len(item[0]),
        reverse=True,
    ):
        if phrase in q:
            logger.debug(f"[Selector] Operational action: {action.value}")
            return ActionCategory.OPERATIONAL, action

    # Unrecognized query — raise error instead of silently defaulting
    error_msg = (
        f"Could not classify query '{query}' into any action. "
        f"Recognized operational actions: {', '.join(_OPERATIONAL_PHRASES.keys())}"
    )
    logger.error(f"[Selector] {error_msg}")
    raise ActionClassificationError(error_msg)


def select_protocol(
    resource: ResourceRecord,
    category: ActionCategory,
) -> tuple[Protocol, str]:
    """
    Step 5 — Database-driven protocol discovery.
    
    Protocol selection is now determined dynamically from infrastructure metadata
    stored in PostgreSQL, not hardcoded based on deployment_type.
    
    Discovery order:
    1. Query credential vault path for protocol indicators
    2. Query database for protocols associated with IP + credentials
    3. Select primary protocol from supported list
    4. Return protocol with discovery reason
    
    This removes developer hardcoding and makes protocol ownership
    infrastructure-driven (single source of truth: PostgreSQL).
    
    Returns (selected_protocol, reason_string).
    """
    
    logger.info(
        f"[Selector] Step 5 — Protocol Selection for {resource.name} "
        f"({resource.uuid[:8]}…)"
    )
    
    # Use database-driven protocol discovery
    protocol, reason = discover_protocol_for_resource(resource)
    
    logger.info(
        f"[Selector] Protocol selected: {protocol.value} — {reason}"
    )
    
    return protocol, reason


def build_endpoint(
    resource: ResourceRecord,
    protocol: Protocol,
    resource_type: Optional[ResourceType] = None,
) -> str:
    """
    Step 6 (partial) — Dynamically construct endpoint URL.
    
    Uses route_mapper to generate endpoints based on:
    - Protocol (OneView or COMS)
    - Resource type (ServerHardware, Enclosure, etc.)
    - Resource UUID
    - Management host or IP
    
    Parameters
    ----------
    resource : ResourceRecord
        The resource with UUID, host, and metadata
    protocol : Protocol
        The selected protocol (OneView or COMS)
    resource_type : ResourceType, optional
        The resource type. If None, defaults based on protocol.
        For backward compatibility, defaults to ServerHardware/Server.
    
    Returns
    -------
    str
        Full API endpoint URL
    
    Examples
    --------
    OneView Server Hardware:
        Base: https://oneview.example.com
        Route: /rest/v1/server-hardware/{uuid}
        Result: https://oneview.example.com/rest/v1/server-hardware/abc123
    
    COMS Server:
        Base: https://compute-ops.cloud.com
        Route: /compute-ops/v1/servers/{uuid}
        Result: https://compute-ops.cloud.com/compute-ops/v1/servers/xyz789
    """
    # Determine resource type if not specified
    if resource_type is None:
        resource_type = get_default_resource_type(protocol)
        logger.debug(
            f"[Selector] No resource type specified — "
            f"using default: {resource_type.value} for {protocol.value}"
        )
    
    # Get base URL from management_host or fallback to ip_address
    base_host = resource.management_host or resource.ip_address
    
    # Build endpoint using route_mapper
    endpoint = route_mapper.build_endpoint(
        base_url=f"https://{base_host}",
        resource_type=resource_type,
        uuid=resource.uuid,
        protocol=protocol,
    )
    
    logger.info(
        f"[Selector] Built endpoint: {resource.name} [{resource.uuid[:8]}…] "
        f"resource_type={resource_type.value} protocol={protocol.value} "
        f"→ {endpoint[:80]}…"
    )
    
    return endpoint
