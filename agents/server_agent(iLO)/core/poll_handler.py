import httpx
import structlog
import asyncio
from typing import Dict, Any, List
from datetime import datetime

try:
    from apscheduler.schedulers.background import BackgroundScheduler
    _HAS_APScheduler = True
except ImportError:
    _HAS_APScheduler = False

from config.settings import settings
from core.adapter_manager import get_adapter
from core.normalization import normalize_metrics
from core.anomaly_detection import detect_anomalies

logger = structlog.get_logger()

STATIC_SERVERS = [
    {"id": "OV1-RackServer-001", "provider": "redfish", "credentials_ref": "mock"},
    {"id": "CoM-CloudNode-001", "provider": "ilo", "credentials_ref": "mock"},
    {"id": "MS-123", "provider": "ipmi", "credentials_ref": "mock"},
]

class ServerPollHandler:
    def __init__(self) -> None:
        self.scheduler = BackgroundScheduler() if _HAS_APScheduler else None

    def start(self) -> None:
        if self.scheduler and settings.POLL_ENABLED:
            self.scheduler.add_job(
                self.run_poll_cycle,
                "interval",
                seconds=settings.POLL_INTERVAL_SECONDS,
                id="server-poll-job",
                replace_existing=True
            )
            self.scheduler.start()
            logger.info("ServerPollHandler started", interval=settings.POLL_INTERVAL_SECONDS)

    def stop(self) -> None:
        if self.scheduler and self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("ServerPollHandler stopped")

    def run_poll_cycle(self) -> Dict[str, int]:
        """Runs one full poll cycle synchronously and returns the counts."""
        summary = {"polled": 0, "warnings": 0, "criticals": 0, "errors": 0}
        
        # 1. Fetch server list
        servers = []
        if settings.POLL_SERVER_LIST_SOURCE == "cmdb":
            try:
                with httpx.Client(timeout=5.0) as client:
                    resp = client.get(f"{settings.CMDB_URL}/resources", params={"type": "server"})
                    if resp.status_code == 200:
                        servers = resp.json().get("items", [])
                    else:
                        logger.warning("CMDB returned non-200, falling back to static server list", status_code=resp.status_code)
                        servers = STATIC_SERVERS
            except Exception as e:
                logger.warning("Failed to reach CMDB for server list, falling back to static server list", error=str(e))
                servers = STATIC_SERVERS
        else:
            servers = STATIC_SERVERS

        logger.info("Starting server poll cycle", count=len(servers))

        # 2. Poll each server
        for s in servers:
            resource_id = s.get("id") or s.get("resource_id") or s.get("serial_number")
            provider = s.get("provider") or "default"
            credentials_ref = s.get("credentials_ref") or "mock"
            
            if not resource_id:
                summary["errors"] += 1
                continue

            try:
                adapter = get_adapter(provider, credentials_ref)
                
                # Fetch metrics and sensors
                raw_metrics = adapter.fetch_system_metrics(resource_id)
                sensors = adapter.fetch_sensors(resource_id)
                
                # Merge and normalize
                raw_metrics["sensors"] = sensors
                normalized = normalize_metrics(raw_metrics)
                
                # Anomaly check
                level, insights = detect_anomalies(normalized)
                
                summary["polled"] += 1
                if level.value == "warning":
                    summary["warnings"] += 1
                elif level.value == "critical":
                    summary["criticals"] += 1

                # Sync to CMDB
                self._write_to_cmdb(resource_id, normalized.model_dump(), level.value)

            except Exception as exc:
                logger.error("Failed to poll server during cycle", resource_id=resource_id, error=str(exc))
                summary["errors"] += 1

        logger.info("Server poll cycle completed", summary=summary)
        return summary

    def _write_to_cmdb(self, resource_id: str, metrics: dict, status_level: str) -> None:
        try:
            url = f"{settings.CMDB_URL}/resources/{resource_id}/metrics"
            payload = {
                "metrics": metrics,
                "status_level": status_level,
                "agent": "server-agent",
                "updated_at": datetime.utcnow().isoformat()
            }
            with httpx.Client(timeout=5.0) as client:
                resp = client.put(url, json=payload)
                # Fail silently or log warn since this is mock server
                if resp.status_code not in (200, 201, 204):
                    logger.debug("CMDB put returned non-200", status_code=resp.status_code)
        except Exception as e:
            logger.debug("Bypassed CMDB PUT / failed to post metrics", error=str(e))
