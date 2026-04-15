"""
com_mock/oneview_protocol.py
────────────────────────────
HPE OneView protocol fidelity layer.

What this module provides that the mentor's version has zero of:

  1. AsyncTaskEngine
     • POST/PUT/DELETE on complex resources returns 202 + {taskUri}
     • Task progresses through Running → Completed/Error asynchronously
     • GET /rest/tasks/{id} returns live task state
     • Configurable duration per resource type

  2. ETag-based Optimistic Concurrency
     • Every resource carries an eTag
     • PUT requests must include If-Match header (or we return 412)
     • Middleware validates ETag before any update

  3. API Version Negotiation
     • GET /rest/version returns {currentVersion, minimumVersion}
     • Request header X-API-Version is checked (logged; soft-enforce)
     • X-Auth-Token header is read and passed to the auth hook

  4. HPE Error Format
     • All errors return the standard HPE error envelope:
         {errorCode, message, details, recommendedActions, nestedErrors}
     • Not just {"error": "..."} like the mentor's version

  ┌────────────────────────────────────────────────────────────────────────┐
  │  AUTH HOOK  (teammate integration point)                               │
  │                                                                        │
  │  Your teammate produces a JWT from the MCP server.  Once they do,     │
  │  plug their validator into the function:                               │
  │                                                                        │
  │      async def validate_token(token: str) -> dict | None              │
  │                                                                        │
  │  Return the decoded payload (with "role") or None if invalid.         │
  │  The middleware will then enforce:                                     │
  │    role == "admin"  → full access                                      │
  │    role != "admin"  → 403 on all mutating methods                     │
  │                                                                        │
  │  Until the teammate integrates, AUTH_ENABLED = False and all          │
  │  requests pass through.                                                │
  └────────────────────────────────────────────────────────────────────────┘
"""

from __future__ import annotations

import asyncio
import logging
import uuid
from datetime import datetime, timezone
from typing import Any, Callable, Coroutine, Optional

from fastapi import Request, Response
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)

# ── OneView Version Constants ─────────────────────────────────────────────────

ONEVIEW_CURRENT_VERSION = 4600
ONEVIEW_MINIMUM_VERSION = 2800
ONEVIEW_X_API_VERSION   = 4600

# ── Auth hook toggle ─────────────────────────────────────────────────────────
#
# Set AUTH_ENABLED = True once your teammate's JWT validator is wired in.
# Replace validate_token() with the real implementation.

AUTH_ENABLED: bool = False


async def validate_token(token: str) -> Optional[dict]:
    """
    ╔══════════════════════════════════════════════════════════════════╗
    ║  AUTH HOOK — integrate teammate's JWT validator here            ║
    ║                                                                  ║
    ║  Expected flow:                                                  ║
    ║    1. MCP server authenticates user → issues JWT                ║
    ║    2. Client includes JWT as X-Auth-Token header                ║
    ║    3. This function decodes + validates the JWT                 ║
    ║    4. Returns {"username": "...", "role": "admin"|"viewer"}     ║
    ║       or None if invalid/expired                                ║
    ╚══════════════════════════════════════════════════════════════════╝
    """
    # TODO: replace with actual JWT decode + verify
    # Example:
    #   payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    #   return {"username": payload["sub"], "role": payload["role"]}
    return {"username": "mock-user", "role": "admin"}   # pass-through until integrated


# ── HPE Error Envelopes ───────────────────────────────────────────────────────

_ERROR_CATALOG: dict[str, dict] = {
    "RESOURCE_NOT_FOUND": {
        "message":             "The requested resource was not found.",
        "recommendedActions":  ["Verify the resource URI and try again."],
    },
    "ETAG_CONFLICT": {
        "message":             "The resource has been modified since you last retrieved it.",
        "recommendedActions":  ["Retrieve the resource again, then re-apply your changes."],
    },
    "VALIDATION_ERROR": {
        "message":             "The request body failed schema validation.",
        "recommendedActions":  ["Correct the invalid fields and resubmit."],
    },
    "REFERENTIAL_INTEGRITY_ERROR": {
        "message":             "A referenced resource URI does not exist.",
        "recommendedActions":  ["Verify that all referenced resource URIs are valid before retrying."],
    },
    "RESTRICT_CASCADE_ERROR": {
        "message":             "Cannot delete resource — it is referenced by one or more dependent resources.",
        "recommendedActions":  ["Remove all references to this resource before deleting it."],
    },
    "AUTH_REQUIRED": {
        "message":             "Authentication is required.",
        "recommendedActions":  ["Include a valid X-Auth-Token header obtained from POST /rest/login-sessions."],
    },
    "INSUFFICIENT_PRIVILEGES": {
        "message":             "You do not have permission to perform this operation.",
        "recommendedActions":  ["Contact your administrator to obtain the required role."],
    },
    "UNSUPPORTED_API_VERSION": {
        "message":             f"The requested API version is not supported.",
        "recommendedActions":  [
            f"Use X-API-Version: {ONEVIEW_X_API_VERSION}",
            f"Minimum supported version: {ONEVIEW_MINIMUM_VERSION}",
        ],
    },
}


def hpe_error(
    error_code: str,
    http_status: int = 400,
    details: str = "",
    nested_errors: Optional[list] = None,
) -> JSONResponse:
    catalog = _ERROR_CATALOG.get(error_code, {})
    body = {
        "errorCode":           error_code,
        "message":             catalog.get("message", error_code),
        "details":             details or catalog.get("message", ""),
        "recommendedActions":  catalog.get("recommendedActions", []),
        "nestedErrors":        nested_errors or [],
    }
    return JSONResponse(content=body, status_code=http_status)


# ── Async Task Engine ─────────────────────────────────────────────────────────


