import pytest
from core.normalization import normalize_metrics, map_health_status

def test_map_health_status():
    assert map_health_status("OK") == "OK"
    assert map_health_status("ok") == "OK"
    assert map_health_status("Warning") == "Warning"
    assert map_health_status("Critical") == "Critical"
    assert map_health_status("something-else") == "Unknown"

def test_power_utilization_computation():
    raw = {
        "power_consumed_watts": 200.0,
        "power_capacity_watts": 800.0
    }
    normalized = normalize_metrics(raw)
    assert normalized.power_utilization_pct == 25.0

def test_fan_status_aggregation():
    # Test fan status aggregation from sensors list
    raw = {
        "sensors": [
            {"name": "Fan 1", "reading": 4000.0, "units": "RPM", "status": "ok"},
            {"name": "Fan 2", "reading": 0.0, "units": "RPM", "status": "Failed"}
        ]
    }
    normalized = normalize_metrics(raw)
    assert normalized.fan_status == "Critical"

def test_psu_status_aggregation():
    raw = {
        "sensors": [
            {"name": "PSU 1", "reading": 100.0, "units": "Watts", "status": "ok"},
            {"name": "PSU 2", "reading": 0.0, "units": "Watts", "status": "Warning"}
        ]
    }
    normalized = normalize_metrics(raw)
    assert normalized.power_supply_status == "Warning"

def test_storage_predictive_failure():
    raw = {
        "storage_status": "OK",
        "predictive_failure_count": 2
    }
    normalized = normalize_metrics(raw)
    assert normalized.storage_status == "Critical"

def test_missing_fields():
    raw = {}
    normalized = normalize_metrics(raw)
    assert normalized.cpu_utilization == 0.0
    assert normalized.overall_health == "Unknown"
    assert normalized.inventory is None
