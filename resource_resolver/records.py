"""Data models for the resource resolver routing pipeline."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from enums import CacheStatus, IdentifierType


@dataclass
class DeviceRecord:
    """Authoritative device-routing record stored in PostgreSQL and Redis."""

    id: str
    serial_number: str
    management_source: str
    ip_address: Optional[str] = None
    fqdn: Optional[str] = None
    source_host: Optional[str] = None
    source_device_id: Optional[str] = None
    device_type: Optional[str] = None
    last_seen: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_row(cls, row: dict) -> "DeviceRecord":
        return cls(
            id=str(row.get("id") or row.get("uuid") or ""),
            serial_number=str(row.get("serial_number") or ""),
            management_source=str(row.get("management_source") or ""),
            ip_address=str(row["ip_address"]) if row.get("ip_address") else None,
            fqdn=str(row["fqdn"]) if row.get("fqdn") else None,
            source_host=str(row["source_host"]) if row.get("source_host") else None,
            source_device_id=(
                str(row["source_device_id"]) if row.get("source_device_id") else None
            ),
            device_type=row.get("device_type"),
            last_seen=row.get("last_seen"),
            created_at=row.get("created_at"),
            updated_at=row.get("updated_at"),
        )

    @staticmethod
    def _serialize_datetime(value: object) -> Optional[str]:
        if not value:
            return None
        if hasattr(value, "isoformat"):
            return value.isoformat()
        return str(value)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "serial_number": self.serial_number,
            "ip_address": self.ip_address,
            "fqdn": self.fqdn,
            "management_source": self.management_source,
            "source_host": self.source_host,
            "source_device_id": self.source_device_id,
            "device_type": self.device_type,
            "last_seen": self._serialize_datetime(self.last_seen),
            "created_at": self._serialize_datetime(self.created_at),
            "updated_at": self._serialize_datetime(self.updated_at),
        }


@dataclass
class RouteResolution:
    """Resolver API result consumed by the MCP orchestrator."""

    identifier: str
    identifier_type: IdentifierType
    device: DeviceRecord
    mcp_tool: str
    credential_ref: Optional[str]
    cache_status: CacheStatus
    resolution_ms: int
    api_endpoint: str
    management_source: str
    resource: dict
    action: dict

    def to_dict(self) -> dict:
        return {
            "identifier": self.identifier,
            "identifier_type": self.identifier_type.value,
            "management_source": self.management_source,
            "source_host": self.device.source_host,
            "mcp_tool": self.mcp_tool,
            "credential_ref": self.credential_ref,
            "cache_status": self.cache_status.value,
            "resolution_ms": self.resolution_ms,
            "api_endpoint": self.api_endpoint,
            "resource": self.resource,
            "action": self.action,
            "device": self.device.to_dict(),
        }

