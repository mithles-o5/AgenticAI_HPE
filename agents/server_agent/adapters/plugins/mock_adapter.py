from typing import Dict, List, Any, Optional
from adapters.base import ServerAdapter

class MockAdapter(ServerAdapter):
    # ── Dynamic Router ────────────────────────────────────────────────────────
    def _dynamic_call(self, method: str, api_path: str, resource_id: str, payload: dict, base_url: str = "") -> Optional[Dict[str, Any]]:
        import httpx
        from urllib.parse import urlparse
        try:
            parsed = urlparse(api_path)
            api_path = f"http://127.0.0.1:8002{parsed.path}"
            if parsed.query:
                api_path += f"?{parsed.query}"

            url = f"{base_url}{api_path}".format(id=resource_id, systemId=resource_id, hostId=resource_id)
            response = httpx.request(method, url, json=payload, timeout=10.0)
            try:
                return response.json()
            except:
                return {"status": "success", "status_code": response.status_code, "text": response.text}
        except Exception as e:
            return {"result": "failed", "detail": f"Dynamic mock API call failed: {e}"}

    def fetch_system_metrics(self, resource_id: str, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        parameters = parameters or {}
        api_path = parameters.get("api_path")
        if not api_path:
            return {"result": "failed", "detail": "Dynamic routing failed: No api_path provided by orchestrator. The agent is strictly dynamic."}
        return self._dynamic_call(parameters.get("http_method", "GET"), api_path, resource_id, parameters.get("payload", {}), parameters.get("base_url", ""))

    def fetch_sensors(self, resource_id: str, parameters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        parameters = parameters or {}
        api_path = parameters.get("api_path")
        if not api_path:
            return [{"result": "failed", "detail": "Dynamic routing failed: No api_path provided by orchestrator. The agent is strictly dynamic."}]
        res = self._dynamic_call(parameters.get("http_method", "GET"), api_path, resource_id, parameters.get("payload", {}), parameters.get("base_url", ""))
        return res if isinstance(res, list) else [res]

    def fetch_event_log(self, resource_id: str, severity_filter: Optional[str] = None, parameters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        parameters = parameters or {}
        api_path = parameters.get("api_path")
        if not api_path:
            return [{"result": "failed", "detail": "Dynamic routing failed: No api_path provided by orchestrator. The agent is strictly dynamic."}]
        res = self._dynamic_call(parameters.get("http_method", "GET"), api_path, resource_id, parameters.get("payload", {}), parameters.get("base_url", ""))
        return res if isinstance(res, list) else [res]

    def clear_event_log(self, resource_id: str, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        parameters = parameters or {}
        api_path = parameters.get("api_path")
        if not api_path:
            return {"result": "failed", "detail": "Dynamic routing failed: No api_path provided by orchestrator. The agent is strictly dynamic."}
        return self._dynamic_call(parameters.get("http_method", "POST"), api_path, resource_id, parameters.get("payload", {}), parameters.get("base_url", ""))

    def execute_power_action(self, resource_id: str, action: str, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        parameters = parameters or {}
        api_path = parameters.get("api_path")
        if not api_path:
            return {"result": "failed", "detail": "Dynamic routing failed: No api_path provided by orchestrator. The agent is strictly dynamic."}
        return self._dynamic_call(parameters.get("http_method", "POST"), api_path, resource_id, parameters.get("payload", {}), parameters.get("base_url", ""))

    def set_boot_order(self, resource_id: str, boot_order: List[str], parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        parameters = parameters or {}
        api_path = parameters.get("api_path")
        if not api_path:
            return {"result": "failed", "detail": "Dynamic routing failed: No api_path provided by orchestrator. The agent is strictly dynamic."}
        return self._dynamic_call(parameters.get("http_method", "POST"), api_path, resource_id, parameters.get("payload", {}), parameters.get("base_url", ""))

    def mount_virtual_media(self, resource_id: str, media_url: str, device_type: str, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        parameters = parameters or {}
        api_path = parameters.get("api_path")
        if not api_path:
            return {"result": "failed", "detail": "Dynamic routing failed: No api_path provided by orchestrator. The agent is strictly dynamic."}
        return self._dynamic_call(parameters.get("http_method", "POST"), api_path, resource_id, parameters.get("payload", {}), parameters.get("base_url", ""))

    def discover_inventory(self, filters: Dict[str, Any], parameters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        parameters = parameters or {}
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

    def health_check(self, resource_id: str, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        parameters = parameters or {}
        api_path = parameters.get("api_path")
        if not api_path:
            return {"result": "failed", "detail": "Dynamic routing failed: No api_path provided by orchestrator. The agent is strictly dynamic."}
        return self._dynamic_call(parameters.get("http_method", "GET"), api_path, resource_id, parameters.get("payload", {}), parameters.get("base_url", ""))

