"""Mock cloud adapter — zero external dependencies, for local dev and testing."""

from __future__ import annotations
import random
import time
from typing import Any, Dict, List, Optional

from adapters.base import BaseCloudAdapter


class MockCloudAdapter(BaseCloudAdapter):
    """Simulates a cloud provider backend with deterministic-ish mock data."""

    @property
    def provider_name(self) -> str:
        return "mock"

    # ── Dynamic Router ────────────────────────────────────────────────────────
    def _dynamic_call(self, method: str, api_path: str, resource_id: str, payload: dict, base_url: str = "") -> Optional[Dict[str, Any]]:
        import httpx
        from urllib.parse import urlparse
        import re
        import re
        try:
            parsed = urlparse(api_path)
            api_path = f"http://127.0.0.1:8003{parsed.path}"
            if parsed.query:
                api_path += f"?{parsed.query}"

            url = f"{base_url}{api_path}".format(id=resource_id, systemId=resource_id, hostId=resource_id)
            response = httpx.request(method, url, json=payload, timeout=10.0)
            response.raise_for_status()
            try:
                data = response.json()
                if response.status_code == 404 and ("interfaces" in api_path or "metrics" in api_path):
                    # Fallback: try fetching the base device data
                    base_api_path = re.sub(r'/(interfaces|metrics).*', '', api_path)
                    base_url_full = f"{base_url}{base_api_path}".format(id=resource_id, systemId=resource_id, hostId=resource_id)
                    fallback_resp = httpx.request("GET", base_url_full, timeout=10.0)
                    if fallback_resp.status_code == 200:
                        device_data = fallback_resp.json()
                        if "interfaces" in api_path:
                            ports = device_data.get("ports", {})
                            result = []
                            for p_name, p_status in ports.items():
                                result.append({"interface": p_name, "status": p_status})
                            return result if result else data
                        elif "metrics" in api_path:
                            # Try to build a metrics dict from the device data
                            metrics = {}
                            for k in ["temperature_celsius", "storage_capacity_gb", "cpu_cores", "active_vms", "allocated_vcpu", "allocated_ram_gb", "power_state", "status", "health"]:
                                if k in device_data:
                                    metrics[k] = device_data[k]
                            return metrics if metrics else data
                return data
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

    # ── fetch_metrics ─────────────────────────────────────────────────────────
    def fetch_metrics(
        self,
        resource_id: str,
        resource_type: str,
        region: Optional[str],
        credentials: Dict[str, Any],
        parameters: Dict[str, Any],
    ) -> Dict[str, Any]:
        api_path = parameters.get("api_path")
        if not api_path:
            return {"result": "failed", "detail": "Dynamic routing failed: No api_path provided by orchestrator. The agent is strictly dynamic."}
        return self._dynamic_call(parameters.get("http_method", "GET"), api_path, resource_id, parameters.get("payload", {}), parameters.get("base_url", ""))

    # ── execute_action ────────────────────────────────────────────────────────
    def execute_action(
        self,
        resource_id: str,
        resource_type: str,
        region: Optional[str],
        action: str,
        credentials: Dict[str, Any],
        parameters: Dict[str, Any],
    ) -> Dict[str, Any]:
        api_path = parameters.get("api_path")
        if not api_path:
            return {"result": "failed", "detail": "Dynamic routing failed: No api_path provided by orchestrator. The agent is strictly dynamic."}
            
        payload = parameters.get("payload") or {}
        if not payload:
            payload = {
                "action": action,
                "state": parameters.get("state"),
                "action_verb": parameters.get("action_verb"),
                "action_type": parameters.get("action_type")
            }
        return self._dynamic_call(parameters.get("http_method", "POST"), api_path, resource_id, payload, parameters.get("base_url", ""))

    # ── discover_resources ────────────────────────────────────────────────────
    def discover_resources(
        self,
        region: Optional[str],
        resource_type: str,
        credentials: Dict[str, Any],
        parameters: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        api_path = parameters.get("api_path")
        if not api_path:
            return [{"result": "failed", "detail": "Dynamic routing failed: No api_path provided by orchestrator. The agent is strictly dynamic."}]
            
        res = self._dynamic_call(parameters.get("http_method", "GET"), api_path, "", parameters.get("payload", {}), parameters.get("base_url", ""))
        if isinstance(res, list):
            return res
        elif isinstance(res, dict):
            for key in ["items", "members", "devices", "instances", "resources"]:
                if key in res and isinstance(res[key], list):
                    return res[key]
        return [res] if isinstance(res, dict) else []

    # ── health_check ──────────────────────────────────────────────────────────
    def health_check(
        self,
        resource_id: str,
        resource_type: str,
        region: Optional[str],
        credentials: Dict[str, Any],
        parameters: Dict[str, Any],
    ) -> Dict[str, Any]:
        api_path = parameters.get("api_path")
        if not api_path:
            return {"result": "failed", "detail": "Dynamic routing failed: No api_path provided by orchestrator. The agent is strictly dynamic."}
        return self._dynamic_call(parameters.get("http_method", "GET"), api_path, resource_id, parameters.get("payload", {}), parameters.get("base_url", ""))

    def list_resources(
        self,
        region: Optional[str],
        credentials: Dict[str, Any],
        parameters: Dict[str, Any],
        skip: int = 0,
        limit: int = 10,
    ) -> Dict[str, Any]:
        """
        List cloud resources using the api_path and provider_label passed from mcp_server.
        Calls the cloud mock server at port 8003.
        """
        parameters = parameters or {}
        resource_type = parameters.get("resource_type", "virtual_machine")
        api_path = parameters.get("api_path", "")
        if not api_path:
            api_path = f"/api/v1/devices?device_type={resource_type}"
        provider_label = parameters.get("provider_label", "mock_server(cloud)")
        base_url = "http://127.0.0.1:8003"
        url = f"{base_url}{api_path}"

        import requests
        try:
            resp = requests.get(url, timeout=5)
            if resp.status_code != 200:
                return {"total": 0, "devices": [],
                        "error": f"{provider_label} HTTP {resp.status_code}"}
            data = resp.json()
        except Exception as e:
            return {"total": 0, "devices": [], "error": str(e)}

        # Normalise to list
        if isinstance(data, list):
            devices = data
        elif isinstance(data, dict):
            devices = (
                data.get("items")
                or data.get("devices")
                or data.get("members")
                or data.get("Members")
                or data.get("resources")
                or []
            )
        else:
            devices = []

        # Tag provider
        for item in devices:
            if isinstance(item, dict) and not item.get("management_source"):
                item["management_source"] = provider_label

        paginated = devices[skip: skip + limit] if limit else devices
        return {"total": len(devices), "devices": paginated}

        resource_type = parameters.get("resource_type")
        devices = []
        
        if api_path:
            res = self._dynamic_call(parameters.get("http_method", "GET"), api_path, "", parameters.get("payload", {}), parameters.get("base_url", ""))
            if isinstance(res, list):
                devices = res
            elif isinstance(res, dict):
                for key in ["items", "members", "instances", "devices", "resources"]:
                    if key in res and isinstance(res[key], list):
                        devices = res[key]
                        break
        else:
            # If no specific api_path, fetch from both ComOps and Cloud Mock
            import httpx
            import asyncio
            
            async def fetch(url):
                try:
                    async with httpx.AsyncClient() as client:
                        resp = await client.get(url, timeout=5.0)
                        if resp.status_code == 200:
                            return resp.json()
                except Exception:
                    pass
                return None
    
            comops_url = f"http://127.0.0.1:8001/compute-ops-mgmt/v1/servers"
            cloud_url = f"http://127.0.0.1:8003/api/v1/devices"
            
            loop = asyncio.get_event_loop()
            if loop.is_running():
                import nest_asyncio
                nest_asyncio.apply()
                
            results = loop.run_until_complete(asyncio.gather(fetch(comops_url), fetch(cloud_url)))
            for res in results:
                if not res:
                    continue
                if isinstance(res, list):
                    devices.extend(res)
                elif isinstance(res, dict):
                    for key in ["items", "members", "instances", "devices", "resources"]:
                        if key in res and isinstance(res[key], list):
                            devices.extend(res[key])
                            break

        # Filter
        filtered_devices = []
        for d in devices:
            dtype = str(d.get("device_type", "")).lower()
            if resource_type == "server":
                if dtype not in ["virtual_machine", "kubernetes_cluster", "bare_metal", "kubernetes_node", "compute"]:
                    continue
            elif resource_type == "network":
                if dtype not in ["virtual_network", "subnet", "switch", "router", "load_balancer", "access_point"]:
                    continue
            elif resource_type == "storage":
                if dtype not in ["storage_system", "volume", "namespace", "database_service"]:
                    continue
            filtered_devices.append(d)
                
        paginated_devices = filtered_devices[skip : skip + limit] if limit else filtered_devices
        return {"total": len(filtered_devices), "devices": paginated_devices}
