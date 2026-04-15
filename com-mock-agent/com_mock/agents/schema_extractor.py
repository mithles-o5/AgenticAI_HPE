"""
com_mock/agents/schema_extractor.py
────────────────────────────────────
Agent 2 — SchemaExtractorAgent

Processes a batch of fetched doc pages and extracts real field schemas.
Unlike the mentor's version (which just sends section names to the LLM),
this agent sends actual page content and asks for structured field schemas.

Output per resource: {fields: {name: {type, values, min, max}}, endpoints: [...]}
"""

from __future__ import annotations

import json
import logging
import re
from typing import Any, Callable, Coroutine

from langchain_core.messages import HumanMessage, SystemMessage

logger = logging.getLogger(__name__)

SCHEMA_EXTRACT_SYSTEM = """\
You are an API schema analyst. Given raw text from an API documentation page,
extract the data model and REST endpoints for the resource described.

Return ONLY valid JSON (no markdown) with this structure:
{
  "resource_slug": "server-hardware",
  "type_name": "ServerHardwareV10",
  "base_path": "/rest/server-hardware",
  "fields": {
    "fieldName": {
      "type": "string|integer|boolean|enum|ref|array_ref",
      "values": ["only for enum"],
      "min": 0,
      "max": 100,
      "nullable": true,
      "required": false,
      "description": "short description"
    }
  },
  "endpoints": [
    {"method": "GET",  "path": "/rest/server-hardware",       "summary": "List all"},
    {"method": "GET",  "path": "/rest/server-hardware/{id}",  "summary": "Get one"},
    {"method": "POST", "path": "/rest/server-hardware",       "summary": "Create"},
    {"method": "PUT",  "path": "/rest/server-hardware/{id}",  "summary": "Update"},
    {"method": "DELETE","path": "/rest/server-hardware/{id}", "summary": "Delete"}
  ],
  "task_operations": ["POST", "PUT", "DELETE"]
}

Extract as many real fields as you can find in the page. Focus on field names,
their types, and allowed values. If you see enum values listed, include them."""


def _extract_json(text: str) -> Any:
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    m = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    if m:
        try:
            return json.loads(m.group(1))
        except json.JSONDecodeError:
            pass
    for start_char, end_char in [("{", "}"), ("[", "]")]:
        start = text.find(start_char)
        end = text.rfind(end_char)
        if start != -1 and end > start:
            try:
                return json.loads(text[start:end + 1])
            except json.JSONDecodeError:
                pass
    return None


async def run_schema_extractor_batch(
    pages_batch: list[tuple[str, str]],
    llm: Any,
    report: Callable[[str], Coroutine],
) -> dict[str, dict]:
    """
    Extract schemas from a batch of (url, text) page pairs.
    Returns dict of resource_slug → schema_dict.
    """
    extracted: dict[str, dict] = {}

    for url, page_text in pages_batch:
        if not page_text.strip():
            continue

        await report(f"  🔬 SchemaExtractor: processing {url[:60]}")

        try:
            response = await llm.ainvoke([
                SystemMessage(content=SCHEMA_EXTRACT_SYSTEM),
                HumanMessage(content=f"API documentation page:\n\n{page_text[:8000]}"),
            ])

            data = _extract_json(response.content)
            if not data or not isinstance(data, dict):
                continue

            slug = data.get("resource_slug", "")
            if not slug:
                continue

            extracted[slug] = data
            field_count = len(data.get("fields", {}))
            ep_count = len(data.get("endpoints", []))
            await report(f"    ✅ {slug}: {field_count} fields, {ep_count} endpoints")

        except Exception as exc:
            logger.warning("Schema extraction failed for %s: %s", url, exc)
            await report(f"    ⚠️  Extraction failed for {url[:50]}: {type(exc).__name__}")

    return extracted
