"""Abstract base class for all network protocol adapters."""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class BaseNetworkAdapter(ABC):
    """Protocol-agnostic interface for network devices."""

    @property
    @abstractmethod
    def protocol_name(self) -> str:
        """Short protocol identifier: 'snmp' | 'netconf' | 'rest' | 'mock'."""

    @abstractmethod
    def fetch_interface_metrics(
        self,
        device_id: str,
        credentials: Dict[str, Any],
        parameters: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """Return a list of interface metric dicts for the device."""

    @abstractmethod
    def push_config(
        self,
        device_id: str,
        config_payload: Dict[str, Any],
        credentials: Dict[str, Any],
        parameters: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Push configuration to the device. Returns {"result": str, "detail": Any}."""

    @abstractmethod
    def discover_neighbors(
        self,
        device_id: str,
        credentials: Dict[str, Any],
        parameters: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """
        Discover directly connected neighbors (LLDP/CDP).
        Returns list of {"neighbor_id": str, "neighbor_port": str, "local_port": str}.
        """

    @abstractmethod
    def health_check(
        self,
        device_id: str,
        credentials: Dict[str, Any],
        parameters: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Return {"healthy": bool, "detail": str}."""
