"""
api_mocker/mock_server.py
Dynamic FastAPI mock server generated from discovered API specifications.

Features
────────
- Automatic route registration from the discovered API spec JSON
- In-memory CRUD store — POST/PUT/DELETE actually mutate state
- Pagination support (start, count query params)
- Basic filter support
- Full Swagger / OpenAPI docs at /docs
- CORS enabled for browser-based testing
"""

from __future__ import annotations

import json
import logging
import os
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from fastapi import FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


# ── In-memory mock data store ────────────────────────────────────────────────


class MockDataStore:
    """
    In-memory store that holds resource collections.

    Initialised from the mock_data.json produced by the crawler graph.
    Supports basic CRUD so POST/PUT/DELETE requests actually work.
    """

    def __init__(self) -> None:
        # collection_path → list[dict]
        self.collections: dict[str, list[dict]] = {}
        # "METHOD /path" → static response (for non-collection endpoints)
        self.static_responses: dict[str, Any] = {}

    def load(self, endpoints: list[dict], mock_data: dict[str, Any]) -> None:
        """Populate the store from the crawler output."""
        for ep in endpoints:
            method = ep.get("method", "GET")
            path = ep.get("path", "")
            key = f"{method} {path}"
            data = mock_data.get(key)

            if method == "GET" and "{" not in path:
                # Collection endpoint — store members/items
                if isinstance(data, dict):
                    items = data.get("members") or data.get("items") or []
                    if items:
                        self.collections[path] = list(items)
                    else:
                        self.collections.setdefault(path, [])
                else:
                    self.collections.setdefault(path, [])
                self.static_responses[key] = data
            else:
                self.static_responses[key] = data

    # ── CRUD helpers ─────────────────────────────────────────────────────

    def get_collection(
        self,
        path: str,
        start: int = 0,
        count: int = 50,
        filter_str: Optional[str] = None,
        sort: Optional[str] = None,
    ) -> dict:
        items = self.collections.get(path, [])

        # Basic text filter
        if filter_str:
            items = [
                i
                for i in items
                if filter_str.lower() in json.dumps(i).lower()
            ]

        # Basic sort
        if sort:
            field = sort.split(":")[0].strip()
            reverse = "desc" in sort.lower()
            items = sorted(
                items,
                key=lambda x: str(x.get(field, "")),
                reverse=reverse,
            )

        page = items[start : start + count]
        total = len(items)

        # Build response — auto-detect collection format
        template = self.static_responses.get(f"GET {path}", {}) or {}
        # Support both HPE-style 'members' and generic 'items' format
        list_key = "members" if "members" in template else "items"
        return {
            **template,
            list_key: page,
            "count": len(page),
            "total": total,
            "start": start,
            "prevPageUri": (
                f"{path}?start={max(0, start - count)}&count={count}"
                if start > 0
                else None
            ),
            "nextPageUri": (
                f"{path}?start={start + count}&count={count}"
                if start + count < total
                else None
            ),
            "uri": path,
        }

    def get_resource(
        self, collection_path: str, resource_id: str
    ) -> Optional[dict]:
        for item in self.collections.get(collection_path, []):
            uri = item.get("uri", "")
            if uri.endswith(resource_id) or item.get("uuid") == resource_id:
                return item
        return None

    def create_resource(self, collection_path: str, data: dict) -> dict:
        new_id = str(uuid.uuid4()).upper()
        data.setdefault("uri", f"{collection_path}/{new_id}")
        data.setdefault("uuid", new_id)
        now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        data.setdefault("created", now)
        data["modified"] = now
        data.setdefault("eTag", now)
        self.collections.setdefault(collection_path, []).append(data)
        return data

    def update_resource(
        self, collection_path: str, resource_id: str, data: dict
    ) -> Optional[dict]:
        items = self.collections.get(collection_path, [])
        for i, item in enumerate(items):
            uri = item.get("uri", "")
            if uri.endswith(resource_id) or item.get("uuid") == resource_id:
                now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
                items[i] = {**item, **data, "modified": now, "eTag": now}
                return items[i]
        return None

    def delete_resource(
        self, collection_path: str, resource_id: str
    ) -> Optional[dict]:
        items = self.collections.get(collection_path, [])
        for i, item in enumerate(items):
            uri = item.get("uri", "")
            if uri.endswith(resource_id) or item.get("uuid") == resource_id:
                return items.pop(i)
        return None


