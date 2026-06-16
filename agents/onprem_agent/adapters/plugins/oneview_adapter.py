import httpx
import logging
from config.settings import settings
from adapters.base import BaseAdapter

logger = logging.getLogger("onprem_agent.adapters.oneview")

class OneViewAdapter(BaseAdapter):
    def __init__(self, base_url: str = None):
        self.base_url = base_url or settings.ONEVIEW_URL

    async def _get_client(self, credentials: dict) -> httpx.AsyncClient:
        # Simulate OneView session setup
        headers = {"X-API-Version": "1200", "Content-Type": "application/json"}
        client = httpx.AsyncClient(base_url=self.base_url, headers=headers, timeout=10.0)
        
        if credentials and "username" in credentials and "password" in credentials:
            try:
                # Mock endpoint login-sessions
                payload = {
                    "userName": credentials["username"],
                    "password": credentials["password"]
                }
                resp = await client.post("/rest/login-sessions", json=payload)
                if resp.status_code == 200:
                    token_data = resp.json()
                    session_id = token_data.get("sessionID")
                    if session_id:
                        client.headers["auth"] = session_id
            except Exception as e:
                logger.warning(f"Failed to authenticate with OneView mock session: {e}")
        
        return client

    async def health_check(self, resource_type: str, resource_id: str, credentials: dict, parameters: dict) -> dict:
        async with await self._get_client(credentials) as client:
            if resource_type in ("server_profile", "server_hardware", "server-hardware") or (not resource_type and resource_id.startswith("OV")):
                resp = await client.get(f"/rest/server-hardware/{resource_id}")
                if resp.status_code == 200:
                    return {"resource_type": resource_type or "server_hardware", "raw": resp.json()}
                else:
                    return {
                        "resource_type": resource_type,
                        "raw": {
                            "uuid": resource_id,
                            "name": f"OV-Mock-{resource_id[-6:]}",
                            "health": "Warning",
                            "powerState": "On",
                            "status": "NotFoundFallback"
                        }
                    }
            elif resource_type == "enclosure":
                resp = await client.get(f"/rest/rack-managers/{resource_id}")
                if resp.status_code == 200:
                    return {"resource_type": "enclosure", "raw": resp.json()}
                else:
                    return {
                        "resource_type": "enclosure",
                        "raw": {
                            "uuid": resource_id,
                            "name": f"Enclosure-OV-{resource_id[-4:]}",
                            "health": "OK",
                            "state": "Normal"
                        }
                    }
            else:
                # Interconnect, logical_switch, composable_resource, etc.
                return {
                    "resource_type": resource_type,
                    "raw": {
                        "uuid": resource_id,
                        "name": f"OneView-{resource_type}-{resource_id[-6:]}",
                        "health": "OK",
                        "state": "Configured",
                        "status": "Simulated"
                    }
                }

    async def fetch_metrics(self, resource_type: str, resource_id: str, credentials: dict, parameters: dict) -> dict:
        async with await self._get_client(credentials) as client:
            power_state = "On"
            if resource_type in ("server_profile", "server_hardware", "server-hardware") or (not resource_type and resource_id.startswith("OV")):
                resp = await client.get(f"/rest/server-hardware/{resource_id}")
                if resp.status_code == 200:
                    power_state = resp.json().get("powerState", "On")

            if power_state == "Off":
                metrics = {
                    "cpu_utilization_percent": 0.0,
                    "memory_utilization_percent": 0.0,
                    "power_draw_watts": 15.0,
                    "temperature_celsius": 20.0,
                    "power_state": "Off"
                }
            else:
                metrics = {
                    "cpu_utilization_percent": 45.2,
                    "memory_utilization_percent": 60.8,
                    "power_draw_watts": 280.0,
                    "temperature_celsius": 32.5,
                    "power_state": "On"
                }
                
                # Query real endpoint thermal if resource is server
                if resource_type in ("server_profile", "server_hardware", "server-hardware") or (not resource_type and resource_id.startswith("OV")):
                    resp = await client.get(f"/rest/server-hardware/{resource_id}/thermal")
                    if resp.status_code == 200:
                        thermal_data = resp.json()
                        temp = thermal_data.get("temperatureCelsius")
                        if temp:
                            metrics["temperature_celsius"] = float(temp)
            
            # Query chassis utilization if enclosure
            if resource_type == "enclosure":
                resp = await client.get(f"/rest/rack-managers/{resource_id}/chassis/utilization")
                if resp.status_code == 200:
                    util_data = resp.json()
                    metrics["power_draw_watts"] = util_data.get("powerWatts", 350.0)
            
            return metrics

    async def fetch_alerts(self, resource_type: str, resource_id: str, credentials: dict, parameters: dict) -> list:
        # Simulate OneView Alert collection since mock server doesn't have a dedicated /rest/alerts endpoint
        # We generate a list of mock alerts, including some warnings or critical alerts if the resource is degraded
        alerts = [
            {
                "id": "alert-101",
                "severity": "Warning",
                "description": "Redundant power supply failure detected in bay 2",
                "created": "2026-06-09T12:00:00Z",
                "category": "power"
            }
        ]
        return alerts

    async def execute_action(self, resource_type: str, resource_id: str, credentials: dict, parameters: dict) -> dict:
        action_type = parameters.get("action_type")
        async with await self._get_client(credentials) as client:
            if action_type == "power":
                state = parameters.get("state", "On")
                payload = {"powerState": state}
                resp = await client.put(f"/rest/server-hardware/{resource_id}/powerState", json=payload)
                if resp.status_code == 200:
                    return {"status": "success", "action_taken": f"Power state set to {state}", "raw": resp.json()}
                else:
                    return {"status": "failed", "error": f"OneView returned code {resp.status_code}"}
            elif action_type == "firmware_update":
                version = parameters.get("firmware_version", "iLO5 2.70")
                payload = {"serverUUID": resource_id, "firmwareBaselineId": version}
                resp = await client.post("/rest/server-hardware/firmware-compliance", json=payload)
                if resp.status_code == 200 or resp.status_code == 201:
                    return {"status": "success", "action_taken": f"Triggered compliance update to baseline {version}", "raw": resp.json()}
                else:
                    return {"status": "failed", "error": f"Failed to post firmware compliance. Status code: {resp.status_code}"}
            elif action_type == "profile_assign":
                profile_id = parameters.get("profile_id", "prof-default")
                # Simulate profile assignment
                return {
                    "status": "success",
                    "action_taken": f"Server profile {profile_id} successfully assigned to hardware {resource_id}",
                    "details": {"profileId": profile_id, "hardwareUri": f"/rest/server-hardware/{resource_id}"}
                }
            else:
                return {"status": "failed", "error": f"Unsupported action type: {action_type}"}

    async def discover_inventory(self, resource_type: str, credentials: dict, parameters: dict) -> list:
        async with await self._get_client(credentials) as client:
            inventory = []
            if resource_type in ("server_profile", "server_hardware", "server-hardware") or not resource_type:
                resp = await client.get("/rest/server-hardware")
                if resp.status_code == 200:
                    servers = resp.json()
                    # Handle if returned structure is list or dict
                    if isinstance(servers, dict) and "members" in servers:
                        servers = servers["members"]
                    elif isinstance(servers, dict) and "server_hardware" in servers:
                        servers = list(servers["server_hardware"].values())
                    for s in servers:
                        inventory.append({
                            "uuid": s.get("uuid"),
                            "name": s.get("name"),
                            "type": "server_hardware",
                            "model": s.get("model"),
                            "ip_address": s.get("ip_address"),
                            "power_state": s.get("powerState"),
                            "health": s.get("health", "OK")
                        })
            
            if resource_type == "enclosure" or not resource_type:
                resp = await client.get("/rest/rack-managers")
                if resp.status_code == 200:
                    managers = resp.json()
                    if isinstance(managers, dict) and "members" in managers:
                        managers = managers["members"]
                    for m in managers:
                        inventory.append({
                            "uuid": m.get("uuid") or m.get("id"),
                            "name": m.get("name"),
                            "type": "enclosure",
                            "model": "HPE Intelligent Series Rack",
                            "ip_address": m.get("ipAddress"),
                            "power_state": "On",
                            "health": "OK"
                        })
            
            return inventory

    async def sync_cmdb(self, credentials: dict, parameters: dict) -> dict:
        servers = await self.discover_inventory("server_hardware", credentials, parameters)
        enclosures = await self.discover_inventory("enclosure", credentials, parameters)
        return {
            "provider": "oneview",
            "timestamp": "2026-06-09T23:03:15Z",
            "servers": servers,
            "enclosures": enclosures
        }
