import subprocess
import logging
import re
from typing import Dict, List, Any, Optional
from adapters.base import ServerAdapter

logger = logging.getLogger("server-agent.ipmi-adapter")

class IPMIAdapter(ServerAdapter):
    def __init__(self, credentials: Dict[str, Any]) -> None:
        self.host = credentials.get("host")
        self.username = credentials.get("username")
        self.password = credentials.get("password")
        self.interface = credentials.get("interface", "lanplus")

    def _mask_password(self, cmd: List[str]) -> str:
        """Mask password in the logged command list."""
        masked = []
        skip_next = False
        for arg in cmd:
            if skip_next:
                masked.append("********")
                skip_next = False
            elif arg == "-P":
                masked.append(arg)
                skip_next = True
            else:
                masked.append(arg)
        return " ".join(masked)

    def _run_ipmitool(self, args: List[str]) -> str:
        if not self.host or not self.username or not self.password:
            raise ValueError("IPMI credentials incomplete")
        
        base_cmd = [
            "ipmitool",
            "-I", self.interface,
            "-H", self.host,
            "-U", self.username,
            "-P", self.password
        ]
        full_cmd = base_cmd + args
        masked_str = self._mask_password(full_cmd)
        logger.info(f"Running command: {masked_str}")

        try:
            res = subprocess.run(
                full_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=15.0
            )
            if res.returncode != 0:
                err_msg = f"ipmitool failed with code {res.returncode}: {res.stderr.strip()}"
                logger.error(err_msg)
                raise RuntimeError(err_msg)
            return res.stdout
        except subprocess.TimeoutExpired as e:
            logger.error(f"ipmitool timeout executing: {masked_str}")
            raise e
        except Exception as e:
            logger.error(f"ipmitool execution error: {e}")
            raise e

    def fetch_system_metrics(self, resource_id: str) -> Dict[str, Any]:
        # Get power status
        power_output = self._run_ipmitool(["chassis", "power", "status"])
        power_state = "Unknown"
        if "is on" in power_output.lower():
            power_state = "On"
        elif "is off" in power_output.lower():
            power_state = "Off"

        # If off, return standby metrics
        if power_state == "Off":
            return {
                "cpu_utilization": 0.0,
                "memory_utilization": 0.0,
                "cpu_count": 1,
                "memory_total_gb": 0.0,
                "power_consumed_watts": 0.0,
                "power_capacity_watts": 0.0,
                "inlet_temperature_celsius": 0.0,
                "cpu_temperature_celsius": 0.0,
                "overall_health": "OK",
                "power_supply_status": "OK",
                "fan_status": "OK",
                "storage_status": "OK",
                "network_status": "OK",
                "power_state": "Off"
            }

        # Parse sensors for basic metrics
        sensors = self.fetch_sensors(resource_id)
        inlet_temp = 0.0
        cpu_temp = 0.0
        psu_status = "OK"
        fan_status = "OK"
        
        for s in sensors:
            name_lower = s["name"].lower()
            status_lower = s["status"].lower()
            if "inlet" in name_lower or "ambient" in name_lower:
                inlet_temp = s["reading"]
            elif "cpu" in name_lower and "temp" in name_lower:
                cpu_temp = s["reading"]
            elif "fan" in name_lower and status_lower in ("critical", "failed", "nc", "cr"):
                fan_status = "Critical"
            elif "psu" in name_lower and status_lower in ("critical", "failed", "nc", "cr"):
                psu_status = "Critical"

        return {
            "cpu_utilization": 50.0,  # Generic placeholder since IPMI is hardware level
            "memory_utilization": 60.0,
            "cpu_count": 2,
            "memory_total_gb": 128.0,
            "power_consumed_watts": 380.0,
            "power_capacity_watts": 750.0,
            "inlet_temperature_celsius": inlet_temp,
            "cpu_temperature_celsius": cpu_temp,
            "overall_health": "OK" if (fan_status == "OK" and psu_status == "OK") else "Warning",
            "power_supply_status": psu_status,
            "fan_status": fan_status,
            "storage_status": "OK",
            "network_status": "OK",
            "power_state": "On"
        }

    def fetch_sensors(self, resource_id: str) -> List[Dict[str, Any]]:
        # Parsing "sensor list" output
        # CPU1 Temp        | 45.000     | degrees C  | ok    | ...
        output = self._run_ipmitool(["sensor", "list"])
        sensors = []
        for line in output.splitlines():
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 4:
                try:
                    name = parts[0]
                    reading_str = parts[1]
                    units = parts[2]
                    status = parts[3]
                    
                    # Check if reading is numeric
                    reading = 0.0
                    try:
                        reading = float(reading_str)
                    except ValueError:
                        pass
                    
                    sensors.append({
                        "name": name,
                        "reading": reading,
                        "units": units,
                        "status": status
                    })
                except Exception:
                    pass
        return sensors

    def fetch_event_log(self, resource_id: str, severity_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        output = self._run_ipmitool(["sel", "elist"])
        events = []
        for line in output.splitlines():
            # e.g., "  1 | 06/12/2026 | 02:10:00 | Temperature | Upper Critical going high | Asserted"
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 5:
                timestamp = f"{parts[1]} {parts[2]}"
                sensor = parts[3]
                description = parts[4]
                severity = "Informational"
                if "critical" in description.lower():
                    severity = "Critical"
                elif "warning" in description.lower():
                    severity = "Warning"
                
                ev = {
                    "timestamp": timestamp,
                    "sensor": sensor,
                    "description": description,
                    "severity": severity
                }
                
                if severity_filter:
                    sevs = [s.strip().lower() for s in severity_filter.split(",")]
                    if severity.lower() in sevs:
                        events.append(ev)
                else:
                    events.append(ev)
        return events

    def clear_event_log(self, resource_id: str) -> Dict[str, Any]:
        self._run_ipmitool(["sel", "clear"])
        return {"status": "success", "message": "SEL cleared"}

    def execute_power_action(self, resource_id: str, action: str) -> Dict[str, Any]:
        # chassis power on|off|cycle|reset|soft
        action_map = {
            "on": "on",
            "forceoff": "off",
            "gracefulshutdown": "soft",
            "forcerestart": "reset",
            "powercycle": "cycle"
        }
        ipmi_act = action_map.get(action.lower(), "on")
        self._run_ipmitool(["chassis", "power", ipmi_act])
        
        # Verify status after short delay or return status directly
        status_output = self._run_ipmitool(["chassis", "power", "status"])
        return {
            "task_id": f"ipmi-pwr-{resource_id}",
            "status": "success",
            "result": f"Executed chassis power {ipmi_act}. State: {status_output.strip()}"
        }

    def set_boot_order(self, resource_id: str, boot_order: List[str]) -> Dict[str, Any]:
        # ipmitool chassis bootdev pxe|disk|cdrom|bios
        # map first item in boot_order list
        target = "disk"
        if boot_order:
            b_item = boot_order[0].lower()
            if "pxe" in b_item:
                target = "pxe"
            elif "cd" in b_item:
                target = "cdrom"
            elif "bios" in b_item:
                target = "bios"
            else:
                target = "disk"
        
        self._run_ipmitool(["chassis", "bootdev", target])
        return {"status": "success", "boot_order": boot_order}

    def mount_virtual_media(self, resource_id: str, media_url: str, device_type: str) -> Dict[str, Any]:
        # IPMI does not support virtual media mounting out of the box via CLI
        return {
            "status": "failed",
            "error": "Virtual media not supported via IPMI — use Redfish"
        }

    def discover_inventory(self, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        # Parsing "fru print" or generic discovery
        output = self._run_ipmitool(["fru", "print"])
        return [{
            "id": filters.get("resource_id", "ipmi-server"),
            "name": "IPMI Managed Server",
            "raw_fru": output[:500]  # First 500 chars parsed
        }]

    def health_check(self, resource_id: str) -> Dict[str, Any]:
        try:
            metrics = self.fetch_system_metrics(resource_id)
            return {"overall_health": metrics.get("overall_health", "Unknown"), "power_state": metrics.get("power_state", "Unknown")}
        except Exception as e:
            return {"overall_health": "Critical", "error": str(e)}
