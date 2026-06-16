"""Cloud Agent tests — task handler, normalization, anomaly detection, routes."""

import sys
import os

# Ensure agent root is on path for all test imports
_AGENT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _AGENT_ROOT not in sys.path:
    sys.path.insert(0, _AGENT_ROOT)

import pytest
from fastapi.testclient import TestClient

from main import app
from models.task_models import TaskRequest, TaskResponse
from core.normalization import normalize_metrics
from core.anomaly_detection import detect_anomalies, AnomalyRule
from core.execution_engine import CloudExecutionEngine

client = TestClient(app)


# ── Normalization tests ────────────────────────────────────────────────────────

def test_normalize_metrics_known_alias():
    raw = {"CPUUtilization": 45.0, "MemoryUtilization": 60.0}
    norm = normalize_metrics(raw)
    assert norm["cpu_utilization_pct"] == 45.0
    assert norm["memory_utilization_pct"] == 60.0


def test_normalize_metrics_unknown_key_preserved():
    raw = {"my_custom_metric": 99}
    norm = normalize_metrics(raw)
    assert norm["my_custom_metric"] == 99


def test_normalize_metrics_canonical_key_unchanged():
    raw = {"cpu_utilization_pct": 50.0}
    norm = normalize_metrics(raw)
    assert norm["cpu_utilization_pct"] == 50.0


# ── Anomaly detection tests ────────────────────────────────────────────────────

def test_anomaly_healthy():
    metrics = {"cpu_utilization_pct": 30.0, "memory_utilization_pct": 40.0}
    report = detect_anomalies(metrics)
    assert report.status_level == "healthy"
    assert len(report.insights) == 0


def test_anomaly_warning_cpu():
    metrics = {"cpu_utilization_pct": 80.0, "memory_utilization_pct": 30.0}
    report = detect_anomalies(metrics)
    assert report.status_level == "warning"
    assert any("cpu" in i.lower() for i in report.insights)


def test_anomaly_critical_cpu():
    metrics = {"cpu_utilization_pct": 95.0, "memory_utilization_pct": 30.0}
    report = detect_anomalies(metrics)
    assert report.status_level == "critical"


def test_anomaly_missing_metric_skipped():
    metrics = {}    # no metrics at all
    report = detect_anomalies(metrics)
    assert report.status_level == "healthy"


def test_anomaly_custom_rule():
    rule = AnomalyRule(metric="my_metric", warning_level=50.0, critical_level=80.0, unit="units")
    metrics = {"my_metric": 55.0}
    report = detect_anomalies(metrics, rules=[rule])
    assert report.status_level == "warning"


# ── Execution engine (mock adapter) ───────────────────────────────────────────

def test_engine_fetch_metrics():
    engine = CloudExecutionEngine()
    req = TaskRequest(
        task_id="t-001",
        task_type="monitoring",
        resource_type="vm",
        resource_id="mock-vm-001",
        provider="mock",
        action="fetch_metrics",
    )
    resp = engine.execute(req)
    assert resp.task_id == "t-001"
    assert resp.status == "success"
    assert "cpu_utilization_pct" in resp.metrics


def test_engine_health_check():
    engine = CloudExecutionEngine()
    req = TaskRequest(
        task_id="t-002",
        task_type="health_check",
        resource_type="vm",
        resource_id="mock-vm-002",
        provider="mock",
        action="health_check",
    )
    resp = engine.execute(req)
    assert resp.status in {"success", "partial"}
    assert "healthy" in resp.metrics


def test_engine_discover_resources():
    engine = CloudExecutionEngine()
    req = TaskRequest(
        task_id="t-003",
        task_type="discovery",
        resource_type="vm",
        resource_id="n/a",
        provider="mock",
        action="discover_resources",
        parameters={"limit": 3},
    )
    resp = engine.execute(req)
    assert resp.status == "success"
    assert "resources" in resp.metrics
    assert len(resp.metrics["resources"]) == 3


def test_engine_unknown_provider():
    engine = CloudExecutionEngine()
    req = TaskRequest(
        task_id="t-004",
        task_type="monitoring",
        resource_type="vm",
        resource_id="any",
        provider="nonexistent-cloud",
        action="fetch_metrics",
    )
    resp = engine.execute(req)
    assert resp.status == "failed"
    assert resp.errors


# ── API route tests ────────────────────────────────────────────────────────────

def test_health_endpoint():
    r = client.get("/cloud-agent/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    assert "mock" in data["providers"]


def test_providers_endpoint():
    r = client.get("/cloud-agent/providers")
    assert r.status_code == 200
    providers = r.json()["providers"]
    assert set(providers) >= {"mock", "aws", "azure", "gcp"}


def test_execute_task_endpoint():
    payload = {
        "task_id": "route-t-001",
        "task_type": "monitoring",
        "resource_type": "vm",
        "resource_id": "mock-vm-route-01",
        "provider": "mock",
        "action": "fetch_metrics",
    }
    r = client.post("/cloud-agent/execute-task", json=payload)
    assert r.status_code == 200
    body = r.json()
    assert body["task_id"] == "route-t-001"
    assert body["status"] == "success"


def test_execute_task_endpoint_invalid_provider():
    payload = {
        "task_id": "route-t-002",
        "task_type": "monitoring",
        "resource_type": "vm",
        "resource_id": "vm-01",
        "provider": "bad-provider",
        "action": "fetch_metrics",
    }
    r = client.post("/cloud-agent/execute-task", json=payload)
    assert r.status_code == 200        # agent returns 200 with failed status in body
    assert r.json()["status"] == "failed"
