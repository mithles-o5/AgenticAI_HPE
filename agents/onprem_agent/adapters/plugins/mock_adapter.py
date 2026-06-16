from adapters.base import BaseAdapter

class MockAdapter(BaseAdapter):
    async def health_check(self, resource_type: str, resource_id: str, credentials: dict, parameters: dict) -> dict:
        return {
            "resource_type": resource_type or "server_hardware",
            "raw": {
                "uuid": resource_id or "mock-uuid-1234",
                "name": "MockServer-01",
                "health": "OK",
                "status": "Healthy",
                "powerState": "On"
            }
        }

    async def fetch_metrics(self, resource_type: str, resource_id: str, credentials: dict, parameters: dict) -> dict:
        return {
            "cpu_utilization_percent": 12.5,
            "memory_utilization_percent": 34.0,
            "power_draw_watts": 120,
            "temperature_celsius": 24.5
        }

    async def fetch_alerts(self, resource_type: str, resource_id: str, credentials: dict, parameters: dict) -> list:
        return [
            {
                "id": "mock-alert-001",
                "severity": "Warning",
                "description": "Mock Alert Description",
                "created": "2026-06-09T00:00:00Z"
            }
        ]

    async def execute_action(self, resource_type: str, resource_id: str, credentials: dict, parameters: dict) -> dict:
        action_type = parameters.get("action_type")
        if action_type == "power":
            state = parameters.get("state", "On")
            return {"status": "success", "action_taken": f"Power state set to {state}"}
        elif action_type == "firmware_update":
            version = parameters.get("firmware_version", "1.0.0")
            return {"status": "success", "action_taken": f"Triggered firmware upgrade to {version}"}
        elif action_type == "profile_assign":
            profile_id = parameters.get("profile_id", "mock-profile")
            return {"status": "success", "action_taken": f"Assigned profile {profile_id}"}
        return {"status": "failed", "error": "Unknown action"}

    async def discover_inventory(self, resource_type: str, credentials: dict, parameters: dict) -> list:
        return [
            {
                "uuid": "mock-uuid-1",
                "name": "Mock-Server-1",
                "type": "server_hardware",
                "model": "Mock-Model-A",
                "ip_address": "127.0.0.1",
                "power_state": "On",
                "health": "OK"
            }
        ]

    async def sync_cmdb(self, credentials: dict, parameters: dict) -> dict:
        return {
            "provider": "mock",
            "timestamp": "2026-06-09T23:03:15Z",
            "servers": await self.discover_inventory(None, credentials, parameters)
        }
