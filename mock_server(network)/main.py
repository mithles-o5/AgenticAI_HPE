import uuid
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
import os
from models import DeviceSchema, NetworkVlanRequest, NetworkPortStatusRequest

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
    store = db.get_collection(collection_path)
    if id not in store:
        raise HTTPException(status_code=404, detail="Device not found")
    return store[id]

@app.post("/network/v1/devices")
def create_network_device(payload: DeviceSchema):
    collection_path = "/network/v1/devices"
    
    payload_dict = payload.dict()
    item_id = payload_dict.get("id") or payload_dict.get("serial_number") or str(uuid.uuid4())
    payload_dict["id"] = item_id
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.put("/network/v1/devices/{id}")
def update_network_device(id: str, payload: DeviceSchema):
    collection_path = "/network/v1/devices"
    store = db.get_collection(collection_path)
    if id not in store:
        raise HTTPException(status_code=404, detail="Device not found")
    
    existing = store[id]
    payload_dict = {k: v for k, v in payload.dict().items() if v is not None}
    existing.update(payload_dict)
    db.upsert_item(collection_path, id, existing)
    return existing

@app.delete("/network/v1/devices/{id}")
def delete_network_device(id: str):
    collection_path = "/network/v1/devices"
    store = db.get_collection(collection_path)
    if id not in store:
        raise HTTPException(status_code=404, detail="Device not found")
    deleted = db.delete_item(collection_path, id)
    return {"message": "Deleted successfully", "id": id, "item": deleted}


@app.post("/network/v1/devices/{id}/vlans")
def post_network_device_vlans(id: str, payload: NetworkVlanRequest):
    collection_path = "/network/v1/devices"
    store = db.get_collection(collection_path)
    if id not in store:
        raise HTTPException(status_code=404, detail="Device not found")
    
    device = dict(store[id])
    configured_vlans = device.get("configured_vlans") or []
    if isinstance(configured_vlans, str):
        try:
            configured_vlans = json.loads(configured_vlans)
        except Exception:
            configured_vlans = []
            
    configured_vlans.append(payload.dict())
    device["configured_vlans"] = configured_vlans
    
    db.upsert_item(collection_path, id, device)
    return device


@app.post("/network/v1/devices/{id}/ports/{port_name}/status")
def post_network_device_port_status(id: str, port_name: str, payload: NetworkPortStatusRequest):
    collection_path = "/network/v1/devices"
    store = db.get_collection(collection_path)
    if id not in store:
        raise HTTPException(status_code=404, detail="Device not found")
    
    device = dict(store[id])
    ports = device.get("ports") or {}
    if isinstance(ports, str):
        try:
            ports = json.loads(ports)
        except Exception:
            ports = {}
            
    ports[port_name] = payload.status
    device["ports"] = ports
    
    db.upsert_item(collection_path, id, device)
    return device


@app.patch("/network/v1/devices/{id}")
def patch_network_device(id: str, payload: dict):
    collection_path = "/network/v1/devices"
    store = db.get_collection(collection_path)
    if id not in store:
        raise HTTPException(status_code=404, detail="Device not found")
    
    existing = dict(store[id])
    payload_dict = {k: v for k, v in payload.items() if v is not None}
    existing.update(payload_dict)
    db.upsert_item(collection_path, id, existing)
    return existing


from pydantic import BaseModel

class NetworkPowerRequest(BaseModel):
    action: str


@app.post("/network/v1/devices/{id}/power")
def post_network_device_power(id: str, payload: NetworkPowerRequest):
    """
    Action Route: POST /network/v1/devices/{id}/power
    """
    import datetime
    collection_path = "/network/v1/devices"
    store = db.get_collection(collection_path)
    if id not in store:
        raise HTTPException(status_code=404, detail="Device not found")
        
    action_upper = payload.action.upper()
    if action_upper not in ["ON", "OFF"]:
        raise HTTPException(status_code=400, detail="Invalid action. Only 'ON' or 'OFF' are allowed.")
        
    device = dict(store[id])
    device["power_state"] = action_upper
    device["updated_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S+05:30")
    db.upsert_item(collection_path, id, device)
    return device


