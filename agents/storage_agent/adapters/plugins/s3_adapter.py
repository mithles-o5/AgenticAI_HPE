"""S3-compatible object storage adapter stub — integrate boto3 / MinIO in production."""

from __future__ import annotations
from typing import Any, Dict, List
from adapters.base import BaseStorageAdapter


class S3StorageAdapter(BaseStorageAdapter):
    @property
    def provider_name(self) -> str:
        return "s3"

    def fetch_capacity(self, resource_id, resource_type, credentials, parameters) -> Dict[str, Any]:
        return {"note": f"[S3 STUB] capacity for bucket '{resource_id}'."}

    def fetch_performance(self, resource_id, resource_type, credentials, parameters) -> Dict[str, Any]:
        return {"note": f"[S3 STUB] performance for bucket '{resource_id}'."}

    def execute_action(self, resource_id, resource_type, action, credentials, parameters) -> Dict[str, Any]:
        return {"result": "stub", "detail": f"[S3 STUB] action='{action}' on '{resource_id}'."}

    def discover_arrays(self, credentials, parameters) -> List[Dict[str, Any]]:
        return [{"note": "[S3 STUB] bucket list. Integrate s3.list_buckets()."}]

    def health_check(self, resource_id, resource_type, credentials, parameters) -> Dict[str, Any]:
        return {"healthy": True, "detail": f"[S3 STUB] head-bucket for '{resource_id}'."}
