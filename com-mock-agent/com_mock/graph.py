"""
com_mock/graph.py
─────────────────
Parallel multi-agent LangGraph for the COM/OneView mock generation pipeline.

Graph topology
──────────────
                    START
                      │
              [doc_fetcher_node]
                      │
         ┌────────────┴────────────┐
    is_hpe_oneview?           is_unknown_api?
         │                         │
  [fast_path_node]    [parallel schema extraction]
  (skip extraction)    [schema_extractor_node × N]
         │                   [merge_schemas_node]
         └────────────┬────────────┘
                      │
           [relationship_mapper_node]
                      │
           [data_synthesizer_node]  ◄──────┐
                      │                     │ (retry)
             [validator_node]               │
                      │                     │
           errors & retries < max? ─────────┘
                      │ (no more retries)
             [db_seeder_node]
                      │
                     END

Key upgrades over the mentor's linear 3-node pipeline:
  • Parallel schema extraction (asyncio.gather for all doc pages)
  • Validation–retry loop (up to 3 passes per failing resource type)
  • Fast-path for HPE OneView (skips extraction entirely)
  • DB seeder writes to SQLite — data survives restarts
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
from pathlib import Path
from typing import Any, Callable, Coroutine, Literal, Optional

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import HumanMessage
from langgraph.graph import END, START, StateGraph

from com_mock.agents.data_synthesizer import run_data_synthesizer
from com_mock.agents.doc_fetcher import run_doc_fetcher
from com_mock.agents.relationship_mapper import run_relationship_mapper
from com_mock.agents.validator import run_validator
from com_mock.db import DatabaseEngine
from com_mock.llm_provider import create_llm
from com_mock.resource_graph import ONEVIEW_RESOURCE_SCHEMAS
from com_mock.state import COMCrawlerState

logger = logging.getLogger(__name__)

ProgressCallback = Optional[Callable[[str], Coroutine[Any, Any, None]]]

SCHEMA_EXTRACTION_CONCURRENCY = 4   # parallel LLM calls for schema extraction


def build_com_crawler_graph(
    db: DatabaseEngine,
    progress_callback: ProgressCallback = None,
    llm: Optional[BaseChatModel] = None,
    provider: Optional[str] = None,
    model: Optional[str] = None,
    output_dir: str = "output",
):
    """
    Build and compile the LangGraph for COM/OneView mock generation.

    Returns a compiled LangGraph that accepts COMCrawlerState.
    """
    if llm is None:
        llm = create_llm(provider=provider, model=model)

    async def _report(msg: str) -> None:
        logger.info(msg)
        if progress_callback:
            await progress_callback(msg)

    # ──────────────────────────────────────────────────────────────────────
    # Node 1 — Doc Fetcher
    # ──────────────────────────────────────────────────────────────────────

    async def doc_fetcher_node(state: COMCrawlerState) -> dict:
        return await run_doc_fetcher(state, _report)

    # ──────────────────────────────────────────────────────────────────────
    # Node 2a — Fast Path (HPE OneView)
    # Skips LLM extraction and jumps straight to relationship mapping.
    # ──────────────────────────────────────────────────────────────────────

    async def fast_path_node(state: COMCrawlerState) -> dict:
        await _report("⚡ Fast-path: using seeded HPE OneView schemas (no LLM extraction needed)")
        # The extracted_schemas for fast-path are loaded from ONEVIEW_RESOURCE_SCHEMAS
        fake_extracted = {
            slug: {
                "resource_slug": slug,
                "type_name": schema.get("type_name", slug),
                "base_path": schema.get("base_path", f"/rest/{slug}"),
                "fields": {
                    k: {"type": v.get("type", "string")}
                    for k, v in schema.get("fields", {}).items()
                },
                "endpoints": _build_endpoints_from_schema(slug, schema),
                "task_operations": list(schema.get("task_operations", [])),
            }
            for slug, schema in ONEVIEW_RESOURCE_SCHEMAS.items()
        }
        return {
            "extracted_schemas":       fake_extracted,
            "schema_batches_total":    0,
            "schema_batches_done":     0,
            "schema_extraction_errors": [],
            "status":                  "mapping",
            "progress_log":            state.get("progress_log", [])
                                       + ["Fast-path: HPE schemas loaded"],
        }

    # ──────────────────────────────────────────────────────────────────────
    # Node 2b — Parallel Schema Extractor (unknown APIs)
    # ──────────────────────────────────────────────────────────────────────

    async def schema_extractor_node(state: COMCrawlerState) -> dict:
        """
        Extract schemas from all fetched pages in parallel.
        Uses asyncio.gather with SCHEMA_EXTRACTION_CONCURRENCY batches.
        """
        from com_mock.agents.schema_extractor import run_schema_extractor_batch

        pages = list(state.get("fetched_pages", {}).items())  # [(url, text), ...]

        if not pages:
            await _report("⚠️  No pages to extract from — using generic schema")
            return {
                "extracted_schemas":        {},
                "schema_batches_total":     0,
                "schema_batches_done":      0,
                "schema_extraction_errors": [],
                "status":                   "mapping",
            }

        # Split pages into parallel batches
        batch_size = max(1, len(pages) // SCHEMA_EXTRACTION_CONCURRENCY + 1)
        batches = [pages[i : i + batch_size] for i in range(0, len(pages), batch_size)]

        await _report(
            f"🔬 SchemaExtractor: {len(pages)} pages → {len(batches)} parallel batches"
        )

        tasks = [
            run_schema_extractor_batch(batch, llm, _report)
            for batch in batches
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        merged: dict[str, dict] = {}
        errors: list[str] = []

        for i, result in enumerate(results):
            if isinstance(result, Exception):
                err = f"Batch {i} extraction error: {result}"
                errors.append(err)
                await _report(f"  ⚠️  {err}")
            elif isinstance(result, dict):
                # Merge — later batches don't overwrite earlier ones
                for slug, schema in result.items():
                    merged.setdefault(slug, schema)

        await _report(
            f"✅ SchemaExtractor complete: {len(merged)} resource schemas extracted"
        )

        return {
            "extracted_schemas":        merged,
            "schema_batches_total":     len(batches),
            "schema_batches_done":      len(batches),
            "schema_extraction_errors": errors,
            "status":                   "mapping",
            "progress_log":             state.get("progress_log", [])
                                        + [f"Extracted {len(merged)} schemas"],
        }

    # ──────────────────────────────────────────────────────────────────────
    # Node 3 — Relationship Mapper
    # ──────────────────────────────────────────────────────────────────────

    async def relationship_mapper_node(state: COMCrawlerState) -> dict:
        return await run_relationship_mapper(state, _report)

    # ──────────────────────────────────────────────────────────────────────
    # Node 4 — Data Synthesizer (also handles retries)
    # ──────────────────────────────────────────────────────────────────────

    async def data_synthesizer_node(state: COMCrawlerState) -> dict:
        return await run_data_synthesizer(state, _report)

    # ──────────────────────────────────────────────────────────────────────
    # Node 5 — Validator
    # ──────────────────────────────────────────────────────────────────────

    async def validator_node(state: COMCrawlerState) -> dict:
        return await run_validator(state, _report)

    # ──────────────────────────────────────────────────────────────────────
    # Node 6 — DB Seeder
    # ──────────────────────────────────────────────────────────────────────

    async def db_seeder_node(state: COMCrawlerState) -> dict:
        """
        Write all synthesized data to the SQLite database.
        Also writes the api_spec.json + mock_data.json for backward compat.
        """
        synthesized: dict[str, list[dict]] = state.get("synthesized_data", {})
        await _report(f"\n💾 DbSeeder: writing {sum(len(v) for v in synthesized.values())} records to SQLite")

        seeded_types: list[str] = []
        total_seeded = 0

        for resource_type, instances in synthesized.items():
            if not instances:
                continue
            n = await db.bulk_seed(resource_type, instances)
            seeded_types.append(resource_type)
            total_seeded += n
            await _report(f"  📥 {resource_type}: {n} records seeded")

        # Build api_spec for Swagger + backward compatibility
        api_spec = _build_api_spec(state)
        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)

        with open(out / "api_spec.json", "w", encoding="utf-8") as f:
            json.dump(api_spec, f, indent=2, default=str)

        # Minimal mock_data.json stub (actual data is now in SQLite)
        with open(out / "mock_data.json", "w", encoding="utf-8") as f:
            json.dump({"note": "Live data served from SQLite. See /rest/* endpoints."}, f)

        await _report(f"✅ DbSeeder complete: {total_seeded} records across {len(seeded_types)} resource types")

        return {
            "seeded_resource_types": seeded_types,
            "seeded_total_records":  total_seeded,
            "api_spec":              api_spec,
            "status":                "complete",
            "progress_log":          state.get("progress_log", [])
                                     + [f"Seeded {total_seeded} records to SQLite"],
        }

    # ──────────────────────────────────────────────────────────────────────
    # Routing
    # ──────────────────────────────────────────────────────────────────────

    def route_after_fetch(
        state: COMCrawlerState,
    ) -> Literal["fast_path_node", "schema_extractor_node"]:
        return "fast_path_node" if state.get("is_hpe_oneview") else "schema_extractor_node"

    def route_after_validation(
        state: COMCrawlerState,
    ) -> Literal["data_synthesizer_node", "db_seeder_node"]:
        if state.get("retry_resource_types"):
            return "data_synthesizer_node"
        return "db_seeder_node"

    # ──────────────────────────────────────────────────────────────────────
    # Assemble graph
    # ──────────────────────────────────────────────────────────────────────

    graph = StateGraph(COMCrawlerState)

    graph.add_node("doc_fetcher_node",         doc_fetcher_node)
    graph.add_node("fast_path_node",           fast_path_node)
    graph.add_node("schema_extractor_node",    schema_extractor_node)
    graph.add_node("relationship_mapper_node", relationship_mapper_node)
    graph.add_node("data_synthesizer_node",    data_synthesizer_node)
    graph.add_node("validator_node",           validator_node)
    graph.add_node("db_seeder_node",           db_seeder_node)

    graph.add_edge(START, "doc_fetcher_node")
    graph.add_conditional_edges("doc_fetcher_node", route_after_fetch)
    graph.add_edge("fast_path_node",        "relationship_mapper_node")
    graph.add_edge("schema_extractor_node", "relationship_mapper_node")
    graph.add_edge("relationship_mapper_node", "data_synthesizer_node")
    graph.add_edge("data_synthesizer_node",    "validator_node")
    graph.add_conditional_edges("validator_node", route_after_validation)
    graph.add_edge("db_seeder_node", END)

    return graph.compile()


# ── Helpers ──────────────────────────────────────────────────────────────────

def _build_endpoints_from_schema(slug: str, schema: dict) -> list[dict]:
    """Build standard CRUD endpoint list from a resource schema."""
    base = schema.get("base_path", f"/rest/{slug}")
    cat = schema.get("category", "GENERAL")
    task_ops = schema.get("task_operations", set())
    endpoints = [
        {"method": "GET",    "path": base,          "summary": f"List {slug}", "category": cat},
        {"method": "GET",    "path": f"{base}/{{id}}", "summary": f"Get {slug} by ID", "category": cat},
    ]
    if "POST" in task_ops or True:
        endpoints.append({"method": "POST", "path": base, "summary": f"Create {slug}", "category": cat})
    if "PUT" in task_ops or True:
        endpoints.append({"method": "PUT", "path": f"{base}/{{id}}", "summary": f"Update {slug}", "category": cat})
    if "DELETE" in task_ops or True:
        endpoints.append({"method": "DELETE", "path": f"{base}/{{id}}", "summary": f"Delete {slug}", "category": cat})
    return endpoints


def _build_api_spec(state: dict) -> dict:
    """Construct the api_spec.json output from the final pipeline state."""
    is_hpe = state.get("is_hpe_oneview", False)
    schemas = ONEVIEW_RESOURCE_SCHEMAS if is_hpe else {}
    extracted = state.get("extracted_schemas", schemas)

    all_endpoints = []
    for slug, schema_data in extracted.items():
        cat = schema_data.get("category", "GENERAL")
        base = schema_data.get("base_path", f"/rest/{slug}")
        for ep in schema_data.get("endpoints", []):
            ep_full = dict(ep)
            ep_full.setdefault("category", cat)
            ep_full.setdefault("subcategory", slug)
            all_endpoints.append(ep_full)

    return {
        "title":           "HPE OneView / COM Mock API",
        "version":         "4600",
        "source_url":      state.get("source_url", ""),
        "total_endpoints": len(all_endpoints),
        "total_sections":  len(extracted),
        "endpoints":       all_endpoints,
        "sections":        [
            {"name": slug, "base_path": s.get("base_path", f"/rest/{slug}")}
            for slug, s in extracted.items()
        ],
    }
