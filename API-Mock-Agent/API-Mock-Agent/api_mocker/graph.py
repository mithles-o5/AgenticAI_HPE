"""
api_mocker/graph.py
LangGraph agent graph for API documentation crawling and mock generation.

Graph topology
──────────────
  START → discover_sections → extract_batch ──┐
                                  ▲            │
                                  │ (more)     │
                                  └────────────┘
                                       │ (done)
                                       ▼
                                   finalize → END

Nodes
─────
  discover_sections  – Fetch the docs index page, discover all API sections.
  extract_batch      – For each batch of sections, use the LLM to extract
                       REST API endpoints with sample responses.
  finalize           – Assemble the full API spec & mock data, save to JSON.
"""

from __future__ import annotations

import json
import logging
import os
import re
from typing import Any, Callable, Coroutine, Literal, Optional

import httpx
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import END, START, StateGraph

from api_mocker.llm_provider import create_llm, list_providers
from api_mocker.state import APICrawlerState

logger = logging.getLogger(__name__)

# ── Configuration ────────────────────────────────────────────────────────────

BATCH_SIZE = 5  # Sections per LLM call

# ── Prompts ──────────────────────────────────────────────────────────────────

DISCOVER_PROMPT = """\
You are an API documentation analyst.  Given the HTML content of an API
documentation page, extract EVERY API section / resource group listed.

Look for navigation menus, sidebar links, table-of-contents, or headings
that represent distinct API resource groups or categories.

Return a JSON array where each element has:
  "name"           : section display name (e.g. "Users", "Server Hardware")
  "url"            : relative or absolute URL to the section page (if visible) or ""
  "category_group" : parent group in UPPER CASE (e.g. "RESOURCES", "AUTH")

Include ALL sections you can find.  Be thorough.

Return ONLY the JSON array.  No markdown fences, no explanation."""

EXTRACT_PROMPT = """\
Generate REST API endpoints for these API sections:
{sections_text}

Rules:
- Path convention: {base_path}/<resource-kebab-case>
- Standard CRUD: GET (list), GET /{{id}}, POST, PUT /{{id}}, DELETE /{{id}}
- Collection GET returns: {{"items":[...], "count":N, "total":N}}
- Include {instance_count} realistic sample items per collection, each with unique IDs and varied data
- Use UUID format for IDs (each item gets a different UUID)

Return JSON (NO markdown):
{{"sections":[{{"name":"...","endpoints":[{{"method":"GET","path":"...","summary":"...","parameters":[],"response_example":{{...}}}}]}}]}}"""

# ── HPE OneView fallback section list (used ONLY when URL matches HPE docs) ──

