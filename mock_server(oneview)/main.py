import uuid
from fastapi import FastAPI, Query, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import json
import os
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
    """
    collection_path = f"/rest/server-hardware/{id}/thermal"
    static_data = db.get_static("get_rest_server_hardware_id_thermal", dict())
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
    """
    collection_path = f"/rest/ethernet-networks/bulk"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.put("/rest/storage-volumes/{id}")
def put_rest_storage_volumes_id(id: str, payload: PutRestStorageVolumesIdRequest):
    """
    Dynamic CRUD Route: PUT /rest/storage-volumes/{id}
    """
    collection_path = f"/rest/storage-volumes"
    item_id = id
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

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
    """
    collection_path = f"/rest/rack-managers"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

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
    """
    collection_path = f"/rest/rack-managers"
    item_id = id
    payload_dict = {}
    existing = db.get_item(collection_path, item_id) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, item_id, existing)
    return existing

@app.delete("/rest/rack-managers/{id}")
def delete_rest_rack_managers_id(id: str):
    """
    Dynamic CRUD Route: DELETE /rest/rack-managers/{id}
    """
    collection_path = f"/rest/rack-managers"
    item_id = id
    item = db.get_item(collection_path, item_id)
    if item:
        deleted = db.delete_item(collection_path, item_id)
        return {"message": "Deleted successfully", "id": item_id, "item": deleted}
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

@app.get("/rest/rack-managers/{id}/chassis/utilization")
def get_rest_rack_managers_id_chassis_utilization(id: str):
    """
    Dynamic CRUD Route: GET /rest/rack-managers/{id}/chassis/utilization
    """
    collection_path = f"/rest/rack-managers/{id}/chassis/utilization"
    static_data = db.get_static("get_rest_rack_managers_id_chassis_utilization", dict())
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
def get_rest_server_hardware():
    """
    Dynamic CRUD Route: GET /rest/server-hardware
    """
    collection_path = f"/rest/server-hardware"
    static_data = db.get_static("get_rest_server_hardware", dict())
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

@app.post("/rest/server-hardware")
def post_rest_server_hardware(payload: PostRestServerHardwareRequest):
    """
    Dynamic CRUD Route: POST /rest/server-hardware
    """
    collection_path = f"/rest/server-hardware"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

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
    """
    collection_path = f"/rest/server-hardware/discovery"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.post("/rest/server-hardware/firmware-compliance")
def post_rest_server_hardware_firmware_compliance(payload: PostRestServerHardwareFirmwareComplianceRequest):
    """
    Dynamic CRUD Route: POST /rest/server-hardware/firmware-compliance
    """
    collection_path = f"/rest/server-hardware/firmware-compliance"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

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
        return item
    raise HTTPException(status_code=404, detail="Server hardware not found")


@app.put("/rest/server-hardware/{id}")
def put_rest_server_hardware_id(id: str, payload: dict):
    """
    Dynamic CRUD Route: PUT /rest/server-hardware/{id}
    """
    collection_path = f"/rest/server-hardware"
        
    existing = db.get_item(collection_path, id)

        
    if not existing:

        
        raise HTTPException(status_code=404, detail="Resource not found")

        
    existing = dict(existing)
    payload_dict = {k: v for k, v in payload.items() if v is not None}
    existing.update(payload_dict)
    db.upsert_item(collection_path, existing["id"], existing)
    return existing


@app.delete("/rest/server-hardware/{id}")
def delete_rest_server_hardware_id(id: str):
    """
    Dynamic CRUD Route: DELETE /rest/server-hardware/{id}
    """
    collection_path = f"/rest/server-hardware"
        
    store = db.get_collection(collection_path)
    if id not in store:
        static_list = db.get_static("get_rest_server_hardware").get("members", [])
        static_item = None
        for item in static_list:
            if item.get("id") == id:
                static_item = item
                break
        if not static_item and db.get_static("get_rest_server_hardware_id").get("id") == id:
            static_item = db.get_static("get_rest_server_hardware_id")
            
        if static_item:
            return {"message": "Deleted successfully", "id": id, "item": static_item}
        else:
            raise HTTPException(status_code=404, detail="Server hardware not found")
            
    deleted = db.delete_item(collection_path, id)
    return {"message": "Deleted successfully", "id": id, "item": deleted}


class OneViewPowerRequest(BaseModel):
    powerState: str = None
    powerControl: str = None
    action: str = None


@app.put("/rest/server-hardware/{id}/powerState")
@app.post("/rest/server-hardware/{id}/power")
def post_oneview_device_power(id: str, payload: OneViewPowerRequest):
    """
    Action Route: PUT/POST to change power state of a server
    """
    collection_path = f"/rest/server-hardware"
        
    device = db.get_item(collection_path, id)
    if not device:
        raise HTTPException(status_code=404, detail="Server hardware not found")
            
    device = dict(device)
    state = payload.powerState or payload.action or "On"
    
    import random
    
    if state.upper() in ["ON", "POWERON"]:
        device["power_state"] = "ON"
        device["powerState"] = "On"
        device["cpu_utilization_percent"] = round(random.uniform(10.0, 90.0), 1)
        device["memory_utilization_percent"] = round(random.uniform(10.0, 90.0), 1)
        device["power_draw_watts"] = round(random.uniform(150.0, 400.0), 1)
        device["temperature_celsius"] = round(random.uniform(25.0, 45.0), 1)
    elif state.upper() in ["OFF", "POWEROFF"]:
        device["power_state"] = "OFF"
        device["powerState"] = "Off"
        device["cpu_utilization_percent"] = 0.0
        device["memory_utilization_percent"] = 0.0
        device["power_draw_watts"] = 0.0
        device["temperature_celsius"] = 0.0
    else:
        raise HTTPException(status_code=400, detail="Invalid power state. Only 'ON', 'OFF', 'PowerOn', or 'PowerOff' are allowed.")
        
    import datetime
    device["updated_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S+05:30")
    # Need to save with the UUID, not the name
    db.upsert_item(collection_path, device["id"], device)
    return device

