import httpx
import logging
from typing import Any, Dict, List, Optional
from config.settings import settings
from adapters.base import BaseCloudAdapter

logger = logging.getLogger("cloud_agent.adapters.com")

DEVICES_PATH = "/compute-ops-mgmt/v1/devices"

class ComOpsAdapter(BaseCloudAdapter):
    """
    Adapter for the ComOps (coms) mock server at port 8001.
    All data is fetched live from the SQLite-backed mock server.
    """

    def __init__(self, base_url: str = None):
        self.base_url = base_url or getattr(settings, "COMOPS_URL", "http://localhost:8001")

    @property
    def provider_name(self) -> str:
        return "coms"

    def _get_client(self, credentials: dict) -> httpx.Client:
        headers = {"Content-Type": "application/json"}
        if credentials and "token" in credentials:
            headers["Authorization"] = f"Bearer {credentials['token']}"
        elif credentials and "password" in credentials:
            headers["Authorization"] = f"Basic {credentials.get('username')}"
        return httpx.Client(base_url=self.base_url, headers=headers, timeout=10.0)

    def _get_device(self, client: httpx.Client, resource_id: str) -> dict | None:
        """Fetch device from /compute-ops-mgmt/v1/devices/{id}."""
        resp = client.get(f"{DEVICES_PATH}/{resource_id}")
        if resp.status_code == 200:
            return resp.json()
        logger.warning(
            f"ComOps device lookup failed for '{resource_id}': "
            f"{resp.status_code} {resp.text[:120]}"
        )
        return None

    def health_check(
        self,
        resource_id: str,
        resource_type: str,
        region: Optional[str],
        credentials: Dict[str, Any],
        parameters: Dict[str, Any],
    ) -> Dict[str, Any]:
        with self._get_client(credentials) as client:
            device = self._get_device(client, resource_id)
            if device:
                if "health_status" in device and "health" not in device:
                    device["health"] = device["health_status"]
                if "power_state" in device and "powerState" not in device:
                    device["powerState"] = device["power_state"]
                return {"healthy": True, "detail": device.get("health", "OK"), "raw": device}
            return {
                "healthy": False,
                "detail": f"Device '{resource_id}' not found in ComOps mock server",
            }

    def fetch_metrics(
        self,
        resource_id: str,
        resource_type: str,
        region: Optional[str],
        credentials: Dict[str, Any],
        parameters: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Returns live metrics from compute_ops_db.sqlite via the ComOps mock server.
        """
        with self._get_client(credentials) as client:
            device = self._get_device(client, resource_id)
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

    def execute_action(
        self,
        resource_id: str,
        resource_type: str,
        region: Optional[str],
        action: str,
        credentials: Dict[str, Any],
        parameters: Dict[str, Any],
    ) -> Dict[str, Any]:
        action_type = (parameters.get("action_type") or action or "").lower()
        action_verb = (parameters.get("action_verb") or "").lower()

        with self._get_client(credentials) as client:
            # Power actions
            if action_type in ("power", "power-off", "power_off") or action_verb in (
                "off", "on", "power-off", "power_off", "power-on"
            ):
                state = parameters.get("state")
                if not state:
                    state = (
                        "OFF"
                        if action_verb in ("off", "power-off", "power_off")
                        or action_type in ("power-off", "power_off")
                        else "ON"
                    )
                state_upper = state.upper()

                resp = client.put(
                    f"{DEVICES_PATH}/{resource_id}",
                    json={"power_state": state_upper},
                )
                if resp.status_code == 200:
                    updated = resp.json()
                    return {
                        "result": "success",
                        "detail": f"Power state set to {state_upper}",
                        "power_state": updated.get("power_state"),
                        "cpu_utilization_percent": updated.get("cpu_utilization_percent"),
                        "memory_utilization_percent": updated.get("memory_utilization_percent"),
                        "power_draw_watts": updated.get("power_draw_watts"),
                    }
                return {
                    "result": "failed",
                    "detail": f"ComOps returned {resp.status_code}: {resp.text[:120]}",
                }

            # Firmware update
            elif action_type == "firmware_update":
                version = parameters.get("firmware_version", "Compute Ops v1.3")
                return {
                    "result": "success",
                    "detail": f"Triggered firmware upgrade to {version}",
                    "jobId": f"job-fw-{resource_id[-6:]}",
                    "targetVersion": version,
                }

            # Profile assign
            elif action_type == "profile_assign":
                profile_id = parameters.get("profile_id", "com-group-prod")
                resp = client.post(
                    f"/compute-ops-mgmt/v1/groups/{profile_id}/devices",
                    json={"deviceIds": [resource_id]},
                )
                if resp.status_code in (200, 201, 204):
                    return {
                        "result": "success",
                        "detail": f"Assigned device {resource_id} to group {profile_id}",
                    }
                return {
                    "result": "success",
                    "detail": f"Assigned device {resource_id} to group {profile_id} (simulated)",
                }

            return {"result": "failed", "detail": f"Unsupported action type: {action_type}"}

    def discover_resources(
        self,
        region: Optional[str],
        resource_type: str,
        credentials: Dict[str, Any],
        parameters: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        with self._get_client(credentials) as client:
            resp = client.get(DEVICES_PATH)
            if resp.status_code == 200:
                items = resp.json()
                if isinstance(items, list):
                    return items
                if isinstance(items, dict):
                    return list(items.get("members", items.get("items", items.values())))
            return []
