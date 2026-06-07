"""Management-source routing helpers for the resource resolver."""

from __future__ import annotations

import os
from typing import Optional


def normalize_management_source(source: str) -> str:
    """Return the canonical management-source name used by routing."""
    normalized = (source or "").strip().lower()
    if normalized == "oneview":
        return "oneview"
    if normalized in {"com", "coms", "compute-ops", "compute_ops"}:
        return "coms"
    if normalized == "manual":
        return "manual"
    if normalized == "static":
        return "static"
    return (source or "").strip()


def get_mcp_tool_target(management_source: str) -> str:
    """Map a management source to the MCP tool the orchestrator should invoke."""
    source = normalize_management_source(management_source)
    if source == "oneview":
        return os.getenv("ONEVIEW_MCP_TOOL", "oneview")
    if source == "coms":
        return os.getenv("COMS_MCP_TOOL", "compute_ops")
    if source == "manual":
        return os.getenv("MANUAL_MCP_TOOL", "manual_resource")
    if source == "static":
        return os.getenv("STATIC_MCP_TOOL", "static_resource")
    return os.getenv("DEFAULT_MCP_TOOL", source)


def get_credential_ref(
    management_source: str,
    source_host: Optional[str],
) -> Optional[str]:
    """Return a vault reference without exposing any credential material."""
    source = normalize_management_source(management_source)
    if source == "oneview":
        configured = os.getenv("ONEVIEW_CREDENTIAL_REF")
    elif source == "coms":
        configured = os.getenv("COMS_CREDENTIAL_REF")
    elif source == "manual":
        configured = os.getenv("MANUAL_CREDENTIAL_REF")
    else:
        configured = os.getenv("DEFAULT_CREDENTIAL_REF")

    if configured:
        return configured.format(source_host=source_host or "")
    return None



def discover_route(
    management_source: str,
    source_host: Optional[str],
) -> tuple[str, Optional[str]]:
    """Return the MCP tool target and credential reference for a device."""
    return (
        get_mcp_tool_target(management_source),
        get_credential_ref(management_source, source_host),
    )
