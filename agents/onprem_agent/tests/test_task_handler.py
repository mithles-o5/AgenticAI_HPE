import sys
import os
import pytest

# Ensure parents are on path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.task_request import TaskRequest
from core.task_handler import TaskHandler

@pytest.mark.asyncio
async def test_task_handler_success():
    handler = TaskHandler()
    request = TaskRequest(
        task_id="test-task-1",
        task_type="health_check",
        agent_type="onprem",
        resource_type="server_profile",
        resource_id="OV1-RackServer-001",
        provider="mock",
        action="health_check"
    )
    response = await handler.handle_task(request)
    assert response.task_id == "test-task-1"
    assert response.status == "success"
    assert response.status_level == "healthy"
    assert "MockServer-01" in response.insights[0]["message"]

@pytest.mark.asyncio
async def test_task_handler_default_provider_error():
    handler = TaskHandler()
    request = TaskRequest(
        task_id="test-task-2",
        task_type="health_check",
        agent_type="onprem",
        resource_type="server_profile",
        resource_id="OV1-RackServer-001",
        provider="default", # Invalid as per instruction
        action="health_check"
    )
    response = await handler.handle_task(request)
    assert response.status == "failed"
    assert "Provider must be supplied" in response.errors[0]

@pytest.mark.asyncio
async def test_task_handler_power_action():
    handler = TaskHandler()
    request = TaskRequest(
        task_id="test-task-3",
        task_type="power_on",
        agent_type="onprem",
        resource_type="server_profile",
        resource_id="OV1-RackServer-001",
        provider="mock",
        action="execute_action",
        parameters={"action_type": "power", "state": "On"}
    )
    response = await handler.handle_task(request)
    assert response.status == "success"
    assert "power_on" in response.actions_taken
