"""Cloud Agent execution engine — wraps adapter calls with tenacity retry + error normalization."""

from __future__ import annotations
import logging
from typing import Any, Dict, Optional

from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from config.settings import settings
from core.adapter_manager import AdapterManager
from core.cred_vault_client import CredVaultClient
from core.normalization import normalize_metrics, normalize_resource_list
from core.anomaly_detection import detect_anomalies
from models.task_models import TaskRequest, TaskResponse

logger = logging.getLogger(__name__)

_vault = CredVaultClient()


def _make_retry(**kwargs):
    return retry(
        stop=stop_after_attempt(settings.RETRY_ATTEMPTS),
        wait=wait_exponential(multiplier=settings.RETRY_WAIT_SECONDS, min=1, max=10),
        retry=retry_if_exception_type(Exception),
        reraise=True,
        **kwargs,
    )


class CloudExecutionEngine:
    """
    Orchestrates the full task lifecycle:
      1. Resolve credentials from Vault
      2. Select the correct adapter
      3. Execute the adapter call (with retry)
      4. Normalize the result
      5. Run anomaly detection
      6. Return a canonical TaskResponse
    """

    def execute(self, request: TaskRequest) -> TaskResponse:
        errors: list[str] = []
        actions_taken: list[str] = []

        # ── Step 1: Resolve credentials ───────────────────────────────────────
        credentials: Dict[str, Any] = {}
        if request.credentials_ref:
            try:
                credentials = _vault.get(request.credentials_ref)
                actions_taken.append(f"Fetched credentials from vault ref '{request.credentials_ref}'.")
            except Exception as exc:
                logger.warning("Vault fetch failed for ref '%s': %s", request.credentials_ref, exc)
                errors.append(f"Credential fetch warning: {exc}")

        # ── Step 2: Select adapter ────────────────────────────────────────────
        try:
            adapter = AdapterManager.get(request.provider)
            actions_taken.append(f"Selected adapter: {adapter.provider_name}.")
        except ValueError as exc:
            return TaskResponse(
                task_id=request.task_id,
                status="failed",
                resource_type=request.resource_type,
                resource_id=request.resource_id,
                region=request.region,
                provider=request.provider,
                errors=[str(exc)],
            )

        # ── Step 3: Dispatch action ───────────────────────────────────────────
        metrics: Dict[str, Any] = {}
        action_result: Dict[str, Any] = {}

        action = request.action.lower()

        try:
            if action == "fetch_metrics":
                raw = self._fetch_metrics(adapter, request, credentials)
                metrics = normalize_metrics(raw)
                actions_taken.append("Fetched and normalized metrics.")

            elif action == "execute_action":
                action_result = self._execute_action(adapter, request, credentials)
                actions_taken.append(f"Executed action '{request.parameters.get('action_verb', 'unspecified')}'.")

            elif action == "health_check":
                action_result = self._health_check(adapter, request, credentials)
                actions_taken.append("Ran health check.")

            elif action == "discover_resources":
                raw_list = self._discover(adapter, request, credentials)
                action_result = {"resources": normalize_resource_list(raw_list)}
                actions_taken.append(f"Discovered {len(raw_list)} resources.")

            elif action == "detect_anomaly":
                raw = self._fetch_metrics(adapter, request, credentials)
                metrics = normalize_metrics(raw)
                actions_taken.append("Fetched metrics for anomaly detection.")

            else:
                errors.append(f"Unknown action '{request.action}'. Supported: fetch_metrics, execute_action, health_check, discover_resources, detect_anomaly.")

        except Exception as exc:
            logger.error("Adapter call failed: %s", exc, exc_info=True)
            errors.append(f"Adapter error: {exc}")

        # ── Step 4: Anomaly detection (runs if we have metrics) ───────────────
        anomaly_report = detect_anomalies(metrics) if metrics else None
        status_level = anomaly_report.status_level if anomaly_report else "healthy"
        insights = anomaly_report.insights if anomaly_report else []

        if anomaly_report and anomaly_report.insights:
            actions_taken.append("Anomaly detection completed — issues found.")

        # ── Step 5: Compose response ──────────────────────────────────────────
        final_metrics = {**metrics, **action_result}
        status = "failed" if errors and not final_metrics else ("success" if not errors else "partial")

        return TaskResponse(
            task_id=request.task_id,
            status=status,
            agent_type="cloud",
            resource_type=request.resource_type,
            resource_id=request.resource_id,
            region=request.region,
            provider=request.provider,
            metrics=final_metrics,
            actions_taken=actions_taken,
            status_level=status_level,
            insights=insights,
            errors=errors,
        )

    # ── Retry-wrapped adapter calls ───────────────────────────────────────────

    def _fetch_metrics(self, adapter, req: TaskRequest, creds: Dict) -> Dict:
        @_make_retry()
        def _call():
            return adapter.fetch_metrics(
                resource_id=req.resource_id,
                resource_type=req.resource_type,
                region=req.region,
                credentials=creds,
                parameters=req.parameters,
            )
        return _call()

    def _execute_action(self, adapter, req: TaskRequest, creds: Dict) -> Dict:
        @_make_retry()
        def _call():
            return adapter.execute_action(
                resource_id=req.resource_id,
                resource_type=req.resource_type,
                region=req.region,
                action=req.parameters.get("action_verb", req.action),
                credentials=creds,
                parameters=req.parameters,
            )
        return _call()

    def _health_check(self, adapter, req: TaskRequest, creds: Dict) -> Dict:
        @_make_retry()
        def _call():
            return adapter.health_check(
                resource_id=req.resource_id,
                resource_type=req.resource_type,
                region=req.region,
                credentials=creds,
                parameters=req.parameters,
            )
        return _call()

    def _discover(self, adapter, req: TaskRequest, creds: Dict) -> list:
        @_make_retry()
        def _call():
            return adapter.discover_resources(
                region=req.region,
                resource_type=req.resource_type,
                credentials=creds,
                parameters=req.parameters,
            )
        return _call()
