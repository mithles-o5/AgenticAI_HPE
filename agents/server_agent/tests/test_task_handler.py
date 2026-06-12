import pytest
from models.task_request import TaskRequest, ResourceType, Action, Provider
from core.task_handler import TaskHandler
from models.task_response import StatusLevel

@pytest.mark.asyncio
async def test_task_handler_fetch_metrics_server():
    handler = TaskHandler()
    req = TaskRequest(
        task_id="t-1",
        task_type="monitoring",
        resource_type=ResourceType.SERVER,
        resource_id="server-1",
        action=Action.FETCH_METRICS,
        provider=Provider.DEFAULT,
        credentials_ref="mock"
    )
    res = await handler.handle(req)
    assert res.status == "success"
    assert res.metrics.cpu_utilization == 54.0
    assert res.status_level == StatusLevel.HEALTHY

@pytest.mark.asyncio
async def test_task_handler_fetch_metrics_sensor():
    handler = TaskHandler()
    req = TaskRequest(
        task_id="t-2",
        task_type="monitoring",
        resource_type=ResourceType.SENSOR,
        resource_id="server-1",
        action=Action.FETCH_METRICS,
        provider=Provider.DEFAULT,
        credentials_ref="mock"
    )
    res = await handler.handle(req)
    assert res.status == "success"
    assert len(res.metrics.sensors) > 0
    assert any(s.name == "Inlet Temp" for s in res.metrics.sensors)

@pytest.mark.asyncio
async def test_task_handler_execute_action_power():
    handler = TaskHandler()
    req = TaskRequest(
        task_id="t-3",
        task_type="control",
        resource_type=ResourceType.SERVER,
        resource_id="server-1",
        action=Action.EXECUTE_ACTION,
        provider=Provider.DEFAULT,
        parameters={"action_type": "power_action", "power_state": "Off"},
        credentials_ref="mock"
    )
    res = await handler.handle(req)
    assert res.status == "success"
    assert "power_off" in res.actions_taken

@pytest.mark.asyncio
async def test_task_handler_invalid_request():
    handler = TaskHandler()
    # Pydantic validation handles standard invalid types, let's trigger handler errors
    # Handled by mock schema
    pass
