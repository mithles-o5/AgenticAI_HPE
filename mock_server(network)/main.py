import uuid
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
import os
from models import DeviceSchema, NetworkVlanRequest, NetworkPortStatusRequest, ArubaVlanRequest, ArubaPortStatusRequest

from database import db

app = FastAPI(title='Mock Network Server', description='Mock Network API Server')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/network/v1/devices")
def get_network_devices():
    """
    Retrieves a comprehensive list of all network devices.
    """
    collection_path = "/network/v1/devices"
    return db.get_all(collection_path)

@app.get("/network/v1/devices/{id}")
def get_network_device_by_id(id: str):
    collection_path = "/network/v1/devices"
    item = db.get_item(collection_path, id)
    if item:
        return item
    raise HTTPException(status_code=404, detail="Device not found")

@app.post("/network/v1/devices")
def create_network_device(payload: DeviceSchema):
    import random
    import datetime
    collection_path = "/network/v1/devices"
    
    payload_dict = payload.dict()
    item_id = payload_dict.get("id") or payload_dict.get("serial_number") or str(uuid.uuid4())
    payload_dict["id"] = item_id

    # Add default mock data so metrics aren't null
    if payload_dict.get("power_state") is None:
        payload_dict["power_state"] = "ON"
    if payload_dict.get("health_status") is None:
        payload_dict["health_status"] = "OK"

    # Only populate metrics if the device is ON
    if payload_dict.get("power_state", "ON").upper() in ["ON", "POWERON"]:
        if payload_dict.get("cpu_utilization_percent") is None:
            payload_dict["cpu_utilization_percent"] = round(random.uniform(10.0, 90.0), 1)
        if payload_dict.get("memory_utilization_percent") is None:
            payload_dict["memory_utilization_percent"] = round(random.uniform(10.0, 90.0), 1)
        if payload_dict.get("power_draw_watts") is None:
            payload_dict["power_draw_watts"] = round(random.uniform(150.0, 400.0), 1)
        if payload_dict.get("temperature_celsius") is None:
            payload_dict["temperature_celsius"] = round(random.uniform(25.0, 45.0), 1)

    if not payload_dict.get("ports"):
        # Generate some default mock ports
        payload_dict["ports"] = {
            f"GigabitEthernet1/0/{i}": ("UP" if random.random() > 0.3 else "DOWN")
            for i in range(1, 25)
        }

    if not payload_dict.get("configured_vlans"):
        payload_dict["configured_vlans"] = [
            {"vlan_id": 1, "name": "Management"}
        ]
    
    payload_dict["created_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S+05:30")
    payload_dict["updated_at"] = payload_dict["created_at"]

    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.put("/network/v1/devices/{id}")
@app.post("/network/v1/devices/{id}")
def update_network_device(id: str, payload: DeviceSchema):
    from fastapi import HTTPException
    import random
    import datetime
    
    collection_path = "/network/v1/devices"
    item = db.get_item(collection_path, id)
    if not item:
        raise HTTPException(status_code=404, detail="Device not found")
        
    device = dict(item)
    payload_dict = payload.dict(exclude_unset=True) if hasattr(payload, 'dict') else payload
    state = payload_dict.get("power_state") or payload_dict.get("powerState") or payload_dict.get("action")
    if state:
        if state.upper() in ["ON", "POWERON"]:
            device["power_state"] = "ON"
            device["cpu_utilization_percent"] = round(random.uniform(10.0, 90.0), 1)
            device["memory_utilization_percent"] = round(random.uniform(10.0, 90.0), 1)
            device["power_draw_watts"] = round(random.uniform(150.0, 400.0), 1)
            device["temperature_celsius"] = round(random.uniform(25.0, 45.0), 1)
        elif state.upper() in ["OFF", "POWEROFF"]:
            device["power_state"] = "OFF"
            device["cpu_utilization_percent"] = 0.0
            device["memory_utilization_percent"] = 0.0
            device["power_draw_watts"] = 0.0
            device["temperature_celsius"] = 0.0
            
    # Also apply any other payload properties
    for k, v in payload_dict.items():
        if k not in ["power_state", "powerState", "action"]:
            device[k] = v
            
    device["updated_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S+05:30")
    db.upsert_item(collection_path, device["id"], device)
    return device

@app.delete("/network/v1/devices/{id}")
def delete_network_device(id: str):
    """
    CRUD Route: DELETE /network/v1/devices/{id}
    """
    collection_path = "/network/v1/devices"
    item = db.get_item(collection_path, id)
    if not item:
        raise HTTPException(status_code=404, detail="Device not found")
    deleted = db.delete_item(collection_path, item["id"])
    return {"message": "Deleted successfully", "id": id, "item": deleted}

@app.patch("/network/v1/devices/{id}")
def patch_network_device(id: str, payload: dict):
    """
    CRUD Route: PATCH /network/v1/devices/{id}
    """
    import datetime
    collection_path = "/network/v1/devices"
    item = db.get_item(collection_path, id)
    if not item:
        raise HTTPException(status_code=404, detail="Device not found")
    
    device = dict(item)
    if "ports" not in device:
        device["ports"] = {}
        
    payload_dict = {k: v for k, v in payload.items() if v is not None}
    
    for k, v in payload_dict.items():
        # Handle port updates from natural language mapping (e.g. "port eth0", "ports/eth0/status")
        k_lower = k.lower()
        if k_lower.startswith("port ") or k_lower.startswith("ports/"):
            # Extract port name: "port eth0" -> "eth0", "ports/eth0/status" -> "eth0"
            port_name = k.split(" ", 1)[1] if " " in k else k.split("/")[1]
            device["ports"][port_name] = v
        else:
            device[k] = v
            
    device["updated_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S+05:30")
    db.upsert_item(collection_path, device["id"], device)
    return device

from pydantic import BaseModel
class NetworkPowerRequest(BaseModel):
    action: str

@app.post("/network/v1/devices/{id}/power")
def post_network_device_power(id: str, payload: NetworkPowerRequest):
    """
    Action Route: POST /network/v1/devices/{id}/power
    """
    import random
    import datetime
    collection_path = "/network/v1/devices"
    item = db.get_item(collection_path, id)
    if not item:
        raise HTTPException(status_code=404, detail="Device not found")
        
    device = dict(item)
    action_upper = payload.action.upper()
    if action_upper not in ["ON", "OFF"]:
        raise HTTPException(status_code=400, detail="Invalid action. Only 'ON' or 'OFF' are allowed.")
        
    device["power_state"] = action_upper
    if action_upper == "ON":
        device["cpu_utilization_percent"] = round(random.uniform(10.0, 90.0), 1)
        device["memory_utilization_percent"] = round(random.uniform(10.0, 90.0), 1)
        device["power_draw_watts"] = round(random.uniform(150.0, 400.0), 1)
        device["temperature_celsius"] = round(random.uniform(25.0, 45.0), 1)
    else:
        device["cpu_utilization_percent"] = 0.0
        device["memory_utilization_percent"] = 0.0
        device["power_draw_watts"] = 0.0
        device["temperature_celsius"] = 0.0
        
    device["updated_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S+05:30")
    db.upsert_item(collection_path, device["id"], device)
    return device

@app.post("/network/v1/devices/{id}/vlans")
def post_network_device_vlans(id: str, payload: NetworkVlanRequest):
    """
    Action Route: POST /network/v1/devices/{id}/vlans
    Adds a VLAN to the device. Idempotent: if the vlan_id already exists,
    updates its name rather than creating a duplicate entry.
    """
    import datetime
    collection_path = "/network/v1/devices"
    item = db.get_item(collection_path, id)
    if not item:
        raise HTTPException(status_code=404, detail="Device not found")

    device = dict(item)
    configured_vlans = device.get("configured_vlans") or []
    if isinstance(configured_vlans, str):
        try:
            configured_vlans = json.loads(configured_vlans)
        except Exception:
            configured_vlans = []
    elif not isinstance(configured_vlans, list):
        configured_vlans = []

    new_vlan = payload.dict()
    new_vlan_id = int(new_vlan["vlan_id"])
    
    # Deduplicate: rebuild list to filter out duplicates and enforce type safety
    filtered_vlans = []
    replaced = False
    for v in configured_vlans:
        if isinstance(v, dict):
            try:
                vid = int(v.get("vlan_id"))
                if vid == new_vlan_id:
                    if not replaced:
                        filtered_vlans.append(new_vlan)
                        replaced = True
                    # else skip to remove duplicates
                else:
                    filtered_vlans.append(v)
            except (ValueError, TypeError):
                filtered_vlans.append(v)
        else:
            filtered_vlans.append(v)
            
    if not replaced:
        filtered_vlans.append(new_vlan)
        
    configured_vlans = filtered_vlans

    device["configured_vlans"] = configured_vlans
    device["updated_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S+05:30")
    db.upsert_item(collection_path, device["id"], device)
    return device

def _resolve_port_key(ports: dict, requested_name: str) -> str:
    """
    Find the correct stored key for a port name that may have been URL-decoded,
    abbreviated, or slightly different from the stored form.
    Priority: exact match > case-insensitive match > fuzzy numeric suffix match.
    """
    if requested_name in ports:
        return requested_name
    lower = requested_name.lower()
    for key in ports:
        if key.lower() == lower:
            return key
    # Strip common prefixes and match by trailing number e.g. "3" from "GigabitEthernet1/0/3"
    import re
    req_num = re.search(r'(\d+)$', requested_name)
    if req_num:
        suffix = req_num.group(1)
        for key in ports:
            if re.search(r'(\d+)$', key) and re.search(r'(\d+)$', key).group(1) == suffix:
                return key
    # Fallback: use the requested name as-is (will create new entry)
    return requested_name


@app.post("/network/v1/devices/{id}/ports/{port_name:path}/status")
def post_network_device_port_status(id: str, port_name: str, payload: NetworkPortStatusRequest):
    """
    Action Route: POST /network/v1/devices/{id}/ports/{port_name}/status
    Supports slash-containing port names like GigabitEthernet1/0/3.
    """
    import datetime
    collection_path = "/network/v1/devices"
    item = db.get_item(collection_path, id)
    if not item:
        raise HTTPException(status_code=404, detail="Device not found")

    device = dict(item)
    ports = device.get("ports") or {}
    if isinstance(ports, str):
        try:
            ports = json.loads(ports)
        except Exception:
            ports = {}
    elif not isinstance(ports, dict):
        ports = {}

    # Strip trailing "/status" if the :path consumed it
    if port_name.endswith("/status"):
        port_name = port_name[:-len("/status")]

    resolved_key = _resolve_port_key(ports, port_name)
    new_status = payload.status.upper()
    ports[resolved_key] = new_status
    device["ports"] = ports
    device["updated_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S+05:30")
    db.upsert_item(collection_path, device["id"], device)
    return device


@app.get("/network/v1/devices/{id}/vlans")
def get_network_device_vlans(id: str):
    """
    GET the configured VLANs for a device.
    """
    collection_path = "/network/v1/devices"
    item = db.get_item(collection_path, id)
    if not item:
        raise HTTPException(status_code=404, detail="Device not found")
    vlans = item.get("configured_vlans") or []
    if isinstance(vlans, str):
        try:
            vlans = json.loads(vlans)
        except Exception:
            vlans = []
    return {"device_id": id, "configured_vlans": vlans, "count": len(vlans)}


@app.get("/monitoring/v1/switches")
def get_aruba_switches():
    """
    Aruba Central Endpoint: GET /monitoring/v1/switches
    Retrieves a comprehensive list of all switches available in the network. Use this endpoint for broad listing queries.
    """
    collection_path = "/network/v1/devices"
    devices = db.get_all(collection_path)
    switches = []
    for d in devices:
        switches.append({
            "serial": d.get("id"),
            "name": d.get("name"),
            "ip_address": d.get("ip_address"),
            "model": d.get("device_type", "AOS-CX-6300"),
            "status": d.get("health_status", "CONNECTED"),
            "power_state": d.get("power_state", "ON"),
            "cpu_utilization": d.get("cpu_utilization_percent"),
            "memory_utilization": d.get("memory_utilization_percent"),
            "temperature": d.get("temperature_celsius")
        })
    return {"switches": switches, "count": len(switches)}


@app.get("/monitoring/v1/switches/{serial}")
def get_aruba_switch_by_serial(serial: str):
    """
    Aruba Central Endpoint: GET /monitoring/v1/switches/{serial}
    """
    collection_path = "/network/v1/devices"
    item = db.get_item(collection_path, serial)
    if not item:
        raise HTTPException(status_code=404, detail="Switch not found")
    return {
        "serial": item.get("id"),
        "name": item.get("name"),
        "ip_address": item.get("ip_address"),
        "model": item.get("device_type", "AOS-CX-6300"),
        "status": item.get("health_status", "CONNECTED"),
        "power_state": item.get("power_state", "ON"),
        "cpu_utilization": item.get("cpu_utilization_percent"),
        "memory_utilization": item.get("memory_utilization_percent"),
        "temperature": item.get("temperature_celsius")
    }


@app.get("/monitoring/v1/switches/{serial}/ports")
def get_aruba_switch_ports(serial: str):
    """
    Aruba Central Endpoint: GET /monitoring/v1/switches/{serial}/ports
    """
    collection_path = "/network/v1/devices"
    item = db.get_item(collection_path, serial)
    if not item:
        raise HTTPException(status_code=404, detail="Switch not found")
    ports = item.get("ports") or {}
    if isinstance(ports, str):
        try:
            ports = json.loads(ports)
        except Exception:
            ports = {}
    return {"serial": serial, "ports": ports}


@app.get("/monitoring/v1/switches/{serial}/vlan")
def get_aruba_switch_vlans(serial: str):
    """
    Aruba Central Endpoint: GET /monitoring/v1/switches/{serial}/vlan
    """
    collection_path = "/network/v1/devices"
    item = db.get_item(collection_path, serial)
    if not item:
        raise HTTPException(status_code=404, detail="Switch not found")
    vlans = item.get("configured_vlans") or []
    if isinstance(vlans, str):
        try:
            vlans = json.loads(vlans)
        except Exception:
            vlans = []
    return {"serial": serial, "vlans": vlans}


@app.post("/monitoring/v1/switches/{serial}/vlan")
def post_aruba_switch_vlan(serial: str, payload: ArubaVlanRequest):
    """
    Aruba Central Endpoint: POST /monitoring/v1/switches/{serial}/vlan
    Adds a VLAN to the switch. Idempotent: same vlan_id updates the existing entry.
    """
    import datetime
    collection_path = "/network/v1/devices"
    item = db.get_item(collection_path, serial)
    if not item:
        raise HTTPException(status_code=404, detail="Switch not found")

    device = dict(item)
    configured_vlans = device.get("configured_vlans") or []
    if isinstance(configured_vlans, str):
        try:
            configured_vlans = json.loads(configured_vlans)
        except Exception:
            configured_vlans = []
    elif not isinstance(configured_vlans, list):
        configured_vlans = []

    new_vlan = payload.dict()
    existing_ids = [v.get("vlan_id") if isinstance(v, dict) else v for v in configured_vlans]
    if new_vlan["vlan_id"] in existing_ids:
        for i, v in enumerate(configured_vlans):
            if isinstance(v, dict) and v.get("vlan_id") == new_vlan["vlan_id"]:
                configured_vlans[i] = new_vlan
                break
    else:
        configured_vlans.append(new_vlan)

    device["configured_vlans"] = configured_vlans
    device["updated_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S+05:30")
    db.upsert_item(collection_path, device["id"], device)
    return {"serial": serial, "vlans": configured_vlans}


@app.post("/monitoring/v1/switches/{serial}/ports/{port_name:path}/status")
def post_aruba_switch_port_status(serial: str, port_name: str, payload: ArubaPortStatusRequest):
    """
    Aruba Central Endpoint: POST /monitoring/v1/switches/{serial}/ports/{port_name}/status
    Supports slash-containing port names like GigabitEthernet1/0/3.
    """
    import datetime
    collection_path = "/network/v1/devices"
    item = db.get_item(collection_path, serial)
    if not item:
        raise HTTPException(status_code=404, detail="Switch not found")

    device = dict(item)
    ports = device.get("ports") or {}
    if isinstance(ports, str):
        try:
            ports = json.loads(ports)
        except Exception:
            ports = {}
    elif not isinstance(ports, dict):
        ports = {}

    # Strip trailing "/status" if the :path consumed it
    if port_name.endswith("/status"):
        port_name = port_name[:-len("/status")]

    resolved_key = _resolve_port_key(ports, port_name)
    new_status = payload.status.upper()
    ports[resolved_key] = new_status
    device["ports"] = ports
    device["updated_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S+05:30")
    db.upsert_item(collection_path, device["id"], device)
    return {"serial": serial, "ports": ports}


@app.get("/monitoring/v1/switches/{serial}/vlans")
def get_aruba_switch_vlans(serial: str):
    """
    Aruba Central Endpoint: GET /monitoring/v1/switches/{serial}/vlans
    """
    collection_path = "/network/v1/devices"
    item = db.get_item(collection_path, serial)
    if not item:
        raise HTTPException(status_code=404, detail="Switch not found")
    vlans = item.get("configured_vlans") or []
    if isinstance(vlans, str):
        try:
            vlans = json.loads(vlans)
        except Exception:
            vlans = []
    return {"serial": serial, "vlans": vlans, "count": len(vlans)}

# --- AUTO-GENERATED MODELS IMPORT ---
from models import Aruba_initiatecxpoebouncev1_Request, Aruba_downloadreportlink_Request, Aruba_createzonesv1_Request, Aruba_initiatecxtraceroutev1_Request, Aruba_initiategwiperfv1_Request, Aruba_initiateaptcpv1_Request, Aruba_initiatecxpingv1_Request, Aruba_disconnectuserbymacapv1_Request, Aruba_deletewalltypesv1_Request, Aruba_importfloorsv1_Request, Aruba_initiateappingv1_Request, Aruba_initiatecxcabletestv1_Request, Aruba_removedevicesonfloorv1_Request, Aruba_placeplanneddevicesonfloorv1_Request, Aruba_initiatepvospoebouncev1_Request, Aruba_runaossshowcommandsv1_Request, Aruba_updateuserreport_Request, Aruba_updatewebhookv1_Request, Aruba_deletewallsv1_Request, Aruba_initiategwhttpv1_Request, Aruba_replaceimagev1_Request, Aruba_disconnectuserbynetworkapv1_Request, Aruba_runcxshowcommandsv1_Request, Aruba_changedeviceassignmentv1_Request, Aruba_initiatecxhttpv1_Request, Aruba_updatezonesv1_Request, Aruba_updateassettagdatabyassettagidv1_Request, Aruba_runapshowcommandsv1_Request, Aruba_initiateapspeedtestv1_Request, Aruba_rungwshowcommandsv1_Request, Aruba_disconnectclientbymacgwv1_Request, Aruba_initiatecxaaav1_Request, Aruba_clearalerts_Request, Aruba_initiategwportbouncev1_Request, Aruba_startaprangingscanv1_Request, Aruba_initiateapnslookupv1_Request, Aruba_deletezonesv1_Request, Aruba_createwebhookv1_Request, Aruba_initiateaphttpv1_Request, Aruba_deferalerts_Request, Aruba_putdeviceadminlocationv1_Request, Aruba_initiatepvosportbouncev1_Request, Aruba_setpriorityalerts_Request, Aruba_updatewalltypesv1_Request, Aruba_scalefloormapv1_Request, Aruba_generateaccesstoken_Request, Aruba_patchwebhookv1_Request, Aruba_initiatepvostraceroutev1_Request, Aruba_initiateaphttpsv1_Request, Aruba_initiateapaaav1_Request, Aruba_initiategwtraceroutev1_Request, Aruba_updatewallsv1_Request, Aruba_initiategwhttpsv1_Request, Aruba_updatefloormapv1_Request, Aruba_initiatecxportbouncev1_Request, Aruba_updatebuildingv1_Request, Aruba_rungatewaypingsweepv1_Request, Aruba_initiategwpingv1_Request, Aruba_initiategwpoebouncev1_Request, Aruba_initiateaptraceroutev1_Request, Aruba_createfloorv1_Request, Aruba_initiatepvospingv1_Request, Aruba_createwallsv1_Request, Aruba_placedevicesonfloorv1_Request, Aruba_removeplanneddevicesonfloorv1_Request, Aruba_createassettagdatabyassettagidv1_Request, Aruba_setactivealerts_Request, Aruba_createwalltypesv1_Request, Aruba_initiatepvoscabletestv1_Request

# --- AUTO-GENERATED ROUTES ---
@app.api_route("/as/token.oauth2", methods=["POST"])
def post_as_token_oauth2(payload: Aruba_generateaccesstoken_Request):
    """
    Aruba Central Endpoint: POST /as/token.oauth2
    """
    collection_path = "/as/token_oauth2"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("serial") or payload_dict.get("name") or str(uuid.uuid4())
    payload_dict["id"] = item_id
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/network-monitoring/v1/aps", methods=["GET"])
def get_network_monitoring_v1_aps():
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/aps
    Retrieves a comprehensive list of all access points (APs) available in the network. Use this endpoint for broad listing queries.
    """
    collection_path = "/network-monitoring/v1/aps"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_aps", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/radios", methods=["GET"])
def get_network_monitoring_v1_radios():
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/radios
    """
    collection_path = "/network-monitoring/v1/radios"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_radios", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/bssids", methods=["GET"])
