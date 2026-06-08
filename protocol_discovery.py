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
    env_key = f"{source.upper()}_MCP_TOOL"
    default_tool = "compute_ops" if source == "coms" else source
    return os.getenv(env_key, default_tool)


def get_credential_ref(
    management_source: str,
    source_host: Optional[str],
) -> Optional[str]:
    """Return a vault reference without exposing any credential material."""
    source = normalize_management_source(management_source)
    env_key = f"{source.upper()}_CREDENTIAL_REF"
    configured = os.getenv(env_key) or os.getenv("DEFAULT_CREDENTIAL_REF")

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
