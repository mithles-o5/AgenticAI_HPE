"""
MCP Server Entry Point — Resource Resolver
============================================
Run by Claude Desktop via:
  command : D:/Resource Resolver/.venv/Scripts/python.exe
  args    : ["D:/Resource Resolver/mcp_tool.py"]

Exposes two tools to Claude:
  1. resolve_resource(query, uuid_hint)
  2. list_servers()

CRITICAL: Nothing must print to stdout — MCP uses stdio JSON transport.
          All logs go to resolver.log only.
"""

from __future__ import annotations

import json
import logging
import os
import sys

# ── path: ensure flat files are importable ────────────────────────────────────
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, THIS_DIR)

# ── logging → FILE ONLY, never stdout ────────────────────────────────────────
_log_path = os.path.join(THIS_DIR, "resolver.log")
_handler  = logging.FileHandler(_log_path, encoding="utf-8")
_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)-8s %(name)s: %(message)s"))
logging.root.addHandler(_handler)
logging.root.setLevel(logging.INFO)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("requests").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# ── imports ───────────────────────────────────────────────────────────────────
from mcp.server.fastmcp import FastMCP

from cache       import ResourceCache
from sample_data import load_sample_registry
from resolver    import ResourceResolver
from errors      import ResolverError

# ── singletons (built once at startup) ───────────────────────────────────────
_registry = load_sample_registry()
_cache    = ResourceCache(ttl=300)
_resolver = ResourceResolver(registry=_registry, cache=_cache)

# ── MCP server ────────────────────────────────────────────────────────────────
mcp = FastMCP("resource-resolver")


# ─────────────────────────────────────────────────────────────────────────────
# Tool 1 — resolve_resource
# ─────────────────────────────────────────────────────────────────────────────

@mcp.tool()
def resolve_resource(query: str, uuid_hint: str = "") -> str:
    """
    Resolve a natural language datacenter command into a full execution context.

    Examples:
      "turn on rack-server-04"
      "reboot synergy-compute-03"
      "power off dell-07"
      "allocate synergy03"
      "status ipmi-node-11"
      "cold boot blade-enclosure-01"

    Returns full resource details: UUID, vendor, protocol, endpoint,
    credential reference, metadata, hardware state, and action classification.

    Parameters
    ----------
    query     : Natural language command
    uuid_hint : Optional UUID to skip fuzzy matching
    """
    try:
        ctx     = _resolver.resolve(query, uuid_hint=uuid_hint)
        payload = _build_payload(ctx)
        logger.info(
            f"resolve_resource OK — "
            f"{payload['resource']['name']} | "
            f"{payload['action']['action']} | "
            f"{payload['protocol_selection']['selected']}"
        )
        return json.dumps(payload, indent=2)

    except ResolverError as exc:
        logger.warning(f"resolve_resource error: {exc}")
        return json.dumps({"status": "error", "error": str(exc), "query": query}, indent=2)
    except Exception as exc:
        logger.exception("resolve_resource unexpected error")
        return json.dumps({"status": "error", "error": str(exc), "query": query}, indent=2)


# ─────────────────────────────────────────────────────────────────────────────
# Tool 2 — list_servers
# ─────────────────────────────────────────────────────────────────────────────

@mcp.tool()
def list_servers() -> str:
    """
    List all servers registered in the Resource Resolver.

    Returns name, UUID, vendor, protocols, model, location,
    power state, health, owner, and aliases for every server.
    """
    servers = []
    for r in _registry.all_records():
        servers.append({
            "name":                r.name,
            "uuid":                r.uuid,
            "aliases":             r.aliases,
            "vendor":              r.vendor.value,
            "supported_protocols": [p.value for p in r.supported_protocols],
            "model":               r.model,
            "serial":              r.serial,
            "location":            r.location,
            "enclosure":           r.enclosure,
            "bay":                 r.bay,
            "owner":               r.owner,
            "tags":                r.tags,
            "power_state":         r.power_state,
            "health":              r.health.value,
            "ip_address":          r.ip_address,
            "management_host":     r.management_host,
            "firmware":            r.firmware,
        })

    logger.info(f"list_servers — returned {len(servers)} records")
    return json.dumps({"total": len(servers), "servers": servers}, indent=2)


# ─────────────────────────────────────────────────────────────────────────────
# Payload builder
# ─────────────────────────────────────────────────────────────────────────────

def _build_payload(ctx) -> dict:
    record = (
        _cache.get_by_uuid(ctx.resource_uuid)[0]
        or _registry.get_by_uuid(ctx.resource_uuid)
    )

    payload = {
        "status":     "resolved",
        "request_id": ctx.request_id,

        # ── PRIMARY: API ENDPOINT URL (Top-level for prominence) ──────────────
        "api_endpoint": ctx.endpoint,
        "protocol":     ctx.selected_protocol.value,
        "api_type":     f"HPE {ctx.selected_protocol.value}",

        # ── Resource Identity ─────────────────────────────────────────────────
        "resource": {
            "name":    ctx.resource_name,
            "uuid":    ctx.resource_uuid,
            "aliases": record.aliases if record else [],
            "vendor":  ctx.vendor.value,
            "owner":   record.owner if record else None,
        },

        # ── Action & Protocol Decision ────────────────────────────────────────
        "action": {
            "category": ctx.action_category.value,
            "action":   ctx.action.value if hasattr(ctx.action, "value") else str(ctx.action),
        },

        "protocol_selection": {
            "selected": ctx.selected_protocol.value,
            "reason":   ctx.protocol_reason,
            "supported_protocols": [p.value for p in record.supported_protocols] if record else [],
        },

        # ── Credentials ───────────────────────────────────────────────────────
        "credentials": {
            "vault_path": ctx.credential_ref.vault_path if ctx.credential_ref else None,
            "auth_type":  ctx.credential_ref.auth_type if ctx.credential_ref else None,
            "username":   ctx.credential_ref.username if ctx.credential_ref else None,
        },

        # ── Hardware Details ──────────────────────────────────────────────────
        "hardware": {
            "model":    record.model if record else None,
            "serial":   record.serial if record else None,
            "firmware": record.firmware if record else None,
            "asset_tag": record.asset_tag if record else None,
            "tags":     record.tags if record else [],
        },

        # ── Current State ─────────────────────────────────────────────────────
        "state": {
            "power_state": record.power_state if record else None,
            "health":      record.health.value if record else None,
            "etag":        record.etag if record else None,
        },

        # ── Resolution Info ───────────────────────────────────────────────────
        "resolution": {
            "query":        ctx.query,
            "resolved_by":  ctx.resolved_by,
            "cache_status": ctx.cache_status.value,
        },
    }

    return payload


# ─────────────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    logger.info("Resource Resolver MCP server starting")
    mcp.run()
