"""Database queries for the authoritative resource resolver registry."""

from __future__ import annotations

from typing import Iterable, Optional

from psycopg2 import extras

from db import db_manager
from enums import IdentifierType
from errors import EndpointNotFoundError
from protocol_discovery import normalize_management_source


def _device_select() -> str:
    return """
        SELECT
            d.id::text AS id,
            d.serial_number,
            d.ip_address,
            d.fqdn,
            d.management_source,
            d.source_host,
            d.source_device_id,
            d.device_type,
            d.last_seen,
            d.created_at,
            d.updated_at
        FROM devices d
    """


class DeviceQueries:
    """Exact device lookups and source synchronization."""

    @staticmethod
    def get_by_id(device_id: str) -> Optional[dict]:
        return db_manager.execute_query(
            _device_select() + " WHERE d.id = %s::uuid LIMIT 1",
            (device_id,),
            fetch_one=True,
        )

    @staticmethod
    def get_by_ip(ip_address: str) -> Optional[dict]:
        return db_manager.execute_query(
            _device_select() + " WHERE d.ip_address = %s::inet LIMIT 1",
            (ip_address,),
            fetch_one=True,
        )

    @staticmethod
    def get_by_serial(serial_number: str) -> Optional[dict]:
        return db_manager.execute_query(
            _device_select() + " WHERE lower(d.serial_number) = lower(%s) LIMIT 1",
            (serial_number,),
            fetch_one=True,
        )

    @staticmethod
    def get_by_fqdn(fqdn: str) -> Optional[dict]:
        return db_manager.execute_query(
            _device_select() + " WHERE lower(d.fqdn) = lower(%s) LIMIT 1",
            (fqdn,),
            fetch_one=True,
        )

    @classmethod
    def get_by_identifier(
        cls,
        identifier: str,
        identifier_type: IdentifierType,
    ) -> Optional[dict]:
        if identifier_type == IdentifierType.IP:
            return cls.get_by_ip(identifier)
        if identifier_type == IdentifierType.FQDN:
            return cls.get_by_fqdn(identifier)
        return cls.get_by_serial(identifier)

    @staticmethod
    def list_all(limit: int = 1000, offset: int = 0) -> list[dict]:
        return db_manager.execute_query(
            _device_select()
            + """
                ORDER BY d.serial_number
                LIMIT %s OFFSET %s
            """,
            (limit, offset),
            fetch_all=True,
        ) or []

    @staticmethod
    def list_devices_by_management_source(
        management_source: str,
        source_host: Optional[str] = None,
    ) -> list[dict]:
        source = normalize_management_source(management_source)
        source_aliases = [source]
        if source_host:
            query = (
                _device_select()
                + """
                    WHERE lower(d.management_source) = ANY(%s)
                      AND lower(d.source_host) = lower(%s)
                    ORDER BY d.serial_number
                """
            )
            params = ([alias.lower() for alias in source_aliases], source_host)
        else:
            query = (
                _device_select()
                + """
                    WHERE lower(d.management_source) = ANY(%s)
                    ORDER BY d.serial_number
                """
            )
            params = ([alias.lower() for alias in source_aliases],)
        return db_manager.execute_query(query, params, fetch_all=True) or []

    @staticmethod
    def count_total() -> int:
        row = db_manager.execute_query(
            "SELECT COUNT(*) AS count FROM devices",
            fetch_one=True,
        )
        return int(row["count"]) if row else 0

    @staticmethod
    def upsert(device: dict) -> dict:
        source = normalize_management_source(device["management_source"])
        row = db_manager.execute_query(
            """
            INSERT INTO devices (
                serial_number, ip_address, fqdn, management_source,
                source_host, source_device_id, device_type, last_seen, created_at, updated_at
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, COALESCE(%s, NOW()), NOW(), NOW())
            ON CONFLICT (serial_number) DO UPDATE SET
                ip_address = EXCLUDED.ip_address,
                fqdn = EXCLUDED.fqdn,
                management_source = EXCLUDED.management_source,
                source_host = EXCLUDED.source_host,
                source_device_id = EXCLUDED.source_device_id,
                device_type = EXCLUDED.device_type,
                last_seen = EXCLUDED.last_seen,
                updated_at = NOW()
            RETURNING id::text AS id, serial_number, ip_address, fqdn,
                      management_source, source_host, source_device_id, device_type,
                      last_seen, created_at, updated_at
            """,
            (
                device["serial_number"],
                device.get("ip_address"),
                device.get("fqdn"),
                source,
                device.get("source_host"),
                device.get("source_device_id"),
                device.get("device_type"),
                device.get("last_seen"),
            ),
            fetch_one=True,
        )
        return dict(row)

    @staticmethod
    def sync_source_devices(
        management_source: str,
        source_host: str,
        devices: Iterable[dict],
    ) -> dict:
        """Upsert one source's inventory and remove devices no longer reported.

        Reconciliation is performed against the **previous poll snapshot**
        stored in the ``poll_snapshots`` table (not the live ``devices`` table),
        so the diff is accurate even across service restarts and crashes.

        Behaviour on the very first poll for a source (no previous snapshot):
            devices_added = 0
            devices_removed = 0
        The current inventory is stored as the baseline for the next poll.

        Returns:
            dict containing:
                ``source_type``    : normalised management source
                ``source_host``    : source host identifier
                ``devices_found``  : total incoming count from the live source
                ``devices_added``  : serial numbers present now but not in last snapshot
                ``devices_removed``: serial numbers in last snapshot but absent now
        """
        source = normalize_management_source(management_source)
        device_rows = list(devices)
        incoming_sns = {str(d["serial_number"]).strip() for d in device_rows}
        conn = db_manager.get_connection()

        try:
            with conn.cursor() as cur:
                # ── 1. Load the previous poll snapshot (persistent baseline) ──────────
                cur.execute(
                    """
                    SELECT serial_numbers
                    FROM poll_snapshots
                    WHERE lower(source_type) = lower(%s)
                      AND lower(source_host) = lower(%s)
                    """,
                    (source, source_host),
                )
                snapshot_row = cur.fetchone()

                if snapshot_row is None:
                    # First-ever poll for this source — no baseline exists yet.
                    # Report zero diff so we don't generate false positives.
                    previous_sns: set[str] = set()
                    is_first_poll = True
                else:
                    previous_sns = set(snapshot_row[0])  # psycopg2 deserialises JSONB → list
                    is_first_poll = False

                if is_first_poll:
                    devices_added = 0
                    devices_removed = 0
                else:
                    devices_added   = len(incoming_sns - previous_sns)
                    devices_removed = len(previous_sns - incoming_sns)

                # ── 2. Upsert incoming devices into the authoritative table ────────────
                for device in device_rows:
                    serial_number = str(device["serial_number"]).strip()
                    cur.execute(
                        """
                        INSERT INTO devices (
                            serial_number, ip_address, fqdn, management_source,
                            source_host, source_device_id, device_type, last_seen,
                            created_at, updated_at
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, COALESCE(%s, NOW()), NOW(), NOW())
                        ON CONFLICT (serial_number) DO UPDATE SET
                            ip_address = EXCLUDED.ip_address,
                            fqdn = EXCLUDED.fqdn,
                            management_source = EXCLUDED.management_source,
                            source_host = EXCLUDED.source_host,
                            source_device_id = EXCLUDED.source_device_id,
                            device_type = EXCLUDED.device_type,
                            last_seen = EXCLUDED.last_seen,
                            updated_at = NOW()
                        """,
                        (
                            serial_number,
                            device.get("ip_address"),
                            device.get("fqdn"),
                            source,
                            source_host,
                            device.get("source_device_id"),
                            device.get("device_type"),
                            device.get("last_seen"),
                        ),
                    )

                # ── 3. Purge devices that disappeared from the live source ─────────────
                if incoming_sns:
                    cur.execute(
                        """
                        DELETE FROM devices
                        WHERE lower(management_source) = lower(%s)
                          AND lower(source_host) = lower(%s)
                          AND NOT (serial_number = ANY(%s))
                        """,
                        (source, source_host, list(incoming_sns)),
                    )
                else:
                    cur.execute(
                        """
                        DELETE FROM devices
                        WHERE lower(management_source) = lower(%s)
                          AND lower(source_host) = lower(%s)
                        """,
                        (source, source_host),
                    )

                # ── 4. Persist the new snapshot as the baseline for the next poll ──────
                import json as _json
                cur.execute(
                    """
                    INSERT INTO poll_snapshots (source_type, source_host, serial_numbers, snapshot_at)
                    VALUES (%s, %s, %s::jsonb, NOW())
                    ON CONFLICT (source_type, source_host) DO UPDATE SET
                        serial_numbers = EXCLUDED.serial_numbers,
                        snapshot_at    = EXCLUDED.snapshot_at
                    """,
                    (source, source_host, _json.dumps(list(incoming_sns))),
                )

            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            db_manager.return_connection(conn)

        return {
            "source_type": source,
            "source_host": source_host,
            "devices_found": len(device_rows),
            "devices_added": devices_added,
            "devices_removed": devices_removed,
        }



