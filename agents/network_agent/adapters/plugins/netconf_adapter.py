"""Netconf adapter stub — swap with ncclient in production."""

from __future__ import annotations
from typing import Any, Dict, List
from adapters.base import BaseNetworkAdapter


class NetconfNetworkAdapter(BaseNetworkAdapter):
    @property
    def protocol_name(self) -> str:
        return "netconf"

    def fetch_interface_metrics(self, device_id, credentials, parameters) -> List[Dict[str, Any]]:
        return [{"note": f"[NETCONF STUB] fetch_interface_metrics for {device_id}"}]

    def push_config(self, device_id, config_payload, credentials, parameters) -> Dict[str, Any]:
        return {"result": "stub", "detail": f"[NETCONF STUB] Config push for {device_id}."}

    def discover_neighbors(self, device_id, credentials, parameters) -> List[Dict[str, Any]]:
        return [{"note": f"[NETCONF STUB] neighbor discovery for {device_id}"}]

    def health_check(self, device_id, credentials, parameters) -> Dict[str, Any]:
        return {"healthy": True, "detail": f"[NETCONF STUB] health-check for {device_id}"}
