"""SNMP network adapter stub — swap snmp_get_bulk with pysnmp or net-snmp in production."""

from __future__ import annotations
from typing import Any, Dict, List

from adapters.base import BaseNetworkAdapter


class SNMPNetworkAdapter(BaseNetworkAdapter):
    @property
    def protocol_name(self) -> str:
        return "snmp"

    def fetch_interface_metrics(self, device_id, credentials, parameters) -> List[Dict[str, Any]]:
        # Stub: replace with pysnmp bulk walk of IF-MIB
        return [{"note": f"[SNMP STUB] fetch_interface_metrics for {device_id}"}]

    def push_config(self, device_id, config_payload, credentials, parameters) -> Dict[str, Any]:
        return {"result": "stub", "detail": "[SNMP STUB] Config push not supported over SNMP."}

    def discover_neighbors(self, device_id, credentials, parameters) -> List[Dict[str, Any]]:
        return [{"note": f"[SNMP STUB] neighbor discovery for {device_id}"}]

    def health_check(self, device_id, credentials, parameters) -> Dict[str, Any]:
        return {"healthy": True, "detail": f"[SNMP STUB] health-check for {device_id}"}
