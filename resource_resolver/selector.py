"""
Protocol Selector
==================
Steps 3, 4, and 5 of the resolver spec.

Loads dynamic routes configuration from the routes.json files of mock servers.
"""

from __future__ import annotations

import os
import json
import logging
from typing import Union, Optional

from records import (
    Vendor, Protocol, ActionCategory,
    PowerAction, ProvisionAction,
    ResourceRecord, DeploymentType,
)
from errors import ActionClassificationError

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────────────────────
# Dynamic Route Registry Loading
# ─────────────────────────────────────────────────────────────────────────────

BASE_DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
OV_ROUTES_PATH = os.path.join(BASE_DIR, "mock_server(oneview)", "routes.json")
COM_ROUTES_PATH = os.path.join(BASE_DIR, "mock_server(Comops)", "routes.json")

ROUTE_CONFIGS: dict[str, dict] = {}

def load_route_configs():
    ROUTE_CONFIGS.clear()
    for path in [OV_ROUTES_PATH, COM_ROUTES_PATH]:
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                    protocol_str = cfg.get("protocol")
                    if protocol_str:
                        ROUTE_CONFIGS[protocol_str] = cfg
                        logger.info(f"[Selector] Loaded route config for protocol '{protocol_str}' from {path}")
            except Exception as e:
                logger.error(f"[Selector] Failed to load route config from {path}: {e}")

# Load initial configurations at startup
load_route_configs()

# Helper to map a string action name back to the Enum member
def get_action_enum(action_name: str) -> Union[PowerAction, ProvisionAction, str]:
    # Check PowerAction members
    for member in PowerAction:
        if member.value == action_name:
            return member
    # Check ProvisionAction members
    for member in ProvisionAction:
        if member.value == action_name:
            return member
    # Fallback to string if not in standard enums (fully custom actions!)
    return action_name

# ─────────────────────────────────────────────────────────────────────────────
# Public helpers
# ─────────────────────────────────────────────────────────────────────────────

def classify_action(
    query: str,
) -> tuple[ActionCategory, Union[PowerAction, ProvisionAction, str]]:
    """
    Step 4 — Classify query into Provisioning or Operational and return
    the specific action.
    """
    q = query.lower()

    # Check for explicit action override (action:Name)
    explicit_action = None
    if "action:" in q:
        parts = query.split()
        for part in parts:
            if part.lower().startswith("action:"):
                explicit_action = part.split(":", 1)[1]
                break

    if explicit_action:
        # Check category
        load_route_configs()
        provision_actions = ["Create", "Allocate", "Deallocate", "Delete"]
        category = ActionCategory.OPERATIONAL
        for protocol_cfg in ROUTE_CONFIGS.values():
            if explicit_action in protocol_cfg.get("endpoints", {}):
                endpoint = protocol_cfg["endpoints"][explicit_action]
                method = endpoint.get("method", "GET").upper()
                if explicit_action in provision_actions or method in ["POST", "DELETE"] and any(p in explicit_action.lower() for p in ["create", "delete", "allocate", "deallocate"]):
                    category = ActionCategory.PROVISIONING
                break
        return category, explicit_action

    # Check for collection listing queries first
    list_keywords = ["list", "show all", "get all", "all"]
    control_keywords = ["turn on", "power on", "turn off", "power off", "reboot", "restart", "delete", "create"]
    if any(k in q for k in list_keywords) and not any(c in q for c in control_keywords):
        return ActionCategory.OPERATIONAL, "List"

    # Reload route configs to ensure we reflect any runtime updates
    load_route_configs()

    # Group endpoints from loaded configs into Provisioning vs Operational actions
    provision_actions = ["Create", "Allocate", "Deallocate", "Delete"]
    provision_triggers = []
    operational_triggers = []

    for protocol_cfg in ROUTE_CONFIGS.values():
        for action_name, endpoint in protocol_cfg.get("endpoints", {}).items():
            triggers = endpoint.get("triggers", [])
            for trigger in triggers:
                if action_name in provision_actions:
                    provision_triggers.append((trigger, action_name))
                else:
                    operational_triggers.append((trigger, action_name))

    # Sort triggers by length descending to match longest phrase first
    provision_triggers.sort(key=lambda x: len(x[0]), reverse=True)
    operational_triggers.sort(key=lambda x: len(x[0]), reverse=True)

    # 1. Match Provisioning triggers
    for trigger, action_name in provision_triggers:
        if trigger in q:
            logger.debug(f"[Selector] Classified Provisioning action: {action_name}")
            return ActionCategory.PROVISIONING, get_action_enum(action_name)

    # 2. Match Operational triggers
    for trigger, action_name in operational_triggers:
        if trigger in q:
            logger.debug(f"[Selector] Classified Operational action: {action_name}")
            return ActionCategory.OPERATIONAL, get_action_enum(action_name)

    # Default fallback to Status
    logger.warning(f"[Selector] Could not classify query '{query}' — defaulting to Status")
    return ActionCategory.OPERATIONAL, PowerAction.STATUS


