import sys
import os
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.poll_handler import PollHandler
from core.task_handler import TaskHandler

@pytest.mark.asyncio
async def test_poll_handler_sync():
    task_handler = TaskHandler()
    poll_handler = PollHandler(task_handler=task_handler)
    
    # Run poll sync using the mock provider
    response = await poll_handler.trigger_sync(provider="mock")
    
    assert response.status == "success"
    assert response.actions_taken == ["sync_cmdb"]
    assert response.status_level == "healthy"
    assert response.metrics["servers_synced"] == 1
    assert "Collected CMDB sync" in response.insights[0]["message"]

