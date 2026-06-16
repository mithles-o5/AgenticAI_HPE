from typing import Tuple, List
from models.task_response import ServerMetrics, StatusLevel
from config.settings import settings

def detect_anomalies(metrics: ServerMetrics) -> Tuple[StatusLevel, List[str]]:
    insights = []
    is_critical = False
    is_warning = False

    # CRITICAL RULES
    if metrics.overall_health == "Critical":
        is_critical = True
        insights.append("Server overall health is Critical — immediate action required")
        
    if metrics.power_supply_status == "Critical":
        is_critical = True
        insights.append("One or more power supplies have failed")
        
    if metrics.fan_status == "Critical":
        is_critical = True
        insights.append("One or more fans have failed — risk of thermal shutdown")
        
    if metrics.cpu_temperature_celsius >= settings.TEMPERATURE_CRITICAL_THRESHOLD:
        is_critical = True
        insights.append(
            f"CPU temperature {metrics.cpu_temperature_celsius}°C exceeds critical threshold ({settings.TEMPERATURE_CRITICAL_THRESHOLD}°C)"
        )
        
    if metrics.storage_status == "Critical" or metrics.predictive_failure_count > 0:
        is_critical = True
        count = metrics.predictive_failure_count or 1
        insights.append(f"{count} drive(s) reporting predictive failure — replace soon")
        
    if metrics.critical_event_count > 0:
        is_critical = True
        insights.append(f"{metrics.critical_event_count} critical event(s) in system event log")

    # WARNING RULES
    if metrics.cpu_utilization > settings.CPU_WARNING_THRESHOLD:
        is_warning = True
        insights.append(f"CPU utilization at {metrics.cpu_utilization}% exceeds {settings.CPU_WARNING_THRESHOLD}% threshold")
        
    if metrics.memory_utilization > settings.MEMORY_WARNING_THRESHOLD:
        is_warning = True
        insights.append(f"Memory utilization at {metrics.memory_utilization}% exceeds {settings.MEMORY_WARNING_THRESHOLD}% threshold")
        
    # Check warning temp if not already critical
    if metrics.cpu_temperature_celsius >= settings.TEMPERATURE_WARNING_THRESHOLD and metrics.cpu_temperature_celsius < settings.TEMPERATURE_CRITICAL_THRESHOLD:
        is_warning = True
        insights.append(f"CPU temperature {metrics.cpu_temperature_celsius}°C approaching critical threshold")
        
    if metrics.inlet_temperature_celsius >= settings.TEMPERATURE_WARNING_THRESHOLD:
        is_warning = True
        insights.append(f"Inlet temperature {metrics.inlet_temperature_celsius}°C elevated")
        
    if metrics.power_utilization_pct > 85.0:
        is_warning = True
        insights.append(f"Power draw at {metrics.power_utilization_pct}% of rated capacity")
        
    if metrics.power_supply_status == "Warning":
        is_warning = True
        insights.append("Power supply degraded")
        
    if metrics.fan_status == "Warning":
        is_warning = True
        insights.append("Fan degraded — monitor closely")
        
    if metrics.network_status in ("Warning", "Critical"):
        is_warning = True
        insights.append("Network interface degradation detected")
        
    if metrics.power_state == "Off":
        is_warning = True
        insights.append("Server is powered off")
        
    if metrics.event_count > 0 and metrics.critical_event_count == 0:
        is_warning = True
        insights.append(f"{metrics.event_count} non-critical event(s) in system event log")

    # Decide Status Level
    if is_critical:
        level = StatusLevel.CRITICAL
    elif is_warning:
        level = StatusLevel.WARNING
    else:
        level = StatusLevel.HEALTHY

    return level, insights
