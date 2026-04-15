"""
com_mock/db.py
──────────────
Async SQLite state engine.

Replaces the mentor's plain Python dict with a proper persistent store.
Key capabilities:
  • Full CRUD with ACID transactions (aiosqlite)
  • Schema-per-category dynamic tables via JSON blob storage
  • ETag-based optimistic concurrency
  • Append-only resource_events audit log (every mutation recorded)
  • Task table with state-machine progression
  • Survives server restarts — data persists between runs
  • `--reset` wipes back to the generated baseline seed
"""

from __future__ import annotations

import json
import logging
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

import aiosqlite

logger = logging.getLogger(__name__)

# ── Schema ───────────────────────────────────────────────────────────────────

DDL = """
PRAGMA journal_mode = WAL;
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS resources (
    resource_type   TEXT    NOT NULL,
    resource_id     TEXT    NOT NULL,
    uri             TEXT    NOT NULL UNIQUE,
    data            TEXT    NOT NULL,          -- JSON blob
    etag            TEXT    NOT NULL,
    created_at      TEXT    NOT NULL,
    updated_at      TEXT    NOT NULL,
    PRIMARY KEY (resource_type, resource_id)
);

CREATE INDEX IF NOT EXISTS idx_resources_uri
    ON resources(uri);

CREATE INDEX IF NOT EXISTS idx_resources_type
    ON resources(resource_type);

CREATE TABLE IF NOT EXISTS tasks (
    task_id             TEXT PRIMARY KEY,
    uri                 TEXT NOT NULL UNIQUE,
    task_type           TEXT NOT NULL DEFAULT 'User',
    task_state          TEXT NOT NULL DEFAULT 'Running',
    task_name           TEXT NOT NULL DEFAULT '',
    percent_complete    INTEGER NOT NULL DEFAULT 0,
    state_reason        TEXT NOT NULL DEFAULT '',
    associated_resource_uri TEXT,
    owner               TEXT NOT NULL DEFAULT 'system',
    data                TEXT NOT NULL,          -- JSON blob (full task object)
    created_at          TEXT NOT NULL,
    updated_at          TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS resource_events (
    event_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    resource_type   TEXT,
    resource_id     TEXT,
    uri             TEXT,
    operation       TEXT NOT NULL,   -- CREATE | UPDATE | DELETE | PATCH
    payload         TEXT,            -- JSON diff / payload
    actor           TEXT DEFAULT 'system',
    timestamp       TEXT NOT NULL
);
"""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _new_etag() -> str:
    return str(uuid.uuid4()).replace("-", "")


