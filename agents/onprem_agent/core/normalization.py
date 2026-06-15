import logging
from core.exceptions import NormalizationError

logger = logging.getLogger("onprem_agent.normalization")

def normalize_status(health_val: str) -> str:
    """Normalize status strings into healthy, warning, critical."""
    if not health_val:
        return "healthy"
    
    val = health_val.lower().strip()
    if val in ("ok", "healthy", "normal", "green"):
        return "healthy"
    elif val in ("warning", "major", "yellow", "degreeded", "degraded"):
        return "warning"
    elif val in ("critical", "criticalerror", "red", "error", "failed"):
        return "critical"
    
    return "healthy"

def normalize_server_data(provider: str, raw_data: dict) -> dict:
    """Normalize server profile or hardware data from OneView or ComOps."""
    try:
        if provider == "oneview":
            return {
                "id": raw_data.get("uuid") or raw_data.get("id", ""),
                "name": raw_data.get("name", "Unknown OneView Server"),
                "model": raw_data.get("model", "HPE ProLiant Server"),
                "ip_address": raw_data.get("ip_address") or raw_data.get("ipAddress", ""),
                "power_state": raw_data.get("powerState", "Unknown"),
                "health_status": normalize_status(raw_data.get("health") or raw_data.get("status")),
                "location": raw_data.get("location", "Datacenter Rack")
            }
        elif provider == "com":
            return {
                "id": raw_data.get("uuid") or raw_data.get("id", ""),
                "name": raw_data.get("name", "Unknown Cloud Server"),
                "model": raw_data.get("model", "HPE GreenLake Instance"),
                "ip_address": raw_data.get("ip_address") or raw_data.get("ipAddress", ""),
                "power_state": raw_data.get("powerState", "Unknown"),
                "health_status": normalize_status(raw_data.get("health") or raw_data.get("status")),
                "location": raw_data.get("location", "GreenLake Cloud")
            }
        else: # Mock or default
            return {
                "id": raw_data.get("uuid") or raw_data.get("id", ""),
                "name": raw_data.get("name", "Mock Server"),
                "model": raw_data.get("model", "Mock Model"),
                "ip_address": raw_data.get("ip_address", "127.0.0.1"),
                "power_state": raw_data.get("powerState", "On"),
                "health_status": normalize_status(raw_data.get("health")),
                "location": raw_data.get("location", "Virtual Lab")
            }
    except Exception as e:
        logger.error(f"Error normalizing server data for provider {provider}: {e}")
        raise NormalizationError(f"Failed to normalize server response: {e}") from e

def normalize_metrics(raw_metrics: dict) -> dict:
    """Unifies metrics keys and guarantees numeric formats."""
    return {
        "cpu_utilization_percent": float(raw_metrics.get("cpu_utilization_percent", 0.0)),
        "memory_utilization_percent": float(raw_metrics.get("memory_utilization_percent", 0.0)),
        "power_draw_watts": float(raw_metrics.get("power_draw_watts", 0.0)),
        "temperature_celsius": float(raw_metrics.get("temperature_celsius", 0.0))
    }

def normalize_alerts(provider: str, raw_alerts: list) -> list:
    """Normalizes alert lists to standard format."""
    normalized = []
    for alert in raw_alerts:
        try:
            severity = normalize_status(alert.get("severity") or alert.get("status"))
            normalized.append({
                "alert_id": alert.get("id") or alert.get("alert_id") or alert.get("alertId", "unknown"),
                "severity": severity,
                "description": alert.get("description") or alert.get("message") or "No alert details provided",
                "timestamp": alert.get("created") or alert.get("timestamp") or "2026-06-09T23:03:15Z"
            })
        except Exception as e:
            logger.warning(f"Skipping bad alert format in normalizer: {e}")
            continue
    return normalized
