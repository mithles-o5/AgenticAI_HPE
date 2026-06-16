from typing import Dict, List, Any, Optional
from adapters.base import ServerAdapter

class MockAdapter(ServerAdapter):
    # Class-level dictionaries to persist state for mock resources
    _power_states: Dict[str, str] = {}
    _boot_orders: Dict[str, List[str]] = {}
    _virtual_media: Dict[str, Dict[str, Any]] = {}
    _cleared_logs: Dict[str, bool] = {}

    def _get_power_state(self, resource_id: str) -> str:
        # Default to "On" if not set
        return self._power_states.get(resource_id, "On")

    def fetch_system_metrics(self, resource_id: str) -> Dict[str, Any]:
        power_state = self._get_power_state(resource_id)
        if power_state == "Off":
            return {
                "cpu_utilization": 0.0,
                "memory_utilization": 0.0,
                "cpu_count": 2,
                "memory_total_gb": 256.0,
                "power_consumed_watts": 18.5,  # Standby power
                "power_capacity_watts": 800.0,
                "inlet_temperature_celsius": 22.0,
                "cpu_temperature_celsius": 24.5,
                "overall_health": "OK",
                "power_supply_status": "OK",
                "fan_status": "OK",
                "storage_status": "OK",
                "network_status": "OK",
                "power_state": "Off"
            }
        else:
            return {
                "cpu_utilization": 54.0,
                "memory_utilization": 67.5,
                "cpu_count": 2,
                "memory_total_gb": 256.0,
                "power_consumed_watts": 420.0,
                "power_capacity_watts": 800.0,
                "inlet_temperature_celsius": 24.0,
                "cpu_temperature_celsius": 58.0,
                "overall_health": "OK",
                "power_supply_status": "OK",
                "fan_status": "OK",
                "storage_status": "OK",
                "network_status": "OK",
                "power_state": "On"
            }

    def fetch_sensors(self, resource_id: str) -> List[Dict[str, Any]]:
        power_state = self._get_power_state(resource_id)
        is_on = (power_state != "Off")
        
        return [
            {"name": "Inlet Temp", "reading": 24.0 if is_on else 22.0, "units": "C", "status": "ok"},
            {"name": "CPU1 Temp", "reading": 58.0 if is_on else 24.5, "units": "C", "status": "ok"},
            {"name": "Fan 1", "reading": 4500.0 if is_on else 0.0, "units": "RPM", "status": "ok"},
            {"name": "Fan 2", "reading": 4400.0 if is_on else 0.0, "units": "RPM", "status": "ok"},
            {"name": "Fan 3", "reading": 4600.0 if is_on else 0.0, "units": "RPM", "status": "ok"},
            {"name": "Fan 4", "reading": 4550.0 if is_on else 0.0, "units": "RPM", "status": "ok"},
            {"name": "PSU 1", "reading": 210.0 if is_on else 9.0, "units": "Watts", "status": "ok"},
            {"name": "PSU 2", "reading": 210.0 if is_on else 9.5, "units": "Watts", "status": "ok"},
        ]

    def fetch_event_log(self, resource_id: str, severity_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        if self._cleared_logs.get(resource_id, False):
            return []

        all_events = [
            {"timestamp": "2026-06-12T04:15:30Z", "sensor": "Power Supply", "description": "Power redundancy regained", "severity": "Informational"},
            {"timestamp": "2026-06-12T03:10:00Z", "sensor": "Fan 1", "description": "Fan speed returned to normal", "severity": "Informational"},
            {"timestamp": "2026-06-11T22:05:12Z", "sensor": "Drive 3", "description": "Predictive failure alert", "severity": "Warning"},
        ]
        if severity_filter:
            sevs = [s.strip().lower() for s in severity_filter.split(",")]
            return [e for e in all_events if e["severity"].lower() in sevs]
        return all_events

    def clear_event_log(self, resource_id: str) -> Dict[str, Any]:
        self._cleared_logs[resource_id] = True
        return {"status": "success", "message": "Log cleared successfully"}

    def execute_power_action(self, resource_id: str, action: str) -> Dict[str, Any]:
        action_clean = action.strip().lower()
        if action_clean in ("off", "forceoff", "gracefulshutdown"):
            self._power_states[resource_id] = "Off"
            ret_state = "Off"
        elif action_clean in ("on", "forcerestart", "powercycle"):
            self._power_states[resource_id] = "On"
            ret_state = "On"
        else:
            ret_state = self._get_power_state(resource_id)

        # Reset cleared logs status if rebooted to keep mock realistic
        if action_clean in ("forcerestart", "powercycle"):
            self._cleared_logs[resource_id] = False

        return {
            "task_id": f"mock-pwr-{resource_id}",
            "state": "Completed",
            "result": f"Action {action} successful. Current state: {ret_state}"
        }

    def set_boot_order(self, resource_id: str, boot_order: List[str]) -> Dict[str, Any]:
        self._boot_orders[resource_id] = boot_order
        return {
            "status": "success",
            "boot_order": boot_order
        }

    def mount_virtual_media(self, resource_id: str, media_url: str, device_type: str) -> Dict[str, Any]:
        self._virtual_media[resource_id] = {
            "media_url": media_url,
            "device_type": device_type,
            "mounted": True
        }
        return {
            "status": "success",
            "message": f"Successfully mounted {media_url} as {device_type}"
        }

    def discover_inventory(self, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        # Filters could contain resource_id
        res_id = filters.get("resource_id", "mock-server-01")
        return [
            {
                "id": res_id,
                "name": "Mock Baremetal Server",
                "cpus": [
                    {"model": "Intel Xeon Platinum 8380 CPU @ 2.30GHz", "cores": 40, "count": 2}
                ],
                "memory": [
                    {"size_gb": 32, "speed_mhz": 3200, "count": 8}
                ],
                "storage": [
                    {
                        "controller": "Smart Array P408i-a SR Gen10",
                        "drives": [
                            {"model": "HPE 1.2TB SAS 10K", "size_gb": 1200, "status": "OK"},
                            {"model": "HPE 1.2TB SAS 10K", "size_gb": 1200, "status": "OK"},
                            {"model": "HPE 1.2TB SAS 10K", "size_gb": 1200, "status": "OK"},
                            {"model": "HPE 1.2TB SAS 10K", "size_gb": 1200, "status": "OK"}
                        ]
                    }
                ],
                "nics": [
                    {"name": "Embedded LOM 1 Port 1", "mac": "00:11:22:33:44:55", "speed_gbps": 10},
                    {"name": "Embedded LOM 1 Port 2", "mac": "00:11:22:33:44:56", "speed_gbps": 10}
                ],
                "firmware": [
                    {"component": "System ROM", "version": "U32 v2.72"},
                    {"component": "iLO 5", "version": "v2.44"}
                ]
            }
        ]

    def health_check(self, resource_id: str) -> Dict[str, Any]:
        power_state = self._get_power_state(resource_id)
        if power_state == "Off":
            return {"overall_health": "OK", "power_state": "Off"}
        return {"overall_health": "OK", "power_state": "On"}