class PollSnapshotQueries:
    """Read and write persistent poll snapshots used as the reconciliation baseline."""

    @staticmethod
    def get(source_type: str, source_host: str) -> Optional[set[str]]:
        """Return the last persisted serial-number set for a source, or None on first poll."""
        row = db_manager.execute_query(
            """
            SELECT serial_numbers
            FROM poll_snapshots
            WHERE lower(source_type) = lower(%s)
              AND lower(source_host) = lower(%s)
            """,
            (source_type, source_host),
            fetch_one=True,
        )
        if row is None:
            return None
        return set(row["serial_numbers"])

    @staticmethod
    def save(source_type: str, source_host: str, serial_numbers: set[str]) -> None:
        """Upsert the snapshot for a source after a successful poll cycle."""
        import json as _json
        db_manager.execute_query(
            """
            INSERT INTO poll_snapshots (source_type, source_host, serial_numbers, snapshot_at)
            VALUES (%s, %s, %s::jsonb, NOW())
            ON CONFLICT (source_type, source_host) DO UPDATE SET
                serial_numbers = EXCLUDED.serial_numbers,
                snapshot_at    = EXCLUDED.snapshot_at
            """,
            (source_type, source_host, _json.dumps(list(serial_numbers))),
            fetch_all=False,
        )


