"""Abstract base class for all storage adapters."""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class BaseStorageAdapter(ABC):
    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Short provider ID: 'dscc' | 'nas' | 's3' | 'mock'."""

    @abstractmethod
    def fetch_capacity(
        self,
        resource_id: str,
        resource_type: str,
        credentials: Dict[str, Any],
        parameters: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Return capacity metrics: total_tb, used_tb, free_tb, utilization_pct."""

    @abstractmethod
    def fetch_performance(
        self,
        resource_id: str,
        resource_type: str,
        credentials: Dict[str, Any],
        parameters: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Return performance metrics: read_iops, write_iops, read_latency_ms, write_latency_ms."""

    @abstractmethod
    def execute_action(
        self,
        resource_id: str,
        resource_type: str,
        action: str,
        credentials: Dict[str, Any],
        parameters: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Execute control-plane action (create_volume, delete_volume, snapshot, resize, etc.)."""

    @abstractmethod
    def discover_arrays(
        self,
        credentials: Dict[str, Any],
        parameters: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """Discover storage arrays/pools. Each dict: {id, name, type, status, capacity_tb}."""

    @abstractmethod
    def health_check(
        self,
        resource_id: str,
        resource_type: str,
        credentials: Dict[str, Any],
        parameters: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Return {"healthy": bool, "detail": str, "checks": dict}."""

    @abstractmethod
    def list_resources(
        self,
        credentials: Dict[str, Any],
        parameters: Dict[str, Any],
        skip: int = 0,
        limit: int = 10,
    ) -> Dict[str, Any]:
        """List managed systems/resources with pagination."""
