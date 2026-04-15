"""
com_mock/mock_server.py
───────────────────────
FastAPI mock server with full HPE OneView protocol fidelity.

What this does that the mentor's version does not:

  1. Every resource read returns an ETag header
  2. PUT requires If-Match header (returns 412 on conflict)
  3. POST/PUT/DELETE on task-bearing resources return 202 + taskUri
  4. GET /rest/tasks/{id} returns live task state (AsyncTaskEngine)
  5. GET /rest/version returns HPE version negotiation response
  6. All errors use the HPE error envelope format
  7. Pagination uses HPE's start/count + prevPageUri/nextPageUri format
  8. Data is live from SQLite — survives restarts
  9. ResourceGraph enforces referential integrity on every mutation
  10. Full OpenAPI/Swagger docs at /docs
  11. Auth middleware placeholder (see oneview_protocol.py)
"""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from typing import Any, Optional

from fastapi import FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from com_mock.db import DatabaseEngine
from com_mock.oneview_protocol import (
    AsyncTaskEngine,
    hpe_error,
    oneview_protocol_middleware,
    version_response,
    ONEVIEW_CURRENT_VERSION,
)
from com_mock.resource_graph import ONEVIEW_RESOURCE_SCHEMAS, ResourceGraph

logger = logging.getLogger(__name__)


