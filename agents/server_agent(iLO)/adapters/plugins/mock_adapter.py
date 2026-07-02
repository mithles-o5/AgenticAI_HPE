from typing import Dict, List, Any, Optional
from adapters.base import ServerAdapter

class MockAdapter(ServerAdapter):
    # ── Dynamic Router ────────────────────────────────────────────────────────
    def _dynamic_call(self, method: str, api_path: str, resource_id: str, payload: dict, base_url: str = "") -> Optional[Dict[str, Any]]:
        import httpx
        from urllib.parse import urlparse
        try:
            parsed = urlparse(api_path)
            api_path = f"http://127.0.0.1:8010{parsed.path}"
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

    def fetch_system_metrics(self, resource_id: str, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        parameters = parameters or {}
        api_path = parameters.get("api_path")
        res = None
        if api_path:
            res = self._dynamic_call(parameters.get("http_method", "GET"), api_path, resource_id, parameters.get("payload", {}), parameters.get("base_url", ""))
        
        if not res or res.get("result") == "failed":
            # Fallback to realistic static mock data for unit tests and offline mode
            return {
                "cpu_utilization": 54.0,
                "memory_utilization": 60.0,
                "cpu_count": 2,
                "memory_total_gb": 128.0,
                "power_consumed_watts": 320.0,
                "power_capacity_watts": 800.0,
                "inlet_temperature_celsius": 22.0,
                "cpu_temperature_celsius": 52.0,
                "overall_health": "OK",
                "power_supply_status": "OK",
                "fan_status": "OK",
                "storage_status": "OK",
                "network_status": "OK",
                "power_state": "On"
            }
        return res

    def fetch_sensors(self, resource_id: str, parameters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        parameters = parameters or {}
        api_path = parameters.get("api_path")
        res = None
        if api_path:
            res = self._dynamic_call(parameters.get("http_method", "GET"), api_path, resource_id, parameters.get("payload", {}), parameters.get("base_url", ""))
            
        if not res or isinstance(res, dict) and res.get("result") == "failed":
            return [
                {"name": "Inlet Temp", "reading": 22.0, "units": "C", "status": "OK"},
                {"name": "Fan 1", "reading": 45.0, "units": "Percent", "status": "OK"}
            ]
        return res if isinstance(res, list) else [res]

    def fetch_event_log(self, resource_id: str, severity_filter: Optional[str] = None, parameters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        parameters = parameters or {}
        api_path = parameters.get("api_path")
        res = None
        if api_path:
            res = self._dynamic_call(parameters.get("http_method", "GET"), api_path, resource_id, parameters.get("payload", {}), parameters.get("base_url", ""))
            
        if not res or isinstance(res, dict) and res.get("result") == "failed":
            return [
                {"id": "1", "message": "System booted", "severity": "OK", "created_at": "2026-06-25T10:00:00Z"}
            ]
        return res if isinstance(res, list) else [res]

    def clear_event_log(self, resource_id: str, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        parameters = parameters or {}
        api_path = parameters.get("api_path")
        res = None
        if api_path:
            res = self._dynamic_call(parameters.get("http_method", "POST"), api_path, resource_id, parameters.get("payload", {}), parameters.get("base_url", ""))
            
        if not res or res.get("result") == "failed":
            return {"status": "success", "detail": "Event log cleared"}
        return res

    def execute_power_action(self, resource_id: str, action: str, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        parameters = parameters or {}
        api_path = parameters.get("api_path")
        res = None
        payload = parameters.get("payload") or {}
        if not payload:
            payload = {"ResetType": "On" if action.lower() in ("on", "poweron") else "ForceOff", "powerState": action.upper()}
            
        if api_path:
            method = parameters.get("http_method", "POST")
            if method == "GET":
                method = "POST"
            res = self._dynamic_call(method, api_path, resource_id, payload, parameters.get("base_url", ""))
            
        if not res or res.get("result") == "failed":
            return {
                "status": "success",
                "actions_taken": [f"power_{action.lower()}"]
            }
        return res

    def set_boot_order(self, resource_id: str, boot_order: List[str], parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        parameters = parameters or {}
        api_path = parameters.get("api_path")
        res = None
        if api_path:
            res = self._dynamic_call(parameters.get("http_method", "POST"), api_path, resource_id, parameters.get("payload", {}), parameters.get("base_url", ""))
            
        if not res or res.get("result") == "failed":
            return {"status": "success", "detail": "Boot order updated"}
        return res

    def mount_virtual_media(self, resource_id: str, media_url: str, device_type: str, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        parameters = parameters or {}
        api_path = parameters.get("api_path")
        res = None
        if api_path:
            res = self._dynamic_call(parameters.get("http_method", "POST"), api_path, resource_id, parameters.get("payload", {}), parameters.get("base_url", ""))
            
        if not res or res.get("result") == "failed":
            return {"status": "success", "detail": "Virtual media mounted"}
        return res

    def list_resources(self, filters: Dict[str, Any], skip: int = 0, limit: int = 10, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Fetch a paginated list of resources from the iLO mock server using the api_path from parameters."""
        parameters = parameters or {}
        api_path = parameters.get("api_path", "/redfish/v1/systems")
        provider_label = parameters.get("provider_label", "mock_server(iLO)")
        base_url = "http://127.0.0.1:8010"
        url = f"{base_url}{api_path}"

        import requests
        try:
            resp = requests.get(url, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                # Normalise to list
                if isinstance(data, list):
                    members = data
                elif isinstance(data, dict):
                    members = (
                        data.get("Members")
                        or data.get("items")
                        or data.get("devices")
                        or data.get("members")
                        or []
                    )
                else:
                    members = []
                # Tag each device
                for item in members:
                    if isinstance(item, dict) and not item.get("management_source"):
                        item["management_source"] = provider_label
                total = data.get("Members@odata.count", len(members)) if isinstance(data, dict) else len(members)
                return {"total": total, "devices": members}
        except Exception as e:
            import structlog
            logger = structlog.stdlib.get_logger()
            logger.error("Failed to list resources from mock API", error=str(e))
        return {"total": 0, "devices": []}


    def discover_inventory(self, filters: Dict[str, Any], parameters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        parameters = parameters or {}
        api_path = parameters.get("api_path")
        res = None
        if api_path:
            res = self._dynamic_call(parameters.get("http_method", "GET"), api_path, "", parameters.get("payload", {}), parameters.get("base_url", ""))
            
        if not res or (isinstance(res, dict) and res.get("result") == "failed") or (isinstance(res, list) and len(res) > 0 and "result" in res[0] and res[0]["result"] == "failed"):
            return [
                {
                    "cpus": [{"model": "Intel Xeon", "cores": 8}],
                    "memory": [{"size_gb": 64}],
                    "storage": [],
                    "nics": [],
                    "firmware": []
                }
            ]
            
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
        res = None
        if api_path:
            res = self._dynamic_call(parameters.get("http_method", "GET"), api_path, resource_id, parameters.get("payload", {}), parameters.get("base_url", ""))
            
        if not res or res.get("result") == "failed":
            return {
                "overall_health": "OK",
                "status": {"Health": "OK", "State": "Enabled"}
            }
        return res

