"""
Resource Registry
==================
Step 1 + 3 of the resolver pipeline.

  - Queries PostgreSQL directly (no in-memory storage)
  - Exact UUID lookup
  - Alias index lookup
  - Fuzzy search using database full-text search
  - CMDB adapter hook — override cmdb_lookup() to query your CMDB

On a cache miss the resolver calls registry.lookup(), which tries:
  1. Exact UUID match (database query)
  2. Exact alias match (database query)
  3. Fuzzy match against name / model / serial / tags (database FTS)
  4. External CMDB query  (override cmdb_lookup())
"""

from __future__ import annotations

import logging
from typing import Optional

from records import ResourceRecord
from db_queries import ServerQueries

logger = logging.getLogger(__name__)


class ResourceRegistry:
    """
    Database-backed registry. All lookups go to PostgreSQL.
    Zero in-memory storage of server data.
    """

    def __init__(self) -> None:
        pass  # No in-memory caches

    # ─────────────────────────────────────── write (no-op)
    def register(self, record: ResourceRecord) -> None:
        """No-op: data already in database."""
        logger.debug(f"[Registry] Record {record.name} already in database")

    # ─────────────────────────────────────── read (database queries)

    def get_by_uuid(self, uid: str) -> Optional[ResourceRecord]:
        """Query database for UUID."""
        row = ServerQueries.get_by_uuid(uid)
        return self._row_to_record(row) if row else None

    def get_by_alias(self, alias: str) -> Optional[ResourceRecord]:
        """Query database for alias."""
        row = ServerQueries.get_by_alias(alias)
        return self._row_to_record(row) if row else None

    def fuzzy_search(self, query: str) -> Optional[ResourceRecord]:
        """Fuzzy search using database."""
        rows = ServerQueries.fuzzy_search(query, limit=1)
        return self._row_to_record(rows[0]) if rows else None

    def lookup(self, query: str, uuid_hint: str = "") -> tuple[Optional[ResourceRecord], str]:
        """
        Full lookup chain: uuid → alias → fuzzy → cmdb.
        Returns (record, method_used).
        """
        # Try UUID hint first
        if uuid_hint:
            r = self.get_by_uuid(uuid_hint)
            if r:
                return r, "uuid"

        # Try exact alias match for each token
        for token in query.split():
            r = self.get_by_alias(token)
            if r:
                return r, "alias"

        # Fuzzy search in database
        r = self.fuzzy_search(query)
        if r:
            return r, "fuzzy"

        # External CMDB fallback
        r = self.cmdb_lookup(query)
        if r:
            return r, "cmdb"

        return None, "not_found"

    # ─────────────────────────────────────── helper

    @staticmethod
    def _row_to_record(row: dict) -> Optional[ResourceRecord]:
        """Convert database row to ResourceRecord."""
        if not row:
            return None
        
        from enums import Vendor, Protocol, ResourceHealth, DeploymentType, ResourceType
        from records import CredentialRef
        
        # Parse vendor
        vendor_name = row.get("vendor_name", "HPE")
        try:
            vendor = Vendor[vendor_name.upper()]
        except KeyError:
            vendor = Vendor.HPE
        
        # Parse protocols
        protocols = []
        if row.get("protocols"):
            for p in row["protocols"].split(", "):
                p_clean = p.strip().upper()
                try:
                    protocols.append(Protocol[p_clean])
                except KeyError:
                    pass
        
        # Parse aliases
        aliases = []
        if row.get("aliases"):
            aliases = [a.strip() for a in row["aliases"].split(", ") if a.strip()]
        
        # Parse tags
        tags = []
        if row.get("tags"):
            tags = [t.strip() for t in row["tags"].split(", ") if t.strip()]
        
        # Parse health
        health_str = row.get("power_state", "Unknown")
        try:
            health = ResourceHealth[health_str.upper()]
        except KeyError:
            health = ResourceHealth.UNKNOWN
        
        # Build credential reference if vault_path exists
        credential_ref = None
        if row.get("vault_path"):
            credential_ref = CredentialRef(
                vault_path=row["vault_path"],
                auth_type=row.get("auth_type", "basic"),
            )
        
        return ResourceRecord(
            uuid=row["uuid"],
            name=row["name"],
            vendor=vendor,
            model=row.get("model", ""),
            serial=row.get("serial", ""),
            ip_address=row.get("ip_address", ""),
            management_host=row.get("management_host", ""),
            location=row.get("location"),
            owner=row.get("owner"),
            supported_protocols=protocols,
            aliases=aliases,
            tags=tags,
            firmware=row.get("firmware", ""),
            power_state=row.get("power_state", "Unknown"),
            health=health,
            credential_ref=credential_ref,
        )

        return None, "none"
