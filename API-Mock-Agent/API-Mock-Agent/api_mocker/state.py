"""
api_mocker/state.py
LangGraph state definition for the API crawler agent.

The state tracks every stage of the crawl → extract → generate pipeline.
"""

from __future__ import annotations

from typing import Annotated, Any

from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class APICrawlerState(TypedDict):
    """State passed between nodes in the API crawler LangGraph."""

    # LangChain message history (used for LLM context)
    messages: Annotated[list[BaseMessage], add_messages]

    # URL of the API documentation index page
    source_url: str

    # Discovered API sections: [{name, url, category_group}, ...]
    sections_discovered: list[dict]

    # Current processing batch index (sections are processed in batches)
    current_batch_idx: int

    # How many sections to process per LLM call
    batch_size: int

    # How many sample instances to generate per collection (default: 3)
    instance_count: int

    # Accumulated API endpoints (list of dicts matching APIEndpoint schema)
    discovered_endpoints: list[dict]

    # Generated mock response data: {"METHOD /path": {...}, ...}
    mock_data: dict[str, Any]

    # Pipeline status: discovering | extracting | generating | complete | error
    status: str

    # Accumulated errors (non-fatal)
    errors: list[str]

    # Human-readable progress log
    progress_log: list[str]
