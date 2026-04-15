"""
com_mock/agents/doc_fetcher.py
──────────────────────────────
Agent 1 — DocFetcherAgent

Recursively fetches API documentation pages starting from the source URL.
Follows links that look like API section pages (up to max_fetch_depth).

Key upgrades over the mentor's version:
  • Actually follows real links, doesn't just look at one page
  • Deduplicates visited URLs (no loops)
  • Cleans HTML → plain text before storing (smaller, easier for LLM)
  • Concurrently fetches up to 8 pages at a time
  • Detects HPE OneView URL → sets fast-path flag to skip extraction
"""

from __future__ import annotations

import asyncio
import logging
import re
from typing import Callable, Coroutine, Optional
from urllib.parse import urljoin, urlparse

import httpx

logger = logging.getLogger(__name__)

_HPE_HINTS = ["hpe.com", "oneview", "dp00003271"]

# Link patterns that suggest API section pages
_API_LINK_PATTERNS = re.compile(
    r'href=["\']([^"\'#?]+)["\']',
    re.IGNORECASE,
)

_SKIP_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".pdf", ".css", ".js",
    ".ico", ".svg", ".woff", ".ttf", ".zip",
}


def _is_hpe_oneview_url(url: str) -> bool:
    url_lower = url.lower()
    return any(hint in url_lower for hint in _HPE_HINTS)


def _clean_html(html: str) -> str:
    """Strip scripts, styles, and tags — return readable plain text."""
    text = re.sub(r"<script[^>]*>[\s\S]*?</script>", " ", html, flags=re.IGNORECASE)
    text = re.sub(r"<style[^>]*>[\s\S]*?</style>", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _extract_candidate_links(html: str, base_url: str, visited: set[str]) -> list[str]:
    """Extract links from HTML that look like API section pages."""
    parsed_base = urlparse(base_url)
    base_domain = parsed_base.netloc
    candidates: list[str] = []

    for match in _API_LINK_PATTERNS.finditer(html):
        href = match.group(1).strip()
        if not href or href.startswith(("javascript:", "mailto:", "#")):
            continue

        # Resolve to absolute URL
        full_url = urljoin(base_url, href)
        parsed = urlparse(full_url)

        # Stay on same domain
        if parsed.netloc != base_domain:
            continue

        # Skip binary files
        ext = "." + full_url.rsplit(".", 1)[-1].lower() if "." in full_url.rsplit("/", 1)[-1] else ""
        if ext in _SKIP_EXTENSIONS:
            continue

        # Skip already-visited
        if full_url in visited:
            continue

        # Only follow paths that look like API documentation
        path_lower = parsed.path.lower()
        api_hints = [
            "/rest/", "/api/", "/v1/", "/v2/", "/resource",
            "server", "storage", "network", "firmware", "setting",
            "hardware", "profile", "enclosure",
        ]
        if any(hint in path_lower for hint in api_hints):
            candidates.append(full_url)

    return list(dict.fromkeys(candidates))[:20]  # deduplicate, cap at 20 per page


async def _fetch_page(url: str, client: httpx.AsyncClient) -> Optional[str]:
    """Fetch one page and return HTML, or None on failure."""
    try:
        r = await client.get(url, timeout=15)
        r.raise_for_status()
        return r.text
    except Exception as exc:
        logger.debug("Failed to fetch %s: %s", url, exc)
        return None


async def run_doc_fetcher(
    state: dict,
    report: Callable[[str], Coroutine],
) -> dict:
    """
    LangGraph node: DocFetcherAgent

    Fetches the source URL and recursively follows links up to max_fetch_depth.
    Short-circuits to fast-path if the URL is HPE OneView.
    """
    source_url: str = state["source_url"]
    max_depth: int = state.get("max_fetch_depth", 2)

    await report(f"🌐 DocFetcherAgent starting: {source_url}")

    # ── Fast path: HPE OneView ────────────────────────────────────────────
    if _is_hpe_oneview_url(source_url):
        await report("⚡ Detected HPE OneView URL — activating fast-path (using seeded schemas)")
        return {
            "is_hpe_oneview":  True,
            "fetched_pages":   {},
            "visited_urls":    [source_url],
            "pages_to_fetch":  [],
            "status":          "mapping",
            "progress_log":    state.get("progress_log", []) + ["Fast-path: HPE OneView detected"],
        }

    # ── Normal path: recursive fetch ─────────────────────────────────────
    fetched_pages: dict[str, str] = {}
    visited: set[str] = set(state.get("visited_urls", []))
    to_fetch: list[tuple[str, int]] = [(source_url, 0)]  # (url, depth)

    headers = {
        "User-Agent": "COM-MockAgent/2.0 (API Documentation Crawler)",
        "Accept": "text/html,application/xhtml+xml",
    }

    async with httpx.AsyncClient(
        verify=False,
        follow_redirects=True,
        headers=headers,
    ) as client:
        while to_fetch:
            # Process up to 8 URLs concurrently per depth level
            current_batch = []
            while to_fetch and len(current_batch) < 8:
                url, depth = to_fetch.pop(0)
                if url not in visited:
                    current_batch.append((url, depth))
                    visited.add(url)

            if not current_batch:
                break

            # Concurrent fetch
            tasks = [_fetch_page(url, client) for url, _ in current_batch]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            for (url, depth), html in zip(current_batch, results):
                if isinstance(html, Exception) or html is None:
                    logger.debug("Skipped %s", url)
                    continue

                clean = _clean_html(html)
                fetched_pages[url] = clean[:12000]  # cap per-page size
                await report(f"  📄 Fetched ({depth}) {url[:70]} ({len(clean)} chars)")

                # Discover child links for next depth
                if depth < max_depth:
                    children = _extract_candidate_links(html, url, visited)
                    for child in children:
                        to_fetch.append((child, depth + 1))

    await report(f"✅ DocFetcherAgent: fetched {len(fetched_pages)} pages")

    if not fetched_pages:
        await report("⚠️  No pages fetched — will use generic sections")

    return {
        "is_hpe_oneview":  False,
        "fetched_pages":   fetched_pages,
        "visited_urls":    list(visited),
        "pages_to_fetch":  [],
        "status":          "extracting",
        "progress_log":    state.get("progress_log", [])
                           + [f"Fetched {len(fetched_pages)} pages"],
    }
