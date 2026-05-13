"""
Protocol Selector
==================
Steps 3, 4, and 5 of the resolver spec.

Step 3 — Vendor & Capability Detection
  Reads the resource's vendor field and deployment_type.
  (HPE only)

Step 4 — Action Classification
  Maps the NL query intent to either:
    • ActionCategory.PROVISIONING  (Create / Allocate)
    • ActionCategory.OPERATIONAL   (Power / Reboot / Status / …)

Step 5 — Protocol Selection Decision Logic
  Cloud Deployment       → COMS  (HPE Compute Ops API)
  On-Premises Deployment → OneView  (HPE OneView REST API)
"""

from __future__ import annotations

import logging
from typing import Union

from records import (
    Vendor, Protocol, ActionCategory,
    PowerAction, ProvisionAction,
    ResourceRecord, DeploymentType,
)
from errors import ActionClassificationError

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

_PROVISIONING_PHRASES: dict[str, ProvisionAction] = {
    "create":     ProvisionAction.CREATE,
    "provision":  ProvisionAction.CREATE,
    "allocate":   ProvisionAction.ALLOCATE,
    "deploy":     ProvisionAction.ALLOCATE,
    "deallocate": ProvisionAction.DEALLOCATE,
    "release":    ProvisionAction.DEALLOCATE,
    "delete":     ProvisionAction.DELETE,
    "destroy":    ProvisionAction.DELETE,
    "deprovision":ProvisionAction.DELETE,
}


# ─────────────────────────────────────────────────────────────────────────────
# Public helpers
# ─────────────────────────────────────────────────────────────────────────────

def classify_action(
    query: str,
) -> tuple[ActionCategory, Union[PowerAction, ProvisionAction]]:
    """
    Step 4 — Classify query into Provisioning or Operational and return
    the specific action.  Raises ActionClassificationError if unrecognised.
    """
    q = query.lower()

    for phrase, action in sorted(
        _PROVISIONING_PHRASES.items(),
        key=lambda item: len(item[0]),
        reverse=True,
    ):
        if phrase in q:
            logger.debug(f"[Selector] Provisioning action: {action.value}")
            return ActionCategory.PROVISIONING, action

    for phrase, action in sorted(
        _OPERATIONAL_PHRASES.items(),
        key=lambda item: len(item[0]),
        reverse=True,
    ):
        if phrase in q:
            logger.debug(f"[Selector] Operational action: {action.value}")
            return ActionCategory.OPERATIONAL, action

    # Default: treat unknown queries as a status check
    logger.warning(f"[Selector] Could not classify query '{query}' — defaulting to Status")
    return ActionCategory.OPERATIONAL, PowerAction.STATUS


def select_protocol(
    resource: ResourceRecord,
    category: ActionCategory,
) -> tuple[Protocol, str]:
    """
    Step 5 — Protocol selection decision logic for HPE resources.
    
    Routes based on deployment type:
    - Cloud (Compute Ops)       → COMS protocol
    - On-Premises (OneView)     → ONEVIEW protocol

    Returns (selected_protocol, reason_string).
    """
    
    # ── Cloud Deployment → COMS (Compute Ops API) ────────────────────────────
    if resource.deployment_type == DeploymentType.CLOUD:
        if Protocol.COMS in resource.supported_protocols:
            return Protocol.COMS, (
                f"Cloud deployment detected — COMS selected "
                f"(HPE Compute Ops API for {category.value} actions)"
            )
        raise ActionClassificationError(
            f"Cloud deployment requested for '{resource.name}' "
            f"but COMS is not in its supported protocols: {[p.value for p in resource.supported_protocols]}"
        )

    # ── On-Premises Deployment → ONEVIEW (HPE OneView API) ──────────────────
    if resource.deployment_type == DeploymentType.ON_PREM:
        if Protocol.ONEVIEW in resource.supported_protocols:
            return Protocol.ONEVIEW, (
                f"On-Premises deployment detected — OneView selected "
                f"(HPE OneView REST API for {category.value} actions)"
            )
        raise ActionClassificationError(
            f"On-Premises deployment requested for '{resource.name}' "
            f"but OneView is not in its supported protocols: {[p.value for p in resource.supported_protocols]}"
        )

    raise ActionClassificationError(
        f"Unknown deployment type for '{resource.name}': {resource.deployment_type}"
    )


def build_endpoint(resource: ResourceRecord, protocol: Protocol) -> str:
    """
    Construct the target URL pointing to the local mock server.

    Mock server runs on http://localhost:8000 and mirrors the real
    HPE OneView REST API structure (without the /v1 segment):

      OneView (On-Premises):
        http://localhost:8000/rest/server-hardware/{uuid}

      COMS (Cloud):
        http://localhost:8000/compute-ops/v1/servers/{uuid}
    """

    if protocol == Protocol.ONEVIEW:
        return f"http://localhost:8000/rest/server-hardware/{resource.uuid}"

    if protocol == Protocol.COMS:
        return f"http://localhost:8000/compute-ops/v1/servers/{resource.uuid}"

    # Fallback
    return resource.management_host or resource.ip_address
