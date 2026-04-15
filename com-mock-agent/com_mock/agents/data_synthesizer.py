"""
com_mock/agents/data_synthesizer.py
────────────────────────────────────
Agent 4 — DataSynthesisAgent

Generates schema-compliant, relationally consistent resource instances.

Key difference from the mentor's template generator:
  • Uses the extracted field schemas to generate typed, realistic data
  • Resolves foreign-key refs to real existing URIs (not random strings)
  • Generation order respects the dependency graph
    (create ServerHardwareTypes before ServerHardware that references them)
  • Retry-aware: receives the set of resource types that failed validation
    and regenerates only those (the validator sends them back here)
"""

from __future__ import annotations

import logging
from typing import Callable, Coroutine

from com_mock.resource_graph import ONEVIEW_RESOURCE_SCHEMAS, synthesize_resource

logger = logging.getLogger(__name__)

# Topological order for HPE OneView — leaf dependencies first
HPE_GENERATION_ORDER = [
    # Level 0 — no dependencies
    "server-hardware-types",
    "enclosure-groups",
    "ethernet-networks",
    "fc-networks",
    "storage-systems",
    "firmware-drivers",
    "scopes",
    # Level 1 — depend on level 0
    "enclosures",
    "storage-pools",
    "server-profile-templates",
    # Level 2 — depend on level 0+1
    "volumes",
    "network-sets",
    "server-profiles",
    "racks",
    # Level 3 — depend on level 2
    "server-hardware",
    # Generated independently (not in main resource graph)
    "tasks",
    "alerts",
    "events",
]


async def run_data_synthesizer(
    state: dict,
    report: Callable[[str], Coroutine],
) -> dict:
    """
    LangGraph node: DataSynthesisAgent

    Generates `instances_per_resource` instances for each resource type.
    For retry runs, only regenerates `retry_resource_types`.
    """
    n = state.get("instances_per_resource", 5)
    is_hpe = state.get("is_hpe_oneview", False)
    retry_types: list[str] = state.get("retry_resource_types", [])
    existing: dict[str, list[dict]] = state.get("synthesized_data", {})

    schemas = ONEVIEW_RESOURCE_SCHEMAS if is_hpe else _build_schemas_from_extracted(state)

    # Determine which types to (re)generate
    if retry_types:
        types_to_generate = retry_types
        await report(f"🔄 DataSynthesizer: re-synthesizing {len(retry_types)} resource types")
    else:
        types_to_generate = HPE_GENERATION_ORDER if is_hpe else list(schemas.keys())
        await report(f"🧬 DataSynthesizer: generating {n} instances × {len(types_to_generate)} types")

    synthesized: dict[str, list[dict]] = dict(existing)

    # Build the existing-refs map (URI lists per slug)
    existing_refs: dict[str, list[str]] = {
        slug: [r["uri"] for r in items]
        for slug, items in synthesized.items()
        if items
    }

    for resource_slug in types_to_generate:
        schema = schemas.get(resource_slug)
        if not schema:
            # Fallback: build minimal schema from relationship_graph entry
            schema = _minimal_schema(resource_slug)

        instances: list[dict] = []
        for i in range(n):
            try:
                item = synthesize_resource(resource_slug, i, schema, existing_refs)
                instances.append(item)
            except Exception as exc:
                logger.warning("Synthesis error %s[%d]: %s", resource_slug, i, exc)

        synthesized[resource_slug] = instances
        # Update refs so later types can reference these
        existing_refs[resource_slug] = [r["uri"] for r in instances]
        await report(f"  ✅ {resource_slug}: {len(instances)} instances")

    # Also generate tasks + alerts for realism
    if not retry_types:
        synthesized["tasks"]  = _generate_tasks(n)
        synthesized["alerts"] = _generate_alerts(n, existing_refs)
        synthesized["events"] = _generate_events(n, existing_refs)

    total = sum(len(v) for v in synthesized.values())
    await report(f"🧬 DataSynthesizer complete: {total} total records")

    return {
        "synthesized_data":   synthesized,
        "retry_resource_types": [],
        "status":             "validating",
        "progress_log":       state.get("progress_log", [])
                              + [f"Synthesized {total} records"],
    }


# ── Helper generators ────────────────────────────────────────────────────────

def _generate_tasks(n: int) -> list[dict]:
    import hashlib
    tasks = []
    states = ["Completed", "Completed", "Completed", "Error", "Warning"]
    names = ["Apply server profile", "Update firmware", "Power on server", "Add to scope", "Configure network"]
    for i in range(n):
        uid_seed = f"task:{i}"
        uid = hashlib.md5(uid_seed.encode()).hexdigest()
        task_id = f"{uid[:8]}-{uid[8:12]}-{uid[12:16]}-{uid[16:20]}-{uid[20:32]}"
        tasks.append({
            "type":            "TaskResourceV2",
            "category":        "tasks",
            "id":              task_id,
            "uri":             f"/rest/tasks/{task_id}",
            "taskType":        "User",
            "taskState":       states[i % len(states)],
            "name":            names[i % len(names)],
            "percentComplete": 100 if states[i % len(states)] in ("Completed", "Error") else 50,
            "stateReason":     "Completed normally" if states[i % len(states)] == "Completed" else "Operation failed",
            "owner":           "Administrator",
            "eTag":            uid,
            "created":         f"2025-0{(i % 9) + 1}-{(i % 28) + 1:02d}T10:00:00.000Z",
            "modified":        f"2025-0{(i % 9) + 1}-{(i % 28) + 1:02d}T10:01:30.000Z",
        })
    return tasks