HPE_KNOWN_SECTIONS: list[dict[str, str]] = [
    # SERVERS
    {"name": "Rack Managers", "category_group": "SERVERS", "url": ""},
    {"name": "Server Hardware", "category_group": "SERVERS", "url": ""},
    {"name": "Server Hardware Migration", "category_group": "SERVERS", "url": ""},
    {"name": "Server Hardware Types", "category_group": "SERVERS", "url": ""},
    {"name": "Server Profile Templates", "category_group": "SERVERS", "url": ""},
    {"name": "Server Profiles", "category_group": "SERVERS", "url": ""},
    # NETWORKING
    {"name": "Ethernet Networks", "category_group": "NETWORKING", "url": ""},
    {"name": "FC Networks", "category_group": "NETWORKING", "url": ""},
    {"name": "Network Sets", "category_group": "NETWORKING", "url": ""},
    # STORAGE
    {"name": "Storage Pools", "category_group": "STORAGE", "url": ""},
    {"name": "Storage Systems", "category_group": "STORAGE", "url": ""},
    {"name": "Storage Templates", "category_group": "STORAGE", "url": ""},
    {"name": "Storage Volume Attachments", "category_group": "STORAGE", "url": ""},
    {"name": "Storage Volume Sets", "category_group": "STORAGE", "url": ""},
    {"name": "Volumes", "category_group": "STORAGE", "url": ""},
    # FC-SANS
    {"name": "Endpoints", "category_group": "FC-SANS", "url": ""},
    {"name": "Managed SANs", "category_group": "FC-SANS", "url": ""},
    {"name": "Providers", "category_group": "FC-SANS", "url": ""},
    {"name": "SAN Managers", "category_group": "FC-SANS", "url": ""},
    # FACILITIES
    {"name": "Datacenters", "category_group": "FACILITIES", "url": ""},
    {"name": "Power Devices", "category_group": "FACILITIES", "url": ""},
    {"name": "Racks", "category_group": "FACILITIES", "url": ""},
    {"name": "Unmanaged Devices", "category_group": "FACILITIES", "url": ""},
    # HYPERVISORS
    {"name": "Hypervisor Managers", "category_group": "HYPERVISORS", "url": ""},
    {"name": "Hypervisor Cluster Profiles", "category_group": "HYPERVISORS", "url": ""},
    {"name": "Hypervisor Host Profiles", "category_group": "HYPERVISORS", "url": ""},
    # DATA SERVICES
    {"name": "Metric Streaming", "category_group": "DATA SERVICES", "url": ""},
    {"name": "Remote Syslog", "category_group": "DATA SERVICES", "url": ""},
    # FIRMWARE
    {"name": "Firmware Bundles", "category_group": "FIRMWARE", "url": ""},
    {"name": "Firmware Drivers", "category_group": "FIRMWARE", "url": ""},
    {"name": "Hardware-Compliance", "category_group": "FIRMWARE", "url": ""},
    {"name": "Repositories", "category_group": "FIRMWARE", "url": ""},
    {"name": "Updates", "category_group": "FIRMWARE", "url": ""},
    # ACTIVITY
    {"name": "Alerts", "category_group": "ACTIVITY", "url": ""},
    {"name": "Audit Logs", "category_group": "ACTIVITY", "url": ""},
    {"name": "Audit Log Forwarding", "category_group": "ACTIVITY", "url": ""},
    {"name": "Events", "category_group": "ACTIVITY", "url": ""},
    {"name": "Reports", "category_group": "ACTIVITY", "url": ""},
    {"name": "Tasks", "category_group": "ACTIVITY", "url": ""},
    # SETTINGS
    {"name": "Appliance EULA", "category_group": "SETTINGS", "url": ""},
    {"name": "Appliance Firmware", "category_group": "SETTINGS", "url": ""},
    {"name": "Appliance Health-status", "category_group": "SETTINGS", "url": ""},
    {"name": "Appliance Network Interfaces", "category_group": "SETTINGS", "url": ""},
    {"name": "Appliance Node Information", "category_group": "SETTINGS", "url": ""},
    {"name": "Appliance Proxy Configuration", "category_group": "SETTINGS", "url": ""},
    {"name": "Appliance SNMPv1 Trap Destinations", "category_group": "SETTINGS", "url": ""},
    {"name": "Appliance SNMPv3 Trap Destinations", "category_group": "SETTINGS", "url": ""},
    {"name": "Appliance SSH Access", "category_group": "SETTINGS", "url": ""},
    {"name": "Appliance Time and Locale Configuration", "category_group": "SETTINGS", "url": ""},
    {"name": "Backups", "category_group": "SETTINGS", "url": ""},
    {"name": "Domains", "category_group": "SETTINGS", "url": ""},
    {"name": "Email notification", "category_group": "SETTINGS", "url": ""},
    {"name": "Global Settings", "category_group": "SETTINGS", "url": ""},
    {"name": "HA Nodes", "category_group": "SETTINGS", "url": ""},
    {"name": "Licenses", "category_group": "SETTINGS", "url": ""},
    {"name": "Restores", "category_group": "SETTINGS", "url": ""},
    {"name": "Scopes", "category_group": "SETTINGS", "url": ""},
    {"name": "Version", "category_group": "SETTINGS", "url": ""},
    # SECURITY
    {"name": "Active User Sessions", "category_group": "SECURITY", "url": ""},
    {"name": "Appliance Certificates", "category_group": "SECURITY", "url": ""},
    {"name": "Authorizations", "category_group": "SECURITY", "url": ""},
    {"name": "Certificate Authority", "category_group": "SECURITY", "url": ""},
    {"name": "Login Sessions", "category_group": "SECURITY", "url": ""},
    {"name": "Login Domains", "category_group": "SECURITY", "url": ""},
    {"name": "Roles", "category_group": "SECURITY", "url": ""},
    {"name": "Users", "category_group": "SECURITY", "url": ""},
    {"name": "Sessions", "category_group": "SECURITY", "url": ""},
    # SEARCH
    {"name": "Index Resources", "category_group": "SEARCH", "url": ""},
    {"name": "Labels", "category_group": "SEARCH", "url": ""},
]


