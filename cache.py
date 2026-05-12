"""
Cache Layer
============
Step 2 of the resolver pipeline.

The resolver checks this cache before hitting the registry or any external
source (CMDB / HPE OneView).  On a miss the registry populates the cache
so subsequent lookups are fast.

Design:
  - In-process TTL dict (swap for Redis in production)
  - Keyed by UUID (primary) and alias (secondary → UUID pointer)
  - TTL default: 300 seconds
"""

from __future__ import annotations

import logging
import time
from typing import Optional

from records import ResourceRecord, CacheStatus

logger = logging.getLogger(__name__)

DEFAULT_TTL = 300   # seconds


class _Entry:
    __slots__ = ("record", "expires_at")

    def __init__(self, record: ResourceRecord, ttl: int) -> None:
        self.record     = record
        self.expires_at = time.monotonic() + ttl

    @property
    def alive(self) -> bool:
        return time.monotonic() < self.expires_at


class ResourceCache:
    """
    Thread-safe (GIL-protected) in-memory TTL cache.
    Replace with a Redis-backed implementation for multi-process deployments.
    """

    def __init__(self, ttl: int = DEFAULT_TTL) -> None:
        self._ttl:     int                     = ttl
        self._by_uuid: dict[str, _Entry]       = {}
        self._aliases: dict[str, str]          = {}   # alias_lower → uuid

    # ─────────────────────────────────────── write

    def put(self, record: ResourceRecord) -> None:
        entry = _Entry(record, self._ttl)
        self._by_uuid[record.uuid] = entry
        self._aliases[record.name.lower()] = record.uuid
        if record.serial:
            self._aliases[record.serial.lower()] = record.uuid
        for alias in record.aliases:
            self._aliases[alias.lower()] = record.uuid
        logger.debug(f"[Cache] PUT {record.name} [{record.uuid[:8]}…] ttl={self._ttl}s")

    def invalidate(self, uuid: str) -> None:
        self._by_uuid.pop(uuid, None)
        self._aliases = {k: v for k, v in self._aliases.items() if v != uuid}

    # ─────────────────────────────────────── read

    def get_by_uuid(self, uid: str) -> tuple[Optional[ResourceRecord], CacheStatus]:
        entry = self._by_uuid.get(uid)
        if entry and entry.alive:
            logger.debug(f"[Cache] HIT uuid={uid[:8]}…")
            return entry.record, CacheStatus.HIT
        if entry:
            self._by_uuid.pop(uid, None)   # evict expired
        return None, CacheStatus.MISS

    def get_by_alias(self, alias: str) -> tuple[Optional[ResourceRecord], CacheStatus]:
        uid = self._aliases.get(alias.lower())
        if not uid:
            return None, CacheStatus.MISS
        return self.get_by_uuid(uid)

    # ─────────────────────────────────────── housekeeping

    def evict_expired(self) -> int:
        dead = [uid for uid, e in self._by_uuid.items() if not e.alive]
        for uid in dead:
            self.invalidate(uid)
        return len(dead)

    def __len__(self) -> int:
        return sum(1 for e in self._by_uuid.values() if e.alive)

    def stats(self) -> dict:
        return {"live_entries": len(self), "alias_keys": len(self._aliases)}