def _generate_alerts(n: int, refs: dict[str, list[str]]) -> list[dict]:
    import hashlib
    severities = ["OK", "Warning", "Warning", "Critical", "OK"]
    states = ["Active", "Cleared", "Active", "Locked", "Cleared"]
    descriptions = [
        "Fan redundancy reduced in the enclosure.",
        "iLO firmware update is recommended.",
        "Network connectivity degraded on uplink.",
        "Storage pool utilization exceeded 80%.",
        "Power supply redundancy lost.",
    ]
    alerts = []
    # Pick a random resource URI to attach alerts to
    all_uris = [uri for uris in refs.values() for uri in uris]
    for i in range(n):
        uid_seed = f"alert:{i}"
        uid = hashlib.md5(uid_seed.encode()).hexdigest()
        alert_id = f"{uid[:8]}-{uid[8:12]}-{uid[12:16]}-{uid[16:20]}-{uid[20:32]}"
        resource_uri = all_uris[i % len(all_uris)] if all_uris else "/rest/server-hardware/unknown"
        alerts.append({
            "type":             "AlertResourceV3",
            "category":         "alerts",
            "id":               alert_id,
            "uri":              f"/rest/alerts/{alert_id}",
            "alertTypeID":      f"ALERT_{i:04d}",
            "severity":         severities[i % len(severities)],
            "alertState":       states[i % len(states)],
            "description":      descriptions[i % len(descriptions)],
            "correctiveAction": "Review and acknowledge the alert.",
            "resourceUri":      resource_uri,
            "eTag":             uid,
            "created":          f"2025-0{(i % 9) + 1}-{(i % 28) + 1:02d}T08:00:00.000Z",
            "modified":         f"2025-0{(i % 9) + 1}-{(i % 28) + 1:02d}T08:00:00.000Z",
        })
    return alerts


def _generate_events(n: int, refs: dict[str, list[str]]) -> list[dict]:
    import hashlib
    severities = ["OK", "Warning", "Critical", "OK", "Warning"]
    types = ["ServerPower", "NetworkChange", "StorageAlert", "FirmwareUpdate", "ConfigChange"]
    descriptions = [
        "Server power state changed to On.",
        "Network uplink state changed to Active.",
        "Storage pool capacity warning threshold reached.",
        "Firmware updated successfully.",
        "Server profile configuration changed.",
    ]
    events = []
    all_uris = [uri for uris in refs.values() for uri in uris]
    for i in range(n):
        uid_seed = f"event:{i}"
        uid = hashlib.md5(uid_seed.encode()).hexdigest()
        event_id = f"{uid[:8]}-{uid[8:12]}-{uid[12:16]}-{uid[16:20]}-{uid[20:32]}"
        resource_uri = all_uris[i % len(all_uris)] if all_uris else "/rest/server-hardware/unknown"
        events.append({
            "type":             "EventResourceV2",
            "category":         "events",
            "id":               event_id,
            "uri":              f"/rest/events/{event_id}",
            "eventTypeID":      types[i % len(types)],
            "severity":         severities[i % len(severities)],
            "description":      descriptions[i % len(descriptions)],
            "resourceUri":      resource_uri,
            "eTag":             uid,
            "created":          f"2025-0{(i % 9) + 1}-{(i % 28) + 1:02d}T09:00:00.000Z",
            "modified":         f"2025-0{(i % 9) + 1}-{(i % 28) + 1:02d}T09:00:00.000Z",
        })
    return events


def _minimal_schema(resource_slug: str) -> dict:
    return {
        "type_name":       resource_slug,
        "base_path":       f"/rest/{resource_slug}",
        "category":        "GENERAL",
        "task_operations": {"POST", "PUT", "DELETE"},
        "task_duration_ms": 1000,
        "fields":          {},
        "relationships":   {},
    }


def _build_schemas_from_extracted(state: dict) -> dict:
    """
    Convert LLM-extracted schemas (from SchemaExtractorAgent) into the
    same format used by ONEVIEW_RESOURCE_SCHEMAS so synthesize_resource()
    can be reused.
    """
    extracted: dict = state.get("extracted_schemas", {})
    result = {}

    for slug, schema_data in extracted.items():
        fields = {}
        for fname, fspec in schema_data.get("fields", {}).items():
            ftype = fspec.get("type", "string")
            entry: dict = {"type": ftype}
            if fspec.get("values"):
                entry["values"] = fspec["values"]
            if fspec.get("min") is not None:
                entry["min"] = fspec["min"]
            if fspec.get("max") is not None:
                entry["max"] = fspec["max"]
            if fspec.get("nullable") is not None:
                entry["nullable"] = fspec["nullable"]
            if fspec.get("required"):
                entry["required"] = True
            if fspec.get("target"):
                entry["target"] = fspec["target"]
            fields[fname] = entry

        # Infer task operations from extracted endpoint list
        task_ops = set()
        for ep in schema_data.get("endpoints", []):
            m = ep.get("method", "")
            if m in ("POST", "PUT", "DELETE"):
                task_ops.add(m)

        result[slug] = {
            "type_name":       schema_data.get("type_name", slug),
            "base_path":       schema_data.get("base_path", f"/rest/{slug}"),
            "category":        schema_data.get("category", "GENERAL"),
            "task_operations": task_ops,
            "task_duration_ms": 1000,
            "fields":          fields,
            "relationships":   {},
        }

    return result
