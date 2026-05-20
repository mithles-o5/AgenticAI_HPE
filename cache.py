"""
Cache Layer
============
Step 2 of the resolver pipeline.

The resolver checks this cache before hitting the registry or any external
source (CMDB / HPE OneView).  On a miss the registry populates the cache
so subsequent lookups are fast.

Design:
  - Redis-backed distributed TTL cache
  - Keyed by UUID (primary) and alias (secondary → UUID pointer)
  - TTL default: 300 seconds
  - Supports multi-process deployments
"""

from __future__ import annotations

import json
import logging
import os
from typing import Optional

import redis

from records import ResourceRecord, CacheStatus

logger = logging.getLogger(__name__)

DEFAULT_TTL = 300   # seconds


class ResourceCache:
    """
    Redis-backed TTL cache for distributed caching across multiple MCP servers.
    Stores serialized ResourceRecords with automatic expiration.
    """

    def __init__(
        self,
        ttl: int = DEFAULT_TTL,
        host: str = os.getenv("REDIS_HOST", "localhost"),
        port: int = int(os.getenv("REDIS_PORT", "6379")),
        db: int = int(os.getenv("REDIS_DB", "0")),
        password: str = os.getenv("REDIS_PASSWORD", None),
    ) -> None:
        self._ttl = ttl
        self._redis_prefix = "resource_resolver:"
        
        try:
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
            # Test connection
            self._client.ping()
            logger.info(
                f"[Cache] Redis connected: {host}:{port}/db={db} "
                f"(ttl={ttl}s)"
            )
        except redis.ConnectionError as e:
            logger.error(f"[Cache] Redis connection failed: {e}")
            raise

    # ─────────────────────────────────────── write

    def put(self, record: ResourceRecord) -> None:
        """Store resource record in Redis with TTL."""
        try:
            # Serialize record to JSON
            record_json = json.dumps(record.to_dict())
            
            # Store by UUID
            uuid_key = f"{self._redis_prefix}uuid:{record.uuid}"
            self._client.setex(uuid_key, self._ttl, record_json)
            
            # Store UUID→name alias mapping
            alias_key = f"{self._redis_prefix}alias:{record.name.lower()}"
            self._client.setex(alias_key, self._ttl, record.uuid)
            
            # Store UUID→serial alias mapping
            if record.serial:
                serial_key = f"{self._redis_prefix}alias:{record.serial.lower()}"
                self._client.setex(serial_key, self._ttl, record.uuid)
            
            # Store UUID→custom alias mappings
            for alias in record.aliases:
                custom_key = f"{self._redis_prefix}alias:{alias.lower()}"
                self._client.setex(custom_key, self._ttl, record.uuid)
            
            logger.debug(
                f"[Cache] PUT {record.name} [{record.uuid[:8]}…] "
                f"ttl={self._ttl}s"
            )
        except Exception as e:
            logger.error(f"[Cache] Error storing record: {e}")
            raise

    def invalidate(self, uuid: str) -> None:
        """Remove resource record from cache."""
        try:
            uuid_key = f"{self._redis_prefix}uuid:{uuid}"
            self._client.delete(uuid_key)
            logger.debug(f"[Cache] INVALIDATE uuid={uuid[:8]}…")
        except Exception as e:
            logger.error(f"[Cache] Error invalidating record: {e}")

    # ─────────────────────────────────────── read

    def get_by_uuid(self, uid: str) -> tuple[Optional[ResourceRecord], CacheStatus]:
        """Retrieve resource by UUID."""
        try:
            uuid_key = f"{self._redis_prefix}uuid:{uid}"
            record_json = self._client.get(uuid_key)
            
            if record_json:
                logger.debug(f"[Cache] HIT uuid={uid[:8]}…")
                # Deserialize and reconstruct ResourceRecord
                record = self._deserialize_record(record_json)
                return record, CacheStatus.HIT
            else:
                logger.debug(f"[Cache] MISS uuid={uid[:8]}…")
                return None, CacheStatus.MISS
        except Exception as e:
            logger.error(f"[Cache] Error retrieving by UUID: {e}")
            return None, CacheStatus.MISS

    def get_by_alias(self, alias: str) -> tuple[Optional[ResourceRecord], CacheStatus]:
        """Retrieve resource by alias (name/serial/custom)."""
        try:
            alias_key = f"{self._redis_prefix}alias:{alias.lower()}"
            uid = self._client.get(alias_key)
            
            if not uid:
                logger.debug(f"[Cache] MISS alias={alias}")
                return None, CacheStatus.MISS
            
            logger.debug(f"[Cache] Alias '{alias}' → UUID {uid[:8]}…, fetching record...")
            record, status = self.get_by_uuid(uid)
            logger.debug(f"[Cache] get_by_uuid returned: record={record is not None}, status={status}")
            return record, status
        except Exception as e:
            logger.error(f"[Cache] Error retrieving by alias: {e}", exc_info=True)
            return None, CacheStatus.MISS

    # ─────────────────────────────────────── housekeeping

    def evict_expired(self) -> int:
        """Remove expired entries (Redis handles this automatically)."""
        # Redis automatically removes expired keys, but we can report stats
        return 0

    def __len__(self) -> int:
        """Get approximate number of cached records."""
        try:
            pattern = f"{self._redis_prefix}uuid:*"
            count = self._client.keys(pattern).__len__()
            return count
        except Exception as e:
            logger.error(f"[Cache] Error getting cache size: {e}")
            return 0

    def stats(self) -> dict:
        """Get cache statistics."""
        try:
            uuid_pattern = f"{self._redis_prefix}uuid:*"
            alias_pattern = f"{self._redis_prefix}alias:*"
            
            uuid_count = self._client.keys(uuid_pattern).__len__()
            alias_count = self._client.keys(alias_pattern).__len__()
            
            return {
                "live_records": uuid_count,
                "alias_mappings": alias_count,
                "redis_host": self._client.connection_pool.connection_kwargs.get("host"),
                "redis_port": self._client.connection_pool.connection_kwargs.get("port"),
                "ttl": self._ttl,
            }
        except Exception as e:
            logger.error(f"[Cache] Error getting stats: {e}")
            return {"error": str(e)}

    # ─────────────────────────────────────── private

    def _deserialize_record(self, json_str: str) -> Optional[ResourceRecord]:
        """Reconstruct ResourceRecord from JSON."""
        try:
            from enums import Vendor, Protocol, ResourceHealth, DeploymentType, ResourceType
            
            data = json.loads(json_str)
            
            # Reconstruct credential ref if present
            cred_dict = data.get("credential_ref")
            cred_ref = None
            if cred_dict:
                from records import CredentialRef
                cred_ref = CredentialRef(
                    vault_path=cred_dict.get("vault_path", ""),
                    auth_type=cred_dict.get("auth_type", "basic"),
                    username=cred_dict.get("username"),
                    certificate=cred_dict.get("certificate"),
                )
            
            # Parse deployment type with fallback
            deployment_type_str = data.get("deployment_type", "On-Premises")
            try:
                deployment_type = DeploymentType(deployment_type_str)
            except ValueError:
                logger.warning(
                    f"[Cache] Unknown deployment type '{deployment_type_str}', defaulting to ON_PREM"
                )
                deployment_type = DeploymentType.ON_PREM
            
            # Parse resource type with fallback
            resource_type_str = data.get("resource_type", "ServerHardware")
            try:
                resource_type = ResourceType(resource_type_str)
            except ValueError:
                logger.warning(
                    f"[Cache] Unknown resource type '{resource_type_str}', defaulting to SERVER_HARDWARE"
                )
                resource_type = ResourceType.SERVER_HARDWARE
            
            # Reconstruct ResourceRecord
            record = ResourceRecord(
                name=data["name"],
                uuid=data["uuid"],
                aliases=data.get("aliases", []),
                ip_address=data.get("ip_address", ""),
                management_host=data.get("management_host", ""),
                vendor=Vendor(data.get("vendor", "HPE")),
                deployment_type=deployment_type,
                supported_protocols=[Protocol(p) for p in data.get("supported_protocols", [])],
                resource_type=resource_type,
                model=data.get("model", ""),
                serial=data.get("serial", ""),
                firmware=data.get("firmware", ""),
                enclosure=data.get("enclosure", ""),
                bay=data.get("bay"),
                location=data.get("location"),
                asset_tag=data.get("asset_tag"),
                owner=data.get("owner"),
                tags=data.get("tags", []),
                power_state=data.get("power_state", "Unknown"),
                health=ResourceHealth(data.get("health", "UNKNOWN")),
                etag=data.get("etag"),
                credential_ref=cred_ref,
            )
            logger.debug(
                f"[Cache] Successfully deserialized record: {record.name} [{record.uuid[:8]}…]"
            )
            return record
        except Exception as e:
            logger.error(f"[Cache] Error deserializing record: {e}", exc_info=True)
            return None