# ── URL detection helpers ────────────────────────────────────────────────────

def _is_hpe_oneview_url(url: str) -> bool:
    """Check if the URL points to HPE OneView documentation."""
    url_lower = url.lower()
    return any(
        hint in url_lower
        for hint in ["hpe.com", "oneview", "dp00003271"]
    )


def _detect_base_path(state: dict) -> str:
    """Detect the base path convention from the source URL or existing endpoints.

    Heuristics:
      - HPE OneView URLs → /rest
      - URLs containing /api/v → /api/v{n}
      - URLs containing /v1, /v2 etc → /v{n}
      - Default → /api
    """
    url = state.get("source_url", "")
    if _is_hpe_oneview_url(url):
        return "/rest"
    # Check for /api/v{n} pattern in URL
    m = re.search(r"(/api/v\d+)", url)
    if m:
        return m.group(1)
    # Check for /v{n} pattern
    m = re.search(r"(/v\d+)", url)
    if m:
        return f"/api{m.group(1)}"
    # Check existing endpoints
    endpoints = state.get("discovered_endpoints", [])
    if endpoints:
        paths = [ep.get("path", "") for ep in endpoints[:5]]
        for p in paths:
            m = re.match(r"(/[^/]+)", p)
            if m:
                return m.group(1)
    return "/api"


def _parse_sections_from_html(html: str, base_url: str) -> list[dict[str, str]]:
    """Parse API sections from HTML using common documentation patterns.

    Looks for navigation links, sidebar items, and heading patterns that
    indicate API resource sections.  Works with Swagger, ReadTheDocs,
    Slate/Shins, Redoc, custom docs, and plain HTML with anchor links.
    """
    from urllib.parse import urljoin

    sections: list[dict[str, str]] = []
    seen_names: set[str] = set()

    # ── Pattern 1: Swagger / OpenAPI tag groups ──────────────────────────
    # Look for <a class="...tag..." href="..."> patterns
    tag_patterns = [
        # Swagger UI / Redoc tag links
        r'<a[^>]*class="[^"]*(?:opblock-tag|menu-item|tag)[^"]*"[^>]*>\s*([^<]+)',
        # Navigation sidebar links (common in doc generators)
        r'<a[^>]*class="[^"]*(?:nav-link|sidebar-link|toc-link|menu-link)[^"]*"[^>]*href="([^"]*)"[^>]*>\s*([^<]+)',
        # Generic sidebar list items
        r'<li[^>]*class="[^"]*(?:sidebar|nav|toc|menu)[^"]*"[^>]*>\s*<a[^>]*href="([^"]*)"[^>]*>\s*([^<]+)',
    ]

    for pattern in tag_patterns:
        for match in re.finditer(pattern, html, re.IGNORECASE):
            groups = match.groups()
            if len(groups) == 1:
                name = groups[0].strip()
                url = ""
            elif len(groups) == 2:
                url, name = groups[0].strip(), groups[1].strip()
            else:
                continue

            name = re.sub(r"\s+", " ", name).strip()
            if not name or len(name) < 2 or len(name) > 80:
                continue
            if name.lower() in seen_names:
                continue

            # Skip non-API nav items
            skip_words = {"home", "overview", "introduction", "getting started",
                          "authentication", "changelog", "contact", "support",
                          "faq", "about", "search", "login", "logout", "back"}
            if name.lower() in skip_words:
                continue

            seen_names.add(name.lower())
            sections.append({
                "name": name,
                "category_group": _guess_category(name),
                "url": urljoin(base_url, url) if url else "",
            })

    # ── Pattern 2: Heading-based sections (h1/h2/h3 with API-like names) ─
    if not sections:
        heading_re = r"<h[1-3][^>]*(?:id=\"([^\"]*)\")?\s*[^>]*>\s*([^<]+)"
        api_indicators = re.compile(
            r"(?:api|endpoint|resource|route|method|service|operation)",
            re.IGNORECASE,
        )
        for match in re.finditer(heading_re, html, re.IGNORECASE):
            heading_id = match.group(1) or ""
            heading_text = match.group(2).strip()
            heading_text = re.sub(r"\s+", " ", heading_text)
            if not heading_text or len(heading_text) < 2 or len(heading_text) > 80:
                continue
            # Only include headings that look API-related or are after an API-related heading
            context = html[max(0, match.start() - 500):match.start()]
            if api_indicators.search(heading_text) or api_indicators.search(context):
                if heading_text.lower() not in seen_names:
                    seen_names.add(heading_text.lower())
                    url = f"#{heading_id}" if heading_id else ""
                    sections.append({
                        "name": heading_text,
                        "category_group": _guess_category(heading_text),
                        "url": url,
                    })

    # ── Pattern 3: OpenAPI/Swagger JSON embedded in the page ─────────────
    if not sections:
        spec_match = re.search(r'"paths"\s*:\s*\{([^}]+(?:\{[^}]*\}[^}]*)*)\}', html)
        if spec_match:
            paths_text = spec_match.group(0)
            path_re = re.findall(r'"(/[^"]+)"', paths_text)
            for p in path_re:
                # Extract the resource name from the path
                parts = [x for x in p.split("/") if x and not x.startswith("{")]
                if parts:
                    resource = parts[-1].replace("-", " ").replace("_", " ").title()
                    if resource.lower() not in seen_names:
                        seen_names.add(resource.lower())
                        sections.append({
                            "name": resource,
                            "category_group": _guess_category(resource),
                            "url": "",
                        })

    return sections


