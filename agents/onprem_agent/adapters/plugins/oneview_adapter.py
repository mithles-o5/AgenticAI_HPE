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
            if resource_type == "enclosure":
                resp = await client.get(f"/rest/rack-managers/{resource_id}")
                if resp.status_code == 200:
                    return {"resource_type": "enclosure", "raw": resp.json()}
                else:
                    return {"status": "failed", "error": f"Resource not found. Status code: {resp.status_code}"}
            else:
                resp = await client.get(f"/rest/server-hardware/{resource_id}")
                if resp.status_code == 200:
                    data = resp.json()
                    # map health_status and power_state for generic skills
                    if "health_status" in data and "health" not in data:
                        data["health"] = data["health_status"]
                    if "power_state" in data and "powerState" not in data:
                        data["powerState"] = data["power_state"]
                    return {"resource_type": resource_type or "server_hardware", "raw": data}
                else:
                    return {"status": "failed", "error": f"Resource not found. Status code: {resp.status_code}"}

    async def fetch_metrics(self, resource_type: str, resource_id: str, credentials: dict, parameters: dict) -> dict:
        async with await self._get_client(credentials) as client:
            metrics = {}
            if resource_type != "enclosure":
                resp = await client.get(f"/rest/server-hardware/{resource_id}")
                if resp.status_code == 200:
                    data = resp.json()
                    metrics = data
            
            # Query chassis utilization if enclosure
            if resource_type == "enclosure":
                resp = await client.get(f"/rest/rack-managers/{resource_id}/chassis/utilization")
                if resp.status_code == 200:
                    util_data = resp.json()
                    metrics.update(util_data)
            
            if not metrics:
                 return {"status": "failed", "error": "No metrics or resource found in DB"}
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
        action_type = parameters.get("action_type", "").lower()
        action_verb = parameters.get("action_verb", "").lower()
        import logging; log = logging.getLogger(__name__)
        log.info(f"DEBUG: execute_action type={action_type} verb={action_verb}")
        async with await self._get_client(credentials) as client:
            if action_type in ("power", "power-off", "power_off") or action_verb in ("power-off", "off", "on", "power_off"):
                state = parameters.get("state")
                if not state:
                    state = "Off" if action_verb in ("off", "power-off", "power_off") or action_type in ("power-off", "power_off") else "On"
                payload = {"powerState": state}
                log.info(f"DEBUG: payload={payload}")
                resp = await client.put(f"/rest/server-hardware/{resource_id}/powerState", json=payload)
                log.info(f"DEBUG: resp.status_code={resp.status_code} text={resp.text}")
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