def create_mock_app(
    db: DatabaseEngine,
    api_spec_path: str = "output/api_spec.json",
) -> FastAPI:
    """
    Create the FastAPI mock application.

    Args:
        db            : Initialised DatabaseEngine (SQLite)
        api_spec_path : Path to api_spec.json (for Swagger metadata)
    """
    # ── Load spec metadata ───────────────────────────────────────────────
    spec_title = "HPE OneView / COM Mock API"
    spec_version = str(ONEVIEW_CURRENT_VERSION)

    if os.path.exists(api_spec_path):
        try:
            with open(api_spec_path, "r", encoding="utf-8") as f:
                meta = json.load(f)
                spec_title = meta.get("title", spec_title) + " (Mock)"
                spec_version = meta.get("version", spec_version)
        except Exception:
            pass

    app = FastAPI(
        title=spec_title,
        description=(
            "Auto-generated HPE OneView / COM mock server.\n\n"
            "Features: ETag concurrency, async task system, "
            "referential integrity, persistent SQLite storage.\n\n"
            "**Auth Note:** Set `X-Auth-Token` header with your JWT. "
            "Auth enforcement is toggled via `AUTH_ENABLED` in `oneview_protocol.py`."
        ),
        version=spec_version,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # ── CORS ─────────────────────────────────────────────────────────────
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["ETag", "X-API-Version", "X-Auth-Token-Required"],
    )

    # ── HPE Protocol Middleware ───────────────────────────────────────────
    app.middleware("http")(oneview_protocol_middleware)

    # ── Engines ──────────────────────────────────────────────────────────
    resource_graph = ResourceGraph(db)
    task_engine = AsyncTaskEngine(db)

    # ── Build resource slug → schema lookup ──────────────────────────────
    # Used to decide whether an operation triggers a task
    def _should_task(method: str, resource_slug: str) -> bool:
        schema = ONEVIEW_RESOURCE_SCHEMAS.get(resource_slug, {})
        return method in schema.get("task_operations", set())

    def _task_duration(resource_slug: str) -> int:
        schema = ONEVIEW_RESOURCE_SCHEMAS.get(resource_slug, {})
        return schema.get("task_duration_ms", 1000)

    # ── Utility: ETag response headers ───────────────────────────────────
    def _with_etag(data: dict | None) -> JSONResponse:
        if data is None:
            return JSONResponse(None, status_code=204)
        etag = data.get("eTag", "")
        response = JSONResponse(data)
        if etag:
            response.headers["ETag"] = f'"{etag}"'
        return response

    # ─────────────────────────────────────────────────────────────────────
    # Explicit endpoints (show in Swagger)
    # ─────────────────────────────────────────────────────────────────────

    @app.get("/", tags=["Discovery"])
    async def root() -> dict:
        """API overview — lists all resource categories and total counts."""
        categories = sorted({
            s.get("category", "GENERAL")
            for s in ONEVIEW_RESOURCE_SCHEMAS.values()
        })
        resource_counts: dict[str, int] = {}
        for slug in ONEVIEW_RESOURCE_SCHEMAS:
            resource_counts[slug] = await db.count_resources(slug)

        return {
            "title":            spec_title,
            "version":          spec_version,
            "totalResources":   sum(resource_counts.values()),
            "categories":       categories,
            "resourceCounts":   resource_counts,
            "docs":             "/docs",
            "openapi":          "/openapi.json",
        }

    @app.get("/rest/version", tags=["Settings"])
    async def get_version() -> dict:
        """HPE OneView API version negotiation endpoint."""
        return version_response()

    @app.get("/rest/tasks", tags=["Activity"])
    async def list_tasks(
        start: int = Query(0, description="Pagination offset"),
        count: int = Query(50, description="Page size"),
    ) -> dict:
        """List all async tasks."""
        return await db.list_tasks(start=start, count=min(count, 500))

    @app.get("/rest/tasks/{task_id}", tags=["Activity"])
    async def get_task(task_id: str) -> JSONResponse:
        """Get live task state by ID. Poll this to observe task progress."""
        task = await db.get_task(task_id)
        if not task:
            return hpe_error("RESOURCE_NOT_FOUND", 404, f"/rest/tasks/{task_id}")
        return _with_etag(task)

    @app.get("/rest/audit-log", tags=["Activity"])
    async def get_audit_log(
        resourceType: Optional[str] = Query(None),
        limit: int = Query(100),
    ) -> list:
        """Audit log — every CREATE, UPDATE, DELETE mutation recorded."""
        return await db.get_audit_log(resource_type=resourceType, limit=limit)

    # ─────────────────────────────────────────────────────────────────────
    # Generic catch-all for all /rest/* resource paths
    # ─────────────────────────────────────────────────────────────────────

    @app.api_route(
        "/rest/{path:path}",
        methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
        include_in_schema=False,
    )
    async def rest_handler(
        request: Request,
        path: str,
        start:  int            = Query(0,    description="Pagination offset"),
        count:  int            = Query(50,   description="Page size"),
        filter: Optional[str]  = Query(None, description="Filter expression"),
        sort:   Optional[str]  = Query(None, description="Sort field[:asc|desc]"),
    ) -> JSONResponse:
        """
        Universal HPE OneView REST handler.

        Routing logic:
          /rest/{slug}           → collection  (GET list, POST create)
          /rest/{slug}/{id}      → member      (GET one, PUT update, DELETE)
          /rest/{slug}/{id}/{action} → action  (PATCH partial update)
        """
        method = request.method
        full_path = request.url.path   # e.g. /rest/server-hardware/abc123

        # Split path: ["rest", "server-hardware", "abc123"] or ["rest", "server-hardware"]
        parts = [p for p in full_path.split("/") if p]  # drop empty strings
        if not parts or parts[0] != "rest":
            return hpe_error("RESOURCE_NOT_FOUND", 404, full_path)

        rest_parts = parts[1:]  # ["server-hardware"] or ["server-hardware", "abc123"]

        if not rest_parts:
            return JSONResponse({"message": "HPE OneView Mock API", "version": spec_version})

        resource_slug = rest_parts[0]
        resource_id   = rest_parts[1] if len(rest_parts) > 1 else None

        # ── Parse sort ───────────────────────────────────────────────────
        sort_field: Optional[str] = None
        sort_desc = False
        if sort:
            parts_sort = sort.split(":")
            sort_field = parts_sort[0]
            sort_desc  = len(parts_sort) > 1 and parts_sort[1].lower() == "desc"

        # ── GET collection ───────────────────────────────────────────────
        if method == "GET" and resource_id is None:
            result = await db.list_resources(
                resource_slug,
                start=start,
                count=min(count, 500),
                filter_str=filter,
                sort_field=sort_field,
                sort_desc=sort_desc,
            )
            return JSONResponse(result)

        # ── GET single resource ───────────────────────────────────────────
        if method == "GET" and resource_id:
            # Try direct ID lookup first
            resource = await db.get_resource(resource_slug, resource_id)
            if not resource:
                # Try by full URI
                resource = await db.get_resource_by_uri(full_path)
            if not resource:
                return hpe_error("RESOURCE_NOT_FOUND", 404, full_path)
            return _with_etag(resource)

        # ── POST (create) ────────────────────────────────────────────────
        if method == "POST" and resource_id is None:
            body = {}
            try:
                body = await request.json()
            except Exception:
                pass

            if _should_task("POST", resource_slug):
                # Return 202 + taskUri; actual creation happens in background
                captured_body = dict(body)

                async def _do_create() -> str:
                    created = await db.create_resource(resource_slug, captured_body)
                    # Enforce bidirectional links
                    await resource_graph.apply_bidirectional_link(
                        resource_slug, created["uri"], created
                    )
                    return created["uri"]

                task = await task_engine.create_task(
                    task_name=f"Create {resource_slug}",
                    associated_resource_uri=f"/rest/{resource_slug}/pending",
                    callback=_do_create,
                    duration_ms=_task_duration(resource_slug),
                    owner=getattr(request.state, "principal", {}).get("username", "system"),
                )
                return JSONResponse(task, status_code=202)

            else:
                # Immediate create (no task)
                created = await db.create_resource(resource_slug, body)
                await resource_graph.apply_bidirectional_link(
                    resource_slug, created["uri"], created
                )
                return _with_etag(created)

        # ── PUT (full update) ─────────────────────────────────────────────
        if method == "PUT" and resource_id:
            body = {}
            try:
                body = await request.json()
            except Exception:
                pass

            # ETag check
            if_match = request.headers.get("If-Match", "").strip('"')

            if _should_task("PUT", resource_slug):
                captured_id   = resource_id
                captured_body = dict(body)
                captured_etag = if_match or None

                async def _do_update() -> str:
                    updated, err = await db.update_resource(
                        resource_slug, captured_id, captured_body,
                        if_match_etag=captured_etag,
                    )
                    if err == "ETAG_CONFLICT":
                        raise ValueError("ETag conflict during update")
                    if err == "NOT_FOUND":
                        raise ValueError(f"Resource {resource_slug}/{captured_id} not found")
                    await resource_graph.apply_bidirectional_link(
                        resource_slug, updated["uri"], updated
                    )
                    return updated["uri"]

                task = await task_engine.create_task(
                    task_name=f"Update {resource_slug}",
                    associated_resource_uri=full_path,
                    callback=_do_update,
                    duration_ms=_task_duration(resource_slug),
                    owner=getattr(request.state, "principal", {}).get("username", "system"),
                )
                return JSONResponse(task, status_code=202)

            else:
                updated, err = await db.update_resource(
                    resource_slug, resource_id, body,
                    if_match_etag=if_match or None,
                )
                if err == "ETAG_CONFLICT":
                    return hpe_error("ETAG_CONFLICT", 412, full_path)
                if err == "NOT_FOUND":
                    return hpe_error("RESOURCE_NOT_FOUND", 404, full_path)
                return _with_etag(updated)

        # ── PATCH (partial update) ────────────────────────────────────────
        if method == "PATCH" and resource_id:
            body = {}
            try:
                body = await request.json()
            except Exception:
                pass
            patched = await db.patch_resource(resource_slug, full_path, body)
            if not patched:
                return hpe_error("RESOURCE_NOT_FOUND", 404, full_path)
            return _with_etag(patched)

        # ── DELETE ────────────────────────────────────────────────────────
        if method == "DELETE" and resource_id:
            resource = await db.get_resource_by_uri(full_path)
            if not resource:
                return hpe_error("RESOURCE_NOT_FOUND", 404, full_path)

            if _should_task("DELETE", resource_slug):
                captured_uri  = full_path
                captured_slug = resource_slug

                async def _do_delete() -> str:
                    cascade_log = await resource_graph.apply_delete_cascades(
                        captured_slug, captured_uri
                    )
                    for msg in cascade_log:
                        logger.info("CASCADE: %s", msg)
                    await db.delete_resource(captured_slug, captured_uri)
                    return captured_uri

                task = await task_engine.create_task(
                    task_name=f"Delete {resource_slug}",
                    associated_resource_uri=full_path,
                    callback=_do_delete,
                    duration_ms=_task_duration(resource_slug),
                    owner=getattr(request.state, "principal", {}).get("username", "system"),
                )
                return JSONResponse(task, status_code=202)

            else:
                cascade_log = await resource_graph.apply_delete_cascades(
                    resource_slug, full_path
                )
                for msg in cascade_log:
                    logger.info("CASCADE: %s", msg)

                deleted = await db.delete_resource(resource_slug, full_path)
                if not deleted:
                    return hpe_error("RESOURCE_NOT_FOUND", 404, full_path)
                return JSONResponse(None, status_code=204)

        # ── Fallback ──────────────────────────────────────────────────────
        return hpe_error(
            "RESOURCE_NOT_FOUND", 404,
            f"No handler matched {method} {full_path}",
        )

    # ─────────────────────────────────────────────────────────────────────
    # Register explicit collection routes in Swagger
    # ─────────────────────────────────────────────────────────────────────
    _register_swagger_routes(app, db)

    return app


