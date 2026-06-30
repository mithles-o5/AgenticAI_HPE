"""Mock network adapter — no hardware required, deterministic for testing.

Routing strategy
----------------
Every method requires an ``api_path`` to be present in *parameters*.  The
orchestrator (MCP server / execution engine) supplies the correct path at
dispatch time.  The adapter never hard-codes URLs so it works equally well for
a single device or a large fleet (bulk list endpoints).

Supported actions → api_path examples
--------------------------------------
fetch_metrics    GET  /network/v1/devices/{id}
                 GET  /monitoring/v1/switches
                 GET  /monitoring/v1/switches/{serial}
push_config      POST /network/v1/devices/{id}/vlans          (VLAN add)
                 POST /monitoring/v1/switches/{serial}/vlan
                 POST /network/v1/devices/{id}/ports/{p}/status
execute_action   POST /network/v1/devices/{id}/power          (ON / OFF)
                 PUT  /network/v1/devices/{id}                (generic)
discover_neighbors GET /network/v1/devices                   (all)
                 GET  /monitoring/v1/switches                 (switches list)
health_check     GET  /network/v1/devices/{id}
                 GET  /monitoring/v1/switches/{serial}
"""

from __future__ import annotations
import logging
from typing import Any, Dict, List, Optional

import httpx

from adapters.base import BaseNetworkAdapter

logger = logging.getLogger(__name__)

_MOCK_NETWORK_BASE = "http://127.0.0.1:8002"