def get_network_monitoring_v1_bssids():
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/bssids
    """
    collection_path = "/network-monitoring/v1/bssids"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_bssids", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/wlans", methods=["GET"])
def get_network_monitoring_v1_wlans():
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/wlans
    """
    collection_path = "/network-monitoring/v1/wlans"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_wlans", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/swarms", methods=["GET"])
def get_network_monitoring_v1_swarms():
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/swarms
    """
    collection_path = "/network-monitoring/v1/swarms"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_swarms", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/top-aps-by-wireless-usage", methods=["GET"])
def get_network_monitoring_v1_top_aps_by_wireless_usage():
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/top-aps-by-wireless-usage
    """
    collection_path = "/network-monitoring/v1/top-aps-by-wireless-usage"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_top_aps_by_wireless_usage", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/top-aps-by-wired-usage", methods=["GET"])
def get_network_monitoring_v1_top_aps_by_wired_usage():
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/top-aps-by-wired-usage
    """
    collection_path = "/network-monitoring/v1/top-aps-by-wired-usage"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_top_aps_by_wired_usage", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/top-aps-by-usage", methods=["GET"])
def get_network_monitoring_v1_top_aps_by_usage():
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/top-aps-by-usage
    """
    collection_path = "/network-monitoring/v1/top-aps-by-usage"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_top_aps_by_usage", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/aps/{serial_number}", methods=["GET"])
def get_network_monitoring_v1_aps_serial_number(serial_number: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/aps/{serial-number}
    """
    collection_path = f"/network-monitoring/v1/aps"
    item = db.get_item(collection_path, serial_number)
    if item:
        return item
    static_val = db.get_static("get_network_monitoring_v1_aps_serial_number")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-monitoring/v1/aps/{serial_number}/throughput-trends", methods=["GET"])
def get_network_monitoring_v1_aps_serial_number_throughput_trends(serial_number: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/aps/{serial-number}/throughput-trends
    """
    collection_path = f"/network-monitoring/v1/aps/{serial_number}/throughput-trends"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_aps_serial_number_throughput_trends", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/aps/{serial_number}/cpu-utilization-trends", methods=["GET"])
def get_network_monitoring_v1_aps_serial_number_cpu_utilization_trends(serial_number: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/aps/{serial-number}/cpu-utilization-trends
    """
    collection_path = f"/network-monitoring/v1/aps/{serial_number}/cpu-utilization-trends"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_aps_serial_number_cpu_utilization_trends", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/aps/{serial_number}/memory-utilization-trends", methods=["GET"])
def get_network_monitoring_v1_aps_serial_number_memory_utilization_trends(serial_number: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/aps/{serial-number}/memory-utilization-trends
    """
    collection_path = f"/network-monitoring/v1/aps/{serial_number}/memory-utilization-trends"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_aps_serial_number_memory_utilization_trends", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/aps/{serial_number}/power-consumption-trends", methods=["GET"])
def get_network_monitoring_v1_aps_serial_number_power_consumption_trends(serial_number: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/aps/{serial-number}/power-consumption-trends
    """
    collection_path = f"/network-monitoring/v1/aps/{serial_number}/power-consumption-trends"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_aps_serial_number_power_consumption_trends", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/aps/{serial_number}/radios", methods=["GET"])
def get_network_monitoring_v1_aps_serial_number_radios(serial_number: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/aps/{serial-number}/radios
    """
    collection_path = f"/network-monitoring/v1/aps/{serial_number}/radios"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_aps_serial_number_radios", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/aps/{serial_number}/radios/{radio_number}/throughput-trends", methods=["GET"])
def get_network_monitoring_v1_aps_serial_number_radios_radio_number_throughput_trends(serial_number: str, radio_number: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/aps/{serial-number}/radios/{radio-number}/throughput-trends
    """
    collection_path = f"/network-monitoring/v1/aps/{serial_number}/radios/{radio_number}/throughput-trends"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_aps_serial_number_radios_radio_number_throughput_trends", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/aps/{serial_number}/radios/{radio_number}/channel-utilization-trends", methods=["GET"])
def get_network_monitoring_v1_aps_serial_number_radios_radio_number_channel_utilization_trends(serial_number: str, radio_number: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/aps/{serial-number}/radios/{radio-number}/channel-utilization-trends
    """
    collection_path = f"/network-monitoring/v1/aps/{serial_number}/radios/{radio_number}/channel-utilization-trends"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_aps_serial_number_radios_radio_number_channel_utilization_trends", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/aps/{serial_number}/radios/{radio_number}/channel-quality-trends", methods=["GET"])
def get_network_monitoring_v1_aps_serial_number_radios_radio_number_channel_quality_trends(serial_number: str, radio_number: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/aps/{serial-number}/radios/{radio-number}/channel-quality-trends
    """
    collection_path = f"/network-monitoring/v1/aps/{serial_number}/radios/{radio_number}/channel-quality-trends"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_aps_serial_number_radios_radio_number_channel_quality_trends", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/aps/{serial_number}/radios/{radio_number}/noise-floor-trends", methods=["GET"])
def get_network_monitoring_v1_aps_serial_number_radios_radio_number_noise_floor_trends(serial_number: str, radio_number: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/aps/{serial-number}/radios/{radio-number}/noise-floor-trends
    """
    collection_path = f"/network-monitoring/v1/aps/{serial_number}/radios/{radio_number}/noise-floor-trends"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_aps_serial_number_radios_radio_number_noise_floor_trends", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/aps/{serial_number}/radios/{radio_number}/frames-trends", methods=["GET"])
def get_network_monitoring_v1_aps_serial_number_radios_radio_number_frames_trends(serial_number: str, radio_number: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/aps/{serial-number}/radios/{radio-number}/frames-trends
    """
    collection_path = f"/network-monitoring/v1/aps/{serial_number}/radios/{radio_number}/frames-trends"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_aps_serial_number_radios_radio_number_frames_trends", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/aps/{serial_number}/ports", methods=["GET"])
def get_network_monitoring_v1_aps_serial_number_ports(serial_number: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/aps/{serial-number}/ports
    """
    collection_path = f"/network-monitoring/v1/aps/{serial_number}/ports"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_aps_serial_number_ports", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/aps/{serial_number}/ports/{port_index}/throughput-trends", methods=["GET"])
def get_network_monitoring_v1_aps_serial_number_ports_port_index_throughput_trends(serial_number: str, port_index: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/aps/{serial-number}/ports/{port-index}/throughput-trends
    """
    collection_path = f"/network-monitoring/v1/aps/{serial_number}/ports/{port_index}/throughput-trends"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_aps_serial_number_ports_port_index_throughput_trends", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/aps/{serial_number}/ports/{port_index}/frames-trends", methods=["GET"])
def get_network_monitoring_v1_aps_serial_number_ports_port_index_frames_trends(serial_number: str, port_index: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/aps/{serial-number}/ports/{port-index}/frames-trends
    """
    collection_path = f"/network-monitoring/v1/aps/{serial_number}/ports/{port_index}/frames-trends"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_aps_serial_number_ports_port_index_frames_trends", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/aps/{serial_number}/ports/{port_index}/crc-trends", methods=["GET"])
def get_network_monitoring_v1_aps_serial_number_ports_port_index_crc_trends(serial_number: str, port_index: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/aps/{serial-number}/ports/{port-index}/crc-trends
    """
    collection_path = f"/network-monitoring/v1/aps/{serial_number}/ports/{port_index}/crc-trends"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_aps_serial_number_ports_port_index_crc_trends", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/aps/{serial_number}/ports/{port_index}/collisions-trends", methods=["GET"])
def get_network_monitoring_v1_aps_serial_number_ports_port_index_collisions_trends(serial_number: str, port_index: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/aps/{serial-number}/ports/{port-index}/collisions-trends
    """
    collection_path = f"/network-monitoring/v1/aps/{serial_number}/ports/{port_index}/collisions-trends"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_aps_serial_number_ports_port_index_collisions_trends", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/aps/{serial_number}/tunnels", methods=["GET"])
def get_network_monitoring_v1_aps_serial_number_tunnels(serial_number: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/aps/{serial-number}/tunnels
    """
    collection_path = f"/network-monitoring/v1/aps/{serial_number}/tunnels"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_aps_serial_number_tunnels", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/aps/{serial_number}/tunnels/{tunnel_id}", methods=["GET"])
def get_network_monitoring_v1_aps_serial_number_tunnels_tunnel_id(serial_number: str, tunnel_id: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/aps/{serial-number}/tunnels/{tunnel-id}
    """
    collection_path = f"/network-monitoring/v1/aps/{serial_number}/tunnels"
    item = db.get_item(collection_path, tunnel_id)
    if item:
        return item
    static_val = db.get_static("get_network_monitoring_v1_aps_serial_number_tunnels_tunnel_id")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-monitoring/v1/aps/{serial_number}/tunnels/{tunnel_id}/throughput-trends", methods=["GET"])
def get_network_monitoring_v1_aps_serial_number_tunnels_tunnel_id_throughput_trends(serial_number: str, tunnel_id: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/aps/{serial-number}/tunnels/{tunnel-id}/throughput-trends
    """
    collection_path = f"/network-monitoring/v1/aps/{serial_number}/tunnels/{tunnel_id}/throughput-trends"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_aps_serial_number_tunnels_tunnel_id_throughput_trends", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/aps/{serial_number}/tunnels/{tunnel_id}/packet-loss-trends", methods=["GET"])
def get_network_monitoring_v1_aps_serial_number_tunnels_tunnel_id_packet_loss_trends(serial_number: str, tunnel_id: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/aps/{serial-number}/tunnels/{tunnel-id}/packet-loss-trends
    """
    collection_path = f"/network-monitoring/v1/aps/{serial_number}/tunnels/{tunnel_id}/packet-loss-trends"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_aps_serial_number_tunnels_tunnel_id_packet_loss_trends", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/aps/{serial_number}/tunnels/{tunnel_id}/mos-trends", methods=["GET"])
def get_network_monitoring_v1_aps_serial_number_tunnels_tunnel_id_mos_trends(serial_number: str, tunnel_id: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/aps/{serial-number}/tunnels/{tunnel-id}/mos-trends
    """
    collection_path = f"/network-monitoring/v1/aps/{serial_number}/tunnels/{tunnel_id}/mos-trends"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_aps_serial_number_tunnels_tunnel_id_mos_trends", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/aps/{serial_number}/tunnels/{tunnel_id}/jitter-trends", methods=["GET"])
def get_network_monitoring_v1_aps_serial_number_tunnels_tunnel_id_jitter_trends(serial_number: str, tunnel_id: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/aps/{serial-number}/tunnels/{tunnel-id}/jitter-trends
    """
    collection_path = f"/network-monitoring/v1/aps/{serial_number}/tunnels/{tunnel_id}/jitter-trends"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_aps_serial_number_tunnels_tunnel_id_jitter_trends", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/aps/{serial_number}/tunnels/{tunnel_id}/latency-trends", methods=["GET"])
def get_network_monitoring_v1_aps_serial_number_tunnels_tunnel_id_latency_trends(serial_number: str, tunnel_id: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/aps/{serial-number}/tunnels/{tunnel-id}/latency-trends
    """
    collection_path = f"/network-monitoring/v1/aps/{serial_number}/tunnels/{tunnel_id}/latency-trends"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_aps_serial_number_tunnels_tunnel_id_latency_trends", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/aps/{serial_number}/wlans", methods=["GET"])
def get_network_monitoring_v1_aps_serial_number_wlans(serial_number: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/aps/{serial-number}/wlans
    """
    collection_path = f"/network-monitoring/v1/aps/{serial_number}/wlans"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_aps_serial_number_wlans", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/aps/{serial_number}/wlans/{wlan_name}/throughput-trends", methods=["GET"])
def get_network_monitoring_v1_aps_serial_number_wlans_wlan_name_throughput_trends(serial_number: str, wlan_name: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/aps/{serial-number}/wlans/{wlan-name}/throughput-trends
    """
    collection_path = f"/network-monitoring/v1/aps/{serial_number}/wlans/{wlan_name}/throughput-trends"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_aps_serial_number_wlans_wlan_name_throughput_trends", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/wlans/{wlan_name}", methods=["GET"])
def get_network_monitoring_v1_wlans_wlan_name(wlan_name: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/wlans/{wlan-name}
    """
    collection_path = f"/network-monitoring/v1/wlans"
    item = db.get_item(collection_path, wlan_name)
    if item:
        return item
    static_val = db.get_static("get_network_monitoring_v1_wlans_wlan_name")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-monitoring/v1/wlans/{wlan_name}/throughput-trends", methods=["GET"])
def get_network_monitoring_v1_wlans_wlan_name_throughput_trends(wlan_name: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/wlans/{wlan-name}/throughput-trends
    """
    collection_path = f"/network-monitoring/v1/wlans/{wlan_name}/throughput-trends"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_wlans_wlan_name_throughput_trends", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/swarms/{cluster_id}", methods=["GET"])
def get_network_monitoring_v1_swarms_cluster_id(cluster_id: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/swarms/{cluster-id}
    """
    collection_path = f"/network-monitoring/v1/swarms"
    item = db.get_item(collection_path, cluster_id)
    if item:
        return item
    static_val = db.get_static("get_network_monitoring_v1_swarms_cluster_id")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-monitoring/v1/applications", methods=["GET"])
def get_network_monitoring_v1_applications():
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/applications
    """
    collection_path = "/network-monitoring/v1/applications"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_applications", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/client-onboarding-score", methods=["GET"])
def get_network_monitoring_v1_client_onboarding_score():
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/client-onboarding-score
    """
    collection_path = "/network-monitoring/v1/client-onboarding-score"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_client_onboarding_score", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/client-onboarding-stage/export", methods=["GET"])
def get_network_monitoring_v1_client_onboarding_stage_export():
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/client-onboarding-stage/export
    """
    collection_path = "/network-monitoring/v1/client-onboarding-stage/export"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_client_onboarding_stage_export", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/client-onboarding-stage/reasons", methods=["GET"])
def get_network_monitoring_v1_client_onboarding_stage_reasons():
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/client-onboarding-stage/reasons
    """
    collection_path = "/network-monitoring/v1/client-onboarding-stage/reasons"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_client_onboarding_stage_reasons", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/client-onboarding-stage/count", methods=["GET"])
def get_network_monitoring_v1_client_onboarding_stage_count():
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/client-onboarding-stage/count
    """
    collection_path = "/network-monitoring/v1/client-onboarding-stage/count"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_client_onboarding_stage_count", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/clients", methods=["GET"])
def get_network_monitoring_v1_clients():
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/clients
    """
    collection_path = "/network-monitoring/v1/clients"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_clients", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/clients-trend", methods=["GET"])
def get_network_monitoring_v1_clients_trend():
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/clients-trend
    """
    collection_path = "/network-monitoring/v1/clients-trend"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_clients_trend", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/clients-topn-usage", methods=["GET"])
def get_network_monitoring_v1_clients_topn_usage():
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/clients-topn-usage
    """
    collection_path = "/network-monitoring/v1/clients-topn-usage"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_clients_topn_usage", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/clients-usage", methods=["GET"])
def get_network_monitoring_v1_clients_usage():
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/clients-usage
    """
    collection_path = "/network-monitoring/v1/clients-usage"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_clients_usage", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/clients/{mac_address}", methods=["GET"])
def get_network_monitoring_v1_clients_mac_address(mac_address: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/clients/{mac-address}
    """
    collection_path = f"/network-monitoring/v1/clients"
    item = db.get_item(collection_path, mac_address)
    if item:
        return item
    static_val = db.get_static("get_network_monitoring_v1_clients_mac_address")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-monitoring/v1/clients/{mac_address}/mobility-trail", methods=["GET"])
def get_network_monitoring_v1_clients_mac_address_mobility_trail(mac_address: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/clients/{mac-address}/mobility-trail
    """
    collection_path = f"/network-monitoring/v1/clients/{mac_address}/mobility-trail"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_clients_mac_address_mobility_trail", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/devices", methods=["GET"])
def get_network_monitoring_v1_devices():
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/devices
    """
    collection_path = "/network-monitoring/v1/devices"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_devices", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/devices/{serial_number}", methods=["PATCH"])
def patch_network_monitoring_v1_devices_serial_number(serial_number: str):
    """
    Aruba Central Endpoint: PATCH /network-monitoring/v1/devices/{serial-number}
    """
    collection_path = f"/network-monitoring/v1/devices"
    payload_dict = {}
    existing = db.get_item(collection_path, serial_number) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, serial_number, existing)
    return existing

@app.api_route("/network-monitoring/v1/devices/{serial_number}", methods=["DELETE"])
def delete_network_monitoring_v1_devices_serial_number(serial_number: str):
    """
    Aruba Central Endpoint: DELETE /network-monitoring/v1/devices/{serial-number}
    """
    collection_path = f"/network-monitoring/v1/devices"
    deleted = db.delete_item(collection_path, serial_number)
    if deleted:
        return {"message": "Deleted successfully", "id": serial_number, "item": deleted}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-monitoring/v1/device-inventory", methods=["GET"])
def get_network_monitoring_v1_device_inventory():
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/device-inventory
    """
    collection_path = "/network-monitoring/v1/device-inventory"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_device_inventory", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/site-firewall-sessions", methods=["GET"])
def get_network_monitoring_v1_site_firewall_sessions():
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/site-firewall-sessions
    """
    collection_path = "/network-monitoring/v1/site-firewall-sessions"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_site_firewall_sessions", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/client-firewall-sessions", methods=["GET"])
def get_network_monitoring_v1_client_firewall_sessions():
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/client-firewall-sessions
    """
    collection_path = "/network-monitoring/v1/client-firewall-sessions"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_client_firewall_sessions", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/firewall-clients", methods=["GET"])
def get_network_monitoring_v1_firewall_clients():
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/firewall-clients
    """
    collection_path = "/network-monitoring/v1/firewall-clients"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_firewall_clients", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/sitemaps-summary/{site_id}", methods=["GET"])
def get_network_monitoring_v1_sitemaps_summary_site_id(site_id: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/sitemaps-summary/{site-id}
    """
    collection_path = f"/network-monitoring/v1/sitemaps-summary"
    item = db.get_item(collection_path, site_id)
    if item:
        return item
    static_val = db.get_static("get_network_monitoring_v1_sitemaps_summary_site_id")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-monitoring/v1/sitemaps/{site_id}/network-devices-deployed", methods=["POST"])
def post_network_monitoring_v1_sitemaps_site_id_network_devices_deployed(site_id: str, payload: Aruba_placedevicesonfloorv1_Request):
    """
    Aruba Central Endpoint: POST /network-monitoring/v1/sitemaps/{site-id}/network-devices-deployed
    """
    collection_path = f"/network-monitoring/v1/sitemaps/{site_id}/network-devices-deployed"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = db.get_item(collection_path, site_id) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, site_id, existing)
    return existing

@app.api_route("/network-monitoring/v1/sitemaps/{site_id}/network-devices-deployed", methods=["GET"])
def get_network_monitoring_v1_sitemaps_site_id_network_devices_deployed(site_id: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/sitemaps/{site-id}/network-devices-deployed
    """
    collection_path = f"/network-monitoring/v1/sitemaps/{site_id}/network-devices-deployed"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_sitemaps_site_id_network_devices_deployed", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/sitemaps/{site_id}/network-devices-undeploy", methods=["POST"])
def post_network_monitoring_v1_sitemaps_site_id_network_devices_undeploy(site_id: str, payload: Aruba_removedevicesonfloorv1_Request):
    """
    Aruba Central Endpoint: POST /network-monitoring/v1/sitemaps/{site-id}/network-devices-undeploy
    """
    collection_path = f"/network-monitoring/v1/sitemaps/{site_id}/network-devices-undeploy"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = db.get_item(collection_path, site_id) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, site_id, existing)
    return existing

@app.api_route("/network-monitoring/v1/sitemaps/{site_id}/network-devices-assigned", methods=["POST"])
def post_network_monitoring_v1_sitemaps_site_id_network_devices_assigned(site_id: str, payload: Aruba_changedeviceassignmentv1_Request):
    """
    Aruba Central Endpoint: POST /network-monitoring/v1/sitemaps/{site-id}/network-devices-assigned
    """
    collection_path = f"/network-monitoring/v1/sitemaps/{site_id}/network-devices-assigned"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = db.get_item(collection_path, site_id) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, site_id, existing)
    return existing

