"""Storage Agent execution engine."""

from __future__ import annotations
import logging
from typing import Any, Dict

from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from config.settings import settings
from core.adapter_manager import StorageAdapterManager
from core.cred_vault_client import CredVaultClient
from core.normalization import normalize_capacity, normalize_performance, normalize_array_list
from core.anomaly_detection import detect_storage_anomalies
from models.task_models import StorageTaskRequest, StorageTaskResponse

logger = logging.getLogger(__name__)
_vault = CredVaultClient()


def _retry():
    return retry(
        stop=stop_after_attempt(settings.RETRY_ATTEMPTS),
        wait=wait_exponential(multiplier=settings.RETRY_WAIT_SECONDS, min=1, max=10),
        retry=retry_if_exception_type(Exception),
        reraise=True,
    )


class StorageExecutionEngine:
    def execute(self, request: StorageTaskRequest) -> StorageTaskResponse:
        errors, actions = [], []
        metrics: Dict[str, Any] = {}

        # Credentials
        credentials: Dict[str, Any] = {}
        if request.credentials_ref:
            try:
                credentials = _vault.get(request.credentials_ref)
                actions.append(f"Fetched credentials for ref '{request.credentials_ref}'.")
            except Exception as exc:
                errors.append(f"Credential fetch warning: {exc}")

        # Select adapter
        try:
            adapter = StorageAdapterManager.get(request.provider)
            actions.append(f"Selected storage adapter: {adapter.provider_name}.")
        except ValueError as exc:
            return StorageTaskResponse(
                task_id=request.task_id, status="failed",
                resource_type=request.resource_type, resource_id=request.resource_id,
                region=request.region, provider=request.provider, errors=[str(exc)],
            )

        action = request.action.lower()
        status_level = "healthy"
        insights = []

        try:
            if action == "fetch_capacity":
                raw = self._fetch_capacity(adapter, request, credentials)
                metrics["capacity"] = normalize_capacity(raw)
                actions.append("Fetched and normalized capacity metrics.")

            elif action == "fetch_performance":
                raw = self._fetch_perf(adapter, request, credentials)
                metrics["performance"] = normalize_performance(raw)
                actions.append("Fetched and normalized performance metrics.")

            elif action in {"fetch_capacity_and_performance", "poll"}:
                cap_raw  = self._fetch_capacity(adapter, request, credentials)
                perf_raw = self._fetch_perf(adapter, request, credentials)
                cap  = normalize_capacity(cap_raw)
                perf = normalize_performance(perf_raw)
                metrics = {"capacity": cap, "performance": perf}
                anomaly_report = detect_storage_anomalies(cap, perf)
                status_level = anomaly_report.status_level
                insights = anomaly_report.insights
                actions.append("Fetched capacity + performance; anomaly detection ran.")

            elif action == "execute_action":
                result = self._execute(adapter, request, credentials)
                metrics = result
                actions.append(f"Action '{request.parameters.get('action_verb', 'unspecified')}' executed.")

            elif action == "discover_arrays":
                raw = self._discover(adapter, request, credentials)
                metrics = {"arrays": normalize_array_list(raw)}
                actions.append(f"Discovered {len(raw)} arrays.")

            elif action == "health_check":
                result = self._health(adapter, request, credentials)
                metrics = result
                status_level = "healthy" if result.get("healthy") else "critical"
                insights = [] if result.get("healthy") else [result.get("detail", "Health check failed.")]
                actions.append("Health check completed.")

            elif action in ("list", "list_resources"):
                result = self._list_resources(adapter, request, credentials)
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

        status = "failed" if (errors and not metrics) else ("success" if not errors else "partial")
        return StorageTaskResponse(
            task_id=request.task_id, status=status, agent_type="storage",
            resource_type=request.resource_type, resource_id=request.resource_id,
            region=request.region, provider=request.provider,
            metrics=metrics, actions_taken=actions,
            status_level=status_level, insights=insights, errors=errors,
        )

    def _fetch_capacity(self, adapter, req, creds):
        @_retry()
        def _c(): return adapter.fetch_capacity(req.resource_id, req.resource_type, creds, req.parameters)
        return _c()

    def _fetch_perf(self, adapter, req, creds):
        @_retry()
        def _c(): return adapter.fetch_performance(req.resource_id, req.resource_type, creds, req.parameters)
        return _c()

    def _execute(self, adapter, req, creds):
        @_retry()
        def _c(): return adapter.execute_action(req.resource_id, req.resource_type, req.parameters.get("action_verb", req.action), creds, req.parameters)
        return _c()

    def _discover(self, adapter, req, creds):
        @_retry()
        def _c(): return adapter.discover_arrays(creds, req.parameters)
        return _c()

    def _health(self, adapter, req, creds):
        @_retry()
        def _c(): return adapter.health_check(req.resource_id, req.resource_type, creds, req.parameters)
        return _c()

    def _list_resources(self, adapter, req, creds):
        @_retry()
        def _c():
            req.parameters["resource_type"] = req.resource_type
            skip = req.parameters.get("skip", 0)
            limit = req.parameters.get("limit", 10)
            return adapter.list_resources(creds, req.parameters, skip=skip, limit=limit)
        return _c()
