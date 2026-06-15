import sys
import os
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

client = TestClient(app)

def test_health_route():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "healthy", "service": "onprem-agent"}

def test_tasks_route_success():
    payload = {
        "task_id": "route-test-1",
        "task_type": "monitoring",
        "agent_type": "onprem",
        "resource_type": "server_profile",
        "resource_id": "OV-Server-001",
        "provider": "mock",
        "action": "health_check"
    }
    resp = client.post("/tasks", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["task_id"] == "route-test-1"
    assert data["status"] == "success"
    assert data["status_level"] == "healthy"

def test_tasks_route_validation_error():
    payload = {
        "task_id": "route-test-2",
        "task_type": "monitoring",
        # missing agent_type which gets defaults
        # missing action which is required
        "provider": "mock"
    }
    resp = client.post("/tasks", json=payload)
    # FastAPI automatically validates and returns 422 Unprocessable Entity
    assert resp.status_code == 422
