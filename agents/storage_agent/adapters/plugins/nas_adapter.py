"""NAS adapter stub — integrate NFS/SMB REST management APIs in production."""

from __future__ import annotations
from typing import Any, Dict, List
from adapters.base import BaseStorageAdapter


class NASStorageAdapter(BaseStorageAdapter):
    @property
    def provider_name(self) -> str:
        return "nas"

    def fetch_capacity(self, resource_id, resource_type, credentials, parameters) -> Dict[str, Any]:
        return {"note": f"[NAS STUB] capacity for {resource_id}."}

    def fetch_performance(self, resource_id, resource_type, credentials, parameters) -> Dict[str, Any]:
        return {"note": f"[NAS STUB] performance for {resource_id}."}

    def execute_action(self, resource_id, resource_type, action, credentials, parameters) -> Dict[str, Any]:
        return {"result": "stub", "detail": f"[NAS STUB] action='{action}' on {resource_id}."}

    def discover_arrays(self, credentials, parameters) -> List[Dict[str, Any]]:
        return [{"note": "[NAS STUB] array discovery."}]

    def health_check(self, resource_id, resource_type, credentials, parameters) -> Dict[str, Any]:
        return {"healthy": True, "detail": f"[NAS STUB] health-check for {resource_id}."}
