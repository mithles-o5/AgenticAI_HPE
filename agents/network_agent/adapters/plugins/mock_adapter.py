"""Mock network adapter — no hardware required, deterministic for testing."""

from __future__ import annotations
import random
from typing import Any, Dict, List, Optional

from adapters.base import BaseNetworkAdapter


class MockNetworkAdapter(BaseNetworkAdapter):

    @property
    def protocol_name(self) -> str:
        return "mock"

    # ── Dynamic Router ────────────────────────────────────────────────────────
    def _dynamic_call(self, method: str, api_path: str, device_id: str, payload: dict, base_url: str = "") -> Optional[Dict[str, Any]]:
        import httpx
        try:
            url = f"{base_url}{api_path}".format(id=device_id, systemId=device_id, hostId=device_id)
            response = httpx.request(method, url, json=payload, timeout=10.0)
            try:
                return response.json()
            except:
                return {"status": "success", "status_code": response.status_code, "text": response.text}
        except Exception as e:
            return {"result": "failed", "detail": f"Dynamic mock API call failed: {e}"}

    def fetch_interface_metrics(self, device_id, credentials, parameters) -> List[Dict[str, Any]]:
        api_path = parameters.get("api_path")
        if not api_path:
            return [{"result": "failed", "detail": "Dynamic routing failed: No api_path provided by orchestrator. The agent is strictly dynamic."}]
        res = self._dynamic_call(parameters.get("http_method", "GET"), api_path, device_id, parameters.get("payload", {}), parameters.get("base_url", ""))
        return res if isinstance(res, list) else [res]

    def push_config(self, device_id, config_payload, credentials, parameters) -> Dict[str, Any]:
        api_path = parameters.get("api_path")
        if not api_path:
            return {"result": "failed", "detail": "Dynamic routing failed: No api_path provided by orchestrator. The agent is strictly dynamic."}
        return self._dynamic_call(parameters.get("http_method", "POST"), api_path, device_id, parameters.get("payload", {}), parameters.get("base_url", ""))

    def discover_neighbors(self, device_id, credentials, parameters) -> List[Dict[str, Any]]:
        api_path = parameters.get("api_path")
        if not api_path:
            return [{"result": "failed", "detail": "Dynamic routing failed: No api_path provided by orchestrator. The agent is strictly dynamic."}]
        res = self._dynamic_call(parameters.get("http_method", "GET"), api_path, device_id, parameters.get("payload", {}), parameters.get("base_url", ""))
        if isinstance(res, list):
            return res
        elif isinstance(res, dict) and "members" in res:
            return res["members"]
        elif isinstance(res, dict) and "items" in res:
            return res["items"]
        return [res]

    def health_check(self, device_id, credentials, parameters) -> Dict[str, Any]:
        api_path = parameters.get("api_path")
        if not api_path:
            return {"result": "failed", "detail": "Dynamic routing failed: No api_path provided by orchestrator. The agent is strictly dynamic."}
        return self._dynamic_call(parameters.get("http_method", "GET"), api_path, device_id, parameters.get("payload", {}), parameters.get("base_url", ""))