# ── App factory ──────────────────────────────────────────────────────────────


def create_mock_app(
    api_spec_path: str = "output/api_spec.json",
    mock_data_path: str = "output/mock_data.json",
) -> FastAPI:
    """
    Create and configure a FastAPI application that serves mock API
    responses based on the crawler output.  Works with any API spec
    produced by the API Mocker LangGraph agent.
    """

    # Pre-read spec to get title/version for Swagger UI
    spec_title = "Mock API Server"
    spec_version = "1.0.0"
    if os.path.exists(api_spec_path):
        try:
            with open(api_spec_path, "r", encoding="utf-8") as _f:
                _meta = json.load(_f)
                spec_title = _meta.get("title", spec_title) + " (Mock)"
                spec_version = _meta.get("version", spec_version)
        except Exception:
            pass

    app = FastAPI(
        title=spec_title,
        description=(
            "Auto-generated mock server from API documentation.\n\n"
            "This server was created by the API Mocker LangGraph agent."
        ),
        version=spec_version,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ── Load spec & mock data ────────────────────────────────────────────

    if not os.path.exists(api_spec_path) or not os.path.exists(mock_data_path):
        logger.error(
            "API spec or mock data not found. Run the crawler first:\n"
            "  python run_api_mocker.py --url <docs-url>"
        )

        @app.get("/")
        async def _no_data():
            return {
                "error": "No API spec found. Run the crawler first.",
                "hint": "python run_api_mocker.py --url <docs-url>",
            }

        return app

    with open(api_spec_path, "r", encoding="utf-8") as f:
        api_spec = json.load(f)
    with open(mock_data_path, "r", encoding="utf-8") as f:
        mock_data = json.load(f)

    endpoints = api_spec.get("endpoints", [])

    # ── Populate the store ───────────────────────────────────────────────

    store = MockDataStore()
    store.load(endpoints, mock_data)

    # ── Build lookup tables ──────────────────────────────────────────────

    # Exact: "GET /rest/server-hardware" → endpoint dict
    exact_routes: dict[str, dict] = {}
    # Pattern: compiled regex → (method, collection_path, endpoint_dict)
    pattern_routes: list[tuple[re.Pattern, str, str, dict]] = []

    for ep in endpoints:
        method = ep["method"]
        path = ep["path"]
        key = f"{method} {path}"

        if "{" not in path:
            exact_routes[key] = ep
        else:
            # Convert /rest/foo/{id} → regex /rest/foo/(?P<id>[^/]+)
            regex = re.sub(r"\{(\w+)\}", r"(?P<\1>[^/]+)", path)
            # Derive collection path by stripping the last /{param} segment
            collection_path = re.sub(r"/\{[^}]+\}$", "", path)
            pattern_routes.append(
                (re.compile(f"^{regex}$"), method, collection_path, ep)
            )

    logger.info(
        "Mock server loaded: %d exact routes, %d pattern routes",
        len(exact_routes),
        len(pattern_routes),
    )

    # ── Registered routes ────────────────────────────────────────────────

    @app.get("/")
    async def root():
        categories = sorted(
            {ep.get("category", "") for ep in endpoints if ep.get("category")}
        )
        return {
            "title": api_spec.get("title", "Mock API"),
            "version": api_spec.get("version", "1.0.0"),
            "source_url": api_spec.get("source_url", ""),
            "total_endpoints": len(endpoints),
            "categories": categories,
            "docs": "/docs",
            "openapi": "/openapi.json",
        }

    # Detect the base path(s) used by the API spec
    base_paths = sorted({ep["path"].split("/")[1] for ep in endpoints if ep.get("path", "").count("/") >= 2})

    # Register root listing for each detected base path
    for bp in base_paths:
        bp_path = f"/{bp}"

        def _make_base_handler(prefix: str):
            async def _base_root():
                paths = sorted({ep["path"] for ep in endpoints
                                if "{" not in ep["path"] and ep["path"].startswith(prefix)})
                return {"available_paths": paths, "count": len(paths)}
            return _base_root

        try:
            app.add_api_route(
                bp_path,
                _make_base_handler(bp_path),
                methods=["GET"],
                summary=f"List all {bp_path} paths",
                tags=["Discovery"],
            )
        except Exception:
            pass

    # ── Generic catch-all handler for ALL paths ──────────────────────────

    @app.api_route(
        "/{path:path}",
        methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
        include_in_schema=False,
    )
    async def mock_handler(
        request: Request,
        path: str,
        start: int = Query(0, description="Pagination offset"),
        count: int = Query(50, description="Page size (max 500)"),
        filter: Optional[str] = Query(None, description="Filter expression"),
        sort: Optional[str] = Query(None, description="Sort expression"),
    ):
        """
        Catch-all mock handler.  Matches incoming requests against the
        discovered API spec and returns appropriate mock data.
        """
        # Reconstruct the full path from the request
        full_path = request.url.path
        method = request.method

        # ── 1. Try exact match ───────────────────────────────────────────
        key = f"{method} {full_path}"
        if key in exact_routes:
            if method == "GET":
                # Return paginated collection
                if full_path in store.collections:
                    return JSONResponse(
                        store.get_collection(
                            full_path,
                            start=start,
                            count=min(count, 500),
                            filter_str=filter,
                            sort=sort,
                        )
                    )
                # Static response
                resp = mock_data.get(key)
                if resp is not None:
                    return JSONResponse(resp)

            elif method == "POST":
                body = {}
                try:
                    body = await request.json()
                except Exception:
                    pass
                created = store.create_resource(full_path, body)
                return JSONResponse(created, status_code=201)

            # Fallback to static response
            resp = mock_data.get(key)
            if resp is not None:
                return JSONResponse(resp)
            return JSONResponse({"status": "ok"})

        # ── 2. Try pattern match (path params like {id}) ────────────────
        for regex, route_method, collection_path, ep in pattern_routes:
            if route_method != method:
                continue
            match = regex.match(full_path)
            if not match:
                continue

            params = match.groupdict()
            resource_id = params.get("id", "")

            if method == "GET":
                resource = store.get_resource(collection_path, resource_id)
                if resource:
                    return JSONResponse(resource)
                # Fall back to static response
                resp = mock_data.get(f"{method} {ep['path']}")
                if resp is not None:
                    return JSONResponse(resp)
                return JSONResponse(
                    {"error": "Resource not found", "uri": full_path},
                    status_code=404,
                )

            elif method in ("PUT", "PATCH"):
                body = {}
                try:
                    body = await request.json()
                except Exception:
                    pass
                updated = store.update_resource(
                    collection_path, resource_id, body
                )
                if updated:
                    return JSONResponse(updated)
                return JSONResponse(
                    {"error": "Resource not found"}, status_code=404
                )

            elif method == "DELETE":
                deleted = store.delete_resource(collection_path, resource_id)
                if deleted:
                    return JSONResponse(None, status_code=204)
                return JSONResponse(
                    {"error": "Resource not found"}, status_code=404
                )

            # Other methods
            resp = mock_data.get(f"{method} {ep['path']}")
            return JSONResponse(resp or {"status": "ok"})

        # ── 3. No match ─────────────────────────────────────────────────
        return JSONResponse(
            {
                "error": "Endpoint not found in mock spec",
                "method": method,
                "path": full_path,
                "hint": "Check /docs for available endpoints",
            },
            status_code=404,
        )

    # ── Register explicit routes for Swagger documentation ───────────────

    tags_metadata: list[dict] = []
    seen_tags: set[str] = set()

    for ep in endpoints:
        cat = ep.get("category", "General")
        if cat and cat not in seen_tags:
            tags_metadata.append({"name": cat})
            seen_tags.add(cat)

    app.openapi_tags = tags_metadata  # type: ignore[attr-defined]

    # Register a few key collection endpoints explicitly so they show in /docs
    for ep in endpoints:
        if ep["method"] == "GET" and "{" not in ep["path"]:
            _path = ep["path"]
            _summary = ep.get("summary", "")
            _tags = [ep.get("category", "General")]

            def _make_get_handler(p: str):
                async def _handler(
                    request: Request,
                    start: int = Query(0),
                    count: int = Query(50),
                    filter: Optional[str] = Query(None),
                    sort: Optional[str] = Query(None),
                ):
                    if p in store.collections:
                        return JSONResponse(
                            store.get_collection(p, start, min(count, 500), filter, sort)
                        )
                    resp = mock_data.get(f"GET {p}")
                    return JSONResponse(resp or {"items": [], "count": 0})

                return _handler

            try:
                app.add_api_route(
                    _path,
                    _make_get_handler(_path),
                    methods=["GET"],
                    summary=_summary,
                    tags=_tags,
                )
            except Exception:
                pass  # Skip duplicate routes

    return app