@app.api_route("/network-monitoring/v1/sitemaps/{site_id}/network-devices-assigned", methods=["GET"])
def get_network_monitoring_v1_sitemaps_site_id_network_devices_assigned(site_id: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/sitemaps/{site-id}/network-devices-assigned
    """
    collection_path = f"/network-monitoring/v1/sitemaps/{site_id}/network-devices-assigned"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_sitemaps_site_id_network_devices_assigned", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/sitemaps/{site_id}/network-devices-planned", methods=["POST"])
def post_network_monitoring_v1_sitemaps_site_id_network_devices_planned(site_id: str, payload: Aruba_placeplanneddevicesonfloorv1_Request):
    """
    Aruba Central Endpoint: POST /network-monitoring/v1/sitemaps/{site-id}/network-devices-planned
    """
    collection_path = f"/network-monitoring/v1/sitemaps/{site_id}/network-devices-planned"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = db.get_item(collection_path, site_id) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, site_id, existing)
    return existing

@app.api_route("/network-monitoring/v1/sitemaps/{site_id}/network-devices-planned", methods=["GET"])
def get_network_monitoring_v1_sitemaps_site_id_network_devices_planned(site_id: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/sitemaps/{site-id}/network-devices-planned
    """
    collection_path = f"/network-monitoring/v1/sitemaps/{site_id}/network-devices-planned"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_sitemaps_site_id_network_devices_planned", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/sitemaps/{site_id}/network-devices-planned", methods=["DELETE"])
def delete_network_monitoring_v1_sitemaps_site_id_network_devices_planned(site_id: str, payload: Aruba_removeplanneddevicesonfloorv1_Request):
    """
    Aruba Central Endpoint: DELETE /network-monitoring/v1/sitemaps/{site-id}/network-devices-planned
    """
    collection_path = f"/network-monitoring/v1/sitemaps/{site_id}/network-devices-planned"
    deleted = db.delete_item(collection_path, site_id)
    if deleted:
        return {"message": "Deleted successfully", "id": site_id, "item": deleted}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-monitoring/v1/catalogue-aps", methods=["GET"])
def get_network_monitoring_v1_catalogue_aps():
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/catalogue-aps
    """
    collection_path = "/network-monitoring/v1/catalogue-aps"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_catalogue_aps", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/sitemaps/sites", methods=["GET"])
def get_network_monitoring_v1_sitemaps_sites():
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/sitemaps/sites
    """
    collection_path = "/network-monitoring/v1/sitemaps/sites"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_sitemaps_sites", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/sitemaps/{site_id}/floors", methods=["POST"])
def post_network_monitoring_v1_sitemaps_site_id_floors(site_id: str, payload: Aruba_createfloorv1_Request):
    """
    Aruba Central Endpoint: POST /network-monitoring/v1/sitemaps/{site-id}/floors
    """
    collection_path = f"/network-monitoring/v1/sitemaps/{site_id}/floors"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = db.get_item(collection_path, site_id) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, site_id, existing)
    return existing

@app.api_route("/network-monitoring/v1/sitemaps/{site_id}/floors/{floor_id}", methods=["DELETE"])
def delete_network_monitoring_v1_sitemaps_site_id_floors_floor_id(site_id: str, floor_id: str):
    """
    Aruba Central Endpoint: DELETE /network-monitoring/v1/sitemaps/{site-id}/floors/{floor-id}
    """
    collection_path = f"/network-monitoring/v1/sitemaps/{site_id}/floors"
    deleted = db.delete_item(collection_path, floor_id)
    if deleted:
        return {"message": "Deleted successfully", "id": floor_id, "item": deleted}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-monitoring/v1/sitemaps/{site_id}/floors/{floor_id}", methods=["GET"])
def get_network_monitoring_v1_sitemaps_site_id_floors_floor_id(site_id: str, floor_id: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/sitemaps/{site-id}/floors/{floor-id}
    """
    collection_path = f"/network-monitoring/v1/sitemaps/{site_id}/floors"
    item = db.get_item(collection_path, floor_id)
    if item:
        return item
    static_val = db.get_static("get_network_monitoring_v1_sitemaps_site_id_floors_floor_id")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-monitoring/v1/sitemaps/{site_id}/floors/{floor_id}", methods=["PUT"])
def put_network_monitoring_v1_sitemaps_site_id_floors_floor_id(site_id: str, floor_id: str, payload: Aruba_updatefloormapv1_Request):
    """
    Aruba Central Endpoint: PUT /network-monitoring/v1/sitemaps/{site-id}/floors/{floor-id}
    """
    collection_path = f"/network-monitoring/v1/sitemaps/{site_id}/floors"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = db.get_item(collection_path, floor_id) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, floor_id, existing)
    return existing

@app.api_route("/network-monitoring/v1/sitemaps/{site_id}/floors/{floor_id}/scale", methods=["POST"])
def post_network_monitoring_v1_sitemaps_site_id_floors_floor_id_scale(site_id: str, floor_id: str, payload: Aruba_scalefloormapv1_Request):
    """
    Aruba Central Endpoint: POST /network-monitoring/v1/sitemaps/{site-id}/floors/{floor-id}/scale
    """
    collection_path = f"/network-monitoring/v1/sitemaps/{site_id}/floors/{floor_id}/scale"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = db.get_item(collection_path, floor_id) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, floor_id, existing)
    return existing

@app.api_route("/network-monitoring/v1/sitemaps/{site_id}/floors/{floor_id}/image", methods=["GET"])
def get_network_monitoring_v1_sitemaps_site_id_floors_floor_id_image(site_id: str, floor_id: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/sitemaps/{site-id}/floors/{floor-id}/image
    """
    collection_path = f"/network-monitoring/v1/sitemaps/{site_id}/floors/{floor_id}/image"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_sitemaps_site_id_floors_floor_id_image", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/sitemaps/{site_id}/floors/{floor_id}/image", methods=["PUT"])
def put_network_monitoring_v1_sitemaps_site_id_floors_floor_id_image(site_id: str, floor_id: str, payload: Aruba_replaceimagev1_Request):
    """
    Aruba Central Endpoint: PUT /network-monitoring/v1/sitemaps/{site-id}/floors/{floor-id}/image
    """
    collection_path = f"/network-monitoring/v1/sitemaps/{site_id}/floors/{floor_id}/image"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = db.get_item(collection_path, floor_id) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, floor_id, existing)
    return existing

@app.api_route("/network-monitoring/v1/sitemaps/{site_id}/buildings", methods=["GET"])
def get_network_monitoring_v1_sitemaps_site_id_buildings(site_id: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/sitemaps/{site-id}/buildings
    """
    collection_path = f"/network-monitoring/v1/sitemaps/{site_id}/buildings"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_sitemaps_site_id_buildings", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/sitemaps/{site_id}/buildings/{building_id}", methods=["DELETE"])
def delete_network_monitoring_v1_sitemaps_site_id_buildings_building_id(site_id: str, building_id: str):
    """
    Aruba Central Endpoint: DELETE /network-monitoring/v1/sitemaps/{site-id}/buildings/{building-id}
    """
    collection_path = f"/network-monitoring/v1/sitemaps/{site_id}/buildings"
    deleted = db.delete_item(collection_path, building_id)
    if deleted:
        return {"message": "Deleted successfully", "id": building_id, "item": deleted}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-monitoring/v1/sitemaps/{site_id}/buildings/{building_id}", methods=["PUT"])
def put_network_monitoring_v1_sitemaps_site_id_buildings_building_id(site_id: str, building_id: str, payload: Aruba_updatebuildingv1_Request):
    """
    Aruba Central Endpoint: PUT /network-monitoring/v1/sitemaps/{site-id}/buildings/{building-id}
    """
    collection_path = f"/network-monitoring/v1/sitemaps/{site_id}/buildings"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = db.get_item(collection_path, building_id) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, building_id, existing)
    return existing

@app.api_route("/network-monitoring/v1/sitemaps/{site_id}/import", methods=["POST"])
def post_network_monitoring_v1_sitemaps_site_id_import(site_id: str, payload: Aruba_importfloorsv1_Request):
    """
    Aruba Central Endpoint: POST /network-monitoring/v1/sitemaps/{site-id}/import
    """
    collection_path = f"/network-monitoring/v1/sitemaps/{site_id}/import"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = db.get_item(collection_path, site_id) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, site_id, existing)
    return existing

@app.api_route("/network-monitoring/v1/sitemaps/{site_id}/import/{id}", methods=["GET"])
def get_network_monitoring_v1_sitemaps_site_id_import_id(site_id: str, id: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/sitemaps/{site-id}/import/{id}
    """
    collection_path = f"/network-monitoring/v1/sitemaps/{site_id}/import"
    item = db.get_item(collection_path, id)
    if item:
        return item
    static_val = db.get_static("get_network_monitoring_v1_sitemaps_site_id_import_id")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-monitoring/v1/wall-types", methods=["GET"])
def get_network_monitoring_v1_wall_types():
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/wall-types
    """
    collection_path = "/network-monitoring/v1/wall-types"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_wall_types", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/wall-types", methods=["POST"])
def post_network_monitoring_v1_wall_types(payload: Aruba_createwalltypesv1_Request):
    """
    Aruba Central Endpoint: POST /network-monitoring/v1/wall-types
    """
    collection_path = "/network-monitoring/v1/wall-types"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("serial") or payload_dict.get("name") or str(uuid.uuid4())
    payload_dict["id"] = item_id
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/network-monitoring/v1/wall-types", methods=["PUT"])
def put_network_monitoring_v1_wall_types(payload: Aruba_updatewalltypesv1_Request):
    """
    Aruba Central Endpoint: PUT /network-monitoring/v1/wall-types
    """
    collection_path = "/network-monitoring/v1/wall-types"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("serial") or payload_dict.get("name") or str(uuid.uuid4())
    payload_dict["id"] = item_id
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/network-monitoring/v1/wall-types", methods=["DELETE"])
def delete_network_monitoring_v1_wall_types(payload: Aruba_deletewalltypesv1_Request):
    """
    Aruba Central Endpoint: DELETE /network-monitoring/v1/wall-types
    """
    collection_path = "/network-monitoring/v1/wall-types"
    return {"message": "Deletion requested"}

@app.api_route("/network-monitoring/v1/sitemaps/{site_id}/floors/{floor_id}/walls", methods=["GET"])
def get_network_monitoring_v1_sitemaps_site_id_floors_floor_id_walls(site_id: str, floor_id: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/sitemaps/{site-id}/floors/{floor-id}/walls
    """
    collection_path = f"/network-monitoring/v1/sitemaps/{site_id}/floors/{floor_id}/walls"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_sitemaps_site_id_floors_floor_id_walls", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/sitemaps/{site_id}/floors/{floor_id}/walls", methods=["POST"])
def post_network_monitoring_v1_sitemaps_site_id_floors_floor_id_walls(site_id: str, floor_id: str, payload: Aruba_createwallsv1_Request):
    """
    Aruba Central Endpoint: POST /network-monitoring/v1/sitemaps/{site-id}/floors/{floor-id}/walls
    """
    collection_path = f"/network-monitoring/v1/sitemaps/{site_id}/floors/{floor_id}/walls"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = db.get_item(collection_path, floor_id) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, floor_id, existing)
    return existing

@app.api_route("/network-monitoring/v1/sitemaps/{site_id}/floors/{floor_id}/walls", methods=["PUT"])
def put_network_monitoring_v1_sitemaps_site_id_floors_floor_id_walls(site_id: str, floor_id: str, payload: Aruba_updatewallsv1_Request):
    """
    Aruba Central Endpoint: PUT /network-monitoring/v1/sitemaps/{site-id}/floors/{floor-id}/walls
    """
    collection_path = f"/network-monitoring/v1/sitemaps/{site_id}/floors/{floor_id}/walls"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = db.get_item(collection_path, floor_id) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, floor_id, existing)
    return existing

@app.api_route("/network-monitoring/v1/sitemaps/{site_id}/floors/{floor_id}/walls", methods=["DELETE"])
def delete_network_monitoring_v1_sitemaps_site_id_floors_floor_id_walls(site_id: str, floor_id: str, payload: Aruba_deletewallsv1_Request):
    """
    Aruba Central Endpoint: DELETE /network-monitoring/v1/sitemaps/{site-id}/floors/{floor-id}/walls
    """
    collection_path = f"/network-monitoring/v1/sitemaps/{site_id}/floors/{floor_id}/walls"
    deleted = db.delete_item(collection_path, floor_id)
    if deleted:
        return {"message": "Deleted successfully", "id": floor_id, "item": deleted}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-monitoring/v1/sitemaps/{site_id}/floors/{floor_id}/zones", methods=["GET"])
def get_network_monitoring_v1_sitemaps_site_id_floors_floor_id_zones(site_id: str, floor_id: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/sitemaps/{site-id}/floors/{floor-id}/zones
    """
    collection_path = f"/network-monitoring/v1/sitemaps/{site_id}/floors/{floor_id}/zones"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_sitemaps_site_id_floors_floor_id_zones", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/sitemaps/{site_id}/floors/{floor_id}/zones", methods=["POST"])
def post_network_monitoring_v1_sitemaps_site_id_floors_floor_id_zones(site_id: str, floor_id: str, payload: Aruba_createzonesv1_Request):
    """
    Aruba Central Endpoint: POST /network-monitoring/v1/sitemaps/{site-id}/floors/{floor-id}/zones
    """
    collection_path = f"/network-monitoring/v1/sitemaps/{site_id}/floors/{floor_id}/zones"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = db.get_item(collection_path, floor_id) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, floor_id, existing)
    return existing

@app.api_route("/network-monitoring/v1/sitemaps/{site_id}/floors/{floor_id}/zones", methods=["PUT"])
def put_network_monitoring_v1_sitemaps_site_id_floors_floor_id_zones(site_id: str, floor_id: str, payload: Aruba_updatezonesv1_Request):
    """
    Aruba Central Endpoint: PUT /network-monitoring/v1/sitemaps/{site-id}/floors/{floor-id}/zones
    """
    collection_path = f"/network-monitoring/v1/sitemaps/{site_id}/floors/{floor_id}/zones"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = db.get_item(collection_path, floor_id) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, floor_id, existing)
    return existing

@app.api_route("/network-monitoring/v1/sitemaps/{site_id}/floors/{floor_id}/zones", methods=["DELETE"])
def delete_network_monitoring_v1_sitemaps_site_id_floors_floor_id_zones(site_id: str, floor_id: str, payload: Aruba_deletezonesv1_Request):
    """
    Aruba Central Endpoint: DELETE /network-monitoring/v1/sitemaps/{site-id}/floors/{floor-id}/zones
    """
    collection_path = f"/network-monitoring/v1/sitemaps/{site_id}/floors/{floor_id}/zones"
    deleted = db.delete_item(collection_path, floor_id)
    if deleted:
        return {"message": "Deleted successfully", "id": floor_id, "item": deleted}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-monitoring/v1/gateways", methods=["GET"])
def get_network_monitoring_v1_gateways():
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/gateways
    Retrieves a comprehensive list of all gateways available in the network. Use this endpoint for broad listing queries.
    """
    collection_path = "/network-monitoring/v1/gateways"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_gateways", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/gateways/{serial_number}", methods=["GET"])
def get_network_monitoring_v1_gateways_serial_number(serial_number: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/gateways/{serial-number}
    """
    collection_path = f"/network-monitoring/v1/gateways"
    item = db.get_item(collection_path, serial_number)
    if item:
        return item
    static_val = db.get_static("get_network_monitoring_v1_gateways_serial_number")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-monitoring/v1/clusters/{cluster_name}/vlan-mismatch", methods=["GET"])
def get_network_monitoring_v1_clusters_cluster_name_vlan_mismatch(cluster_name: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/clusters/{cluster-name}/vlan-mismatch
    """
    collection_path = f"/network-monitoring/v1/clusters/{cluster_name}/vlan-mismatch"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_clusters_cluster_name_vlan_mismatch", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/clusters/{cluster_name}/connectivity-graph", methods=["GET"])
