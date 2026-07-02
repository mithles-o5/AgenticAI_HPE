"""
AgentDispatcher — routes task requests to the correct OASF agent microservice.

Agent base URLs default to localhost dev ports and can be overridden via env vars:
  CLOUD_AGENT_URL   (default: http://127.0.0.1:8005)
  NETWORK_AGENT_URL (default: http://127.0.0.1:8006)
  STORAGE_AGENT_URL (default: http://127.0.0.1:8007)
"""

from __future__ import annotations

import logging
import os
import uuid
from typing import Any, Dict, Optional

import httpx

logger = logging.getLogger(__name__)

# ── Agent registry ────────────────────────────────────────────────────────────
_AGENT_REGISTRY: Dict[str, str] = {
    "cloud":   os.getenv("CLOUD_AGENT_URL",   "http://127.0.0.1:8005"),
    "network": os.getenv("NETWORK_AGENT_URL", "http://127.0.0.1:8006"),
    "storage": os.getenv("STORAGE_AGENT_URL", "http://127.0.0.1:8007"),
}

# Map action verbs from QueryAgent → agent action strings
_ACTION_MAP: Dict[str, str] = {
    # Status
    "STATUS":      "fetch_metrics",
    "CHECK":       "fetch_metrics",
    "SHOW":        "fetch_metrics",
    "GET":         "fetch_metrics",
    "FETCH":       "fetch_metrics",
    "MONITOR":     "fetch_metrics",
    "FETCH_SENSORS": "fetch_metrics",      # routed with resource_type=sensor
    # Power ON
    "ON":          "execute_action",
    "POWER_ON":    "execute_action",
    "TURN_ON":     "execute_action",
    "START":       "execute_action",
    "BOOT":        "execute_action",
    "ENABLE":      "execute_action",
    "POWER_UP":    "execute_action",
    # Power OFF
    "OFF":         "execute_action",
    "POWER_OFF":   "execute_action",
    "TURN_OFF":    "execute_action",
    "SHUTDOWN":    "execute_action",
    "STOP":        "execute_action",
    "HALT":        "execute_action",
    "DISABLE":     "execute_action",
    "POWER_DOWN":  "execute_action",
    # Reset
    "RESET":       "execute_action",
    "REBOOT":      "execute_action",
    "RESTART":     "execute_action",
    "COLD_BOOT":   "execute_action",
    "WARM_BOOT":   "execute_action",
    # Other ops
    "CREATE":      "execute_action",
    "DELETE":      "execute_action",
    "ALLOCATE":    "execute_action",
    "DEALLOCATE":  "execute_action",
    "RELOAD":      "execute_action",
    "RESCAN":      "discover_resources",
    "FAILOVER":    "execute_action",
    "POLICY_SYNC": "execute_action",
    "UPDATE":      "execute_action",
    "PATCH":       "execute_action",
    "MOUNT_VIRTUAL_MEDIA": "execute_action",     # action_type=virtual_media injected by mcp_server
    "FETCH_EVENT_LOG":     "fetch_event_log",
    "CLEAR_EVENT_LOG":     "fetch_event_log",    # clear=True injected by mcp_server
    "DISCOVER_INVENTORY":  "discover_inventory",
    "SYNC_CMDB":           "sync_cmdb",
    "LIST":                "list_resources",
    "LIST_RESOURCES":      "list_resources",
}

# Agent-specific action overrides by domain
_NETWORK_ACTION_MAP: Dict[str, str] = {
    "STATUS": "fetch_metrics",
    "RESCAN": "discover_topology",
}

_STORAGE_ACTION_MAP: Dict[str, str] = {
    "STATUS": "fetch_capacity",
    "RESCAN": "discover_arrays",
}


