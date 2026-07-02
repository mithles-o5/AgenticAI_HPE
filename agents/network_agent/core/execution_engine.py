"""Network Agent execution engine — fully dynamic API routing.

Action dispatch table
---------------------
action              adapter method          api_path pattern (mock_network)
------------------  ----------------------  ----------------------------------------
fetch_metrics       fetch_interface_metrics /network/v1/devices/{id}
                                            /monitoring/v1/switches        (fleet)
execute_config_push push_config             /network/v1/devices/{id}/vlans
                                            /monitoring/v1/switches/{id}/vlan
execute_action      execute_action          /network/v1/devices/{id}/power (ON/OFF)
                                            /network/v1/devices/{id}/ports/{p}/status
discover_topology   discover_neighbors      /network/v1/devices            (all)
                                            /monitoring/v1/switches        (switches)
health_check        health_check            /network/v1/devices/{id}
                                            /monitoring/v1/switches/{id}
detect_fault        fetch + anomaly         /network/v1/devices/{id}
"""

from __future__ import annotations
import logging
from typing import Any, Dict, List

from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from config.settings import settings
from core.adapter_manager import NetworkAdapterManager
from core.cred_vault_client import CredVaultClient
from core.normalization import normalize_interface_metrics, normalize_neighbor_list
from core.anomaly_detection import detect_network_anomalies
from core.topology_builder import TopologyBuilder
from models.task_models import NetworkTaskRequest, NetworkTaskResponse

logger = logging.getLogger(__name__)
_vault = CredVaultClient()

# ── Default API path templates per action ──────────────────────────────────────
# These are only used when the orchestrator does NOT supply an api_path.
_MOCK_DEFAULT_PATHS: Dict[str, str] = {
    "fetch_metrics":        "/network/v1/devices/{id}",
    "execute_config_push":  "/network/v1/devices/{id}/vlans",
    "execute_action":       "/network/v1/devices/{id}/power",
    "discover_topology":    "/network/v1/devices",
    "health_check":         "/network/v1/devices/{id}",
    "detect_fault":         "/network/v1/devices/{id}",
    "list_resources":       "/network/v1/devices",
    "list":                 "/network/v1/devices",
}


def _retry():
    return retry(
        stop=stop_after_attempt(settings.RETRY_ATTEMPTS),
        wait=wait_exponential(multiplier=settings.RETRY_WAIT_SECONDS, min=1, max=10),
        retry=retry_if_exception_type(Exception),
        reraise=True,
    )