class DatabaseEngine:
    """
    Async SQLite engine.  A single instance is shared across the mock server.

    Usage:
        db = DatabaseEngine("output/mock.db")
        await db.init()
        ...
        await db.close()
    """

    def __init__(self, db_path: str = "output/mock.db") -> None:
        self.db_path = db_path
        self._conn: Optional[aiosqlite.Connection] = None

    async def init(self) -> None:
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self._conn = await aiosqlite.connect(self.db_path)
        self._conn.row_factory = aiosqlite.Row
        await self._conn.executescript(DDL)
        await self._conn.commit()
        logger.info("SQLite DB initialised: %s", self.db_path)

    async def close(self) -> None:
        if self._conn:
            await self._conn.close()

    async def reset(self) -> None:
        """Drop all data — used when --reset flag is passed."""
        assert self._conn
        await self._conn.executescript("""
            DELETE FROM resource_events;
            DELETE FROM tasks;
            DELETE FROM resources;
        """)
        await self._conn.commit()
        logger.info("Database reset: all records deleted.")

    # ── Internal helpers ─────────────────────────────────────────────────

    async def _record_event(
        self,
        operation: str,
        resource_type: str,
        resource_id: str,
        uri: str,
        payload: Any,
        actor: str = "system",
    ) -> None:
        assert self._conn
        await self._conn.execute(
            """
            INSERT INTO resource_events
                (resource_type, resource_id, uri, operation, payload, actor, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                resource_type,
                resource_id,
                uri,
                operation,
                json.dumps(payload, default=str),
                actor,
                _now(),
            ),
        )

    # ── Resource CRUD ────────────────────────────────────────────────────

    async def create_resource(
        self,
        resource_type: str,
        data: dict,
        actor: str = "system",
    ) -> dict:
        assert self._conn
        now = _now()
        etag = _new_etag()

        # Ensure required meta fields
        resource_id = data.get("id") or str(uuid.uuid4()).upper()
        uri = data.get("uri") or f"/rest/{resource_type}/{resource_id}"

        data.setdefault("id", resource_id)
        data.setdefault("uri", uri)
        data.setdefault("eTag", etag)
        data.setdefault("created", now)
        data["modified"] = now

        async with self._conn.execute("BEGIN"):
            await self._conn.execute(
                """
                INSERT INTO resources
                    (resource_type, resource_id, uri, data, etag, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (resource_type, resource_id, uri, json.dumps(data, default=str), etag, now, now),
            )
            await self._record_event("CREATE", resource_type, resource_id, uri, data, actor)
        await self._conn.commit()
        logger.debug("CREATED %s %s", resource_type, uri)
        return data

    async def get_resource_by_uri(self, uri: str) -> Optional[dict]:
        assert self._conn
        async with self._conn.execute(
            "SELECT data FROM resources WHERE uri = ?", (uri,)
        ) as cur:
            row = await cur.fetchone()
            return json.loads(row["data"]) if row else None

    async def get_resource(self, resource_type: str, resource_id: str) -> Optional[dict]:
        assert self._conn
        async with self._conn.execute(
            "SELECT data FROM resources WHERE resource_type = ? AND resource_id = ?",
            (resource_type, resource_id),
        ) as cur:
            row = await cur.fetchone()
            return json.loads(row["data"]) if row else None

    async def list_resources(
        self,
        resource_type: str,
        start: int = 0,
        count: int = 50,
        filter_str: Optional[str] = None,
        sort_field: Optional[str] = None,
        sort_desc: bool = False,
    ) -> dict:
        """Return paginated collection in HPE OneView format."""
        assert self._conn

        # Fetch all rows (we do pagination in Python to support JSON filtering)
        async with self._conn.execute(
            "SELECT data FROM resources WHERE resource_type = ? ORDER BY created_at ASC",
            (resource_type,),
        ) as cur:
            rows = await cur.fetchall()

        items = [json.loads(r["data"]) for r in rows]

        # Filter
        if filter_str:
            filter_lower = filter_str.lower()
            items = [i for i in items if filter_lower in json.dumps(i).lower()]

        # Sort
        if sort_field:
            items = sorted(
                items,
                key=lambda x: str(x.get(sort_field, "")),
                reverse=sort_desc,
            )

        total = len(items)
        page = items[start : start + count]

        return {
            "type": f"{resource_type}_list",
            "uri": f"/rest/{resource_type}",
            "start": start,
            "count": len(page),
            "total": total,
            "members": page,
            "prevPageUri": (
                f"/rest/{resource_type}?start={max(0, start - count)}&count={count}"
                if start > 0
                else None
            ),
            "nextPageUri": (
                f"/rest/{resource_type}?start={start + count}&count={count}"
                if start + count < total
                else None
            ),
        }

    async def update_resource(
        self,
        resource_type: str,
        resource_id: str,
        new_data: dict,
        if_match_etag: Optional[str] = None,
        actor: str = "system",
    ) -> tuple[Optional[dict], Optional[str]]:
        """
        Full update (PUT).

        Returns (updated_data, None) on success.
        Returns (None, error_message) on ETag conflict or not-found.
        """
        assert self._conn
        existing = await self.get_resource(resource_type, resource_id)
        if not existing:
            return None, "NOT_FOUND"

        # ETag concurrency check
        if if_match_etag and existing.get("eTag") != if_match_etag:
            return None, "ETAG_CONFLICT"

        now = _now()
        new_etag = _new_etag()
        uri = existing["uri"]

        merged = {**existing, **new_data}
        merged["uri"] = uri                 # URI is immutable
        merged["id"] = existing["id"]       # ID is immutable
        merged["created"] = existing["created"]  # created is immutable
        merged["modified"] = now
        merged["eTag"] = new_etag

        async with self._conn.execute("BEGIN"):
            await self._conn.execute(
                """
                UPDATE resources
                   SET data = ?, etag = ?, updated_at = ?
                 WHERE resource_type = ? AND resource_id = ?
                """,
                (json.dumps(merged, default=str), new_etag, now, resource_type, resource_id),
            )
            await self._record_event("UPDATE", resource_type, resource_id, uri, new_data, actor)
        await self._conn.commit()
        return merged, None

    async def patch_resource(
        self,
        resource_type: str,
        uri: str,
        patch: dict,
        actor: str = "system",
    ) -> Optional[dict]:
        """
        Internal patch by URI (used for cascade nullify / bidirectional links).
        No ETag check — system-internal operation.
        """
        assert self._conn
        existing = await self.get_resource_by_uri(uri)
        if not existing:
            return None

        resource_id = existing["id"]
        now = _now()
        new_etag = _new_etag()

        merged = {**existing, **patch, "modified": now, "eTag": new_etag}

        async with self._conn.execute("BEGIN"):
            await self._conn.execute(
                """
                UPDATE resources
                   SET data = ?, etag = ?, updated_at = ?
                 WHERE uri = ?
                """,
                (json.dumps(merged, default=str), new_etag, now, uri),
            )
            await self._record_event("PATCH", resource_type, resource_id, uri, patch, actor)
        await self._conn.commit()
        return merged

    async def delete_resource(
        self,
        resource_type: str,
        uri: str,
        actor: str = "system",
    ) -> bool:
        """Delete by URI. Returns True if deleted, False if not found."""
        assert self._conn
        existing = await self.get_resource_by_uri(uri)
        if not existing:
            return False

        resource_id = existing["id"]

        async with self._conn.execute("BEGIN"):
            await self._conn.execute(
                "DELETE FROM resources WHERE uri = ?", (uri,)
            )
            await self._record_event("DELETE", resource_type, resource_id, uri, None, actor)
        await self._conn.commit()
        logger.debug("DELETED %s %s", resource_type, uri)
        return True

    async def resource_exists_by_uri(self, resource_type: str, uri: str) -> bool:
        assert self._conn
        async with self._conn.execute(
            "SELECT 1 FROM resources WHERE uri = ?", (uri,)
        ) as cur:
            return (await cur.fetchone()) is not None

    async def find_by_field_uri(
        self, resource_type: str, field_name: str, target_uri: str
    ) -> list[dict]:
        """
        Find all resources of type resource_type where data->>field_name = target_uri
        or where data->>field_name contains target_uri (for array fields).

        Uses SQLite JSON functions (available since 3.38+).
        Falls back to Python scan if JSON functions are unavailable.
        """
        assert self._conn
        results: list[dict] = []
        try:
            # Try SQLite JSON extract first
            async with self._conn.execute(
                """
                SELECT data FROM resources
                 WHERE resource_type = ?
                   AND (
                         json_extract(data, '$.' || ?) = ?
                      OR instr(data, ?) > 0
                   )
                """,
                (resource_type, field_name, target_uri, target_uri),
            ) as cur:
                rows = await cur.fetchall()
                for row in rows:
                    d = json.loads(row["data"])
                    val = d.get(field_name)
                    if val == target_uri or (isinstance(val, list) and target_uri in val):
                        results.append(d)
        except Exception:
            # Fallback: scan all rows (slower but safe)
            async with self._conn.execute(
                "SELECT data FROM resources WHERE resource_type = ?", (resource_type,)
            ) as cur:
                rows = await cur.fetchall()
                for row in rows:
                    d = json.loads(row["data"])
                    val = d.get(field_name)
                    if val == target_uri or (isinstance(val, list) and target_uri in val):
                        results.append(d)

        return results

    # ── Task CRUD ────────────────────────────────────────────────────────

    async def create_task(self, task: dict) -> dict:
        assert self._conn
        now = _now()
        task_id = task.get("id", str(uuid.uuid4()).upper())
        uri = task.get("uri", f"/rest/tasks/{task_id}")

        task.setdefault("id", task_id)
        task.setdefault("uri", uri)
        task.setdefault("created", now)
        task["modified"] = now

        await self._conn.execute(
            """
            INSERT INTO tasks
                (task_id, uri, task_type, task_state, task_name,
                 percent_complete, state_reason, associated_resource_uri,
                 owner, data, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                task_id,
                uri,
                task.get("taskType", "User"),
                task.get("taskState", "Running"),
                task.get("name", "Operation"),
                task.get("percentComplete", 0),
                task.get("stateReason", ""),
                task.get("associatedResourceUri"),
                task.get("owner", "system"),
                json.dumps(task, default=str),
                now,
                now,
            ),
        )
        await self._conn.commit()
        return task

    async def get_task(self, task_id: str) -> Optional[dict]:
        assert self._conn
        async with self._conn.execute(
            "SELECT data FROM tasks WHERE task_id = ?", (task_id,)
        ) as cur:
            row = await cur.fetchone()
            return json.loads(row["data"]) if row else None

    async def get_task_by_uri(self, uri: str) -> Optional[dict]:
        assert self._conn
        async with self._conn.execute(
            "SELECT data FROM tasks WHERE uri = ?", (uri,)
        ) as cur:
            row = await cur.fetchone()
            return json.loads(row["data"]) if row else None

    async def update_task(self, task_id: str, patch: dict) -> Optional[dict]:
        assert self._conn
        existing = await self.get_task(task_id)
        if not existing:
            return None

        now = _now()
        merged = {**existing, **patch, "modified": now}

        await self._conn.execute(
            """
            UPDATE tasks
               SET task_state = ?, percent_complete = ?, state_reason = ?,
                   associated_resource_uri = ?, data = ?, updated_at = ?
             WHERE task_id = ?
            """,
            (
                merged.get("taskState", existing.get("taskState")),
                merged.get("percentComplete", 0),
                merged.get("stateReason", ""),
                merged.get("associatedResourceUri"),
                json.dumps(merged, default=str),
                now,
                task_id,
            ),
        )
        await self._conn.commit()
        return merged

    async def list_tasks(self, start: int = 0, count: int = 50) -> dict:
        assert self._conn
        async with self._conn.execute(
            "SELECT data FROM tasks ORDER BY created_at DESC LIMIT ? OFFSET ?",
            (count, start),
        ) as cur:
            rows = await cur.fetchall()

        async with self._conn.execute("SELECT COUNT(*) FROM tasks") as cur:
            total = (await cur.fetchone())[0]

        return {
            "type": "TaskResourceV2List",
            "uri": "/rest/tasks",
            "start": start,
            "count": len(rows),
            "total": total,
            "members": [json.loads(r["data"]) for r in rows],
        }

    # ── Audit log ────────────────────────────────────────────────────────

    async def get_audit_log(
        self, resource_type: Optional[str] = None, limit: int = 100
    ) -> list[dict]:
        assert self._conn
        if resource_type:
            async with self._conn.execute(
                """
                SELECT * FROM resource_events
                 WHERE resource_type = ?
                 ORDER BY timestamp DESC LIMIT ?
                """,
                (resource_type, limit),
            ) as cur:
                rows = await cur.fetchall()
        else:
            async with self._conn.execute(
                "SELECT * FROM resource_events ORDER BY timestamp DESC LIMIT ?", (limit,)
            ) as cur:
                rows = await cur.fetchall()

        return [dict(r) for r in rows]

    # ── Seed / count ─────────────────────────────────────────────────────

    async def bulk_seed(self, resource_type: str, items: list[dict]) -> int:
        """Insert many resources at once (used during initial seeding)."""
        count = 0
        for item in items:
            try:
                await self.create_resource(resource_type, item)
                count += 1
            except Exception as e:
                logger.warning("Seed skip %s: %s", resource_type, e)
        return count

    async def count_resources(self, resource_type: str) -> int:
        assert self._conn
        async with self._conn.execute(
            "SELECT COUNT(*) FROM resources WHERE resource_type = ?", (resource_type,)
        ) as cur:
            row = await cur.fetchone()
            return row[0] if row else 0
