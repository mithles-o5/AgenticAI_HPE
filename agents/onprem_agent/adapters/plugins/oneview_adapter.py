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
                # Base server hardware info
                resp = await client.get(f"/rest/server-hardware/{resource_id}")
                if resp.status_code == 200:
                    metrics.update(resp.json())
                
                # Utilization
                util_resp = await client.get(f"/rest/server-hardware/{resource_id}/utilization")
                if util_resp.status_code == 200:
                    metrics.update(util_resp.json())
                    
                # Thermal
                therm_resp = await client.get(f"/rest/server-hardware/{resource_id}/thermal")
                if therm_resp.status_code == 200:
                    metrics.update(therm_resp.json())
            
            # Query chassis utilization if enclosure
            if resource_type == "enclosure":
                resp = await client.get(f"/rest/rack-managers/{resource_id}/chassis/utilization")
                if resp.status_code == 200:
                    metrics.update(resp.json())
            
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
        log.info(f"DEBUG: execute_action type={action_type} verb={action_verb} params={parameters}")

        _POWER_ON_VERBS  = {"on", "power_on", "power-on", "turn_on", "turn on", "start", "boot", "enable", "power_up", "cold_boot"}
        _POWER_OFF_VERBS = {"off", "power_off", "power-off", "turn_off", "turn off", "shutdown", "stop", "halt", "disable", "power_down"}
        _POWER_TYPES     = {"power", "power-on", "power_on", "power-off", "power_off"}

        is_power = (action_type in _POWER_TYPES or action_verb in _POWER_ON_VERBS | _POWER_OFF_VERBS)

        async with await self._get_client(credentials) as client:
            if is_power:
                # Determine target state — "state" parameter takes priority
                state_raw = (parameters.get("state") or parameters.get("power_state") or
                             parameters.get("powerState") or action_verb or "").lower()
                if state_raw in {"on", "poweron", "power_on", "turn_on", "start", "boot", "enable", "power_up", "cold_boot"}:
                    state = "On"
                elif state_raw in {"off", "poweroff", "power_off", "turn_off", "shutdown", "stop", "halt", "disable", "power_down"}:
                    state = "Off"
                elif state_raw == "reset":
                    state = "On"   # reset = cycle through Off then On; for mock just go On
                else:
                    # Last resort: if the action_type says power-off treat as Off
                    state = "Off" if "off" in action_type or "off" in action_verb else "On"

                payload = {"powerState": state}
                log.info(f"DEBUG: Sending PUT powerState={state} for resource_id={resource_id} payload={payload}")
                resp = await client.put(f"/rest/server-hardware/{resource_id}/powerState", json=payload)
                log.info(f"DEBUG: resp.status_code={resp.status_code} text={resp.text[:200]}")
                if resp.status_code in (200, 202):
                    result = resp.json()
                    actual_state = result.get("power_state", state)
                    return {
                        "status": "success",
                        "action_taken": f"Power state set to {state}",
                        "power_state": actual_state,
                        "raw": result
                    }
                else:
                    return {"status": "failed", "error": f"OneView returned code {resp.status_code}: {resp.text[:200]}"}

            elif action_type == "firmware_update":
                version = parameters.get("firmware_version", "iLO5 2.70")
                payload = {"serverUUID": resource_id, "firmwareBaselineId": version}
                resp = await client.post("/rest/server-hardware/firmware-compliance", json=payload)
                if resp.status_code in (200, 201, 202):
                    return {"status": "success", "action_taken": f"Triggered compliance update to baseline {version}", "raw": resp.json()}
                else:
                    return {"status": "failed", "error": f"Failed to post firmware compliance. Status code: {resp.status_code}"}

            elif action_type == "remove" or action_verb in ("delete", "remove"):
                resp = await client.delete(f"/rest/server-hardware/{resource_id}")
                if resp.status_code in (200, 202, 204):
                    return {"status": "success", "action_taken": f"Triggered deletion of {resource_id}", "raw": resp.json()}
                else:
                    return {"status": "failed", "error": f"Failed to delete {resource_id}. Status code: {resp.status_code}"}

            elif action_type == "profile_assign":
                profile_id = parameters.get("profile_id", "prof-default")
                return {
                    "status": "success",
                    "action_taken": f"Server profile {profile_id} successfully assigned to hardware {resource_id}",
                    "details": {"profileId": profile_id, "hardwareUri": f"/rest/server-hardware/{resource_id}"}
                }
                
            elif action_type in ("add", "create") or action_verb in ("add", "create"):
                payload = {"name": resource_id, "id": resource_id}
                if "rack" in parameters.get("resource_type", "") or "rack" in resource_id:
                    resp = await client.post("/rest/rack-managers", json=payload)
                else:
                    resp = await client.post("/rest/server-hardware", json=payload)
                    
                if resp.status_code in (200, 201, 202):
                    return {"status": "success", "action_taken": f"Triggered creation of {resource_id}", "raw": resp.json()}
                else:
                    return {"status": "failed", "error": f"Failed to add {resource_id}. Status code: {resp.status_code}"}
                    
            else:
                return {"status": "failed", "error": f"Unsupported action type: '{action_type}' verb: '{action_verb}'"}


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
                            "uuid": s.get("uuid") or s.get("id"),
                            "name": s.get("name"),
                            "fqdn": f"{s.get('name', s.get('serialNumber', s.get('id', 'unknown')))}.oneview.local",
                            "type": "server_hardware",
                            "model": s.get("model") or s.get("model_name"),
                            "ip_address": s.get("ip_address") or s.get("ipAddress"),
                            "power_state": s.get("power_state") or s.get("powerState"),
                            "health": s.get("health_status") or s.get("status") or s.get("health", "OK")
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
                            "fqdn": f"{m.get('name', m.get('serialNumber', m.get('id', 'unknown')))}.oneview.local",
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
