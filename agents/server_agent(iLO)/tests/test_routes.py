import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_health():
    resp = client.get("/server-agent/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["agent"] == "server-agent"
    assert data["status"] == "healthy"

def test_execute_task_valid():
    payload = {
        "task_id": "t-route-1",
        "task_type": "monitoring",
        "resource_type": "server",
        "resource_id": "OV1-RackServer-001",
        "action": "fetch_metrics",
        "provider": "default",
        "credentials_ref": "mock"
    }
    resp = client.post("/server-agent/execute-task", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "success"
    assert data["metrics"]["cpu_utilization"] == 54.0

def test_execute_task_invalid():
    # Invalid action type or missing required fields
    payload = {
        "task_id": "t-route-2",
        "resource_id": "OV1-RackServer-001"
    }
    resp = client.post("/server-agent/execute-task", json=payload)
    assert resp.status_code == 422

def test_get_inventory():
    resp = client.get("/server-agent/inventory/OV1-RackServer-001?provider=default&credentials_ref=mock")
    assert resp.status_code == 200
    data = resp.json()
    assert "cpus" in data
    assert "memory" in data
    assert len(data["cpus"]) > 0

def test_poll_trigger():
    resp = client.post("/server-agent/poll/trigger")
    assert resp.status_code == 200
    data = resp.json()
    assert "polled" in data
    assert data["polled"] > 0