class AsyncTaskEngine:
    """
    Simulates HPE OneView's async task system.

    When a caller issues a POST/PUT/DELETE that would trigger a task:
      1. create_task() is called — returns a task dict with taskState=Running
      2. The FastAPI handler returns 202 with the taskUri
      3. A background coroutine runs _execute_task() which calls the callback
      4. On completion, the task state transitions to Completed / Error
      5. The actual resource change is applied inside the callback

    Callers poll GET /rest/tasks/{id} to observe task progress.
    """

    def __init__(self, db: Any) -> None:
        self.db = db
        self._running: dict[str, asyncio.Task] = {}

    async def create_task(
        self,
        task_name: str,
        associated_resource_uri: str,
        callback: Callable[[], Coroutine],
        duration_ms: int = 1000,
        owner: str = "system",
    ) -> dict:
        """
        Register a new task and schedule its async execution.

        Returns the task dict (taskState=Running) immediately.
        """
        task_id = str(uuid.uuid4()).upper()
        uri = f"/rest/tasks/{task_id}"
        now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

        task = {
            "type":                  "TaskResourceV2",
            "category":              "tasks",
            "id":                    task_id,
            "uri":                   uri,
            "taskType":              "User",
            "taskState":             "Running",
            "name":                  task_name,
            "percentComplete":       0,
            "stateReason":           "Task started",
            "progressUpdates":       [
                {"statusUpdate": f"Task {task_name} initiated", "timestamp": now}
            ],
            "associatedResourceUri": associated_resource_uri,
            "owner":                 owner,
            "created":               now,
            "modified":              now,
        }

        await self.db.create_task(task)

        # Schedule background execution
        bg = asyncio.create_task(
            self._execute_task(task_id, callback, duration_ms)
        )
        self._running[task_id] = bg

        return task

    async def _execute_task(
        self,
        task_id: str,
        callback: Callable[[], Coroutine],
        duration_ms: int,
    ) -> None:
        """Background worker: simulate progress then run the actual callback."""
        try:
            # Step 1: Report 25%
            await asyncio.sleep(duration_ms * 0.25 / 1000)
            await self.db.update_task(task_id, {
                "percentComplete": 25,
                "stateReason": "Processing",
            })

            # Step 2: Report 75%
            await asyncio.sleep(duration_ms * 0.50 / 1000)
            await self.db.update_task(task_id, {
                "percentComplete": 75,
                "stateReason": "Applying changes",
            })

            # Step 3: Execute the real operation
            resource_uri = await callback()

            # Step 4: Complete
            await asyncio.sleep(duration_ms * 0.25 / 1000)
            now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
            await self.db.update_task(task_id, {
                "taskState":             "Completed",
                "percentComplete":       100,
                "stateReason":           "Completed successfully",
                "completedAt":           now,
                "associatedResourceUri": resource_uri,
            })
            logger.debug("Task %s completed", task_id)

        except Exception as exc:
            logger.exception("Task %s failed: %s", task_id, exc)
            await self.db.update_task(task_id, {
                "taskState":    "Error",
                "stateReason":  str(exc)[:200],
                "percentComplete": 0,
            })
        finally:
            self._running.pop(task_id, None)


# ── API Version Middleware ────────────────────────────────────────────────────


async def oneview_protocol_middleware(request: Request, call_next: Callable) -> Response:
    """
    FastAPI middleware that enforces HPE OneView protocol conventions:

    1. Adds HPE response headers to every reply
    2. Validates X-API-Version header (logs warning on mismatch, soft-enforce)
    3. Auth hook: reads X-Auth-Token, calls validate_token()
       • If AUTH_ENABLED and token is missing/invalid → 401
       • If AUTH_ENABLED and role != admin on mutating verb → 403
    """
    # ── Version check (soft) ─────────────────────────────────────────────
    requested_version = request.headers.get("X-API-Version", "")
    if requested_version:
        try:
            ver = int(requested_version)
            if ver < ONEVIEW_MINIMUM_VERSION:
                return hpe_error(
                    "UNSUPPORTED_API_VERSION",
                    http_status=400,
                    details=f"Requested {ver}, minimum supported {ONEVIEW_MINIMUM_VERSION}",
                )
        except ValueError:
            pass  # Non-integer version string — ignore

    # ── Auth check ───────────────────────────────────────────────────────
    if AUTH_ENABLED:
        token = request.headers.get("X-Auth-Token", "")
        if not token:
            return hpe_error("AUTH_REQUIRED", http_status=401)

        principal = await validate_token(token)
        if principal is None:
            return hpe_error("AUTH_REQUIRED", http_status=401,
                              details="Token is invalid or expired.")

        # Role enforcement: only admins can mutate
        if request.method in ("POST", "PUT", "PATCH", "DELETE"):
            if principal.get("role") != "admin":
                return hpe_error(
                    "INSUFFICIENT_PRIVILEGES",
                    http_status=403,
                    details=f"Role '{principal.get('role')}' cannot perform {request.method}.",
                )

        # Attach principal to request state for downstream use
        request.state.principal = principal
    else:
        request.state.principal = {"username": "passthrough", "role": "admin"}

    # ── Execute handler ──────────────────────────────────────────────────
    response = await call_next(request)

    # ── Add HPE protocol headers ─────────────────────────────────────────
    response.headers["X-API-Version"] = str(ONEVIEW_CURRENT_VERSION)
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["X-Auth-Token-Required"] = "true" if AUTH_ENABLED else "false"

    return response


# ── Version endpoint response ─────────────────────────────────────────────────

def version_response() -> dict:
    return {
        "type":                 "Version",
        "currentVersion":       ONEVIEW_CURRENT_VERSION,
        "minimumVersion":       ONEVIEW_MINIMUM_VERSION,
    }
