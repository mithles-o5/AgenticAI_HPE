"""Azure cloud adapter stub — generic REST interface, no SDK dependency."""

from __future__ import annotations
from typing import Any, Dict, List, Optional

from adapters.base import BaseCloudAdapter


class AzureCloudAdapter(BaseCloudAdapter):
    """Azure Monitor + ARM REST adapter (stub — swap with azure-mgmt-* in prod)."""

    @property
    def provider_name(self) -> str:
        return "azure"

    def fetch_metrics(self, resource_id, resource_type, region, credentials, parameters) -> Dict[str, Any]:
        return {"source": "azure", "resource_id": resource_id, "note": "Stub — integrate Azure Monitor SDK for live data."}

    def execute_action(self, resource_id, resource_type, region, action, credentials, parameters) -> Dict[str, Any]:
        return {"result": "stub", "detail": f"[AZURE STUB] action='{action}' on {resource_id}."}

    def discover_resources(self, region, resource_type, credentials, parameters) -> List[Dict[str, Any]]:
        return [{"note": f"[AZURE STUB] discovery for {resource_type} in {region}."}]

    def health_check(self, resource_id, resource_type, region, credentials, parameters) -> Dict[str, Any]:
        return {"healthy": True, "detail": f"[AZURE STUB] health-check for {resource_id}."}
