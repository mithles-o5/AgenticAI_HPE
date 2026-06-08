"""Database queries for the authoritative resource resolver registry."""

from __future__ import annotations

from typing import Iterable, Optional

from psycopg2 import extras

from db import db_manager
from enums import IdentifierType
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
        if source == "CoM":
            source_aliases.extend(["com", "coms"])
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

        NOTE: The polling collectors (poll_oneview / poll_coms) read from the
        same PostgreSQL database that this method writes to.  That means the
        incoming ``devices`` list already reflects the current DB state, so a
        naïve upsert+rowcount approach always reports added=0 and removed=0.

        Fix: snapshot the serial numbers that exist for this (source, host)
        pair *before* the upsert loop, then compute the diff manually:
          - added   = serial numbers in the incoming list but NOT in the snapshot
          - removed = serial numbers in the snapshot but NOT in the incoming list
                      (these rows are also physically deleted below)
        """
        source = normalize_management_source(management_source)
        device_rows = list(devices)
        incoming_sns: set[str] = {
            str(d["serial_number"]).strip() for d in device_rows
        }
        conn = db_manager.get_connection()

        try:
            with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
                # ── Step 1: snapshot existing SNs for this source/host ──────
                cur.execute(
                    """
                    SELECT serial_number
                    FROM devices
                    WHERE lower(management_source) = lower(%s)
                      AND lower(source_host)       = lower(%s)
                    """,
                    (source, source_host),
                )
                existing_sns: set[str] = {row["serial_number"] for row in cur.fetchall()}

                # ── Step 2: diff ─────────────────────────────────────────────
                added_sns   = incoming_sns - existing_sns   # new arrivals
                removed_sns = existing_sns - incoming_sns   # departed devices

                # ── Step 3: upsert incoming devices ──────────────────────────
                serial_numbers: list[str] = []
                for device in device_rows:
                    serial_number = str(device["serial_number"]).strip()
                    serial_numbers.append(serial_number)
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

                # ── Step 4: delete devices no longer reported ─────────────────
                if serial_numbers:
                    cur.execute(
                        """
                        DELETE FROM devices
                        WHERE lower(management_source) = lower(%s)
                          AND lower(source_host) = lower(%s)
                          AND NOT (serial_number = ANY(%s))
                        """,
                        (source, source_host, serial_numbers),
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
            "devices_added": len(added_sns),
            "devices_removed": len(removed_sns),
        }


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
