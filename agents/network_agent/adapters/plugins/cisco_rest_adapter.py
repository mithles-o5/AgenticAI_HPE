"""Cisco REST adapter stub — replace with Cisco DNA Center / RESTCONF calls in production."""

from __future__ import annotations
from typing import Any, Dict, List
from adapters.base import BaseNetworkAdapter


class CiscoRESTNetworkAdapter(BaseNetworkAdapter):
    @property
    def protocol_name(self) -> str:
        return "rest"

    def fetch_interface_metrics(self, device_id, credentials, parameters) -> List[Dict[str, Any]]:
        return [{"note": f"[REST STUB] fetch_interface_metrics for {device_id}"}]

    def push_config(self, device_id, config_payload, credentials, parameters) -> Dict[str, Any]:
        return {"result": "stub", "detail": f"[REST STUB] Config push for {device_id}."}

    def discover_neighbors(self, device_id, credentials, parameters) -> List[Dict[str, Any]]:
        return [{"note": f"[REST STUB] neighbor discovery for {device_id}"}]

    def health_check(self, device_id, credentials, parameters) -> Dict[str, Any]:
        return {"healthy": True, "detail": f"[REST STUB] health-check for {device_id}"}
