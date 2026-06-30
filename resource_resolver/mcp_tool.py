"""MCP entry point for the resource resolver."""

from __future__ import annotations

import json
import logging
import os
import sys

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, THIS_DIR)

_log_path = os.path.join(THIS_DIR, "resolver.log")
_handler = logging.FileHandler(_log_path, encoding="utf-8")
_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)-8s %(name)s: %(message)s"))
logging.root.addHandler(_handler)
logging.root.setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)

from mcp.server.fastmcp import FastMCP

from cache import ResourceCache
from db_loader import load_registry_from_db
from db_queries import DeviceQueries, get_statistics
from errors import ResolverError, UnsupportedManagementSourceError, InvalidCMDBRecordError
from resolver import ResourceResolver
from query_agent import QueryAgent, parse_query_hybrid


logger.info("Starting resource resolver with PostgreSQL registry and Memurai cache")
_registry = load_registry_from_db()
_cache = ResourceCache()
_resolver = ResourceResolver(registry=_registry, cache=_cache)

mcp = FastMCP("resource-resolver")


@mcp.tool()
def resolve_resource(
    query: str,
    identifier_type: str = "",
    requested_by: str = "mcp-orchestrator",
    user_identity: str = "",
    user_role: str = "",
) -> str:
    """
    Resolve a natural language query for a device IP, serial number, or FQDN 
    to the owning management source and execution routing context.
    """
    identifier = query
    try:
        # 1. NLP preprocessing and classification belongs ONLY to QueryAgent
        parsed_payload = parse_query_hybrid(query)
        identifier = parsed_payload.get("identifier", query)

        # 2. Resource Resolver handles deterministic routing resolution
        result = _resolver.resolve(
            parsed_payload=parsed_payload,
            identifier_type=identifier_type or None,
            requested_by=requested_by,
            user_identity=user_identity or None,
            user_role=user_role or None,
        )
        payload = {"status": "resolved", **result.to_dict()}
        return json.dumps(payload, indent=2)
    except UnsupportedManagementSourceError as exc:
        logger.warning("resolve_resource unsupported management source: %s", exc)
        return json.dumps(
            {
                "status": "error",
                "error_code": "UNSUPPORTED_MANAGEMENT_SOURCE",
                "management_source": exc.management_source,
            },
            indent=2,
        )
    except InvalidCMDBRecordError as exc:
        logger.warning("resolve_resource invalid CMDB record: %s", exc)
        return json.dumps(
            {
                "status": "error",
                "error_code": "INVALID_CMDB_RECORD",
                "error": str(exc),
            },
            indent=2,
        )
    except ResolverError as exc:
        logger.warning("resolve_resource error: %s", exc)
        return json.dumps(
            {
                "status": "error",
                "identifier": identifier,
                "identifier_type": identifier_type,
                "error": str(exc),
            },
            indent=2,
        )
    except Exception as exc:
        logger.exception("resolve_resource unexpected error")
        return json.dumps(
            {
                "status": "error",
                "identifier": identifier,
                "identifier_type": identifier_type,
                "error": str(exc),
            },
            indent=2,
        )



@mcp.tool()
def list_devices(page: int = 1, page_size: int = 50, device_type: str = "") -> str:
    """
    List known devices from the resolver registry.
    Use the device_type parameter to perform bulk enumeration or category-level queries (like 'gateway', 'switch', 'access_point', 'server').
    """
    page = max(page, 1)
    if page_size < 1 or page_size > 500:
        page_size = 50
    offset = (page - 1) * page_size
    total_count = DeviceQueries.count_total(device_type=device_type)
    rows = DeviceQueries.list_all(limit=page_size, offset=offset, device_type=device_type)
    total_pages = (total_count + page_size - 1) // page_size

    return json.dumps(
        {
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total": total_count,
                "total_pages": total_pages,
                "has_next": page < total_pages,
                "has_prev": page > 1,
            },
            "devices": [dict(row) for row in rows],
        },
        indent=2,
        default=str,
    )


@mcp.tool()
def manual_register_device(
    serial_number: str,
    management_source: str,
    source_host: str,
    ip_address: str = "",
    fqdn: str = "",
    source_device_id: str = "",
    device_type: str = "",
) -> str:
    """Manual registration escape hatch for devices missing from polling."""
    try:
        device = _registry.register(
            {
                "serial_number": serial_number,
                "ip_address": ip_address or None,
                "fqdn": fqdn or None,
                "management_source": management_source,
                "source_host": source_host,
                "source_device_id": source_device_id or None,
                "device_type": device_type or None,
            }
        )
        _cache.put_device(device)
        return json.dumps(
            {
                "status": "registered",
                "device": device.to_dict(),
            },
            indent=2,
        )
    except Exception as exc:
        logger.exception("manual_register_device failed")
        return json.dumps({"status": "error", "error": str(exc)}, indent=2)


@mcp.tool()
def cache_stats() -> str:
    """Return Memurai cache key counts for resolver hot-cache monitoring."""
    return json.dumps({"status": "ok", "cache": _cache.stats()}, indent=2)


@mcp.tool()
def resolver_statistics() -> str:
    """Return PostgreSQL registry, routing-audit, and poll-history statistics."""
    return json.dumps({"status": "ok", "statistics": get_statistics()}, indent=2, default=str)


if __name__ == "__main__":
    logger.info("Resource Resolver MCP server starting")
    
    # Start background polling loop
    from polling_engine import start_background_polling
    poll_interval = int(os.getenv("POLL_INTERVAL_SECONDS", "600"))
    start_background_polling(_cache, poll_interval)
    
    mcp.run()