def get_network_monitoring_v1_clusters_cluster_name_connectivity_graph(cluster_name: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/clusters/{cluster-name}/connectivity-graph
    """
    collection_path = f"/network-monitoring/v1/clusters/{cluster_name}/connectivity-graph"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_clusters_cluster_name_connectivity_graph", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/gateways/{serial_number}/vlans/{vlan_id}", methods=["GET"])
def get_network_monitoring_v1_gateways_serial_number_vlans_vlan_id(serial_number: str, vlan_id: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/gateways/{serial-number}/vlans/{vlan-id}
    """
    collection_path = f"/network-monitoring/v1/gateways/{serial_number}/vlans"
    item = db.get_item(collection_path, vlan_id)
    if item:
        return item
    static_val = db.get_static("get_network_monitoring_v1_gateways_serial_number_vlans_vlan_id")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-monitoring/v1/clusters/{cluster_name}/members", methods=["GET"])
def get_network_monitoring_v1_clusters_cluster_name_members(cluster_name: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/clusters/{cluster-name}/members
    """
    collection_path = f"/network-monitoring/v1/clusters/{cluster_name}/members"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_clusters_cluster_name_members", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/gateways/{serial_number}/tunnels/{tunnel_name}", methods=["GET"])
def get_network_monitoring_v1_gateways_serial_number_tunnels_tunnel_name(serial_number: str, tunnel_name: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/gateways/{serial-number}/tunnels/{tunnel-name}
    """
    collection_path = f"/network-monitoring/v1/gateways/{serial_number}/tunnels"
    item = db.get_item(collection_path, tunnel_name)
    if item:
        return item
    static_val = db.get_static("get_network_monitoring_v1_gateways_serial_number_tunnels_tunnel_name")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-monitoring/v1/gateways/{serial_number}/ports", methods=["GET"])
def get_network_monitoring_v1_gateways_serial_number_ports(serial_number: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/gateways/{serial-number}/ports
    """
    collection_path = f"/network-monitoring/v1/gateways/{serial_number}/ports"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_gateways_serial_number_ports", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/gateways/{serial_number}/ports/{port_number}", methods=["GET"])
def get_network_monitoring_v1_gateways_serial_number_ports_port_number(serial_number: str, port_number: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/gateways/{serial-number}/ports/{port-number}
    """
    collection_path = f"/network-monitoring/v1/gateways/{serial_number}/ports"
    item = db.get_item(collection_path, port_number)
    if item:
        return item
    static_val = db.get_static("get_network_monitoring_v1_gateways_serial_number_ports_port_number")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-monitoring/v1/clusters/{cluster_name}/tunnels", methods=["GET"])
def get_network_monitoring_v1_clusters_cluster_name_tunnels(cluster_name: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/clusters/{cluster-name}/tunnels
    """
    collection_path = f"/network-monitoring/v1/clusters/{cluster_name}/tunnels"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_clusters_cluster_name_tunnels", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/gateways/{serial_number}/vlans", methods=["GET"])
def get_network_monitoring_v1_gateways_serial_number_vlans(serial_number: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/gateways/{serial-number}/vlans
    """
    collection_path = f"/network-monitoring/v1/gateways/{serial_number}/vlans"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_gateways_serial_number_vlans", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/gateways/{serial_number}/tunnels", methods=["GET"])
def get_network_monitoring_v1_gateways_serial_number_tunnels(serial_number: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/gateways/{serial-number}/tunnels
    """
    collection_path = f"/network-monitoring/v1/gateways/{serial_number}/tunnels"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_gateways_serial_number_tunnels", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/gateways/{serial_number}/uplinks", methods=["GET"])
def get_network_monitoring_v1_gateways_serial_number_uplinks(serial_number: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/gateways/{serial-number}/uplinks
    """
    collection_path = f"/network-monitoring/v1/gateways/{serial_number}/uplinks"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_gateways_serial_number_uplinks", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/gateways/{serial_number}/cpu-utilization-trends", methods=["GET"])
def get_network_monitoring_v1_gateways_serial_number_cpu_utilization_trends(serial_number: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/gateways/{serial-number}/cpu-utilization-trends
    """
    collection_path = f"/network-monitoring/v1/gateways/{serial_number}/cpu-utilization-trends"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_gateways_serial_number_cpu_utilization_trends", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/gateways/{serial_number}/memory-utilization-trends", methods=["GET"])
def get_network_monitoring_v1_gateways_serial_number_memory_utilization_trends(serial_number: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/gateways/{serial-number}/memory-utilization-trends
    """
    collection_path = f"/network-monitoring/v1/gateways/{serial_number}/memory-utilization-trends"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_gateways_serial_number_memory_utilization_trends", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/gateways/{serial_number}/tunnels/{tunnel_name}/throughput-trends", methods=["GET"])
def get_network_monitoring_v1_gateways_serial_number_tunnels_tunnel_name_throughput_trends(serial_number: str, tunnel_name: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/gateways/{serial-number}/tunnels/{tunnel-name}/throughput-trends
    """
    collection_path = f"/network-monitoring/v1/gateways/{serial_number}/tunnels/{tunnel_name}/throughput-trends"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_gateways_serial_number_tunnels_tunnel_name_throughput_trends", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/gateways/{serial_number}/tunnels/{tunnel_name}/status-trends", methods=["GET"])
def get_network_monitoring_v1_gateways_serial_number_tunnels_tunnel_name_status_trends(serial_number: str, tunnel_name: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/gateways/{serial-number}/tunnels/{tunnel-name}/status-trends
    """
    collection_path = f"/network-monitoring/v1/gateways/{serial_number}/tunnels/{tunnel_name}/status-trends"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_gateways_serial_number_tunnels_tunnel_name_status_trends", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/clusters/{cluster_name}/capacity-trends", methods=["GET"])
def get_network_monitoring_v1_clusters_cluster_name_capacity_trends(cluster_name: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/clusters/{cluster-name}/capacity-trends
    """
    collection_path = f"/network-monitoring/v1/clusters/{cluster_name}/capacity-trends"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_clusters_cluster_name_capacity_trends", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/clusters/{cluster_name}/capacity-trends/{serial_number}", methods=["GET"])
def get_network_monitoring_v1_clusters_cluster_name_capacity_trends_serial_number(cluster_name: str, serial_number: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/clusters/{cluster-name}/capacity-trends/{serial-number}
    """
    collection_path = f"/network-monitoring/v1/clusters/{cluster_name}/capacity-trends"
    item = db.get_item(collection_path, serial_number)
    if item:
        return item
    static_val = db.get_static("get_network_monitoring_v1_clusters_cluster_name_capacity_trends_serial_number")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-monitoring/v1/gateways/{serial_number}/ports/{port_number}/throughput-trends", methods=["GET"])
def get_network_monitoring_v1_gateways_serial_number_ports_port_number_throughput_trends(serial_number: str, port_number: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/gateways/{serial-number}/ports/{port-number}/throughput-trends
    """
    collection_path = f"/network-monitoring/v1/gateways/{serial_number}/ports/{port_number}/throughput-trends"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_gateways_serial_number_ports_port_number_throughput_trends", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/clusters/{cluster_name}/tunnels-health-summary", methods=["GET"])
def get_network_monitoring_v1_clusters_cluster_name_tunnels_health_summary(cluster_name: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/clusters/{cluster-name}/tunnels-health-summary
    """
    collection_path = f"/network-monitoring/v1/clusters/{cluster_name}/tunnels-health-summary"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_clusters_cluster_name_tunnels_health_summary", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/clusters/{cluster_name}/tunnels-status-summary", methods=["GET"])
def get_network_monitoring_v1_clusters_cluster_name_tunnels_status_summary(cluster_name: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/clusters/{cluster-name}/tunnels-status-summary
    """
    collection_path = f"/network-monitoring/v1/clusters/{cluster_name}/tunnels-status-summary"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_clusters_cluster_name_tunnels_status_summary", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/gateways/{serial_number}/lan-tunnels-health-summary", methods=["GET"])
def get_network_monitoring_v1_gateways_serial_number_lan_tunnels_health_summary(serial_number: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/gateways/{serial-number}/lan-tunnels-health-summary
    """
    collection_path = f"/network-monitoring/v1/gateways/{serial_number}/lan-tunnels-health-summary"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_gateways_serial_number_lan_tunnels_health_summary", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/gateways/{serial_number}/wan-availability-trends", methods=["GET"])
def get_network_monitoring_v1_gateways_serial_number_wan_availability_trends(serial_number: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/gateways/{serial-number}/wan-availability-trends
    """
    collection_path = f"/network-monitoring/v1/gateways/{serial_number}/wan-availability-trends"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_gateways_serial_number_wan_availability_trends", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/gateways/{serial_number}/vpn-availability-trends", methods=["GET"])
def get_network_monitoring_v1_gateways_serial_number_vpn_availability_trends(serial_number: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/gateways/{serial-number}/vpn-availability-trends
    """
    collection_path = f"/network-monitoring/v1/gateways/{serial_number}/vpn-availability-trends"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_gateways_serial_number_vpn_availability_trends", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/gateways/{serial_number}/ports/{port_number}/frames-trends", methods=["GET"])
def get_network_monitoring_v1_gateways_serial_number_ports_port_number_frames_trends(serial_number: str, port_number: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/gateways/{serial-number}/ports/{port-number}/frames-trends
    """
    collection_path = f"/network-monitoring/v1/gateways/{serial_number}/ports/{port_number}/frames-trends"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_gateways_serial_number_ports_port_number_frames_trends", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/gateways/{serial_number}/ports/{port_number}/frames-errors-trends", methods=["GET"])
def get_network_monitoring_v1_gateways_serial_number_ports_port_number_frames_errors_trends(serial_number: str, port_number: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/gateways/{serial-number}/ports/{port-number}/frames-errors-trends
    """
    collection_path = f"/network-monitoring/v1/gateways/{serial_number}/ports/{port_number}/frames-errors-trends"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_gateways_serial_number_ports_port_number_frames_errors_trends", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/gateways/{serial_number}/ports/{port_number}/frames-packets-trends", methods=["GET"])
def get_network_monitoring_v1_gateways_serial_number_ports_port_number_frames_packets_trends(serial_number: str, port_number: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/gateways/{serial-number}/ports/{port-number}/frames-packets-trends
    """
    collection_path = f"/network-monitoring/v1/gateways/{serial_number}/ports/{port_number}/frames-packets-trends"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_gateways_serial_number_ports_port_number_frames_packets_trends", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/gateways/{serial_number}/tunnels/{tunnel_name}/dropped-packet-trends", methods=["GET"])
def get_network_monitoring_v1_gateways_serial_number_tunnels_tunnel_name_dropped_packet_trends(serial_number: str, tunnel_name: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/gateways/{serial-number}/tunnels/{tunnel-name}/dropped-packet-trends
    """
    collection_path = f"/network-monitoring/v1/gateways/{serial_number}/tunnels/{tunnel_name}/dropped-packet-trends"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_gateways_serial_number_tunnels_tunnel_name_dropped_packet_trends", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/gateways/{serial_number}/wan-tunnels-health-summary", methods=["GET"])
def get_network_monitoring_v1_gateways_serial_number_wan_tunnels_health_summary(serial_number: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/gateways/{serial-number}/wan-tunnels-health-summary
    """
    collection_path = f"/network-monitoring/v1/gateways/{serial_number}/wan-tunnels-health-summary"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_gateways_serial_number_wan_tunnels_health_summary", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/gateways/{serial_number}/uplinks/{link_tag}", methods=["GET"])
def get_network_monitoring_v1_gateways_serial_number_uplinks_link_tag(serial_number: str, link_tag: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/gateways/{serial-number}/uplinks/{link-tag}
    """
    collection_path = f"/network-monitoring/v1/gateways/{serial_number}/uplinks"
    item = db.get_item(collection_path, link_tag)
    if item:
        return item
    static_val = db.get_static("get_network_monitoring_v1_gateways_serial_number_uplinks_link_tag")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-monitoring/v1/gateways/{serial_number}/uplinks/{link_tag}/throughput-trends", methods=["GET"])
def get_network_monitoring_v1_gateways_serial_number_uplinks_link_tag_throughput_trends(serial_number: str, link_tag: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/gateways/{serial-number}/uplinks/{link-tag}/throughput-trends
    """
    collection_path = f"/network-monitoring/v1/gateways/{serial_number}/uplinks/{link_tag}/throughput-trends"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_gateways_serial_number_uplinks_link_tag_throughput_trends", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/gateways/{serial_number}/uplinks/{link_tag}/wan-compression-trends", methods=["GET"])
def get_network_monitoring_v1_gateways_serial_number_uplinks_link_tag_wan_compression_trends(serial_number: str, link_tag: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/gateways/{serial-number}/uplinks/{link-tag}/wan-compression-trends
    """
    collection_path = f"/network-monitoring/v1/gateways/{serial_number}/uplinks/{link_tag}/wan-compression-trends"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_gateways_serial_number_uplinks_link_tag_wan_compression_trends", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/gateways/{serial_number}/uplinks/{link_tag}/probes", methods=["GET"])
def get_network_monitoring_v1_gateways_serial_number_uplinks_link_tag_probes(serial_number: str, link_tag: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/gateways/{serial-number}/uplinks/{link-tag}/probes
    """
    collection_path = f"/network-monitoring/v1/gateways/{serial_number}/uplinks/{link_tag}/probes"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_gateways_serial_number_uplinks_link_tag_probes", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/gateways/{serial_number}/uplinks/{link_tag}/wan-availability-trends", methods=["GET"])
def get_network_monitoring_v1_gateways_serial_number_uplinks_link_tag_wan_availability_trends(serial_number: str, link_tag: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/gateways/{serial-number}/uplinks/{link-tag}/wan-availability-trends
    """
    collection_path = f"/network-monitoring/v1/gateways/{serial_number}/uplinks/{link_tag}/wan-availability-trends"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_gateways_serial_number_uplinks_link_tag_wan_availability_trends", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/gateways/{serial_number}/uplinks/{vlan_id}/vpn-availability-trends", methods=["GET"])
def get_network_monitoring_v1_gateways_serial_number_uplinks_vlan_id_vpn_availability_trends(serial_number: str, vlan_id: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/gateways/{serial-number}/uplinks/{vlan-id}/vpn-availability-trends
    """
    collection_path = f"/network-monitoring/v1/gateways/{serial_number}/uplinks/{vlan_id}/vpn-availability-trends"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_gateways_serial_number_uplinks_vlan_id_vpn_availability_trends", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/gateways/{serial_number}/hardware-temperature-trends", methods=["GET"])
def get_network_monitoring_v1_gateways_serial_number_hardware_temperature_trends(serial_number: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/gateways/{serial-number}/hardware-temperature-trends
    """
    collection_path = f"/network-monitoring/v1/gateways/{serial_number}/hardware-temperature-trends"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_gateways_serial_number_hardware_temperature_trends", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/gateways/{serial_number}/dhcp-pools", methods=["GET"])
def get_network_monitoring_v1_gateways_serial_number_dhcp_pools(serial_number: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/gateways/{serial-number}/dhcp-pools
    """
    collection_path = f"/network-monitoring/v1/gateways/{serial_number}/dhcp-pools"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_gateways_serial_number_dhcp_pools", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/gateways/{serial_number}/dhcp-clients", methods=["GET"])
def get_network_monitoring_v1_gateways_serial_number_dhcp_clients(serial_number: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/gateways/{serial-number}/dhcp-clients
    """
    collection_path = f"/network-monitoring/v1/gateways/{serial_number}/dhcp-clients"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_gateways_serial_number_dhcp_clients", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/gateways/{serial_number}/uplinks/{link_tag}/probes/{probe}/performance-trends", methods=["GET"])
def get_network_monitoring_v1_gateways_serial_number_uplinks_link_tag_probes_probe_performance_trends(serial_number: str, link_tag: str, probe: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/gateways/{serial-number}/uplinks/{link-tag}/probes/{probe}/performance-trends
    """
    collection_path = f"/network-monitoring/v1/gateways/{serial_number}/uplinks/{link_tag}/probes/{probe}/performance-trends"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_gateways_serial_number_uplinks_link_tag_probes_probe_performance_trends", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/sites-health", methods=["GET"])
def get_network_monitoring_v1_sites_health():
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/sites-health
    """
    collection_path = "/network-monitoring/v1/sites-health"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_sites_health", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/site-health/{site_id}", methods=["GET"])
def get_network_monitoring_v1_site_health_site_id(site_id: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/site-health/{site-id}
    """
    collection_path = f"/network-monitoring/v1/site-health"
    item = db.get_item(collection_path, site_id)
    if item:
        return item
    static_val = db.get_static("get_network_monitoring_v1_site_health_site_id")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-monitoring/v1/sites-device-health", methods=["GET"])
def get_network_monitoring_v1_sites_device_health():
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/sites-device-health
    """
    collection_path = "/network-monitoring/v1/sites-device-health"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_sites_device_health", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/tenant-device-health", methods=["GET"])
def get_network_monitoring_v1_tenant_device_health():
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/tenant-device-health
    """
    collection_path = "/network-monitoring/v1/tenant-device-health"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_tenant_device_health", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/sites-client-health", methods=["GET"])
def get_network_monitoring_v1_sites_client_health():
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/sites-client-health
    """
    collection_path = "/network-monitoring/v1/sites-client-health"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_sites_client_health", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/tenant-client-health", methods=["GET"])
def get_network_monitoring_v1_tenant_client_health():
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/tenant-client-health
    """
    collection_path = "/network-monitoring/v1/tenant-client-health"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_tenant_client_health", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/switches", methods=["GET"])
def get_network_monitoring_v1_switches():
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/switches
    Retrieves a comprehensive list of all switches available in the network. Use this endpoint for broad listing queries.
    """
    collection_path = "/network-monitoring/v1/switches"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_switches", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/switches/{serial_number}", methods=["GET"])
def get_network_monitoring_v1_switches_serial_number(serial_number: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/switches/{serial-number}
    """
    collection_path = f"/network-monitoring/v1/switches"
    item = db.get_item(collection_path, serial_number)
    if item:
        return item
    static_val = db.get_static("get_network_monitoring_v1_switches_serial_number")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-monitoring/v1/stack/{serial_number}/members", methods=["GET"])
def get_network_monitoring_v1_stack_serial_number_members(serial_number: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/stack/{serial-number}/members
    """
    collection_path = f"/network-monitoring/v1/stack/{serial_number}/members"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_stack_serial_number_members", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/switches/{serial_number}/hardware-categories", methods=["GET"])
def get_network_monitoring_v1_switches_serial_number_hardware_categories(serial_number: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/switches/{serial-number}/hardware-categories
    """
    collection_path = f"/network-monitoring/v1/switches/{serial_number}/hardware-categories"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_switches_serial_number_hardware_categories", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/switches/{serial_number}/lag", methods=["GET"])
def get_network_monitoring_v1_switches_serial_number_lag(serial_number: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/switches/{serial-number}/lag
    """
    collection_path = f"/network-monitoring/v1/switches/{serial_number}/lag"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_switches_serial_number_lag", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/switches/{serial_number}/interfaces", methods=["GET"])
def get_network_monitoring_v1_switches_serial_number_interfaces(serial_number: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/switches/{serial-number}/interfaces
    """
    collection_path = f"/network-monitoring/v1/switches/{serial_number}/interfaces"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_switches_serial_number_interfaces", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/switches/{serial_number}/vlans", methods=["GET"])
def get_network_monitoring_v1_switches_serial_number_vlans(serial_number: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/switches/{serial-number}/vlans
    """
    collection_path = f"/network-monitoring/v1/switches/{serial_number}/vlans"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_switches_serial_number_vlans", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/switches/topn-interface-trends", methods=["GET"])
def get_network_monitoring_v1_switches_topn_interface_trends():
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/switches/topn-interface-trends
    """
    collection_path = "/network-monitoring/v1/switches/topn-interface-trends"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_switches_topn_interface_trends", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/switches/{serial_number}/interface-trends", methods=["GET"])
def get_network_monitoring_v1_switches_serial_number_interface_trends(serial_number: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/switches/{serial-number}/interface-trends
    """
    collection_path = f"/network-monitoring/v1/switches/{serial_number}/interface-trends"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_switches_serial_number_interface_trends", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/switches/{serial_number}/hardware-trends", methods=["GET"])
def get_network_monitoring_v1_switches_serial_number_hardware_trends(serial_number: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/switches/{serial-number}/hardware-trends
    """
    collection_path = f"/network-monitoring/v1/switches/{serial_number}/hardware-trends"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_switches_serial_number_hardware_trends", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/switches/{serial_number}/interface-poe", methods=["GET"])
def get_network_monitoring_v1_switches_serial_number_interface_poe(serial_number: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/switches/{serial-number}/interface-poe
    """
    collection_path = f"/network-monitoring/v1/switches/{serial_number}/interface-poe"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_switches_serial_number_interface_poe", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/switches/{serial_number}/vsx", methods=["GET"])
def get_network_monitoring_v1_switches_serial_number_vsx(serial_number: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/switches/{serial-number}/vsx
    """
    collection_path = f"/network-monitoring/v1/switches/{serial_number}/vsx"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_monitoring_v1_switches_serial_number_vsx", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-monitoring/v1/topology/{site_id}", methods=["GET"])
def get_network_monitoring_v1_topology_site_id(site_id: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/topology/{site-id}
    """
    collection_path = f"/network-monitoring/v1/topology"
    item = db.get_item(collection_path, site_id)
    if item:
        return item
    static_val = db.get_static("get_network_monitoring_v1_topology_site_id")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-monitoring/v1/unmanaged-device/{mac_address}", methods=["GET"])
def get_network_monitoring_v1_unmanaged_device_mac_address(mac_address: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/unmanaged-device/{mac-address}
    """
    collection_path = f"/network-monitoring/v1/unmanaged-device"
    item = db.get_item(collection_path, mac_address)
    if item:
        return item
    static_val = db.get_static("get_network_monitoring_v1_unmanaged_device_mac_address")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-monitoring/v1/isolated-devices/{site_id}", methods=["GET"])
def get_network_monitoring_v1_isolated_devices_site_id(site_id: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/isolated-devices/{site-id}
    """
    collection_path = f"/network-monitoring/v1/isolated-devices"
    item = db.get_item(collection_path, site_id)
    if item:
        return item
    static_val = db.get_static("get_network_monitoring_v1_isolated_devices_site_id")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-monitoring/v1/neighbours/{serial_number}", methods=["GET"])
def get_network_monitoring_v1_neighbours_serial_number(serial_number: str):
    """
    Aruba Central Endpoint: GET /network-monitoring/v1/neighbours/{serial-number}
    """
    if serial_number == "aruba-cx-017":
        return {
            "neighbors": [
                {
                    "local_port": "GigabitEthernet1/0/1",
                    "remote_chassis_id": "core-sw-018",
                    "remote_port": "GigabitEthernet1/0/24",
                    "remote_system_name": "core-sw-018"
                },
                {
                    "local_port": "GigabitEthernet1/0/12",
                    "remote_chassis_id": "edge-router-019",
                    "remote_port": "GigabitEthernet1/0/1",
                    "remote_system_name": "edge-router-019"
                }
            ]
        }
        
    collection_path = f"/network-monitoring/v1/neighbours"
    item = db.get_item(collection_path, serial_number)
    if item:
        return item
    static_val = db.get_static("get_network_monitoring_v1_neighbours_serial_number")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-msp/v1/list-tenants", methods=["GET"])
def get_network_msp_v1_list_tenants():
    """
    Aruba Central Endpoint: GET /network-msp/v1/list-tenants
    """
    collection_path = "/network-msp/v1/list-tenants"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_msp_v1_list_tenants", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-notifications/v1/alert-config", methods=["GET"])
def get_network_notifications_v1_alert_config():
    """
    Aruba Central Endpoint: GET /network-notifications/v1/alert-config
    """
    collection_path = "/network-notifications/v1/alert-config"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_notifications_v1_alert_config", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-notifications/v1/alerts", methods=["GET"])
def get_network_notifications_v1_alerts():
    """
    Aruba Central Endpoint: GET /network-notifications/v1/alerts
    """
    collection_path = "/network-notifications/v1/alerts"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_notifications_v1_alerts", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-notifications/v1/alerts/clear", methods=["POST"])
def post_network_notifications_v1_alerts_clear(payload: Aruba_clearalerts_Request):
    """
    Aruba Central Endpoint: POST /network-notifications/v1/alerts/clear
    """
    collection_path = "/network-notifications/v1/alerts/clear"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("serial") or payload_dict.get("name") or str(uuid.uuid4())
    payload_dict["id"] = item_id
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/network-notifications/v1/alerts/defer", methods=["POST"])
def post_network_notifications_v1_alerts_defer(payload: Aruba_deferalerts_Request):
    """
    Aruba Central Endpoint: POST /network-notifications/v1/alerts/defer
    """
    collection_path = "/network-notifications/v1/alerts/defer"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("serial") or payload_dict.get("name") or str(uuid.uuid4())
    payload_dict["id"] = item_id
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/network-notifications/v1/alerts/active", methods=["POST"])
def post_network_notifications_v1_alerts_active(payload: Aruba_setactivealerts_Request):
    """
    Aruba Central Endpoint: POST /network-notifications/v1/alerts/active
    """
    collection_path = "/network-notifications/v1/alerts/active"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("serial") or payload_dict.get("name") or str(uuid.uuid4())
    payload_dict["id"] = item_id
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/network-notifications/v1/alerts/priority", methods=["POST"])
def post_network_notifications_v1_alerts_priority(payload: Aruba_setpriorityalerts_Request):
    """
    Aruba Central Endpoint: POST /network-notifications/v1/alerts/priority
    """
    collection_path = "/network-notifications/v1/alerts/priority"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("serial") or payload_dict.get("name") or str(uuid.uuid4())
    payload_dict["id"] = item_id
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/network-notifications/v1/alerts/classification", methods=["GET"])
def get_network_notifications_v1_alerts_classification():
    """
    Aruba Central Endpoint: GET /network-notifications/v1/alerts/classification
    """
    collection_path = "/network-notifications/v1/alerts/classification"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_notifications_v1_alerts_classification", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-notifications/v1/alerts/async-operations/{task_id}", methods=["GET"])
