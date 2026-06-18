from adapters.base import BaseAdapter

class MockAdapter(BaseAdapter):
    # ── Dynamic Router ────────────────────────────────────────────────────────
    async def _dynamic_call(self, method: str, api_path: str, resource_id: str, payload: dict, base_url: str = "") -> dict | list | None:
        import httpx
        from urllib.parse import urlparse
        try:
            parsed = urlparse(api_path)
            if "compute-ops-mgmt" in parsed.path:
                api_path = f"http://127.0.0.1:8001{parsed.path}"
            else:
                api_path = f"http://127.0.0.1:8000{parsed.path}"
            if parsed.query:
                api_path += f"?{parsed.query}"

            url = f"{base_url}{api_path}".format(id=resource_id, systemId=resource_id, hostId=resource_id)
            async with httpx.AsyncClient() as client:
                response = await client.request(method, url, json=payload, timeout=10.0)
                try:
                    return response.json()
                except:
                    return {"status": "success", "status_code": response.status_code, "text": response.text}
        except Exception as e:
            return {"result": "failed", "detail": f"Dynamic mock API call failed: {e}"}

    async def health_check(self, resource_type: str, resource_id: str, credentials: dict, parameters: dict) -> dict:
        api_path = parameters.get("api_path")
        if not api_path:
            return {"result": "failed", "detail": "Dynamic routing failed: No api_path provided by orchestrator. The agent is strictly dynamic."}
        return await self._dynamic_call(parameters.get("http_method", "GET"), api_path, resource_id, parameters.get("payload", {}), parameters.get("base_url", ""))

    async def fetch_metrics(self, resource_type: str, resource_id: str, credentials: dict, parameters: dict) -> dict:
        api_path = parameters.get("api_path")
        if not api_path:
            return {"result": "failed", "detail": "Dynamic routing failed: No api_path provided by orchestrator. The agent is strictly dynamic."}
        return await self._dynamic_call(parameters.get("http_method", "GET"), api_path, resource_id, parameters.get("payload", {}), parameters.get("base_url", ""))

    async def fetch_alerts(self, resource_type: str, resource_id: str, credentials: dict, parameters: dict) -> list:
        api_path = parameters.get("api_path")
        if not api_path:
            return [{"result": "failed", "detail": "Dynamic routing failed: No api_path provided by orchestrator. The agent is strictly dynamic."}]
        res = await self._dynamic_call(parameters.get("http_method", "GET"), api_path, resource_id, parameters.get("payload", {}), parameters.get("base_url", ""))
        return res if isinstance(res, list) else [res]

    async def execute_action(self, resource_type: str, resource_id: str, credentials: dict, parameters: dict) -> dict:
        api_path = parameters.get("api_path")
        if not api_path:
            return {"result": "failed", "detail": "Dynamic routing failed: No api_path provided by orchestrator. The agent is strictly dynamic."}
        return await self._dynamic_call(parameters.get("http_method", "POST"), api_path, resource_id, parameters.get("payload", {}), parameters.get("base_url", ""))

    async def discover_inventory(self, resource_type: str, credentials: dict, parameters: dict) -> list:
        api_path = parameters.get("api_path")
        if not api_path:
            return [{"result": "failed", "detail": "Dynamic routing failed: No api_path provided by orchestrator. The agent is strictly dynamic."}]
            
        res = await self._dynamic_call(parameters.get("http_method", "GET"), api_path, "", parameters.get("payload", {}), parameters.get("base_url", ""))
        if isinstance(res, list):
            return res
        elif isinstance(res, dict) and "members" in res:
            return res["members"]
        elif isinstance(res, dict) and "items" in res:
            return res["items"]
        return [res]

    async def sync_cmdb(self, credentials: dict, parameters: dict) -> dict:
        return {
            "provider": "mock",
            "timestamp": "2026-06-09T23:03:15Z",
            "servers": await self.discover_inventory(None, credentials, parameters)
        }
