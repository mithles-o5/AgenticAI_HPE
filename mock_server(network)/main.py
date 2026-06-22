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
    collection_path = "/network/v1/devices"
    
    payload_dict = payload.dict()
    item_id = payload_dict.get("id") or payload_dict.get("serial_number") or str(uuid.uuid4())
    payload_dict["id"] = item_id
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
    payload_dict = {k: v for k, v in payload.items() if v is not None}
    device.update(payload_dict)
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
        
    configured_vlans.append(payload.dict())
    device["configured_vlans"] = configured_vlans
    device["updated_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S+05:30")
    db.upsert_item(collection_path, device["id"], device)
    return device

@app.post("/network/v1/devices/{id}/ports/{port_name}/status")
def post_network_device_port_status(id: str, port_name: str, payload: NetworkPortStatusRequest):
    """
    Action Route: POST /network/v1/devices/{id}/ports/{port_name}/status
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
        
    ports[port_name] = payload.status
    device["ports"] = ports
    device["updated_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S+05:30")
    db.upsert_item(collection_path, device["id"], device)
    return device


@app.get("/monitoring/v1/switches")
def get_aruba_switches():
    """
    Aruba Central Endpoint: GET /monitoring/v1/switches
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
        
    configured_vlans.append(payload.dict())
    device["configured_vlans"] = configured_vlans
    device["updated_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S+05:30")
    db.upsert_item(collection_path, device["id"], device)
    return {"serial": serial, "vlans": configured_vlans}


@app.post("/monitoring/v1/switches/{serial}/ports/{port_name}/status")
def post_aruba_switch_port_status(serial: str, port_name: str, payload: ArubaPortStatusRequest):
    """
    Aruba Central Endpoint: POST /monitoring/v1/switches/{serial}/ports/{port_name}/status
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
        
    ports[port_name] = payload.status
    device["ports"] = ports
    device["updated_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S+05:30")
    db.upsert_item(collection_path, device["id"], device)
    return {"serial": serial, "ports": ports}


