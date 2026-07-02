"""Mock storage adapter — deterministic, no external dependencies."""

from __future__ import annotations
import random
from typing import Any, Dict, List, Optional

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
            api_path = f"http://127.0.0.1:8005{parsed.path}"
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

    def list_resources(self, credentials, parameters, skip: int = 0, limit: int = 100) -> Dict[str, Any]:
        """List storage resources using api_path and provider_label from parameters."""
        parameters = parameters or {}
        resource_type = parameters.get("resource_type", "storage_system")
        api_path = parameters.get("api_path")
        if not api_path:
            api_path = f"/data-services/v1beta1/devices?device_type={resource_type}"
        provider_label = parameters.get("provider_label", "mock_server(storage)")

        import httpx
        base_url = "http://127.0.0.1:8005"
        url = f"{base_url}{api_path}"
        try:
            resp = httpx.get(url, timeout=5)
            if resp.status_code != 200:
                return {"total": 0, "devices": [],
                        "error": f"{provider_label} HTTP {resp.status_code}"}
            res = resp.json()
        except Exception as e:
            return {"total": 0, "devices": [], "error": str(e)}

        if isinstance(res, list):
            devices = res
        elif isinstance(res, dict):
            devices = (
                res.get("devices")
                or res.get("items")
                or res.get("members")
                or res.get("resources")
                or []
            )
        else:
            devices = []

        # Tag provider label
        for d in devices:
            if isinstance(d, dict) and not d.get("management_source"):
                d["management_source"] = provider_label

        paginated = devices[skip: skip + limit] if limit else devices
        return {"total": len(devices), "devices": paginated}