class MockNetworkAdapter(BaseNetworkAdapter):

    @property
    def protocol_name(self) -> str:
        return "mock_network"

    # ── Low-level HTTP caller ─────────────────────────────────────────────────

    def _call(
        self,
        method: str,
        api_path: str,
        resource_id: str,
        payload: dict,
        base_url: str = "",
    ) -> Any:
        """
        Make an HTTP request to the mock network server.

        *api_path* may contain ``{id}``, ``{serial}``, ``{systemId}``, or
        ``{hostId}`` placeholders — all are replaced with *resource_id*.

        Returns parsed JSON (dict or list) on success, or an error dict.
        """
        effective_base = (base_url or _MOCK_NETWORK_BASE).rstrip("/")

        # Strip any accidental duplicate base URL embedded in api_path
        if api_path.startswith("http://") or api_path.startswith("https://"):
            full_url = api_path
        else:
            path = api_path.lstrip("/")
            full_url = f"{effective_base}/{path}"

        # Substitute id placeholders
        for placeholder in ("{id}", "{serial}", "{systemId}", "{hostId}"):
            full_url = full_url.replace(placeholder, resource_id)

        logger.info("[MockNetworkAdapter] %s %s", method.upper(), full_url)

        try:
            resp = httpx.request(
                method.upper(), full_url, json=payload if payload else None, timeout=10.0
            )
            try:
                return resp.json()
            except Exception:
                return {
                    "status_code": resp.status_code,
                    "text": resp.text,
                    "result": "ok" if resp.is_success else "failed",
                }
        except Exception as exc:
            logger.error("[MockNetworkAdapter] request failed: %s", exc)
            return {"result": "failed", "detail": f"Network adapter HTTP error: {exc}"}

    # ── Fallback: try to extract interface-like data from a device record ─────

    @staticmethod
    def _device_to_interfaces(device_data: dict) -> List[Dict[str, Any]]:
        """Convert a flat device record to a list of synthetic interface dicts."""
        interfaces: List[Dict[str, Any]] = []
        ports = device_data.get("ports") or {}
        if isinstance(ports, str):
            import json
            try:
                ports = json.loads(ports)
            except Exception:
                ports = {}
        for port_name, port_status in ports.items():
            interfaces.append({
                "name": port_name,
                "status": port_status if isinstance(port_status, str) else "up",
                "in_octets_per_sec": device_data.get("bandwidth_utilization_percent", 0.0),
                "out_octets_per_sec": device_data.get("bandwidth_utilization_percent", 0.0),
                "in_errors": 0,
                "out_errors": 0,
                "utilization_pct": device_data.get("cpu_utilization_percent", 0.0),
            })
        if not interfaces:
            # Return at least one synthetic interface from device metrics
            interfaces.append({
                "name": device_data.get("name", device_data.get("id", "eth0")),
                "status": device_data.get("health_status", device_data.get("status", "up")).lower(),
                "in_octets_per_sec": 0.0,
                "out_octets_per_sec": 0.0,
                "in_errors": 0,
                "out_errors": 0,
                "utilization_pct": device_data.get("cpu_utilization_percent", 0.0),
                "power_state": device_data.get("power_state", "ON"),
                "temperature_celsius": device_data.get("temperature_celsius"),
                "memory_utilization_percent": device_data.get("memory_utilization_percent"),
            })
        return interfaces

    # ── Public adapter interface ──────────────────────────────────────────────

    def fetch_interface_metrics(
        self,
        device_id: str,
        credentials: dict,
        parameters: dict,
    ) -> List[Dict[str, Any]]:
        """
        Fetch interface / port metrics for one device OR a fleet.

        Parameters
        ----------
        parameters["api_path"]   : Required. e.g. ``/network/v1/devices/{id}``
                                   or ``/monitoring/v1/switches``
        parameters["http_method"]: Optional (default GET)
        """
        api_path = parameters.get("api_path")
        if not api_path:
            return [{
                "result": "failed",
                "detail": "No api_path in parameters. The orchestrator must supply it.",
            }]

        raw = self._call(
            parameters.get("http_method", "GET"),
            api_path,
            device_id,
            parameters.get("payload", {}),
            parameters.get("base_url", ""),
        )

        # Normalise: we always return a list of interface-like dicts
        if isinstance(raw, list):
            return raw
        if isinstance(raw, dict):
            # Bulk switch list → flatten
            if "switches" in raw:
                return raw["switches"]
            if "items" in raw:
                return raw["items"]
            if "members" in raw:
                return raw["members"]
            # Single device record — synthesise interface list
            return self._device_to_interfaces(raw)
        return [{"result": "failed", "detail": f"Unexpected response type: {type(raw)}"}]

    def push_config(
        self,
        device_id: str,
        config_payload: dict,
        credentials: dict,
        parameters: dict,
    ) -> Dict[str, Any]:
        """
        Push a configuration change (VLAN, port status, etc.).

        parameters["api_path"]    : Required. e.g. ``/network/v1/devices/{id}/vlans``
        parameters["http_method"] : Optional (default POST)
        parameters["payload"]     : The config body to POST/PUT
        """
        api_path = parameters.get("api_path")
        if not api_path:
            return {
                "result": "failed",
                "detail": "No api_path in parameters. The orchestrator must supply it.",
            }

        body = parameters.get("payload") or config_payload or {}
        result = self._call(
            parameters.get("http_method", "POST"),
            api_path,
            device_id,
            body,
            parameters.get("base_url", ""),
        )
        if isinstance(result, dict):
            return result
        return {"result": "ok", "data": result}

    def execute_action(
        self,
        device_id: str,
        action: str,
        credentials: dict,
        parameters: dict,
    ) -> Dict[str, Any]:
        """
        Execute a control action on a network device (power ON/OFF, bounce port, etc.).

        Power actions (ON / OFF)
        ~~~~~~~~~~~~~~~~~~~~~~~~
        The preferred endpoint is ``POST /network/v1/devices/{id}/power`` with body
        ``{"action": "ON"}`` or ``{"action": "OFF"}``.

        If the orchestrator supplies a different ``api_path`` (e.g. a bulk path),
        that path is used instead.

        parameters["api_path"]    : Required.
        parameters["http_method"] : Optional (default POST for power, PUT otherwise)
        parameters["payload"]     : Optional body override
        parameters["action_verb"] : The verb from the task planner (on/off/reset …)
        """
        api_path = parameters.get("api_path")
        if not api_path:
            return {
                "result": "failed",
                "detail": "No api_path in parameters. The orchestrator must supply it.",
            }

        action_verb = (parameters.get("action_verb") or action or "").upper()

        # ── Power actions ─────────────────────────────────────────────────────
        if action_verb in {"ON", "OFF", "POWERON", "POWEROFF", "POWER_ON", "POWER_OFF"}:
            normalized_action = "ON" if action_verb in {"ON", "POWERON", "POWER_ON"} else "OFF"

            # Build the power endpoint if not already specific
            if "/power" not in api_path:
                # Derive from whatever api_path was given (strip trailing slashes)
                base_path = api_path.rstrip("/").replace("/{id}", "").replace(
                    f"/{device_id}", ""
                )
                # Use the preferred power sub-route
                power_path = f"{base_path}/{{id}}/power"
                logger.info(
                    "[MockNetworkAdapter] Overriding api_path → %s (power action)", power_path
                )
                api_path = power_path

            body = parameters.get("payload") or {"action": normalized_action}
            result = self._call(
                parameters.get("http_method", "POST"),
                api_path,
                device_id,
                body,
                parameters.get("base_url", ""),
            )
            if isinstance(result, dict):
                return result
            return {"result": "ok", "data": result}

        # ── Generic action (port bounce, etc.) ────────────────────────────────
        body = parameters.get("payload", {})
        result = self._call(
            parameters.get("http_method", "PUT"),
            api_path,
            device_id,
            body,
            parameters.get("base_url", ""),
        )
        if isinstance(result, dict):
            return result
        return {"result": "ok", "data": result}

    def discover_neighbors(
        self,
        device_id: str,
        credentials: dict,
        parameters: dict,
    ) -> List[Dict[str, Any]]:
        """
        Discover neighbours / topology peers.

        For a single device use ``/network/v1/devices/{id}``.
        For a fleet   use ``/network/v1/devices`` or ``/monitoring/v1/switches``.
        """
        api_path = parameters.get("api_path")
        if not api_path:
            return [{
                "result": "failed",
                "detail": "No api_path in parameters. The orchestrator must supply it.",
            }]

        raw = self._call(
            parameters.get("http_method", "GET"),
            api_path,
            device_id,
            parameters.get("payload", {}),
            parameters.get("base_url", ""),
        )

        if isinstance(raw, list):
            return raw
        if isinstance(raw, dict):
            for key in ("members", "items", "switches", "aps", "gateways"):
                if key in raw:
                    return raw[key]
            # Single device — wrap it
            return [raw]
        return [{"result": "failed", "detail": f"Unexpected response: {raw}"}]

    def health_check(
        self,
        device_id: str,
        credentials: dict,
        parameters: dict,
    ) -> Dict[str, Any]:
        """
        Health check for one device or an entire fleet.

        Returns a dict with at least ``{"healthy": bool}``.
        """
        api_path = parameters.get("api_path")
        if not api_path:
            return {
                "result": "failed",
                "detail": "No api_path in parameters. The orchestrator must supply it.",
            }

        raw = self._call(
            parameters.get("http_method", "GET"),
            api_path,
            device_id,
            parameters.get("payload", {}),
            parameters.get("base_url", ""),
        )

        if isinstance(raw, dict):
            # Normalise health status
            health_status = (
                raw.get("health_status")
                or raw.get("status")
                or raw.get("health", "")
            ).upper()
            power_state = raw.get("power_state", "ON")
            healthy = health_status not in {"CRITICAL", "FAILED", "ERROR", "DEGRADED", ""} or health_status == "OK"
            if power_state == "OFF":
                healthy = False
            return {
                "healthy": healthy,
                "health_status": health_status or "UNKNOWN",
                "power_state": power_state,
                "detail": raw,
            }

        # Bulk response (list of switches etc.)
        if isinstance(raw, list):
            all_healthy = all(
                (d.get("health_status", d.get("status", "OK")).upper()
                 not in {"CRITICAL", "FAILED", "ERROR", "DEGRADED"})
                for d in raw
            )
            return {
                "healthy": all_healthy,
                "device_count": len(raw),
                "detail": raw,
            }

        return {"healthy": False, "detail": str(raw)}
