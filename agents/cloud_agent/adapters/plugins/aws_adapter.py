"""AWS cloud adapter — stub using generic REST calls (no boto3 dependency).

In production, swap the _call() method body with real boto3/botocore calls.
The adapter interface remains identical — the core never changes.
"""

from __future__ import annotations
import httpx
from typing import Any, Dict, List, Optional

from adapters.base import BaseCloudAdapter


class AWSCloudAdapter(BaseCloudAdapter):
    """AWS adapter using CloudWatch REST API (generic HTTP, no SDK required)."""

    @property
    def provider_name(self) -> str:
        return "aws"

    def _headers(self, credentials: Dict[str, Any]) -> Dict[str, str]:
        """Build auth headers from injected credentials."""
        return {
            "X-Aws-Access-Key":    credentials.get("access_key_id", ""),
            "X-Aws-Secret-Key":    credentials.get("secret_access_key", ""),
            "X-Aws-Session-Token": credentials.get("session_token", ""),
            "Content-Type":        "application/json",
        }

    def fetch_metrics(
        self,
        resource_id: str,
        resource_type: str,
        region: Optional[str],
        credentials: Dict[str, Any],
        parameters: Dict[str, Any],
    ) -> Dict[str, Any]:
        # Placeholder — replace with boto3 CloudWatch.get_metric_data() in production
        return {
            "source":       "aws",
            "resource_id":  resource_id,
            "region":       region,
            "note":         "Stub — integrate boto3 CloudWatch for live data.",
        }

    def execute_action(
        self,
        resource_id: str,
        resource_type: str,
        region: Optional[str],
        action: str,
        credentials: Dict[str, Any],
        parameters: Dict[str, Any],
    ) -> Dict[str, Any]:
        # Placeholder — replace with boto3 EC2/ECS control-plane calls
        return {
            "result":      "stub",
            "detail":      f"[AWS STUB] action='{action}' on {resource_id} in {region}.",
        }

    def discover_resources(
        self,
        region: Optional[str],
        resource_type: str,
        credentials: Dict[str, Any],
        parameters: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        return [{"note": f"[AWS STUB] discovery for {resource_type} in {region}."}]

    def health_check(
        self,
        resource_id: str,
        resource_type: str,
        region: Optional[str],
        credentials: Dict[str, Any],
        parameters: Dict[str, Any],
    ) -> Dict[str, Any]:
        return {"healthy": True, "detail": f"[AWS STUB] health-check for {resource_id}."}

    def list_resources(self, region: Optional[str], credentials: Dict[str, Any], parameters: Dict[str, Any], skip: int = 0, limit: int = 10) -> Dict[str, Any]:
        return {"total": 0, "devices": [{"note": f"[AWS STUB] list resources"}]}
