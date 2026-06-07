"""PostgreSQL-backed authoritative device registry."""

from __future__ import annotations

from typing import Iterable, Optional

from db_queries import DeviceQueries, PollHistoryQueries, RoutingAuditQueries
from enums import IdentifierType
from records import DeviceRecord


class ResourceRegistry:
    """Exact identifier lookup and source-inventory synchronization."""

    def get_by_identifier(
        self,
        identifier: str,
        identifier_type: IdentifierType,
    ) -> Optional[DeviceRecord]:
        row = DeviceQueries.get_by_identifier(identifier, identifier_type)
        return DeviceRecord.from_row(row) if row else None

    def lookup(
        self,
        identifier: str,
        identifier_type: IdentifierType,
    ) -> Optional[DeviceRecord]:
        return self.get_by_identifier(identifier, identifier_type)

    def register(self, device: dict) -> DeviceRecord:
        """Manual/static registration path using the authoritative database."""
        return DeviceRecord.from_row(DeviceQueries.upsert(device))

    def sync_source(
        self,
        management_source: str,
        source_host: str,
        devices: Iterable[dict],
    ) -> dict:
        return DeviceQueries.sync_source_devices(
            management_source,
            source_host,
            devices,
        )

    def list_all(self, limit: int = 1000, offset: int = 0) -> list[DeviceRecord]:
        return [
            DeviceRecord.from_row(row)
            for row in DeviceQueries.list_all(limit=limit, offset=offset)
        ]

    def list_devices_by_management_source(
        self,
        management_source: str,
        source_host: Optional[str] = None,
    ) -> list[DeviceRecord]:
        return [
            DeviceRecord.from_row(row)
            for row in DeviceQueries.list_devices_by_management_source(management_source, source_host)
        ]

    @staticmethod
    def log_routing_audit(**audit: object) -> None:
        RoutingAuditQueries.log(**audit)

    @staticmethod
    def log_poll_history(result: dict) -> None:
        PollHistoryQueries.log(result)
