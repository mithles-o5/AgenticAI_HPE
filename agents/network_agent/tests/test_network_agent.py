"""Network Agent test suite."""

import sys
import os

_AGENT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _AGENT_ROOT not in sys.path:
    sys.path.insert(0, _AGENT_ROOT)

import pytest
from fastapi.testclient import TestClient

from main import app
from core.normalization import normalize_interface_metrics, normalize_neighbor_list
from core.anomaly_detection import detect_network_anomalies
from core.topology_builder import TopologyBuilder
from core.execution_engine import NetworkExecutionEngine
from models.task_models import NetworkTaskRequest

client = TestClient(app)


# ── Normalization ──────────────────────────────────────────────────────────────

def test_normalize_interface_known_alias():
    raw = [{"ifName": "Gi0/0", "operStatus": "up", "utilPercent": 45.0}]
    norm = normalize_interface_metrics(raw)
    assert norm[0]["name"] == "Gi0/0"
    assert norm[0]["status"] == "up"


def test_normalize_neighbor():
    raw = [{"remoteDeviceId": "sw-002", "remotePort": "Gi0/1", "localPort": "Gi0/2"}]
    norm = normalize_neighbor_list(raw)
    assert norm[0]["neighbor_id"] == "sw-002"


# ── Anomaly detection ──────────────────────────────────────────────────────────

def test_network_anomaly_healthy():
    interfaces = [{"name": "Gi0/0", "status": "up", "utilization_pct": 20.0, "in_errors": 0, "out_errors": 0}]
    report = detect_network_anomalies(interfaces)
    assert report.status_level == "healthy"


def test_network_anomaly_high_util():
    interfaces = [{"name": "Gi0/0", "status": "up", "utilization_pct": 95.0, "in_errors": 0, "out_errors": 0}]
    report = detect_network_anomalies(interfaces)
    assert report.status_level == "critical"


def test_network_anomaly_down_interface():
    interfaces = [{"name": "Gi0/1", "status": "down", "utilization_pct": 0.0, "in_errors": 0, "out_errors": 0}]
    report = detect_network_anomalies(interfaces)
    assert report.status_level in {"warning", "critical"}
    assert any("DOWN" in i for i in report.insights)


# ── Topology builder ───────────────────────────────────────────────────────────

def test_topology_builder_basic():
    builder = TopologyBuilder()
    builder.add_device("sw-001", {"hostname": "switch-1", "device_type": "switch"})
    builder.add_neighbors("sw-001", [
        {"neighbor_id": "sw-002", "local_port": "Gi0/1", "neighbor_port": "Gi0/2"}
    ])
    topo = builder.to_oasf_topology()
    assert any(n["node_id"] == "sw-001" for n in topo)
    assert any(n["node_id"] == "sw-002" for n in topo)


def test_topology_to_dict():
    builder = TopologyBuilder()
    builder.add_device("r-001", {"hostname": "router-1", "device_type": "router"})
    d = builder.to_dict()
    assert "nodes" in d
    assert "edges" in d


# ── Execution engine ───────────────────────────────────────────────────────────

def test_engine_fetch_metrics():
    engine = NetworkExecutionEngine()
    req = NetworkTaskRequest(
        task_id="n-001", task_type="monitoring",
        resource_type="switch", resource_id="sw-mock-001",
        protocol="mock", action="fetch_metrics",
    )
    resp = engine.execute(req)
    assert resp.task_id == "n-001"
    assert resp.status == "success"
    assert "interfaces" in resp.metrics


def test_engine_discover_topology():
    engine = NetworkExecutionEngine()
    req = NetworkTaskRequest(
        task_id="n-002", task_type="discovery",
        resource_type="switch", resource_id="sw-mock-002",
        protocol="mock", action="discover_topology",
    )
    resp = engine.execute(req)
    assert resp.status == "success"
    assert len(resp.topology) > 0


def test_engine_health_check():
    engine = NetworkExecutionEngine()
    req = NetworkTaskRequest(
        task_id="n-003", task_type="health_check",
        resource_type="switch", resource_id="sw-mock-003",
        protocol="mock", action="health_check",
    )
    resp = engine.execute(req)
    assert resp.status in {"success", "partial"}


# ── API routes ─────────────────────────────────────────────────────────────────

def test_health_endpoint():
    r = client.get("/network-agent/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"
    assert "mock" in r.json()["protocols"]


def test_execute_task_endpoint():
    payload = {
        "task_id": "nr-001",
        "task_type": "monitoring",
        "resource_type": "switch",
        "resource_id": "sw-mock-route-01",
        "protocol": "mock",
        "action": "fetch_metrics",
    }
    r = client.post("/network-agent/execute-task", json=payload)
    assert r.status_code == 200
    assert r.json()["task_id"] == "nr-001"
    assert r.json()["status"] == "success"