def select_protocol(
    resource: ResourceRecord,
    category: ActionCategory,
) -> tuple[Protocol, str]:
    """
    Step 5 — Protocol selection decision logic for HPE resources.
    """
    # Cloud Deployment → COMS
    if resource.deployment_type == DeploymentType.CLOUD:
        if Protocol.COMS in resource.supported_protocols:
            return Protocol.COMS, (
                f"Cloud deployment detected — COMS selected "
                f"(HPE Compute Ops API for {category.value} actions)"
            )
        raise ActionClassificationError(
            f"Cloud deployment requested for '{resource.name}' "
            f"but COMS is not supported: {[p.value for p in resource.supported_protocols]}"
        )

    # On-Premises Deployment → ONEVIEW
    if resource.deployment_type == DeploymentType.ON_PREM:
        if Protocol.ONEVIEW in resource.supported_protocols:
            return Protocol.ONEVIEW, (
                f"On-Premises deployment detected — OneView selected "
                f"(HPE OneView REST API for {category.value} actions)"
            )
        raise ActionClassificationError(
            f"On-Premises deployment requested for '{resource.name}' "
            f"but OneView is not supported: {[p.value for p in resource.supported_protocols]}"
        )

    raise ActionClassificationError(
        f"Unknown deployment type for '{resource.name}': {resource.deployment_type}"
    )


def resolve_api_call(
    resource: ResourceRecord,
    protocol: Protocol,
    action: Union[PowerAction, ProvisionAction, str],
    resource_category: str = "",
    parameters: dict = None
) -> tuple[str, str, Optional[dict]]:
    """
    Look up the dynamic API configuration for the resource and action.
    Returns (http_method, full_url, request_body).
    """
    # Force reload route configs to handle dynamic modifications
    load_route_configs()

    action_val = action.value if hasattr(action, "value") else str(action)
    
    # 1. Look up routing config for the protocol
    protocol_key = "OneView" if protocol == Protocol.ONEVIEW else "COMS"
    route_config = ROUTE_CONFIGS.get(protocol_key)
    
    if not route_config:
        # Fallback to defaults if no config file is loaded
        logger.warning(f"[Selector] Route config for {protocol_key} not found. Using defaults.")
        port = 8000 if protocol == Protocol.ONEVIEW else 8001
        route_config = {
            "base_url": f"http://localhost:{port}",
            "endpoints": {}
        }

    # 2. Get the specific endpoint info
    endpoint = route_config["endpoints"].get(action_val)
    if not endpoint:
        # Fallback to Status endpoint if the action is not registered
        endpoint = route_config["endpoints"].get("Status")
        if not endpoint:
            # Absolute minimal fallback structures
            if protocol == Protocol.ONEVIEW:
                endpoint = {"method": "GET", "path_template": "/rest/{resource_category}/{uuid}"}
            else:
                endpoint = {"method": "GET", "path_template": "/compute-ops-mgmt/v1/{resource_category}/{uuid}"}

    # 3. Clean/default resource category if empty
    if not resource_category:
        resource_category = "server-hardware" if protocol == Protocol.ONEVIEW else "servers"

    # 4. Perform dynamic path template parameter substitution
    path_template = endpoint["path_template"]
    path = path_template.replace("{resource_category}", resource_category)
    
    # Identify typical parameters that should default to resource.uuid if not overridden
    default_uuid_replacements = ["{uuid}", "{id}", "{device_id}", "{policy_id}", "{request_id}", "{webhook_id}", "{group-id}", "{location_id}"]
    for replacement in default_uuid_replacements:
        if replacement in path:
            param_key = replacement[1:-1]
            if parameters and param_key in parameters:
                path = path.replace(replacement, str(parameters[param_key]))
            else:
                path = path.replace(replacement, resource.uuid)
                
    # Replace any other custom parameters in the path
    if parameters:
        for k, v in parameters.items():
            path = path.replace(f"{{{k}}}", str(v))
            
    # Fallback to replace resource_name if any {resource_name} is left
    path = path.replace("{resource_name}", resource.name)

    base_url = route_config["base_url"]
    url = f"{base_url.rstrip('/')}/{path.lstrip('/')}"

    # 5. Perform dynamic request body parameter substitution
    body_template = endpoint.get("body_template")
    body = None
    if body_template is not None:
        try:
            body_str = json.dumps(body_template)
            body_str = body_str.replace("{resource_name}", resource.name)
            body_str = body_str.replace("{uuid}", resource.uuid)
            body = json.loads(body_str)
        except Exception as e:
            logger.error(f"[Selector] Failed to construct request body for {action_val}: {e}")
            body = body_template

    # 6. Append remaining unused parameters as query parameters
    if parameters:
        import urllib.parse
        query_params = {}
        for k, v in parameters.items():
            placeholder = f"{{{k}}}"
            if placeholder not in path_template and k not in ["resource_category", "resource_name"]:
                query_params[k] = str(v)
        if query_params:
            url_parts = urllib.parse.urlparse(url)
            existing_query = urllib.parse.parse_qs(url_parts.query)
            for k, val_list in existing_query.items():
                if k not in query_params:
                    query_params[k] = val_list[0]
            new_query_str = urllib.parse.urlencode(query_params)
            url = url_parts._replace(query=new_query_str).geturl()

    return endpoint["method"], url, body


def build_endpoint(resource: ResourceRecord, protocol: Protocol) -> str:
    """
    Deprecated: compatibility wrapper.
    """
    _, url, _ = resolve_api_call(resource, protocol, "Status")
    return url
