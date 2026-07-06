"""
power_ops.py
============
Execution handlers and orchestrator for infrastructure routing.

Endpoint paths are fully registry-driven: all if/elif branching on vendor /
device_type has been removed. The authoritative source for API paths is the
endpoint_registry PostgreSQL table (seeded from oneview_api_prompts.txt and
comops_api_prompts.txt via seed_endpoint_registry.py).
"""
from __future__ import annotations

import logging
import os
from typing import Optional

from records import RouteResolution
from errors import EndpointNotFoundError
from protocol_discovery import normalize_management_source

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Management-source execution handlers
# ---------------------------------------------------------------------------

class GenericHandler:
    """Generic handler for operations on generalized infrastructure."""

    def execute(self, context: dict) -> dict:
        source = context.get("management_source", "UNKNOWN").upper()
        logger.info(
            "[Execution] %s Handler invoking %s %s for action %s",
            source,
            context["http_method"],
            context["api_endpoint"],
            context["action"],
        )
        return {
            "status":       "success",
            "handler":      source,
            "action":       context["action"],
            "http_method":  context["http_method"],
            "api_endpoint": context["api_endpoint"],
        }


# ---------------------------------------------------------------------------
# Execution Orchestrator
# ---------------------------------------------------------------------------


class ExecutionOrchestrator:
    """
    Modular, extensible execution orchestrator for infrastructure routing.

    Endpoint path synthesis is fully registry-driven via EndpointRegistryQueries.
    No hardcoded vendor/device-type if-elif trees remain.
    """

    def __init__(self) -> None:
        self._handlers: dict[str, object] = {}
        self._generic_handler = GenericHandler()

    def register_handler(self, name: str, handler: object) -> None:
        self._handlers[name.lower()] = handler

    # ------------------------------------------------------------------
    # Endpoint resolution — fully DB-driven
    # ------------------------------------------------------------------

    @staticmethod
    def _resolve_endpoint(
        vendor: str,
        action_key: str,
        scheme: str,
        host: str,
        uuid: str,
        device_type: str,
        resource_type: str | None = None,
    ) -> tuple[str, str]:
        """
        Lookup the registry for (vendor, device_type, action_key) and build
        the full URL using the EXACT api_path stored in the DB.

        Only {id} and {uuid} placeholders are substituted at runtime — the
        path itself is preserved verbatim from the vendor API contract.

        Returns (http_method, full_url).  Falls back to a safe generic path
        with a WARNING log when the registry has no matching row so the
        resolver never crashes on a missing entry.
        """
        from db_queries import EndpointRegistryQueries

        meta = EndpointRegistryQueries.get_endpoint(
            vendor=vendor,
            device_type=device_type,
            action_key=action_key,
            resource_type=resource_type,
        )
        http_method = meta["http_method"]
        # Substitute any resource identity placeholders (like {id}, {system_id}, {volume_id})
        # path structure is preserved exactly as defined in the vendor API contract.
        import re
        api_path = re.sub(r'\{[^}]+\}', uuid, meta["api_path"])
        logger.debug(
            "[EndpointRegistry] Resolved | vendor=%s device_type=%s "
            "action=%s method=%s path=%s",
            vendor, meta["device_type"], action_key, http_method, api_path,
        )

        return http_method, f"{scheme}://{host}{api_path}"


    # ------------------------------------------------------------------
    # Context builder (called from resolver.py)
    # ------------------------------------------------------------------

    def build_execution_context(
        self,
        route: RouteResolution,
        action: str,
        category: str,
        resource_type: str | None = None,
        default_source: str | None = None,
        default_device_type: str | None = None,
    ) -> dict:
        """Construct the execution context payload using DB-driven endpoint lookup."""
        device = route.device
        
        # Base URL components
        mock_port = os.getenv("MOCK_AGENT_PORT")
        mock_host = os.getenv("MOCK_AGENT_HOST", "localhost")

        if device:
            source = normalize_management_source(device.management_source)
            if mock_port:
                host   = f"{mock_host}:{mock_port}"
                scheme = "http"
            else:
                host   = device.source_host or "localhost"
                scheme = "https"
            if host and (":" in host or "localhost" in host or "127.0.0.1" in host):
                scheme = "http"

            uuid        = device.source_device_id or device.id
            device_type = (device.device_type or "").strip().lower()
        else:
            # Provisioning operations may not have a device in CMDB yet
            source = default_source or os.getenv("DEFAULT_PROVISIONING_SOURCE")
            if not source:
                raise ValueError(
                    f"Global {action} action requires a management source, but none was provided "
                    "in the route or defaults."
                )

            if mock_port:
                host   = f"{mock_host}:{mock_port}"
                scheme = "http"
            else:
                host   = "localhost"
                scheme = "https"
            uuid = ""
            
            device_type = default_device_type or os.getenv("DEFAULT_PROVISIONING_DEVICE_TYPE")
            if not device_type:
                raise ValueError(
                    f"Global {action} action requires a device_type, but none was provided "
                    "in the route or defaults."
                )

        # ── Registry-driven endpoint synthesis ────────────────────────────────
        http_method, endpoint = self._resolve_endpoint(
            vendor=source,
            action_key=action,
            scheme=scheme,
            host=host,
            uuid=uuid,
            device_type=device_type,
            resource_type=resource_type,
        )
        # ─────────────────────────────────────────────────────────────────────

        return {
            "management_source": source.upper(),
            "source_host":       device.source_host,
            "api_endpoint":      endpoint,
            "http_method":       http_method,
            "action":            action,
            "category":          category,
            "serial_number":     device.serial_number,
            "credential_ref":    route.credential_ref,
            "device_type":       device_type or None,
        }

    # ------------------------------------------------------------------
    # Dispatch
    # ------------------------------------------------------------------
    def execute_operation(self, context: dict) -> dict:
        """Route the operation to the correct registered management source handler or generic handler."""
        source  = context.get("management_source", "").lower()
        
        # Ensure the source is supported based on DB query
        from db_queries import ManagementSourceQueries
        if not ManagementSourceQueries.is_supported(source):
             raise ValueError(
                f"Unsupported management source for execution: {source!r}"
             )

        handler = self._handlers.get(source, self._generic_handler)
        return handler.execute(context)