class AgentDispatcher:
    """
    Stateless dispatcher that resolves target agents via the OASF Capability Registry
    and sends TaskRequest payloads to those agents.
    """

    def __init__(self, timeout_s: float = 15.0) -> None:
        self._timeout = timeout_s

    def dispatch(
        self,
        agent_type: str,
        query_action: str,
        resource_type: str,
        resource_id: str,
        provider_or_protocol: str = "mock",
        parameters: Optional[Dict[str, Any]] = None,
        credentials_ref: Optional[str] = None,
        region: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Query Capability Registry, resolve agent url, format and send task request.
        """
        # ── Step 1: Query Capability Registry ──────────────────────────────
        registry_url = "http://127.0.0.1:8020/agents/lookup"
        try:
            with httpx.Client(timeout=3.0) as client:
                resp = client.get(
                    registry_url,
                    params={
                        "resource_type": resource_type,
                        "provider": provider_or_protocol,
                    }
                )
                resp.raise_for_status()
                agent_record = resp.json()
        except Exception as e:
            logger.warning(f"Failed to query Capability Registry: {e}. Falling back to default routing.")
            # Fallback to local defaults if registry is down
            fallback_ports = {
                "cloud": 8005,
                "network": 8006,
                "storage": 8007,
                "onprem": 8008,
                "server": 8009,
            }
            agent_port = fallback_ports.get(agent_type, 8005)
            agent_record = {
                "name": f"{agent_type}-agent",
                "locators": [{"url": f"http://127.0.0.1:{agent_port}/openapi.json"}]
            }

        # ── Step 1.5: Capability Verification ──────────────────────────────
        # Confirm: Can the agent perform this operation?
        agent_name = agent_record.get("name", "").lower()
        target_skill = None
        if "storage" in agent_name:
            action_skill_map = {
                "STATUS": "storage.monitoring.capacity",
                "CAPACITY": "storage.monitoring.capacity",
                "CREATE_VOLUME": "storage.execute.volume_action",
                "DELETE_VOLUME": "storage.execute.volume_action",
                "RESCAN": "storage.discover.arrays",
                "ON": "storage.execute.volume_action",
                "OFF": "storage.execute.volume_action",
                "LIST": "storage.list.resources",
                "LIST_RESOURCES": "storage.list.resources",
            }
            target_skill = action_skill_map.get(query_action)
        elif "server" in agent_name:
            # Skill names MUST match oasf_record.json exactly
            action_skill_map = {
                "STATUS":              "server.monitoring.health",
                "FETCH_SENSORS":       "server.monitoring.sensors",
                "ON":                  "server.execute.power_action",
                "OFF":                 "server.execute.power_action",
                "POWER_ON":            "server.execute.power_action",
                "POWER_OFF":           "server.execute.power_action",
                "RESET":               "server.execute.power_action",
                "COLD_BOOT":           "server.execute.power_action",
                "MOUNT_VIRTUAL_MEDIA": "server.execute.virtual_media",
                "FETCH_EVENT_LOG":     "server.monitoring.eventlog",
                "CLEAR_EVENT_LOG":     "server.monitoring.eventlog",
                "DISCOVER_INVENTORY":  "server.discover.inventory",
                "SYNC_CMDB":           "server.sync.cmdb",
                "LIST":                "server.list.resources",
                "LIST_RESOURCES":      "server.list.resources",
            }
            target_skill = action_skill_map.get(query_action)
        elif "onprem" in agent_name:
            action_skill_map = {
                "STATUS":        "onprem.monitoring.health",
                "ON":            "onprem.execute.power_action",
                "OFF":           "onprem.execute.power_action",
                "POWER_ON":      "onprem.execute.power_action",
                "POWER_OFF":     "onprem.execute.power_action",
                "LIST":          "onprem.list.resources",
                "LIST_RESOURCES":"onprem.list.resources",
            }
            target_skill = action_skill_map.get(query_action)
        elif "cloud" in agent_name:
            action_skill_map = {
                "STATUS":        "cloud.monitoring.health_check",
                "ON":            "cloud.execute.action",
                "OFF":           "cloud.execute.action",
                "LIST":          "cloud.list.resources",
                "LIST_RESOURCES":"cloud.list.resources",
            }
            target_skill = action_skill_map.get(query_action)
        elif "network" in agent_name:
            action_skill_map = {
                "STATUS":        "network.monitoring.interface",
                "RESCAN":        "network.topology.discover",
                "LIST":          "network.list.resources",
                "LIST_RESOURCES":"network.list.resources",
            }
            target_skill = action_skill_map.get(query_action)

        if target_skill and agent_record.get("skills"):
            agent_skills = [s.get("name") for s in agent_record.get("skills", [])]
            if target_skill not in agent_skills:
                msg = f"Capability error: Agent '{agent_record.get('name')}' does not support skill '{target_skill}' for action '{query_action}'."
                logger.error("[AgentDispatcher] %s", msg)
                return {"status": "failed", "errors": [msg]}

        # Resolve locator URL
        locator_url = agent_record["locators"][0]["url"]
        # Convert locator url (e.g. http://cloud-agent:8005/openapi.json) to localhost/127.0.0.1
        from urllib.parse import urlparse
        parsed = urlparse(locator_url)
        
        # Override hostname to localhost for local dev
        hostname = "127.0.0.1"
        port = parsed.port or 8005

        # Fix onprem agent port if name matches
        agent_name = agent_record.get("name", "")
        if "onprem" in agent_name:
            port = 8008

        base_url = f"http://{hostname}:{port}"
        agent_key = agent_name.replace("-agent", "").lower().strip()

        # Resolve the correct agent action for this domain
        if agent_key == "server":
            agent_action = query_action
        else:
            agent_action = self._resolve_action(agent_key, query_action)

        # Build payload key name — cloud/storage/onprem use "provider"; network uses "protocol"
        if agent_key == "network":
            protocol_key = "protocol"
        else:
            protocol_key = "provider"
        prov_val = provider_or_protocol

        # Normalize resource_type for server-agent
        if agent_key == "server" and resource_type not in {"server", "bmc", "sensor", "firmware", "event_log"}:
            resource_type = "server"

        payload: Dict[str, Any] = {
            "task_id":          str(uuid.uuid4()),
            "task_type":        self._resolve_task_type(query_action),
            "agent_type":       agent_key,
            "resource_type":    resource_type,
            "resource_id":      resource_id,
            protocol_key:       prov_val,
            "action":           agent_action,
            "parameters":       parameters or {},
        }
        if credentials_ref:
            payload["credentials_ref"] = credentials_ref
        if region:
            payload["region"] = region

        # Add action_verb to parameters so execute_action knows what to do
        if agent_action == "execute_action":
            payload["parameters"]["action_verb"] = query_action.lower()
            _POWER_ON_ACTIONS  = {"ON", "POWER_ON", "TURN_ON", "START", "BOOT", "ENABLE", "POWER_UP", "COLD_BOOT"}
            _POWER_OFF_ACTIONS = {"OFF", "POWER_OFF", "TURN_OFF", "SHUTDOWN", "STOP", "HALT", "DISABLE", "POWER_DOWN"}
            _RESET_ACTIONS     = {"RESET", "REBOOT", "RESTART", "WARM_BOOT"}
            if query_action in _POWER_ON_ACTIONS | _POWER_OFF_ACTIONS | _RESET_ACTIONS:
                payload["parameters"]["action_type"] = "power"
                if query_action in _POWER_ON_ACTIONS:
                    payload["parameters"]["state"] = "On"
                elif query_action in _POWER_OFF_ACTIONS:
                    payload["parameters"]["state"] = "Off"
                else:
                    payload["parameters"]["state"] = "Reset"


        # Route endpoint mapping
        if agent_key == "onprem":
            url = f"{base_url}/tasks"
        else:
            url = f"{base_url}/{agent_key}-agent/execute-task"

        logger.info(
            "[AgentDispatcher] Resolved via OASF Capability Registry -> %s | url=%s",
            agent_name, url
        )

        try:
            with httpx.Client(timeout=self._timeout) as client:
                resp = client.post(url, json=payload)
                resp.raise_for_status()
                return resp.json()
        except httpx.ConnectError:
            msg = (
                f"Could not connect to {agent_name} at {base_url}. "
                f"Start it with: python agents/{agent_key}_agent/main.py"
            )
            logger.error("[AgentDispatcher] %s", msg)
            return {"status": "failed", "errors": [msg]}
        except httpx.TimeoutException:
            msg = f"{agent_name} at {base_url} timed out after {self._timeout}s."
            logger.error("[AgentDispatcher] %s", msg)
            return {"status": "failed", "errors": [msg]}
        except httpx.HTTPStatusError as exc:
            msg = f"{agent_name} returned HTTP {exc.response.status_code}: {exc.response.text}"
            logger.error("[AgentDispatcher] %s", msg)
            return {"status": "failed", "errors": [msg]}

    @staticmethod
    def _resolve_action(agent_key: str, query_action: str) -> str:
        """Map a QueryAgent action verb to the domain-specific agent action string."""
        if agent_key == "network":
            return _NETWORK_ACTION_MAP.get(query_action, _ACTION_MAP.get(query_action, "fetch_metrics"))
        if agent_key == "storage":
            return _STORAGE_ACTION_MAP.get(query_action, _ACTION_MAP.get(query_action, "fetch_capacity"))
        # cloud/onprem
        return _ACTION_MAP.get(query_action, "fetch_metrics")

    @staticmethod
    def _resolve_task_type(query_action: str) -> str:
        """Derive task_type from the QueryAgent action."""
        if query_action in {"STATUS"}:
            return "monitoring"
        if query_action in {"RESCAN"}:
            return "discovery"
        if query_action in {"CREATE", "ALLOCATE", "DEALLOCATE", "DELETE"}:
            return "control"
        return "operational"

    @staticmethod
    def registered_agents() -> list[str]:
        return sorted(_AGENT_REGISTRY.keys())

    @staticmethod
    def agent_url(agent_type: str) -> Optional[str]:
        return _AGENT_REGISTRY.get(agent_type.lower())

