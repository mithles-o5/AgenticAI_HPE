from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional

class ServerAdapter(ABC):

    @abstractmethod
    def fetch_system_metrics(self, resource_id: str) -> Dict[str, Any]:
        """Fetch CPU/memory utilization, power, temperature, overall health rollups."""
        pass

    @abstractmethod
    def fetch_sensors(self, resource_id: str) -> List[Dict[str, Any]]:
        """Fetch all sensor readings: fans, PSUs, temperatures, voltages."""
        pass

    @abstractmethod
    def fetch_event_log(self, resource_id: str, severity_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """Fetch system event log (SEL) entries, optionally filtered by severity."""
        pass

    @abstractmethod
    def clear_event_log(self, resource_id: str) -> Dict[str, Any]:
        """Clear the system event log."""
        pass

    @abstractmethod
    def execute_power_action(self, resource_id: str, action: str) -> Dict[str, Any]:
        """Execute power action: On, ForceOff, GracefulShutdown, ForceRestart, PowerCycle."""
        pass

    @abstractmethod
    def set_boot_order(self, resource_id: str, boot_order: List[str]) -> Dict[str, Any]:
        """Set one-time or persistent boot device order."""
        pass

    @abstractmethod
    def mount_virtual_media(self, resource_id: str, media_url: str, device_type: str) -> Dict[str, Any]:
        """Mount an ISO/IMG as virtual media (CD or USB)."""
        pass

    @abstractmethod
    def discover_inventory(self, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """List hardware inventory: CPUs, DIMMs, storage controllers, NICs, firmware versions."""
        pass

    @abstractmethod
    def health_check(self, resource_id: str) -> Dict[str, Any]:
        """Return overall health rollup for the server."""
        pass