def get_network_notifications_v1_alerts_async_operations_task_id(task_id: str):
    """
    Aruba Central Endpoint: GET /network-notifications/v1/alerts/async-operations/{task-id}
    """
    collection_path = f"/network-notifications/v1/alerts/async-operations"
    item = db.get_item(collection_path, task_id)
    if item:
        return item
    static_val = db.get_static("get_network_notifications_v1_alerts_async_operations_task_id")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-notifications/v1/insights", methods=["GET"])
def get_network_notifications_v1_insights():
    """
    Aruba Central Endpoint: GET /network-notifications/v1/insights
    """
    collection_path = "/network-notifications/v1/insights"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_notifications_v1_insights", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-notifications/v1/insights-schema", methods=["GET"])
def get_network_notifications_v1_insights_schema():
    """
    Aruba Central Endpoint: GET /network-notifications/v1/insights-schema
    """
    collection_path = "/network-notifications/v1/insights-schema"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_notifications_v1_insights_schema", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-reporting/v1/reports", methods=["GET"])
def get_network_reporting_v1_reports():
    """
    Aruba Central Endpoint: GET /network-reporting/v1/reports
    """
    collection_path = "/network-reporting/v1/reports"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_reporting_v1_reports", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-reporting/v1/reports/{report_id}", methods=["PUT"])
def put_network_reporting_v1_reports_report_id(report_id: str, payload: Aruba_updateuserreport_Request):
    """
    Aruba Central Endpoint: PUT /network-reporting/v1/reports/{report-id}
    """
    collection_path = f"/network-reporting/v1/reports"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = db.get_item(collection_path, report_id) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, report_id, existing)
    return existing

@app.api_route("/network-reporting/v1/reports/{report_id}", methods=["DELETE"])
def delete_network_reporting_v1_reports_report_id(report_id: str):
    """
    Aruba Central Endpoint: DELETE /network-reporting/v1/reports/{report-id}
    """
    collection_path = f"/network-reporting/v1/reports"
    deleted = db.delete_item(collection_path, report_id)
    if deleted:
        return {"message": "Deleted successfully", "id": report_id, "item": deleted}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-reporting/v1/reports/{report_id}/report-runs", methods=["GET"])
def get_network_reporting_v1_reports_report_id_report_runs(report_id: str):
    """
    Aruba Central Endpoint: GET /network-reporting/v1/reports/{report-id}/report-runs
    """
    collection_path = f"/network-reporting/v1/reports/{report_id}/report-runs"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_reporting_v1_reports_report_id_report_runs", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-reporting/v1/reports/{report_id}/report-runs/{report_run_id}", methods=["DELETE"])
def delete_network_reporting_v1_reports_report_id_report_runs_report_run_id(report_id: str, report_run_id: str):
    """
    Aruba Central Endpoint: DELETE /network-reporting/v1/reports/{report-id}/report-runs/{report-run-id}
    """
    collection_path = f"/network-reporting/v1/reports/{report_id}/report-runs"
    deleted = db.delete_item(collection_path, report_run_id)
    if deleted:
        return {"message": "Deleted successfully", "id": report_run_id, "item": deleted}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-reporting/v1/reports/{report_id}/report-runs/{report_run_id}/download-link", methods=["POST"])
def post_network_reporting_v1_reports_report_id_report_runs_report_run_id_download_link(report_id: str, report_run_id: str, payload: Aruba_downloadreportlink_Request):
    """
    Aruba Central Endpoint: POST /network-reporting/v1/reports/{report-id}/report-runs/{report-run-id}/download-link
    """
    collection_path = f"/network-reporting/v1/reports/{report_id}/report-runs/{report_run_id}/download-link"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = db.get_item(collection_path, report_run_id) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, report_run_id, existing)
    return existing

@app.api_route("/network-services/v1/airmatch-radio/{radio_mac}", methods=["GET"])
def get_network_services_v1_airmatch_radio_radio_mac(radio_mac: str):
    """
    Aruba Central Endpoint: GET /network-services/v1/airmatch-radio/{radio-mac}
    """
    collection_path = f"/network-services/v1/airmatch-radio"
    item = db.get_item(collection_path, radio_mac)
    if item:
        return item
    static_val = db.get_static("get_network_services_v1_airmatch_radio_radio_mac")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-services/v1/airmatch-radio", methods=["GET"])
def get_network_services_v1_airmatch_radio():
    """
    Aruba Central Endpoint: GET /network-services/v1/airmatch-radio
    """
    collection_path = "/network-services/v1/airmatch-radio"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_services_v1_airmatch_radio", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-services/v1/airmatch-ap/{serial_number}", methods=["GET"])
def get_network_services_v1_airmatch_ap_serial_number(serial_number: str):
    """
    Aruba Central Endpoint: GET /network-services/v1/airmatch-ap/{serial-number}
    """
    collection_path = f"/network-services/v1/airmatch-ap"
    item = db.get_item(collection_path, serial_number)
    if item:
        return item
    static_val = db.get_static("get_network_services_v1_airmatch_ap_serial_number")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-services/v1/airmatch-ap", methods=["GET"])
def get_network_services_v1_airmatch_ap():
    """
    Aruba Central Endpoint: GET /network-services/v1/airmatch-ap
    """
    collection_path = "/network-services/v1/airmatch-ap"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_services_v1_airmatch_ap", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-services/v1/airmatch-ap-radio-relations/{serial_number}", methods=["GET"])
def get_network_services_v1_airmatch_ap_radio_relations_serial_number(serial_number: str):
    """
    Aruba Central Endpoint: GET /network-services/v1/airmatch-ap-radio-relations/{serial-number}
    """
    collection_path = f"/network-services/v1/airmatch-ap-radio-relations"
    item = db.get_item(collection_path, serial_number)
    if item:
        return item
    static_val = db.get_static("get_network_services_v1_airmatch_ap_radio_relations_serial_number")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-services/v1/airmatch-priority-rf-events/{radio_mac}", methods=["GET"])
def get_network_services_v1_airmatch_priority_rf_events_radio_mac(radio_mac: str):
    """
    Aruba Central Endpoint: GET /network-services/v1/airmatch-priority-rf-events/{radio-mac}
    """
    collection_path = f"/network-services/v1/airmatch-priority-rf-events"
    item = db.get_item(collection_path, radio_mac)
    if item:
        return item
    static_val = db.get_static("get_network_services_v1_airmatch_priority_rf_events_radio_mac")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-services/v1/airmatch-priority-rf-events", methods=["GET"])
def get_network_services_v1_airmatch_priority_rf_events():
    """
    Aruba Central Endpoint: GET /network-services/v1/airmatch-priority-rf-events
    """
    collection_path = "/network-services/v1/airmatch-priority-rf-events"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_services_v1_airmatch_priority_rf_events", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-services/v1/airmatch-rf-events/{radio_mac}", methods=["GET"])
def get_network_services_v1_airmatch_rf_events_radio_mac(radio_mac: str):
    """
    Aruba Central Endpoint: GET /network-services/v1/airmatch-rf-events/{radio-mac}
    """
    collection_path = f"/network-services/v1/airmatch-rf-events"
    item = db.get_item(collection_path, radio_mac)
    if item:
        return item
    static_val = db.get_static("get_network_services_v1_airmatch_rf_events_radio_mac")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-services/v1/airmatch-rf-events", methods=["GET"])
def get_network_services_v1_airmatch_rf_events():
    """
    Aruba Central Endpoint: GET /network-services/v1/airmatch-rf-events
    """
    collection_path = "/network-services/v1/airmatch-rf-events"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_services_v1_airmatch_rf_events", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-services/v1/airmatch-history/{radio_mac}", methods=["GET"])
def get_network_services_v1_airmatch_history_radio_mac(radio_mac: str):
    """
    Aruba Central Endpoint: GET /network-services/v1/airmatch-history/{radio-mac}
    """
    collection_path = f"/network-services/v1/airmatch-history"
    item = db.get_item(collection_path, radio_mac)
    if item:
        return item
    static_val = db.get_static("get_network_services_v1_airmatch_history_radio_mac")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-services/v1/airmatch-service-config", methods=["GET"])
def get_network_services_v1_airmatch_service_config():
    """
    Aruba Central Endpoint: GET /network-services/v1/airmatch-service-config
    """
    collection_path = "/network-services/v1/airmatch-service-config"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_services_v1_airmatch_service_config", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-services/v1/airmatch-global-config-id", methods=["GET"])
def get_network_services_v1_airmatch_global_config_id():
    """
    Aruba Central Endpoint: GET /network-services/v1/airmatch-global-config-id
    """
    collection_path = "/network-services/v1/airmatch-global-config-id"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_services_v1_airmatch_global_config_id", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-services/v1/airmatch-radio-feasibility/{radio_mac}", methods=["GET"])
def get_network_services_v1_airmatch_radio_feasibility_radio_mac(radio_mac: str):
    """
    Aruba Central Endpoint: GET /network-services/v1/airmatch-radio-feasibility/{radio-mac}
    """
    collection_path = f"/network-services/v1/airmatch-radio-feasibility"
    item = db.get_item(collection_path, radio_mac)
    if item:
        return item
    static_val = db.get_static("get_network_services_v1_airmatch_radio_feasibility_radio_mac")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-services/v1/airmatch-radio-feasibility", methods=["GET"])
def get_network_services_v1_airmatch_radio_feasibility():
    """
    Aruba Central Endpoint: GET /network-services/v1/airmatch-radio-feasibility
    """
    collection_path = "/network-services/v1/airmatch-radio-feasibility"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_services_v1_airmatch_radio_feasibility", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-services/v1/airmatch-board-limit/{serial_number}/{radio_mac}", methods=["GET"])
def get_network_services_v1_airmatch_board_limit_serial_number_radio_mac(serial_number: str, radio_mac: str):
    """
    Aruba Central Endpoint: GET /network-services/v1/airmatch-board-limit/{serial-number}/{radio-mac}
    """
    collection_path = f"/network-services/v1/airmatch-board-limit/{serial_number}"
    item = db.get_item(collection_path, radio_mac)
    if item:
        return item
    static_val = db.get_static("get_network_services_v1_airmatch_board_limit_serial_number_radio_mac")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-services/v1/airmatch-device-config/{serial_number}", methods=["GET"])
def get_network_services_v1_airmatch_device_config_serial_number(serial_number: str):
    """
    Aruba Central Endpoint: GET /network-services/v1/airmatch-device-config/{serial-number}
    """
    collection_path = f"/network-services/v1/airmatch-device-config"
    item = db.get_item(collection_path, serial_number)
    if item:
        return item
    static_val = db.get_static("get_network_services_v1_airmatch_device_config_serial_number")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-services/v1/airmatch-non-friend/{radio_mac}", methods=["GET"])
def get_network_services_v1_airmatch_non_friend_radio_mac(radio_mac: str):
    """
    Aruba Central Endpoint: GET /network-services/v1/airmatch-non-friend/{radio-mac}
    """
    collection_path = f"/network-services/v1/airmatch-non-friend"
    item = db.get_item(collection_path, radio_mac)
    if item:
        return item
    static_val = db.get_static("get_network_services_v1_airmatch_non_friend_radio_mac")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-services/v1/airmatch-pathloss/{radio_mac}", methods=["GET"])
def get_network_services_v1_airmatch_pathloss_radio_mac(radio_mac: str):
    """
    Aruba Central Endpoint: GET /network-services/v1/airmatch-pathloss/{radio-mac}
    """
    collection_path = f"/network-services/v1/airmatch-pathloss"
    item = db.get_item(collection_path, radio_mac)
    if item:
        return item
    static_val = db.get_static("get_network_services_v1_airmatch_pathloss_radio_mac")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-services/v1/airmatch-ap-neighbor-list/{serial_number}", methods=["GET"])
def get_network_services_v1_airmatch_ap_neighbor_list_serial_number(serial_number: str):
    """
    Aruba Central Endpoint: GET /network-services/v1/airmatch-ap-neighbor-list/{serial-number}
    """
    collection_path = f"/network-services/v1/airmatch-ap-neighbor-list"
    item = db.get_item(collection_path, serial_number)
    if item:
        return item
    static_val = db.get_static("get_network_services_v1_airmatch_ap_neighbor_list_serial_number")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-services/v1/airmatch-partition", methods=["GET"])
def get_network_services_v1_airmatch_partition():
    """
    Aruba Central Endpoint: GET /network-services/v1/airmatch-partition
    """
    collection_path = "/network-services/v1/airmatch-partition"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_services_v1_airmatch_partition", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-services/v1/airmatch-partition", methods=["POST"])
def post_network_services_v1_airmatch_partition():
    """
    Aruba Central Endpoint: POST /network-services/v1/airmatch-partition
    """
    collection_path = "/network-services/v1/airmatch-partition"
    payload_dict = {}
    item_id = payload_dict.get("id") or payload_dict.get("serial") or payload_dict.get("name") or str(uuid.uuid4())
    payload_dict["id"] = item_id
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/network-services/v1/airmatch-radio-partition/{radio_mac}", methods=["GET"])
def get_network_services_v1_airmatch_radio_partition_radio_mac(radio_mac: str):
    """
    Aruba Central Endpoint: GET /network-services/v1/airmatch-radio-partition/{radio-mac}
    """
    collection_path = f"/network-services/v1/airmatch-radio-partition"
    item = db.get_item(collection_path, radio_mac)
    if item:
        return item
    static_val = db.get_static("get_network_services_v1_airmatch_radio_partition_radio_mac")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-services/v1/airmatch-runnow", methods=["POST"])
def post_network_services_v1_airmatch_runnow():
    """
    Aruba Central Endpoint: POST /network-services/v1/airmatch-runnow
    """
    collection_path = "/network-services/v1/airmatch-runnow"
    payload_dict = {}
    item_id = payload_dict.get("id") or payload_dict.get("serial") or payload_dict.get("name") or str(uuid.uuid4())
    payload_dict["id"] = item_id
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/network-services/v1/airmatch-solution", methods=["GET"])
def get_network_services_v1_airmatch_solution():
    """
    Aruba Central Endpoint: GET /network-services/v1/airmatch-solution
    """
    collection_path = "/network-services/v1/airmatch-solution"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_services_v1_airmatch_solution", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-services/v1/airmatch-solution/{radio_mac}", methods=["GET"])
def get_network_services_v1_airmatch_solution_radio_mac(radio_mac: str):
    """
    Aruba Central Endpoint: GET /network-services/v1/airmatch-solution/{radio-mac}
    """
    collection_path = f"/network-services/v1/airmatch-solution"
    item = db.get_item(collection_path, radio_mac)
    if item:
        return item
    static_val = db.get_static("get_network_services_v1_airmatch_solution_radio_mac")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-services/v1/airmatch-ap-coverage-plan/{serial_number}", methods=["GET"])
def get_network_services_v1_airmatch_ap_coverage_plan_serial_number(serial_number: str):
    """
    Aruba Central Endpoint: GET /network-services/v1/airmatch-ap-coverage-plan/{serial-number}
    """
    collection_path = f"/network-services/v1/airmatch-ap-coverage-plan"
    item = db.get_item(collection_path, serial_number)
    if item:
        return item
    static_val = db.get_static("get_network_services_v1_airmatch_ap_coverage_plan_serial_number")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-services/v1/airmatch-ap-coverage-plan", methods=["GET"])
def get_network_services_v1_airmatch_ap_coverage_plan():
    """
    Aruba Central Endpoint: GET /network-services/v1/airmatch-ap-coverage-plan
    """
    collection_path = "/network-services/v1/airmatch-ap-coverage-plan"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_services_v1_airmatch_ap_coverage_plan", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-services/v1/airmatch-state", methods=["GET"])
def get_network_services_v1_airmatch_state():
    """
    Aruba Central Endpoint: GET /network-services/v1/airmatch-state
    """
    collection_path = "/network-services/v1/airmatch-state"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_services_v1_airmatch_state", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/audit/v1/logs/{id}", methods=["GET"])
def get_audit_v1_logs_id(id: str):
    """
    Aruba Central Endpoint: GET /audit/v1/logs/{id}
    """
    collection_path = f"/audit/v1/logs"
    item = db.get_item(collection_path, id)
    if item:
        return item
    static_val = db.get_static("get_audit_v1_logs_id")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/audit/v1/logs", methods=["GET"])
def get_audit_v1_logs():
    """
    Aruba Central Endpoint: GET /audit/v1/logs
    """
    collection_path = "/audit/v1/logs"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_audit_v1_logs", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-services/v1/fco-resp-info/{serial_number}", methods=["GET"])
def get_network_services_v1_fco_resp_info_serial_number(serial_number: str):
    """
    Aruba Central Endpoint: GET /network-services/v1/fco-resp-info/{serial-number}
    """
    collection_path = f"/network-services/v1/fco-resp-info"
    item = db.get_item(collection_path, serial_number)
    if item:
        return item
    static_val = db.get_static("get_network_services_v1_fco_resp_info_serial_number")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-services/v1/fco-resp-info-all", methods=["GET"])
def get_network_services_v1_fco_resp_info_all():
    """
    Aruba Central Endpoint: GET /network-services/v1/fco-resp-info-all
    """
    collection_path = "/network-services/v1/fco-resp-info-all"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_services_v1_fco_resp_info_all", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-services/v1/firmware-details", methods=["GET"])
def get_network_services_v1_firmware_details():
    """
    Aruba Central Endpoint: GET /network-services/v1/firmware-details
    """
    collection_path = "/network-services/v1/firmware-details"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_services_v1_firmware_details", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-services/v1/sites/{site_id}/device-locations", methods=["GET"])
def get_network_services_v1_sites_site_id_device_locations(site_id: str):
    """
    Aruba Central Endpoint: GET /network-services/v1/sites/{site-id}/device-locations
    """
    collection_path = f"/network-services/v1/sites/{site_id}/device-locations"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_services_v1_sites_site_id_device_locations", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-services/v1/sites/{site_id}/device-locations/{location_id}", methods=["GET"])
def get_network_services_v1_sites_site_id_device_locations_location_id(site_id: str, location_id: str):
    """
    Aruba Central Endpoint: GET /network-services/v1/sites/{site-id}/device-locations/{location-id}
    """
    collection_path = f"/network-services/v1/sites/{site_id}/device-locations"
    item = db.get_item(collection_path, location_id)
    if item:
        return item
    static_val = db.get_static("get_network_services_v1_sites_site_id_device_locations_location_id")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-services/v1/sites/{site_id}/devices/{serial_number}/location", methods=["GET"])
def get_network_services_v1_sites_site_id_devices_serial_number_location(site_id: str, serial_number: str):
    """
    Aruba Central Endpoint: GET /network-services/v1/sites/{site-id}/devices/{serial-number}/location
    """
    collection_path = f"/network-services/v1/sites/{site_id}/devices/{serial_number}/location"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_services_v1_sites_site_id_devices_serial_number_location", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-services/v1/sites/{site_id}/devices/{serial_number}/location", methods=["POST"])
def post_network_services_v1_sites_site_id_devices_serial_number_location(site_id: str, serial_number: str, payload: Aruba_putdeviceadminlocationv1_Request):
    """
    Aruba Central Endpoint: POST /network-services/v1/sites/{site-id}/devices/{serial-number}/location
    """
    collection_path = f"/network-services/v1/sites/{site_id}/devices/{serial_number}/location"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = db.get_item(collection_path, serial_number) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, serial_number, existing)
    return existing

@app.api_route("/network-services/v1/sites/{site_id}/devices/{serial_number}/location", methods=["DELETE"])
def delete_network_services_v1_sites_site_id_devices_serial_number_location(site_id: str, serial_number: str):
    """
    Aruba Central Endpoint: DELETE /network-services/v1/sites/{site-id}/devices/{serial-number}/location
    """
    collection_path = f"/network-services/v1/sites/{site_id}/devices/{serial_number}/location"
    deleted = db.delete_item(collection_path, serial_number)
    if deleted:
        return {"message": "Deleted successfully", "id": serial_number, "item": deleted}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-services/v1/ap-ranging-scans", methods=["POST"])
def post_network_services_v1_ap_ranging_scans(payload: Aruba_startaprangingscanv1_Request):
    """
    Aruba Central Endpoint: POST /network-services/v1/ap-ranging-scans
    """
    collection_path = "/network-services/v1/ap-ranging-scans"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("serial") or payload_dict.get("name") or str(uuid.uuid4())
    payload_dict["id"] = item_id
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/network-services/v1/sitemaps/{site_id}/floors/{floor_id}/ap-ranging-scans", methods=["GET"])
def get_network_services_v1_sitemaps_site_id_floors_floor_id_ap_ranging_scans(site_id: str, floor_id: str):
    """
    Aruba Central Endpoint: GET /network-services/v1/sitemaps/{site-id}/floors/{floor-id}/ap-ranging-scans
    """
    collection_path = f"/network-services/v1/sitemaps/{site_id}/floors/{floor_id}/ap-ranging-scans"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_services_v1_sitemaps_site_id_floors_floor_id_ap_ranging_scans", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-services/v1/sitemaps/{site_id}/floors/{floor_id}/ap-ranging-scans/{scan_id}", methods=["GET"])
