"""
Resource Resolver — Core Orchestrator
=======================================
Implements all 6 steps of the resolver spec:

  Step 1  Resource Identification  — map name/alias/UUID → ResourceRecord
  Step 2  Cache Utilization        — check cache first, fallback to registry/CMDB
  Step 3  Vendor & Capability      — read vendor + supported_protocols from record
  Step 4  Action Classification    — Provisioning vs Operational
  Step 5  Protocol Selection       — COMS / OneView decision tree
  Step 6  Execution Context        — assemble and return ExecutionContext to agent

Output → ExecutionContext (passed to Execution Agent / MCP tool)
"""

from __future__ import annotations

import logging

from records import ExecutionContext, CacheStatus
from registry import ResourceRegistry
from cache import ResourceCache
from selector import classify_action, select_protocol, build_endpoint
from errors import ResourceNotFoundError

logger = logging.getLogger(__name__)


class ResourceResolver:

    def __init__(
        self,
        registry: ResourceRegistry,
        cache:    ResourceCache,
    ) -> None:
        self.registry = registry
        self.cache    = cache

    # ─────────────────────────────────────────────────────────── public

    def resolve(self, query: str, uuid_hint: str = "") -> ExecutionContext:
        """
        Full resolver pipeline — Steps 1-6.
        Returns an ExecutionContext ready for the Execution Agent.
        """

        # ── Step 2: Cache check ───────────────────────────────────────────────
        record, cache_status = self._cache_lookup(query, uuid_hint)

        # ── Steps 1 + 2 miss: query registry / CMDB ──────────────────────────
        if record is None:
            record, method = self.registry.lookup(query, uuid_hint)
            if record is None:
                raise ResourceNotFoundError(
                    f"Resource not found for query '{query}'. "
                    "Checked database, aliases, and fuzzy search. "
                    "Check the resource name, alias, or UUID."
                )
            self.cache.put(record)   # populate cache for next call
            resolved_by = method
        else:
            resolved_by = "cache"

        # ── Step 3: Vendor & capability already on the record ─────────────────
        logger.info(
            f"[Resolver] Identified: {record.name} [{record.uuid[:8]}…] "
            f"vendor={record.vendor.value} "
            f"protocols={[p.value for p in record.supported_protocols]}"
        )

        # ── Step 4: Action classification ─────────────────────────────────────
        category, action = classify_action(query)

        # ── Step 5: Protocol selection ────────────────────────────────────────
        protocol, reason = select_protocol(record, category)

        # ── Step 6: Assemble execution context ────────────────────────────────
        ctx = ExecutionContext(
            resource_uuid     = record.uuid,
            resource_name     = record.name,
            vendor            = record.vendor,
            action_category   = category,
            action            = action,
            selected_protocol = protocol,
            protocol_reason   = reason,
            endpoint          = build_endpoint(record, protocol),
            credential_ref    = record.credential_ref,
            resolved_by       = resolved_by,
            cache_status      = cache_status,
            query             = query,
        )

        logger.info(
            f"[Resolver] ExecutionContext ready — "
            f"action={action.value} protocol={protocol.value} "
            f"endpoint={ctx.endpoint} cache={cache_status.value}"
        )
        return ctx

    # ─────────────────────────────────────────────────────────── private

    def _cache_lookup(self, query: str, uuid_hint: str):
        if uuid_hint:
            record, status = self.cache.get_by_uuid(uuid_hint)
            if record:
                return record, status

        for token in query.split():
            record, status = self.cache.get_by_alias(token)
            if record:
                return record, status

        return None, CacheStatus.MISS
