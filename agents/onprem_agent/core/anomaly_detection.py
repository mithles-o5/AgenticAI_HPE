import logging

logger = logging.getLogger("onprem_agent.anomaly_detection")

def detect_anomalies(health_data: dict = None, metrics: dict = None, alerts: list = None) -> tuple[str, list[dict]]:
    """
    Evaluates health, metrics, and alerts to find anomalies.
    Returns: (status_level, insights)
      - status_level: "healthy", "warning", or "critical"
      - insights: list of dicts with {"type": "anomaly", "severity": "...", "message": "..."}
    """
    status_level = "healthy"
    insights = []

    # 1. Health Status Checks
    if health_data:
        health_status = health_data.get("health_status", "healthy")
        if health_status == "critical":
            status_level = "critical"
            insights.append({
                "type": "health_anomaly",
                "severity": "critical",
                "message": f"Resource health status is Critical. Resource ID: {health_data.get('id')}"
            })
        elif health_status == "warning":
            if status_level != "critical":
                status_level = "warning"
            insights.append({
                "type": "health_anomaly",
                "severity": "warning",
                "message": f"Resource health status is Warning. Resource ID: {health_data.get('id')}"
            })

    # 2. Metrics Anomaly Checks
    if metrics:
        cpu = metrics.get("cpu_utilization_percent", 0.0)
        mem = metrics.get("memory_utilization_percent", 0.0)
        temp = metrics.get("temperature_celsius", 0.0)

        # CPU thresholds
        if cpu >= 95.0:
            status_level = "critical"
            insights.append({
                "type": "utilization_anomaly",
                "severity": "critical",
                "message": f"Critical CPU utilisation detected: {cpu}% (>= 95%)"
            })
        elif cpu >= 90.0:
            if status_level != "critical":
                status_level = "warning"
            insights.append({
                "type": "utilization_anomaly",
                "severity": "warning",
                "message": f"High CPU utilisation warning: {cpu}% (>= 90%)"
            })

        # Memory thresholds
        if mem >= 98.0:
            status_level = "critical"
            insights.append({
                "type": "utilization_anomaly",
                "severity": "critical",
                "message": f"Critical Memory utilisation detected: {mem}% (>= 98%)"
            })
        elif mem >= 95.0:
            if status_level != "critical":
                status_level = "warning"
            insights.append({
                "type": "utilization_anomaly",
                "severity": "warning",
                "message": f"High Memory utilisation warning: {mem}% (>= 95%)"
            })

        # Temperature thresholds
        if temp >= 80.0:
            status_level = "critical"
            insights.append({
                "type": "thermal_anomaly",
                "severity": "critical",
                "message": f"Critical system temperature detected: {temp}°C (>= 80°C)"
            })
        elif temp >= 70.0:
            if status_level != "critical":
                status_level = "warning"
            insights.append({
                "type": "thermal_anomaly",
                "severity": "warning",
                "message": f"High system temperature warning: {temp}°C (>= 70°C)"
            })

    # 3. Alert Logs Anomaly Checks
    if alerts:
        for alert in alerts:
            severity = alert.get("severity")
            if severity == "critical":
                status_level = "critical"
                insights.append({
                    "type": "active_alert",
                    "severity": "critical",
                    "message": f"Active CRITICAL alert: {alert.get('description')} (ID: {alert.get('alert_id')})"
                })
            elif severity == "warning":
                if status_level != "critical":
                    status_level = "warning"
                insights.append({
                    "type": "active_alert",
                    "severity": "warning",
                    "message": f"Active WARNING alert: {alert.get('description')} (ID: {alert.get('alert_id')})"
                })

    return status_level, insights
