"""Storage Agent test suite."""

import sys
import os

_AGENT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _AGENT_ROOT not in sys.path:
    sys.path.insert(0, _AGENT_ROOT)

import pytest
from fastapi.testclient import TestClient

from main import app
from core.normalization import normalize_capacity, normalize_performance, normalize_array_list
from core.anomaly_detection import detect_storage_anomalies
from core.execution_engine import StorageExecutionEngine
from models.task_models import StorageTaskRequest

client = TestClient(app)


# ── Normalization ──────────────────────────────────────────────────────────────

def test_normalize_capacity_alias():
    raw = {"totalCapacityTiB": 100.0, "usedCapacityTiB": 60.0, "freeCapacityTiB": 40.0, "utilizationPercent": 60.0}
    norm = normalize_capacity(raw)
    assert norm["total_tb"] == 100.0
    assert norm["utilization_pct"] == 60.0


def test_normalize_performance_alias():
    raw = {"readIOPS": 5000, "writeIOPS": 3000, "readLatencyMs": 2.5}
    norm = normalize_performance(raw)
    assert norm["read_iops"] == 5000
    assert norm["read_latency_ms"] == 2.5


def test_normalize_array_list():
    raw = [{"id": "a-001", "name": "Array-1", "type": "SAN", "status": "online", "capacity_tb": 50.0}]
    norm = normalize_array_list(raw)
    assert norm[0]["id"] == "a-001"
    assert norm[0]["capacity_tb"] == 50.0


# ── Anomaly detection ──────────────────────────────────────────────────────────

def test_storage_anomaly_healthy():
    cap  = {"utilization_pct": 50.0, "total_tb": 100.0, "used_tb": 50.0}
    perf = {"read_iops": 100, "write_iops": 100, "read_latency_ms": 1.0, "write_latency_ms": 1.0}
    report = detect_storage_anomalies(cap, perf)
    assert report.status_level == "healthy"


def test_storage_anomaly_critical_capacity():
    cap  = {"utilization_pct": 95.0}
    perf = {}
    report = detect_storage_anomalies(cap, perf)
    assert report.status_level == "critical"
    assert any("CRITICAL" in i for i in report.insights)


def test_storage_anomaly_high_latency():
    cap  = {}
    perf = {"read_latency_ms": 60.0, "write_latency_ms": 1.0}
    report = detect_storage_anomalies(cap, perf)
    assert report.status_level in {"warning", "critical"}


# ── Execution engine ───────────────────────────────────────────────────────────

def test_engine_fetch_capacity():
    engine = StorageExecutionEngine()
    req = StorageTaskRequest(
        task_id="s-001", task_type="monitoring",
        resource_type="volume", resource_id="mock-vol-001",
        provider="mock", action="fetch_capacity",
    )
    resp = engine.execute(req)
    assert resp.status == "success"
    assert "capacity" in resp.metrics
    assert "utilization_pct" in resp.metrics["capacity"]


def test_engine_fetch_performance():
    engine = StorageExecutionEngine()
    req = StorageTaskRequest(
        task_id="s-002", task_type="monitoring",
        resource_type="volume", resource_id="mock-vol-002",
        provider="mock", action="fetch_performance",
    )
    resp = engine.execute(req)
    assert resp.status == "success"
    assert "performance" in resp.metrics


def test_engine_discover_arrays():
    engine = StorageExecutionEngine()
    req = StorageTaskRequest(
        task_id="s-003", task_type="discovery",
        resource_type="array", resource_id="n/a",
        provider="mock", action="discover_arrays",
        parameters={"limit": 2},
    )
    resp = engine.execute(req)
    assert resp.status == "success"
    assert len(resp.metrics.get("arrays", [])) == 2


def test_engine_unknown_provider():
    engine = StorageExecutionEngine()
    req = StorageTaskRequest(
        task_id="s-004", task_type="monitoring",
        resource_type="volume", resource_id="any",
        provider="bad-provider", action="fetch_capacity",
    )
    resp = engine.execute(req)
    assert resp.status == "failed"
    assert resp.errors


def test_engine_poll():
    engine = StorageExecutionEngine()
    req = StorageTaskRequest(
        task_id="s-005", task_type="poll",
        resource_type="volume", resource_id="mock-vol-005",
        provider="mock", action="poll",
    )
    resp = engine.execute(req)
    assert resp.status in {"success", "partial"}
    assert "capacity" in resp.metrics
    assert "performance" in resp.metrics


# ── API routes ─────────────────────────────────────────────────────────────────

def test_health_endpoint():
    r = client.get("/storage-agent/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"
    assert "mock" in r.json()["providers"]


def test_providers_endpoint():
    r = client.get("/storage-agent/providers")
    assert r.status_code == 200
    providers = r.json()["providers"]
    assert set(providers) >= {"mock", "dscc", "nas", "s3"}


def test_execute_task_endpoint():
    payload = {
        "task_id": "sr-001",
        "task_type": "monitoring",
        "resource_type": "volume",
        "resource_id": "mock-vol-route-01",
        "provider": "mock",
        "action": "fetch_capacity",
    }
    r = client.post("/storage-agent/execute-task", json=payload)
    assert r.status_code == 200
    assert r.json()["status"] == "success"
