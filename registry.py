"""
Resource Registry
==================
Step 1 + 3 of the resolver pipeline.

  - Primary store for ResourceRecords (keyed by UUID)
  - Alias index for name / serial / custom alias lookup
  - Fuzzy search for NL query matching
  - CMDB adapter hook — override cmdb_lookup() to query your CMDB

On a cache miss the resolver calls registry.lookup(), which tries:
  1. Exact UUID match
  2. Exact alias match
  3. Fuzzy match against name / model / serial / tags
  4. External CMDB query  (override cmdb_lookup())
"""

from __future__ import annotations

import logging
from typing import Optional

from records import ResourceRecord

logger = logging.getLogger(__name__)


class ResourceRegistry:

    def __init__(self) -> None:
        self._by_uuid:  dict[str, ResourceRecord] = {}
        self._by_alias: dict[str, str]            = {}   #dict[alias_lower, uuid]

    # ─────────────────────────────────────── write
    def register(self, record: ResourceRecord) -> None:
        self._by_uuid[record.uuid] = record
        self._idx(record.uuid, record.name)
        if record.serial:
            self._idx(record.uuid, record.serial)
        for alias in record.aliases:
            self._idx(record.uuid, alias)
        logger.debug(f"[Registry] Registered {record.name} [{record.uuid[:8]}…]")

    def _idx(self, uid: str, key: str) -> None:
        if key:
            self._by_alias[key.lower()] = uid

    # ─────────────────────────────────────── read

    def get_by_uuid(self, uid: str) -> Optional[ResourceRecord]:
        return self._by_uuid.get(uid)

    def get_by_alias(self, alias: str) -> Optional[ResourceRecord]:
        uid = self._by_alias.get(alias.lower())
        return self._by_uuid.get(uid) if uid else None

    def fuzzy_search(self, query: str) -> Optional[ResourceRecord]:
        words = query.lower().split()
        best, best_score = None, 0
        for r in self._by_uuid.values():
            haystack = (
                f"{r.name} {r.model} {r.serial} {r.enclosure} "
                f"{r.location or ''} {r.owner or ''} {' '.join(r.aliases)} "
                f"{' '.join(r.tags)}"
            ).lower()
            score = sum(
                3 if w in r.name.lower()   else
                2 if w in r.serial.lower() else
                1 if w in haystack         else 0
                for w in words
            )
            if score > best_score:
                best, best_score = r, score
        return best if best_score > 0 else None

    def lookup(self, query: str, uuid_hint: str = "") -> tuple[Optional[ResourceRecord], str]:
        """
        Full lookup chain: uuid → alias → fuzzy → cmdb.
        Returns (record, method_used).
        """
        if uuid_hint:
            r = self.get_by_uuid(uuid_hint)
            if r:
                return r, "uuid"

        for token in query.split():
            r = self.get_by_alias(token)
            if r:
                return r, "alias"

        r = self.fuzzy_search(query)
        if r:
            return r, "fuzzy"

        # External CMDB fallback
        r = self.cmdb_lookup(query)
        if r:
            self.register(r)
            return r, "cmdb"

        return None, "none"

    # ─────────────────────────────────────── CMDB hook

    def cmdb_lookup(self, query: str) -> Optional[ResourceRecord]:
        """
        Override this method to query your CMDB (ServiceNow, Nautobot, etc.)
        or HPE OneView server inventory.

        Example:
            def cmdb_lookup(self, query):
                data = my_cmdb_client.search(query)
                if data:
                    return ResourceRecord(name=data["name"], uuid=data["uuid"], ...)
                return None
        """
        logger.debug(f"[Registry] CMDB lookup not configured — query: '{query}'")
        return None

    def all_records(self) -> list[ResourceRecord]:
        return list(self._by_uuid.values())

    def __len__(self) -> int:
        return len(self._by_uuid)