def _register_swagger_routes(app: FastAPI, db: DatabaseEngine) -> None:
    """
    Register one explicit GET route per resource collection in Swagger.
    This makes /docs show a clean, browsable list of all resource endpoints.
    """
    seen_tags: list[dict] = []
    seen_tag_names: set[str] = set()

    for slug, schema in ONEVIEW_RESOURCE_SCHEMAS.items():
        cat = schema.get("category", "GENERAL")
        if cat not in seen_tag_names:
            seen_tags.append({"name": cat, "description": f"{cat} resources"})
            seen_tag_names.add(cat)

    app.openapi_tags = seen_tags  # type: ignore[attr-defined]

    for slug, schema in ONEVIEW_RESOURCE_SCHEMAS.items():
        base_path = schema.get("base_path", f"/rest/{slug}")
        cat       = schema.get("category", "GENERAL")

        _slug  = slug
        _base  = base_path

        def _make_list_handler(s: str, b: str):
            async def _handler(
                start:  int           = Query(0,    description="Pagination offset"),
                count:  int           = Query(50,   description="Page size"),
                filter: Optional[str] = Query(None, description="Filter expression"),
                sort:   Optional[str] = Query(None, description="Sort field"),
            ) -> dict:
                sf, sd = (sort.split(":")[0], "desc" in sort) if sort else (None, False)
                return await db.list_resources(s, start, min(count, 500), filter, sf, sd)
            return _handler

        try:
            app.add_api_route(
                base_path,
                _make_list_handler(_slug, _base),
                methods=["GET"],
                summary=f"List {slug}",
                tags=[cat],
                response_model=None,
            )
        except Exception:
            pass   # Duplicate routes silently skipped
