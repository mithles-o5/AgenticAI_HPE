import pytest
from core.poll_handler import ServerPollHandler
from config.settings import settings

def test_poll_cycle_success(monkeypatch):
    handler = ServerPollHandler()
    
    # Mock settings list source to static
    monkeypatch.setattr(settings, "POLL_SERVER_LIST_SOURCE", "static")
    
    summary = handler.run_poll_cycle()
    assert summary["polled"] == 2
    assert summary["errors"] == 0
