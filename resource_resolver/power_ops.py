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
from protocol_discovery import normalize_management_source
from errors import EndpointNotFoundError

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Vendor-agnostic fallback path templates
# Used ONLY when the registry contains no row for (vendor, device_type, action_key).
# These are last-resort safe paths — only {resource} and {id} are substituted.
# ---------------------------------------------------------------------------
_FALLBACK_PATHS: dict[str, str] = {
    "oneview": "/rest/{resource}/{id}",
    "coms":    "/compute-ops-mgmt/v1/{resource}/{id}",
}
_FALLBACK_METHOD = "GET"



# ---------------------------------------------------------------------------
# Management-source execution handlers
# ---------------------------------------------------------------------------


class OneViewHandler:
    """Handler for HPE OneView operations on generalized infrastructure."""

    def execute(self, context: dict) -> dict:
        logger.info(
            "[Execution] OneView Handler invoking %s %s for action %s",
            context["http_method"],
            context["api_endpoint"],
            context["action"],
        )
        return {
            "status":       "success",
            "handler":      "ONEVIEW",
            "action":       context["action"],
            "http_method":  context["http_method"],
            "api_endpoint": context["api_endpoint"],
        }


class ComsHandler:
    """Handler for HPE COMS operations on generalized infrastructure."""

    def execute(self, context: dict) -> dict:
        logger.info(
            "[Execution] COMS Handler invoking %s %s for action %s",
            context["http_method"],
            context["api_endpoint"],
            context["action"],
        )
        return {
            "status":       "success",
            "handler":      "COMS",
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
        self.register_handler("oneview", OneViewHandler())
        self.register_handler("coms",    ComsHandler())

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

        try:
            meta = EndpointRegistryQueries.get_endpoint(
                vendor=vendor,
                device_type=device_type or "server",
                action_key=action_key,
            )
            http_method = meta["http_method"]
            # Substitute only resource identity placeholders — path structure
            # is preserved exactly as defined in the vendor API contract.
            api_path = meta["api_path"].format(id=uuid, uuid=uuid)
            logger.debug(
                "[EndpointRegistry] Resolved | vendor=%s device_type=%s "
                "action=%s method=%s path=%s",
                vendor, meta["device_type"], action_key, http_method, api_path,
            )
        except EndpointNotFoundError:
            # Graceful fallback: generic REST path rather than crashing.
            fallback_tpl = _FALLBACK_PATHS.get(vendor, "/rest/{resource}/{id}")
            api_path     = fallback_tpl.format(
                resource=device_type or "servers", id=uuid
            )
            http_method  = _FALLBACK_METHOD
            logger.warning(
                "[EndpointRegistry] No registry row for vendor=%r device_type=%r "
                "action_key=%r — using fallback path %s",
                vendor, device_type, action_key, api_path,
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
    ) -> dict:
        """Construct the execution context payload using DB-driven endpoint lookup."""
        device = route.device
        source = normalize_management_source(device.management_source)

        # Base URL components
        mock_port = os.getenv("MOCK_AGENT_PORT")
        mock_host = os.getenv("MOCK_AGENT_HOST", "localhost")

        if mock_port:
            host   = f"{mock_host}:{mock_port}"
            scheme = "http"
        else:
            host   = device.source_host 
            if ":" in host or "localhost" in host or "127.0.0.1" in host:
                scheme = "http"
            else:
                scheme = "https"

        uuid        = device.source_device_id or device.id
        device_type = (device.device_type or "").strip().lower()

        # ── Registry-driven endpoint synthesis ────────────────────────────────
        http_method, endpoint = self._resolve_endpoint(
            vendor=source,
            action_key=action,
            scheme=scheme,
            host=host,
            uuid=uuid,
            device_type=device_type,
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
#Just prints the log messages, that's it
    def execute_operation(self, context: dict) -> dict:
        """Route the operation to the correct registered management source handler."""
        source  = context["management_source"].lower()
        handler = self._handlers.get(source)
        if handler is not None:
            return handler.execute(context)
        raise ValueError(
            f"Unsupported management source for execution: {context['management_source']!r}"
        )
