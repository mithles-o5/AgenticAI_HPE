"""Abstract base class for all cloud provider adapters.

Every adapter plugin (AWS, Azure, GCP, mock, …) must subclass BaseCloudAdapter
and implement the four abstract methods. The Cloud Agent core never calls
provider-specific APIs directly — it always goes through this interface.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class BaseCloudAdapter(ABC):
    """Protocol-agnostic adapter interface for cloud providers."""

    # ── Adapter identity ──────────────────────────────────────────────────────
    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Short, stable identifier for this provider (e.g. 'aws', 'gcp')."""

    # ── Core operations ───────────────────────────────────────────────────────

    @abstractmethod
    def fetch_metrics(
        self,
        resource_id: str,
        resource_type: str,
        region: Optional[str],
        credentials: Dict[str, Any],
        parameters: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Fetch observability metrics for the target resource.

        Returns a flat dict of metric name → value.
        All values must be JSON-serialisable primitives (str, int, float, bool).
        """

    @abstractmethod
    def execute_action(
        self,
        resource_id: str,
        resource_type: str,
        region: Optional[str],
        action: str,
        credentials: Dict[str, Any],
        parameters: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Execute a control-plane operation (start, stop, resize, etc.).

        Returns a dict with at least {"result": <str>, "detail": <Any>}.
        """

    @abstractmethod
    def discover_resources(
        self,
        region: Optional[str],
        resource_type: str,
        credentials: Dict[str, Any],
        parameters: Dict[str, Any],
    ) -> list[Dict[str, Any]]:
        """
        Discover and enumerate resources of the given type in the target region.

        Returns a list of resource descriptor dicts. Each dict must contain
        at minimum: {"id": str, "name": str, "type": str, "status": str}.
        """

    @abstractmethod
    def health_check(
        self,
        resource_id: str,
        resource_type: str,
        region: Optional[str],
        credentials: Dict[str, Any],
        parameters: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Return the health status of the target resource.

        Returns a dict with at least: {"healthy": bool, "detail": str}.
        """
