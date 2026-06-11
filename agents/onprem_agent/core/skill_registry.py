import logging
from abc import ABC, abstractmethod
from typing import Dict
from core.normalization import (
    normalize_server_data,
    normalize_metrics,
    normalize_alerts
)
from core.anomaly_detection import detect_anomalies
from core.exceptions import SkillError

logger = logging.getLogger("onprem_agent.skill_registry")

class BaseSkill(ABC):
    @abstractmethod
    async def execute(self, adapter, request, credentials: dict) -> dict:
        """Execute the skill logic against the adapter."""
        pass

class HealthSkill(BaseSkill):
    async def execute(self, adapter, request, credentials: dict) -> dict:
        raw_res = await adapter.health_check(
            request.resource_type,
            request.resource_id,
            credentials,
            request.parameters
        )
        normalized = normalize_server_data(request.provider, raw_res.get("raw", {}))
        
        # Determine status level & insights
        status_level, insights = detect_anomalies(health_data=normalized)
        if not insights:
            insights.append({
                "type": "health_info",
                "severity": "info",
                "message": f"Resource {normalized.get('name', request.resource_id)} is healthy"
            })
        
        return {
            "status": "success",
            "metrics": {},
            "actions_taken": ["health_check"],
            "status_level": status_level,
            "insights": insights,
            "normalized_data": normalized
        }


class UtilizationSkill(BaseSkill):
    async def execute(self, adapter, request, credentials: dict) -> dict:
        raw_metrics = await adapter.fetch_metrics(
            request.resource_type,
            request.resource_id,
            credentials,
            request.parameters
        )
        normalized = normalize_metrics(raw_metrics)
        
        # Determine status level & insights
        status_level, insights = detect_anomalies(metrics=normalized)
        
        return {
            "status": "success",
            "metrics": normalized,
            "actions_taken": ["fetch_metrics"],
            "status_level": status_level,
            "insights": insights
        }

class AlertsSkill(BaseSkill):
    async def execute(self, adapter, request, credentials: dict) -> dict:
        raw_alerts = await adapter.fetch_alerts(
            request.resource_type,
            request.resource_id,
            credentials,
            request.parameters
        )
        normalized = normalize_alerts(request.provider, raw_alerts)
        
        # Determine status level & insights
        status_level, insights = detect_anomalies(alerts=normalized)
        
        return {
            "status": "success",
            "metrics": {"alert_count": len(normalized)},
            "actions_taken": ["fetch_alerts"],
            "status_level": status_level,
            "insights": insights,
            "normalized_data": {"alerts": normalized}
        }

class PowerActionSkill(BaseSkill):
    async def execute(self, adapter, request, credentials: dict) -> dict:
        state = request.parameters.get("state")
        if not state:
            raise SkillError("Parameter 'state' (On/Off/Reset) is required for power_action.")
        
        params = {"action_type": "power", "state": state}
        res = await adapter.execute_action(
            request.resource_type,
            request.resource_id,
            credentials,
            params
        )
        
        if res.get("status") == "success":
            return {
                "status": "success",
                "metrics": {},
                "actions_taken": [f"power_{state.lower()}"],
                "status_level": "healthy",
                "insights": [{"type": "lifecycle_event", "message": f"Power state set to {state}"}]
            }
        else:
            return {
                "status": "failed",
                "metrics": {},
                "actions_taken": [],
                "status_level": "critical",
                "errors": [res.get("error", "Power action failed")]
            }

class ProfileAssignSkill(BaseSkill):
    async def execute(self, adapter, request, credentials: dict) -> dict:
        profile_id = request.parameters.get("profile_id")
        if not profile_id:
            raise SkillError("Parameter 'profile_id' is required for profile_assign.")
        
        params = {"action_type": "profile_assign", "profile_id": profile_id}
        res = await adapter.execute_action(
            request.resource_type,
            request.resource_id,
            credentials,
            params
        )
        
        if res.get("status") == "success":
            return {
                "status": "success",
                "metrics": {},
                "actions_taken": ["profile_assignment"],
                "status_level": "healthy",
                "insights": [{"type": "configuration_change", "message": f"Assigned profile {profile_id}"}]
            }
        else:
            return {
                "status": "failed",
                "metrics": {},
                "actions_taken": [],
                "status_level": "critical",
                "errors": [res.get("error", "Profile assignment failed")]
            }

class FirmwareUpdateSkill(BaseSkill):
    async def execute(self, adapter, request, credentials: dict) -> dict:
        version = request.parameters.get("firmware_version")
        if not version:
            raise SkillError("Parameter 'firmware_version' is required for firmware_update.")
        
        params = {"action_type": "firmware_update", "firmware_version": version}
        res = await adapter.execute_action(
            request.resource_type,
            request.resource_id,
            credentials,
            params
        )
        
        if res.get("status") == "success":
            return {
                "status": "success",
                "metrics": {},
                "actions_taken": [f"firmware_upgrade_to_{version}"],
                "status_level": "healthy",
                "insights": [{"type": "lifecycle_event", "message": f"Triggered firmware upgrade to {version}"}]
            }
        else:
            return {
                "status": "failed",
                "metrics": {},
                "actions_taken": [],
                "status_level": "critical",
                "errors": [res.get("error", "Firmware update failed")]
            }

