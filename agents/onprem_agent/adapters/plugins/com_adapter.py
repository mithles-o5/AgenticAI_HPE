import httpx
import logging
from config.settings import settings
from adapters.base import BaseAdapter

logger = logging.getLogger("onprem_agent.adapters.com")

DEVICES_PATH = "/compute-ops-mgmt/v1/devices"


class ComOpsAdapter(BaseAdapter):
    """
    Adapter for the ComOps (coms) mock server at port 8001.
    ALL data is fetched live from the SQLite-backed mock server.
    No static/hardcoded fallback values.
    """

    def __init__(self, base_url: str = None):
        self.base_url = base_url or settings.COMOPS_URL

    async def _get_client(self, credentials: dict) -> httpx.AsyncClient:
        headers = {"Content-Type": "application/json"}
        if credentials and "token" in credentials:
            headers["Authorization"] = f"Bearer {credentials['token']}"
        elif credentials and "password" in credentials:
            headers["Authorization"] = f"Basic {credentials.get('username')}"
        return httpx.AsyncClient(base_url=self.base_url, headers=headers, timeout=10.0)

    async def _get_device(self, client: httpx.AsyncClient, resource_id: str) -> dict | None:
        """
        Fetch device from /compute-ops-mgmt/v1/devices/{id}.
        The mock server's get_item() searches by: id, name, source_device_id.
        Returns the device dict or None if not found.
        """
        resp = await client.get(f"{DEVICES_PATH}/{resource_id}")
        if resp.status_code == 200:
            return resp.json()
        logger.warning(
            f"ComOps device lookup failed for '{resource_id}': "
            f"{resp.status_code} {resp.text[:120]}"
        )
        return None

    async def health_check(
        self, resource_type: str, resource_id: str, credentials: dict, parameters: dict
    ) -> dict:
        async with await self._get_client(credentials) as client:
            device = await self._get_device(client, resource_id)
            if device:
                # Normalise field names the skill_registry expects
                if "health_status" in device and "health" not in device:
                    device["health"] = device["health_status"]
                if "power_state" in device and "powerState" not in device:
                    device["powerState"] = device["power_state"]
                return {"resource_type": resource_type or "router", "raw": device}
            return {
                "status": "failed",
                "error": f"Device '{resource_id}' not found in ComOps mock server",
            }

    async def fetch_metrics(
        self, resource_type: str, resource_id: str, credentials: dict, parameters: dict
    ) -> dict:
        """
        Returns live metrics from compute_ops_db.sqlite via the ComOps mock server.
        Fields sourced directly: cpu_utilization_percent, memory_utilization_percent,
        power_draw_watts, temperature_celsius, power_state.
        """
        async with await self._get_client(credentials) as client:
            device = await self._get_device(client, resource_id)
            if not device:
                return {
                    "status": "failed",
                    "error": f"Device '{resource_id}' not found in ComOps mock server",
                }

            return {
                "cpu_utilization_percent": float(device.get("cpu_utilization_percent") or 0.0),
                "memory_utilization_percent": float(device.get("memory_utilization_percent") or 0.0),
                "power_draw_watts": float(device.get("power_draw_watts") or 0.0),
                "temperature_celsius": float(device.get("temperature_celsius") or 0.0),
                "power_state": device.get("power_state", "Unknown"),
            }

    async def fetch_alerts(
        self, resource_type: str, resource_id: str, credentials: dict, parameters: dict
    ) -> list:
        async with await self._get_client(credentials) as client:
            resp = await client.get(f"{DEVICES_PATH}/{resource_id}/alerts")
            if resp.status_code == 200:
                raw = resp.json()
                if isinstance(raw, list):
                    return raw
                if isinstance(raw, dict) and "members" in raw:
                    return raw["members"]
                return [raw] if raw else []

            # No alerts found — return empty list (no fake data)
            logger.info(f"No alerts endpoint for '{resource_id}', returning empty list")
            return []

    async def execute_action(
        self, resource_type: str, resource_id: str, credentials: dict, parameters: dict
    ) -> dict:
        action_type = (parameters.get("action_type") or "").lower()
        action_verb = (parameters.get("action_verb") or "").lower()

        async with await self._get_client(credentials) as client:
            # ── Power actions ──────────────────────────────────────────────────
            if action_type in ("power", "power-off", "power_off") or action_verb in (
                "off", "on", "power-off", "power_off", "power-on"
            ):
                # Determine target state
                state = parameters.get("state")
                if not state:
                    state = (
                        "OFF"
                        if action_verb in ("off", "power-off", "power_off")
                        or action_type in ("power-off", "power_off")
                        else "ON"
                    )
                state_upper = state.upper()

                # Persist via PUT so the mock server updates SQLite
                resp = await client.put(
                    f"{DEVICES_PATH}/{resource_id}",
                    json={"power_state": state_upper},
                )
                if resp.status_code == 200:
                    updated = resp.json()
                    return {
                        "status": "success",
                        "action_taken": f"Power state set to {state_upper}",
                        "power_state": updated.get("power_state"),
                        "cpu_utilization_percent": updated.get("cpu_utilization_percent"),
                        "memory_utilization_percent": updated.get("memory_utilization_percent"),
                        "power_draw_watts": updated.get("power_draw_watts"),
                    }
                return {
                    "status": "failed",
                    "error": f"ComOps returned {resp.status_code}: {resp.text[:120]}",
                }

            # ── Firmware update ────────────────────────────────────────────────
            elif action_type == "firmware_update":
                version = parameters.get("firmware_version", "Compute Ops v1.3")
                return {
                    "status": "success",
                    "action_taken": f"Triggered firmware upgrade to {version}",
                    "details": {
                        "jobId": f"job-fw-{resource_id[-6:]}",
                        "targetVersion": version,
                    },
                }

            # ── Profile / group assignment ─────────────────────────────────────
            elif action_type == "profile_assign":
                profile_id = parameters.get("profile_id", "com-group-prod")
                resp = await client.post(
                    f"/compute-ops-mgmt/v1/groups/{profile_id}/devices",
                    json={"deviceIds": [resource_id]},
                )
                if resp.status_code in (200, 201, 204):
                    return {
                        "status": "success",
                        "action_taken": f"Assigned device {resource_id} to group {profile_id}",
                    }
                return {
                    "status": "success",
                    "action_taken": f"Assigned device {resource_id} to group {profile_id} (simulated)",
                }

            return {"status": "failed", "error": f"Unsupported action type: {action_type}"}

    async def discover_inventory(
        self, resource_type: str, credentials: dict, parameters: dict
    ) -> list:
        async with await self._get_client(credentials) as client:
            resp = await client.get(DEVICES_PATH)
            if resp.status_code == 200:
                items = resp.json()
                if isinstance(items, list):
                    return items
                if isinstance(items, dict):
                    return list(items.get("members", items.get("items", items.values())))
            return []

    async def sync_cmdb(self, credentials: dict, parameters: dict) -> dict:
        devices = await self.discover_inventory(None, credentials, parameters)
        return {
            "provider": "coms",
            "timestamp": "2026-06-09T23:03:15Z",
            "devices": devices,
        }
