import pytest
from models.task_response import ServerMetrics, StatusLevel
from core.anomaly_detection import detect_anomalies

def test_anomaly_clean():
    metrics = ServerMetrics(
        cpu_utilization=30.0,
        cpu_temperature_celsius=50.0,
        overall_health="OK",
        power_state="On"
    )
    level, insights = detect_anomalies(metrics)
    assert level == StatusLevel.HEALTHY
    assert len(insights) == 0

def test_anomaly_cpu_warning():
    metrics = ServerMetrics(
        cpu_utilization=90.0,
        overall_health="OK",
        power_state="On"
    )
    level, insights = detect_anomalies(metrics)
    assert level == StatusLevel.WARNING
    assert any("CPU utilization" in i for i in insights)

def test_anomaly_cpu_temp_critical():
    metrics = ServerMetrics(
        cpu_temperature_celsius=95.0,
        overall_health="OK",
        power_state="On"
    )
    level, insights = detect_anomalies(metrics)
    assert level == StatusLevel.CRITICAL
    assert any("CPU temperature" in i for i in insights)

def test_anomaly_fan_critical():
    metrics = ServerMetrics(
        fan_status="Critical",
        overall_health="OK",
        power_state="On"
    )
    level, insights = detect_anomalies(metrics)
    assert level == StatusLevel.CRITICAL
    assert any("fans have failed" in i for i in insights)

def test_anomaly_power_off_warning():
    metrics = ServerMetrics(
        power_state="Off",
        overall_health="OK"
    )
    level, insights = detect_anomalies(metrics)
    assert level == StatusLevel.WARNING
    assert any("powered off" in i for i in insights)

def test_multiple_anomalies_highest_wins():
    metrics = ServerMetrics(
        cpu_utilization=95.0,        # Warning
        cpu_temperature_celsius=95.0, # Critical
        overall_health="OK",
        power_state="On"
    )
    level, insights = detect_anomalies(metrics)
    assert level == StatusLevel.CRITICAL
    assert len(insights) == 2
