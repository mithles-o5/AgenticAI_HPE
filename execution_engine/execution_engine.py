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
    "STATUS":      "fetch_metrics",
    "ON":          "execute_action",
    "OFF":         "execute_action",
    "RESET":       "execute_action",
    "COLD_BOOT":   "execute_action",
    "CREATE":      "execute_action",
    "DELETE":      "execute_action",
    "ALLOCATE":    "execute_action",
    "DEALLOCATE":  "execute_action",
    "RELOAD":      "execute_action",
    "RESCAN":      "discover_resources",
    "FAILOVER":    "execute_action",
    "POLICY_SYNC": "execute_action",
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
        # Resolve the OASF skill name dynamically
        action_upper = query_action.upper()
        skill_name = None
        if agent_type == "storage":
            if action_upper in {"STATUS", "CAPACITY"}:
                skill_name = "storage.monitoring.capacity"
            elif action_upper in {"CREATE", "ALLOCATE", "DEALLOCATE", "DELETE", "CREATE_VOLUME", "DELETE_VOLUME", "ON", "OFF", "RESET"}:
                skill_name = "storage.execute.volume_action"
            elif action_upper in {"RESCAN"}:
                skill_name = "storage.discover.arrays"
            else:
                skill_name = f"storage.execute.{query_action.lower()}"
        elif agent_type == "network":
            if action_upper in {"STATUS"}:
                skill_name = "network.monitoring.interface"
            elif action_upper in {"RESCAN"}:
                skill_name = "network.topology.discover"
            elif action_upper in {"ON", "OFF", "RESET"}:
                skill_name = "network.execute.config_push"
            else:
                skill_name = f"network.execute.{query_action.lower()}"
        elif agent_type == "cloud":
            if action_upper in {"STATUS"}:
                skill_name = "cloud.monitoring.metrics"
            elif action_upper in {"RESCAN"}:
                skill_name = "cloud.discover.resources"
            elif action_upper in {"ON", "OFF", "RESET"}:
                skill_name = "cloud.execute.action"
            else:
                skill_name = f"cloud.execute.{query_action.lower()}"
        elif agent_type == "server":
            if action_upper in {"STATUS"}:
                skill_name = "server.monitoring.health"
            elif action_upper in {"ON", "OFF", "RESET"}:
                skill_name = "server.execute.power_action"
            else:
                skill_name = f"server.execute.{query_action.lower()}"
        elif agent_type == "onprem":
            if action_upper in {"STATUS"}:
                skill_name = "onprem.monitoring.health"
            elif action_upper in {"ON", "OFF", "RESET"}:
                skill_name = "onprem.execute.power_action"
            else:
                skill_name = f"onprem.execute.{query_action.lower()}"

        # ── Step 1: Query Capability Registry ──────────────────────────────
        registry_url = "http://127.0.0.1:8020/agents/lookup"
        try:
            with httpx.Client(timeout=3.0) as client:
                resp = client.get(
                    registry_url,
                    params={
                        "resource_type": resource_type,
                        "provider": provider_or_protocol,
                        "skill": skill_name,
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
                "skills": [
                    {"name": "storage.monitoring.capacity"},
                    {"name": "storage.monitoring.performance"},
                    {"name": "storage.execute.volume_action"},
                    {"name": "storage.discover.arrays"},
                    {"name": "storage.diagnose.fault"}
                ] if agent_type == "storage" else [],
                "locators": [{"url": f"http://127.0.0.1:{agent_port}/openapi.json"}]
            }

        # Verify dynamic capability via Capability Registry
        if skill_name:
            agent_skills = [s.get("name").lower() for s in agent_record.get("skills", [])]
            if skill_name.lower() not in agent_skills:
                msg = f"Capability error: Operation '{query_action}' (OASF skill '{skill_name}') is not registered for {agent_type}-agent."
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
        agent_action = self._resolve_action(agent_key, query_action)

        # Build payload key name — cloud/storage/onprem use "provider"; network uses "protocol"
        if agent_key == "network":
            protocol_key = "protocol"
            prov_val = provider_or_protocol
        else:
            protocol_key = "provider"
            prov_val = "com" if (agent_key == "onprem" and provider_or_protocol == "coms") else provider_or_protocol

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