def _guess_category(name: str) -> str:
    """Guess a category group for a section name."""
    name_lower = name.lower()
    category_hints = {
        "AUTH": ["auth", "login", "session", "token", "oauth", "user", "role",
                 "permission", "credential", "password", "certificate", "security"],
        "RESOURCES": ["server", "device", "machine", "instance", "node", "host",
                      "cluster", "compute", "hardware", "rack", "pool"],
        "NETWORKING": ["network", "ethernet", "fc ", "vlan", "subnet", "dns",
                       "port", "interface", "connection", "route", "firewall"],
        "STORAGE": ["storage", "volume", "disk", "snapshot", "backup",
                    "repository", "bucket", "blob", "file"],
        "MONITORING": ["alert", "event", "log", "metric", "audit", "report",
                       "health", "status", "monitor", "notification", "task"],
        "CONFIG": ["setting", "config", "preference", "option", "global",
                   "eula", "license", "domain", "scope", "version", "firmware"],
    }
    for cat, hints in category_hints.items():
        for hint in hints:
            if hint in name_lower:
                return cat
    return "GENERAL"


# ── Helpers ──────────────────────────────────────────────────────────────────

def _extract_json(text: str) -> Any:
    """Try to extract JSON from LLM output (handles markdown fences)."""
    # Try raw parse first
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    # Strip markdown code fences
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass
    # Try to find the first [ or { and parse from there
    for start_char, end_char in [("[", "]"), ("{", "}")]:
        start = text.find(start_char)
        end = text.rfind(end_char)
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(text[start : end + 1])
            except json.JSONDecodeError:
                pass
    raise ValueError(f"Could not extract JSON from LLM response: {text[:200]}...")


# ── Sample data generator ────────────────────────────────────────────────────

# Varied names/adjectives used to make each simulated instance distinct
_ADJECTIVES = [
    "Primary", "Secondary", "Backup", "Staging", "Production",
    "Dev", "Test", "QA", "Demo", "Legacy", "New", "Temp",
    "Regional", "Global", "Local", "Internal", "External",
    "Alpha", "Beta", "Gamma", "Delta", "Core", "Edge",
    "Main", "Aux", "DR", "Archive", "Hot-Standby", "Pilot",
    "Lab", "Sandbox", "Canary", "Baseline", "Mirror", "Replica",
    "North", "South", "East", "West", "Central", "Default",
    "Custom", "Shared", "Dedicated", "Managed", "Unmanaged",
    "Express", "Premium", "Standard", "Basic", "Advanced",
]

_STATUSES = ["active", "inactive", "provisioning", "error", "maintenance",
             "ready", "warning", "degraded", "disabled", "pending"]