class NetworkExecutionEngine:

    def execute(self, request: NetworkTaskRequest) -> NetworkTaskResponse:
        errors: List[str] = []
        actions: List[str] = []
        metrics: Dict[str, Any] = {}

        # ── Step 1: Credentials ──────────────────────────────────────────────
        credentials: Dict[str, Any] = {}
        if request.credentials_ref:
            try:
                credentials = _vault.get(request.credentials_ref)
                actions.append(f"Fetched credentials for ref '{request.credentials_ref}'.")
            except Exception as exc:
                errors.append(f"Credential fetch warning: {exc}")

        # ── Step 2: Select adapter ───────────────────────────────────────────
        try:
            adapter = NetworkAdapterManager.get(request.protocol)
            actions.append(f"Selected protocol adapter: {adapter.protocol_name}.")
        except ValueError as exc:
            return NetworkTaskResponse(
                task_id=request.task_id, status="failed",
                resource_type=request.resource_type, resource_id=request.resource_id,
                region=request.region, protocol=request.protocol, errors=[str(exc)],
            )

        # ── Step 2.5: Ensure api_path is present in parameters ───────────────
        parameters = dict(request.parameters)
        if not parameters.get("api_path"):
            action_lower = request.action.lower()
            default_path = _MOCK_DEFAULT_PATHS.get(action_lower, "/network/v1/devices/{id}")
            parameters["api_path"] = default_path
            logger.info(
                "[NetworkEngine] No api_path supplied — using default: %s", default_path
            )

        # ── Step 3: Dispatch ─────────────────────────────────────────────────
        topology_nodes = []
        action = request.action.lower()
        status_level = "healthy"
        insights: List[str] = []

        try:
            if action == "fetch_metrics":
                raw = self._fetch(adapter, request, credentials, parameters)
                # raw is always a list after adapter normalization
                if not isinstance(raw, list):
                    raw = [raw] if isinstance(raw, dict) else []
                norm = normalize_interface_metrics(raw)
                metrics = {"interfaces": norm}
                actions.append(f"Fetched metrics for {len(norm)} interface(s)/device(s).")
                anomaly_report = detect_network_anomalies(norm)
                status_level = anomaly_report.status_level
                insights = anomaly_report.insights

            elif action == "execute_config_push":
                result = self._push_config(adapter, request, credentials, parameters)
                metrics = result if isinstance(result, dict) else {"result": result}
                actions.append("Config push executed.")
                status_level = "healthy"

            elif action == "execute_action":
                result = self._execute_action(adapter, request, credentials, parameters)
                metrics = result if isinstance(result, dict) else {"result": result}
                action_verb = parameters.get("action_verb", "unspecified")
                actions.append(f"Action '{action_verb}' executed.")
                status_level = "healthy"
                # Check if device came back healthy after power action
                if isinstance(result, dict):
                    ps = result.get("power_state", "")
                    hs = result.get("health_status", result.get("status", ""))
                    if ps:
                        actions.append(f"Power state now: {ps}")
                    if hs and hs.upper() in {"CRITICAL", "FAILED", "ERROR"}:
                        status_level = "critical"

            elif action == "discover_topology":
                raw_neighbors = self._discover(adapter, request, credentials, parameters)
                if not isinstance(raw_neighbors, list):
                    raw_neighbors = [raw_neighbors] if isinstance(raw_neighbors, dict) else []
                norm_neighbors = normalize_neighbor_list(raw_neighbors)
                builder = TopologyBuilder()
                builder.add_device(
                    request.resource_id,
                    {"hostname": request.resource_id, "device_type": request.resource_type},
                )
                builder.add_neighbors(request.resource_id, norm_neighbors)
                topology_nodes = builder.to_oasf_topology()
                metrics = builder.to_dict()
                actions.append(f"Topology discovered: {len(norm_neighbors)} peer(s).")
                status_level = "healthy"

            elif action == "health_check":
                result = self._health(adapter, request, credentials, parameters)
                metrics = result if isinstance(result, dict) else {"result": result}
                if isinstance(result, dict):
                    status_level = "healthy" if result.get("healthy") else "critical"
                    detail = result.get("detail", "")
                    if not result.get("healthy"):
                        insights = [str(detail) if detail else "Health check returned unhealthy."]
                else:
                    status_level = "healthy"
                actions.append("Health check completed.")

            elif action == "detect_fault":
                raw = self._fetch(adapter, request, credentials, parameters)
                if not isinstance(raw, list):
                    raw = [raw] if isinstance(raw, dict) else []
                norm = normalize_interface_metrics(raw)
                anomaly_report = detect_network_anomalies(norm)
                metrics = {"interfaces": norm}
                status_level = anomaly_report.status_level
                insights = anomaly_report.insights
                actions.append(
                    f"Fault detection scan completed — "
                    f"{len(anomaly_report.insights)} issue(s) found."
                )

            elif action in ("list", "list_resources"):
                result = self._list_resources(adapter, request, credentials, parameters)
                if isinstance(result, dict) and "devices" in result:
                    inventory = result.get("devices", [])
                    metrics = {"inventory": inventory}
                    actions.append(f"Listed {len(inventory)} resources.")
                    status_level = "healthy"
                else:
                    errors.append(f"Failed to list resources: {result}")

            else:
                errors.append(f"Unknown action '{request.action}'.")

        except Exception as exc:
            logger.exception("Adapter error for task '%s'", request.task_id)
            errors.append(f"Adapter error: {exc}")
            status_level = "healthy"

        status = (
            "failed"
            if (errors and not metrics)
            else ("success" if not errors else "partial")
        )

        return NetworkTaskResponse(
            task_id=request.task_id,
            status=status,
            agent_type="network",
            resource_type=request.resource_type,
            resource_id=request.resource_id,
            region=request.region,
            protocol=request.protocol,
            metrics=metrics,
            topology=topology_nodes,
            actions_taken=actions,
            status_level=status_level,
            insights=insights,
            errors=errors,
        )

    # ── Private helpers ───────────────────────────────────────────────────────

    def _fetch(self, adapter, req, creds, params):
        @_retry()
        def _c():
            return adapter.fetch_interface_metrics(req.resource_id, creds, params)
        return _c()

    def _push_config(self, adapter, req, creds, params):
        config = params.get("config", params.get("payload", {}))
        @_retry()
        def _c():
            return adapter.push_config(req.resource_id, config, creds, params)
        return _c()

    def _execute_action(self, adapter, req, creds, params):
        action_verb = params.get("action_verb", req.action)
        @_retry()
        def _c():
            return adapter.execute_action(req.resource_id, action_verb, creds, params)
        return _c()

    def _discover(self, adapter, req, creds, params):
        @_retry()
        def _c():
            return adapter.discover_neighbors(req.resource_id, creds, params)
        return _c()

    def _health(self, adapter, req, creds, params):
        @_retry()
        def _c():
            return adapter.health_check(req.resource_id, creds, params)
        return _c()

    def _list_resources(self, adapter, req, creds, params):
        @_retry()
        def _call():
            params["resource_type"] = req.resource_type
            skip = params.get("skip", 0)
            limit = params.get("limit", 10)
            return adapter.list_resources(creds, params, skip=skip, limit=limit)
        return _call()