def get_network_services_v1_sitemaps_site_id_floors_floor_id_ap_ranging_scans_scan_id(site_id: str, floor_id: str, scan_id: str):
    """
    Aruba Central Endpoint: GET /network-services/v1/sitemaps/{site-id}/floors/{floor-id}/ap-ranging-scans/{scan-id}
    """
    collection_path = f"/network-services/v1/sitemaps/{site_id}/floors/{floor_id}/ap-ranging-scans"
    item = db.get_item(collection_path, scan_id)
    if item:
        return item
    static_val = db.get_static("get_network_services_v1_sitemaps_site_id_floors_floor_id_ap_ranging_scans_scan_id")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-services/v1/sitemaps/{site_id}/floors/{floor_id}/ap-ranging-scans/{scan_id}", methods=["DELETE"])
def delete_network_services_v1_sitemaps_site_id_floors_floor_id_ap_ranging_scans_scan_id(site_id: str, floor_id: str, scan_id: str):
    """
    Aruba Central Endpoint: DELETE /network-services/v1/sitemaps/{site-id}/floors/{floor-id}/ap-ranging-scans/{scan-id}
    """
    collection_path = f"/network-services/v1/sitemaps/{site_id}/floors/{floor_id}/ap-ranging-scans"
    deleted = db.delete_item(collection_path, scan_id)
    if deleted:
        return {"message": "Deleted successfully", "id": scan_id, "item": deleted}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-services/v1/wifi-clients-locations", methods=["GET"])
def get_network_services_v1_wifi_clients_locations():
    """
    Aruba Central Endpoint: GET /network-services/v1/wifi-clients-locations
    """
    collection_path = "/network-services/v1/wifi-clients-locations"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_services_v1_wifi_clients_locations", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-services/v1/asset-tags", methods=["GET"])
def get_network_services_v1_asset_tags():
    """
    Aruba Central Endpoint: GET /network-services/v1/asset-tags
    """
    collection_path = "/network-services/v1/asset-tags"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_services_v1_asset_tags", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-services/v1/asset-tags/{asset_tag_id}", methods=["GET"])
def get_network_services_v1_asset_tags_asset_tag_id(asset_tag_id: str):
    """
    Aruba Central Endpoint: GET /network-services/v1/asset-tags/{asset-tag-id}
    """
    collection_path = f"/network-services/v1/asset-tags"
    item = db.get_item(collection_path, asset_tag_id)
    if item:
        return item
    static_val = db.get_static("get_network_services_v1_asset_tags_asset_tag_id")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-services/v1/asset-tags/{asset_tag_id}/metadata", methods=["PUT"])
def put_network_services_v1_asset_tags_asset_tag_id_metadata(asset_tag_id: str, payload: Aruba_updateassettagdatabyassettagidv1_Request):
    """
    Aruba Central Endpoint: PUT /network-services/v1/asset-tags/{asset-tag-id}/metadata
    """
    collection_path = f"/network-services/v1/asset-tags/{asset_tag_id}/metadata"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = db.get_item(collection_path, asset_tag_id) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, asset_tag_id, existing)
    return existing

@app.api_route("/network-services/v1/asset-tags/{asset_tag_id}/metadata", methods=["POST"])
def post_network_services_v1_asset_tags_asset_tag_id_metadata(asset_tag_id: str, payload: Aruba_createassettagdatabyassettagidv1_Request):
    """
    Aruba Central Endpoint: POST /network-services/v1/asset-tags/{asset-tag-id}/metadata
    """
    collection_path = f"/network-services/v1/asset-tags/{asset_tag_id}/metadata"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = db.get_item(collection_path, asset_tag_id) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, asset_tag_id, existing)
    return existing

@app.api_route("/network-services/v1/asset-tags/{asset_tag_id}/metadata", methods=["DELETE"])
def delete_network_services_v1_asset_tags_asset_tag_id_metadata(asset_tag_id: str):
    """
    Aruba Central Endpoint: DELETE /network-services/v1/asset-tags/{asset-tag-id}/metadata
    """
    collection_path = f"/network-services/v1/asset-tags/{asset_tag_id}/metadata"
    deleted = db.delete_item(collection_path, asset_tag_id)
    if deleted:
        return {"message": "Deleted successfully", "id": asset_tag_id, "item": deleted}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-services/v1/location-analytics/trends", methods=["GET"])
def get_network_services_v1_location_analytics_trends():
    """
    Aruba Central Endpoint: GET /network-services/v1/location-analytics/trends
    """
    collection_path = "/network-services/v1/location-analytics/trends"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_services_v1_location_analytics_trends", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-services/v1/location-analytics/sites/insights", methods=["GET"])
def get_network_services_v1_location_analytics_sites_insights():
    """
    Aruba Central Endpoint: GET /network-services/v1/location-analytics/sites/insights
    """
    collection_path = "/network-services/v1/location-analytics/sites/insights"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_services_v1_location_analytics_sites_insights", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-services/v1/webhooks", methods=["GET"])
def get_network_services_v1_webhooks():
    """
    Aruba Central Endpoint: GET /network-services/v1/webhooks
    """
    collection_path = "/network-services/v1/webhooks"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_services_v1_webhooks", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-services/v1/webhooks", methods=["POST"])
def post_network_services_v1_webhooks(payload: Aruba_createwebhookv1_Request):
    """
    Aruba Central Endpoint: POST /network-services/v1/webhooks
    """
    collection_path = "/network-services/v1/webhooks"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("serial") or payload_dict.get("name") or str(uuid.uuid4())
    payload_dict["id"] = item_id
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.api_route("/network-services/v1/webhooks/{id}", methods=["GET"])
def get_network_services_v1_webhooks_id(id: str):
    """
    Aruba Central Endpoint: GET /network-services/v1/webhooks/{id}
    """
    collection_path = f"/network-services/v1/webhooks"
    item = db.get_item(collection_path, id)
    if item:
        return item
    static_val = db.get_static("get_network_services_v1_webhooks_id")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-services/v1/webhooks/{id}", methods=["PUT"])
def put_network_services_v1_webhooks_id(id: str, payload: Aruba_updatewebhookv1_Request):
    """
    Aruba Central Endpoint: PUT /network-services/v1/webhooks/{id}
    """
    collection_path = f"/network-services/v1/webhooks"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = db.get_item(collection_path, id) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, id, existing)
    return existing

@app.api_route("/network-services/v1/webhooks/{id}", methods=["PATCH"])
def patch_network_services_v1_webhooks_id(id: str, payload: Aruba_patchwebhookv1_Request):
    """
    Aruba Central Endpoint: PATCH /network-services/v1/webhooks/{id}
    """
    collection_path = f"/network-services/v1/webhooks"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = db.get_item(collection_path, id) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, id, existing)
    return existing

@app.api_route("/network-services/v1/webhooks/{id}", methods=["DELETE"])
def delete_network_services_v1_webhooks_id(id: str):
    """
    Aruba Central Endpoint: DELETE /network-services/v1/webhooks/{id}
    """
    collection_path = f"/network-services/v1/webhooks"
    deleted = db.delete_item(collection_path, id)
    if deleted:
        return {"message": "Deleted successfully", "id": id, "item": deleted}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-services/v1/webhooks/{id}/rotate-hmac-key", methods=["POST"])
def post_network_services_v1_webhooks_id_rotate_hmac_key(id: str):
    """
    Aruba Central Endpoint: POST /network-services/v1/webhooks/{id}/rotate-hmac-key
    """
    collection_path = f"/network-services/v1/webhooks/{id}/rotate-hmac-key"
    payload_dict = {}
    existing = db.get_item(collection_path, id) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, id, existing)
    return existing

@app.api_route("/network-troubleshooting/v1/aos-s/{serial_number}/ping", methods=["POST"])
def post_network_troubleshooting_v1_aos_s_serial_number_ping(serial_number: str, payload: Aruba_initiatepvospingv1_Request):
    """
    Aruba Central Endpoint: POST /network-troubleshooting/v1/aos-s/{serial-number}/ping
    """
    collection_path = f"/network-troubleshooting/v1/aos-s/{serial_number}/ping"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = db.get_item(collection_path, serial_number) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, serial_number, existing)
    return existing

@app.api_route("/network-troubleshooting/v1/aos-s/{serial_number}/ping/async-operations/{task_id}", methods=["GET"])
def get_network_troubleshooting_v1_aos_s_serial_number_ping_async_operations_task_id(serial_number: str, task_id: str):
    """
    Aruba Central Endpoint: GET /network-troubleshooting/v1/aos-s/{serial-number}/ping/async-operations/{task-id}
    """
    collection_path = f"/network-troubleshooting/v1/aos-s/{serial_number}/ping/async-operations"
    item = db.get_item(collection_path, task_id)
    if item:
        return item
    static_val = db.get_static("get_network_troubleshooting_v1_aos_s_serial_number_ping_async_operations_task_id")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-troubleshooting/v1/aos-s/{serial_number}/traceroute", methods=["POST"])
def post_network_troubleshooting_v1_aos_s_serial_number_traceroute(serial_number: str, payload: Aruba_initiatepvostraceroutev1_Request):
    """
    Aruba Central Endpoint: POST /network-troubleshooting/v1/aos-s/{serial-number}/traceroute
    """
    collection_path = f"/network-troubleshooting/v1/aos-s/{serial_number}/traceroute"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = db.get_item(collection_path, serial_number) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, serial_number, existing)
    return existing

@app.api_route("/network-troubleshooting/v1/aos-s/{serial_number}/traceroute/async-operations/{task_id}", methods=["GET"])
def get_network_troubleshooting_v1_aos_s_serial_number_traceroute_async_operations_task_id(serial_number: str, task_id: str):
    """
    Aruba Central Endpoint: GET /network-troubleshooting/v1/aos-s/{serial-number}/traceroute/async-operations/{task-id}
    """
    collection_path = f"/network-troubleshooting/v1/aos-s/{serial_number}/traceroute/async-operations"
    item = db.get_item(collection_path, task_id)
    if item:
        return item
    static_val = db.get_static("get_network_troubleshooting_v1_aos_s_serial_number_traceroute_async_operations_task_id")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-troubleshooting/v1/aos-s/{serial_number}/poeBounce", methods=["POST"])
def post_network_troubleshooting_v1_aos_s_serial_number_poebounce(serial_number: str, payload: Aruba_initiatepvospoebouncev1_Request):
    """
    Aruba Central Endpoint: POST /network-troubleshooting/v1/aos-s/{serial-number}/poeBounce
    """
    collection_path = f"/network-troubleshooting/v1/aos-s/{serial_number}/poeBounce"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = db.get_item(collection_path, serial_number) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, serial_number, existing)
    return existing

@app.api_route("/network-troubleshooting/v1/aos-s/{serial_number}/poeBounce/async-operations/{task_id}", methods=["GET"])
def get_network_troubleshooting_v1_aos_s_serial_number_poebounce_async_operations_task_id(serial_number: str, task_id: str):
    """
    Aruba Central Endpoint: GET /network-troubleshooting/v1/aos-s/{serial-number}/poeBounce/async-operations/{task-id}
    """
    collection_path = f"/network-troubleshooting/v1/aos-s/{serial_number}/poeBounce/async-operations"
    item = db.get_item(collection_path, task_id)
    if item:
        return item
    static_val = db.get_static("get_network_troubleshooting_v1_aos_s_serial_number_poebounce_async_operations_task_id")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-troubleshooting/v1/aos-s/{serial_number}/portBounce", methods=["POST"])
def post_network_troubleshooting_v1_aos_s_serial_number_portbounce(serial_number: str, payload: Aruba_initiatepvosportbouncev1_Request):
    """
    Aruba Central Endpoint: POST /network-troubleshooting/v1/aos-s/{serial-number}/portBounce
    """
    collection_path = f"/network-troubleshooting/v1/aos-s/{serial_number}/portBounce"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = db.get_item(collection_path, serial_number) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, serial_number, existing)
    return existing

@app.api_route("/network-troubleshooting/v1/aos-s/{serial_number}/portBounce/async-operations/{task_id}", methods=["GET"])
def get_network_troubleshooting_v1_aos_s_serial_number_portbounce_async_operations_task_id(serial_number: str, task_id: str):
    """
    Aruba Central Endpoint: GET /network-troubleshooting/v1/aos-s/{serial-number}/portBounce/async-operations/{task-id}
    """
    collection_path = f"/network-troubleshooting/v1/aos-s/{serial_number}/portBounce/async-operations"
    item = db.get_item(collection_path, task_id)
    if item:
        return item
    static_val = db.get_static("get_network_troubleshooting_v1_aos_s_serial_number_portbounce_async_operations_task_id")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-troubleshooting/v1/aos-s/{serial_number}/cableTest", methods=["POST"])
def post_network_troubleshooting_v1_aos_s_serial_number_cabletest(serial_number: str, payload: Aruba_initiatepvoscabletestv1_Request):
    """
    Aruba Central Endpoint: POST /network-troubleshooting/v1/aos-s/{serial-number}/cableTest
    """
    collection_path = f"/network-troubleshooting/v1/aos-s/{serial_number}/cableTest"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = db.get_item(collection_path, serial_number) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, serial_number, existing)
    return existing

@app.api_route("/network-troubleshooting/v1/aos-s/{serial_number}/cableTest/async-operations/{task_id}", methods=["GET"])
def get_network_troubleshooting_v1_aos_s_serial_number_cabletest_async_operations_task_id(serial_number: str, task_id: str):
    """
    Aruba Central Endpoint: GET /network-troubleshooting/v1/aos-s/{serial-number}/cableTest/async-operations/{task-id}
    """
    collection_path = f"/network-troubleshooting/v1/aos-s/{serial_number}/cableTest/async-operations"
    item = db.get_item(collection_path, task_id)
    if item:
        return item
    static_val = db.get_static("get_network_troubleshooting_v1_aos_s_serial_number_cabletest_async_operations_task_id")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-troubleshooting/v1/aos-s/{serial_number}/getArpTable", methods=["POST"])
def post_network_troubleshooting_v1_aos_s_serial_number_getarptable(serial_number: str):
    """
    Aruba Central Endpoint: POST /network-troubleshooting/v1/aos-s/{serial-number}/getArpTable
    """
    collection_path = f"/network-troubleshooting/v1/aos-s/{serial_number}/getArpTable"
    payload_dict = {}
    existing = db.get_item(collection_path, serial_number) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, serial_number, existing)
    return existing

@app.api_route("/network-troubleshooting/v1/aos-s/{serial_number}/getArpTable/async-operations/{task_id}", methods=["GET"])
def get_network_troubleshooting_v1_aos_s_serial_number_getarptable_async_operations_task_id(serial_number: str, task_id: str):
    """
    Aruba Central Endpoint: GET /network-troubleshooting/v1/aos-s/{serial-number}/getArpTable/async-operations/{task-id}
    """
    collection_path = f"/network-troubleshooting/v1/aos-s/{serial_number}/getArpTable/async-operations"
    item = db.get_item(collection_path, task_id)
    if item:
        return item
    static_val = db.get_static("get_network_troubleshooting_v1_aos_s_serial_number_getarptable_async_operations_task_id")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-troubleshooting/v1/aos-s/{serial_number}/show-commands", methods=["GET"])
def get_network_troubleshooting_v1_aos_s_serial_number_show_commands(serial_number: str):
    """
    Aruba Central Endpoint: GET /network-troubleshooting/v1/aos-s/{serial-number}/show-commands
    """
    collection_path = f"/network-troubleshooting/v1/aos-s/{serial_number}/show-commands"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_troubleshooting_v1_aos_s_serial_number_show_commands", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-troubleshooting/v1/aos-s/{serial_number}/showCommands", methods=["POST"])
def post_network_troubleshooting_v1_aos_s_serial_number_showcommands(serial_number: str, payload: Aruba_runaossshowcommandsv1_Request):
    """
    Aruba Central Endpoint: POST /network-troubleshooting/v1/aos-s/{serial-number}/showCommands
    """
    collection_path = f"/network-troubleshooting/v1/aos-s/{serial_number}/showCommands"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = db.get_item(collection_path, serial_number) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, serial_number, existing)
    return existing

@app.api_route("/network-troubleshooting/v1/aos-s/{serial_number}/showCommands/async-operations/{task_id}", methods=["GET"])
def get_network_troubleshooting_v1_aos_s_serial_number_showcommands_async_operations_task_id(serial_number: str, task_id: str):
    """
    Aruba Central Endpoint: GET /network-troubleshooting/v1/aos-s/{serial-number}/showCommands/async-operations/{task-id}
    """
    collection_path = f"/network-troubleshooting/v1/aos-s/{serial_number}/showCommands/async-operations"
    item = db.get_item(collection_path, task_id)
    if item:
        return item
    static_val = db.get_static("get_network_troubleshooting_v1_aos_s_serial_number_showcommands_async_operations_task_id")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-troubleshooting/v1/aos-s/{serial_number}/reboot", methods=["POST"])
def post_network_troubleshooting_v1_aos_s_serial_number_reboot(serial_number: str):
    """
    Aruba Central Endpoint: POST /network-troubleshooting/v1/aos-s/{serial-number}/reboot
    """
    collection_path = f"/network-troubleshooting/v1/aos-s/{serial_number}/reboot"
    payload_dict = {}
    existing = db.get_item(collection_path, serial_number) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, serial_number, existing)
    return existing

@app.api_route("/network-troubleshooting/v1/aos-s/{serial_number}/locate", methods=["POST"])
def post_network_troubleshooting_v1_aos_s_serial_number_locate(serial_number: str):
    """
    Aruba Central Endpoint: POST /network-troubleshooting/v1/aos-s/{serial-number}/locate
    """
    collection_path = f"/network-troubleshooting/v1/aos-s/{serial_number}/locate"
    payload_dict = {}
    existing = db.get_item(collection_path, serial_number) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, serial_number, existing)
    return existing

@app.api_route("/network-troubleshooting/v1/aos-s/{serial_number}/list-tasks", methods=["GET"])
def get_network_troubleshooting_v1_aos_s_serial_number_list_tasks(serial_number: str):
    """
    Aruba Central Endpoint: GET /network-troubleshooting/v1/aos-s/{serial-number}/list-tasks
    """
    collection_path = f"/network-troubleshooting/v1/aos-s/{serial_number}/list-tasks"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_troubleshooting_v1_aos_s_serial_number_list_tasks", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-troubleshooting/v1/aps/{serial_number}/ping", methods=["POST"])
def post_network_troubleshooting_v1_aps_serial_number_ping(serial_number: str, payload: Aruba_initiateappingv1_Request):
    """
    Aruba Central Endpoint: POST /network-troubleshooting/v1/aps/{serial-number}/ping
    """
    collection_path = f"/network-troubleshooting/v1/aps/{serial_number}/ping"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = db.get_item(collection_path, serial_number) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, serial_number, existing)
    return existing

@app.api_route("/network-troubleshooting/v1/aps/{serial_number}/ping/async-operations/{task_id}", methods=["GET"])
def get_network_troubleshooting_v1_aps_serial_number_ping_async_operations_task_id(serial_number: str, task_id: str):
    """
    Aruba Central Endpoint: GET /network-troubleshooting/v1/aps/{serial-number}/ping/async-operations/{task-id}
    """
    collection_path = f"/network-troubleshooting/v1/aps/{serial_number}/ping/async-operations"
    item = db.get_item(collection_path, task_id)
    if item:
        return item
    static_val = db.get_static("get_network_troubleshooting_v1_aps_serial_number_ping_async_operations_task_id")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-troubleshooting/v1/aps/{serial_number}/traceroute", methods=["POST"])
def post_network_troubleshooting_v1_aps_serial_number_traceroute(serial_number: str, payload: Aruba_initiateaptraceroutev1_Request):
    """
    Aruba Central Endpoint: POST /network-troubleshooting/v1/aps/{serial-number}/traceroute
    """
    collection_path = f"/network-troubleshooting/v1/aps/{serial_number}/traceroute"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = db.get_item(collection_path, serial_number) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, serial_number, existing)
    return existing

@app.api_route("/network-troubleshooting/v1/aps/{serial_number}/traceroute/async-operations/{task_id}", methods=["GET"])
def get_network_troubleshooting_v1_aps_serial_number_traceroute_async_operations_task_id(serial_number: str, task_id: str):
    """
    Aruba Central Endpoint: GET /network-troubleshooting/v1/aps/{serial-number}/traceroute/async-operations/{task-id}
    """
    collection_path = f"/network-troubleshooting/v1/aps/{serial_number}/traceroute/async-operations"
    item = db.get_item(collection_path, task_id)
    if item:
        return item
    static_val = db.get_static("get_network_troubleshooting_v1_aps_serial_number_traceroute_async_operations_task_id")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-troubleshooting/v1/aps/{serial_number}/speedtest", methods=["POST"])
def post_network_troubleshooting_v1_aps_serial_number_speedtest(serial_number: str, payload: Aruba_initiateapspeedtestv1_Request):
    """
    Aruba Central Endpoint: POST /network-troubleshooting/v1/aps/{serial-number}/speedtest
    """
    collection_path = f"/network-troubleshooting/v1/aps/{serial_number}/speedtest"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = db.get_item(collection_path, serial_number) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, serial_number, existing)
    return existing

