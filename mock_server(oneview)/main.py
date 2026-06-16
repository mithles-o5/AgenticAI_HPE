from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import json
import os
from models import *

mock_file = os.path.join(os.path.dirname(__file__), "mock_data.json")
try:
    with open(mock_file, "r", encoding="utf-8") as f:
        MOCK_DB = json.load(f)
except Exception:
    MOCK_DB = {}

app = FastAPI(title='Generated Mock Server', description='Generated automatically from API docs.')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/rest/login-sessions")
def post_rest_login_sessions(payload: PostRestLoginSessionsRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("post_rest_login_sessions", dict())

@app.post("/rest/login-sessions/auth-token")
def post_rest_login_sessions_auth_token(payload: PostRestLoginSessionsAuthTokenRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("post_rest_login_sessions_auth_token", dict())

@app.post("/rest/certificates/client/rabbitmq")
def post_rest_certificates_client_rabbitmq(payload: PostRestCertificatesClientRabbitmqRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("post_rest_certificates_client_rabbitmq", dict())

@app.get("/rest/certificates/client/rabbitmq/keypair/default")
def get_rest_certificates_client_rabbitmq_keypair_default():
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_rest_certificates_client_rabbitmq_keypair_default", dict())

@app.get("/rest/certificates/ca")
def get_rest_certificates_ca():
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_rest_certificates_ca", dict())

@app.delete("/rest/certificates/ca/rabbitmq_readonly")
def delete_rest_certificates_ca_rabbitmq_readonly():
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("delete_rest_certificates_ca_rabbitmq_readonly", dict())

@app.get("/rest/server-hardware/{id}/chassis")
def get_rest_server_hardware_id_chassis(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_rest_server_hardware_id_chassis", dict())

@app.get("/rest/server-hardware/{id}/firmwareInventory")
def get_rest_server_hardware_id_firmwareinventory(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_rest_server_hardware_id_firmwareinventory", dict())

@app.get("/rest/server-hardware/{id}/networkAdapters")
def get_rest_server_hardware_id_networkadapters(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_rest_server_hardware_id_networkadapters", dict())

@app.get("/rest/server-hardware/{id}/powerSupplies")
def get_rest_server_hardware_id_powersupplies(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_rest_server_hardware_id_powersupplies", dict())

@app.get("/rest/server-hardware/{id}/processors")
def get_rest_server_hardware_id_processors(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_rest_server_hardware_id_processors", dict())

@app.get("/rest/server-hardware/{id}/softwareInventory")
def get_rest_server_hardware_id_softwareinventory(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_rest_server_hardware_id_softwareinventory", dict())

@app.get("/rest/server-hardware/{id}/thermal")
def get_rest_server_hardware_id_thermal(id: str):
    """
    Returns dynamic thermal metrics based on the server's powerState.
    """
    server = find_server(id)
    if server and server.get("powerState") == "Off":
        return {
            "temperatureCelsius": 20.0,
            "status": "OK",
            "fanSpeedRpm": 0
        }
    return {
        "temperatureCelsius": 35.8,
        "status": "OK",
        "fanSpeedRpm": 4500
    }

@app.get("/rest/rack-managers/{id}/chassis/{uuid}")
def get_rest_rack_managers_id_chassis_uuid(id: str, uuid: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_rest_rack_managers_id_chassis_uuid", dict())

@app.post("/rest/ethernet-networks/bulk")
def post_rest_ethernet_networks_bulk(payload: PostRestEthernetNetworksBulkRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("post_rest_ethernet_networks_bulk", dict())

@app.put("/rest/storage-volumes/{id}")
def put_rest_storage_volumes_id(id: str, payload: PutRestStorageVolumesIdRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("put_rest_storage_volumes_id", dict())

@app.get("/rest/updates")
def get_rest_updates():
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_rest_updates", dict())

@app.get("/rest/updates/{id}")
def get_rest_updates_id(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_rest_updates_id", dict())

@app.get("/rest/rack-managers")
def get_rest_rack_managers():
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_rest_rack_managers", dict())

@app.post("/rest/rack-managers")
def post_rest_rack_managers(payload: PostRestRackManagersRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("post_rest_rack_managers", dict())

@app.get("/rest/rack-managers/chassis")
def get_rest_rack_managers_chassis():
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_rest_rack_managers_chassis", dict())

@app.get("/rest/rack-managers/managers")
def get_rest_rack_managers_managers():
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_rest_rack_managers_managers", dict())

@app.get("/rest/rack-managers/partitions")
def get_rest_rack_managers_partitions():
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_rest_rack_managers_partitions", dict())

@app.get("/rest/rack-managers/{id}")
def get_rest_rack_managers_id(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_rest_rack_managers_id", dict())

@app.patch("/rest/rack-managers/{id}")
def patch_rest_rack_managers_id(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("patch_rest_rack_managers_id", dict())

@app.delete("/rest/rack-managers/{id}")
def delete_rest_rack_managers_id(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("delete_rest_rack_managers_id", dict())

@app.get("/rest/rack-managers/{id}/chassis")
def get_rest_rack_managers_id_chassis(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_rest_rack_managers_id_chassis", dict())

@app.get("/rest/rack-managers/{id}/chassis/utilization")
def get_rest_rack_managers_id_chassis_utilization(id: str):
    """
    Returns dynamic power utilization by summing power consumption of all registered servers.
    """
    servers = MOCK_DB.get("server_hardware", {})
    total_power = 0
    for s_data in servers.values():
        if s_data.get("powerState") == "Off":
            total_power += 15 # Standby power
        else:
            total_power += 285 # Running power
            
    # Default fallback if no servers
    if total_power == 0:
        total_power = 15
        
    return {
        "powerWatts": total_power,
        "chassisStatus": "Normal"
    }

@app.get("/rest/rack-managers/{id}/environmentalConfiguration")
def get_rest_rack_managers_id_environmentalconfiguration(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_rest_rack_managers_id_environmentalconfiguration", dict())

@app.get("/rest/rack-managers/{id}/managers")
def get_rest_rack_managers_id_managers(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_rest_rack_managers_id_managers", dict())

@app.get("/rest/rack-managers/{id}/managers/{managerid}")
def get_rest_rack_managers_id_managers_managerid(id: str, managerid: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_rest_rack_managers_id_managers_managerid", dict())

@app.get("/rest/rack-managers/{id}/partitions")
def get_rest_rack_managers_id_partitions(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_rest_rack_managers_id_partitions", dict())

@app.get("/rest/rack-managers/{id}/partitions/{uuid}")
def get_rest_rack_managers_id_partitions_uuid(id: str, uuid: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_rest_rack_managers_id_partitions_uuid", dict())

@app.get("/rest/rack-managers/{id}/remoteSupportSettings")
def get_rest_rack_managers_id_remotesupportsettings(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_rest_rack_managers_id_remotesupportsettings", dict())

@app.get("/rest/server-hardware")
def get_rest_server_hardware():
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_rest_server_hardware", dict())

@app.post("/rest/server-hardware")
def post_rest_server_hardware(payload: PostRestServerHardwareRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("post_rest_server_hardware", dict())

@app.get("/rest/server-hardware/*/firmware")
def get_rest_server_hardware_firmware():
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_rest_server_hardware_firmware", dict())

@app.post("/rest/server-hardware/discovery")
def post_rest_server_hardware_discovery(payload: PostRestServerHardwareDiscoveryRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("post_rest_server_hardware_discovery", dict())

@app.post("/rest/server-hardware/firmware-compliance")
def post_rest_server_hardware_firmware_compliance(payload: PostRestServerHardwareFirmwareComplianceRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("post_rest_server_hardware_firmware_compliance", dict())

@app.get("/rest/server-hardware/schema")
def get_rest_server_hardware_schema():
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_rest_server_hardware_schema", dict())

def find_server(id: str):
    servers = MOCK_DB.get("server_hardware", {})
    if id in servers:
        return servers[id]
    
    # Check exact match for name, serial number, or IP first
    for s_id, s_data in servers.items():
        if s_data.get("name", "").lower() == id.lower():
            return s_data
        if s_data.get("serialNumber", "").lower() == id.lower():
            return s_data
        if s_data.get("ip_address") == id:
            return s_data

    import re
    match = re.search(r"(\d+)$", id)
    if match:
        suffix = match.group(1)
        suffix_val = int(suffix)
        for s_id, s_data in servers.items():
            name = s_data.get("name", "")
            if name.endswith(f"-{suffix}") or name.endswith(f"-{suffix_val}"):
                return s_data
            sn = s_data.get("serialNumber", "")
            if sn.endswith(f"-{suffix}") or sn.endswith(f"-{suffix_val}"):
                return s_data
            if s_id.startswith(id) or id.startswith(s_id):
                return s_data
            
    return None

@app.get("/rest/server-hardware/{id}")
def get_rest_server_hardware_id(id: str):
    """
    Returns actual server data from 1500-server database or raises 404.
    """
    server = find_server(id)
    if server:
        return server
    from fastapi import HTTPException
    raise HTTPException(status_code=404, detail="Resource not found")

# --- Added specifically for 1500-server scaling Demo ---
@app.put("/rest/server-hardware/{id}/powerState")
def put_rest_server_hardware_id_powerstate(id: str, payload: dict = {}):
    """
    Handles power commands for ANY dynamically generated OneView server.
    Actually updates the MOCK_DB state so subsequent GETs reflect the change.
    """
    state = payload.get("powerState", "Unknown")
    
    server = find_server(id)
    if server:
        server["powerState"] = state
        try:
            with open(mock_file, "w", encoding="utf-8") as f:
                json.dump(MOCK_DB, f, indent=4)
        except Exception as e:
            print(f"Error writing to mock_data.json: {e}")
            
        return {
            "status": "success",
            "message": f"Server {id} power state successfully changed to {state}",
            "powerState": state,
            "uuid": server.get("uuid", id),
            "server_details": server
        }
    
    # Fallback if somehow not in DB
    return {
        "status": "success",
        "message": f"Server {id} power state successfully changed to {state}",
        "powerState": state,
        "uuid": id
    }