class RoutingAuditQueries:
    @staticmethod
    def log(
        identifier: str,
        identifier_type: IdentifierType,
        resolved_source: Optional[str],
        resolved_host: Optional[str],
        cache_hit: bool,
        resolution_ms: int,
        requested_by: Optional[str],
    ) -> None:
        db_manager.execute_query(
            """
            INSERT INTO routing_audit (
                identifier, identifier_type, resolved_source, resolved_host,
                cache_hit, resolution_ms, requested_by, timestamp
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
            """,
            (
                identifier,
                identifier_type.value,
                resolved_source,
                resolved_host,
                cache_hit,
                resolution_ms,
                requested_by,
            ),
            fetch_all=False,
        )


class PollHistoryQueries:
    @staticmethod
    def log(result: dict) -> None:
        db_manager.execute_query(
            """
            INSERT INTO poll_history (
                source_type, source_host, devices_found, devices_added,
                devices_removed, duration_ms, status, error_message, timestamp
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW())
            """,
            (
                result["source_type"],
                result["source_host"],
                result.get("devices_found", 0),
                result.get("devices_added", 0),
                result.get("devices_removed", 0),
                result.get("duration_ms"),
                result.get("status"),
                result.get("error_message"),
            ),
            fetch_all=False,
        )


class StatisticsQueries:
    @staticmethod
    def devices_by_source() -> list[dict]:
        return db_manager.execute_query(
            """
            SELECT management_source, source_host, COUNT(*) AS device_count
            FROM devices
            GROUP BY management_source, source_host
            ORDER BY management_source, source_host
            """,
            fetch_all=True,
        ) or []

    @staticmethod
    def routing_audit_by_source() -> list[dict]:
        return db_manager.execute_query(
            """
            SELECT resolved_source, cache_hit, COUNT(*) AS audit_count
            FROM routing_audit
            GROUP BY resolved_source, cache_hit
            ORDER BY resolved_source, cache_hit
            """,
            fetch_all=True,
        ) or []

    @staticmethod
    def poll_history_by_source() -> list[dict]:
        return db_manager.execute_query(
            """
            SELECT source_type, source_host, status, COUNT(*) AS poll_count
            FROM poll_history
            GROUP BY source_type, source_host, status
            ORDER BY source_type, source_host, status
            """,
            fetch_all=True,
        ) or []


def get_statistics() -> dict:
    return {
        "devices_by_source": StatisticsQueries.devices_by_source(),
        "routing_audit_by_source": StatisticsQueries.routing_audit_by_source(),
        "poll_history_by_source": StatisticsQueries.poll_history_by_source(),
    }


