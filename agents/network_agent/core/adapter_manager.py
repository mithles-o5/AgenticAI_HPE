"""Network AdapterManager — selects the correct protocol adapter by label."""

from __future__ import annotations
from typing import Dict, Type

from adapters.base import BaseNetworkAdapter
from adapters.plugins.mock_adapter import MockNetworkAdapter
from adapters.plugins.snmp_adapter import SNMPNetworkAdapter
from adapters.plugins.netconf_adapter import NetconfNetworkAdapter
from adapters.plugins.cisco_rest_adapter import CiscoRESTNetworkAdapter

REGISTRY: Dict[str, Type[BaseNetworkAdapter]] = {
    "mock":         MockNetworkAdapter,
    "mock_network": MockNetworkAdapter,
    "snmp":         SNMPNetworkAdapter,
    "netconf": NetconfNetworkAdapter,
    "rest":    CiscoRESTNetworkAdapter,
}


class NetworkAdapterManager:
    @staticmethod
    def get(protocol: str) -> BaseNetworkAdapter:
        key = protocol.strip().lower()
        cls = REGISTRY.get(key)
        if cls is None:
            raise ValueError(f"No adapter for protocol '{protocol}'. Known: {sorted(REGISTRY)}")
        return cls()

    @staticmethod
    def registered_protocols() -> list[str]:
        return sorted(REGISTRY.keys())
