"""Mock storage adapter — deterministic, no external dependencies."""

from __future__ import annotations
import random
from typing import Any, Dict, List

from adapters.base import BaseStorageAdapter


class MockStorageAdapter(BaseStorageAdapter):

    @property
    def provider_name(self) -> str:
        return "mock"

    # ── Dynamic Router ────────────────────────────────────────────────────────
    def _dynamic_call(self, method: str, api_path: str, resource_id: str, payload: dict, base_url: str = "") -> Optional[Dict[str, Any]]:
        import httpx
        from urllib.parse import urlparse
        try:
            parsed = urlparse(api_path)
            api_path = f"http://127.0.0.1:8004{parsed.path}"
            if parsed.query:
                api_path += f"?{parsed.query}"

            url = f"{base_url}{api_path}".format(id=resource_id, systemId=resource_id, hostId=resource_id)
            response = httpx.request(method, url, json=payload, timeout=10.0)
            response.raise_for_status()
            try:
                return response.json()
            except:
                return {"status": "success", "status_code": response.status_code, "text": response.text}
        except httpx.HTTPStatusError as e:
            try:
                err_data = e.response.json()
            except:
                err_data = e.response.text
            raise Exception(f"HTTP Error {e.response.status_code}: {err_data}")
        except Exception as e:
            raise Exception(f"Dynamic mock API call failed: {e}")

    def fetch_capacity(self, resource_id, resource_type, credentials, parameters) -> Dict[str, Any]:
        api_path = parameters.get("api_path")
        if not api_path:
            return {"result": "failed", "detail": "Dynamic routing failed: No api_path provided by orchestrator. The agent is strictly dynamic."}
        return self._dynamic_call(parameters.get("http_method", "GET"), api_path, resource_id, parameters.get("payload", {}), parameters.get("base_url", ""))

    def fetch_performance(self, resource_id, resource_type, credentials, parameters) -> Dict[str, Any]:
        api_path = parameters.get("api_path")
        if not api_path:
            return {"result": "failed", "detail": "Dynamic routing failed: No api_path provided by orchestrator. The agent is strictly dynamic."}
        return self._dynamic_call(parameters.get("http_method", "GET"), api_path, resource_id, parameters.get("payload", {}), parameters.get("base_url", ""))

    def execute_action(self, resource_id, resource_type, action, credentials, parameters) -> Dict[str, Any]:
        api_path = parameters.get("api_path")
        if not api_path:
            return {"result": "failed", "detail": "Dynamic routing failed: No api_path provided by orchestrator. The agent is strictly dynamic."}
        return self._dynamic_call(parameters.get("http_method", "POST"), api_path, resource_id, parameters.get("payload", {}), parameters.get("base_url", ""))

    def discover_arrays(self, credentials, parameters) -> List[Dict[str, Any]]:
        api_path = parameters.get("api_path")
        if not api_path:
            return [{"result": "failed", "detail": "Dynamic routing failed: No api_path provided by orchestrator. The agent is strictly dynamic."}]
            
        res = self._dynamic_call(parameters.get("http_method", "GET"), api_path, "", parameters.get("payload", {}), parameters.get("base_url", ""))
        if isinstance(res, list):
            return res
        elif isinstance(res, dict) and "members" in res:
            return res["members"]
        elif isinstance(res, dict) and "items" in res:
            return res["items"]
        return [res]

    def health_check(self, resource_id, resource_type, credentials, parameters) -> Dict[str, Any]:
        api_path = parameters.get("api_path")
        if not api_path:
            return {"result": "failed", "detail": "Dynamic routing failed: No api_path provided by orchestrator. The agent is strictly dynamic."}
        return self._dynamic_call(parameters.get("http_method", "GET"), api_path, resource_id, parameters.get("payload", {}), parameters.get("base_url", ""))