# ---------------------------------------------------------------------------
# Endpoint Registry Queries
# ---------------------------------------------------------------------------

logger_ep = __import__("logging").getLogger(__name__)


class EndpointRegistryQueries:
    """
    Thread-safe lookup helper for the endpoint_registry table.

    Each call acquires a pooled connection, runs the SELECT, and releases it.
    No connection is held between calls.

    Lookup priority
    ---------------
    1. Exact match on (vendor, device_type, action_key)
    2. Fallback to (vendor, 'server', action_key)  — covers the case where
       device_type in the devices table is NULL / unmapped.
    3. Raise EndpointNotFoundError if neither resolves.
    """

    @staticmethod
    def get_endpoint(
        vendor: str,
        device_type: str,
        action_key: str,
    ) -> dict:
        """
        Resolve a (vendor, device_type, action_key) triple to its exact
        HTTP method and API path as stored in the registry.

        Parameters
        ----------
        vendor      : normalised management source  ("oneview" / "coms")
        device_type : device classification         ("server", "storage", …)
        action_key  : action key as stored in the registry
                      ("On", "Status", "get_rest_server_hardware_id", …)

        Returns
        -------
        dict with keys:
            ``http_method`` (str)  — e.g. "PUT"
            ``api_path``    (str)  — e.g. "/rest/server-hardware/{id}/powerState"
            ``device_type`` (str)  — matched device_type (may differ if fallback used)

        Raises
        ------
        EndpointNotFoundError
            When no row matches via exact or fallback lookup.
        """
        # ── Pass 1: exact match ───────────────────────────────────────────────
        row = db_manager.execute_query(
            """
            SELECT http_method, api_path, device_type
            FROM   endpoint_registry
            WHERE  lower(vendor)      = lower(%s)
              AND  lower(device_type) = lower(%s)
              AND  lower(action_key)  = lower(%s)
            LIMIT 1
            """,
            (vendor, device_type or "server", action_key),
            fetch_one=True,
        )

        if row is None and (device_type or "server").lower() != "server":
            # ── Pass 2: fallback to 'server' (most common operational type) ───
            logger_ep.debug(
                "[EndpointRegistry] No exact match for device_type=%r — trying 'server' fallback",
                device_type,
            )
            row = db_manager.execute_query(
                """
                SELECT http_method, api_path, device_type
                FROM   endpoint_registry
                WHERE  lower(vendor)      = lower(%s)
                  AND  lower(device_type) = 'server'
                  AND  lower(action_key)  = lower(%s)
                LIMIT 1
                """,
                (vendor, action_key),
                fetch_one=True,
            )

        if row is None:
            logger_ep.warning(
                "[EndpointRegistry] No endpoint found | vendor=%r "
                "device_type=%r action_key=%r",
                vendor, device_type, action_key,
            )
            raise EndpointNotFoundError(
                f"No endpoint registered for vendor={vendor!r} "
                f"device_type={device_type!r} action_key={action_key!r}"
            )

        logger_ep.debug(
            "[EndpointRegistry] Resolved | vendor=%s device_type=%s "
            "action_key=%s → %s %s",
            vendor, row["device_type"], action_key,
            row["http_method"], row["api_path"],
        )
        return {
            "http_method": row["http_method"],
            "api_path":    row["api_path"],
            "device_type": row["device_type"],
        }

    @staticmethod
    def list_by_vendor(vendor: str) -> list[dict]:
        """Return all registered endpoints for a vendor (useful for debugging)."""
        rows = db_manager.execute_query(
            """
            SELECT device_type, action_key, http_method, api_path
            FROM   endpoint_registry
            WHERE  lower(vendor) = lower(%s)
            ORDER  BY device_type, action_key
            """,
            (vendor,),
            fetch_all=True,
        )
        return [dict(r) for r in rows] if rows else []

    @staticmethod
    def list_by_vendor_and_type(vendor: str, device_type: str) -> list[dict]:
        """Return all endpoints for a specific (vendor, device_type) pair."""
        rows = db_manager.execute_query(
            """
            SELECT action_key, http_method, api_path
            FROM   endpoint_registry
            WHERE  lower(vendor)      = lower(%s)
              AND  lower(device_type) = lower(%s)
            ORDER  BY action_key
            """,
            (vendor, device_type),
            fetch_all=True,
        )
        return [dict(r) for r in rows] if rows else []
