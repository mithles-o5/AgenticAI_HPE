"""
com_mock/state.py
LangGraph state for the COM/OneView mock-generation pipeline.

Pipeline phases
───────────────
  PHASE 1  DocFetcher       → fetches raw documentation pages
  PHASE 2  SchemaExtractor  → extracts field schemas per resource (parallel)
  PHASE 3  RelationshipMapper → resolves cross-resource foreign-key graph
  PHASE 4  DataSynthesizer  → generates schema-compliant realistic instances
  PHASE 5  Validator        → checks referential integrity; sends failures back
  PHASE 6  DbSeeder         → persists approved data to SQLite
"""

from __future__ import annotations

from typing import Annotated, Any

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict


class COMCrawlerState(TypedDict):
    # ── LangChain message bus ────────────────────────────────────────────
    messages: Annotated[list[BaseMessage], add_messages]

    # ── Input ────────────────────────────────────────────────────────────
    source_url: str
    max_fetch_depth: int          # How deep to follow links (default: 2)
    instances_per_resource: int   # Sample items per collection (default: 5)
    output_dir: str

    # ── Phase 1: Doc Fetching ────────────────────────────────────────────
    # url → raw HTML content
    fetched_pages: dict[str, str]
    # URLs still in the fetch queue
    pages_to_fetch: list[str]
    # Tracks already-visited URLs to avoid loops
    visited_urls: list[str]

    # ── Phase 2: Schema Extraction ───────────────────────────────────────
    # resource_slug → extracted schema dict
    # e.g. "server-hardware" → {fields: {...}, ...}
    extracted_schemas: dict[str, dict]
    # Sub-batches dispatched (used by fan-out / fan-in)
    schema_batches_total: int
    schema_batches_done: int
    schema_extraction_errors: list[str]

    # ── Phase 3: Relationship Mapping ────────────────────────────────────
    # resource_slug → list of relationship descriptors
    # e.g. "server-hardware" → [{"field": "serverProfileUri", "target": "server-profiles", ...}]
    relationship_graph: dict[str, list[dict]]

    # ── Phase 4: Data Synthesis ──────────────────────────────────────────
    # resource_slug → list of synthesized resource dicts
    synthesized_data: dict[str, list[dict]]
    # Which resource types need re-synthesis (populated by validator)
    retry_resource_types: list[str]

    # ── Phase 5: Validation ──────────────────────────────────────────────
    # resource_slug → list of error messages
    validation_errors: dict[str, list[str]]
    # How many times each resource type has been retried
    validation_retries: dict[str, int]
    max_validation_retries: int   # default: 3

    # ── Phase 6: DB Seed ─────────────────────────────────────────────────
    seeded_resource_types: list[str]
    seeded_total_records: int

    # ── Final output ─────────────────────────────────────────────────────
    api_spec: dict[str, Any]

    # ── Pipeline control ─────────────────────────────────────────────────
    # one of: fetching | extracting | mapping | synthesizing | validating
    #         seeding | complete | error
    status: str
    is_hpe_oneview: bool          # fast-path flag — skips doc extraction
    errors: list[str]
    progress_log: list[str]
