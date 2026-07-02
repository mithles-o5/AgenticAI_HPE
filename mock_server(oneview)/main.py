import uuid
from fastapi import FastAPI, Query, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import json
import os
import asyncio
import threading
from fastapi.responses import JSONResponse
import logging
from models import *

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from database import db

app = FastAPI(title='Generated Mock Server', description='Generated automatically from API docs.')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/rest/custom-servers")
def get_rest_custom_servers():
    """
    Custom CRUD Route: GET /rest/custom-servers
    """
    collection_path = "/rest/custom-servers"
    return db.get_all(collection_path)

@app.get("/rest/custom-servers/{id}")
def get_rest_custom_servers_id(id: str):
    """
    Custom CRUD Route: GET /rest/custom-servers/{id}
    """
    collection_path = "/rest/custom-servers"
    store = db.get_collection(collection_path)
    if id not in store:
        raise HTTPException(status_code=404, detail="Server not found")
    return store[id]

@app.get("/rest/custom-servers/{id}/{feature}")
def get_rest_custom_servers_id_feature(id: str, feature: str):
    """
    Custom CRUD Route: Get a specific feature value of a custom server
    """
    collection_path = "/rest/custom-servers"
    store = db.get_collection(collection_path)
    if id not in store:
        raise HTTPException(status_code=404, detail="Server not found")
    
    server = store[id]
    if feature not in server:
        raise HTTPException(status_code=404, detail=f"Feature '{feature}' not found on this server")
    
    return {
        "id": id,
        "name": server.get("name"),
        "feature": feature,
        "value": server.get(feature)
    }



@app.post("/rest/custom-servers")
def post_rest_custom_servers(payload: CustomServerCreateRequest):
    """
    Custom CRUD Route: POST /rest/custom-servers
    """
    collection_path = "/rest/custom-servers"
    
    item_id = str(uuid.uuid4())
    item_data = payload.dict()
    item_data["id"] = item_id
    db.upsert_item(collection_path, item_id, item_data)
    return item_data

@app.put("/rest/custom-servers/{id}")
def put_rest_custom_servers_id(id: str, payload: CustomServerUpdateRequest):
    """
    Custom CRUD Route: PUT /rest/custom-servers/{id}
    """
    collection_path = "/rest/custom-servers"
    store = db.get_collection(collection_path)
    if id not in store:
        raise HTTPException(status_code=404, detail="Server not found")
    
    existing = store[id]
    payload_dict = {k: v for k, v in payload.dict().items() if v is not None}
    existing.update(payload_dict)
    db.upsert_item(collection_path, existing["id"], existing)
    return existing

@app.delete("/rest/custom-servers/{id}")
def delete_rest_custom_servers_id(id: str):
    """
    Custom CRUD Route: DELETE /rest/custom-servers/{id}
    """
    collection_path = "/rest/custom-servers"
    store = db.get_collection(collection_path)
    if id not in store:
        raise HTTPException(status_code=404, detail="Server not found")
    deleted = db.delete_item(collection_path, id)
    return {"message": "Deleted successfully", "id": id, "item": deleted}


@app.get("/rest/custom-switches")
def get_rest_custom_switches():
    """
    Custom CRUD Route: GET /rest/custom-switches
    """
    collection_path = "/rest/custom-switches"
    return db.get_all(collection_path)

@app.get("/rest/custom-switches/{id}")
def get_rest_custom_switches_id(id: str):
    """
    Custom CRUD Route: GET /rest/custom-switches/{id}
    """
    collection_path = "/rest/custom-switches"
    store = db.get_collection(collection_path)
    if id not in store:
        raise HTTPException(status_code=404, detail="Switch not found")
    return store[id]

@app.get("/rest/custom-switches/{id}/{feature}")
def get_rest_custom_switches_id_feature(id: str, feature: str):
    """
    Custom CRUD Route: Get a specific feature value of a custom switch
    """
    collection_path = "/rest/custom-switches"
    store = db.get_collection(collection_path)
    if id not in store:
        raise HTTPException(status_code=404, detail="Switch not found")
    
    switch = store[id]
    if feature not in switch:
        raise HTTPException(status_code=404, detail=f"Feature '{feature}' not found on this switch")
    
    return {
        "id": id,
        "name": switch.get("name"),
        "feature": feature,
        "value": switch.get(feature)
    }

@app.post("/rest/custom-switches")
def post_rest_custom_switches(payload: CustomSwitchCreateRequest):
    """
    Custom CRUD Route: POST /rest/custom-switches
    """
    collection_path = "/rest/custom-switches"
    
    item_id = str(uuid.uuid4())
    item_data = payload.dict()
    item_data["id"] = item_id
    db.upsert_item(collection_path, item_id, item_data)
    return item_data

@app.put("/rest/custom-switches/{id}")
def put_rest_custom_switches_id(id: str, payload: CustomSwitchUpdateRequest):
    """
    Custom CRUD Route: PUT /rest/custom-switches/{id}
    """
    collection_path = "/rest/custom-switches"
    store = db.get_collection(collection_path)
    if id not in store:
        raise HTTPException(status_code=404, detail="Switch not found")
    
    existing = store[id]
    payload_dict = {k: v for k, v in payload.dict().items() if v is not None}
    existing.update(payload_dict)
    db.upsert_item(collection_path, existing["id"], existing)
    return existing

@app.delete("/rest/custom-switches/{id}")
def delete_rest_custom_switches_id(id: str):
    """
    Custom CRUD Route: DELETE /rest/custom-switches/{id}
    """
    collection_path = "/rest/custom-switches"
    store = db.get_collection(collection_path)
    if id not in store:
        raise HTTPException(status_code=404, detail="Switch not found")
    deleted = db.delete_item(collection_path, id)
    return {"message": "Deleted successfully", "id": id, "item": deleted}


@app.post("/rest/login-sessions")
def post_rest_login_sessions(payload: PostRestLoginSessionsRequest):

    """
    Dynamic CRUD Route: POST /rest/login-sessions
    """
    collection_path = f"/rest/login-sessions"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.post("/rest/login-sessions/auth-token")
def post_rest_login_sessions_auth_token(payload: PostRestLoginSessionsAuthTokenRequest):
    """
    Dynamic CRUD Route: POST /rest/login-sessions/auth-token
    """
    collection_path = f"/rest/login-sessions/auth-token"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.post("/rest/certificates/client/rabbitmq")
def post_rest_certificates_client_rabbitmq(payload: PostRestCertificatesClientRabbitmqRequest):
    """
    Dynamic CRUD Route: POST /rest/certificates/client/rabbitmq
    """
    collection_path = f"/rest/certificates/client/rabbitmq"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.get("/rest/certificates/client/rabbitmq/keypair/default")
