"""Network Agent execution engine."""

from __future__ import annotations
import logging
from typing import Any, Dict

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


def _retry():
    return retry(
        stop=stop_after_attempt(settings.RETRY_ATTEMPTS),
        wait=wait_exponential(multiplier=settings.RETRY_WAIT_SECONDS, min=1, max=10),
        retry=retry_if_exception_type(Exception),
        reraise=True,
    )


class NetworkExecutionEngine:
    def execute(self, request: NetworkTaskRequest) -> NetworkTaskResponse:
        errors: list[str] = []
        actions: list[str] = []
        metrics: Dict[str, Any] = {}

        # Step 1: Credentials
        credentials: Dict[str, Any] = {}
        if request.credentials_ref:
            try:
                credentials = _vault.get(request.credentials_ref)
                actions.append(f"Fetched credentials for ref '{request.credentials_ref}'.")
            except Exception as exc:
                errors.append(f"Credential fetch warning: {exc}")

        # Step 2: Select adapter
        try:
            adapter = NetworkAdapterManager.get(request.protocol)
            actions.append(f"Selected protocol adapter: {adapter.protocol_name}.")
        except ValueError as exc:
            return NetworkTaskResponse(
                task_id=request.task_id, status="failed",
                resource_type=request.resource_type, resource_id=request.resource_id,
                region=request.region, protocol=request.protocol, errors=[str(exc)],
            )

        # Step 3: Dispatch
        topology_nodes = []
        action = request.action.lower()

        try:
            if action == "fetch_metrics":
                raw = self._fetch(adapter, request, credentials)
                norm = normalize_interface_metrics(raw)
                metrics = {"interfaces": norm}
                actions.append(f"Fetched metrics for {len(norm)} interfaces.")

                # Anomaly detection
                anomaly_report = detect_network_anomalies(norm)
                status_level = anomaly_report.status_level
                insights = anomaly_report.insights

            elif action == "execute_config_push":
                result = self._push_config(adapter, request, credentials)
                metrics = result
                actions.append("Config push executed.")
                status_level = "healthy"
                insights = []

            elif action == "execute_action":
                result = self._execute_action(adapter, request, credentials)
                metrics = result
                actions.append(f"Action '{request.parameters.get('action_verb', 'unspecified')}' executed.")
                status_level = "healthy"
                insights = []

            elif action == "discover_topology":
                raw_neighbors = self._discover(adapter, request, credentials)
                norm_neighbors = normalize_neighbor_list(raw_neighbors)
                builder = TopologyBuilder()
                builder.add_device(request.resource_id, {"hostname": request.resource_id, "device_type": request.resource_type})
                builder.add_neighbors(request.resource_id, norm_neighbors)
                topology_nodes = builder.to_oasf_topology()
                metrics = builder.to_dict()
                actions.append(f"Topology discovered: {len(norm_neighbors)} neighbors.")
                status_level = "healthy"
                insights = []

            elif action == "health_check":
                result = self._health(adapter, request, credentials)
                metrics = result
                status_level = "healthy" if result.get("healthy") else "critical"
                insights = [] if result.get("healthy") else [result.get("detail", "Health check failed.")]
                actions.append("Health check completed.")

            elif action == "detect_fault":
                raw = self._fetch(adapter, request, credentials)
                norm = normalize_interface_metrics(raw)
                anomaly_report = detect_network_anomalies(norm)
                metrics = {"interfaces": norm}
                status_level = anomaly_report.status_level
                insights = anomaly_report.insights
                actions.append("Fault detection scan completed.")

            else:
                errors.append(f"Unknown action '{request.action}'.")
                status_level = "healthy"
                insights = []

        except Exception as exc:
            logger.exception("Adapter error for task '%s'", request.task_id)
            errors.append(f"Adapter error: {exc}")
            status_level = "healthy"
            insights = []

        status = "failed" if (errors and not metrics) else ("success" if not errors else "partial")
        return NetworkTaskResponse(
            task_id=request.task_id, status=status, agent_type="network",
            resource_type=request.resource_type, resource_id=request.resource_id,
            region=request.region, protocol=request.protocol,
            metrics=metrics, topology=topology_nodes,
            actions_taken=actions, status_level=status_level,
            insights=insights, errors=errors,
        )

    def _fetch(self, adapter, req, creds):
        @_retry()
        def _c(): return adapter.fetch_interface_metrics(req.resource_id, creds, req.parameters)
        return _c()

    def _push_config(self, adapter, req, creds):
        @_retry()
        def _c(): return adapter.push_config(req.resource_id, req.parameters.get("config", {}), creds, req.parameters)
        return _c()

    def _execute_action(self, adapter, req, creds):
        @_retry()
        def _c(): return adapter.execute_action(req.resource_id, req.parameters.get("action_verb", req.action), creds, req.parameters)
        return _c()

    def _discover(self, adapter, req, creds):
        @_retry()
        def _c(): return adapter.discover_neighbors(req.resource_id, creds, req.parameters)
        return _c()

    def _health(self, adapter, req, creds):
        @_retry()
        def _c(): return adapter.health_check(req.resource_id, creds, req.parameters)
        return _c()
