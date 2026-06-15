"""DSCC (HPE GreenLake Data Services Cloud Console) adapter calling mock server."""

from __future__ import annotations
import os
import requests
from typing import Any, Dict, List
from adapters.base import BaseStorageAdapter


class DSCCStorageAdapter(BaseStorageAdapter):
    @property
    def provider_name(self) -> str:
        return "dscc"

    def _url(self, path: str) -> str:
        base_url = os.getenv("MOCK_STORAGE_SERVER_URL", "http://127.0.0.1:8004")
        return f"{base_url}{path}"

    def fetch_capacity(self, resource_id: str, resource_type: str, credentials: Dict[str, Any], parameters: Dict[str, Any]) -> Dict[str, Any]:
        # Dynamically scale capacity based on active secrets (used here as mock volume allocation)
        active_allocations = 0
        try:
            resp = requests.get(self._url("/data-services/v1beta1/secrets"), timeout=5.0)
            if resp.status_code == 200:
                secrets_list = resp.json().get("items", [])
                active_allocations = len(secrets_list)
        except Exception:
            pass
            
        total_tb = 500.0
        used_tb = min(120.0 + (active_allocations * 15.0), total_tb) # 15TB allocated per item
        free_tb = total_tb - used_tb
        utilization_pct = round((used_tb / total_tb) * 100.0, 1)

        try:
            resp = requests.get(self._url("/data-services/v1beta1/settings"), timeout=5.0)
            settings_data = resp.json() if resp.status_code == 200 else {}
        except Exception:
            settings_data = {}

        return {
            "total_tb": total_tb,
            "used_tb": used_tb,
            "free_tb": free_tb,
            "utilization_pct": utilization_pct,
            "provider_settings": settings_data
        }

    def fetch_performance(self, resource_id: str, resource_type: str, credentials: Dict[str, Any], parameters: Dict[str, Any]) -> Dict[str, Any]:
        try:
            resp = requests.get(self._url("/data-services/v1beta1/async-operations"), timeout=5.0)
            ops_data = resp.json() if resp.status_code == 200 else {}
        except Exception:
            ops_data = {}

        return {
            "read_iops": 12500,
            "write_iops": 8500,
            "read_latency_ms": 1.25,
            "write_latency_ms": 2.1,
            "active_operations": ops_data.get("count", 0)
        }

    def execute_action(self, resource_id: str, resource_type: str, action: str, credentials: Dict[str, Any], parameters: Dict[str, Any]) -> Dict[str, Any]:
        payload = {
            "service": "StorageAgent",
            "name": f"volume-{resource_id}",
            "secret": f"action-{action}"
        }
        try:
            resp = requests.post(self._url("/data-services/v1beta1/secrets"), json=payload, timeout=5.0)
            if resp.status_code in (200, 201):
                return {"result": "success", "detail": f"DSCC action {action} succeeded: {resp.json()}"}
            return {"result": "failed", "detail": f"DSCC mock server returned {resp.status_code}"}
        except Exception as e:
            return {"result": "failed", "detail": f"Failed to reach DSCC mock server: {e}"}

    def discover_arrays(self, credentials: Dict[str, Any], parameters: Dict[str, Any]) -> List[Dict[str, Any]]:
        try:
            resp = requests.get(self._url("/data-services/v1beta1/storage-locations"), timeout=5.0)
            if resp.status_code == 200:
                items = resp.json().get("items", [])
                return [
                    {
                        "id": item.get("id"),
                        "name": item.get("name"),
                        "type": "CloudStoragePool",
                        "status": "online",
                        "capacity_tb": 250.0
                    }
                    for item in items
                ]
        except Exception:
            pass
        return [{"id": "fallback-dscc-001", "name": "DSCC-Fallback-Array", "type": "SAN", "status": "online", "capacity_tb": 100.0}]

    def health_check(self, resource_id: str, resource_type: str, credentials: Dict[str, Any], parameters: Dict[str, Any]) -> Dict[str, Any]:
        try:
            resp = requests.get(self._url("/data-services/v1beta1/issues"), timeout=5.0)
            if resp.status_code == 200:
                issues = resp.json().get("items", [])
                healthy = len(issues) == 0
                return {
                    "healthy": healthy,
                    "detail": "No active issues on DSCC Console." if healthy else f"Found {len(issues)} active console issues.",
                    "checks": {"connectivity": "ok", "disk_status": "ok" if healthy else "degraded"}
                }
        except Exception as e:
            return {
                "healthy": False,
                "detail": f"Failed to connect to DSCC mock server: {e}",
                "checks": {"connectivity": "failed"}
            }
        return {"healthy": True, "detail": "DSCC health check default success.", "checks": {"connectivity": "ok"}}