def _generate_sample_items(
    section_name: str, path: str, count: int = 3
) -> list[dict]:
    """Generate `count` varied sample items for a given resource type.

    Each item gets a unique UUID, distinct name, and rotated status so that
    mock collections look realistic during development / testing.
    """
    import hashlib

    resource_type = section_name.lower().replace(" ", "_")
    items: list[dict] = []

    for i in range(max(1, count)):
        # Deterministic but unique UUID per (section + index)
        seed = f"{section_name}:{i}"
        uid = hashlib.md5(seed.encode()).hexdigest()
        uuid_str = f"{uid[:8]}-{uid[8:12]}-{uid[12:16]}-{uid[16:20]}-{uid[20:32]}"

        adj = _ADJECTIVES[i % len(_ADJECTIVES)]
        status = _STATUSES[i % len(_STATUSES)]

        # Stagger created/modified dates so items look like they were added over time
        day = str((i % 28) + 1).zfill(2)
        hour = str((i * 3) % 24).zfill(2)

        items.append({
            "id": uuid_str,
            "type": resource_type,
            "uri": f"{path}/{uuid_str}",
            "name": f"{adj} {section_name} {i + 1}",
            "description": f"Auto-generated sample {section_name.lower()} instance #{i + 1}",
            "status": status,
            "created": f"2025-06-{day}T{hour}:30:00.000Z",
            "modified": f"2025-06-{day}T{hour}:45:00.000Z",
        })

    return items


def _default_collection_response(
    section_name: str, path: str, instance_count: int = 3
) -> dict:
    """Generate a default collection response template with N items."""
    items = _generate_sample_items(section_name, path, instance_count)
    return {
        "type": f"{section_name.lower().replace(' ', '_')}_list",
        "uri": path,
        "count": len(items),
        "total": len(items),
        "start": 0,
        "items": items,
        "created": "2025-06-15T10:30:00.000Z",
        "modified": "2025-06-15T10:30:00.000Z",
    }


def _default_single_response(section_name: str, path: str) -> dict:
    """Generate a default single-resource response template."""
    return {
        "type": section_name.lower().replace(" ", "_"),
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "uri": f"{path}/550e8400-e29b-41d4-a716-446655440000",
        "name": f"Sample {section_name}",
        "status": "active",
        "created": "2025-06-15T10:30:00.000Z",
        "modified": "2025-06-15T10:30:00.000Z",
    }


def _default_task_response() -> dict:
    return {
        "type": "task",
        "id": "7b0a5f25-4444-4444-4444-e2c73acf3e6e",
        "uri": "/tasks/7b0a5f25-4444-4444-4444-e2c73acf3e6e",
        "name": "Async Operation",
        "state": "completed",
        "status": "success",
        "created": "2025-06-15T10:30:00.000Z",
        "modified": "2025-06-15T10:30:00.000Z",
    }


# ── Graph factory ────────────────────────────────────────────────────────────

ProgressCallback = Optional[Callable[[str], Coroutine[Any, Any, None]]]


