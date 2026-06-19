"""OASF Polling Engine — concurrent source collection with bounded threading."""

from __future__ import annotations

import logging
import os
import threading
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed, Future
from typing import Optional

import httpx

from cache import ResourceCache
from db_queries import DeviceQueries, PollHistoryQueries
from records import DeviceRecord

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

_DEFAULT_MAX_WORKERS: int = int(os.getenv("POLL_MAX_WORKERS", "8"))


# ---------------------------------------------------------------------------
# Mock DSCC client
# ---------------------------------------------------------------------------


class MockDSCCClient:
    """Mock DSCC/GreenLake client for discovering OneView instances."""

    def list_oneview_instances(self) -> list[str]:
        ov_host = os.getenv("HPE_OV_HOST", "oneview-01.mgmt.local")
        return [ov_host]


# ---------------------------------------------------------------------------
# Polling Engine
# ---------------------------------------------------------------------------


class PollingEngine:
    """OASF Polling Engine — concurrent collection, authoritative sync, cache warming."""

    def __init__(
        self,
        cache: ResourceCache,
        max_workers: int = _DEFAULT_MAX_WORKERS,
    ) -> None:
        self.cache = cache
        self.dscc_client = MockDSCCClient()
        self._max_workers = max_workers
        # Reconciliation state is now persisted in the poll_snapshots PostgreSQL
        # table — no in-memory baseline is maintained here.

    # ------------------------------------------------------------------
    # Source collectors
    # ------------------------------------------------------------------

    def poll_oneview(self, ov_host: str) -> list[dict]:
        """Fetch the current inventory for one OneView instance from PostgreSQL."""
        logger.info("[Polling][OneView] Starting collection | host=%s", ov_host)
        t0 = time.perf_counter()
        rows = DeviceQueries.list_devices_by_management_source(
            management_source="oneview", source_host=ov_host
        )
        devices = [DeviceRecord.from_row(row).to_dict() for row in rows]
        elapsed_ms = int((time.perf_counter() - t0) * 1000)
        logger.info(
            "[Polling][OneView] Collection complete | host=%s devices=%d elapsed_ms=%d",
            ov_host, len(devices), elapsed_ms,
        )
        return devices

    def poll_coms(self, acid: str) -> list[dict]:
        """Fetch the current COMS inventory from PostgreSQL."""
        logger.info("[Polling][COMS] Starting collection | acid=%s", acid)
        t0 = time.perf_counter()
        rows = DeviceQueries.list_devices_by_management_source(management_source="coms")
        devices = [DeviceRecord.from_row(row).to_dict() for row in rows]
        elapsed_ms = int((time.perf_counter() - t0) * 1000)
        logger.info(
            "[Polling][COMS] Collection complete | acid=%s devices=%d elapsed_ms=%d",
            acid, len(devices), elapsed_ms,
        )
        return devices

    def poll_mock_server(self, host: str) -> list[dict]:
        """Fetch the current mock_server inventory from PostgreSQL."""
        logger.info("[Polling][Mock Server] Starting collection | host=%s", host)
        t0 = time.perf_counter()
        rows = DeviceQueries.list_devices_by_management_source(
            management_source="mock_server", source_host=host
        )
        devices = [DeviceRecord.from_row(row).to_dict() for row in rows]
        elapsed_ms = int((time.perf_counter() - t0) * 1000)
        logger.info(
            "[Polling][Mock Server] Collection complete | host=%s devices=%d elapsed_ms=%d",
            host, len(devices), elapsed_ms,
        )
        return devices

    def poll_mock_storage(self, host: str) -> list[dict]:
        """Fetch the current mock_storage inventory from the live REST endpoint.

        Queries GET /data-services/v1beta1/devices on the mock storage server
        (default: http://127.0.0.1:8004) and normalises each item into the
        dict shape expected by DeviceQueries.sync_source_devices.
        """
        logger.info("[Polling][Mock Storage] Starting HTTP collection | host=%s", host)
        t0 = time.perf_counter()

        base_url = os.getenv("MOCK_STORAGE_URL", "http://127.0.0.1:8004")
        endpoint = f"{base_url}/data-services/v1beta1/devices"
        timeout = float(os.getenv("MOCK_STORAGE_TIMEOUT", "10"))

        try:
            response = httpx.get(endpoint, timeout=timeout)
            response.raise_for_status()
            raw_items: list[dict] = response.json()
        except httpx.HTTPError as exc:
            elapsed_ms = int((time.perf_counter() - t0) * 1000)
            logger.error(
                "[Polling][Mock Storage] HTTP request failed | host=%s url=%s error=%s elapsed_ms=%d",
                host, endpoint, exc, elapsed_ms,
            )
            raise

        # Normalise raw API items into the canonical device dict shape.
        devices: list[dict] = []
        for item in raw_items:
            serial = (
                item.get("serial_number")
                or item.get("id")
                or ""
            )
            if not serial:
                logger.warning(
                    "[Polling][Mock Storage] Skipping item with no serial_number | item=%r", item
                )
                continue
            devices.append({
                "serial_number":   str(serial),
                "ip_address":      item.get("ip_address"),
                "fqdn":            item.get("fqdn"),
                "management_source": "mock_storage",
                "source_host":     host,
                "source_device_id": str(item.get("id") or serial),
                "device_type":     item.get("device_type"),
                "last_seen":       item.get("updated_at") or item.get("last_seen"),
            })

        elapsed_ms = int((time.perf_counter() - t0) * 1000)
        logger.info(
            "[Polling][Mock Storage] HTTP collection complete | host=%s devices=%d elapsed_ms=%d",
            host, len(devices), elapsed_ms,
        )
        return devices

    def poll_mock_network(self, host: str) -> list[dict]:
        """Fetch the current mock_network inventory from PostgreSQL."""
        logger.info("[Polling][Mock Network] Starting collection | host=%s", host)
        t0 = time.perf_counter()
        rows = DeviceQueries.list_devices_by_management_source(
            management_source="mock_network", source_host=host
        )
        devices = [DeviceRecord.from_row(row).to_dict() for row in rows]
        elapsed_ms = int((time.perf_counter() - t0) * 1000)
        logger.info(
            "[Polling][Mock Network] Collection complete | host=%s devices=%d elapsed_ms=%d",
            host, len(devices), elapsed_ms,
        )
        return devices

    def poll_mock_cloud(self, host: str) -> list[dict]:
        """Fetch the current mock_cloud inventory from PostgreSQL."""
        logger.info("[Polling][Mock Cloud] Starting collection | host=%s", host)
        t0 = time.perf_counter()
        rows = DeviceQueries.list_devices_by_management_source(
            management_source="mock_cloud", source_host=host
        )
        devices = [DeviceRecord.from_row(row).to_dict() for row in rows]
        elapsed_ms = int((time.perf_counter() - t0) * 1000)
        logger.info(
            "[Polling][Mock Cloud] Collection complete | host=%s devices=%d elapsed_ms=%d",
            host, len(devices), elapsed_ms,
        )
        return devices

    # ------------------------------------------------------------------
    # Per-source sync + warm (called from worker threads)
    # ------------------------------------------------------------------

    def _collect_source(
        self,
        source_type: str,
        source_host: str,
        cycle_id: str,
    ) -> dict:
        """
        Collect, normalize, and return one source's batch result.
        Called concurrently inside the thread pool — must be fully self-contained.
        """
        t0 = time.perf_counter()
        try:
            collector_name = f"poll_{source_type.lower()}"
            collector = getattr(self, collector_name, None)
            if collector is None:
                raise ValueError(f"No collector defined for source type {source_type!r}")
            devices = collector(source_host)

            logger.info(
                "[Polling][%s] Collection succeeded | host=%s devices=%d cycle=%s",
                source_type.upper(), source_host, len(devices), cycle_id,
            )
            return {
                "source_type": source_type,
                "source_host": source_host,
                "devices": devices,
                "status": "success",
                "error": None,
                "collection_ms": int((time.perf_counter() - t0) * 1000),
            }

        except Exception as exc:
            elapsed_ms = int((time.perf_counter() - t0) * 1000)
            logger.error(
                "[Polling][%s] Collection failed | host=%s error=%s cycle=%s elapsed_ms=%d",
                source_type.upper(), source_host, exc, cycle_id, elapsed_ms,
            )
            return {
                "source_type": source_type,
                "source_host": source_host,
                "devices": [],
                "status": "failed",
                "error": str(exc),
                "collection_ms": elapsed_ms,
            }

    # ------------------------------------------------------------------
    # Post-collection: sync + warm (sequential — called after all futures resolve)
    # ------------------------------------------------------------------

    def _sync_and_warm(self, item: dict, cycle_start: float, cycle_id: str) -> None:
        """
        Sync one collected batch to PostgreSQL and warm Memurai.
        Runs sequentially after concurrent collection completes.
        """
        source_type = item["source_type"]
        source_host = item["source_host"]
        source_key  = (source_type, source_host)
        duration_ms = int((time.perf_counter() - cycle_start) * 1000)

        if item["status"] == "success":
            # 3. Authoritative PostgreSQL sync
            sync_res = DeviceQueries.sync_source_devices(
                management_source=source_type,
                source_host=source_host,
                devices=item["devices"],
            )

            # 4. Incremental warming is disabled during polling cycles to prevent bulk cache churn.
            # Redis is populated lazily on demand when lookups occur.

            # 5. Poll history — use DB-computed diff counts
            PollHistoryQueries.log({
                "source_type": source_type,
                "source_host": source_host,
                "devices_found": sync_res["devices_found"],
                "devices_added": sync_res["devices_added"],
                "devices_removed": sync_res["devices_removed"],
                "duration_ms": duration_ms,
                "status": "success",
                "error_message": None,
            })
            logger.info(
                "[Polling][Sync] Source synced | source=%s host=%s "
                "found=%d added=%d removed=%d duration_ms=%d cycle=%s",
                source_type, source_host,
                sync_res["devices_found"], sync_res["devices_added"],
                sync_res["devices_removed"], duration_ms, cycle_id,
            )

        else:
            PollHistoryQueries.log({
                "source_type": source_type,
                "source_host": source_host,
                "devices_found": 0,
                "devices_added": 0,
                "devices_removed": 0,
                "duration_ms": duration_ms,
                "status": "failed",
                "error_message": item["error"],
            })
            logger.warning(
                "[Polling][Sync] Source failed | source=%s host=%s error=%s cycle=%s",
                source_type, source_host, item["error"], cycle_id,
            )

    # ------------------------------------------------------------------
    # Main poll cycle
    # ------------------------------------------------------------------

    def run_poll_cycle(self) -> list[dict]:
        """
        Execute a full poll cycle with concurrent source collection.

        Lifecycle:
            Discovery
            ↓
            Concurrent collection (ThreadPoolExecutor)
            ↓
            Normalization
            ↓
            PostgreSQL authoritative sync
            ↓
            Incremental Memurai warming
            ↓
            Poll history logging
        """
        cycle_id = uuid.uuid4().hex[:8]
        cycle_start = time.perf_counter()
        logger.info("[Polling] Poll cycle started | cycle=%s max_workers=%d", cycle_id, self._max_workers)

        # 1. Discovery
        ov_instances = self.dscc_client.list_oneview_instances()
        coms_acid = os.getenv("COMS_ACID", "coms-01.cloud.local")

        # Build the full list of (source_type, source_host) work items
        work_items: list[tuple[str, str]] = [
            ("oneview", ov) for ov in ov_instances
        ] + [
            ("coms", coms_acid),
            ("mock_server", "mock-server-manager.local"),
            ("mock_storage", "mock-storage-manager.local"),
            ("mock_network", "mock-network-manager.local"),
            ("mock_cloud", "mock-cloud-manager.local"),
        ]
        logger.info(
            "[Polling] Sources scheduled | cycle=%s count=%d sources=%s",
            cycle_id, len(work_items),
            [f"{st}:{sh}" for st, sh in work_items],
        )

        # 2. Concurrent collection — bounded by max_workers
        collected_batches: list[dict] = []
        future_to_source: dict[Future, tuple[str, str]] = {}

        with ThreadPoolExecutor(max_workers=self._max_workers) as executor:
            for source_type, source_host in work_items:
                future = executor.submit(
                    self._collect_source, source_type, source_host, cycle_id
                )
                future_to_source[future] = (source_type, source_host)

            for future in as_completed(future_to_source):
                source_type, source_host = future_to_source[future]
                try:
                    batch = future.result()
                except Exception as exc:
                    # Defensive catch — _collect_source already handles its own
                    # exceptions, but protect the outer loop regardless.
                    logger.error(
                        "[Polling] Unexpected future error | source=%s host=%s error=%s cycle=%s",
                        source_type, source_host, exc, cycle_id,
                    )
                    batch = {
                        "source_type": source_type,
                        "source_host": source_host,
                        "devices": [],
                        "status": "failed",
                        "error": str(exc),
                        "collection_ms": 0,
                    }
                collected_batches.append(batch)

        collection_ms = int((time.perf_counter() - cycle_start) * 1000)
        logger.info(
            "[Polling] Concurrent collection complete | cycle=%s sources=%d collection_ms=%d",
            cycle_id, len(collected_batches), collection_ms,
        )

        # 3-5. Sequential sync + warm + history logging (per source)
        results: list[dict] = []
        for batch in collected_batches:
            try:
                self._sync_and_warm(batch, cycle_start, cycle_id)
            except Exception as exc:
                logger.error(
                    "[Polling] Sync/warm failed | source=%s host=%s error=%s cycle=%s",
                    batch["source_type"], batch["source_host"], exc, cycle_id,
                )
            results.append(batch)

        total_ms = int((time.perf_counter() - cycle_start) * 1000)
        success_count = sum(1 for b in results if b["status"] == "success")
        fail_count = len(results) - success_count
        logger.info(
            "[Polling] Poll cycle complete | cycle=%s total_ms=%d success=%d failed=%d",
            cycle_id, total_ms, success_count, fail_count,
        )
        return results


def start_background_polling(cache: ResourceCache, interval_seconds: int = 600) -> threading.Thread:
    """Start the PollingEngine running in a background daemon thread."""
    pe = PollingEngine(cache)

    def _loop() -> None:
        logger.info(
            "[Polling] Starting background polling thread (interval=%ds)",
            interval_seconds,
        )
        # Allow startup connection settling
        time.sleep(5)
        while True:
            try:
                pe.run_poll_cycle()
            except Exception as exc:
                logger.exception("[Polling] Background poll cycle encountered error: %s", exc)
            time.sleep(interval_seconds)

    thread = threading.Thread(
        target=_loop,
        name="OASF-Background-Polling",
        daemon=True,
    )
    thread.start()
    return thread

