"""Memurai hot cache for resource resolver routing."""

from __future__ import annotations

import json
import logging
import os
from datetime import datetime
from collections.abc import Iterable
from typing import Optional

import redis

from enums import CacheStatus, IdentifierType
from records import DeviceRecord
from protocol_discovery import normalize_management_source

logger = logging.getLogger(__name__)

DEFAULT_TTL = 900


class ResourceCache:
    """Memurai cache using the architecture-defined resolver keyspace."""

    def __init__(
        self,
        ttl: int = int(os.getenv("CACHE_TTL", str(DEFAULT_TTL))),
        host: str = os.getenv("MEMURAI_HOST", os.getenv("REDIS_HOST", "localhost")),
        port: int = int(os.getenv("MEMURAI_PORT", os.getenv("REDIS_PORT", "6379"))),
        db: int = int(os.getenv("MEMURAI_DB", os.getenv("REDIS_DB", "0"))),
        password: str | None = os.getenv("MEMURAI_PASSWORD", os.getenv("REDIS_PASSWORD")),
    ) -> None:
        self._ttl = ttl
        self._client = redis.Redis(
            host=host,
            port=port,
            db=db,
            password=password,
            decode_responses=True,
            socket_connect_timeout=5,
            socket_keepalive=True,
            health_check_interval=30,
        )
        self._connected = True
        try:
            self._client.ping()
            logger.info("[Cache] Memurai connected at %s:%s/db=%s ttl=%ss", host, port, db, ttl)
        except redis.exceptions.ConnectionError as e:
            self._connected = False
            logger.warning("[Cache] Memurai connection failed: %s. Cache disabled.", e)

    @staticmethod
    def key(identifier_type: IdentifierType, identifier: str) -> str:
        return f"resolver:{identifier_type.value}:{identifier.lower()}"

    @staticmethod
    def source_key(device: DeviceRecord) -> str:
        source = normalize_management_source(device.management_source)
        if source == "coms":
            device_id = device.source_device_id or device.id or "unknown"
            return f"resolver:source:coms:{device_id}"
        host = device.source_host or "unknown"
        return f"resolver:source:{host}"

    @staticmethod
    def poll_key(source_type: str, source_host: str, source_device_id: str | None = None) -> str:
        source = normalize_management_source(source_type)
        if source == "coms":
            device_id = source_device_id or source_host or "unknown"
            return f"resolver:poll:coms:{device_id}"
        return f"resolver:poll:{source_host}"

    def put_device(self, device: DeviceRecord) -> None:
        """Store lookup keys and source membership for one device in Memurai using pipelines."""
        if not getattr(self, "_connected", True): return
        payload_data = {
            "management_source": normalize_management_source(device.management_source),
            "source_host": device.source_host,
            "serial_number": device.serial_number,
            "fqdn": device.fqdn,
            "ip_address": device.ip_address,
            "id": device.id,
            "source_device_id": device.source_device_id,
            "device_type": device.device_type,
            "last_seen": device._serialize_datetime(device.last_seen) if device.last_seen else None,
            "created_at": device._serialize_datetime(device.created_at) if device.created_at else None,
            "updated_at": device._serialize_datetime(device.updated_at) if device.updated_at else None,
        }
        payload = json.dumps(payload_data)

        # Pipeline write optimization to reduce round-trips
        pipe = self._client.pipeline()
        if device.ip_address:
            pipe.setex(self.key(IdentifierType.IP, device.ip_address), self._ttl, payload)
        if device.serial_number:
            pipe.setex(
                self.key(IdentifierType.SERIAL_NUMBER, device.serial_number),
                self._ttl,
                payload,
            )
        if device.fqdn:
            pipe.setex(self.key(IdentifierType.FQDN, device.fqdn), self._ttl, payload)
        if device.serial_number:
            source_key = self.source_key(device)
            pipe.sadd(source_key, device.serial_number)
            pipe.expire(source_key, self._ttl)
        pipe.execute()

    def get_by_identifier(
        self,
        identifier: str,
        identifier_type: IdentifierType,
    ) -> tuple[Optional[DeviceRecord], CacheStatus]:
        if not getattr(self, "_connected", True): return None, CacheStatus.MISS
        try:
            raw = self._client.get(self.key(identifier_type, identifier))
            if not raw:
                return None, CacheStatus.MISS
            return self._deserialize_device(raw), CacheStatus.HIT
        except Exception as exc:
            logger.warning("[Cache] Lookup failed for %s:%s: %s", identifier_type.value, identifier, exc)
            return None, CacheStatus.MISS

    def warm_from_devices(self, devices: Iterable[DeviceRecord]) -> int:
        """Warm Memurai cache using pipelines to reduce RTT overhead."""
        if not getattr(self, "_connected", True): return 0
        count = 0
        pipe = self._client.pipeline()
        for device in devices:
            payload_data = {
                "management_source": normalize_management_source(device.management_source),
                "source_host": device.source_host,
                "serial_number": device.serial_number,
                "fqdn": device.fqdn,
                "ip_address": device.ip_address,
                "id": device.id,
                "source_device_id": device.source_device_id,
                "device_type": device.device_type,
                "last_seen": device._serialize_datetime(device.last_seen) if device.last_seen else None,
                "created_at": device._serialize_datetime(device.created_at) if device.created_at else None,
                "updated_at": device._serialize_datetime(device.updated_at) if device.updated_at else None,
            }
            payload = json.dumps(payload_data)

            if device.ip_address:
                pipe.setex(self.key(IdentifierType.IP, device.ip_address), self._ttl, payload)
            if device.serial_number:
                pipe.setex(
                    self.key(IdentifierType.SERIAL_NUMBER, device.serial_number),
                    self._ttl,
                    payload,
                )
            if device.fqdn:
                pipe.setex(self.key(IdentifierType.FQDN, device.fqdn), self._ttl, payload)
            if device.serial_number:
                source_key = self.source_key(device)
                pipe.sadd(source_key, device.serial_number)
                pipe.expire(source_key, self._ttl)
            
            count += 1
            if count % 100 == 0:
                pipe.execute()
                pipe = self._client.pipeline()
        
        pipe.execute()
        return count

    def warm_devices(self, devices: Iterable[DeviceRecord]) -> int:
        """Warm cache with specified devices (incremental)."""
        return self.warm_from_devices(devices)

    def warm_recent_devices(self, limit: int = 100) -> int:
        """Incremental cache warming using recently resolved/seen devices from audit logs."""
        from db import db_manager
        rows = db_manager.execute_query(
            "SELECT identifier, MAX(timestamp) as max_ts FROM routing_audit GROUP BY identifier ORDER BY max_ts DESC LIMIT %s",
            (limit,),
            fetch_all=True
        ) or []
        identifiers = [row["identifier"] for row in rows]

        from db_queries import DeviceQueries
        devices_to_warm = []
        for ident in identifiers:
            row = DeviceQueries.get_by_serial(ident) or DeviceQueries.get_by_ip(ident) or DeviceQueries.get_by_fqdn(ident)
            if row:
                devices_to_warm.append(DeviceRecord.from_row(row))
        return self.warm_from_devices(devices_to_warm)

    def warm_updated_devices(self, limit: int = 100) -> int:
        """Incremental cache warming using recently updated devices from PostgreSQL."""
        from db import db_manager
        rows = db_manager.execute_query(
            "SELECT * FROM devices ORDER BY updated_at DESC LIMIT %s",
            (limit,),
            fetch_all=True
        ) or []
        devices = [DeviceRecord.from_row(row) for row in rows]
        return self.warm_from_devices(devices)

    def put_poll_metadata(
        self,
        source_type: str,
        source_host: str,
        metadata: dict,
        source_device_id: str | None = None,
    ) -> None:
        if not getattr(self, "_connected", True): return
        pkey = self.poll_key(source_type, source_host, source_device_id)
        pipe = self._client.pipeline()
        pipe.hset(pkey, mapping={
            key: "" if value is None else str(value)
            for key, value in metadata.items()
        })
        pipe.expire(pkey, self._ttl)
        pipe.execute()

    def invalidate_device(self, device: DeviceRecord) -> None:
        if not getattr(self, "_connected", True): return
        keys = []
        if device.ip_address:
            keys.append(self.key(IdentifierType.IP, device.ip_address))
        if device.serial_number:
            keys.append(self.key(IdentifierType.SERIAL_NUMBER, device.serial_number))
        if device.fqdn:
            keys.append(self.key(IdentifierType.FQDN, device.fqdn))
        if keys:
            self._client.delete(*keys)

    def _count_pattern(self, pattern: str) -> int:
        """Non-blocking scan_iter helper for large keyspaces."""
        count = 0
        for _ in self._client.scan_iter(match=pattern, count=1000):
            count += 1
        return count

    def stats(self) -> dict:
        """Non-blocking stats lookup using SCAN."""
        if not getattr(self, "_connected", True): return {"ip_keys": 0, "serial_keys": 0, "fqdn_keys": 0, "source_indexes": 0, "poll_metadata": 0, "ttl": self._ttl, "status": "disconnected"}
        return {
            "ip_keys": self._count_pattern("resolver:ip:*"),
            "serial_keys": self._count_pattern("resolver:sn:*"),
            "fqdn_keys": self._count_pattern("resolver:fqdn:*"),
            "source_indexes": self._count_pattern("resolver:source:*"),
            "poll_metadata": self._count_pattern("resolver:poll:*"),
            "ttl": self._ttl,
        }



    @staticmethod
    def _parse_datetime(value: object) -> Optional[datetime]:
        if not value:
            return None
        if isinstance(value, datetime):
            return value
        try:
            return datetime.fromisoformat(str(value))
        except ValueError:
            return None

    @classmethod
    def _deserialize_device(cls, raw: str) -> DeviceRecord:
        """Standardized OASF deserialization without legacy compatibility fallbacks."""
        data = json.loads(raw)
        return DeviceRecord(
            id=str(data.get("id") or ""),
            serial_number=str(data.get("serial_number") or ""),
            ip_address=data.get("ip_address"),
            fqdn=data.get("fqdn"),
            management_source=str(data.get("management_source") or ""),
            source_host=data.get("source_host"),
            source_device_id=data.get("source_device_id"),
            device_type=data.get("device_type"),
            last_seen=cls._parse_datetime(data.get("last_seen")),
            created_at=cls._parse_datetime(data.get("created_at")),
            updated_at=cls._parse_datetime(data.get("updated_at")),
        )