def get_rest_certificates_client_rabbitmq_keypair_default():
    """
    Dynamic CRUD Route: GET /rest/certificates/client/rabbitmq/keypair/default
    """
    collection_path = f"/rest/certificates/client/rabbitmq/keypair/default"
    static_data = db.get_static("get_rest_certificates_client_rabbitmq_keypair_default", dict())
    dynamic_items = db.get_all(collection_path)
    if not dynamic_items:
        return static_data
    if isinstance(static_data, list):
        res = list(static_data)
        existing = {item.get("id") or item.get("uuid") or item.get("name") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name")
            if iid not in existing:
                res.append(item)
        return res
    elif isinstance(static_data, dict):
        res = dict(static_data)
        for key in ["items", "members"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    return static_data

@app.get("/rest/certificates/ca")
def get_rest_certificates_ca():
    """
    Dynamic CRUD Route: GET /rest/certificates/ca
    """
    collection_path = f"/rest/certificates/ca"
    static_data = db.get_static("get_rest_certificates_ca", dict())
    dynamic_items = db.get_all(collection_path)
    if not dynamic_items:
        return static_data
    if isinstance(static_data, list):
        res = list(static_data)
        existing = {item.get("id") or item.get("uuid") or item.get("name") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name")
            if iid not in existing:
                res.append(item)
        return res
    elif isinstance(static_data, dict):
        res = dict(static_data)
        for key in ["items", "members"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    return static_data

@app.delete("/rest/certificates/ca/rabbitmq_readonly")
def delete_rest_certificates_ca_rabbitmq_readonly():
    """
    Dynamic CRUD Route: DELETE /rest/certificates/ca/rabbitmq_readonly
    """
    return db.get_static("delete_rest_certificates_ca_rabbitmq_readonly", dict())

@app.get("/rest/server-hardware/{id}/chassis")
def get_rest_server_hardware_id_chassis(id: str):
    """
    Dynamic CRUD Route: GET /rest/server-hardware/{id}/chassis
    """
    collection_path = f"/rest/server-hardware/{id}/chassis"
    static_data = db.get_static("get_rest_server_hardware_id_chassis", dict())
    dynamic_items = db.get_all(collection_path)
    if not dynamic_items:
        return static_data
    if isinstance(static_data, list):
        res = list(static_data)
        existing = {item.get("id") or item.get("uuid") or item.get("name") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name")
            if iid not in existing:
                res.append(item)
        return res
    elif isinstance(static_data, dict):
        res = dict(static_data)
        for key in ["items", "members"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    return static_data

@app.get("/rest/server-hardware/{id}/firmwareInventory")
def get_rest_server_hardware_id_firmwareinventory(id: str):
    """
    Dynamic CRUD Route: GET /rest/server-hardware/{id}/firmwareInventory
    """
    collection_path = f"/rest/server-hardware/{id}/firmwareInventory"
    static_data = db.get_static("get_rest_server_hardware_id_firmwareinventory", dict())
    dynamic_items = db.get_all(collection_path)
    if not dynamic_items:
        return static_data
    if isinstance(static_data, list):
        res = list(static_data)
        existing = {item.get("id") or item.get("uuid") or item.get("name") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name")
            if iid not in existing:
                res.append(item)
        return res
    elif isinstance(static_data, dict):
        res = dict(static_data)
        for key in ["items", "members"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    return static_data

@app.get("/rest/server-hardware/{id}/networkAdapters")
def get_rest_server_hardware_id_networkadapters(id: str):
    """
    Dynamic CRUD Route: GET /rest/server-hardware/{id}/networkAdapters
    """
    collection_path = f"/rest/server-hardware/{id}/networkAdapters"
    static_data = db.get_static("get_rest_server_hardware_id_networkadapters", dict())
    dynamic_items = db.get_all(collection_path)
    if not dynamic_items:
        return static_data
    if isinstance(static_data, list):
        res = list(static_data)
        existing = {item.get("id") or item.get("uuid") or item.get("name") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name")
            if iid not in existing:
                res.append(item)
        return res
    elif isinstance(static_data, dict):
        res = dict(static_data)
        for key in ["items", "members"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    return static_data

@app.get("/rest/server-hardware/{id}/powerSupplies")
def get_rest_server_hardware_id_powersupplies(id: str):
    """
    Dynamic CRUD Route: GET /rest/server-hardware/{id}/powerSupplies
    """
    collection_path = f"/rest/server-hardware/{id}/powerSupplies"
    static_data = db.get_static("get_rest_server_hardware_id_powersupplies", dict())
    dynamic_items = db.get_all(collection_path)
    if not dynamic_items:
        return static_data
    if isinstance(static_data, list):
        res = list(static_data)
        existing = {item.get("id") or item.get("uuid") or item.get("name") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name")
            if iid not in existing:
                res.append(item)
        return res
    elif isinstance(static_data, dict):
        res = dict(static_data)
        for key in ["items", "members"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    return static_data

@app.get("/rest/server-hardware/{id}/processors")
def get_rest_server_hardware_id_processors(id: str):
    """
    Dynamic CRUD Route: GET /rest/server-hardware/{id}/processors
    """
    collection_path = f"/rest/server-hardware/{id}/processors"
    static_data = db.get_static("get_rest_server_hardware_id_processors", dict())
    dynamic_items = db.get_all(collection_path)
    if not dynamic_items:
        return static_data
    if isinstance(static_data, list):
        res = list(static_data)
        existing = {item.get("id") or item.get("uuid") or item.get("name") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name")
            if iid not in existing:
                res.append(item)
        return res
    elif isinstance(static_data, dict):
        res = dict(static_data)
        for key in ["items", "members"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    return static_data

@app.get("/rest/server-hardware/{id}/softwareInventory")
def get_rest_server_hardware_id_softwareinventory(id: str):
    """
    Dynamic CRUD Route: GET /rest/server-hardware/{id}/softwareInventory
    """
    collection_path = f"/rest/server-hardware/{id}/softwareInventory"
    static_data = db.get_static("get_rest_server_hardware_id_softwareinventory", dict())
    dynamic_items = db.get_all(collection_path)
    if not dynamic_items:
        return static_data
    if isinstance(static_data, list):
        res = list(static_data)
        existing = {item.get("id") or item.get("uuid") or item.get("name") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name")
            if iid not in existing:
                res.append(item)
        return res
    elif isinstance(static_data, dict):
        res = dict(static_data)
        for key in ["items", "members"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    return static_data

@app.get("/rest/server-hardware/{id}/thermal")
def get_rest_server_hardware_id_thermal(id: str):
    """
    Dynamic CRUD Route: GET /rest/server-hardware/{id}/thermal
    Returns temperature data.
    - Device ON  : reads stored temperature from DB (set at power-on time).
    - Device OFF : always returns 0.0 — no ambient guessing.
    """
    server = db.get_item("/rest/server-hardware", id)
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")

    power_state = (server.get("power_state") or "Off")
    is_on = str(power_state).upper().startswith("ON") or "POWERON" in str(power_state).upper()

    if is_on:
        import random
        stored_temp = server.get("temperature_celsius")
        temperature_celsius = (
            float(stored_temp) if stored_temp is not None and float(stored_temp) > 0
            else round(random.uniform(30.0, 55.0), 1)
        )
    else:
        # Device is OFF — all thermal metrics are 0
        temperature_celsius = 0.0

    return {
        "id": id,
        "temperature_celsius": temperature_celsius
    }

@app.get("/rest/server-hardware/{id}/utilization")
def get_rest_server_hardware_id_utilization(id: str):
    """
    Dynamic CRUD Route: GET /rest/server-hardware/{id}/utilization
    Returns live utilization — reads stored values from DB, generates random if missing for ON devices.
    """
    server = db.get_item("/rest/server-hardware", id)
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")

    power_state = (server.get("power_state") or server.get("powerState") or "Off")
    is_on = str(power_state).upper().startswith("ON") or "POWERON" in str(power_state).upper()

    import random
    if is_on:
        # Prefer stored values; if they're 0 or missing, generate fresh random and persist
        cpu = server.get("cpu_utilization_percent")
        mem = server.get("memory_utilization_percent")
        power = server.get("power_draw_watts")

        # If stored metrics are zero/None (device just turned on but metrics not yet set), randomize
        cpu   = float(cpu)   if cpu   is not None and float(cpu)   > 0 else round(random.uniform(10.0, 90.0), 1)
        mem   = float(mem)   if mem   is not None and float(mem)   > 0 else round(random.uniform(10.0, 90.0), 1)
        power = float(power) if power is not None and float(power) > 0 else round(random.uniform(150.0, 400.0), 1)

        # Drift stored values slightly each poll for realism (+/- 5%)
        cpu   = max(1.0, min(99.0, round(cpu   + random.uniform(-5.0, 5.0), 1)))
        mem   = max(1.0, min(99.0, round(mem   + random.uniform(-3.0, 3.0), 1)))
        power = max(50.0, min(500.0, round(power + random.uniform(-15.0, 15.0), 1)))

        # Persist the drifted values back to DB so the base GET is always consistent
        updated = dict(server)
        updated["cpu_utilization_percent"]    = cpu
        updated["memory_utilization_percent"] = mem
        updated["power_draw_watts"]           = power
        db.upsert_item("/rest/server-hardware", updated["id"], updated)
    else:
        cpu   = 0.0
        mem   = 0.0
        power = 0.0

    return {
        "id": id,
        "cpu_utilization_percent":    cpu,
        "memory_utilization_percent": mem,
        "power_draw_watts":           power
    }

@app.get("/rest/rack-managers/{id}/chassis/utilization")
def get_rest_rack_managers_id_chassis_utilization(id: str):
    """
    Dynamic CRUD Route: GET /rest/rack-managers/{id}/chassis/utilization
    """
    rack = db.get_item("/rest/rack-managers", id)
    if not rack:
        raise HTTPException(status_code=404, detail="Rack manager not found")
        
    power_state = rack.get("powerState") or rack.get("power_state") or "On"
    import random
    if str(power_state).upper().startswith("ON") or "POWERON" in str(power_state).upper():
        power = round(random.uniform(1000.0, 3000.0), 1)
        temp = round(random.uniform(25.0, 35.0), 1)
    else:
        power = 0.0
        temp = round(random.uniform(20.0, 25.0), 1)
        
    return {
        "id": id,
        "power_draw_watts": power,
        "temperature_celsius": temp
    }

@app.get("/rest/rack-managers/{id}/chassis/{uuid}")
def get_rest_rack_managers_id_chassis_uuid(id: str, uuid: str):
    """
    Dynamic CRUD Route: GET /rest/rack-managers/{id}/chassis/{uuid}
    """
    collection_path = f"/rest/rack-managers/{id}/chassis"
    item_id = uuid
    item = db.get_item(collection_path, item_id)
    if item:
        return item
    static_val = db.get_static("get_rest_rack_managers_id_chassis_uuid", dict())
    return static_val

@app.post("/rest/ethernet-networks/bulk")
def post_rest_ethernet_networks_bulk(payload: PostRestEthernetNetworksBulkRequest):
    """
    Dynamic CRUD Route: POST /rest/ethernet-networks/bulk
    Returns 202 Accepted.
    """
    collection_path = f"/rest/ethernet-networks/bulk"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
        
    payload_dict["status"] = "Creating"
    db.upsert_item(collection_path, item_id, payload_dict)
    
    t = threading.Thread(
        target=_apply_async_crud,
        args=(collection_path, item_id, payload_dict, 8, "POST"),
        daemon=True
    )
    t.start()
    return JSONResponse(status_code=202, content=payload_dict)

@app.put("/rest/storage-volumes/{id}")
def put_rest_storage_volumes_id(id: str, payload: PutRestStorageVolumesIdRequest):
    """
    Dynamic CRUD Route: PUT /rest/storage-volumes/{id}
    Returns 202 Accepted.
    """
    collection_path = f"/rest/storage-volumes"
    item_id = id
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    
    existing = db.get_item(collection_path, item_id) or {"id": item_id}
    existing["status"] = "Updating"
    db.upsert_item(collection_path, item_id, existing)
    
    t = threading.Thread(
        target=_apply_async_crud,
        args=(collection_path, item_id, payload_dict, 5, "PUT"),
        daemon=True
    )
    t.start()
    return JSONResponse(status_code=202, content=existing)

@app.get("/rest/updates")
def get_rest_updates():
    """
    Dynamic CRUD Route: GET /rest/updates
    """
    collection_path = f"/rest/updates"
    static_data = db.get_static("get_rest_updates", dict())
    dynamic_items = db.get_all(collection_path)
    if not dynamic_items:
        return static_data
    if isinstance(static_data, list):
        res = list(static_data)
        existing = {item.get("id") or item.get("uuid") or item.get("name") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name")
            if iid not in existing:
                res.append(item)
        return res
    elif isinstance(static_data, dict):
        res = dict(static_data)
        for key in ["items", "members"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    return static_data

@app.get("/rest/updates/{id}")
def get_rest_updates_id(id: str):
    """
    Dynamic CRUD Route: GET /rest/updates/{id}
    """
    collection_path = f"/rest/updates"
    item_id = id
    item = db.get_item(collection_path, item_id)
    if item:
        return item
    static_val = db.get_static("get_rest_updates_id", dict())
    return static_val

@app.get("/rest/rack-managers")
def get_rest_rack_managers():
    """
    Dynamic CRUD Route: GET /rest/rack-managers
    """
    collection_path = f"/rest/rack-managers"
    static_data = db.get_static("get_rest_rack_managers", dict())
    dynamic_items = db.get_all(collection_path)
    if not dynamic_items:
        return static_data
    if isinstance(static_data, list):
        res = list(static_data)
        existing = {item.get("id") or item.get("uuid") or item.get("name") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name")
            if iid not in existing:
                res.append(item)
        return res
    elif isinstance(static_data, dict):
        res = dict(static_data)
        for key in ["items", "members"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    return static_data

@app.post("/rest/rack-managers")
def post_rest_rack_managers(payload: PostRestRackManagersRequest):
    """
    Dynamic CRUD Route: POST /rest/rack-managers
    Returns 202 Accepted.
    """
    collection_path = f"/rest/rack-managers"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
        
    payload_dict["status"] = "Adding"
    db.upsert_item(collection_path, item_id, payload_dict)
    
    t = threading.Thread(
        target=_apply_async_crud,
        args=(collection_path, item_id, payload_dict, 10, "POST"),
        daemon=True
    )
    t.start()
    return JSONResponse(status_code=202, content=payload_dict)

@app.get("/rest/rack-managers/chassis")
def get_rest_rack_managers_chassis():
    """
    Dynamic CRUD Route: GET /rest/rack-managers/chassis
    """
    collection_path = f"/rest/rack-managers/chassis"
    static_data = db.get_static("get_rest_rack_managers_chassis", dict())
    dynamic_items = db.get_all(collection_path)
    if not dynamic_items:
        return static_data
    if isinstance(static_data, list):
        res = list(static_data)
        existing = {item.get("id") or item.get("uuid") or item.get("name") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name")
            if iid not in existing:
                res.append(item)
        return res
    elif isinstance(static_data, dict):
        res = dict(static_data)
        for key in ["items", "members"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    return static_data

@app.get("/rest/rack-managers/managers")
def get_rest_rack_managers_managers():
    """
    Dynamic CRUD Route: GET /rest/rack-managers/managers
    """
    collection_path = f"/rest/rack-managers/managers"
    static_data = db.get_static("get_rest_rack_managers_managers", dict())
    dynamic_items = db.get_all(collection_path)
    if not dynamic_items:
        return static_data
    if isinstance(static_data, list):
        res = list(static_data)
        existing = {item.get("id") or item.get("uuid") or item.get("name") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name")
            if iid not in existing:
                res.append(item)
        return res
    elif isinstance(static_data, dict):
        res = dict(static_data)
        for key in ["items", "members"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    return static_data

@app.get("/rest/rack-managers/partitions")
def get_rest_rack_managers_partitions():
    """
    Dynamic CRUD Route: GET /rest/rack-managers/partitions
    """
    collection_path = f"/rest/rack-managers/partitions"
    static_data = db.get_static("get_rest_rack_managers_partitions", dict())
    dynamic_items = db.get_all(collection_path)
    if not dynamic_items:
        return static_data
    if isinstance(static_data, list):
        res = list(static_data)
        existing = {item.get("id") or item.get("uuid") or item.get("name") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name")
            if iid not in existing:
                res.append(item)
        return res
    elif isinstance(static_data, dict):
        res = dict(static_data)
        for key in ["items", "members"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    return static_data

@app.get("/rest/rack-managers/{id}")
def get_rest_rack_managers_id(id: str):
    """
    Dynamic CRUD Route: GET /rest/rack-managers/{id}
    """
    collection_path = f"/rest/rack-managers"
    item = db.get_item(collection_path, id)
    if item:
        return item
    raise HTTPException(status_code=404, detail="Rack manager not found")

@app.patch("/rest/rack-managers/{id}")
def patch_rest_rack_managers_id(id: str):
    """
    Dynamic CRUD Route: PATCH /rest/rack-managers/{id}
    Returns 202 Accepted.
    """
    collection_path = f"/rest/rack-managers"
    item_id = id
    payload_dict = {}
    existing = db.get_item(collection_path, item_id) or {"id": item_id}
    
    existing["status"] = "Updating"
    db.upsert_item(collection_path, item_id, existing)
    
    t = threading.Thread(
        target=_apply_async_crud,
        args=(collection_path, item_id, payload_dict, 5, "PATCH"),
        daemon=True
    )
    t.start()
    return JSONResponse(status_code=202, content=existing)

@app.delete("/rest/rack-managers/{id}")
def delete_rest_rack_managers_id(id: str):
    """
    Dynamic CRUD Route: DELETE /rest/rack-managers/{id}
    Returns 202 Accepted.
    """
    collection_path = f"/rest/rack-managers"
    item_id = id
    item = db.get_item(collection_path, item_id)
    if item:
        item = dict(item)
        item["status"] = "Removing"
        db.upsert_item(collection_path, item_id, item)
        
        t = threading.Thread(
            target=_apply_async_crud,
            args=(collection_path, item_id, {}, 10, "DELETE"),
            daemon=True
        )
        t.start()
        return JSONResponse(status_code=202, content={"message": "Deletion accepted", "id": item_id, "item": item})
    return db.get_static("delete_rest_rack_managers_id", dict())

@app.get("/rest/rack-managers/{id}/chassis")
def get_rest_rack_managers_id_chassis(id: str):
    """
    Dynamic CRUD Route: GET /rest/rack-managers/{id}/chassis
    """
    collection_path = f"/rest/rack-managers/{id}/chassis"
    static_data = db.get_static("get_rest_rack_managers_id_chassis", dict())
    dynamic_items = db.get_all(collection_path)
    if not dynamic_items:
        return static_data
    if isinstance(static_data, list):
        res = list(static_data)
        existing = {item.get("id") or item.get("uuid") or item.get("name") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name")
            if iid not in existing:
                res.append(item)
        return res
    elif isinstance(static_data, dict):
        res = dict(static_data)
        for key in ["items", "members"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    return static_data


@app.get("/rest/rack-managers/{id}/environmentalConfiguration")
def get_rest_rack_managers_id_environmentalconfiguration(id: str):
    """
    Dynamic CRUD Route: GET /rest/rack-managers/{id}/environmentalConfiguration
    """
    collection_path = f"/rest/rack-managers/{id}/environmentalConfiguration"
    static_data = db.get_static("get_rest_rack_managers_id_environmentalconfiguration", dict())
    dynamic_items = db.get_all(collection_path)
    if not dynamic_items:
        return static_data
    if isinstance(static_data, list):
        res = list(static_data)
        existing = {item.get("id") or item.get("uuid") or item.get("name") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name")
            if iid not in existing:
                res.append(item)
        return res
    elif isinstance(static_data, dict):
        res = dict(static_data)
        for key in ["items", "members"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    return static_data

@app.get("/rest/rack-managers/{id}/managers")
def get_rest_rack_managers_id_managers(id: str):
    """
    Dynamic CRUD Route: GET /rest/rack-managers/{id}/managers
    """
    collection_path = f"/rest/rack-managers/{id}/managers"
    static_data = db.get_static("get_rest_rack_managers_id_managers", dict())
    dynamic_items = db.get_all(collection_path)
    if not dynamic_items:
        return static_data
    if isinstance(static_data, list):
        res = list(static_data)
        existing = {item.get("id") or item.get("uuid") or item.get("name") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name")
            if iid not in existing:
                res.append(item)
        return res
    elif isinstance(static_data, dict):
        res = dict(static_data)
        for key in ["items", "members"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    return static_data

@app.get("/rest/rack-managers/{id}/managers/{managerid}")
def get_rest_rack_managers_id_managers_managerid(id: str, managerid: str):
    """
    Dynamic CRUD Route: GET /rest/rack-managers/{id}/managers/{managerid}
    """
    collection_path = f"/rest/rack-managers/{id}/managers"
    item_id = managerid
    item = db.get_item(collection_path, item_id)
    if item:
        return item
    static_val = db.get_static("get_rest_rack_managers_id_managers_managerid", dict())
    return static_val

@app.get("/rest/rack-managers/{id}/partitions")
def get_rest_rack_managers_id_partitions(id: str):
    """
    Dynamic CRUD Route: GET /rest/rack-managers/{id}/partitions
    """
    collection_path = f"/rest/rack-managers/{id}/partitions"
    static_data = db.get_static("get_rest_rack_managers_id_partitions", dict())
    dynamic_items = db.get_all(collection_path)
    if not dynamic_items:
        return static_data
    if isinstance(static_data, list):
        res = list(static_data)
        existing = {item.get("id") or item.get("uuid") or item.get("name") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name")
            if iid not in existing:
                res.append(item)
        return res
    elif isinstance(static_data, dict):
        res = dict(static_data)
        for key in ["items", "members"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    return static_data

@app.get("/rest/rack-managers/{id}/partitions/{uuid}")
def get_rest_rack_managers_id_partitions_uuid(id: str, uuid: str):
    """
    Dynamic CRUD Route: GET /rest/rack-managers/{id}/partitions/{uuid}
    """
    collection_path = f"/rest/rack-managers/{id}/partitions"
    item_id = uuid
    item = db.get_item(collection_path, item_id)
    if item:
        return item
    static_val = db.get_static("get_rest_rack_managers_id_partitions_uuid", dict())
    return static_val

@app.get("/rest/rack-managers/{id}/remoteSupportSettings")
def get_rest_rack_managers_id_remotesupportsettings(id: str):
    """
    Dynamic CRUD Route: GET /rest/rack-managers/{id}/remoteSupportSettings
    """
    collection_path = f"/rest/rack-managers/{id}/remoteSupportSettings"
    static_data = db.get_static("get_rest_rack_managers_id_remotesupportsettings", dict())
    dynamic_items = db.get_all(collection_path)
    if not dynamic_items:
        return static_data
    if isinstance(static_data, list):
        res = list(static_data)
        existing = {item.get("id") or item.get("uuid") or item.get("name") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name")
            if iid not in existing:
                res.append(item)
        return res
    elif isinstance(static_data, dict):
        res = dict(static_data)
        for key in ["items", "members"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    return static_data

@app.get("/rest/server-hardware")
def get_rest_server_hardware(skip: int = 0, limit: int = 100):
    """
    Dynamic CRUD Route: GET /rest/server-hardware
    """
    collection_path = f"/rest/server-hardware"
    static_data = db.get_static("get_rest_server_hardware", dict())
    dynamic_items = db.get_all(collection_path, 0, 999999)
    if not dynamic_items:
        if isinstance(static_data, list):
            return static_data[skip : skip + limit]
        elif isinstance(static_data, dict):
            res = dict(static_data)
            for key in ["items", "members", "devices"]:
                if key in res and isinstance(res[key], list):
                    res["total"] = len(res[key])
                    res[key] = res[key][skip : skip + limit]
                    break
            return res
        return static_data
    if isinstance(static_data, list):
        res = list(static_data)
        existing = {item.get("id") or item.get("uuid") or item.get("name") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name")
            if iid not in existing:
                res.append(item)
        return res[skip : skip + limit]
    elif isinstance(static_data, dict):
        res = dict(static_data)
        for key in ["items", "members", "devices"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name")
                    if iid not in existing:
                        res[key].append(item)
                res["total"] = len(res[key])
                res[key] = res[key][skip : skip + limit]
                break
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    return static_data

@app.post("/rest/server-hardware")
def post_rest_server_hardware(payload: PostRestServerHardwareRequest):
    """
    Dynamic CRUD Route: POST /rest/server-hardware
    Returns 202 Accepted and adds the server in the background.
    """
    collection_path = f"/rest/server-hardware"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
        
    payload_dict["status"] = "Adding"
    db.upsert_item(collection_path, item_id, payload_dict)
    
    t = threading.Thread(
        target=_apply_async_crud,
        args=(collection_path, item_id, payload_dict, 8, "POST"),
        daemon=True
    )
    t.start()
    return JSONResponse(status_code=202, content=payload_dict)

@app.get("/rest/server-hardware/*/firmware")
def get_rest_server_hardware_firmware():
    """
    Dynamic CRUD Route: GET /rest/server-hardware/*/firmware
    """
    collection_path = f"/rest/server-hardware/*/firmware"
    static_data = db.get_static("get_rest_server_hardware_firmware", dict())
    dynamic_items = db.get_all(collection_path)
    if not dynamic_items:
        return static_data
    if isinstance(static_data, list):
        res = list(static_data)
        existing = {item.get("id") or item.get("uuid") or item.get("name") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name")
            if iid not in existing:
                res.append(item)
        return res
    elif isinstance(static_data, dict):
        res = dict(static_data)
        for key in ["items", "members"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    return static_data

@app.post("/rest/server-hardware/discovery")
def post_rest_server_hardware_discovery(payload: PostRestServerHardwareDiscoveryRequest):
    """
    Dynamic CRUD Route: POST /rest/server-hardware/discovery
    Returns 202 Accepted and simulates discovery latency.
    """
    collection_path = f"/rest/server-hardware/discovery"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
        
    payload_dict["status"] = "Discovering"
    db.upsert_item(collection_path, item_id, payload_dict)
    
    t = threading.Thread(
        target=_apply_async_crud,
        args=(collection_path, item_id, payload_dict, 5, "POST"),
        daemon=True
    )
    t.start()
    return JSONResponse(status_code=202, content=payload_dict)

@app.post("/rest/server-hardware/firmware-compliance")
def post_rest_server_hardware_firmware_compliance(payload: PostRestServerHardwareFirmwareComplianceRequest):
    """
    Dynamic CRUD Route: POST /rest/server-hardware/firmware-compliance
    Returns 202 Accepted and performs a long flashing process.
    """
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    server_id = payload_dict.get("serverUUID")
    baseline = payload_dict.get("firmwareBaselineId")
    
    if not server_id or not baseline:
        raise HTTPException(status_code=400, detail="serverUUID and firmwareBaselineId are required")
        
    server = db.get_item("/rest/server-hardware", server_id)
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")
        
    server["status"] = "Flashing"
    import datetime
    server["updated_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S+05:30")
    db.upsert_item("/rest/server-hardware", server_id, server)
    
    # We pass the final desired payload to the async helper
    t = threading.Thread(
        target=_apply_async_crud,
        args=("/rest/server-hardware", server_id, {"firmware_version": baseline}, 12, "PUT"),
        daemon=True
    )
    t.start()
    
    return JSONResponse(status_code=202, content={
        "status": "Flashing",
        "message": f"Server {server_id} firmware update to {baseline} started. Will complete in ~12s.",
        "serverUUID": server_id,
        "firmwareBaselineId": baseline
    })

@app.get("/rest/server-hardware/schema")
def get_rest_server_hardware_schema():
    """
    Dynamic CRUD Route: GET /rest/server-hardware/schema
    """
    collection_path = f"/rest/server-hardware/schema"
    static_data = db.get_static("get_rest_server_hardware_schema", dict())
    dynamic_items = db.get_all(collection_path)
    if not dynamic_items:
        return static_data
    if isinstance(static_data, list):
        res = list(static_data)
        existing = {item.get("id") or item.get("uuid") or item.get("name") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name")
            if iid not in existing:
                res.append(item)
        return res
    elif isinstance(static_data, dict):
        res = dict(static_data)
        for key in ["items", "members"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    return static_data

@app.get("/rest/server-hardware/{id}")
def get_rest_server_hardware_id(id: str):
    """
    Dynamic CRUD Route: GET /rest/server-hardware/{id}
    """
    collection_path = f"/rest/server-hardware"
    item = db.get_item(collection_path, id)
    if item:
        if item.get("status") == "Removing":
            item["power_state"] = "Removing"
            item["powerState"] = "Removing"
        return item
    raise HTTPException(status_code=404, detail="Server hardware not found")


@app.put("/rest/server-hardware/{id}")
def put_rest_server_hardware_id(id: str, payload: dict):
    """
    Dynamic CRUD Route: PUT /rest/server-hardware/{id}
    Returns 202 Accepted.
    """
    collection_path = f"/rest/server-hardware"
    existing = db.get_item(collection_path, id)

    if not existing:
        raise HTTPException(status_code=404, detail="Resource not found")

    existing = dict(existing)
    existing["status"] = "Updating"
    db.upsert_item(collection_path, id, existing)
    
    payload_dict = {k: v for k, v in payload.items() if v is not None}
    
    t = threading.Thread(
        target=_apply_async_crud,
        args=(collection_path, id, payload_dict, 5, "PUT"),
        daemon=True
    )
    t.start()
    return JSONResponse(status_code=202, content=existing)


@app.delete("/rest/server-hardware/{id}")
def delete_rest_server_hardware_id(id: str):
    """
    Dynamic CRUD Route: DELETE /rest/server-hardware/{id}
    Returns 202 Accepted.
    """
    collection_path = f"/rest/server-hardware"
    item = db.get_item(collection_path, id)
    if item:
        item = dict(item)
        item["status"] = "Removing"
        db.upsert_item(collection_path, id, item)
        
        t = threading.Thread(
            target=_apply_async_crud,
            args=(collection_path, id, {}, 8, "DELETE"),
            daemon=True
        )
        t.start()
        return JSONResponse(status_code=202, content={"message": "Deletion accepted", "id": id, "item": item})
    return db.get_static("delete_rest_server_hardware_id", dict())
# ---------------------------------------------------------------------------
# Power operation delay — simulates real hardware boot/shutdown latency.
# POWER_OP_DELAY_SECONDS: how long the device stays in TRANSITIONING state.
# ---------------------------------------------------------------------------
POWER_OP_DELAY_SECONDS = 8   # realistic boot/shutdown delay


class OneViewPowerRequest(BaseModel):
    powerState: str = None   # camelCase (OneView API standard)
    powerControl: str = None
    action: str = None
    power_state: str = None  # snake_case alternative


def _apply_async_crud(
    collection_path: str,
    item_id: str,
    payload: dict,
    delay: float,
    action: str
):
    import time, datetime
    time.sleep(delay)
    
    if action == "DELETE":
        db.delete_item(collection_path, item_id)
        logging.getLogger(__name__).info(f"[AsyncCrud] Deleted {item_id} from {collection_path} after {delay}s.")
        return

    current = db.get_item(collection_path, item_id)
    if not current:
        current = {"id": item_id}
    else:
        current = dict(current)
        
    current.update(payload)
    current["status"] = "OK"
    current["updated_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S+05:30")
    
    db.upsert_item(collection_path, item_id, current)
    logging.getLogger(__name__).info(f"[AsyncCrud] Upserted {item_id} in {collection_path} after {delay}s.")

    # Automatically populate dummy sub-resources so health checks return proper data rather than generic unknown static_data
    if action == "POST":
        import uuid
        if collection_path == "/rest/rack-managers":
            db.upsert_item(f"{collection_path}/{item_id}/chassis", str(uuid.uuid4()), {"status": "OK"})
            db.upsert_item(f"{collection_path}/{item_id}/environmentalConfiguration", str(uuid.uuid4()), {"status": "OK"})
            db.upsert_item(f"{collection_path}/{item_id}/managers", str(uuid.uuid4()), {"status": "OK"})
            db.upsert_item(f"{collection_path}/{item_id}/partitions", str(uuid.uuid4()), {"status": "OK"})
        elif collection_path == "/rest/server-hardware":
            db.upsert_item(f"{collection_path}/{item_id}/utilization", str(uuid.uuid4()), {"status": "OK"})
            db.upsert_item(f"{collection_path}/{item_id}/thermal", str(uuid.uuid4()), {"status": "OK"})


def _apply_power_state_after_delay(
    collection_path: str,
    device_id: str,
    target_state: str,
    delay: float
):
    """Background thread: waits `delay` seconds then commits the final power state to the DB."""
    import time, random, datetime
    time.sleep(delay)

    current = db.get_item(collection_path, device_id)
    if not current:
        return
    device = dict(current)

    if target_state == "ON":
        device["power_state"]                = "ON"
        device["cpu_utilization_percent"]    = round(random.uniform(10.0, 90.0), 1)
        device["memory_utilization_percent"] = round(random.uniform(10.0, 90.0), 1)
        device["power_draw_watts"]           = round(random.uniform(150.0, 400.0), 1)
        device["temperature_celsius"]        = round(random.uniform(30.0, 50.0), 1)
    else:  # OFF
        device["power_state"]                = "OFF"
        device["cpu_utilization_percent"]    = 0.0
        device["memory_utilization_percent"] = 0.0
        device["power_draw_watts"]           = 0.0
        device["temperature_celsius"]        = 0.0

    device["updated_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S+05:30")
    device.pop("powerState", None)
    db.upsert_item(collection_path, device_id, device)
    logging.getLogger(__name__).info(
        f"[PowerOp] Device {device_id} transitioned to {target_state} after {delay}s delay."
    )


@app.put("/rest/server-hardware/{id}/powerState")
@app.post("/rest/server-hardware/{id}/power")
def post_oneview_device_power(id: str, payload: OneViewPowerRequest):
    """
    Action Route: PUT/POST to change power state of a server.
    Returns 202 Accepted immediately with state=TRANSITIONING.
    The actual state change is applied after POWER_OP_DELAY_SECONDS in the background.
    """
    import datetime
    collection_path = "/rest/server-hardware"

    device = db.get_item(collection_path, id)
    if not device:
        raise HTTPException(status_code=404, detail="Server hardware not found")

    device = dict(device)

    raw_state = payload.powerState or payload.power_state or payload.action or ""
    raw_upper = str(raw_state).upper().strip()

    _ON_STATES  = {"ON", "POWERON", "POWER_ON", "START", "BOOT", "ENABLE", "TRUE"}
    _OFF_STATES = {"OFF", "POWEROFF", "POWER_OFF", "SHUTDOWN", "STOP", "HALT", "DISABLE", "FALSE"}

    if raw_upper in _ON_STATES:
        target_state = "ON"
    elif raw_upper in _OFF_STATES:
        target_state = "OFF"
    else:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid power state '{raw_state}'. Accepted: On, Off, PowerOn, PowerOff."
        )

    # Mark device as TRANSITIONING immediately so concurrent reads show in-progress
    device["power_state"] = "TRANSITIONING"
    device["updated_at"]  = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S+05:30")
    device.pop("powerState", None)
    db.upsert_item(collection_path, device["id"], device)

    # Schedule the actual state change in a background thread
    t = threading.Thread(
        target=_apply_power_state_after_delay,
        args=(collection_path, device["id"], target_state, POWER_OP_DELAY_SECONDS),
        daemon=True
    )
    t.start()

    # Return 202 with current transitioning snapshot
    return JSONResponse(
        status_code=202,
        content={
            "id":          device["id"],
            "name":        device.get("name", id),
            "power_state": "TRANSITIONING",
            "target":      target_state,
            "message":     f"Power {target_state} operation accepted. Device will be {target_state} in ~{POWER_OP_DELAY_SECONDS}s.",
            "estimated_completion_seconds": POWER_OP_DELAY_SECONDS
        }
    )


@app.get("/rest/ethernet-networks")
def get_rest_ethernet_networks():
    """
    Dynamic CRUD Route: GET /rest/ethernet-networks
    """
    collection_path = "/rest/ethernet-networks"
    return db.get_all(collection_path)

@app.get("/rest/ethernet-networks/{id}")
def get_rest_ethernet_networks_id(id: str):
    """
    Dynamic CRUD Route: GET /rest/ethernet-networks/{id}
    """
    collection_path = f"/rest/ethernet-networks"
    item = db.get_item(collection_path, id)
    if item:
        return item
    raise HTTPException(status_code=404, detail="ethernet-networks not found")

@app.post("/rest/ethernet-networks")
def post_rest_ethernet_networks(payload: dict, request: Request):
    """
    Dynamic CRUD Route: POST /rest/ethernet-networks
    Returns 202 Accepted.
    """
    collection_path = "/rest/ethernet-networks"
    item_id = payload.get("id") or payload.get("uri", "").split("/")[-1] or str(uuid.uuid4())
    payload["id"] = item_id
    if "uri" not in payload:
        payload["uri"] = f"/rest/ethernet-networks/{item_id}"
    payload["status"] = "Adding"

    db.upsert_item(collection_path, item_id, payload)

    t = threading.Thread(
        target=_apply_async_crud,
        args=(collection_path, item_id, {"status": "OK"}, 3, "POST"),
        daemon=True
    )
    t.start()
    return JSONResponse(status_code=202, content={"message": "Creation accepted", "id": item_id, "item": payload})

@app.put("/rest/ethernet-networks/{id}")
def put_rest_ethernet_networks_id(id: str, payload: dict):
    """
    Dynamic CRUD Route: PUT /rest/ethernet-networks/{id}
    Returns 202 Accepted.
    """
    collection_path = "/rest/ethernet-networks"
    existing = db.get_item(collection_path, id)
    if not existing:
        raise HTTPException(status_code=404, detail="ethernet-networks not found")
    
    payload["id"] = id
    payload["status"] = "Updating"
    
    db.upsert_item(collection_path, id, payload)
    
    t = threading.Thread(
        target=_apply_async_crud,
        args=(collection_path, id, {"status": "OK"}, 3, "PUT"),
        daemon=True
    )
    t.start()
    return JSONResponse(status_code=202, content={"message": "Update accepted", "id": id, "item": payload})

@app.delete("/rest/ethernet-networks/{id}")
def delete_rest_ethernet_networks_id(id: str):
    """
    Dynamic CRUD Route: DELETE /rest/ethernet-networks/{id}
    Returns 202 Accepted.
    """
    collection_path = "/rest/ethernet-networks"
    item = db.get_item(collection_path, id)
    if item:
        item = dict(item)
        item["status"] = "Removing"
        db.upsert_item(collection_path, id, item)
        
        t = threading.Thread(
            target=_apply_async_crud,
            args=(collection_path, id, {}, 5, "DELETE"),
            daemon=True
        )
        t.start()
        return JSONResponse(status_code=202, content={"message": "Deletion accepted", "id": id, "item": item})
    raise HTTPException(status_code=404, detail="ethernet-networks not found")

@app.get("/rest/fc-networks")
def get_rest_fc_networks():
    """
    Dynamic CRUD Route: GET /rest/fc-networks
    """
    collection_path = "/rest/fc-networks"
    return db.get_all(collection_path)

@app.get("/rest/fc-networks/{id}")
def get_rest_fc_networks_id(id: str):
    """
    Dynamic CRUD Route: GET /rest/fc-networks/{id}
    """
    collection_path = f"/rest/fc-networks"
    item = db.get_item(collection_path, id)
    if item:
        return item
    raise HTTPException(status_code=404, detail="fc-networks not found")

@app.post("/rest/fc-networks")
def post_rest_fc_networks(payload: dict, request: Request):
    """
    Dynamic CRUD Route: POST /rest/fc-networks
    Returns 202 Accepted.
    """
    collection_path = "/rest/fc-networks"
    item_id = payload.get("id") or payload.get("uri", "").split("/")[-1] or str(uuid.uuid4())
    payload["id"] = item_id
    if "uri" not in payload:
        payload["uri"] = f"/rest/fc-networks/{item_id}"
    payload["status"] = "Adding"

    db.upsert_item(collection_path, item_id, payload)

    t = threading.Thread(
        target=_apply_async_crud,
        args=(collection_path, item_id, {"status": "OK"}, 3, "POST"),
        daemon=True
    )
    t.start()
    return JSONResponse(status_code=202, content={"message": "Creation accepted", "id": item_id, "item": payload})

@app.put("/rest/fc-networks/{id}")
def put_rest_fc_networks_id(id: str, payload: dict):
    """
    Dynamic CRUD Route: PUT /rest/fc-networks/{id}
    Returns 202 Accepted.
    """
    collection_path = "/rest/fc-networks"
    existing = db.get_item(collection_path, id)
    if not existing:
        raise HTTPException(status_code=404, detail="fc-networks not found")
    
    payload["id"] = id
    payload["status"] = "Updating"
    
    db.upsert_item(collection_path, id, payload)
    
    t = threading.Thread(
        target=_apply_async_crud,
        args=(collection_path, id, {"status": "OK"}, 3, "PUT"),
        daemon=True
    )
    t.start()
    return JSONResponse(status_code=202, content={"message": "Update accepted", "id": id, "item": payload})

@app.delete("/rest/fc-networks/{id}")
def delete_rest_fc_networks_id(id: str):
    """
    Dynamic CRUD Route: DELETE /rest/fc-networks/{id}
    Returns 202 Accepted.
    """
    collection_path = "/rest/fc-networks"
    item = db.get_item(collection_path, id)
    if item:
        item = dict(item)
        item["status"] = "Removing"
        db.upsert_item(collection_path, id, item)
        
        t = threading.Thread(
            target=_apply_async_crud,
            args=(collection_path, id, {}, 5, "DELETE"),
            daemon=True
        )
        t.start()
        return JSONResponse(status_code=202, content={"message": "Deletion accepted", "id": id, "item": item})
    raise HTTPException(status_code=404, detail="fc-networks not found")

@app.get("/rest/fcoe-networks")
def get_rest_fcoe_networks():
    """
    Dynamic CRUD Route: GET /rest/fcoe-networks
    """
    collection_path = "/rest/fcoe-networks"
    return db.get_all(collection_path)

@app.get("/rest/fcoe-networks/{id}")
def get_rest_fcoe_networks_id(id: str):
    """
    Dynamic CRUD Route: GET /rest/fcoe-networks/{id}
    """
    collection_path = f"/rest/fcoe-networks"
    item = db.get_item(collection_path, id)
    if item:
        return item
    raise HTTPException(status_code=404, detail="fcoe-networks not found")

@app.post("/rest/fcoe-networks")
def post_rest_fcoe_networks(payload: dict, request: Request):
    """
    Dynamic CRUD Route: POST /rest/fcoe-networks
    Returns 202 Accepted.
    """
    collection_path = "/rest/fcoe-networks"
    item_id = payload.get("id") or payload.get("uri", "").split("/")[-1] or str(uuid.uuid4())
    payload["id"] = item_id
    if "uri" not in payload:
        payload["uri"] = f"/rest/fcoe-networks/{item_id}"
    payload["status"] = "Adding"

    db.upsert_item(collection_path, item_id, payload)

    t = threading.Thread(
        target=_apply_async_crud,
        args=(collection_path, item_id, {"status": "OK"}, 3, "POST"),
        daemon=True
    )
    t.start()
    return JSONResponse(status_code=202, content={"message": "Creation accepted", "id": item_id, "item": payload})

@app.put("/rest/fcoe-networks/{id}")
def put_rest_fcoe_networks_id(id: str, payload: dict):
    """
    Dynamic CRUD Route: PUT /rest/fcoe-networks/{id}
    Returns 202 Accepted.
    """
    collection_path = "/rest/fcoe-networks"
    existing = db.get_item(collection_path, id)
    if not existing:
        raise HTTPException(status_code=404, detail="fcoe-networks not found")
    
    payload["id"] = id
    payload["status"] = "Updating"
    
    db.upsert_item(collection_path, id, payload)
    
    t = threading.Thread(
        target=_apply_async_crud,
        args=(collection_path, id, {"status": "OK"}, 3, "PUT"),
        daemon=True
    )
    t.start()
    return JSONResponse(status_code=202, content={"message": "Update accepted", "id": id, "item": payload})

@app.delete("/rest/fcoe-networks/{id}")
def delete_rest_fcoe_networks_id(id: str):
    """
    Dynamic CRUD Route: DELETE /rest/fcoe-networks/{id}
    Returns 202 Accepted.
    """
    collection_path = "/rest/fcoe-networks"
    item = db.get_item(collection_path, id)
    if item:
        item = dict(item)
        item["status"] = "Removing"
        db.upsert_item(collection_path, id, item)
        
        t = threading.Thread(
            target=_apply_async_crud,
            args=(collection_path, id, {}, 5, "DELETE"),
            daemon=True
        )
        t.start()
        return JSONResponse(status_code=202, content={"message": "Deletion accepted", "id": id, "item": item})
    raise HTTPException(status_code=404, detail="fcoe-networks not found")

@app.get("/rest/logical-interconnect-groups")
def get_rest_logical_interconnect_groups():
    """
    Dynamic CRUD Route: GET /rest/logical-interconnect-groups
    """
    collection_path = "/rest/logical-interconnect-groups"
    return db.get_all(collection_path)

@app.get("/rest/logical-interconnect-groups/{id}")
def get_rest_logical_interconnect_groups_id(id: str):
    """
    Dynamic CRUD Route: GET /rest/logical-interconnect-groups/{id}
    """
    collection_path = f"/rest/logical-interconnect-groups"
    item = db.get_item(collection_path, id)
    if item:
        return item
    raise HTTPException(status_code=404, detail="logical-interconnect-groups not found")

@app.post("/rest/logical-interconnect-groups")
def post_rest_logical_interconnect_groups(payload: dict, request: Request):
    """
    Dynamic CRUD Route: POST /rest/logical-interconnect-groups
    Returns 202 Accepted.
    """
    collection_path = "/rest/logical-interconnect-groups"
    item_id = payload.get("id") or payload.get("uri", "").split("/")[-1] or str(uuid.uuid4())
    payload["id"] = item_id
    if "uri" not in payload:
        payload["uri"] = f"/rest/logical-interconnect-groups/{item_id}"
    payload["status"] = "Adding"

    db.upsert_item(collection_path, item_id, payload)

    t = threading.Thread(
        target=_apply_async_crud,
        args=(collection_path, item_id, {"status": "OK"}, 3, "POST"),
        daemon=True
    )
    t.start()
    return JSONResponse(status_code=202, content={"message": "Creation accepted", "id": item_id, "item": payload})

@app.put("/rest/logical-interconnect-groups/{id}")
def put_rest_logical_interconnect_groups_id(id: str, payload: dict):
    """
    Dynamic CRUD Route: PUT /rest/logical-interconnect-groups/{id}
    Returns 202 Accepted.
    """
    collection_path = "/rest/logical-interconnect-groups"
    existing = db.get_item(collection_path, id)
    if not existing:
        raise HTTPException(status_code=404, detail="logical-interconnect-groups not found")
    
    payload["id"] = id
    payload["status"] = "Updating"
    
    db.upsert_item(collection_path, id, payload)
    
    t = threading.Thread(
        target=_apply_async_crud,
        args=(collection_path, id, {"status": "OK"}, 3, "PUT"),
        daemon=True
    )
    t.start()
    return JSONResponse(status_code=202, content={"message": "Update accepted", "id": id, "item": payload})

@app.delete("/rest/logical-interconnect-groups/{id}")
def delete_rest_logical_interconnect_groups_id(id: str):
    """
    Dynamic CRUD Route: DELETE /rest/logical-interconnect-groups/{id}
    Returns 202 Accepted.
    """
    collection_path = "/rest/logical-interconnect-groups"
    item = db.get_item(collection_path, id)
    if item:
        item = dict(item)
        item["status"] = "Removing"
        db.upsert_item(collection_path, id, item)
        
        t = threading.Thread(
            target=_apply_async_crud,
            args=(collection_path, id, {}, 5, "DELETE"),
            daemon=True
        )
        t.start()
        return JSONResponse(status_code=202, content={"message": "Deletion accepted", "id": id, "item": item})
    raise HTTPException(status_code=404, detail="logical-interconnect-groups not found")

@app.get("/rest/uplink-sets")
def get_rest_uplink_sets():
    """
    Dynamic CRUD Route: GET /rest/uplink-sets
    """
    collection_path = "/rest/uplink-sets"
    return db.get_all(collection_path)

@app.get("/rest/uplink-sets/{id}")
def get_rest_uplink_sets_id(id: str):
    """
    Dynamic CRUD Route: GET /rest/uplink-sets/{id}
    """
    collection_path = f"/rest/uplink-sets"
    item = db.get_item(collection_path, id)
    if item:
        return item
    raise HTTPException(status_code=404, detail="uplink-sets not found")

@app.post("/rest/uplink-sets")
def post_rest_uplink_sets(payload: dict, request: Request):
    """
    Dynamic CRUD Route: POST /rest/uplink-sets
    Returns 202 Accepted.
    """
    collection_path = "/rest/uplink-sets"
    item_id = payload.get("id") or payload.get("uri", "").split("/")[-1] or str(uuid.uuid4())
    payload["id"] = item_id
    if "uri" not in payload:
        payload["uri"] = f"/rest/uplink-sets/{item_id}"
    payload["status"] = "Adding"

    db.upsert_item(collection_path, item_id, payload)

    t = threading.Thread(
        target=_apply_async_crud,
        args=(collection_path, item_id, {"status": "OK"}, 3, "POST"),
        daemon=True
    )
    t.start()
    return JSONResponse(status_code=202, content={"message": "Creation accepted", "id": item_id, "item": payload})

@app.put("/rest/uplink-sets/{id}")
def put_rest_uplink_sets_id(id: str, payload: dict):
    """
    Dynamic CRUD Route: PUT /rest/uplink-sets/{id}
    Returns 202 Accepted.
    """
    collection_path = "/rest/uplink-sets"
    existing = db.get_item(collection_path, id)
    if not existing:
        raise HTTPException(status_code=404, detail="uplink-sets not found")
    
    payload["id"] = id
    payload["status"] = "Updating"
    
    db.upsert_item(collection_path, id, payload)
    
    t = threading.Thread(
        target=_apply_async_crud,
        args=(collection_path, id, {"status": "OK"}, 3, "PUT"),
        daemon=True
    )
    t.start()
    return JSONResponse(status_code=202, content={"message": "Update accepted", "id": id, "item": payload})

@app.delete("/rest/uplink-sets/{id}")
def delete_rest_uplink_sets_id(id: str):
    """
    Dynamic CRUD Route: DELETE /rest/uplink-sets/{id}
    Returns 202 Accepted.
    """
    collection_path = "/rest/uplink-sets"
    item = db.get_item(collection_path, id)
    if item:
        item = dict(item)
        item["status"] = "Removing"
        db.upsert_item(collection_path, id, item)
        
        t = threading.Thread(
            target=_apply_async_crud,
            args=(collection_path, id, {}, 5, "DELETE"),
            daemon=True
        )
        t.start()
        return JSONResponse(status_code=202, content={"message": "Deletion accepted", "id": id, "item": item})
    raise HTTPException(status_code=404, detail="uplink-sets not found")

@app.get("/rest/logical-interconnects")
def get_rest_logical_interconnects():
    """
    Dynamic CRUD Route: GET /rest/logical-interconnects
    """
    collection_path = "/rest/logical-interconnects"
    return db.get_all(collection_path)

@app.get("/rest/logical-interconnects/{id}")
def get_rest_logical_interconnects_id(id: str):
    """
    Dynamic CRUD Route: GET /rest/logical-interconnects/{id}
    """
    collection_path = "/rest/logical-interconnects"
    item = db.get_item(collection_path, id)
    if item:
        return item
    raise HTTPException(status_code=404, detail="logical-interconnects not found")

@app.put("/rest/logical-interconnects/{id}")
def put_rest_logical_interconnects_id(id: str, payload: dict):
    """
    Dynamic CRUD Route: PUT /rest/logical-interconnects/{id}
    Returns 202 Accepted.
    """
    collection_path = "/rest/logical-interconnects"
    existing = db.get_item(collection_path, id)
    if not existing:
        raise HTTPException(status_code=404, detail="logical-interconnects not found")
    
    payload["id"] = id
    payload["status"] = "Updating"
    
    db.upsert_item(collection_path, id, payload)
    
    t = threading.Thread(
        target=_apply_async_crud,
        args=(collection_path, id, {"status": "OK"}, 5, "PUT"),
        daemon=True
    )
    t.start()
    return JSONResponse(status_code=202, content={"message": "Update accepted", "id": id, "item": payload})


@app.get("/rest/storage-systems")
def get_rest_storage_systems():
    """
    Dynamic CRUD Route: GET /rest/storage-systems
    """
    collection_path = "/rest/storage-systems"
    return db.get_all(collection_path)

@app.get("/rest/storage-systems/{id}")
def get_rest_storage_systems_id(id: str):
    """
    Dynamic CRUD Route: GET /rest/storage-systems/{id}
    """
    collection_path = f"/rest/storage-systems"
    item = db.get_item(collection_path, id)
    if item:
        return item
    raise HTTPException(status_code=404, detail="storage-systems not found")

@app.post("/rest/storage-systems")
def post_rest_storage_systems(payload: dict, request: Request):
    """
    Dynamic CRUD Route: POST /rest/storage-systems
    Returns 202 Accepted.
    """
    collection_path = "/rest/storage-systems"
    item_id = payload.get("id") or payload.get("uri", "").split("/")[-1] or str(uuid.uuid4())
    payload["id"] = item_id
    if "uri" not in payload:
        payload["uri"] = f"/rest/storage-systems/{item_id}"
    payload["status"] = "Adding"

    db.upsert_item(collection_path, item_id, payload)

    t = threading.Thread(
        target=_apply_async_crud,
        args=(collection_path, item_id, {"status": "OK"}, 5, "POST"),
        daemon=True
    )
    t.start()
    return JSONResponse(status_code=202, content={"message": "Creation accepted", "id": item_id, "item": payload})

@app.put("/rest/storage-systems/{id}")
def put_rest_storage_systems_id_batch2(id: str, payload: dict):
    """
    Dynamic CRUD Route: PUT /rest/storage-systems/{id}
    Returns 202 Accepted.
    """
    collection_path = "/rest/storage-systems"
    existing = db.get_item(collection_path, id)
    if not existing:
        raise HTTPException(status_code=404, detail="storage-systems not found")
    
    payload["id"] = id
    payload["status"] = "Updating"
    
    db.upsert_item(collection_path, id, payload)
    
    t = threading.Thread(
        target=_apply_async_crud,
        args=(collection_path, id, {"status": "OK"}, 5, "PUT"),
        daemon=True
    )
    t.start()
    return JSONResponse(status_code=202, content={"message": "Update accepted", "id": id, "item": payload})

@app.delete("/rest/storage-systems/{id}")
def delete_rest_storage_systems_id(id: str):
    """
    Dynamic CRUD Route: DELETE /rest/storage-systems/{id}
    Returns 202 Accepted.
    """
    collection_path = "/rest/storage-systems"
    item = db.get_item(collection_path, id)
    if item:
        item = dict(item)
        item["status"] = "Removing"
        db.upsert_item(collection_path, id, item)
        
        t = threading.Thread(
            target=_apply_async_crud,
            args=(collection_path, id, {}, 6, "DELETE"),
            daemon=True
        )
        t.start()
        return JSONResponse(status_code=202, content={"message": "Deletion accepted", "id": id, "item": item})
    raise HTTPException(status_code=404, detail="storage-systems not found")

@app.get("/rest/storage-pools")
def get_rest_storage_pools():
    """
    Dynamic CRUD Route: GET /rest/storage-pools
    """
    collection_path = "/rest/storage-pools"
    return db.get_all(collection_path)

@app.get("/rest/storage-pools/{id}")
def get_rest_storage_pools_id(id: str):
    """
    Dynamic CRUD Route: GET /rest/storage-pools/{id}
    """
    collection_path = f"/rest/storage-pools"
    item = db.get_item(collection_path, id)
    if item:
        return item
    raise HTTPException(status_code=404, detail="storage-pools not found")

@app.post("/rest/storage-pools")
def post_rest_storage_pools(payload: dict, request: Request):
    """
    Dynamic CRUD Route: POST /rest/storage-pools
    Returns 202 Accepted.
    """
    collection_path = "/rest/storage-pools"
    item_id = payload.get("id") or payload.get("uri", "").split("/")[-1] or str(uuid.uuid4())
    payload["id"] = item_id
    if "uri" not in payload:
        payload["uri"] = f"/rest/storage-pools/{item_id}"
    payload["status"] = "Adding"

    db.upsert_item(collection_path, item_id, payload)

    t = threading.Thread(
        target=_apply_async_crud,
        args=(collection_path, item_id, {"status": "OK"}, 5, "POST"),
        daemon=True
    )
    t.start()
    return JSONResponse(status_code=202, content={"message": "Creation accepted", "id": item_id, "item": payload})

@app.put("/rest/storage-pools/{id}")
def put_rest_storage_pools_id_batch2(id: str, payload: dict):
    """
    Dynamic CRUD Route: PUT /rest/storage-pools/{id}
    Returns 202 Accepted.
    """
    collection_path = "/rest/storage-pools"
    existing = db.get_item(collection_path, id)
    if not existing:
        raise HTTPException(status_code=404, detail="storage-pools not found")
    
    payload["id"] = id
    payload["status"] = "Updating"
    
    db.upsert_item(collection_path, id, payload)
    
    t = threading.Thread(
        target=_apply_async_crud,
        args=(collection_path, id, {"status": "OK"}, 5, "PUT"),
        daemon=True
    )
    t.start()
    return JSONResponse(status_code=202, content={"message": "Update accepted", "id": id, "item": payload})

@app.delete("/rest/storage-pools/{id}")
def delete_rest_storage_pools_id(id: str):
    """
    Dynamic CRUD Route: DELETE /rest/storage-pools/{id}
    Returns 202 Accepted.
    """
    collection_path = "/rest/storage-pools"
    item = db.get_item(collection_path, id)
    if item:
        item = dict(item)
        item["status"] = "Removing"
        db.upsert_item(collection_path, id, item)
        
        t = threading.Thread(
            target=_apply_async_crud,
            args=(collection_path, id, {}, 6, "DELETE"),
            daemon=True
        )
        t.start()
        return JSONResponse(status_code=202, content={"message": "Deletion accepted", "id": id, "item": item})
    raise HTTPException(status_code=404, detail="storage-pools not found")

@app.get("/rest/storage-volumes")
def get_rest_storage_volumes():
    """
    Dynamic CRUD Route: GET /rest/storage-volumes
    """
    collection_path = "/rest/storage-volumes"
    return db.get_all(collection_path)

@app.get("/rest/storage-volumes/{id}")
def get_rest_storage_volumes_id(id: str):
    """
    Dynamic CRUD Route: GET /rest/storage-volumes/{id}
    """
    collection_path = f"/rest/storage-volumes"
    item = db.get_item(collection_path, id)
    if item:
        return item
    raise HTTPException(status_code=404, detail="storage-volumes not found")

@app.post("/rest/storage-volumes")
def post_rest_storage_volumes(payload: dict, request: Request):
    """
    Dynamic CRUD Route: POST /rest/storage-volumes
    Returns 202 Accepted.
    """
    collection_path = "/rest/storage-volumes"
    item_id = payload.get("id") or payload.get("uri", "").split("/")[-1] or str(uuid.uuid4())
    payload["id"] = item_id
    if "uri" not in payload:
        payload["uri"] = f"/rest/storage-volumes/{item_id}"
    payload["status"] = "Adding"

    db.upsert_item(collection_path, item_id, payload)

    t = threading.Thread(
        target=_apply_async_crud,
        args=(collection_path, item_id, {"status": "OK"}, 5, "POST"),
        daemon=True
    )
    t.start()
    return JSONResponse(status_code=202, content={"message": "Creation accepted", "id": item_id, "item": payload})

@app.put("/rest/storage-volumes/{id}")
def put_rest_storage_volumes_id_batch2(id: str, payload: dict):
    """
    Dynamic CRUD Route: PUT /rest/storage-volumes/{id}
    Returns 202 Accepted.
    """
    collection_path = "/rest/storage-volumes"
    existing = db.get_item(collection_path, id)
    if not existing:
        raise HTTPException(status_code=404, detail="storage-volumes not found")
    
    payload["id"] = id
    payload["status"] = "Updating"
    
    db.upsert_item(collection_path, id, payload)
    
    t = threading.Thread(
        target=_apply_async_crud,
        args=(collection_path, id, {"status": "OK"}, 5, "PUT"),
        daemon=True
    )
    t.start()
    return JSONResponse(status_code=202, content={"message": "Update accepted", "id": id, "item": payload})

@app.delete("/rest/storage-volumes/{id}")
def delete_rest_storage_volumes_id(id: str):
    """
    Dynamic CRUD Route: DELETE /rest/storage-volumes/{id}
    Returns 202 Accepted.
    """
    collection_path = "/rest/storage-volumes"
    item = db.get_item(collection_path, id)
    if item:
        item = dict(item)
        item["status"] = "Removing"
        db.upsert_item(collection_path, id, item)
        
        t = threading.Thread(
            target=_apply_async_crud,
            args=(collection_path, id, {}, 6, "DELETE"),
            daemon=True
        )
        t.start()
        return JSONResponse(status_code=202, content={"message": "Deletion accepted", "id": id, "item": item})
    raise HTTPException(status_code=404, detail="storage-volumes not found")

@app.get("/rest/storage-volume-templates")
def get_rest_storage_volume_templates():
    """
    Dynamic CRUD Route: GET /rest/storage-volume-templates
    """
    collection_path = "/rest/storage-volume-templates"
    return db.get_all(collection_path)

@app.get("/rest/storage-volume-templates/{id}")
def get_rest_storage_volume_templates_id(id: str):
    """
    Dynamic CRUD Route: GET /rest/storage-volume-templates/{id}
    """
    collection_path = f"/rest/storage-volume-templates"
    item = db.get_item(collection_path, id)
    if item:
        return item
    raise HTTPException(status_code=404, detail="storage-volume-templates not found")

@app.post("/rest/storage-volume-templates")
def post_rest_storage_volume_templates(payload: dict, request: Request):
    """
    Dynamic CRUD Route: POST /rest/storage-volume-templates
    Returns 202 Accepted.
    """
    collection_path = "/rest/storage-volume-templates"
    item_id = payload.get("id") or payload.get("uri", "").split("/")[-1] or str(uuid.uuid4())
    payload["id"] = item_id
    if "uri" not in payload:
        payload["uri"] = f"/rest/storage-volume-templates/{item_id}"
    payload["status"] = "Adding"

    db.upsert_item(collection_path, item_id, payload)

    t = threading.Thread(
        target=_apply_async_crud,
        args=(collection_path, item_id, {"status": "OK"}, 5, "POST"),
        daemon=True
    )
    t.start()
    return JSONResponse(status_code=202, content={"message": "Creation accepted", "id": item_id, "item": payload})

@app.put("/rest/storage-volume-templates/{id}")
def put_rest_storage_volume_templates_id_batch2(id: str, payload: dict):
    """
    Dynamic CRUD Route: PUT /rest/storage-volume-templates/{id}
    Returns 202 Accepted.
    """
    collection_path = "/rest/storage-volume-templates"
    existing = db.get_item(collection_path, id)
    if not existing:
        raise HTTPException(status_code=404, detail="storage-volume-templates not found")
    
    payload["id"] = id
    payload["status"] = "Updating"
    
    db.upsert_item(collection_path, id, payload)
    
    t = threading.Thread(
        target=_apply_async_crud,
        args=(collection_path, id, {"status": "OK"}, 5, "PUT"),
        daemon=True
    )
    t.start()
    return JSONResponse(status_code=202, content={"message": "Update accepted", "id": id, "item": payload})

@app.delete("/rest/storage-volume-templates/{id}")
def delete_rest_storage_volume_templates_id(id: str):
    """
    Dynamic CRUD Route: DELETE /rest/storage-volume-templates/{id}
    Returns 202 Accepted.
    """
    collection_path = "/rest/storage-volume-templates"
    item = db.get_item(collection_path, id)
    if item:
        item = dict(item)
        item["status"] = "Removing"
        db.upsert_item(collection_path, id, item)
        
        t = threading.Thread(
            target=_apply_async_crud,
            args=(collection_path, id, {}, 6, "DELETE"),
            daemon=True
        )
        t.start()
        return JSONResponse(status_code=202, content={"message": "Deletion accepted", "id": id, "item": item})
    raise HTTPException(status_code=404, detail="storage-volume-templates not found")

@app.get("/rest/san-managers")
def get_rest_san_managers():
    """
    Dynamic CRUD Route: GET /rest/san-managers
    """
    collection_path = "/rest/san-managers"
    return db.get_all(collection_path)

@app.get("/rest/san-managers/{id}")
def get_rest_san_managers_id(id: str):
    """
    Dynamic CRUD Route: GET /rest/san-managers/{id}
    """
    collection_path = f"/rest/san-managers"
    item = db.get_item(collection_path, id)
    if item:
        return item
    raise HTTPException(status_code=404, detail="san-managers not found")

@app.post("/rest/san-managers")
def post_rest_san_managers(payload: dict, request: Request):
    """
    Dynamic CRUD Route: POST /rest/san-managers
    Returns 202 Accepted.
    """
    collection_path = "/rest/san-managers"
    item_id = payload.get("id") or payload.get("uri", "").split("/")[-1] or str(uuid.uuid4())
    payload["id"] = item_id
    if "uri" not in payload:
        payload["uri"] = f"/rest/san-managers/{item_id}"
    payload["status"] = "Adding"

    db.upsert_item(collection_path, item_id, payload)

    t = threading.Thread(
        target=_apply_async_crud,
        args=(collection_path, item_id, {"status": "OK"}, 5, "POST"),
        daemon=True
    )
    t.start()
    return JSONResponse(status_code=202, content={"message": "Creation accepted", "id": item_id, "item": payload})

@app.put("/rest/san-managers/{id}")
def put_rest_san_managers_id_batch2(id: str, payload: dict):
    """
    Dynamic CRUD Route: PUT /rest/san-managers/{id}
    Returns 202 Accepted.
    """
    collection_path = "/rest/san-managers"
    existing = db.get_item(collection_path, id)
    if not existing:
        raise HTTPException(status_code=404, detail="san-managers not found")
    
    payload["id"] = id
    payload["status"] = "Updating"
    
    db.upsert_item(collection_path, id, payload)
    
    t = threading.Thread(
        target=_apply_async_crud,
        args=(collection_path, id, {"status": "OK"}, 5, "PUT"),
        daemon=True
    )
    t.start()
    return JSONResponse(status_code=202, content={"message": "Update accepted", "id": id, "item": payload})

@app.delete("/rest/san-managers/{id}")
def delete_rest_san_managers_id(id: str):
    """
    Dynamic CRUD Route: DELETE /rest/san-managers/{id}
    Returns 202 Accepted.
    """
    collection_path = "/rest/san-managers"
    item = db.get_item(collection_path, id)
    if item:
        item = dict(item)
        item["status"] = "Removing"
        db.upsert_item(collection_path, id, item)
        
        t = threading.Thread(
            target=_apply_async_crud,
            args=(collection_path, id, {}, 6, "DELETE"),
            daemon=True
        )
        t.start()
        return JSONResponse(status_code=202, content={"message": "Deletion accepted", "id": id, "item": item})
    raise HTTPException(status_code=404, detail="san-managers not found")

