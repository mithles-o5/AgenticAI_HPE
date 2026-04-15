"""
com_mock/agents/relationship_mapper.py
───────────────────────────────────────
Agent 3 — RelationshipMapperAgent

Analyses extracted schemas and identifies cross-resource foreign key relationships.
For unknown APIs (not HPE OneView), this agent infers relationships from field names.

Rules applied:
  • Fields ending in 'Uri' or 'Uris' that match known resource slugs → ref / array_ref
  • Fields named '*Id' that look like foreign keys → ref
  • Fields named '*Ids' → array_ref
  • Explicit $ref in extracted schemas → ref
"""

from __future__ import annotations

import logging
import re
from typing import Callable, Coroutine

logger = logging.getLogger(__name__)

_URI_FIELD_RE = re.compile(r"^([a-z][a-zA-Z0-9]+?)(Uri|Uris|ID|Ids)$")


def _slug_from_camel(camel: str) -> str:
    """Convert camelCase prefix to kebab-case resource slug."""
    # serverHardware → server-hardware
    s = re.sub(r"(?<!^)(?=[A-Z])", "-", camel).lower()
    # Handle plural: server-hardwares → server-hardware (approximate)
    if s.endswith("s") and not s.endswith("ss"):
        # Don't strip s from things like "status", "address"
        pass
    return s


async def run_relationship_mapper(
    state: dict,
    report: Callable[[str], Coroutine],
) -> dict:
    """
    LangGraph node: RelationshipMapperAgent

    Builds the relationship_graph dict from extracted_schemas.
    For HPE OneView fast-path, the relationship graph is already embedded
    in ONEVIEW_RESOURCE_SCHEMAS — this agent enriches unknown APIs.
    """
    schemas: dict = state.get("extracted_schemas", {})
    is_hpe = state.get("is_hpe_oneview", False)

    if is_hpe:
        # Fast path: relationships come from ONEVIEW_RESOURCE_SCHEMAS
        from com_mock.resource_graph import ONEVIEW_RESOURCE_SCHEMAS
        rg: dict[str, list[dict]] = {}
        for slug, schema in ONEVIEW_RESOURCE_SCHEMAS.items():
            rels = []
            for field_name, rel in schema.get("relationships", {}).items():
                rels.append({
                    "field":       field_name,
                    "target":      rel["target"],
                    "cascade":     rel.get("cascade", "nullify"),
                    "bidirectional": rel.get("bidirectional"),
                })
            rg[slug] = rels

        await report(f"📊 RelationshipMapper: mapped {len(rg)} HPE resources (fast-path)")
        return {
            "relationship_graph": rg,
            "status":             "synthesizing",
            "progress_log":       state.get("progress_log", [])
                                  + [f"Mapped {len(rg)} resource relationships (HPE fast-path)"],
        }

    # Unknown API: infer from field naming conventions
    known_slugs = set(schemas.keys())
    rg = {}

    for slug, schema in schemas.items():
        rels = []
        fields = schema.get("fields", {})

        for field_name, field_spec in fields.items():
            # Explicit ref in extracted schema
            if field_spec.get("type") in ("ref", "array_ref"):
                target = field_spec.get("target", "")
                if target:
                    rels.append({
                        "field":   field_name,
                        "target":  target,
                        "cascade": "nullify",
                    })
                continue

            # Infer from field name pattern
            m = _URI_FIELD_RE.match(field_name)
            if not m:
                continue

            prefix = m.group(1)   # e.g. "serverHardware"
            suffix = m.group(2)   # e.g. "Uri"
            candidate_slug = _slug_from_camel(prefix)

            # Check if the inferred slug exists in our known set
            matched_slug = None
            for known in known_slugs:
                if known == candidate_slug or known.startswith(candidate_slug):
                    matched_slug = known
                    break

            if matched_slug:
                is_array = suffix in ("Uris", "Ids")
                rels.append({
                    "field":   field_name,
                    "target":  matched_slug,
                    "cascade": "nullify",
                    "is_array": is_array,
                })

        rg[slug] = rels

    total_rels = sum(len(v) for v in rg.values())
    await report(f"📊 RelationshipMapper: found {total_rels} cross-resource relationships")

    return {
        "relationship_graph": rg,
        "status":             "synthesizing",
        "progress_log":       state.get("progress_log", [])
                              + [f"Mapped {total_rels} relationships across {len(rg)} resources"],
    }
