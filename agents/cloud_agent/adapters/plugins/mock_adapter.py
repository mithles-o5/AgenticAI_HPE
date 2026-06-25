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
        except Exception as e:
            return {"result": "failed", "detail": f"Dynamic mock API call failed: {e}"}

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
        elif isinstance(res, dict) and "items" in res:
            return res["items"]
        return [res]

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
