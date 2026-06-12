from typing import Dict, Any, List
from models.task_response import ServerMetrics, SensorReading
from config.settings import settings

def map_health_status(health: str) -> str:
    if not health:
        return "Unknown"
    h_clean = str(health).strip().lower()
    if h_clean in ("ok", "healthy", "good"):
        return "OK"
    elif h_clean in ("warning", "degraded"):
        return "Warning"
    elif h_clean in ("critical", "fatal", "failed", "nc", "cr"):
        return "Critical"
    return "Unknown"

def normalize_metrics(raw_data: Dict[str, Any]) -> ServerMetrics:
    # Handle direct sensor response list if passed
    if "sensors" in raw_data:
        sensor_list = raw_data["sensors"]
        metrics = ServerMetrics()
        metrics.sensors = [
            SensorReading(
                name=s.get("name", "Unknown"),
                reading=float(s.get("reading", 0.0)),
                units=s.get("units", ""),
                status=map_health_status(s.get("status"))
            )
            for s in sensor_list
        ]
        # Aggregate sensors to statuses
        fan_failures = settings.FAN_FAILURE_STATUS_VALUES.split(",")
        psu_failures = settings.PSU_FAILURE_STATUS_VALUES.split(",")
        
        metrics.fan_status = "OK"
        metrics.power_supply_status = "OK"
        
        for s in metrics.sensors:
            name = s.name.lower()
            status = s.status
            if "fan" in name:
                if status in fan_failures or status == "Critical":
                    metrics.fan_status = "Critical"
                elif status == "Warning" and metrics.fan_status != "Critical":
                    metrics.fan_status = "Warning"
            elif "psu" in name or "power supply" in name:
                if status in psu_failures or status == "Critical":
                    metrics.power_supply_status = "Critical"
                elif status == "Warning" and metrics.power_supply_status != "Critical":
                    metrics.power_supply_status = "Warning"
                    
        return metrics

    # Extract metrics fields
    cpu_util = float(raw_data.get("cpu_utilization", 0.0))
    mem_util = float(raw_data.get("memory_utilization", 0.0))
    cpu_count = int(raw_data.get("cpu_count", 0))
    mem_total = float(raw_data.get("memory_total_gb", 0.0))
    
    p_cons = float(raw_data.get("power_consumed_watts", 0.0))
    p_cap = float(raw_data.get("power_capacity_watts", 0.0))
    
    inlet_temp = float(raw_data.get("inlet_temperature_celsius", 0.0))
    cpu_temp = float(raw_data.get("cpu_temperature_celsius", 0.0))
    
    overall = map_health_status(raw_data.get("overall_health", "Unknown"))
    psu_status = map_health_status(raw_data.get("power_supply_status", "Unknown"))
    fan_status = map_health_status(raw_data.get("fan_status", "Unknown"))
    stor_status = map_health_status(raw_data.get("storage_status", "Unknown"))
    net_status = map_health_status(raw_data.get("network_status", "Unknown"))
    
    power_state = raw_data.get("power_state", "Unknown")
    pred_fail = int(raw_data.get("predictive_failure_count", 0))
    
    # Compute power pct
    p_pct = 0.0
    if p_cap > 0.0:
        p_pct = round((p_cons / p_cap) * 100.0, 2)
        
    # Cap percentages at 100.0
    cpu_util = min(cpu_util, 100.0)
    mem_util = min(mem_util, 100.0)
    p_pct = min(p_pct, 100.0)

    # Storage predictive failure logic
    if settings.DISK_PREDICTIVE_FAILURE_FLAG and pred_fail > 0:
        stor_status = "Critical"

    return ServerMetrics(
        cpu_utilization=cpu_util,
        memory_utilization=mem_util,
        cpu_count=cpu_count,
        memory_total_gb=mem_total,
        power_consumed_watts=p_cons,
        power_capacity_watts=p_cap,
        power_utilization_pct=p_pct,
        inlet_temperature_celsius=inlet_temp,
        cpu_temperature_celsius=cpu_temp,
        overall_health=overall,
        power_supply_status=psu_status,
        fan_status=fan_status,
        storage_status=stor_status,
        network_status=net_status,
        power_state=power_state,
        predictive_failure_count=pred_fail,
        inventory=raw_data.get("inventory")
    )