@app.api_route("/network-troubleshooting/v1/aps/{serial_number}/speedtest/async-operations/{task_id}", methods=["GET"])
def get_network_troubleshooting_v1_aps_serial_number_speedtest_async_operations_task_id(serial_number: str, task_id: str):
    """
    Aruba Central Endpoint: GET /network-troubleshooting/v1/aps/{serial-number}/speedtest/async-operations/{task-id}
    """
    collection_path = f"/network-troubleshooting/v1/aps/{serial_number}/speedtest/async-operations"
    item = db.get_item(collection_path, task_id)
    if item:
        return item
    static_val = db.get_static("get_network_troubleshooting_v1_aps_serial_number_speedtest_async_operations_task_id")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-troubleshooting/v1/aps/{serial_number}/http", methods=["POST"])
def post_network_troubleshooting_v1_aps_serial_number_http(serial_number: str, payload: Aruba_initiateaphttpv1_Request):
    """
    Aruba Central Endpoint: POST /network-troubleshooting/v1/aps/{serial-number}/http
    """
    collection_path = f"/network-troubleshooting/v1/aps/{serial_number}/http"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = db.get_item(collection_path, serial_number) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, serial_number, existing)
    return existing

@app.api_route("/network-troubleshooting/v1/aps/{serial_number}/http/async-operations/{task_id}", methods=["GET"])
def get_network_troubleshooting_v1_aps_serial_number_http_async_operations_task_id(serial_number: str, task_id: str):
    """
    Aruba Central Endpoint: GET /network-troubleshooting/v1/aps/{serial-number}/http/async-operations/{task-id}
    """
    collection_path = f"/network-troubleshooting/v1/aps/{serial_number}/http/async-operations"
    item = db.get_item(collection_path, task_id)
    if item:
        return item
    static_val = db.get_static("get_network_troubleshooting_v1_aps_serial_number_http_async_operations_task_id")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-troubleshooting/v1/aps/{serial_number}/https", methods=["POST"])
def post_network_troubleshooting_v1_aps_serial_number_https(serial_number: str, payload: Aruba_initiateaphttpsv1_Request):
    """
    Aruba Central Endpoint: POST /network-troubleshooting/v1/aps/{serial-number}/https
    """
    collection_path = f"/network-troubleshooting/v1/aps/{serial_number}/https"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = db.get_item(collection_path, serial_number) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, serial_number, existing)
    return existing

@app.api_route("/network-troubleshooting/v1/aps/{serial_number}/https/async-operations/{task_id}", methods=["GET"])
def get_network_troubleshooting_v1_aps_serial_number_https_async_operations_task_id(serial_number: str, task_id: str):
    """
    Aruba Central Endpoint: GET /network-troubleshooting/v1/aps/{serial-number}/https/async-operations/{task-id}
    """
    collection_path = f"/network-troubleshooting/v1/aps/{serial_number}/https/async-operations"
    item = db.get_item(collection_path, task_id)
    if item:
        return item
    static_val = db.get_static("get_network_troubleshooting_v1_aps_serial_number_https_async_operations_task_id")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-troubleshooting/v1/aps/{serial_number}/tcp", methods=["POST"])
def post_network_troubleshooting_v1_aps_serial_number_tcp(serial_number: str, payload: Aruba_initiateaptcpv1_Request):
    """
    Aruba Central Endpoint: POST /network-troubleshooting/v1/aps/{serial-number}/tcp
    """
    collection_path = f"/network-troubleshooting/v1/aps/{serial_number}/tcp"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = db.get_item(collection_path, serial_number) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, serial_number, existing)
    return existing

@app.api_route("/network-troubleshooting/v1/aps/{serial_number}/tcp/async-operations/{task_id}", methods=["GET"])
def get_network_troubleshooting_v1_aps_serial_number_tcp_async_operations_task_id(serial_number: str, task_id: str):
    """
    Aruba Central Endpoint: GET /network-troubleshooting/v1/aps/{serial-number}/tcp/async-operations/{task-id}
    """
    collection_path = f"/network-troubleshooting/v1/aps/{serial_number}/tcp/async-operations"
    item = db.get_item(collection_path, task_id)
    if item:
        return item
    static_val = db.get_static("get_network_troubleshooting_v1_aps_serial_number_tcp_async_operations_task_id")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-troubleshooting/v1/aps/{serial_number}/getArpTable", methods=["POST"])
def post_network_troubleshooting_v1_aps_serial_number_getarptable(serial_number: str):
    """
    Aruba Central Endpoint: POST /network-troubleshooting/v1/aps/{serial-number}/getArpTable
    """
    collection_path = f"/network-troubleshooting/v1/aps/{serial_number}/getArpTable"
    payload_dict = {}
    existing = db.get_item(collection_path, serial_number) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, serial_number, existing)
    return existing

@app.api_route("/network-troubleshooting/v1/aps/{serial_number}/getArpTable/async-operations/{task_id}", methods=["GET"])
def get_network_troubleshooting_v1_aps_serial_number_getarptable_async_operations_task_id(serial_number: str, task_id: str):
    """
    Aruba Central Endpoint: GET /network-troubleshooting/v1/aps/{serial-number}/getArpTable/async-operations/{task-id}
    """
    collection_path = f"/network-troubleshooting/v1/aps/{serial_number}/getArpTable/async-operations"
    item = db.get_item(collection_path, task_id)
    if item:
        return item
    static_val = db.get_static("get_network_troubleshooting_v1_aps_serial_number_getarptable_async_operations_task_id")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-troubleshooting/v1/aps/{serial_number}/nslookup", methods=["POST"])
def post_network_troubleshooting_v1_aps_serial_number_nslookup(serial_number: str, payload: Aruba_initiateapnslookupv1_Request):
    """
    Aruba Central Endpoint: POST /network-troubleshooting/v1/aps/{serial-number}/nslookup
    """
    collection_path = f"/network-troubleshooting/v1/aps/{serial_number}/nslookup"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = db.get_item(collection_path, serial_number) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, serial_number, existing)
    return existing

@app.api_route("/network-troubleshooting/v1/aps/{serial_number}/nslookup/async-operations/{task_id}", methods=["GET"])
def get_network_troubleshooting_v1_aps_serial_number_nslookup_async_operations_task_id(serial_number: str, task_id: str):
    """
    Aruba Central Endpoint: GET /network-troubleshooting/v1/aps/{serial-number}/nslookup/async-operations/{task-id}
    """
    collection_path = f"/network-troubleshooting/v1/aps/{serial_number}/nslookup/async-operations"
    item = db.get_item(collection_path, task_id)
    if item:
        return item
    static_val = db.get_static("get_network_troubleshooting_v1_aps_serial_number_nslookup_async_operations_task_id")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-troubleshooting/v1/aps/{serial_number}/aaa", methods=["POST"])
def post_network_troubleshooting_v1_aps_serial_number_aaa(serial_number: str, payload: Aruba_initiateapaaav1_Request):
    """
    Aruba Central Endpoint: POST /network-troubleshooting/v1/aps/{serial-number}/aaa
    """
    collection_path = f"/network-troubleshooting/v1/aps/{serial_number}/aaa"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = db.get_item(collection_path, serial_number) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, serial_number, existing)
    return existing

@app.api_route("/network-troubleshooting/v1/aps/{serial_number}/aaa/async-operations/{task_id}", methods=["GET"])
def get_network_troubleshooting_v1_aps_serial_number_aaa_async_operations_task_id(serial_number: str, task_id: str):
    """
    Aruba Central Endpoint: GET /network-troubleshooting/v1/aps/{serial-number}/aaa/async-operations/{task-id}
    """
    collection_path = f"/network-troubleshooting/v1/aps/{serial_number}/aaa/async-operations"
    item = db.get_item(collection_path, task_id)
    if item:
        return item
    static_val = db.get_static("get_network_troubleshooting_v1_aps_serial_number_aaa_async_operations_task_id")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-troubleshooting/v1/aps/{serial_number}/show-commands", methods=["GET"])
def get_network_troubleshooting_v1_aps_serial_number_show_commands(serial_number: str):
    """
    Aruba Central Endpoint: GET /network-troubleshooting/v1/aps/{serial-number}/show-commands
    """
    collection_path = f"/network-troubleshooting/v1/aps/{serial_number}/show-commands"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_troubleshooting_v1_aps_serial_number_show_commands", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-troubleshooting/v1/aps/{serial_number}/showCommands", methods=["POST"])
def post_network_troubleshooting_v1_aps_serial_number_showcommands(serial_number: str, payload: Aruba_runapshowcommandsv1_Request):
    """
    Aruba Central Endpoint: POST /network-troubleshooting/v1/aps/{serial-number}/showCommands
    """
    collection_path = f"/network-troubleshooting/v1/aps/{serial_number}/showCommands"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = db.get_item(collection_path, serial_number) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, serial_number, existing)
    return existing

@app.api_route("/network-troubleshooting/v1/aps/{serial_number}/showCommands/async-operations/{task_id}", methods=["GET"])
def get_network_troubleshooting_v1_aps_serial_number_showcommands_async_operations_task_id(serial_number: str, task_id: str):
    """
    Aruba Central Endpoint: GET /network-troubleshooting/v1/aps/{serial-number}/showCommands/async-operations/{task-id}
    """
    collection_path = f"/network-troubleshooting/v1/aps/{serial_number}/showCommands/async-operations"
    item = db.get_item(collection_path, task_id)
    if item:
        return item
    static_val = db.get_static("get_network_troubleshooting_v1_aps_serial_number_showcommands_async_operations_task_id")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-troubleshooting/v1/aps/{serial_number}/reboot", methods=["POST"])
def post_network_troubleshooting_v1_aps_serial_number_reboot(serial_number: str):
    """
    Aruba Central Endpoint: POST /network-troubleshooting/v1/aps/{serial-number}/reboot
    """
    collection_path = f"/network-troubleshooting/v1/aps/{serial_number}/reboot"
    payload_dict = {}
    existing = db.get_item(collection_path, serial_number) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, serial_number, existing)
    return existing

@app.api_route("/network-troubleshooting/v1/aps/{serial_number}/rebootSwarm", methods=["POST"])
def post_network_troubleshooting_v1_aps_serial_number_rebootswarm(serial_number: str):
    """
    Aruba Central Endpoint: POST /network-troubleshooting/v1/aps/{serial-number}/rebootSwarm
    """
    collection_path = f"/network-troubleshooting/v1/aps/{serial_number}/rebootSwarm"
    payload_dict = {}
    existing = db.get_item(collection_path, serial_number) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, serial_number, existing)
    return existing

@app.api_route("/network-troubleshooting/v1/aps/{serial_number}/locate", methods=["POST"])
def post_network_troubleshooting_v1_aps_serial_number_locate(serial_number: str):
    """
    Aruba Central Endpoint: POST /network-troubleshooting/v1/aps/{serial-number}/locate
    """
    collection_path = f"/network-troubleshooting/v1/aps/{serial_number}/locate"
    payload_dict = {}
    existing = db.get_item(collection_path, serial_number) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, serial_number, existing)
    return existing

@app.api_route("/network-troubleshooting/v1/aps/{serial_number}/disconnectUserAll", methods=["POST"])
def post_network_troubleshooting_v1_aps_serial_number_disconnectuserall(serial_number: str):
    """
    Aruba Central Endpoint: POST /network-troubleshooting/v1/aps/{serial-number}/disconnectUserAll
    """
    collection_path = f"/network-troubleshooting/v1/aps/{serial_number}/disconnectUserAll"
    payload_dict = {}
    existing = db.get_item(collection_path, serial_number) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, serial_number, existing)
    return existing

@app.api_route("/network-troubleshooting/v1/aps/{serial_number}/disconnectUserByMacAddress", methods=["POST"])
def post_network_troubleshooting_v1_aps_serial_number_disconnectuserbymacaddress(serial_number: str, payload: Aruba_disconnectuserbymacapv1_Request):
    """
    Aruba Central Endpoint: POST /network-troubleshooting/v1/aps/{serial-number}/disconnectUserByMacAddress
    """
    collection_path = f"/network-troubleshooting/v1/aps/{serial_number}/disconnectUserByMacAddress"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = db.get_item(collection_path, serial_number) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, serial_number, existing)
    return existing

@app.api_route("/network-troubleshooting/v1/aps/{serial_number}/disconnectUserByNetwork", methods=["POST"])
def post_network_troubleshooting_v1_aps_serial_number_disconnectuserbynetwork(serial_number: str, payload: Aruba_disconnectuserbynetworkapv1_Request):
    """
    Aruba Central Endpoint: POST /network-troubleshooting/v1/aps/{serial-number}/disconnectUserByNetwork
    """
    collection_path = f"/network-troubleshooting/v1/aps/{serial_number}/disconnectUserByNetwork"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = db.get_item(collection_path, serial_number) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, serial_number, existing)
    return existing

@app.api_route("/network-troubleshooting/v1/aps/{serial_number}/list-tasks", methods=["GET"])
def get_network_troubleshooting_v1_aps_serial_number_list_tasks(serial_number: str):
    """
    Aruba Central Endpoint: GET /network-troubleshooting/v1/aps/{serial-number}/list-tasks
    """
    collection_path = f"/network-troubleshooting/v1/aps/{serial_number}/list-tasks"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_troubleshooting_v1_aps_serial_number_list_tasks", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-troubleshooting/v1/cx/{serial_number}/ping", methods=["POST"])
def post_network_troubleshooting_v1_cx_serial_number_ping(serial_number: str, payload: Aruba_initiatecxpingv1_Request):
    """
    Aruba Central Endpoint: POST /network-troubleshooting/v1/cx/{serial-number}/ping
    """
    collection_path = f"/network-troubleshooting/v1/cx/{serial_number}/ping"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = db.get_item(collection_path, serial_number) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, serial_number, existing)
    return existing

@app.api_route("/network-troubleshooting/v1/cx/{serial_number}/ping/async-operations/{task_id}", methods=["GET"])
def get_network_troubleshooting_v1_cx_serial_number_ping_async_operations_task_id(serial_number: str, task_id: str):
    """
    Aruba Central Endpoint: GET /network-troubleshooting/v1/cx/{serial-number}/ping/async-operations/{task-id}
    """
    collection_path = f"/network-troubleshooting/v1/cx/{serial_number}/ping/async-operations"
    item = db.get_item(collection_path, task_id)
    if item:
        return item
    static_val = db.get_static("get_network_troubleshooting_v1_cx_serial_number_ping_async_operations_task_id")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-troubleshooting/v1/cx/{serial_number}/traceroute", methods=["POST"])
def post_network_troubleshooting_v1_cx_serial_number_traceroute(serial_number: str, payload: Aruba_initiatecxtraceroutev1_Request):
    """
    Aruba Central Endpoint: POST /network-troubleshooting/v1/cx/{serial-number}/traceroute
    """
    collection_path = f"/network-troubleshooting/v1/cx/{serial_number}/traceroute"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = db.get_item(collection_path, serial_number) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, serial_number, existing)
    return existing

@app.api_route("/network-troubleshooting/v1/cx/{serial_number}/traceroute/async-operations/{task_id}", methods=["GET"])
def get_network_troubleshooting_v1_cx_serial_number_traceroute_async_operations_task_id(serial_number: str, task_id: str):
    """
    Aruba Central Endpoint: GET /network-troubleshooting/v1/cx/{serial-number}/traceroute/async-operations/{task-id}
    """
    collection_path = f"/network-troubleshooting/v1/cx/{serial_number}/traceroute/async-operations"
    item = db.get_item(collection_path, task_id)
    if item:
        return item
    static_val = db.get_static("get_network_troubleshooting_v1_cx_serial_number_traceroute_async_operations_task_id")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-troubleshooting/v1/cx/{serial_number}/poeBounce", methods=["POST"])
def post_network_troubleshooting_v1_cx_serial_number_poebounce(serial_number: str, payload: Aruba_initiatecxpoebouncev1_Request):
    """
    Aruba Central Endpoint: POST /network-troubleshooting/v1/cx/{serial-number}/poeBounce
    """
    collection_path = f"/network-troubleshooting/v1/cx/{serial_number}/poeBounce"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = db.get_item(collection_path, serial_number) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, serial_number, existing)
    return existing

@app.api_route("/network-troubleshooting/v1/cx/{serial_number}/poeBounce/async-operations/{task_id}", methods=["GET"])
def get_network_troubleshooting_v1_cx_serial_number_poebounce_async_operations_task_id(serial_number: str, task_id: str):
    """
    Aruba Central Endpoint: GET /network-troubleshooting/v1/cx/{serial-number}/poeBounce/async-operations/{task-id}
    """
    collection_path = f"/network-troubleshooting/v1/cx/{serial_number}/poeBounce/async-operations"
    item = db.get_item(collection_path, task_id)
    if item:
        return item
    static_val = db.get_static("get_network_troubleshooting_v1_cx_serial_number_poebounce_async_operations_task_id")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-troubleshooting/v1/cx/{serial_number}/portBounce", methods=["POST"])
def post_network_troubleshooting_v1_cx_serial_number_portbounce(serial_number: str, payload: Aruba_initiatecxportbouncev1_Request):
    """
    Aruba Central Endpoint: POST /network-troubleshooting/v1/cx/{serial-number}/portBounce
    """
    collection_path = f"/network-troubleshooting/v1/cx/{serial_number}/portBounce"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = db.get_item(collection_path, serial_number) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, serial_number, existing)
    return existing

@app.api_route("/network-troubleshooting/v1/cx/{serial_number}/portBounce/async-operations/{task_id}", methods=["GET"])
def get_network_troubleshooting_v1_cx_serial_number_portbounce_async_operations_task_id(serial_number: str, task_id: str):
    """
    Aruba Central Endpoint: GET /network-troubleshooting/v1/cx/{serial-number}/portBounce/async-operations/{task-id}
    """
    collection_path = f"/network-troubleshooting/v1/cx/{serial_number}/portBounce/async-operations"
    item = db.get_item(collection_path, task_id)
    if item:
        return item
    static_val = db.get_static("get_network_troubleshooting_v1_cx_serial_number_portbounce_async_operations_task_id")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-troubleshooting/v1/cx/{serial_number}/cableTest", methods=["POST"])
def post_network_troubleshooting_v1_cx_serial_number_cabletest(serial_number: str, payload: Aruba_initiatecxcabletestv1_Request):
    """
    Aruba Central Endpoint: POST /network-troubleshooting/v1/cx/{serial-number}/cableTest
    """
    collection_path = f"/network-troubleshooting/v1/cx/{serial_number}/cableTest"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = db.get_item(collection_path, serial_number) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, serial_number, existing)
    return existing

@app.api_route("/network-troubleshooting/v1/cx/{serial_number}/cableTest/async-operations/{task_id}", methods=["GET"])
def get_network_troubleshooting_v1_cx_serial_number_cabletest_async_operations_task_id(serial_number: str, task_id: str):
    """
    Aruba Central Endpoint: GET /network-troubleshooting/v1/cx/{serial-number}/cableTest/async-operations/{task-id}
    """
    collection_path = f"/network-troubleshooting/v1/cx/{serial_number}/cableTest/async-operations"
    item = db.get_item(collection_path, task_id)
    if item:
        return item
    static_val = db.get_static("get_network_troubleshooting_v1_cx_serial_number_cabletest_async_operations_task_id")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-troubleshooting/v1/cx/{serial_number}/http", methods=["POST"])
def post_network_troubleshooting_v1_cx_serial_number_http(serial_number: str, payload: Aruba_initiatecxhttpv1_Request):
    """
    Aruba Central Endpoint: POST /network-troubleshooting/v1/cx/{serial-number}/http
    """
    collection_path = f"/network-troubleshooting/v1/cx/{serial_number}/http"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = db.get_item(collection_path, serial_number) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, serial_number, existing)
    return existing

@app.api_route("/network-troubleshooting/v1/cx/{serial_number}/http/async-operations/{task_id}", methods=["GET"])
def get_network_troubleshooting_v1_cx_serial_number_http_async_operations_task_id(serial_number: str, task_id: str):
    """
    Aruba Central Endpoint: GET /network-troubleshooting/v1/cx/{serial-number}/http/async-operations/{task-id}
    """
    collection_path = f"/network-troubleshooting/v1/cx/{serial_number}/http/async-operations"
    item = db.get_item(collection_path, task_id)
    if item:
        return item
    static_val = db.get_static("get_network_troubleshooting_v1_cx_serial_number_http_async_operations_task_id")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-troubleshooting/v1/cx/{serial_number}/aaa", methods=["POST"])
def post_network_troubleshooting_v1_cx_serial_number_aaa(serial_number: str, payload: Aruba_initiatecxaaav1_Request):
    """
    Aruba Central Endpoint: POST /network-troubleshooting/v1/cx/{serial-number}/aaa
    """
    collection_path = f"/network-troubleshooting/v1/cx/{serial_number}/aaa"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = db.get_item(collection_path, serial_number) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, serial_number, existing)
    return existing

