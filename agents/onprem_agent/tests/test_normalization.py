import sys
import os
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.normalization import (
    normalize_status,
    normalize_server_data,
    normalize_metrics,
    normalize_alerts
)

def test_normalize_status():
    assert normalize_status("OK") == "healthy"
    assert normalize_status("Normal") == "healthy"
    assert normalize_status("Warning") == "warning"
    assert normalize_status("degreeded") == "warning"
    assert normalize_status("Critical") == "critical"
    assert normalize_status("error") == "critical"
    assert normalize_status("unknown") == "healthy"

def test_normalize_server_data_oneview():
    raw = {
        "uuid": "ov-server-1",
        "name": "OV-Server-Prod-01",
        "model": "DL380 Gen10",
        "ip_address": "10.0.1.10",
        "powerState": "On",
        "health": "Warning"
    }
    norm = normalize_server_data("oneview", raw)
    assert norm["id"] == "ov-server-1"
    assert norm["name"] == "OV-Server-Prod-01"
    assert norm["health_status"] == "warning"

def test_normalize_metrics():
    raw = {
        "cpu_utilization_percent": "15.5",
        "memory_utilization_percent": 80,
        "power_draw_watts": 150.2,
        "temperature_celsius": 30
    }
    norm = normalize_metrics(raw)
    assert norm["cpu_utilization_percent"] == 15.5
    assert norm["memory_utilization_percent"] == 80.0
    assert norm["power_draw_watts"] == 150.2
    assert norm["temperature_celsius"] == 30.0
