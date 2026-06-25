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
def update_network_device(id: str, payload: dict):
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