class InventorySkill(BaseSkill):
    async def execute(self, adapter, request, credentials: dict) -> dict:
        inventory = await adapter.discover_inventory(
            request.resource_type,
            credentials,
            request.parameters
        )
        return {
            "status": "success",
            "metrics": {"discovered_count": len(inventory)},
            "actions_taken": ["discover_inventory"],
            "status_level": "healthy",
            "insights": [{"type": "discovery", "message": f"Discovered {len(inventory)} resources"}],
            "normalized_data": {"inventory": inventory}
        }

class AnomalySkill(BaseSkill):
    async def execute(self, adapter, request, credentials: dict) -> dict:
        # Runs diagnostic health, metrics, and alerts to perform custom diagnose.anomaly
        health_data = {}
        metrics_data = {}
        alerts_data = []
        errors = []

        try:
            raw_health = await adapter.health_check(request.resource_type, request.resource_id, credentials, request.parameters)
            health_data = normalize_server_data(request.provider, raw_health.get("raw", {}))
        except Exception as e:
            errors.append(f"Diagnostics: health_check failed: {e}")

        try:
            raw_metrics = await adapter.fetch_metrics(request.resource_type, request.resource_id, credentials, request.parameters)
            metrics_data = normalize_metrics(raw_metrics)
        except Exception as e:
            errors.append(f"Diagnostics: fetch_metrics failed: {e}")

        try:
            raw_alerts = await adapter.fetch_alerts(request.resource_type, request.resource_id, credentials, request.parameters)
            alerts_data = normalize_alerts(request.provider, raw_alerts)
        except Exception as e:
            errors.append(f"Diagnostics: fetch_alerts failed: {e}")

        status_level, insights = detect_anomalies(
            health_data=health_data or None,
            metrics=metrics_data or None,
            alerts=alerts_data or None
        )

        return {
            "status": "success" if not errors else "partial",
            "metrics": metrics_data,
            "actions_taken": ["diagnose_anomaly"],
            "status_level": status_level,
            "insights": insights,
            "errors": errors
        }

class SyncCmdbSkill(BaseSkill):
    async def execute(self, adapter, request, credentials: dict) -> dict:
        cmdb_payload = await adapter.sync_cmdb(credentials, request.parameters)
        # In a real setup, we would POST this payload to settings.CMDB_URL.
        # We will mock the client POST request and record success.
        import httpx
        from config.settings import settings
        
        actions = ["sync_cmdb"]
        insights = [{"type": "cmdb_sync", "message": f"Collected CMDB sync payload with {len(cmdb_payload.get('servers', []))} servers"}]
        errors = []
        
        cmdb_url = settings.CMDB_URL
        if cmdb_url and not cmdb_url.startswith("mock") and "localhost:8004" not in cmdb_url:
            try:
                async with httpx.AsyncClient() as client:
                    resp = await client.post(f"{cmdb_url}/inventory", json=cmdb_payload, timeout=10.0)
                    resp.raise_for_status()
                    insights.append({"type": "cmdb_sync_post", "message": f"Successfully POSTed inventory to CMDB at {cmdb_url}"})
            except Exception as e:
                logger.error(f"CMDB sync post failed: {e}")
                errors.append(f"Failed to post to CMDB endpoint: {e}")
        else:
            insights.append({"type": "cmdb_sync_mock", "message": "Bypassed CMDB POST (running in mock/local mode)"})

        return {
            "status": "success" if not errors else "failed",
            "metrics": {"servers_synced": len(cmdb_payload.get("servers", []))},
            "actions_taken": actions,
            "status_level": "healthy" if not errors else "critical",
            "insights": insights,
            "errors": errors,
            "normalized_data": cmdb_payload
        }

# Global registry mapping skills
SKILLS: Dict[str, BaseSkill] = {
    "onprem.monitoring.health": HealthSkill(),
    "onprem.monitoring.utilization": UtilizationSkill(),
    "onprem.monitoring.alerts": AlertsSkill(),
    "onprem.execute.power_action": PowerActionSkill(),
    "onprem.execute.profile_assign": ProfileAssignSkill(),
    "onprem.execute.firmware_update": FirmwareUpdateSkill(),
    "onprem.discover.inventory": InventorySkill(),
    "onprem.diagnose.anomaly": AnomalySkill(),
    "onprem.sync.cmdb": SyncCmdbSkill()
}

def resolve_skill_name(action: str, parameters: dict = None) -> str:
    """Resolve action strings to their canonical OASF skill name."""
    act = action.lower().strip()
    if act == "health_check":
        return "onprem.monitoring.health"
    elif act == "fetch_metrics":
        return "onprem.monitoring.utilization"
    elif act == "fetch_alerts":
        return "onprem.monitoring.alerts"
    elif act == "discover_inventory":
        return "onprem.discover.inventory"
    elif act == "diagnose_anomaly":
        return "onprem.diagnose.anomaly"
    elif act == "sync_cmdb":
        return "onprem.sync.cmdb"
    elif act == "execute_action":
        action_type = (parameters or {}).get("action_type", "").lower()
        if action_type == "power":
            return "onprem.execute.power_action"
        elif action_type == "profile_assign":
            return "onprem.execute.profile_assign"
        elif action_type == "firmware_update":
            return "onprem.execute.firmware_update"
        else:
            raise SkillError(f"Unknown execute_action type: '{action_type}'")
    else:
        raise SkillError(f"Unsupported action: '{action}'")