@app.api_route("/network-troubleshooting/v1/cx/{serial_number}/aaa/async-operations/{task_id}", methods=["GET"])
def get_network_troubleshooting_v1_cx_serial_number_aaa_async_operations_task_id(serial_number: str, task_id: str):
    """
    Aruba Central Endpoint: GET /network-troubleshooting/v1/cx/{serial-number}/aaa/async-operations/{task-id}
    """
    collection_path = f"/network-troubleshooting/v1/cx/{serial_number}/aaa/async-operations"
    item = db.get_item(collection_path, task_id)
    if item:
        return item
    static_val = db.get_static("get_network_troubleshooting_v1_cx_serial_number_aaa_async_operations_task_id")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-troubleshooting/v1/cx/{serial_number}/show-commands", methods=["GET"])
def get_network_troubleshooting_v1_cx_serial_number_show_commands(serial_number: str):
    """
    Aruba Central Endpoint: GET /network-troubleshooting/v1/cx/{serial-number}/show-commands
    """
    collection_path = f"/network-troubleshooting/v1/cx/{serial_number}/show-commands"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_troubleshooting_v1_cx_serial_number_show_commands", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-troubleshooting/v1/cx/{serial_number}/showCommands", methods=["POST"])
def post_network_troubleshooting_v1_cx_serial_number_showcommands(serial_number: str, payload: Aruba_runcxshowcommandsv1_Request):
    """
    Aruba Central Endpoint: POST /network-troubleshooting/v1/cx/{serial-number}/showCommands
    """
    collection_path = f"/network-troubleshooting/v1/cx/{serial_number}/showCommands"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = db.get_item(collection_path, serial_number) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, serial_number, existing)
    return existing

@app.api_route("/network-troubleshooting/v1/cx/{serial_number}/showCommands/async-operations/{task_id}", methods=["GET"])
def get_network_troubleshooting_v1_cx_serial_number_showcommands_async_operations_task_id(serial_number: str, task_id: str):
    """
    Aruba Central Endpoint: GET /network-troubleshooting/v1/cx/{serial-number}/showCommands/async-operations/{task-id}
    """
    collection_path = f"/network-troubleshooting/v1/cx/{serial_number}/showCommands/async-operations"
    item = db.get_item(collection_path, task_id)
    if item:
        return item
    static_val = db.get_static("get_network_troubleshooting_v1_cx_serial_number_showcommands_async_operations_task_id")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-troubleshooting/v1/cx/{serial_number}/locate", methods=["POST"])
def post_network_troubleshooting_v1_cx_serial_number_locate(serial_number: str):
    """
    Aruba Central Endpoint: POST /network-troubleshooting/v1/cx/{serial-number}/locate
    """
    collection_path = f"/network-troubleshooting/v1/cx/{serial_number}/locate"
    payload_dict = {}
    existing = db.get_item(collection_path, serial_number) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, serial_number, existing)
    return existing

@app.api_route("/network-troubleshooting/v1/cx/{serial_number}/reboot", methods=["POST"])
def post_network_troubleshooting_v1_cx_serial_number_reboot(serial_number: str):
    """
    Aruba Central Endpoint: POST /network-troubleshooting/v1/cx/{serial-number}/reboot
    """
    collection_path = f"/network-troubleshooting/v1/cx/{serial_number}/reboot"
    payload_dict = {}
    existing = db.get_item(collection_path, serial_number) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, serial_number, existing)
    return existing

@app.api_route("/network-troubleshooting/v1/cx/{serial_number}/list-tasks", methods=["GET"])
def get_network_troubleshooting_v1_cx_serial_number_list_tasks(serial_number: str):
    """
    Aruba Central Endpoint: GET /network-troubleshooting/v1/cx/{serial-number}/list-tasks
    """
    collection_path = f"/network-troubleshooting/v1/cx/{serial_number}/list-tasks"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_troubleshooting_v1_cx_serial_number_list_tasks", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-troubleshooting/v1/events", methods=["GET"])
def get_network_troubleshooting_v1_events():
    """
    Aruba Central Endpoint: GET /network-troubleshooting/v1/events
    """
    collection_path = "/network-troubleshooting/v1/events"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_troubleshooting_v1_events", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-troubleshooting/v1/event-extra-attributes", methods=["GET"])
def get_network_troubleshooting_v1_event_extra_attributes():
    """
    Aruba Central Endpoint: GET /network-troubleshooting/v1/event-extra-attributes
    """
    collection_path = "/network-troubleshooting/v1/event-extra-attributes"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_troubleshooting_v1_event_extra_attributes", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-troubleshooting/v1/event-filters", methods=["GET"])
def get_network_troubleshooting_v1_event_filters():
    """
    Aruba Central Endpoint: GET /network-troubleshooting/v1/event-filters
    """
    collection_path = "/network-troubleshooting/v1/event-filters"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_troubleshooting_v1_event_filters", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-troubleshooting/v1/gateways/{serial_number}/ping", methods=["POST"])
def post_network_troubleshooting_v1_gateways_serial_number_ping(serial_number: str, payload: Aruba_initiategwpingv1_Request):
    """
    Aruba Central Endpoint: POST /network-troubleshooting/v1/gateways/{serial-number}/ping
    """
    collection_path = f"/network-troubleshooting/v1/gateways/{serial_number}/ping"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = db.get_item(collection_path, serial_number) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, serial_number, existing)
    return existing

@app.api_route("/network-troubleshooting/v1/gateways/{serial_number}/ping/async-operations/{task_id}", methods=["GET"])
def get_network_troubleshooting_v1_gateways_serial_number_ping_async_operations_task_id(serial_number: str, task_id: str):
    """
    Aruba Central Endpoint: GET /network-troubleshooting/v1/gateways/{serial-number}/ping/async-operations/{task-id}
    """
    collection_path = f"/network-troubleshooting/v1/gateways/{serial_number}/ping/async-operations"
    item = db.get_item(collection_path, task_id)
    if item:
        return item
    static_val = db.get_static("get_network_troubleshooting_v1_gateways_serial_number_ping_async_operations_task_id")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-troubleshooting/v1/gateways/{serial_number}/pingSweep", methods=["POST"])
def post_network_troubleshooting_v1_gateways_serial_number_pingsweep(serial_number: str, payload: Aruba_rungatewaypingsweepv1_Request):
    """
    Aruba Central Endpoint: POST /network-troubleshooting/v1/gateways/{serial-number}/pingSweep
    """
    collection_path = f"/network-troubleshooting/v1/gateways/{serial_number}/pingSweep"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = db.get_item(collection_path, serial_number) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, serial_number, existing)
    return existing

@app.api_route("/network-troubleshooting/v1/gateways/{serial_number}/pingSweep/async-operations/{task_id}", methods=["GET"])
def get_network_troubleshooting_v1_gateways_serial_number_pingsweep_async_operations_task_id(serial_number: str, task_id: str):
    """
    Aruba Central Endpoint: GET /network-troubleshooting/v1/gateways/{serial-number}/pingSweep/async-operations/{task-id}
    """
    collection_path = f"/network-troubleshooting/v1/gateways/{serial_number}/pingSweep/async-operations"
    item = db.get_item(collection_path, task_id)
    if item:
        return item
    static_val = db.get_static("get_network_troubleshooting_v1_gateways_serial_number_pingsweep_async_operations_task_id")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-troubleshooting/v1/gateways/{serial_number}/traceroute", methods=["POST"])
def post_network_troubleshooting_v1_gateways_serial_number_traceroute(serial_number: str, payload: Aruba_initiategwtraceroutev1_Request):
    """
    Aruba Central Endpoint: POST /network-troubleshooting/v1/gateways/{serial-number}/traceroute
    """
    collection_path = f"/network-troubleshooting/v1/gateways/{serial_number}/traceroute"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = db.get_item(collection_path, serial_number) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, serial_number, existing)
    return existing

@app.api_route("/network-troubleshooting/v1/gateways/{serial_number}/traceroute/async-operations/{task_id}", methods=["GET"])
def get_network_troubleshooting_v1_gateways_serial_number_traceroute_async_operations_task_id(serial_number: str, task_id: str):
    """
    Aruba Central Endpoint: GET /network-troubleshooting/v1/gateways/{serial-number}/traceroute/async-operations/{task-id}
    """
    collection_path = f"/network-troubleshooting/v1/gateways/{serial_number}/traceroute/async-operations"
    item = db.get_item(collection_path, task_id)
    if item:
        return item
    static_val = db.get_static("get_network_troubleshooting_v1_gateways_serial_number_traceroute_async_operations_task_id")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-troubleshooting/v1/gateways/{serial_number}/poeBounce", methods=["POST"])
def post_network_troubleshooting_v1_gateways_serial_number_poebounce(serial_number: str, payload: Aruba_initiategwpoebouncev1_Request):
    """
    Aruba Central Endpoint: POST /network-troubleshooting/v1/gateways/{serial-number}/poeBounce
    """
    collection_path = f"/network-troubleshooting/v1/gateways/{serial_number}/poeBounce"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = db.get_item(collection_path, serial_number) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, serial_number, existing)
    return existing

@app.api_route("/network-troubleshooting/v1/gateways/{serial_number}/poeBounce/async-operations/{task_id}", methods=["GET"])
def get_network_troubleshooting_v1_gateways_serial_number_poebounce_async_operations_task_id(serial_number: str, task_id: str):
    """
    Aruba Central Endpoint: GET /network-troubleshooting/v1/gateways/{serial-number}/poeBounce/async-operations/{task-id}
    """
    collection_path = f"/network-troubleshooting/v1/gateways/{serial_number}/poeBounce/async-operations"
    item = db.get_item(collection_path, task_id)
    if item:
        return item
    static_val = db.get_static("get_network_troubleshooting_v1_gateways_serial_number_poebounce_async_operations_task_id")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-troubleshooting/v1/gateways/{serial_number}/portBounce", methods=["POST"])
def post_network_troubleshooting_v1_gateways_serial_number_portbounce(serial_number: str, payload: Aruba_initiategwportbouncev1_Request):
    """
    Aruba Central Endpoint: POST /network-troubleshooting/v1/gateways/{serial-number}/portBounce
    """
    collection_path = f"/network-troubleshooting/v1/gateways/{serial_number}/portBounce"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = db.get_item(collection_path, serial_number) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, serial_number, existing)
    return existing

@app.api_route("/network-troubleshooting/v1/gateways/{serial_number}/portBounce/async-operations/{task_id}", methods=["GET"])
def get_network_troubleshooting_v1_gateways_serial_number_portbounce_async_operations_task_id(serial_number: str, task_id: str):
    """
    Aruba Central Endpoint: GET /network-troubleshooting/v1/gateways/{serial-number}/portBounce/async-operations/{task-id}
    """
    collection_path = f"/network-troubleshooting/v1/gateways/{serial_number}/portBounce/async-operations"
    item = db.get_item(collection_path, task_id)
    if item:
        return item
    static_val = db.get_static("get_network_troubleshooting_v1_gateways_serial_number_portbounce_async_operations_task_id")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-troubleshooting/v1/gateways/{serial_number}/iperf", methods=["POST"])
def post_network_troubleshooting_v1_gateways_serial_number_iperf(serial_number: str, payload: Aruba_initiategwiperfv1_Request):
    """
    Aruba Central Endpoint: POST /network-troubleshooting/v1/gateways/{serial-number}/iperf
    """
    collection_path = f"/network-troubleshooting/v1/gateways/{serial_number}/iperf"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = db.get_item(collection_path, serial_number) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, serial_number, existing)
    return existing

@app.api_route("/network-troubleshooting/v1/gateways/{serial_number}/iperf/async-operations/{task_id}", methods=["GET"])
def get_network_troubleshooting_v1_gateways_serial_number_iperf_async_operations_task_id(serial_number: str, task_id: str):
    """
    Aruba Central Endpoint: GET /network-troubleshooting/v1/gateways/{serial-number}/iperf/async-operations/{task-id}
    """
    collection_path = f"/network-troubleshooting/v1/gateways/{serial_number}/iperf/async-operations"
    item = db.get_item(collection_path, task_id)
    if item:
        return item
    static_val = db.get_static("get_network_troubleshooting_v1_gateways_serial_number_iperf_async_operations_task_id")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-troubleshooting/v1/gateways/{serial_number}/http", methods=["POST"])
def post_network_troubleshooting_v1_gateways_serial_number_http(serial_number: str, payload: Aruba_initiategwhttpv1_Request):
    """
    Aruba Central Endpoint: POST /network-troubleshooting/v1/gateways/{serial-number}/http
    """
    collection_path = f"/network-troubleshooting/v1/gateways/{serial_number}/http"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = db.get_item(collection_path, serial_number) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, serial_number, existing)
    return existing

@app.api_route("/network-troubleshooting/v1/gateways/{serial_number}/http/async-operations/{task_id}", methods=["GET"])
def get_network_troubleshooting_v1_gateways_serial_number_http_async_operations_task_id(serial_number: str, task_id: str):
    """
    Aruba Central Endpoint: GET /network-troubleshooting/v1/gateways/{serial-number}/http/async-operations/{task-id}
    """
    collection_path = f"/network-troubleshooting/v1/gateways/{serial_number}/http/async-operations"
    item = db.get_item(collection_path, task_id)
    if item:
        return item
    static_val = db.get_static("get_network_troubleshooting_v1_gateways_serial_number_http_async_operations_task_id")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-troubleshooting/v1/gateways/{serial_number}/https", methods=["POST"])
def post_network_troubleshooting_v1_gateways_serial_number_https(serial_number: str, payload: Aruba_initiategwhttpsv1_Request):
    """
    Aruba Central Endpoint: POST /network-troubleshooting/v1/gateways/{serial-number}/https
    """
    collection_path = f"/network-troubleshooting/v1/gateways/{serial_number}/https"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = db.get_item(collection_path, serial_number) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, serial_number, existing)
    return existing

@app.api_route("/network-troubleshooting/v1/gateways/{serial_number}/https/async-operations/{task_id}", methods=["GET"])
def get_network_troubleshooting_v1_gateways_serial_number_https_async_operations_task_id(serial_number: str, task_id: str):
    """
    Aruba Central Endpoint: GET /network-troubleshooting/v1/gateways/{serial-number}/https/async-operations/{task-id}
    """
    collection_path = f"/network-troubleshooting/v1/gateways/{serial_number}/https/async-operations"
    item = db.get_item(collection_path, task_id)
    if item:
        return item
    static_val = db.get_static("get_network_troubleshooting_v1_gateways_serial_number_https_async_operations_task_id")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-troubleshooting/v1/gateways/{serial_number}/getArpTable", methods=["POST"])
def post_network_troubleshooting_v1_gateways_serial_number_getarptable(serial_number: str):
    """
    Aruba Central Endpoint: POST /network-troubleshooting/v1/gateways/{serial-number}/getArpTable
    """
    collection_path = f"/network-troubleshooting/v1/gateways/{serial_number}/getArpTable"
    payload_dict = {}
    existing = db.get_item(collection_path, serial_number) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, serial_number, existing)
    return existing

@app.api_route("/network-troubleshooting/v1/gateways/{serial_number}/getArpTable/async-operations/{task_id}", methods=["GET"])
def get_network_troubleshooting_v1_gateways_serial_number_getarptable_async_operations_task_id(serial_number: str, task_id: str):
    """
    Aruba Central Endpoint: GET /network-troubleshooting/v1/gateways/{serial-number}/getArpTable/async-operations/{task-id}
    """
    collection_path = f"/network-troubleshooting/v1/gateways/{serial_number}/getArpTable/async-operations"
    item = db.get_item(collection_path, task_id)
    if item:
        return item
    static_val = db.get_static("get_network_troubleshooting_v1_gateways_serial_number_getarptable_async_operations_task_id")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-troubleshooting/v1/gateways/{serial_number}/show-commands", methods=["GET"])
def get_network_troubleshooting_v1_gateways_serial_number_show_commands(serial_number: str):
    """
    Aruba Central Endpoint: GET /network-troubleshooting/v1/gateways/{serial-number}/show-commands
    """
    collection_path = f"/network-troubleshooting/v1/gateways/{serial_number}/show-commands"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_troubleshooting_v1_gateways_serial_number_show_commands", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val

@app.api_route("/network-troubleshooting/v1/gateways/{serial_number}/showCommands", methods=["POST"])
def post_network_troubleshooting_v1_gateways_serial_number_showcommands(serial_number: str, payload: Aruba_rungwshowcommandsv1_Request):
    """
    Aruba Central Endpoint: POST /network-troubleshooting/v1/gateways/{serial-number}/showCommands
    """
    collection_path = f"/network-troubleshooting/v1/gateways/{serial_number}/showCommands"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = db.get_item(collection_path, serial_number) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, serial_number, existing)
    return existing

@app.api_route("/network-troubleshooting/v1/gateways/{serial_number}/showCommands/async-operations/{task_id}", methods=["GET"])
def get_network_troubleshooting_v1_gateways_serial_number_showcommands_async_operations_task_id(serial_number: str, task_id: str):
    """
    Aruba Central Endpoint: GET /network-troubleshooting/v1/gateways/{serial-number}/showCommands/async-operations/{task-id}
    """
    collection_path = f"/network-troubleshooting/v1/gateways/{serial_number}/showCommands/async-operations"
    item = db.get_item(collection_path, task_id)
    if item:
        return item
    static_val = db.get_static("get_network_troubleshooting_v1_gateways_serial_number_showcommands_async_operations_task_id")
    if static_val is not None:
        return static_val
    raise HTTPException(status_code=404, detail="Resource not found")

@app.api_route("/network-troubleshooting/v1/gateways/{serial_number}/reboot", methods=["POST"])
def post_network_troubleshooting_v1_gateways_serial_number_reboot(serial_number: str):
    """
    Aruba Central Endpoint: POST /network-troubleshooting/v1/gateways/{serial-number}/reboot
    """
    collection_path = f"/network-troubleshooting/v1/gateways/{serial_number}/reboot"
    payload_dict = {}
    existing = db.get_item(collection_path, serial_number) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, serial_number, existing)
    return existing

@app.api_route("/network-troubleshooting/v1/gateways/{serial_number}/disconnectClientAll", methods=["POST"])
def post_network_troubleshooting_v1_gateways_serial_number_disconnectclientall(serial_number: str):
    """
    Aruba Central Endpoint: POST /network-troubleshooting/v1/gateways/{serial-number}/disconnectClientAll
    """
    collection_path = f"/network-troubleshooting/v1/gateways/{serial_number}/disconnectClientAll"
    payload_dict = {}
    existing = db.get_item(collection_path, serial_number) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, serial_number, existing)
    return existing

@app.api_route("/network-troubleshooting/v1/gateways/{serial_number}/disconnectClientByMacAddress", methods=["POST"])
def post_network_troubleshooting_v1_gateways_serial_number_disconnectclientbymacaddress(serial_number: str, payload: Aruba_disconnectclientbymacgwv1_Request):
    """
    Aruba Central Endpoint: POST /network-troubleshooting/v1/gateways/{serial-number}/disconnectClientByMacAddress
    """
    collection_path = f"/network-troubleshooting/v1/gateways/{serial_number}/disconnectClientByMacAddress"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = db.get_item(collection_path, serial_number) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, serial_number, existing)
    return existing

@app.api_route("/network-troubleshooting/v1/gateways/{serial_number}/halt", methods=["POST"])
def post_network_troubleshooting_v1_gateways_serial_number_halt(serial_number: str):
    """
    Aruba Central Endpoint: POST /network-troubleshooting/v1/gateways/{serial-number}/halt
    """
    collection_path = f"/network-troubleshooting/v1/gateways/{serial_number}/halt"
    payload_dict = {}
    existing = db.get_item(collection_path, serial_number) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, serial_number, existing)
    return existing

@app.api_route("/network-troubleshooting/v1/gateways/{serial_number}/list-tasks", methods=["GET"])
def get_network_troubleshooting_v1_gateways_serial_number_list_tasks(serial_number: str):
    """
    Aruba Central Endpoint: GET /network-troubleshooting/v1/gateways/{serial-number}/list-tasks
    """
    collection_path = f"/network-troubleshooting/v1/gateways/{serial_number}/list-tasks"
    dynamic_items = db.get_all(collection_path)
    static_val = db.get_static("get_network_troubleshooting_v1_gateways_serial_number_list_tasks", dict())
    if not dynamic_items:
        return static_val
    if isinstance(static_val, dict):
        res = dict(static_val)
        # Determine default key based on collection_path
        default_key = "items"
        if "switches" in collection_path: default_key = "switches"
        elif "aps" in collection_path or "access-points" in collection_path: default_key = "aps"
        elif "gateways" in collection_path: default_key = "gateways"
        elif "clients" in collection_path: default_key = "clients"
        elif "users" in collection_path: default_key = "users"
        
        if default_key not in res:
            res[default_key] = []

        for key in ["items", "members", "switches", "aps", "gateways", "clients", "users"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    elif isinstance(static_val, list):
        res = list(static_val)
        existing = {item.get("id") or item.get("uuid") or item.get("name") or item.get("serial") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name") or item.get("serial")
            if iid not in existing:
                res.append(item)
        return res
    return static_val
