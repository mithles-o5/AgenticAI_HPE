import sys
import os
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.anomaly_detection import detect_anomalies

def test_anomaly_detection_healthy():
    health = {"health_status": "healthy", "id": "1"}
    metrics = {
        "cpu_utilization_percent": 25.0,
        "memory_utilization_percent": 50.0,
        "temperature_celsius": 35.0
    }
    alerts = []
    
    level, insights = detect_anomalies(health, metrics, alerts)
    assert level == "healthy"
    assert len(insights) == 0

def test_anomaly_detection_cpu_high():
    metrics = {
        "cpu_utilization_percent": 92.0,
        "memory_utilization_percent": 50.0,
        "temperature_celsius": 35.0
    }
    level, insights = detect_anomalies(metrics=metrics)
    assert level == "warning"
    assert "High CPU" in insights[0]["message"]

    metrics["cpu_utilization_percent"] = 96.0
    level, insights = detect_anomalies(metrics=metrics)
    assert level == "critical"
    assert "Critical CPU" in insights[0]["message"]

def test_anomaly_detection_temp_critical():
    metrics = {
        "cpu_utilization_percent": 10.0,
        "memory_utilization_percent": 10.0,
        "temperature_celsius": 85.0
    }
    level, insights = detect_anomalies(metrics=metrics)
    assert level == "critical"
    assert "temperature" in insights[0]["message"].lower()

def test_anomaly_detection_alerts():
    alerts = [
        {"severity": "critical", "description": "Power supply fan failed", "alert_id": "a1"}
    ]
    level, insights = detect_anomalies(alerts=alerts)
    assert level == "critical"
    assert "CRITICAL alert" in insights[0]["message"]
