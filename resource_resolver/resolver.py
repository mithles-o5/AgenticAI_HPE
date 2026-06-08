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

from records import ExecutionContext, CacheStatus, ResourceRecord, DeploymentType, Protocol, ActionCategory
from registry import ResourceRegistry
from cache import ResourceCache
from selector import classify_action, select_protocol, resolve_api_call
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

    def resolve(self, query: str, uuid_hint: str = "", resource_category: str = "", expected_protocol: Protocol | None = None, parameters: dict = None) -> ExecutionContext:
        """
        Full resolver pipeline — Steps 1-6.
        Returns an ExecutionContext ready for the Execution Agent.
        """

        # ── Step 4: Action classification (moved up) ──────────────────────────
        category, action = classify_action(query)
        action_val = action.value if hasattr(action, "value") else str(action)

        # ── Step 2: Cache check ───────────────────────────────────────────────
        record, cache_status = self._cache_lookup(query, uuid_hint)

        # ── Steps 1 + 2 miss: query registry / CMDB ──────────────────────────
        if record is None:
            # 1. Try exact lookup by UUID or alias first
            record = None
            resolved_by = None
            
            if uuid_hint:
                record = self.registry.get_by_uuid(uuid_hint)
                if record:
                    resolved_by = "uuid"
                    
            if record is None:
                for token in query.split():
                    record = self.registry.get_by_alias(token)
                    if record:
                        resolved_by = "alias"
                        break
                        
            # 2. Check if this is a collection listing OR a provisioning (Create/Allocate) query OR explicit action targeting
            is_collection_query = any(w in query.lower() for w in ["list", "show all", "get all", "all"])
            is_provisioning_query = category == ActionCategory.PROVISIONING or action_val in ["Create", "Allocate"]
            is_action_direct = query.strip().startswith("action:")
            
            if record is None and (is_collection_query or is_provisioning_query or is_action_direct):
                deployment_type = DeploymentType.CLOUD if expected_protocol == Protocol.COMS else DeploymentType.ON_PREM
                supported_protocols = [expected_protocol] if expected_protocol else [Protocol.ONEVIEW, Protocol.COMS]
                record = ResourceRecord(
                    name="Collection",
                    uuid="",
                    deployment_type=deployment_type,
                    supported_protocols=supported_protocols
                )
                resolved_by = "collection"
                
            # 3. Fallback to fuzzy search / CMDB lookup for individual resource target
            if record is None:
                record = self.registry.fuzzy_search(query)
                if record:
                    resolved_by = "fuzzy"
                    
            if record is None:
                record = self.registry.cmdb_lookup(query)
                if record:
                    self.registry.register(record)
                    resolved_by = "cmdb"
                    
            if record is not None:
                if resolved_by != "collection":
                    self.cache.put(record)   # populate cache for next call
            else:
                raise ResourceNotFoundError(
                    f"Resource not found for query '{query}'. "
                    f"Registry has {len(self.registry)} entries. "
                    "Check the resource name, alias, or UUID."
                )
        else:
            resolved_by = "cache"

        # ── Step 3: Vendor & capability already on the record ─────────────────
        logger.info(
            f"[Resolver] Identified: {record.name} [{record.uuid[:8]}…] "
            f"vendor={record.vendor.value} "
            f"protocols={[p.value for p in record.supported_protocols]}"
        )

        # ── Step 5: Protocol selection ────────────────────────────────────────
        protocol, reason = select_protocol(record, category)

        # ── Step 6: Assemble execution context ────────────────────────────────
        http_method, endpoint, body = resolve_api_call(record, protocol, action, resource_category, parameters)

        ctx = ExecutionContext(
            resource_uuid     = record.uuid,
            resource_name     = record.name,
            vendor            = record.vendor,
            action_category   = category,
            action            = action,
            selected_protocol = protocol,
            protocol_reason   = reason,
            endpoint          = endpoint,
            http_method       = http_method,
            request_body      = body,
            credential_ref    = record.credential_ref,
            resolved_by       = resolved_by,
            cache_status      = cache_status,
            query             = query,
        )

        action_val = action.value if hasattr(action, "value") else str(action)
        logger.info(
            f"[Resolver] ExecutionContext ready — "
            f"action={action_val} protocol={protocol.value} "
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
