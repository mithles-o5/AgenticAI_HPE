import logging
from typing import Dict, List, Any, Optional
from adapters.plugins.redfish_adapter import RedfishAdapter

logger = logging.getLogger("server-agent.ilo-adapter")

class ILOAdapter(RedfishAdapter):
    def __init__(self, credentials: Dict[str, Any]) -> None:
        super().__init__(credentials)
        # HPE iLO usually has /redfish/v1/Systems/1 or similar ID. Override if needed.
        self.system_id = "1"

    def fetch_system_metrics(self, resource_id: str) -> Dict[str, Any]:
        # Perform standard Redfish fetch
        metrics = super().fetch_system_metrics(resource_id)
        
        # Override storage using SmartStorage if available
        try:
            smart_resp = self._request("GET", f"/Systems/{resource_id}/SmartStorage/ArrayControllers")
            if smart_resp.status_code == 200:
                controllers = smart_resp.json().get("Members", [])
                predictive_failure_count = 0
                storage_status = "OK"
                
                for ctrl in controllers:
                    ctrl_id = ctrl.get("@odata.id")
                    if ctrl_id:
                        ctrl_detail = self._request("GET", ctrl_id.replace("/redfish/v1", "")).json()
                        # Query SmartStorage Drives
                        drives_link = ctrl_detail.get("Links", {}).get("LogicalDrives", {}).get("@odata.id") or ctrl_detail.get("Links", {}).get("PhysicalDrives", {}).get("@odata.id")
                        if drives_link:
                            drives_resp = self._request("GET", drives_link.replace("/redfish/v1", ""))
                            if drives_resp.status_code == 200:
                                drives = drives_resp.json().get("Members", [])
                                for d in drives:
                                    d_link = d.get("@odata.id")
                                    if d_link:
                                        d_detail = self._request("GET", d_link.replace("/redfish/v1", "")).json()
                                        if d_detail.get("Oem", {}).get("Hpe", {}).get("PredictiveFailure", False):
                                            predictive_failure_count += 1
                                            storage_status = "Critical"
                
                metrics["storage_status"] = storage_status
                metrics["predictive_failure_count"] = predictive_failure_count
        except Exception as e:
            logger.debug(f"Failed to query HPE SmartStorage: {e}. Falling back to standard Redfish storage.")
            
        return metrics

    def fetch_memory_details(self, resource_id: str) -> List[Dict[str, Any]]:
        dimms = []
        try:
            mem_resp = self._request("GET", f"/Systems/{resource_id}/Memory")
            members = mem_resp.json().get("Members", [])
            for m in members:
                m_link = m.get("@odata.id")
                if m_link:
                    m_detail = self._request("GET", m_link.replace("/redfish/v1", "")).json()
                    # Extract HPE OEM detail
                    oem_hpe = m_detail.get("Oem", {}).get("Hpe", {})
                    dimms.append({
                        "id": m_detail.get("Id"),
                        "size_mb": m_detail.get("CapacityMiB"),
                        "status": m_detail.get("Status", {}).get("Health", "Unknown"),
                        "type": m_detail.get("MemoryDeviceType"),
                        "hpe_part_number": oem_hpe.get("BaseModelPartNumber", "N/A")
                    })
        except Exception as e:
            logger.warning(f"Failed to fetch HPE OEM memory details: {e}")
        return dimms

    def mount_virtual_media(self, resource_id: str, media_url: str, device_type: str) -> Dict[str, Any]:
        # Try HPE EmbeddedMedia or default to standard Redfish virtual media
        try:
            embedded_media_resp = self._request("GET", f"/Managers/{resource_id}/EmbeddedMedia")
            if embedded_media_resp.status_code == 200:
                # HPE OEM InsertMedia
                # POST /redfish/v1/Managers/1/VirtualMedia/2/Actions/VirtualMedia.InsertMedia
                # or custom EmbeddedMedia mount
                pass
        except Exception:
            pass
        return super().mount_virtual_media(resource_id, media_url, device_type)