def build_api_crawler_graph(
    progress_callback: ProgressCallback = None,
    llm: Optional[BaseChatModel] = None,
    provider: Optional[str] = None,
    model: Optional[str] = None,
):
    """
    Build and compile the LangGraph for API documentation crawling.

    Args:
        progress_callback: Optional async function called with progress messages.
        llm: Optional pre-configured LLM instance.
        provider: LLM provider name (groq, gemini, ollama, huggingface, anthropic).
                  If None, auto-detects from available API keys.
        model: Optional model name override for the chosen provider.

    Returns:
        Compiled LangGraph that accepts APICrawlerState.
    """

    if llm is None:
        llm = create_llm(provider=provider, model=model)

    async def _report(msg: str) -> None:
        logger.info(msg)
        if progress_callback:
            await progress_callback(msg)

    # ─── Node 1: Discover Sections ───────────────────────────────────────

    async def discover_sections(state: APICrawlerState) -> dict:
        """Discover API sections from any documentation URL.

        Strategy (in order):
          1. Check if URL matches HPE OneView → use curated HPE section list
          2. Fetch the HTML and try to parse nav/sidebar/TOC for sections
          3. If HTML parsing yields sections → use them (optionally refine via LLM)
          4. If HTML parsing fails → send HTML to LLM for extraction
          5. Last resort → generate a generic single-section fallback
        """
        url = state["source_url"]
        await _report(f"📖 API documentation source: {url}")

        # ── Strategy 1: HPE OneView shortcut ─────────────────────────────
        if _is_hpe_oneview_url(url):
            sections = HPE_KNOWN_SECTIONS.copy()
            await _report(
                f"✅ Recognized HPE OneView docs — loaded {len(sections)} known sections"
            )
            return {
                "sections_discovered": sections,
                "current_batch_idx": 0,
                "batch_size": state.get("batch_size", BATCH_SIZE),
                "status": "extracting",
                "errors": state.get("errors", []),
                "progress_log": state.get("progress_log", [])
                + [f"HPE OneView: loaded {len(sections)} known sections"],
            }

        # ── Fetch the documentation page ─────────────────────────────────
        html = ""
        try:
            async with httpx.AsyncClient(
                verify=False, follow_redirects=True, timeout=30
            ) as client:
                r = await client.get(url)
                r.raise_for_status()
                html = r.text
                await _report(f"📥 Fetched {len(html)} bytes from docs page")
        except BaseException as exc:
            await _report(f"⚠️  Could not fetch docs page: {exc}")

        # ── Strategy 2: Parse HTML for nav / sidebar / TOC ───────────────
        sections: list[dict[str, str]] = []
        if html:
            sections = _parse_sections_from_html(html, url)
            if sections:
                await _report(
                    f"✅ Parsed {len(sections)} API sections from HTML structure"
                )

        # ── Strategy 3: Use LLM to extract sections from HTML ────────────
        if not sections and html and llm is not None:
            await _report("🤖 Using LLM to discover API sections from page...")
            try:
                # Send a trimmed version of the HTML to the LLM
                clean_text = re.sub(r"<script[^>]*>[\s\S]*?</script>", "", html)
                clean_text = re.sub(r"<style[^>]*>[\s\S]*?</style>", "", clean_text)
                clean_text = re.sub(r"<[^>]+>", " ", clean_text)
                clean_text = re.sub(r"\s+", " ", clean_text).strip()
                # Limit to ~8000 chars for small models
                clean_text = clean_text[:8000]

                response = await llm.ainvoke(
                    [
                        SystemMessage(
                            content="You are an API documentation analyst. "
                            "Return ONLY valid JSON. No markdown."
                        ),
                        HumanMessage(content=DISCOVER_PROMPT + "\n\nPage content:\n" + clean_text),
                    ]
                )
                parsed = _extract_json(response.content)
                if isinstance(parsed, list) and len(parsed) > 0:
                    sections = parsed
                    await _report(
                        f"✅ LLM discovered {len(sections)} API sections"
                    )
            except BaseException as exc:
                await _report(
                    f"⚠️  LLM discovery failed: {type(exc).__name__}: {str(exc)[:100]}"
                )

        # ── Strategy 4: Generic fallback ─────────────────────────────────
        if not sections:
            await _report(
                "⚠️  Could not discover sections — creating generic API section"
            )
            sections = [
                {"name": "API", "category_group": "GENERAL", "url": url}
            ]

        return {
            "sections_discovered": sections,
            "current_batch_idx": 0,
            "batch_size": state.get("batch_size", BATCH_SIZE),
            "status": "extracting",
            "errors": state.get("errors", []),
            "progress_log": state.get("progress_log", [])
            + [f"Discovered {len(sections)} sections"],
        }

    # ─── Node 2: Extract Batch ───────────────────────────────────────────

    async def extract_batch(state: APICrawlerState) -> dict:
        """Extract endpoints for the current batch of sections via the LLM."""
        idx = state["current_batch_idx"]
        bs = state.get("batch_size", BATCH_SIZE)
        sections = state["sections_discovered"]
        batch = sections[idx : idx + bs]

        batch_num = (idx // bs) + 1
        total_batches = (len(sections) + bs - 1) // bs
        await _report(
            f"\n🔍 Batch {batch_num}/{total_batches}  —  "
            f"Processing: {', '.join(s['name'] for s in batch)}"
        )

        # Build the section text for the prompt
        sections_text_parts: list[str] = []
        for i, sec in enumerate(batch, 1):
            page_content = ""
            # Attempt to fetch the section page for richer extraction
            sec_url = sec.get("url", "")
            if sec_url:
                try:
                    base = state["source_url"].rsplit("/", 1)[0]
                    full_url = (
                        sec_url
                        if sec_url.startswith("http")
                        else f"{base}/{sec_url}"
                    )
                    async with httpx.AsyncClient(
                        verify=False, follow_redirects=True, timeout=12
                    ) as client:
                        r = await client.get(full_url)
                        if r.status_code == 200:
                            text = re.sub(r"<[^>]+>", " ", r.text)
                            text = re.sub(r"\s+", " ", text).strip()
                            page_content = text[:2000]
                except Exception:
                    pass

            entry = f"{i}. {sec['name']} (Category: {sec.get('category_group', 'GENERAL')})"
            if page_content:
                entry += f"\n   Page content: {page_content}"
            else:
                entry += "\n   (No page content — generate standard REST CRUD endpoints)"
            sections_text_parts.append(entry)

        sections_text = "\n\n".join(sections_text_parts)
        # Detect base path convention from existing endpoints or URL
        base_path = _detect_base_path(state)
        n_instances = state.get("instance_count", 3)
        prompt = EXTRACT_PROMPT.format(
            sections_text=sections_text,
            base_path=base_path,
            instance_count=n_instances,
        )

        new_endpoints: list[dict] = []
        errors: list[str] = []

        try:
            response = await llm.ainvoke(
                [
                    SystemMessage(
                        content="You are a REST API expert. "
                        "Return ONLY valid JSON. No markdown."
                    ),
                    HumanMessage(content=prompt),
                ]
            )

            data = _extract_json(response.content)

            # Handle both formats: {"sections": [...]} or [...]
            if isinstance(data, dict) and "sections" in data:
                result_sections = data["sections"]
            elif isinstance(data, list):
                result_sections = data
            else:
                raise ValueError(f"Unexpected JSON structure: {type(data)}")

            for sec_result in result_sections:
                sec_name = sec_result.get("name", "")
                eps = sec_result.get("endpoints", [])
                cat_group = ""
                # Find the category group from the batch
                for b in batch:
                    if b["name"].lower() == sec_name.lower():
                        cat_group = b.get("category_group", "")
                        break

                for ep in eps:
                    ep["category"] = cat_group or ep.get("category", "")
                    ep["subcategory"] = sec_name or ep.get("subcategory", "")
                    new_endpoints.append(ep)

            await _report(
                f"   ✅ Extracted {len(new_endpoints)} endpoints from batch"
            )

        except BaseException as exc:
            errors.append(f"Batch extraction failed (batch {batch_num}): {exc}")
            await _report(f"   ⚠️  LLM error (using fallback): {type(exc).__name__}: {str(exc)[:100]}")
            # Generate fallback CRUD endpoints for each section in the batch
            bp = _detect_base_path(state)
            n_inst = state.get("instance_count", 3)
            for sec in batch:
                new_endpoints.extend(_fallback_crud(sec, base_path=bp, instance_count=n_inst))
            await _report(
                f"   ↳ Generated {len(new_endpoints)} fallback endpoints"
            )

        return {
            "discovered_endpoints": state.get("discovered_endpoints", [])
            + new_endpoints,
            "current_batch_idx": idx + bs,
            "errors": state.get("errors", []) + errors,
            "progress_log": state.get("progress_log", [])
            + [
                f"Batch {batch_num}: extracted {len(new_endpoints)} endpoints"
            ],
        }

    # ─── Node 3: Finalize ────────────────────────────────────────────────

    async def finalize(state: APICrawlerState) -> dict:
        """Build the final mock_data mapping and mark complete."""
        endpoints = state.get("discovered_endpoints", [])
        n_instances = state.get("instance_count", 3)
        await _report(
            f"\n🏗️  Finalizing — {len(endpoints)} total endpoints discovered "
            f"({n_instances} instances per collection)"
        )

        mock_data: dict[str, Any] = {}

        for ep in endpoints:
            method = ep.get("method", "GET")
            path = ep.get("path", "")
            key = f"{method} {path}"

            # Use existing response_example if present
            if ep.get("response_example"):
                mock_data[key] = ep["response_example"]
            else:
                # Generate template-based defaults
                subcategory = ep.get("subcategory", "Resource")
                if method == "GET" and "{" not in path:
                    mock_data[key] = _default_collection_response(
                        subcategory, path, n_instances
                    )
                elif method == "GET":
                    mock_data[key] = _default_single_response(subcategory, path)
                elif method in ("POST", "PUT", "PATCH"):
                    mock_data[key] = _default_task_response()
                elif method == "DELETE":
                    mock_data[key] = None  # 204 No Content
                else:
                    mock_data[key] = {"status": "ok"}

        await _report(f"✅ Generated mock data for {len(mock_data)} endpoint(s)")
        await _report(f"📊 Summary: {len(state['sections_discovered'])} sections, "
                       f"{len(endpoints)} endpoints")

        return {
            "mock_data": mock_data,
            "status": "complete",
            "progress_log": state.get("progress_log", [])
            + [f"Finalized {len(mock_data)} mock responses"],
        }

    # ─── Routing ─────────────────────────────────────────────────────────

    def route_after_extraction(
        state: APICrawlerState,
    ) -> Literal["extract_batch", "finalize"]:
        idx = state["current_batch_idx"]
        total = len(state["sections_discovered"])
        if idx < total:
            return "extract_batch"
        return "finalize"

    # ─── Assemble graph ──────────────────────────────────────────────────

    graph = StateGraph(APICrawlerState)

    graph.add_node("discover_sections", discover_sections)
    graph.add_node("extract_batch", extract_batch)
    graph.add_node("finalize", finalize)

    graph.add_edge(START, "discover_sections")
    graph.add_edge("discover_sections", "extract_batch")
    graph.add_conditional_edges("extract_batch", route_after_extraction)
    graph.add_edge("finalize", END)

    return graph.compile()


# ── Fallback CRUD generator ─────────────────────────────────────────────────

def _fallback_crud(
    section: dict, base_path: str = "/api", instance_count: int = 3
) -> list[dict]:
    """Generate standard CRUD endpoints for a section when LLM fails.

    Args:
        section: Section dict with 'name' and 'category_group'.
        base_path: Base path prefix (e.g. '/rest', '/api/v1', '/v2').
        instance_count: Number of sample items in collection responses.
    """
    name = section.get("name", "Resource")
    cat = section.get("category_group", "GENERAL")
    slug = name.lower().replace(" ", "-")
    path = f"{base_path}/{slug}"

    common_query = [
        {"name": "offset", "location": "query", "param_type": "integer",
         "required": False, "description": "Pagination offset"},
        {"name": "limit", "location": "query", "param_type": "integer",
         "required": False, "description": "Page size"},
        {"name": "filter", "location": "query", "param_type": "string",
         "required": False, "description": "Filter expression"},
        {"name": "sort", "location": "query", "param_type": "string",
         "required": False, "description": "Sort field"},
    ]

    id_param = {
        "name": "id", "location": "path", "param_type": "string",
        "required": True, "description": f"{name} identifier",
    }

    sample_items = _generate_sample_items(name, path, instance_count)
    first_item = sample_items[0] if sample_items else {}

    return [
        {
            "method": "GET", "path": path,
            "summary": f"List all {name}",
            "category": cat, "subcategory": name,
            "parameters": common_query,
            "response_example": {
                "items": sample_items,
                "count": len(sample_items),
                "total": len(sample_items),
                "offset": 0, "uri": path,
            },
        },
        {
            "method": "GET", "path": f"{path}/{{id}}",
            "summary": f"Get {name} by ID",
            "category": cat, "subcategory": name,
            "parameters": [id_param],
            "response_example": first_item,
        },
        {
            "method": "POST", "path": path,
            "summary": f"Create {name}",
            "category": cat, "subcategory": name,
            "parameters": [],
            "request_body": {"name": f"New {name}"},
            "response_example": {**first_item, "id": "new-resource-uuid"},
        },
        {
            "method": "PUT", "path": f"{path}/{{id}}",
            "summary": f"Update {name}",
            "category": cat, "subcategory": name,
            "parameters": [id_param],
            "request_body": {"name": f"Updated {name}"},
            "response_example": first_item,
        },
        {
            "method": "DELETE", "path": f"{path}/{{id}}",
            "summary": f"Delete {name}",
            "category": cat, "subcategory": name,
            "parameters": [id_param],
            "response_example": None,
        },
    ]
