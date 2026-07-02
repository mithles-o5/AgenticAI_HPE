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
            api_path = "/rest/server-hardware"
            
        res = await self._dynamic_call(parameters.get("http_method", "GET"), api_path, "", parameters.get("payload", {}), parameters.get("base_url", ""))
        if isinstance(res, list):
            return res
        elif isinstance(res, dict) and "members" in res:
            return res["members"]
        elif isinstance(res, dict) and "items" in res:
            return res["items"]
        return [res]

    async def list_resources(
        self,
        resource_type: str,
        credentials: dict,
        parameters: dict,
        skip: int = 0,
        limit: int = 100,
    ) -> dict:
        """
        List resources from OneView or ComOps mock server.
        Routing is driven by the api_path parameter passed from mcp_server.
          - /rest/*               -> OneView mock (port 8002)
          - /compute-ops-mgmt/*  -> ComOps mock  (port 8001)
        """
        api_path = parameters.get("api_path", "")
        provider_label = parameters.get("provider_label", "mock_server(onprem)")

        if not api_path:
            if "ComOps" in provider_label:
                api_path = f"/compute-ops-mgmt/v1/devices?device_type={resource_type}"
            else:
                if resource_type == "server":
                    api_path = "/rest/custom-servers"
                elif resource_type == "switch":
                    api_path = "/rest/custom-switches"
                else:
                    api_path = "/rest/server-hardware"

        # Choose base URL based on path prefix
        if "compute-ops-mgmt" in api_path:
            base = "http://127.0.0.1:8001"
        else:
            base = "http://127.0.0.1:8002"

        import httpx
        url = f"{base}{api_path}"
        try:
            async with httpx.AsyncClient(timeout=6.0) as client:
                resp = await client.get(url)
                if resp.status_code != 200:
                    return {"devices": [], "total": 0,
                            "error": f"{provider_label} HTTP {resp.status_code}"}
                data = resp.json()
        except httpx.ConnectError:
            return {"devices": [], "total": 0,
                    "error": f"{provider_label} is offline (connection refused)"}
        except Exception as exc:
            return {"devices": [], "total": 0, "error": str(exc)}

        # Normalise to list
        if isinstance(data, list):
            items = data
        elif isinstance(data, dict):
            items = (
                data.get("members")
                or data.get("items")
                or data.get("devices")
                or data.get("Members")
                or data.get("resources")
                or []
            )
        else:
            items = []

        # Tag each device with provider label
        for item in items:
            if isinstance(item, dict) and not item.get("management_source"):
                item["management_source"] = provider_label

        paginated = items[skip: skip + limit] if limit else items
        return {"devices": paginated, "total": len(items)}

    async def sync_cmdb(self, credentials: dict, parameters: dict) -> dict:
        return {
            "provider": "mock",
            "timestamp": "2026-06-09T23:03:15Z",
            "servers": await self.discover_inventory(None, credentials, parameters)
        }
