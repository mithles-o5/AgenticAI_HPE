"""APScheduler-based poll handler for periodic DSCC capacity pulls."""

from __future__ import annotations
import logging
from datetime import datetime
from typing import Any, Callable, Dict, Optional

try:
    from apscheduler.schedulers.background import BackgroundScheduler
    _HAS_APScheduler = True
except ImportError:
    _HAS_APScheduler = False

from config.settings import settings

logger = logging.getLogger(__name__)


class StoragePollHandler:
    """
    Periodically polls a registered list of storage resources and
    invokes a callback with the raw capacity/performance data.

    Usage:
        handler = StoragePollHandler(poll_callback=my_fn)
        handler.start()
        # ... app runs ...
        handler.stop()
    """

    def __init__(self, poll_callback: Optional[Callable] = None) -> None:
        self._callback = poll_callback or self._default_callback
        self._jobs: Dict[str, Any] = {}     # resource_id → job metadata
        if _HAS_APScheduler:
            self._scheduler = BackgroundScheduler()
        else:
            self._scheduler = None
            logger.warning("apscheduler not installed — poll handler disabled.")

    def start(self) -> None:
        if self._scheduler:
            self._scheduler.start()
            logger.info("StoragePollHandler started (interval=%ds).", settings.POLL_INTERVAL_SECONDS)

    def stop(self) -> None:
        if self._scheduler and self._scheduler.running:
            self._scheduler.shutdown(wait=False)
            logger.info("StoragePollHandler stopped.")

    def register_resource(
        self,
        resource_id: str,
        adapter_provider: str,
        credentials_ref: str,
        resource_type: str = "volume",
    ) -> None:
        """Register a resource for periodic polling."""
        if self._scheduler is None:
            return

        job_id = f"poll-{resource_id}"
        self._scheduler.add_job(
            func=self._poll_resource,
            trigger="interval",
            seconds=settings.POLL_INTERVAL_SECONDS,
            id=job_id,
            replace_existing=True,
            kwargs={
                "resource_id":      resource_id,
                "adapter_provider": adapter_provider,
                "credentials_ref":  credentials_ref,
                "resource_type":    resource_type,
            },
        )
        self._jobs[resource_id] = {
            "job_id":   job_id,
            "provider": adapter_provider,
            "registered_at": datetime.utcnow().isoformat(),
        }
        logger.info("Registered poll job for resource '%s' (provider=%s).", resource_id, adapter_provider)

    def _poll_resource(
        self,
        resource_id: str,
        adapter_provider: str,
        credentials_ref: str,
        resource_type: str,
    ) -> None:
        """Internal poll function executed by the scheduler."""
        try:
            from core.adapter_manager import StorageAdapterManager
            from core.cred_vault_client import CredVaultClient

            adapter = StorageAdapterManager.get(adapter_provider)
            creds   = CredVaultClient().get(credentials_ref)
            capacity = adapter.fetch_capacity(resource_id, resource_type, creds, {})
            perf     = adapter.fetch_performance(resource_id, resource_type, creds, {})
            self._callback(resource_id, capacity, perf)
        except Exception as exc:
            logger.error("Poll failed for '%s': %s", resource_id, exc)

    @staticmethod
    def _default_callback(resource_id: str, capacity: dict, perf: dict) -> None:
        logger.info("[POLL] resource=%s capacity=%s perf=%s", resource_id, capacity, perf)

    def registered_jobs(self) -> Dict[str, Any]:
        return dict(self._jobs)
