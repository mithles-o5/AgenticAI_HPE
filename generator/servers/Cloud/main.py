import uuid
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import json
import os
from models import *

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from db_store import get_db_store

mock_file = os.path.join(os.path.dirname(__file__), "mock_data.json")
MOCK_DB = get_db_store("cloud", mock_file)

app = FastAPI(title='Generated Mock Server', description='Generated automatically from API docs.')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/v1/access-controls")
def get_access_controls():
    """
    Dynamic CRUD Route: GET /api/v1/access-controls
    """
    collection_path = f"/api/v1/access-controls"
    static_data = MOCK_DB.get("get_access_controls", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/audit-events")
def AuditEventsGet():
    """
    Dynamic CRUD Route: GET /api/v1/audit-events
    """
    collection_path = f"/api/v1/audit-events"
    static_data = MOCK_DB.get("AuditEventsGet", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/host-initiator-groups")
def HostGroupList():
    """
    Dynamic CRUD Route: GET /api/v1/host-initiator-groups
    """
    collection_path = f"/api/v1/host-initiator-groups"
    static_data = MOCK_DB.get("HostGroupList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.post("/api/v1/host-initiator-groups")
def HostGroupCreate(payload: HostgroupcreateRequest):
    """
    Dynamic CRUD Route: POST /api/v1/host-initiator-groups
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/host-initiator-groups"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.delete("/api/v1/host-initiator-groups/{hostGroupId}")
def HostGroupDelete(hostGroupId: str):
    """
    Dynamic CRUD Route: DELETE /api/v1/host-initiator-groups/{hostGroupId}
    """
    collection_path = f"/api/v1/host-initiator-groups"
    item_id = hostGroupId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        deleted = MOCK_DB["dynamic_store"][collection_path].pop(item_id)
        return {"message": "Deleted successfully", "id": item_id, "item": deleted}
    return MOCK_DB.get("HostGroupDelete", dict())

@app.get("/api/v1/host-initiator-groups/{hostGroupId}")
def HostGroupGetById(hostGroupId: str):
    """
    Dynamic CRUD Route: GET /api/v1/host-initiator-groups/{hostGroupId}
    """
    collection_path = f"/api/v1/host-initiator-groups"
    item_id = hostGroupId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("HostGroupGetById", dict())
    return static_val

@app.put("/api/v1/host-initiator-groups/{hostGroupId}")
def HostGroupUpdateById(hostGroupId: str, payload: HostgroupupdatebyidRequest):
    """
    Dynamic CRUD Route: PUT /api/v1/host-initiator-groups/{hostGroupId}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/host-initiator-groups"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    item_id = hostGroupId
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/host-initiator-groups/{hostGroupId}/mappedDevices")
def HostGroupMappedDevice(hostGroupId: str):
    """
    Dynamic CRUD Route: GET /api/v1/host-initiator-groups/{hostGroupId}/mappedDevices
    """
    collection_path = f"/api/v1/host-initiator-groups/{hostGroupId}/mappedDevices"
    static_data = MOCK_DB.get("HostGroupMappedDevice", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/host-initiator-groups/bulkmerge")
def findBulkMergeCandidatesForHostGroups():
    """
    Dynamic CRUD Route: GET /api/v1/host-initiator-groups/bulkmerge
    """
    collection_path = f"/api/v1/host-initiator-groups/bulkmerge"
    static_data = MOCK_DB.get("findBulkMergeCandidatesForHostGroups", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.post("/api/v1/host-initiator-groups/bulkmerge")
def BulkMergeHostGroup(payload: BulkmergehostgroupRequest):
    """
    Dynamic CRUD Route: POST /api/v1/host-initiator-groups/bulkmerge
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/host-initiator-groups/bulkmerge"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.post("/api/v1/host-initiator-groups/merge")
def HostGroupMerge(payload: HostgroupmergeRequest):
    """
    Dynamic CRUD Route: POST /api/v1/host-initiator-groups/merge
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/host-initiator-groups/merge"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/host-initiators")
def HostList():
    """
    Dynamic CRUD Route: GET /api/v1/host-initiators
    """
    collection_path = f"/api/v1/host-initiators"
    static_data = MOCK_DB.get("HostList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.post("/api/v1/host-initiators")
def HostCreate(payload: HostcreateRequest):
    """
    Dynamic CRUD Route: POST /api/v1/host-initiators
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/host-initiators"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.delete("/api/v1/host-initiators/{hostId}")
def HostDelete(hostId: str):
    """
    Dynamic CRUD Route: DELETE /api/v1/host-initiators/{hostId}
    """
    collection_path = f"/api/v1/host-initiators"
    item_id = hostId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        deleted = MOCK_DB["dynamic_store"][collection_path].pop(item_id)
        return {"message": "Deleted successfully", "id": item_id, "item": deleted}
    return MOCK_DB.get("HostDelete", dict())

@app.get("/api/v1/host-initiators/{hostId}")
def HostGetById(hostId: str):
    """
    Dynamic CRUD Route: GET /api/v1/host-initiators/{hostId}
    """
    collection_path = f"/api/v1/host-initiators"
    item_id = hostId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("HostGetById", dict())
    return static_val

@app.put("/api/v1/host-initiators/{hostId}")
def HostUpdateById(hostId: str, payload: HostupdatebyidRequest):
    """
    Dynamic CRUD Route: PUT /api/v1/host-initiators/{hostId}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/host-initiators"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    item_id = hostId
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/host-initiators/{hostId}/chap")
def GetHostChapById(hostId: str):
    """
    Dynamic CRUD Route: GET /api/v1/host-initiators/{hostId}/chap
    """
    collection_path = f"/api/v1/host-initiators/{hostId}/chap"
    static_data = MOCK_DB.get("GetHostChapById", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.put("/api/v1/host-initiators/{hostId}/chap")
def UpdateHostChapById(hostId: str, payload: UpdatehostchapbyidRequest):
    """
    Dynamic CRUD Route: PUT /api/v1/host-initiators/{hostId}/chap
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/host-initiators/{hostId}/chap"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})

    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.post("/api/v1/host-initiators/{hostId}/chapkey")
def GenerateChapKeyById(hostId: str, payload: GeneratechapkeybyidRequest):
    """
    Dynamic CRUD Route: POST /api/v1/host-initiators/{hostId}/chapkey
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/host-initiators/{hostId}/chapkey"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/host-initiators/{hostId}/mappedDevices")
def HostMappedDevice(hostId: str):
    """
    Dynamic CRUD Route: GET /api/v1/host-initiators/{hostId}/mappedDevices
    """
    collection_path = f"/api/v1/host-initiators/{hostId}/mappedDevices"
    static_data = MOCK_DB.get("HostMappedDevice", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/host-initiators/{hostId}/storage-performance-history")
def HostVolumePerformanceHistoryGet(hostId: str):
    """
    Dynamic CRUD Route: GET /api/v1/host-initiators/{hostId}/storage-performance-history
    """
    collection_path = f"/api/v1/host-initiators/{hostId}/storage-performance-history"
    static_data = MOCK_DB.get("HostVolumePerformanceHistoryGet", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/host-initiators/{hostId}/volumes")
def HostVolumesGet(hostId: str):
    """
    Dynamic CRUD Route: GET /api/v1/host-initiators/{hostId}/volumes
    """
    collection_path = f"/api/v1/host-initiators/{hostId}/volumes"
    static_data = MOCK_DB.get("HostVolumesGet", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/host-initiators/{hostId}/volumes-snapshots")
def HostMappedVolSnaps(hostId: str):
    """
    Dynamic CRUD Route: GET /api/v1/host-initiators/{hostId}/volumes-snapshots
    """
    collection_path = f"/api/v1/host-initiators/{hostId}/volumes-snapshots"
    static_data = MOCK_DB.get("HostMappedVolSnaps", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/host-initiators/bulkmerge")
def findBulkMergeCandidatesForHosts():
    """
    Dynamic CRUD Route: GET /api/v1/host-initiators/bulkmerge
    """
    collection_path = f"/api/v1/host-initiators/bulkmerge"
    static_data = MOCK_DB.get("findBulkMergeCandidatesForHosts", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.post("/api/v1/host-initiators/bulkmerge")
def BulkMergeHost(payload: BulkmergehostRequest):
    """
    Dynamic CRUD Route: POST /api/v1/host-initiators/bulkmerge
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/host-initiators/bulkmerge"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.post("/api/v1/host-initiators/merge")
def MergeHost(payload: MergehostRequest):
    """
    Dynamic CRUD Route: POST /api/v1/host-initiators/merge
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/host-initiators/merge"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/initiators")
def HostInitiatorList():
    """
    Dynamic CRUD Route: GET /api/v1/initiators
    """
    collection_path = f"/api/v1/initiators"
    static_data = MOCK_DB.get("HostInitiatorList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.post("/api/v1/initiators")
def HostInitiatorCreate(payload: HostinitiatorcreateRequest):
    """
    Dynamic CRUD Route: POST /api/v1/initiators
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/initiators"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.delete("/api/v1/initiators/{initiatorId}")
def HostInitiatorDelete(initiatorId: str):
    """
    Dynamic CRUD Route: DELETE /api/v1/initiators/{initiatorId}
    """
    collection_path = f"/api/v1/initiators"
    item_id = initiatorId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        deleted = MOCK_DB["dynamic_store"][collection_path].pop(item_id)
        return {"message": "Deleted successfully", "id": item_id, "item": deleted}
    return MOCK_DB.get("HostInitiatorDelete", dict())

@app.get("/api/v1/initiators/{initiatorId}")
def HostInitiatorGetById(initiatorId: str):
    """
    Dynamic CRUD Route: GET /api/v1/initiators/{initiatorId}
    """
    collection_path = f"/api/v1/initiators"
    item_id = initiatorId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("HostInitiatorGetById", dict())
    return static_val

@app.get("/api/v1/issues")
def ListIssues():
    """
    Dynamic CRUD Route: GET /api/v1/issues
    """
    collection_path = f"/api/v1/issues"
    static_data = MOCK_DB.get("ListIssues", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/issues/{id}")
def GetIssue(id: str):
    """
    Dynamic CRUD Route: GET /api/v1/issues/{id}
    """
    collection_path = f"/api/v1/issues"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("GetIssue", dict())
    return static_val

@app.get("/api/v1/resource-types")
def get_resource_types():
    """
    Dynamic CRUD Route: GET /api/v1/resource-types
    """
    collection_path = f"/api/v1/resource-types"
    static_data = MOCK_DB.get("get_resource_types", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems")
def SystemsList():
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems
    """
    collection_path = f"/api/v1/storage-systems"
    static_data = MOCK_DB.get("SystemsList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/{id}")
def SystemGetById(id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/{id}
    """
    collection_path = f"/api/v1/storage-systems"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("SystemGetById", dict())
    return static_val

@app.get("/api/v1/storage-systems/{systemId}/storage-pools")
def StoragePoolsList(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/{systemId}/storage-pools
    """
    collection_path = f"/api/v1/storage-systems/{systemId}/storage-pools"
    static_data = MOCK_DB.get("StoragePoolsList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/{systemId}/storage-pools/{id}")
def StoragePoolsGetById(systemId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/{systemId}/storage-pools/{id}
    """
    collection_path = f"/api/v1/storage-systems/{systemId}/storage-pools"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("StoragePoolsGetById", dict())
    return static_val

@app.get("/api/v1/storage-systems/{systemId}/storage-pools/{id}/volumes")
def StoragePoolVolumesList(systemId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/{systemId}/storage-pools/{id}/volumes
    """
    collection_path = f"/api/v1/storage-systems/{systemId}/storage-pools/{id}/volumes"
    static_data = MOCK_DB.get("StoragePoolVolumesList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/{systemId}/volume-sets")
def VolumesetListForSystemBySystemId(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/{systemId}/volume-sets
    """
    collection_path = f"/api/v1/storage-systems/{systemId}/volume-sets"
    static_data = MOCK_DB.get("VolumesetListForSystemBySystemId", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/{systemId}/volume-sets/{id}")
def VolumesetSystemGetById(systemId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/{systemId}/volume-sets/{id}
    """
    collection_path = f"/api/v1/storage-systems/{systemId}/volume-sets"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("VolumesetSystemGetById", dict())
    return static_val

@app.get("/api/v1/storage-systems/{systemId}/volumes")
def VolumeListForSystemBySystemId(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/{systemId}/volumes
    """
    collection_path = f"/api/v1/storage-systems/{systemId}/volumes"
    static_data = MOCK_DB.get("VolumeListForSystemBySystemId", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type1")
def DeviceType1SystemsList():
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1
    """
    collection_path = f"/api/v1/storage-systems/device-type1"
    static_data = MOCK_DB.get("DeviceType1SystemsList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type1/{id}")
def DeviceType1SystemGetById(id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{id}
    """
    collection_path = f"/api/v1/storage-systems/device-type1"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType1SystemGetById", dict())
    return static_val

@app.post("/api/v1/storage-systems/device-type1/{id}")
def SystemLocate(id: str, payload: SystemlocateRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type1/{id}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type1"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type1/{systemId}/alert-contacts")
def DeviceType1AlertContactsList(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/alert-contacts
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/alert-contacts"
    static_data = MOCK_DB.get("DeviceType1AlertContactsList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.post("/api/v1/storage-systems/device-type1/{systemId}/alert-contacts")
def AlertContactsCreate(systemId: str, payload: AlertcontactscreateRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type1/{systemId}/alert-contacts
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/alert-contacts"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.delete("/api/v1/storage-systems/device-type1/{systemId}/alert-contacts/{id}")
def AlertContactsDelete(systemId: str, id: str):
    """
    Dynamic CRUD Route: DELETE /api/v1/storage-systems/device-type1/{systemId}/alert-contacts/{id}
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/alert-contacts"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        deleted = MOCK_DB["dynamic_store"][collection_path].pop(item_id)
        return {"message": "Deleted successfully", "id": item_id, "item": deleted}
    return MOCK_DB.get("AlertContactsDelete", dict())

@app.get("/api/v1/storage-systems/device-type1/{systemId}/alert-contacts/{id}")
def DeviceType1AlertContactsGetById(systemId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/alert-contacts/{id}
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/alert-contacts"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType1AlertContactsGetById", dict())
    return static_val

@app.put("/api/v1/storage-systems/device-type1/{systemId}/alert-contacts/{id}")
def AlertContactsUpdate(systemId: str, id: str, payload: AlertcontactsupdateRequest):
    """
    Dynamic CRUD Route: PUT /api/v1/storage-systems/device-type1/{systemId}/alert-contacts/{id}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/alert-contacts"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    item_id = id
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type1/{systemId}/application-summary")
def DeviceType1ApplicationSummaryGet(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/application-summary
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/application-summary"
    static_data = MOCK_DB.get("DeviceType1ApplicationSummaryGet", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type1/{systemId}/applicationsets")
def DeviceType1VolumeSetsList(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/applicationsets
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/applicationsets"
    static_data = MOCK_DB.get("DeviceType1VolumeSetsList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.post("/api/v1/storage-systems/device-type1/{systemId}/applicationsets")
def DeviceType1VolumeSetsCreate(systemId: str, payload: Devicetype1volumesetscreateRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type1/{systemId}/applicationsets
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/applicationsets"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.post("/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{appsetId}/export")
def DeviceType1VolumeSetExport(systemId: str, appsetId: str, payload: Devicetype1volumesetexportRequest):
    return MOCK_DB.get("DeviceType1VolumeSetExport", dict())

@app.get("/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{appsetId}/replication-partners")
def DeviceType1GetReplicationPartnersByAppSetId(systemId: str, appsetId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/applicationsets/{appsetId}/replication-partners
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{appsetId}/replication-partners"
    static_data = MOCK_DB.get("DeviceType1GetReplicationPartnersByAppSetId", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{appsetId}/replication-partners/{replicationPartnerId}/volumes")
def DeviceType1GetReplicationPartnerVolumesByAppSetId(systemId: str, appsetId: str, replicationPartnerId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/applicationsets/{appsetId}/replication-partners/{replicationPartnerId}/volumes
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{appsetId}/replication-partners/{replicationPartnerId}/volumes"
    static_data = MOCK_DB.get("DeviceType1GetReplicationPartnerVolumesByAppSetId", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.delete("/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{appsetId}/snapsets/{snapsetId}")
def DeviceType1VolumeSetSnapshotDeleteById(systemId: str, appsetId: str, snapsetId: str):
    """
    Dynamic CRUD Route: DELETE /api/v1/storage-systems/device-type1/{systemId}/applicationsets/{appsetId}/snapsets/{snapsetId}
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{appsetId}/snapsets"
    item_id = snapsetId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        deleted = MOCK_DB["dynamic_store"][collection_path].pop(item_id)
        return {"message": "Deleted successfully", "id": item_id, "item": deleted}
    return MOCK_DB.get("DeviceType1VolumeSetSnapshotDeleteById", dict())

@app.get("/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{appsetId}/snapsets/{snapsetId}")
def DeviceType1SnapsetsGetById(systemId: str, appsetId: str, snapsetId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/applicationsets/{appsetId}/snapsets/{snapsetId}
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{appsetId}/snapsets"
    item_id = snapsetId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType1SnapsetsGetById", dict())
    return static_val

@app.post("/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{appsetId}/un-export")
def DeviceType1VolumeSetUnexport(systemId: str, appsetId: str, payload: Devicetype1volumesetunexportRequest):
    return MOCK_DB.get("DeviceType1VolumeSetUnexport", dict())

@app.get("/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{appsetId}/volumes")
def DeviceType1VolumeSetVolumesList(systemId: str, appsetId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/applicationsets/{appsetId}/volumes
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{appsetId}/volumes"
    static_data = MOCK_DB.get("DeviceType1VolumeSetVolumesList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.delete("/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}")
def DeviceType1VolumeSetsDeleteById(systemId: str, id: str):
    """
    Dynamic CRUD Route: DELETE /api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/applicationsets"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        deleted = MOCK_DB["dynamic_store"][collection_path].pop(item_id)
        return {"message": "Deleted successfully", "id": item_id, "item": deleted}
    return MOCK_DB.get("DeviceType1VolumeSetsDeleteById", dict())

@app.get("/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}")
def DeviceType1VolumeSetsGetById(systemId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/applicationsets"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType1VolumeSetsGetById", dict())
    return static_val

@app.put("/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}")
def DeviceType1VolumeSetsEditById(systemId: str, id: str, payload: Devicetype1volumesetseditbyidRequest):
    """
    Dynamic CRUD Route: PUT /api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/applicationsets"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    item_id = id
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}/capacity-statistics")
def DeviceType1VolumeSetCapacityStatisticsGetById(systemId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}/capacity-statistics
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}/capacity-statistics"
    static_data = MOCK_DB.get("DeviceType1VolumeSetCapacityStatisticsGetById", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}/performance")
def DeviceType1GetVolumeSetPerformanceHistory(systemId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}/performance
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}/performance"
    static_data = MOCK_DB.get("DeviceType1GetVolumeSetPerformanceHistory", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}/protection-policies")
def DeviceType1GetProtectionPolicies(systemId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}/protection-policies
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}/protection-policies"
    static_data = MOCK_DB.get("DeviceType1GetProtectionPolicies", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.post("/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}/protection-policies")
def DeviceType1CreateProtectionPolicy(systemId: str, id: str, payload: Devicetype1createprotectionpolicyRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}/protection-policies
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}/protection-policies"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.put("/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}/protection-policies")
def DeviceType1EditProtectionPolicies(systemId: str, id: str, payload: Devicetype1editprotectionpoliciesRequest):
    """
    Dynamic CRUD Route: PUT /api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}/protection-policies
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}/protection-policies"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})

    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.post("/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}/protection-policies/fix")
def DeviceType1FixProtectionPolicy(systemId: str, id: str, payload: Devicetype1fixprotectionpolicyRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}/protection-policies/fix
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}/protection-policies/fix"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.post("/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}/protection-policies/remove")
def DeviceType1removeProtectionPolicies(systemId: str, id: str, payload: Devicetype1removeprotectionpoliciesRequest):
    return MOCK_DB.get("DeviceType1removeProtectionPolicies", dict())

@app.get("/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}/proximity-settings")
def DeviceType1GetProximitySettings(systemId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}/proximity-settings
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}/proximity-settings"
    static_data = MOCK_DB.get("DeviceType1GetProximitySettings", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.put("/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}/proximity-settings")
def DeviceType1EditProximitySettings(systemId: str, id: str, payload: Devicetype1editproximitysettingsRequest):
    """
    Dynamic CRUD Route: PUT /api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}/proximity-settings
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}/proximity-settings"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})

    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.post("/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}/remote-protection/actions")
def DeviceType1actionOnVolumeSets(systemId: str, id: str, payload: Devicetype1actiononvolumesetsRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}/remote-protection/actions
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}/remote-protection/actions"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}/snapsets")
def DeviceType1VolumeSetSnapshotsList(systemId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}/snapsets
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}/snapsets"
    static_data = MOCK_DB.get("DeviceType1VolumeSetSnapshotsList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.post("/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}/snapsets")
def DeviceType1VolumeSetsSnapshotCreate(systemId: str, id: str, payload: Devicetype1volumesetssnapshotcreateRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}/snapsets
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}/snapsets"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}/supported-protection")
def DeviceType1getSupportedProtectionTypes(systemId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}/supported-protection
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}/supported-protection"
    static_data = MOCK_DB.get("DeviceType1getSupportedProtectionTypes", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type1/{systemId}/capacity-history")
def DeviceType1SystemCapacityHistoryGet(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/capacity-history
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/capacity-history"
    static_data = MOCK_DB.get("DeviceType1SystemCapacityHistoryGet", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type1/{systemId}/capacity-summary")
def DeviceType1SystemCapacitySummaryGet(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/capacity-summary
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/capacity-summary"
    static_data = MOCK_DB.get("DeviceType1SystemCapacitySummaryGet", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type1/{systemId}/certificates")
def DeviceType1CertificatesList(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/certificates
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/certificates"
    static_data = MOCK_DB.get("DeviceType1CertificatesList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.post("/api/v1/storage-systems/device-type1/{systemId}/certificates")
def PostCertificate(systemId: str, payload: PostcertificateRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type1/{systemId}/certificates
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/certificates"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type1/{systemId}/certificates/{id}")
def DeviceType1CertificatesGetById(systemId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/certificates/{id}
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/certificates"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType1CertificatesGetById", dict())
    return static_val

@app.put("/api/v1/storage-systems/device-type1/{systemId}/certificates/{id}")
def PutCertificate(systemId: str, id: str, payload: PutcertificateRequest):
    """
    Dynamic CRUD Route: PUT /api/v1/storage-systems/device-type1/{systemId}/certificates/{id}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/certificates"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    item_id = id
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.post("/api/v1/storage-systems/device-type1/{systemId}/certificates/remove")
def RemoveCertificates(systemId: str, payload: RemovecertificatesRequest):
    return MOCK_DB.get("RemoveCertificates", dict())

@app.post("/api/v1/storage-systems/device-type1/{systemId}/collect-support-data")
def DeviceType1SupportDataCollect(systemId: str):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type1/{systemId}/collect-support-data
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/collect-support-data"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = {}
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type1/{systemId}/component-performance-statistics")
def DeviceType1SystemComponentPerformanceStatisticsGet(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/component-performance-statistics
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/component-performance-statistics"
    static_data = MOCK_DB.get("DeviceType1SystemComponentPerformanceStatisticsGet", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type1/{systemId}/enclosures")
def DeviceType1EnclosuresList(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/enclosures
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/enclosures"
    static_data = MOCK_DB.get("DeviceType1EnclosuresList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type1/{systemId}/enclosures/{cageId}/disks")
def DeviceType1DisksList(systemId: str, cageId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/enclosures/{cageId}/disks
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/enclosures/{cageId}/disks"
    static_data = MOCK_DB.get("DeviceType1DisksList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type1/{systemId}/enclosures/{cageId}/disks/{id}")
def DeviceType1DisksGetById(systemId: str, cageId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/enclosures/{cageId}/disks/{id}
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/enclosures/{cageId}/disks"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType1DisksGetById", dict())
    return static_val

@app.get("/api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-card-ports")
def DeviceType1EnclosureCardPortsList(systemId: str, enclosureId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-card-ports
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-card-ports"
    static_data = MOCK_DB.get("DeviceType1EnclosureCardPortsList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-card-ports/{id}")
def DeviceType1EnclosureCardPortsGetById(systemId: str, enclosureId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-card-ports/{id}
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-card-ports"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType1EnclosureCardPortsGetById", dict())
    return static_val

@app.get("/api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-cards")
def DeviceType1EnclosureCardsList(systemId: str, enclosureId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-cards
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-cards"
    static_data = MOCK_DB.get("DeviceType1EnclosureCardsList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-cards/{id}")
def DeviceType1EnclosureCardsGetById(systemId: str, enclosureId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-cards/{id}
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-cards"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType1EnclosureCardsGetById", dict())
    return static_val

@app.post("/api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-cards/{id}")
def EnclosureCardsLocateIOById(systemId: str, enclosureId: str, id: str, payload: EnclosurecardslocateiobyidRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-cards/{id}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-cards"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-disks")
def DeviceType1EnclosureDisksList(systemId: str, enclosureId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-disks
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-disks"
    static_data = MOCK_DB.get("DeviceType1EnclosureDisksList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-disks/{id}")
def DeviceType1EnclosureDisksGetById(systemId: str, enclosureId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-disks/{id}
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-disks"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType1EnclosureDisksGetById", dict())
    return static_val

@app.get("/api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-expanders")
def DeviceType1EnclosureExpandersList(systemId: str, enclosureId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-expanders
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-expanders"
    static_data = MOCK_DB.get("DeviceType1EnclosureExpandersList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-expanders/{id}")
def DeviceType1EnclosureExpandersGetById(systemId: str, enclosureId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-expanders/{id}
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-expanders"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType1EnclosureExpandersGetById", dict())
    return static_val

@app.get("/api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-fans")
def DeviceType1EnclosureFansList(systemId: str, enclosureId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-fans
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-fans"
    static_data = MOCK_DB.get("DeviceType1EnclosureFansList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-fans/{id}")
def DeviceType1EnclosureFansGetById(systemId: str, enclosureId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-fans/{id}
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-fans"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType1EnclosureFansGetById", dict())
    return static_val

@app.get("/api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-powers")
def DeviceType1EnclosurePowersList(systemId: str, enclosureId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-powers
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-powers"
    static_data = MOCK_DB.get("DeviceType1EnclosurePowersList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-powers/{id}")
def DeviceType1EnclosurePowersGetById(systemId: str, enclosureId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-powers/{id}
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-powers"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType1EnclosurePowersGetById", dict())
    return static_val

@app.post("/api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-powers/{id}")
def EnclosurePowersLocatePCMById(systemId: str, enclosureId: str, id: str, payload: EnclosurepowerslocatepcmbyidRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-powers/{id}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-powers"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-sleds")
def DeviceType1EnclosureSledsList(systemId: str, enclosureId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-sleds
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-sleds"
    static_data = MOCK_DB.get("DeviceType1EnclosureSledsList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-sleds/{id}")
def DeviceType1EnclosureSledsGetById(systemId: str, enclosureId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-sleds/{id}
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-sleds"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType1EnclosureSledsGetById", dict())
    return static_val

@app.post("/api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-sleds/{id}")
def EnclosureSledsLocateDriveById(systemId: str, enclosureId: str, id: str, payload: EnclosuresledslocatedrivebyidRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-sleds/{id}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-sleds"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type1/{systemId}/enclosures/{id}")
def DeviceType1EnclosuresGetById(systemId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/enclosures/{id}
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/enclosures"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType1EnclosuresGetById", dict())
    return static_val

@app.post("/api/v1/storage-systems/device-type1/{systemId}/enclosures/{id}")
def EnclosuresLocateById(systemId: str, id: str, payload: EnclosureslocatebyidRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type1/{systemId}/enclosures/{id}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/enclosures"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.put("/api/v1/storage-systems/device-type1/{systemId}/enclosures/{id}")
def EnclosuresEditById(systemId: str, id: str, payload: EnclosureseditbyidRequest):
    """
    Dynamic CRUD Route: PUT /api/v1/storage-systems/device-type1/{systemId}/enclosures/{id}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/enclosures"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    item_id = id
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.post("/api/v1/storage-systems/device-type1/{systemId}/encryption/backup")
def DeviceType1backupActionOnEncryption(systemId: str, payload: Devicetype1backupactiononencryptionRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type1/{systemId}/encryption/backup
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/encryption/backup"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.post("/api/v1/storage-systems/device-type1/{systemId}/encryption/checkekm")
def DeviceType1checkEKMConfiguration(systemId: str):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type1/{systemId}/encryption/checkekm
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/encryption/checkekm"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = {}
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.post("/api/v1/storage-systems/device-type1/{systemId}/encryption/enable")
def DeviceType1enableActionOnEncryption(systemId: str, payload: Devicetype1enableactiononencryptionRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type1/{systemId}/encryption/enable
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/encryption/enable"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.post("/api/v1/storage-systems/device-type1/{systemId}/encryption/rekey")
def DeviceType1rekeyActionOnEncryption(systemId: str, payload: Devicetype1rekeyactiononencryptionRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type1/{systemId}/encryption/rekey
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/encryption/rekey"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.post("/api/v1/storage-systems/device-type1/{systemId}/encryption/restore")
def DeviceType1restoreActionOnEncryption(systemId: str, payload: Devicetype1restoreactiononencryptionRequest):
    return MOCK_DB.get("DeviceType1restoreActionOnEncryption", dict())

@app.post("/api/v1/storage-systems/device-type1/{systemId}/encryption/setekm")
def DeviceType1setEKMConfiguration(systemId: str, payload: Devicetype1setekmconfigurationRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type1/{systemId}/encryption/setekm
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/encryption/setekm"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.post("/api/v1/storage-systems/device-type1/{systemId}/encryption/setekm/backup")
def DeviceType1setekmbackupActionOnEncryption(systemId: str, payload: Devicetype1setekmbackupactiononencryptionRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type1/{systemId}/encryption/setekm/backup
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/encryption/setekm/backup"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type1/{systemId}/headroom-utilization")
def Device1headroomUtilizationGet(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/headroom-utilization
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/headroom-utilization"
    static_data = MOCK_DB.get("Device1headroomUtilizationGet", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type1/{systemId}/host-paths")
def DeviceType1GetAllHostPaths(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/host-paths
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/host-paths"
    static_data = MOCK_DB.get("DeviceType1GetAllHostPaths", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type1/{systemId}/host-paths/{hostPathId}")
def DeviceType1GetHostPathsById(systemId: str, hostPathId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/host-paths/{hostPathId}
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/host-paths"
    item_id = hostPathId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType1GetHostPathsById", dict())
    return static_val

@app.get("/api/v1/storage-systems/device-type1/{systemId}/host-sets")
def DeviceType1GetAllHostSets(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/host-sets
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/host-sets"
    static_data = MOCK_DB.get("DeviceType1GetAllHostSets", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type1/{systemId}/host-sets/{hostSetId}")
def DeviceType1GetHostSetsById(systemId: str, hostSetId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/host-sets/{hostSetId}
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/host-sets"
    item_id = hostSetId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType1GetHostSetsById", dict())
    return static_val

@app.get("/api/v1/storage-systems/device-type1/{systemId}/hosts")
def DeviceType1GetAllHosts(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/hosts
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/hosts"
    static_data = MOCK_DB.get("DeviceType1GetAllHosts", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type1/{systemId}/hosts/{hostId}")
def DeviceType1GetHostById(systemId: str, hostId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/hosts/{hostId}
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/hosts"
    item_id = hostId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType1GetHostById", dict())
    return static_val

@app.get("/api/v1/storage-systems/device-type1/{systemId}/insights/latencyfactors")
def Device1LatencyFactorsGet(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/insights/latencyfactors
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/insights/latencyfactors"
    static_data = MOCK_DB.get("Device1LatencyFactorsGet", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.delete("/api/v1/storage-systems/device-type1/{systemId}/mail-settings")
def MailSettingsDelete(systemId: str):
    """
    Dynamic CRUD Route: DELETE /api/v1/storage-systems/device-type1/{systemId}/mail-settings
    """
    return MOCK_DB.get("MailSettingsDelete", dict())

@app.get("/api/v1/storage-systems/device-type1/{systemId}/mail-settings")
def DeviceType1MailSettingsGet(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/mail-settings
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/mail-settings"
    static_data = MOCK_DB.get("DeviceType1MailSettingsGet", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.post("/api/v1/storage-systems/device-type1/{systemId}/mail-settings")
def MailSettingsAssociate(systemId: str, payload: MailsettingsassociateRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type1/{systemId}/mail-settings
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/mail-settings"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.put("/api/v1/storage-systems/device-type1/{systemId}/mail-settings")
def MailSettingsUpdate(systemId: str, payload: MailsettingsupdateRequest):
    """
    Dynamic CRUD Route: PUT /api/v1/storage-systems/device-type1/{systemId}/mail-settings
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/mail-settings"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})

    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type1/{systemId}/network-services/cim")
def DeviceType1NetworkServiceCimGet(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/network-services/cim
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/network-services/cim"
    static_data = MOCK_DB.get("DeviceType1NetworkServiceCimGet", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.put("/api/v1/storage-systems/device-type1/{systemId}/network-services/cim")
def NetworkServiceCimUpdate(systemId: str, payload: NetworkservicecimupdateRequest):
    """
    Dynamic CRUD Route: PUT /api/v1/storage-systems/device-type1/{systemId}/network-services/cim
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/network-services/cim"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})

    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type1/{systemId}/network-services/snmp-mgr")
def DeviceType1NetworkServiceSnmpMgrList(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/network-services/snmp-mgr
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/network-services/snmp-mgr"
    static_data = MOCK_DB.get("DeviceType1NetworkServiceSnmpMgrList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.post("/api/v1/storage-systems/device-type1/{systemId}/network-services/snmp-mgr")
def NetworkServiceSnmpMgrCreate(systemId: str, payload: NetworkservicesnmpmgrcreateRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type1/{systemId}/network-services/snmp-mgr
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/network-services/snmp-mgr"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.delete("/api/v1/storage-systems/device-type1/{systemId}/network-services/snmp-mgr/{id}")
def NetworkServiceSnmpMgrDelete(systemId: str, id: str):
    """
    Dynamic CRUD Route: DELETE /api/v1/storage-systems/device-type1/{systemId}/network-services/snmp-mgr/{id}
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/network-services/snmp-mgr"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        deleted = MOCK_DB["dynamic_store"][collection_path].pop(item_id)
        return {"message": "Deleted successfully", "id": item_id, "item": deleted}
    return MOCK_DB.get("NetworkServiceSnmpMgrDelete", dict())

@app.get("/api/v1/storage-systems/device-type1/{systemId}/network-services/snmp-mgr/{id}")
def DeviceType1NetworkServiceSnmpMgrGetById(systemId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/network-services/snmp-mgr/{id}
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/network-services/snmp-mgr"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType1NetworkServiceSnmpMgrGetById", dict())
    return static_val

@app.put("/api/v1/storage-systems/device-type1/{systemId}/network-services/snmp-mgr/{id}")
def NetworkServiceSnmpMgrUpdate(systemId: str, id: str, payload: NetworkservicesnmpmgrupdateRequest):
    """
    Dynamic CRUD Route: PUT /api/v1/storage-systems/device-type1/{systemId}/network-services/snmp-mgr/{id}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/network-services/snmp-mgr"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    item_id = id
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type1/{systemId}/network-services/vasa")
def DeviceType1NetworkServiceVasaGet(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/network-services/vasa
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/network-services/vasa"
    static_data = MOCK_DB.get("DeviceType1NetworkServiceVasaGet", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.post("/api/v1/storage-systems/device-type1/{systemId}/network-services/vasa/{vasaId}")
def DeviceType1NetworkServiceVasaConfigure(systemId: str, vasaId: str, payload: Devicetype1networkservicevasaconfigureRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type1/{systemId}/network-services/vasa/{vasaId}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/network-services/vasa"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.post("/api/v1/storage-systems/device-type1/{systemId}/network-services/vasa/{vasaId}/services")
def DeviceType1NetworkServiceConfigureVasaService(systemId: str, vasaId: str, payload: Devicetype1networkserviceconfigurevasaserviceRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type1/{systemId}/network-services/vasa/{vasaId}/services
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/network-services/vasa/{vasaId}/services"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type1/{systemId}/network-settings")
def DeviceType1NetworkSettingsGet(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/network-settings
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/network-settings"
    static_data = MOCK_DB.get("DeviceType1NetworkSettingsGet", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.post("/api/v1/storage-systems/device-type1/{systemId}/network-settings")
def NetworkSettingsAssociate(systemId: str, payload: NetworksettingsassociateRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type1/{systemId}/network-settings
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/network-settings"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type1/{systemId}/nodes")
def DeviceType1NodesList(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/nodes
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/nodes"
    static_data = MOCK_DB.get("DeviceType1NodesList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type1/{systemId}/nodes/{id}")
def DeviceType1NodesGetById(systemId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/nodes/{id}
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/nodes"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType1NodesGetById", dict())
    return static_val

@app.post("/api/v1/storage-systems/device-type1/{systemId}/nodes/{id}")
def NodesLocateById(systemId: str, id: str, payload: NodeslocatebyidRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type1/{systemId}/nodes/{id}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/nodes"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/component-performance-statistics")
def DeviceType1NodeComponentPerformanceStatisticsGet(systemId: str, nodeId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/component-performance-statistics
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/component-performance-statistics"
    static_data = MOCK_DB.get("DeviceType1NodeComponentPerformanceStatisticsGet", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/node-cards")
def DeviceType1NodeCardsList(systemId: str, nodeId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/node-cards
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/node-cards"
    static_data = MOCK_DB.get("DeviceType1NodeCardsList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/node-cards/{id}")
def DeviceType1NodeCardsGetById(systemId: str, nodeId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/node-cards/{id}
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/node-cards"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType1NodeCardsGetById", dict())
    return static_val

@app.post("/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/node-cards/{id}")
def NodeCardLocateById(systemId: str, nodeId: str, id: str, payload: NodecardlocatebyidRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/node-cards/{id}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/node-cards"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/node-cpus")
def DeviceType1NodeCpusList(systemId: str, nodeId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/node-cpus
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/node-cpus"
    static_data = MOCK_DB.get("DeviceType1NodeCpusList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/node-cpus/{id}")
def DeviceType1NodeCpusGetById(systemId: str, nodeId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/node-cpus/{id}
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/node-cpus"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType1NodeCpusGetById", dict())
    return static_val

@app.get("/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/node-drives")
def DeviceType1NodeDrivesList(systemId: str, nodeId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/node-drives
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/node-drives"
    static_data = MOCK_DB.get("DeviceType1NodeDrivesList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/node-drives/{id}")
def DeviceType1NodeDrivesGetById(systemId: str, nodeId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/node-drives/{id}
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/node-drives"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType1NodeDrivesGetById", dict())
    return static_val

@app.get("/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/node-mcus")
def DeviceType1NodeMcusList(systemId: str, nodeId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/node-mcus
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/node-mcus"
    static_data = MOCK_DB.get("DeviceType1NodeMcusList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/node-mcus/{id}")
def DeviceType1NodeMcusGetById(systemId: str, nodeId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/node-mcus/{id}
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/node-mcus"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType1NodeMcusGetById", dict())
    return static_val

@app.get("/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/node-mems")
def DeviceType1NodeMemsList(systemId: str, nodeId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/node-mems
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/node-mems"
    static_data = MOCK_DB.get("DeviceType1NodeMemsList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/node-mems/{id}")
def DeviceType1NodeMemsGetById(systemId: str, nodeId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/node-mems/{id}
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/node-mems"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType1NodeMemsGetById", dict())
    return static_val

@app.get("/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/node-powers")
def DeviceType1NodePowersList(systemId: str, nodeId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/node-powers
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/node-powers"
    static_data = MOCK_DB.get("DeviceType1NodePowersList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/node-powers/{id}")
def DeviceType1NodePowersGetById(systemId: str, nodeId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/node-powers/{id}
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/node-powers"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType1NodePowersGetById", dict())
    return static_val

@app.post("/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/node-powers/{id}")
def NodePowersLocatePCMBById(systemId: str, nodeId: str, id: str, payload: NodepowerslocatepcmbbyidRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/node-powers/{id}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/node-powers"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/nodes-batteries")
def DeviceType1NodeBatteriesList(systemId: str, nodeId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/nodes-batteries
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/nodes-batteries"
    static_data = MOCK_DB.get("DeviceType1NodeBatteriesList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/nodes-batteries/{id}")
def DeviceType1NodeBatteriesGetById(systemId: str, nodeId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/nodes-batteries/{id}
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/nodes-batteries"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType1NodeBatteriesGetById", dict())
    return static_val

@app.get("/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/service-ports")
def DeviceType1NodeServicePortsGetById(systemId: str, nodeId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/service-ports
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/service-ports"
    static_data = MOCK_DB.get("DeviceType1NodeServicePortsGetById", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type1/{systemId}/nodes/service-ports")
def DeviceType1NodeServicePortsList(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/nodes/service-ports
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/nodes/service-ports"
    static_data = MOCK_DB.get("DeviceType1NodeServicePortsList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type1/{systemId}/performance-history")
def DeviceType1SystemPerformanceHistoryGet(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/performance-history
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/performance-history"
    static_data = MOCK_DB.get("DeviceType1SystemPerformanceHistoryGet", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type1/{systemId}/performance-statistics")
def DeviceType1GetSystemPerformanceStatistics(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/performance-statistics
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/performance-statistics"
    static_data = MOCK_DB.get("DeviceType1GetSystemPerformanceStatistics", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type1/{systemId}/physicaldrives-performance")
def DeviceType1PhysicalDrivePerformanceHistoryGet(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/physicaldrives-performance
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/physicaldrives-performance"
    static_data = MOCK_DB.get("DeviceType1PhysicalDrivePerformanceHistoryGet", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type1/{systemId}/ports")
def DeviceType1PortsList(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/ports
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/ports"
    static_data = MOCK_DB.get("DeviceType1PortsList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type1/{systemId}/ports-performance")
def DeviceType1PortsPerformanceHistoryGet(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/ports-performance
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/ports-performance"
    static_data = MOCK_DB.get("DeviceType1PortsPerformanceHistoryGet", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type1/{systemId}/ports/{id}")
def DeviceType1PortsGetById(systemId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/ports/{id}
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/ports"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType1PortsGetById", dict())
    return static_val

@app.post("/api/v1/storage-systems/device-type1/{systemId}/ports/{id}")
def PortEnable(systemId: str, id: str, payload: PortenableRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type1/{systemId}/ports/{id}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/ports"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.post("/api/v1/storage-systems/device-type1/{systemId}/ports/{id}/clear")
def DeviceType1PortsClear(systemId: str, id: str, payload: Devicetype1portsclearRequest):
    return MOCK_DB.get("DeviceType1PortsClear", dict())

@app.put("/api/v1/storage-systems/device-type1/{systemId}/ports/{id}/edit-iscsi")
def DeviceType1IscsiPortEdit(systemId: str, id: str, payload: Devicetype1iscsiporteditRequest):
    """
    Dynamic CRUD Route: PUT /api/v1/storage-systems/device-type1/{systemId}/ports/{id}/edit-iscsi
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/ports/{id}/edit-iscsi"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})

    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.put("/api/v1/storage-systems/device-type1/{systemId}/ports/{id}/edit-rcip")
def DeviceType1RcipPortEdit(systemId: str, id: str, payload: Devicetype1rcipporteditRequest):
    """
    Dynamic CRUD Route: PUT /api/v1/storage-systems/device-type1/{systemId}/ports/{id}/edit-rcip
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/ports/{id}/edit-rcip"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})

    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.put("/api/v1/storage-systems/device-type1/{systemId}/ports/{id}/fc")
def DeviceType1FcPortEdit(systemId: str, id: str, payload: Devicetype1fcporteditRequest):
    """
    Dynamic CRUD Route: PUT /api/v1/storage-systems/device-type1/{systemId}/ports/{id}/fc
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/ports/{id}/fc"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})

    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.post("/api/v1/storage-systems/device-type1/{systemId}/ports/{id}/initialize")
def initialisePorts(systemId: str, id: str):
    return MOCK_DB.get("initialisePorts", dict())

@app.post("/api/v1/storage-systems/device-type1/{systemId}/ports/{id}/ping-iscsi")
def DeviceType1IscsiPortPing(systemId: str, id: str, payload: Devicetype1iscsiportpingRequest):
    return MOCK_DB.get("DeviceType1IscsiPortPing", dict())

@app.post("/api/v1/storage-systems/device-type1/{systemId}/ports/{id}/ping-rcip")
def DeviceType1RcipPortPing(systemId: str, id: str, payload: Devicetype1rcipportpingRequest):
    return MOCK_DB.get("DeviceType1RcipPortPing", dict())

@app.get("/api/v1/storage-systems/device-type1/{systemId}/qos-policy")
def DeviceType1QoSPolicyGetBySystemId(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/qos-policy
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/qos-policy"
    static_data = MOCK_DB.get("DeviceType1QoSPolicyGetBySystemId", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type1/{systemId}/remotecopylinks-performance")
def DeviceType1RemoteCopyLinksPerformanceHistoryGet(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/remotecopylinks-performance
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/remotecopylinks-performance"
    static_data = MOCK_DB.get("DeviceType1RemoteCopyLinksPerformanceHistoryGet", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.post("/api/v1/storage-systems/device-type1/{systemId}/snapshots/{snapshotId}/clone")
def SnapshotCloneCreate(systemId: str, snapshotId: str, payload: SnapshotclonecreateRequest):
    return MOCK_DB.get("SnapshotCloneCreate", dict())

@app.post("/api/v1/storage-systems/device-type1/{systemId}/snapshots/{snapshotId}/export")
def DeviceType1VlunExportForSnapshot(systemId: str, snapshotId: str, payload: Devicetype1vlunexportforsnapshotRequest):
    return MOCK_DB.get("DeviceType1VlunExportForSnapshot", dict())

@app.post("/api/v1/storage-systems/device-type1/{systemId}/snapshots/{snapshotId}/un-export")
def DeviceType1VlunUnexportForSnapshot(systemId: str, snapshotId: str, payload: Devicetype1vlununexportforsnapshotRequest):
    return MOCK_DB.get("DeviceType1VlunUnexportForSnapshot", dict())

@app.get("/api/v1/storage-systems/device-type1/{systemId}/snapshots/{snapshotId}/vluns")
def DeviceType1GetSnapshotVlunsList(systemId: str, snapshotId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/snapshots/{snapshotId}/vluns
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/snapshots/{snapshotId}/vluns"
    static_data = MOCK_DB.get("DeviceType1GetSnapshotVlunsList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type1/{systemId}/snapshots/{snapshotId}/vluns/{id}")
def DeviceType1GetSnapshotVlunsById(systemId: str, snapshotId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/snapshots/{snapshotId}/vluns/{id}
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/snapshots/{snapshotId}/vluns"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType1GetSnapshotVlunsById", dict())
    return static_val

@app.get("/api/v1/storage-systems/device-type1/{systemId}/storage-pools")
def DeviceType1StoragePoolList(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/storage-pools
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/storage-pools"
    static_data = MOCK_DB.get("DeviceType1StoragePoolList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type1/{systemId}/storage-pools/{id}")
def DeviceType1StoragePoolGetById(systemId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/storage-pools/{id}
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/storage-pools"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType1StoragePoolGetById", dict())
    return static_val

@app.get("/api/v1/storage-systems/device-type1/{systemId}/storage-pools/{id}/volumes")
def DeviceType1StoragePoolVolumeGetById(systemId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/storage-pools/{id}/volumes
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/storage-pools/{id}/volumes"
    static_data = MOCK_DB.get("DeviceType1StoragePoolVolumeGetById", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type1/{systemId}/support-settings")
def DeviceType1SupportSettingsGet(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/support-settings
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/support-settings"
    static_data = MOCK_DB.get("DeviceType1SupportSettingsGet", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.post("/api/v1/storage-systems/device-type1/{systemId}/support-settings")
def SupportSettingsAssociate(systemId: str, payload: SupportsettingsassociateRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type1/{systemId}/support-settings
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/support-settings"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.put("/api/v1/storage-systems/device-type1/{systemId}/support-settings")
def SupportSettingsUpdate(systemId: str, payload: SupportsettingsupdateRequest):
    """
    Dynamic CRUD Route: PUT /api/v1/storage-systems/device-type1/{systemId}/support-settings
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/support-settings"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})

    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type1/{systemId}/system-settings")
def DeviceType1SystemSettingsList(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/system-settings
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/system-settings"
    static_data = MOCK_DB.get("DeviceType1SystemSettingsList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.post("/api/v1/storage-systems/device-type1/{systemId}/system-settings")
def SystemSettingsAssociate(systemId: str, payload: SystemsettingsassociateRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type1/{systemId}/system-settings
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/system-settings"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.put("/api/v1/storage-systems/device-type1/{systemId}/system-settings")
def SystemSettingsUpdate(systemId: str, payload: SystemsettingsupdateRequest):
    """
    Dynamic CRUD Route: PUT /api/v1/storage-systems/device-type1/{systemId}/system-settings
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/system-settings"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})

    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type1/{systemId}/system-settings/management-services/vvolscs")
def DeviceType1StorageContainerGet(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/system-settings/management-services/vvolscs
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/system-settings/management-services/vvolscs"
    static_data = MOCK_DB.get("DeviceType1StorageContainerGet", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.post("/api/v1/storage-systems/device-type1/{systemId}/system-settings/management-services/vvolscs")
def DeviceType1CreatevVolSC(systemId: str, payload: Devicetype1createvvolscRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type1/{systemId}/system-settings/management-services/vvolscs
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/system-settings/management-services/vvolscs"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.delete("/api/v1/storage-systems/device-type1/{systemId}/system-settings/management-services/vvolscs/{vvolscId}")
def DeviceType1StorageContainerDeleteById(systemId: str, vvolscId: str):
    """
    Dynamic CRUD Route: DELETE /api/v1/storage-systems/device-type1/{systemId}/system-settings/management-services/vvolscs/{vvolscId}
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/system-settings/management-services/vvolscs"
    item_id = vvolscId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        deleted = MOCK_DB["dynamic_store"][collection_path].pop(item_id)
        return {"message": "Deleted successfully", "id": item_id, "item": deleted}
    return MOCK_DB.get("DeviceType1StorageContainerDeleteById", dict())

@app.put("/api/v1/storage-systems/device-type1/{systemId}/system-settings/management-services/vvolscs/{vvolscId}")
def DeviceType1EditVolSC(systemId: str, vvolscId: str, payload: Devicetype1editvolscRequest):
    """
    Dynamic CRUD Route: PUT /api/v1/storage-systems/device-type1/{systemId}/system-settings/management-services/vvolscs/{vvolscId}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/system-settings/management-services/vvolscs"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    item_id = vvolscId
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.post("/api/v1/storage-systems/device-type1/{systemId}/system-settings/management-services/vvolscs/{vvolscId}/attach")
def DeviceType1AttachDetachVolSC(systemId: str, vvolscId: str, payload: Devicetype1attachdetachvolscRequest):
    return MOCK_DB.get("DeviceType1AttachDetachVolSC", dict())

@app.get("/api/v1/storage-systems/device-type1/{systemId}/system-settings/quorum-witness")
def DeviceType1GetQuorumWitness(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/system-settings/quorum-witness
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/system-settings/quorum-witness"
    static_data = MOCK_DB.get("DeviceType1GetQuorumWitness", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.post("/api/v1/storage-systems/device-type1/{systemId}/system-settings/quorum-witness")
def DeviceType1PostQuorumWitness(systemId: str, payload: Devicetype1postquorumwitnessRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type1/{systemId}/system-settings/quorum-witness
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/system-settings/quorum-witness"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.delete("/api/v1/storage-systems/device-type1/{systemId}/system-settings/quorum-witness/{replicationPartnerId}")
def DeviceType1DeleteQuorumWitness(systemId: str, replicationPartnerId: str):
    """
    Dynamic CRUD Route: DELETE /api/v1/storage-systems/device-type1/{systemId}/system-settings/quorum-witness/{replicationPartnerId}
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/system-settings/quorum-witness"
    item_id = replicationPartnerId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        deleted = MOCK_DB["dynamic_store"][collection_path].pop(item_id)
        return {"message": "Deleted successfully", "id": item_id, "item": deleted}
    return MOCK_DB.get("DeviceType1DeleteQuorumWitness", dict())

@app.get("/api/v1/storage-systems/device-type1/{systemId}/system-settings/quorum-witness/{replicationPartnerId}")
def DeviceType1GetQuorumWitnessWithId(systemId: str, replicationPartnerId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/system-settings/quorum-witness/{replicationPartnerId}
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/system-settings/quorum-witness"
    item_id = replicationPartnerId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType1GetQuorumWitnessWithId", dict())
    return static_val

@app.put("/api/v1/storage-systems/device-type1/{systemId}/system-settings/quorum-witness/{replicationPartnerId}")
def DeviceType1PutQuorumWitness(systemId: str, replicationPartnerId: str, payload: Devicetype1putquorumwitnessRequest):
    """
    Dynamic CRUD Route: PUT /api/v1/storage-systems/device-type1/{systemId}/system-settings/quorum-witness/{replicationPartnerId}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/system-settings/quorum-witness"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    item_id = replicationPartnerId
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type1/{systemId}/system-settings/replication-partners")
def DeviceType1GetReplicationPartners(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/system-settings/replication-partners
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/system-settings/replication-partners"
    static_data = MOCK_DB.get("DeviceType1GetReplicationPartners", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.post("/api/v1/storage-systems/device-type1/{systemId}/system-settings/replication-partners")
def DeviceType1PostReplicationPartners(systemId: str, payload: Devicetype1postreplicationpartnersRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type1/{systemId}/system-settings/replication-partners
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/system-settings/replication-partners"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type1/{systemId}/system-settings/replication-partners/{replicationPartnerId}")
def DeviceType1GetReplicationPartnerWithId(systemId: str, replicationPartnerId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/system-settings/replication-partners/{replicationPartnerId}
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/system-settings/replication-partners"
    item_id = replicationPartnerId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType1GetReplicationPartnerWithId", dict())
    return static_val

@app.put("/api/v1/storage-systems/device-type1/{systemId}/system-settings/replication-partners/{replicationPartnerId}")
def DeviceType1PutReplicationPartner(systemId: str, replicationPartnerId: str, payload: Devicetype1putreplicationpartnerRequest):
    """
    Dynamic CRUD Route: PUT /api/v1/storage-systems/device-type1/{systemId}/system-settings/replication-partners/{replicationPartnerId}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/system-settings/replication-partners"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    item_id = replicationPartnerId
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.post("/api/v1/storage-systems/device-type1/{systemId}/system-settings/replication-partners/remove")
def DeviceType1PostRemoveReplicationPartners(systemId: str, payload: Devicetype1postremovereplicationpartnersRequest):
    return MOCK_DB.get("DeviceType1PostRemoveReplicationPartners", dict())

@app.get("/api/v1/storage-systems/device-type1/{systemId}/targets/{targetName}/performance-history")
def DeviceType1QoSPerformanceStatisticsGetByTargetName(systemId: str, targetName: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/targets/{targetName}/performance-history
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/targets/{targetName}/performance-history"
    static_data = MOCK_DB.get("DeviceType1QoSPerformanceStatisticsGetByTargetName", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type1/{systemId}/telemetry")
def DeviceType1TelemetryGet(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/telemetry
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/telemetry"
    static_data = MOCK_DB.get("DeviceType1TelemetryGet", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type1/{systemId}/trust-certificates")
def DeviceType1TrustedCertificatesList(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/trust-certificates
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/trust-certificates"
    static_data = MOCK_DB.get("DeviceType1TrustedCertificatesList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.post("/api/v1/storage-systems/device-type1/{systemId}/trust-certificates")
def AddTrustedCertificates(systemId: str, payload: AddtrustedcertificatesRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type1/{systemId}/trust-certificates
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/trust-certificates"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type1/{systemId}/trust-certificates/{id}")
def DeviceType1TrustedCertificatesGetById(systemId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/trust-certificates/{id}
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/trust-certificates"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType1TrustedCertificatesGetById", dict())
    return static_val

@app.post("/api/v1/storage-systems/device-type1/{systemId}/trust-certificates/remove")
def RemoveTrustedCertificates(systemId: str, payload: RemovetrustedcertificatesRequest):
    return MOCK_DB.get("RemoveTrustedCertificates", dict())

@app.get("/api/v1/storage-systems/device-type1/{systemId}/vm-manager-settings")
def DeviceType1VMManagerSettingsList(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/vm-manager-settings
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/vm-manager-settings"
    static_data = MOCK_DB.get("DeviceType1VMManagerSettingsList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.post("/api/v1/storage-systems/device-type1/{systemId}/vm-manager-settings")
def DeviceType1PostVCenterSettings(systemId: str, payload: Devicetype1postvcentersettingsRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type1/{systemId}/vm-manager-settings
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/vm-manager-settings"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.delete("/api/v1/storage-systems/device-type1/{systemId}/vm-manager-settings/{vcenterSettingId}")
def DeviceType1DeleteVCenterSettings(systemId: str, vcenterSettingId: str):
    """
    Dynamic CRUD Route: DELETE /api/v1/storage-systems/device-type1/{systemId}/vm-manager-settings/{vcenterSettingId}
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/vm-manager-settings"
    item_id = vcenterSettingId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        deleted = MOCK_DB["dynamic_store"][collection_path].pop(item_id)
        return {"message": "Deleted successfully", "id": item_id, "item": deleted}
    return MOCK_DB.get("DeviceType1DeleteVCenterSettings", dict())

@app.get("/api/v1/storage-systems/device-type1/{systemId}/vm-manager-settings/{vcenterSettingId}")
def DeviceType1VMManagerSettingsGetById(systemId: str, vcenterSettingId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/vm-manager-settings/{vcenterSettingId}
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/vm-manager-settings"
    item_id = vcenterSettingId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType1VMManagerSettingsGetById", dict())
    return static_val

@app.put("/api/v1/storage-systems/device-type1/{systemId}/vm-manager-settings/{vcenterSettingId}")
def DeviceType1PutVCenterSettings(systemId: str, vcenterSettingId: str, payload: Devicetype1putvcentersettingsRequest):
    """
    Dynamic CRUD Route: PUT /api/v1/storage-systems/device-type1/{systemId}/vm-manager-settings/{vcenterSettingId}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/vm-manager-settings"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    item_id = vcenterSettingId
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type1/{systemId}/volumes")
def DeviceType1VolumesList(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/volumes
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/volumes"
    static_data = MOCK_DB.get("DeviceType1VolumesList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.post("/api/v1/storage-systems/device-type1/{systemId}/volumes")
def VolumeCreate(systemId: str, payload: VolumecreateRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type1/{systemId}/volumes
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/volumes"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type1/{systemId}/volumes-performance")
def DeviceType1GetVolumesPerformanceHistory(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/volumes-performance
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/volumes-performance"
    static_data = MOCK_DB.get("DeviceType1GetVolumesPerformanceHistory", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.delete("/api/v1/storage-systems/device-type1/{systemId}/volumes/{id}")
def VolumeDelete(systemId: str, id: str):
    """
    Dynamic CRUD Route: DELETE /api/v1/storage-systems/device-type1/{systemId}/volumes/{id}
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/volumes"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        deleted = MOCK_DB["dynamic_store"][collection_path].pop(item_id)
        return {"message": "Deleted successfully", "id": item_id, "item": deleted}
    return MOCK_DB.get("VolumeDelete", dict())

@app.get("/api/v1/storage-systems/device-type1/{systemId}/volumes/{id}")
def DeviceType1VolumeGetById(systemId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/volumes/{id}
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/volumes"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType1VolumeGetById", dict())
    return static_val

@app.put("/api/v1/storage-systems/device-type1/{systemId}/volumes/{id}")
def VolumeEdit(systemId: str, id: str, payload: VolumeeditRequest):
    """
    Dynamic CRUD Route: PUT /api/v1/storage-systems/device-type1/{systemId}/volumes/{id}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/volumes"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    item_id = id
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type1/{systemId}/volumes/{id}/capacity-history")
def DeviceType1VolumeCapacityHistoryGetById(systemId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/volumes/{id}/capacity-history
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/volumes/{id}/capacity-history"
    static_data = MOCK_DB.get("DeviceType1VolumeCapacityHistoryGetById", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.post("/api/v1/storage-systems/device-type1/{systemId}/volumes/{id}/clone")
def VolumeCloneCreate(systemId: str, id: str, payload: VolumeclonecreateRequest):
    return MOCK_DB.get("VolumeCloneCreate", dict())

@app.post("/api/v1/storage-systems/device-type1/{systemId}/volumes/{id}/export")
def DeviceType1VlunExport(systemId: str, id: str, payload: Devicetype1vlunexportRequest):
    return MOCK_DB.get("DeviceType1VlunExport", dict())

@app.get("/api/v1/storage-systems/device-type1/{systemId}/volumes/{id}/performance-history")
def DeviceType1VolumePerformanceHistoryGetById(systemId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/volumes/{id}/performance-history
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/volumes/{id}/performance-history"
    static_data = MOCK_DB.get("DeviceType1VolumePerformanceHistoryGetById", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type1/{systemId}/volumes/{id}/performance-statistics")
def DeviceType1VolumePerformanceStatisticsGetById(systemId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/volumes/{id}/performance-statistics
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/volumes/{id}/performance-statistics"
    static_data = MOCK_DB.get("DeviceType1VolumePerformanceStatisticsGetById", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type1/{systemId}/volumes/{id}/snapshots")
def DeviceType1VolumeSnapshotsList(systemId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/volumes/{id}/snapshots
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/volumes/{id}/snapshots"
    static_data = MOCK_DB.get("DeviceType1VolumeSnapshotsList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.post("/api/v1/storage-systems/device-type1/{systemId}/volumes/{id}/snapshots")
def VolumeSnapshotCreate(systemId: str, id: str, payload: VolumesnapshotcreateRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type1/{systemId}/volumes/{id}/snapshots
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/volumes/{id}/snapshots"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.post("/api/v1/storage-systems/device-type1/{systemId}/volumes/{id}/un-export")
def DeviceType1VlunUnexport(systemId: str, id: str, payload: Devicetype1vlununexportRequest):
    return MOCK_DB.get("DeviceType1VlunUnexport", dict())

@app.get("/api/v1/storage-systems/device-type1/{systemId}/volumes/{id}/vluns")
def DeviceType1VlunsList(systemId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/volumes/{id}/vluns
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/volumes/{id}/vluns"
    static_data = MOCK_DB.get("DeviceType1VlunsList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type1/{systemId}/volumes/{volumeId}/clones")
def DeviceType1GetClones(systemId: str, volumeId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/volumes/{volumeId}/clones
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/volumes/{volumeId}/clones"
    static_data = MOCK_DB.get("DeviceType1GetClones", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.post("/api/v1/storage-systems/device-type1/{systemId}/volumes/{volumeId}/clones/{cloneId}/promote")
def DeviceType1PromoteCloneVolume(systemId: str, volumeId: str, cloneId: str, payload: Devicetype1promoteclonevolumeRequest):
    return MOCK_DB.get("DeviceType1PromoteCloneVolume", dict())

@app.post("/api/v1/storage-systems/device-type1/{systemId}/volumes/{volumeId}/clones/{cloneId}/resync")
def DeviceType1ResyncCloneVolume(systemId: str, volumeId: str, cloneId: str, payload: Devicetype1resyncclonevolumeRequest):
    return MOCK_DB.get("DeviceType1ResyncCloneVolume", dict())

@app.delete("/api/v1/storage-systems/device-type1/{systemId}/volumes/{volumeId}/snapshots/{snapshotId}")
def VolumeSnapshotGetById(systemId: str, volumeId: str, snapshotId: str):
    """
    Dynamic CRUD Route: DELETE /api/v1/storage-systems/device-type1/{systemId}/volumes/{volumeId}/snapshots/{snapshotId}
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/volumes/{volumeId}/snapshots"
    item_id = snapshotId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        deleted = MOCK_DB["dynamic_store"][collection_path].pop(item_id)
        return {"message": "Deleted successfully", "id": item_id, "item": deleted}
    return MOCK_DB.get("VolumeSnapshotGetById", dict())

@app.get("/api/v1/storage-systems/device-type1/{systemId}/volumes/{volumeId}/snapshots/{snapshotId}")
def DeviceType1SnapshotsGetById(systemId: str, volumeId: str, snapshotId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/volumes/{volumeId}/snapshots/{snapshotId}
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/volumes/{volumeId}/snapshots"
    item_id = snapshotId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType1SnapshotsGetById", dict())
    return static_val

@app.post("/api/v1/storage-systems/device-type1/{systemId}/volumes/{volumeId}/snapshots/{snapshotId}")
def DeviceType1PromoteSnapshot(systemId: str, volumeId: str, snapshotId: str, payload: Devicetype1promotesnapshotRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type1/{systemId}/volumes/{volumeId}/snapshots/{snapshotId}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/volumes/{volumeId}/snapshots"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.delete("/api/v1/storage-systems/device-type1/{systemId}/volumes/{volumeId}/vluns/{id}")
def VlunsDelete(systemId: str, volumeId: str, id: str):
    """
    Dynamic CRUD Route: DELETE /api/v1/storage-systems/device-type1/{systemId}/volumes/{volumeId}/vluns/{id}
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/volumes/{volumeId}/vluns"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        deleted = MOCK_DB["dynamic_store"][collection_path].pop(item_id)
        return {"message": "Deleted successfully", "id": item_id, "item": deleted}
    return MOCK_DB.get("VlunsDelete", dict())

@app.get("/api/v1/storage-systems/device-type1/{systemId}/volumes/{volumeId}/vluns/{id}")
def DeviceType1VlunsGetById(systemId: str, volumeId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type1/{systemId}/volumes/{volumeId}/vluns/{id}
    """
    collection_path = f"/api/v1/storage-systems/device-type1/{systemId}/volumes/{volumeId}/vluns"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType1VlunsGetById", dict())
    return static_val

@app.get("/api/v1/storage-systems/device-type2")
def DeviceType2GetStorageSystem():
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2
    """
    collection_path = f"/api/v1/storage-systems/device-type2"
    static_data = MOCK_DB.get("DeviceType2GetStorageSystem", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type2/{systemId}")
def DeviceType2GetStorageSystemById(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}
    """
    collection_path = f"/api/v1/storage-systems/device-type2"
    item_id = systemId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType2GetStorageSystemById", dict())
    return static_val

@app.put("/api/v1/storage-systems/device-type2/{systemId}")
def DeviceType2EditStorageSystemSettingsById(systemId: str, payload: Devicetype2editstoragesystemsettingsbyidRequest):
    """
    Dynamic CRUD Route: PUT /api/v1/storage-systems/device-type2/{systemId}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type2"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    item_id = systemId
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type2/{systemId}/access-control-records")
def DeviceType2GetAllAccessControlRecords(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}/access-control-records
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/access-control-records"
    static_data = MOCK_DB.get("DeviceType2GetAllAccessControlRecords", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.post("/api/v1/storage-systems/device-type2/{systemId}/access-control-records")
def DeviceType2AccessControlRecordCreate(systemId: str, payload: Devicetype2accesscontrolrecordcreateRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type2/{systemId}/access-control-records
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/access-control-records"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.delete("/api/v1/storage-systems/device-type2/{systemId}/access-control-records/{accessControlRecordId}")
def DeviceType2RemoveAccessControlRecordById(systemId: str, accessControlRecordId: str):
    """
    Dynamic CRUD Route: DELETE /api/v1/storage-systems/device-type2/{systemId}/access-control-records/{accessControlRecordId}
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/access-control-records"
    item_id = accessControlRecordId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        deleted = MOCK_DB["dynamic_store"][collection_path].pop(item_id)
        return {"message": "Deleted successfully", "id": item_id, "item": deleted}
    return MOCK_DB.get("DeviceType2RemoveAccessControlRecordById", dict())

@app.get("/api/v1/storage-systems/device-type2/{systemId}/access-control-records/{accessControlRecordId}")
def DeviceType2GetAccessControlRecordById(systemId: str, accessControlRecordId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}/access-control-records/{accessControlRecordId}
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/access-control-records"
    item_id = accessControlRecordId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType2GetAccessControlRecordById", dict())
    return static_val

@app.put("/api/v1/storage-systems/device-type2/{systemId}/access-control-records/{accessControlRecordId}")
def DeviceType2EditAccessControlRecordById(systemId: str, accessControlRecordId: str, payload: Devicetype2editaccesscontrolrecordbyidRequest):
    """
    Dynamic CRUD Route: PUT /api/v1/storage-systems/device-type2/{systemId}/access-control-records/{accessControlRecordId}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/access-control-records"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    item_id = accessControlRecordId
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.post("/api/v1/storage-systems/device-type2/{systemId}/actions/merge")
def DeviceType2MergeGroups(systemId: str, payload: Devicetype2mergegroupsRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type2/{systemId}/actions/merge
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/actions/merge"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type2/{systemId}/alarms")
def DeviceType2GetAlarms(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}/alarms
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/alarms"
    static_data = MOCK_DB.get("DeviceType2GetAlarms", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type2/{systemId}/alarms/{alarmId}")
def DeviceType2GetAlarmsUsingAlarmId(systemId: str, alarmId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}/alarms/{alarmId}
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/alarms"
    item_id = alarmId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType2GetAlarmsUsingAlarmId", dict())
    return static_val

@app.get("/api/v1/storage-systems/device-type2/{systemId}/application-servers")
def DeviceType2GetAllApplicationServers(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}/application-servers
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/application-servers"
    static_data = MOCK_DB.get("DeviceType2GetAllApplicationServers", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.post("/api/v1/storage-systems/device-type2/{systemId}/application-servers")
def DeviceType2ApplicationServerCreate(systemId: str, payload: Devicetype2applicationservercreateRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type2/{systemId}/application-servers
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/application-servers"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.delete("/api/v1/storage-systems/device-type2/{systemId}/application-servers/{applicationServerId}")
def DeviceType2RemoveApplicationServerById(systemId: str, applicationServerId: str):
    """
    Dynamic CRUD Route: DELETE /api/v1/storage-systems/device-type2/{systemId}/application-servers/{applicationServerId}
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/application-servers"
    item_id = applicationServerId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        deleted = MOCK_DB["dynamic_store"][collection_path].pop(item_id)
        return {"message": "Deleted successfully", "id": item_id, "item": deleted}
    return MOCK_DB.get("DeviceType2RemoveApplicationServerById", dict())

@app.get("/api/v1/storage-systems/device-type2/{systemId}/application-servers/{applicationServerId}")
def DeviceType2GetApplicationServerById(systemId: str, applicationServerId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}/application-servers/{applicationServerId}
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/application-servers"
    item_id = applicationServerId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType2GetApplicationServerById", dict())
    return static_val

@app.put("/api/v1/storage-systems/device-type2/{systemId}/application-servers/{applicationServerId}")
def DeviceType2ApplicationServerEdit(systemId: str, applicationServerId: str, payload: Devicetype2applicationservereditRequest):
    """
    Dynamic CRUD Route: PUT /api/v1/storage-systems/device-type2/{systemId}/application-servers/{applicationServerId}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/application-servers"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    item_id = applicationServerId
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type2/{systemId}/application-summary")
def DeviceType2GetApplicationSummary(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}/application-summary
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/application-summary"
    static_data = MOCK_DB.get("DeviceType2GetApplicationSummary", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type2/{systemId}/applications/{id}/capacity-stats")
def DeviceType2GetApplicationCapacityStatisticsById(systemId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}/applications/{id}/capacity-stats
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/applications/{id}/capacity-stats"
    static_data = MOCK_DB.get("DeviceType2GetApplicationCapacityStatisticsById", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type2/{systemId}/applications/capacity-stats")
def DeviceType2GetApplicationsCapacityStatistics(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}/applications/capacity-stats
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/applications/capacity-stats"
    static_data = MOCK_DB.get("DeviceType2GetApplicationsCapacityStatistics", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type2/{systemId}/arrays")
def GetDeviceType2Arrays(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}/arrays
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/arrays"
    static_data = MOCK_DB.get("GetDeviceType2Arrays", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.post("/api/v1/storage-systems/device-type2/{systemId}/arrays")
def DeviceType2CreateArray(systemId: str, payload: Devicetype2createarrayRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type2/{systemId}/arrays
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/arrays"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.delete("/api/v1/storage-systems/device-type2/{systemId}/arrays/{arrayId}")
def DeviceType2DeleteArrayById(systemId: str, arrayId: str):
    """
    Dynamic CRUD Route: DELETE /api/v1/storage-systems/device-type2/{systemId}/arrays/{arrayId}
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/arrays"
    item_id = arrayId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        deleted = MOCK_DB["dynamic_store"][collection_path].pop(item_id)
        return {"message": "Deleted successfully", "id": item_id, "item": deleted}
    return MOCK_DB.get("DeviceType2DeleteArrayById", dict())

@app.get("/api/v1/storage-systems/device-type2/{systemId}/arrays/{arrayId}")
def GetDeviceType2ArrayById(systemId: str, arrayId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}/arrays/{arrayId}
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/arrays"
    item_id = arrayId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("GetDeviceType2ArrayById", dict())
    return static_val

@app.put("/api/v1/storage-systems/device-type2/{systemId}/arrays/{arrayId}")
def DeviceType2EditArrayById(systemId: str, arrayId: str, payload: Devicetype2editarraybyidRequest):
    """
    Dynamic CRUD Route: PUT /api/v1/storage-systems/device-type2/{systemId}/arrays/{arrayId}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/arrays"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    item_id = arrayId
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.post("/api/v1/storage-systems/device-type2/{systemId}/arrays/{arrayId}/actions/failover")
def DeviceType2ArrayFailover(systemId: str, arrayId: str, payload: Devicetype2arrayfailoverRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type2/{systemId}/arrays/{arrayId}/actions/failover
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/arrays/{arrayId}/actions/failover"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.post("/api/v1/storage-systems/device-type2/{systemId}/autosupport/actions/send")
def DeviceType2SendAutoSupport(systemId: str):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type2/{systemId}/autosupport/actions/send
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/autosupport/actions/send"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = {}
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type2/{systemId}/capacity-history")
def DeviceType2GetStorageSystemCapacityHistory(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}/capacity-history
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/capacity-history"
    static_data = MOCK_DB.get("DeviceType2GetStorageSystemCapacityHistory", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type2/{systemId}/controllers")
def DeviceType2GetAllControllers(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}/controllers
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/controllers"
    static_data = MOCK_DB.get("DeviceType2GetAllControllers", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type2/{systemId}/controllers/{controllerId}")
def DeviceType2GetControllerById(systemId: str, controllerId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}/controllers/{controllerId}
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/controllers"
    item_id = controllerId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType2GetControllerById", dict())
    return static_val

@app.post("/api/v1/storage-systems/device-type2/{systemId}/controllers/{controllerId}/actions/halt")
def DeviceType2ControllerHalt(systemId: str, controllerId: str):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type2/{systemId}/controllers/{controllerId}/actions/halt
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/controllers/{controllerId}/actions/halt"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = {}
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type2/{systemId}/disks")
def DeviceType2GetAllDisks(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}/disks
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/disks"
    static_data = MOCK_DB.get("DeviceType2GetAllDisks", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type2/{systemId}/disks/{diskId}")
def DeviceType2GetDiskById(systemId: str, diskId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}/disks/{diskId}
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/disks"
    item_id = diskId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType2GetDiskById", dict())
    return static_val

@app.put("/api/v1/storage-systems/device-type2/{systemId}/disks/{diskId}")
def DeviceType2DiskEdit(systemId: str, diskId: str, payload: Devicetype2diskeditRequest):
    """
    Dynamic CRUD Route: PUT /api/v1/storage-systems/device-type2/{systemId}/disks/{diskId}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/disks"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    item_id = diskId
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type2/{systemId}/events")
def DeviceType2GetEvents(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}/events
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/events"
    static_data = MOCK_DB.get("DeviceType2GetEvents", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type2/{systemId}/events/{eventId}")
def DeviceType2GetEventsUsingEventId(systemId: str, eventId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}/events/{eventId}
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/events"
    item_id = eventId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType2GetEventsUsingEventId", dict())
    return static_val

@app.get("/api/v1/storage-systems/device-type2/{systemId}/external-key-manager")
def DeviceType2GetExternalKeyManager(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}/external-key-manager
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/external-key-manager"
    static_data = MOCK_DB.get("DeviceType2GetExternalKeyManager", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.post("/api/v1/storage-systems/device-type2/{systemId}/external-key-manager")
def DeviceType2CreateExternalKeyManager(systemId: str, payload: Devicetype2createexternalkeymanagerRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type2/{systemId}/external-key-manager
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/external-key-manager"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.delete("/api/v1/storage-systems/device-type2/{systemId}/external-key-manager/{externalKeyManagerId}")
def DeviceType2DeleteExternalKeyManagerById(systemId: str, externalKeyManagerId: str):
    """
    Dynamic CRUD Route: DELETE /api/v1/storage-systems/device-type2/{systemId}/external-key-manager/{externalKeyManagerId}
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/external-key-manager"
    item_id = externalKeyManagerId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        deleted = MOCK_DB["dynamic_store"][collection_path].pop(item_id)
        return {"message": "Deleted successfully", "id": item_id, "item": deleted}
    return MOCK_DB.get("DeviceType2DeleteExternalKeyManagerById", dict())

@app.get("/api/v1/storage-systems/device-type2/{systemId}/external-key-manager/{externalKeyManagerId}")
def DeviceType2GetExternalKeyManagerById(systemId: str, externalKeyManagerId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}/external-key-manager/{externalKeyManagerId}
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/external-key-manager"
    item_id = externalKeyManagerId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType2GetExternalKeyManagerById", dict())
    return static_val

@app.put("/api/v1/storage-systems/device-type2/{systemId}/external-key-manager/{externalKeyManagerId}")
def DeviceType2EditExternalKeyManagerById(systemId: str, externalKeyManagerId: str, payload: Devicetype2editexternalkeymanagerbyidRequest):
    """
    Dynamic CRUD Route: PUT /api/v1/storage-systems/device-type2/{systemId}/external-key-manager/{externalKeyManagerId}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/external-key-manager"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    item_id = externalKeyManagerId
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.post("/api/v1/storage-systems/device-type2/{systemId}/external-key-manager/{externalKeyManagerId}/actions/migrate")
def DeviceType2MigrateExternalKeyManagerById(systemId: str, externalKeyManagerId: str):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type2/{systemId}/external-key-manager/{externalKeyManagerId}/actions/migrate
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/external-key-manager/{externalKeyManagerId}/actions/migrate"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = {}
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.post("/api/v1/storage-systems/device-type2/{systemId}/external-key-manager/{externalKeyManagerId}/actions/remove")
def DeviceType2RemoveExternalKeyManagerById(systemId: str, externalKeyManagerId: str, payload: Devicetype2removeexternalkeymanagerbyidRequest):
    return MOCK_DB.get("DeviceType2RemoveExternalKeyManagerById", dict())

@app.get("/api/v1/storage-systems/device-type2/{systemId}/fibre-channel-configs")
def DeviceType2GetAllFibreChannelConfigs(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}/fibre-channel-configs
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/fibre-channel-configs"
    static_data = MOCK_DB.get("DeviceType2GetAllFibreChannelConfigs", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type2/{systemId}/fibre-channel-configs/{fcConfigId}")
def DeviceType2GetFibreChannelConfigById(systemId: str, fcConfigId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}/fibre-channel-configs/{fcConfigId}
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/fibre-channel-configs"
    item_id = fcConfigId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType2GetFibreChannelConfigById", dict())
    return static_val

@app.get("/api/v1/storage-systems/device-type2/{systemId}/fibre-channel-interfaces")
def GetDeviceType2FibreChannelInterfaces(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}/fibre-channel-interfaces
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/fibre-channel-interfaces"
    static_data = MOCK_DB.get("GetDeviceType2FibreChannelInterfaces", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type2/{systemId}/fibre-channel-sessions")
def DeviceType2GetAllFibreChannelSessions(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}/fibre-channel-sessions
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/fibre-channel-sessions"
    static_data = MOCK_DB.get("DeviceType2GetAllFibreChannelSessions", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type2/{systemId}/fibre-channel-sessions/{fcSessionId}")
def DeviceType2GetFibreChannelSessionById(systemId: str, fcSessionId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}/fibre-channel-sessions/{fcSessionId}
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/fibre-channel-sessions"
    item_id = fcSessionId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType2GetFibreChannelSessionById", dict())
    return static_val

@app.get("/api/v1/storage-systems/device-type2/{systemId}/folders")
def DeviceType2GetAllFolders(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}/folders
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/folders"
    static_data = MOCK_DB.get("DeviceType2GetAllFolders", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.post("/api/v1/storage-systems/device-type2/{systemId}/folders")
def DeviceType2FolderCreate(systemId: str, payload: Devicetype2foldercreateRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type2/{systemId}/folders
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/folders"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.delete("/api/v1/storage-systems/device-type2/{systemId}/folders/{folderId}")
def DeviceType2RemoveFolderById(systemId: str, folderId: str):
    """
    Dynamic CRUD Route: DELETE /api/v1/storage-systems/device-type2/{systemId}/folders/{folderId}
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/folders"
    item_id = folderId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        deleted = MOCK_DB["dynamic_store"][collection_path].pop(item_id)
        return {"message": "Deleted successfully", "id": item_id, "item": deleted}
    return MOCK_DB.get("DeviceType2RemoveFolderById", dict())

@app.get("/api/v1/storage-systems/device-type2/{systemId}/folders/{folderId}")
def DeviceType2GetFolderById(systemId: str, folderId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}/folders/{folderId}
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/folders"
    item_id = folderId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType2GetFolderById", dict())
    return static_val

@app.put("/api/v1/storage-systems/device-type2/{systemId}/folders/{folderId}")
def DeviceType2FolderEdit(systemId: str, folderId: str, payload: Devicetype2foldereditRequest):
    """
    Dynamic CRUD Route: PUT /api/v1/storage-systems/device-type2/{systemId}/folders/{folderId}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/folders"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    item_id = folderId
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.post("/api/v1/storage-systems/device-type2/{systemId}/folders/{folderId}/attach")
def DeviceType2AttachDetachVvolbyID(systemId: str, folderId: str, payload: Devicetype2attachdetachvvolbyidRequest):
    return MOCK_DB.get("DeviceType2AttachDetachVvolbyID", dict())

@app.get("/api/v1/storage-systems/device-type2/{systemId}/health-status")
def DeviceType2GetHealthStatus(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}/health-status
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/health-status"
    static_data = MOCK_DB.get("DeviceType2GetHealthStatus", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type2/{systemId}/health-status/{healthStatusId}")
def DeviceType2GetHealthStatusUsingHealthId(systemId: str, healthStatusId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}/health-status/{healthStatusId}
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/health-status"
    item_id = healthStatusId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType2GetHealthStatusUsingHealthId", dict())
    return static_val

@app.get("/api/v1/storage-systems/device-type2/{systemId}/host-groups")
def DeviceType2GetAllHostInitiatorGroups(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}/host-groups
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/host-groups"
    static_data = MOCK_DB.get("DeviceType2GetAllHostInitiatorGroups", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.post("/api/v1/storage-systems/device-type2/{systemId}/host-groups")
def DeviceType2HostInitiatorGroupCreate(systemId: str, payload: Devicetype2hostinitiatorgroupcreateRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type2/{systemId}/host-groups
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/host-groups"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.delete("/api/v1/storage-systems/device-type2/{systemId}/host-groups/{hostInitiatorGroupId}")
def DeviceType2RemoveHostInitiatorGroupById(systemId: str, hostInitiatorGroupId: str):
    """
    Dynamic CRUD Route: DELETE /api/v1/storage-systems/device-type2/{systemId}/host-groups/{hostInitiatorGroupId}
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/host-groups"
    item_id = hostInitiatorGroupId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        deleted = MOCK_DB["dynamic_store"][collection_path].pop(item_id)
        return {"message": "Deleted successfully", "id": item_id, "item": deleted}
    return MOCK_DB.get("DeviceType2RemoveHostInitiatorGroupById", dict())

@app.get("/api/v1/storage-systems/device-type2/{systemId}/host-groups/{hostInitiatorGroupId}")
def DeviceType2GetHostInitiatorGroupById(systemId: str, hostInitiatorGroupId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}/host-groups/{hostInitiatorGroupId}
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/host-groups"
    item_id = hostInitiatorGroupId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType2GetHostInitiatorGroupById", dict())
    return static_val

@app.put("/api/v1/storage-systems/device-type2/{systemId}/host-groups/{hostInitiatorGroupId}")
def DeviceType2UpdateHostInitiatorGroupById(systemId: str, hostInitiatorGroupId: str, payload: Devicetype2updatehostinitiatorgroupbyidRequest):
    """
    Dynamic CRUD Route: PUT /api/v1/storage-systems/device-type2/{systemId}/host-groups/{hostInitiatorGroupId}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/host-groups"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    item_id = hostInitiatorGroupId
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type2/{systemId}/host-initiators")
def DeviceType2GetAllInitiators(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}/host-initiators
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/host-initiators"
    static_data = MOCK_DB.get("DeviceType2GetAllInitiators", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.post("/api/v1/storage-systems/device-type2/{systemId}/host-initiators")
def DeviceType2InitiatorsCreate(systemId: str, payload: Devicetype2initiatorscreateRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type2/{systemId}/host-initiators
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/host-initiators"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.delete("/api/v1/storage-systems/device-type2/{systemId}/host-initiators/{hostInitiatorId}")
def DeviceType2RemoveInitiatorsById(systemId: str, hostInitiatorId: str):
    """
    Dynamic CRUD Route: DELETE /api/v1/storage-systems/device-type2/{systemId}/host-initiators/{hostInitiatorId}
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/host-initiators"
    item_id = hostInitiatorId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        deleted = MOCK_DB["dynamic_store"][collection_path].pop(item_id)
        return {"message": "Deleted successfully", "id": item_id, "item": deleted}
    return MOCK_DB.get("DeviceType2RemoveInitiatorsById", dict())

@app.get("/api/v1/storage-systems/device-type2/{systemId}/host-initiators/{hostInitiatorId}")
def DeviceType2GetInitiatorsById(systemId: str, hostInitiatorId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}/host-initiators/{hostInitiatorId}
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/host-initiators"
    item_id = hostInitiatorId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType2GetInitiatorsById", dict())
    return static_val

@app.get("/api/v1/storage-systems/device-type2/{systemId}/local-key-manager")
def DeviceType2GetLocalKeyManager(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}/local-key-manager
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/local-key-manager"
    static_data = MOCK_DB.get("DeviceType2GetLocalKeyManager", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.post("/api/v1/storage-systems/device-type2/{systemId}/local-key-manager")
def DeviceType2CreateLocalKeyManager(systemId: str, payload: Devicetype2createlocalkeymanagerRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type2/{systemId}/local-key-manager
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/local-key-manager"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.delete("/api/v1/storage-systems/device-type2/{systemId}/local-key-manager/{localKeyManagerId}")
def DeviceType2DeleteLocalKeyManagerById(systemId: str, localKeyManagerId: str):
    """
    Dynamic CRUD Route: DELETE /api/v1/storage-systems/device-type2/{systemId}/local-key-manager/{localKeyManagerId}
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/local-key-manager"
    item_id = localKeyManagerId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        deleted = MOCK_DB["dynamic_store"][collection_path].pop(item_id)
        return {"message": "Deleted successfully", "id": item_id, "item": deleted}
    return MOCK_DB.get("DeviceType2DeleteLocalKeyManagerById", dict())

@app.get("/api/v1/storage-systems/device-type2/{systemId}/local-key-manager/{localKeyManagerId}")
def DeviceType2GetLocalKeyManagerById(systemId: str, localKeyManagerId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}/local-key-manager/{localKeyManagerId}
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/local-key-manager"
    item_id = localKeyManagerId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType2GetLocalKeyManagerById", dict())
    return static_val

@app.put("/api/v1/storage-systems/device-type2/{systemId}/local-key-manager/{localKeyManagerId}")
def DeviceType2EditLocalKeyManagerById(systemId: str, localKeyManagerId: str, payload: Devicetype2editlocalkeymanagerbyidRequest):
    """
    Dynamic CRUD Route: PUT /api/v1/storage-systems/device-type2/{systemId}/local-key-manager/{localKeyManagerId}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/local-key-manager"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    item_id = localKeyManagerId
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.put("/api/v1/storage-systems/device-type2/{systemId}/mail-settings")
def DeviceType2EditMailSettings(systemId: str, payload: Devicetype2editmailsettingsRequest):
    """
    Dynamic CRUD Route: PUT /api/v1/storage-systems/device-type2/{systemId}/mail-settings
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/mail-settings"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})

    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type2/{systemId}/network-interfaces")
def GetDeviceType2NetworkInterfaces(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}/network-interfaces
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/network-interfaces"
    static_data = MOCK_DB.get("GetDeviceType2NetworkInterfaces", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type2/{systemId}/network-interfaces/{networkInterfaceId}")
def GetDeviceType2NetworkInterfaceById(systemId: str, networkInterfaceId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}/network-interfaces/{networkInterfaceId}
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/network-interfaces"
    item_id = networkInterfaceId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("GetDeviceType2NetworkInterfaceById", dict())
    return static_val

@app.get("/api/v1/storage-systems/device-type2/{systemId}/network-settings")
def DeviceType2GetAllNetworkSettings(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}/network-settings
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/network-settings"
    static_data = MOCK_DB.get("DeviceType2GetAllNetworkSettings", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type2/{systemId}/network-settings/{networkSettingId}")
def DeviceType2GetNetworkSettingById(systemId: str, networkSettingId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}/network-settings/{networkSettingId}
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/network-settings"
    item_id = networkSettingId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType2GetNetworkSettingById", dict())
    return static_val

@app.put("/api/v1/storage-systems/device-type2/{systemId}/network-settings/{networkSettingId}")
def DeviceType2EditNetworkSettingById(systemId: str, networkSettingId: str, payload: Devicetype2editnetworksettingbyidRequest):
    """
    Dynamic CRUD Route: PUT /api/v1/storage-systems/device-type2/{systemId}/network-settings/{networkSettingId}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/network-settings"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    item_id = networkSettingId
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type2/{systemId}/performance-history")
def DeviceType2GetStorageSystemPerformanceHistory(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}/performance-history
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/performance-history"
    static_data = MOCK_DB.get("DeviceType2GetStorageSystemPerformanceHistory", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type2/{systemId}/performance-policies")
def DeviceType2GetAllPerformancePolicies(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}/performance-policies
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/performance-policies"
    static_data = MOCK_DB.get("DeviceType2GetAllPerformancePolicies", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.post("/api/v1/storage-systems/device-type2/{systemId}/performance-policies")
def DeviceType2PerformancePolicyCreate(systemId: str, payload: Devicetype2performancepolicycreateRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type2/{systemId}/performance-policies
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/performance-policies"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.delete("/api/v1/storage-systems/device-type2/{systemId}/performance-policies/{performancePolicyId}")
def DeviceType2RemovePerfPolicyId(systemId: str, performancePolicyId: str):
    """
    Dynamic CRUD Route: DELETE /api/v1/storage-systems/device-type2/{systemId}/performance-policies/{performancePolicyId}
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/performance-policies"
    item_id = performancePolicyId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        deleted = MOCK_DB["dynamic_store"][collection_path].pop(item_id)
        return {"message": "Deleted successfully", "id": item_id, "item": deleted}
    return MOCK_DB.get("DeviceType2RemovePerfPolicyId", dict())

@app.get("/api/v1/storage-systems/device-type2/{systemId}/performance-policies/{performancePolicyId}")
def DeviceType2GetPerformancePolicyById(systemId: str, performancePolicyId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}/performance-policies/{performancePolicyId}
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/performance-policies"
    item_id = performancePolicyId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType2GetPerformancePolicyById", dict())
    return static_val

@app.put("/api/v1/storage-systems/device-type2/{systemId}/performance-policies/{performancePolicyId}")
def DeviceType2PerformancePolicyEdit(systemId: str, performancePolicyId: str, payload: Devicetype2performancepolicyeditRequest):
    """
    Dynamic CRUD Route: PUT /api/v1/storage-systems/device-type2/{systemId}/performance-policies/{performancePolicyId}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/performance-policies"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    item_id = performancePolicyId
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type2/{systemId}/pools-performance")
def DeviceType2GetPoolsPerformanceHistory(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}/pools-performance
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/pools-performance"
    static_data = MOCK_DB.get("DeviceType2GetPoolsPerformanceHistory", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type2/{systemId}/ports")
def DeviceType2GetAllPorts(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}/ports
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/ports"
    static_data = MOCK_DB.get("DeviceType2GetAllPorts", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type2/{systemId}/ports/{portId}")
def DeviceType2GetPortById(systemId: str, portId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}/ports/{portId}
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/ports"
    item_id = portId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType2GetPortById", dict())
    return static_val

@app.put("/api/v1/storage-systems/device-type2/{systemId}/ports/{portId}")
def DeviceType2EditFCPort(systemId: str, portId: str, payload: Devicetype2editfcportRequest):
    """
    Dynamic CRUD Route: PUT /api/v1/storage-systems/device-type2/{systemId}/ports/{portId}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/ports"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    item_id = portId
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type2/{systemId}/protection-templates")
def DeviceType2GetAllProtectionTemplates(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}/protection-templates
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/protection-templates"
    static_data = MOCK_DB.get("DeviceType2GetAllProtectionTemplates", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.post("/api/v1/storage-systems/device-type2/{systemId}/protection-templates")
def DeviceType2CreateProtectionTemplate(systemId: str, payload: Devicetype2createprotectiontemplateRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type2/{systemId}/protection-templates
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/protection-templates"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type2/{systemId}/protection-templates/{protectionTemplateId}")
def DeviceType2GetProtectionTemplateById(systemId: str, protectionTemplateId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}/protection-templates/{protectionTemplateId}
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/protection-templates"
    item_id = protectionTemplateId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType2GetProtectionTemplateById", dict())
    return static_val

@app.put("/api/v1/storage-systems/device-type2/{systemId}/protection-templates/{protectionTemplateId}")
def DeviceType2EditProtectionTemplate(systemId: str, protectionTemplateId: str, payload: Devicetype2editprotectiontemplateRequest):
    """
    Dynamic CRUD Route: PUT /api/v1/storage-systems/device-type2/{systemId}/protection-templates/{protectionTemplateId}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/protection-templates"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    item_id = protectionTemplateId
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.post("/api/v1/storage-systems/device-type2/{systemId}/protection-templates/remove")
def DeviceType2RemoveProtectionTemplate(systemId: str, payload: Devicetype2removeprotectiontemplateRequest):
    return MOCK_DB.get("DeviceType2RemoveProtectionTemplate", dict())

@app.post("/api/v1/storage-systems/device-type2/{systemId}/provisioning")
def DeviceType2ProvisioningWorklow(systemId: str, payload: Devicetype2provisioningworklowRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type2/{systemId}/provisioning
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/provisioning"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.post("/api/v1/storage-systems/device-type2/{systemId}/provisioning-review")
def DeviceType2ProvisioningReview(systemId: str, payload: Devicetype2provisioningreviewRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type2/{systemId}/provisioning-review
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/provisioning-review"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type2/{systemId}/shelves")
def DeviceType2GetAllShelves(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}/shelves
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/shelves"
    static_data = MOCK_DB.get("DeviceType2GetAllShelves", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type2/{systemId}/shelves/{shelfId}")
def DeviceType2GetShelfById(systemId: str, shelfId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}/shelves/{shelfId}
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/shelves"
    item_id = shelfId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType2GetShelfById", dict())
    return static_val

@app.post("/api/v1/storage-systems/device-type2/{systemId}/shelves/{shelfId}/actions/locate")
def DeviceType2LocateShelfChassis(systemId: str, shelfId: str, payload: Devicetype2locateshelfchassisRequest):
    return MOCK_DB.get("DeviceType2LocateShelfChassis", dict())

@app.put("/api/v1/storage-systems/device-type2/{systemId}/shelves/actions/activate")
def DeviceType2ActivateShelf(systemId: str, payload: Devicetype2activateshelfRequest):
    """
    Dynamic CRUD Route: PUT /api/v1/storage-systems/device-type2/{systemId}/shelves/actions/activate
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/shelves/actions/activate"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})

    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.post("/api/v1/storage-systems/device-type2/{systemId}/snapshot-collections/{snapshotCollectionId}/actions/clone")
def DeviceType2CloneActionOnSnapshotCollections(systemId: str, snapshotCollectionId: str, payload: Devicetype2cloneactiononsnapshotcollectionsRequest):
    return MOCK_DB.get("DeviceType2CloneActionOnSnapshotCollections", dict())

@app.post("/api/v1/storage-systems/device-type2/{systemId}/snapshots/actions/update")
def DeviceType2EditSnapshotById(systemId: str, payload: Devicetype2editsnapshotbyidRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type2/{systemId}/snapshots/actions/update
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/snapshots/actions/update"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type2/{systemId}/storage-pools")
def DeviceType2GetAllPoolDetails(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}/storage-pools
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/storage-pools"
    static_data = MOCK_DB.get("DeviceType2GetAllPoolDetails", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.post("/api/v1/storage-systems/device-type2/{systemId}/storage-pools")
def DeviceType2CreatePool(systemId: str, payload: Devicetype2createpoolRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type2/{systemId}/storage-pools
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/storage-pools"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.delete("/api/v1/storage-systems/device-type2/{systemId}/storage-pools/{storagePoolId}")
def DeviceType2RemovePoolById(systemId: str, storagePoolId: str):
    """
    Dynamic CRUD Route: DELETE /api/v1/storage-systems/device-type2/{systemId}/storage-pools/{storagePoolId}
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/storage-pools"
    item_id = storagePoolId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        deleted = MOCK_DB["dynamic_store"][collection_path].pop(item_id)
        return {"message": "Deleted successfully", "id": item_id, "item": deleted}
    return MOCK_DB.get("DeviceType2RemovePoolById", dict())

@app.get("/api/v1/storage-systems/device-type2/{systemId}/storage-pools/{storagePoolId}")
def DeviceType2GetPoolDetailById(systemId: str, storagePoolId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}/storage-pools/{storagePoolId}
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/storage-pools"
    item_id = storagePoolId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType2GetPoolDetailById", dict())
    return static_val

@app.put("/api/v1/storage-systems/device-type2/{systemId}/storage-pools/{storagePoolId}")
def DeviceType2EditPoolDetailById(systemId: str, storagePoolId: str, payload: Devicetype2editpooldetailbyidRequest):
    """
    Dynamic CRUD Route: PUT /api/v1/storage-systems/device-type2/{systemId}/storage-pools/{storagePoolId}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/storage-pools"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    item_id = storagePoolId
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.post("/api/v1/storage-systems/device-type2/{systemId}/storage-pools/{storagePoolId}/actions/merge")
def DeviceType2MergePoolById(systemId: str, storagePoolId: str, payload: Devicetype2mergepoolbyidRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type2/{systemId}/storage-pools/{storagePoolId}/actions/merge
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/storage-pools/{storagePoolId}/actions/merge"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type2/{systemId}/storage-pools/{storagePoolId}/capacity-history")
def DeviceType2GetPoolCapacityHistory(systemId: str, storagePoolId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}/storage-pools/{storagePoolId}/capacity-history
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/storage-pools/{storagePoolId}/capacity-history"
    static_data = MOCK_DB.get("DeviceType2GetPoolCapacityHistory", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type2/{systemId}/storage-pools/{storagePoolId}/performance-history")
def DeviceType2GetPoolPerformanceHistory(systemId: str, storagePoolId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}/storage-pools/{storagePoolId}/performance-history
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/storage-pools/{storagePoolId}/performance-history"
    static_data = MOCK_DB.get("DeviceType2GetPoolPerformanceHistory", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type2/{systemId}/storage-pools/{storagePoolId}/performance-statistics")
def DeviceType2GetPoolPerformanceStatistics(systemId: str, storagePoolId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}/storage-pools/{storagePoolId}/performance-statistics
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/storage-pools/{storagePoolId}/performance-statistics"
    static_data = MOCK_DB.get("DeviceType2GetPoolPerformanceStatistics", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.put("/api/v1/storage-systems/device-type2/{systemId}/system-settings")
def DeviceType2EditSystemSettings(systemId: str, payload: Devicetype2editsystemsettingsRequest):
    """
    Dynamic CRUD Route: PUT /api/v1/storage-systems/device-type2/{systemId}/system-settings
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/system-settings"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})

    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type2/{systemId}/system-settings/replication-partners")
def DeviceType2GetReplicationPartners(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}/system-settings/replication-partners
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/system-settings/replication-partners"
    static_data = MOCK_DB.get("DeviceType2GetReplicationPartners", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.post("/api/v1/storage-systems/device-type2/{systemId}/system-settings/replication-partners")
def DeviceType2CreateReplicationPartners(systemId: str, payload: Devicetype2createreplicationpartnersRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type2/{systemId}/system-settings/replication-partners
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/system-settings/replication-partners"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type2/{systemId}/system-settings/replication-partners/{replicationpartnerId}")
def DeviceType2GetReplicationPartnersById(systemId: str, replicationpartnerId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}/system-settings/replication-partners/{replicationpartnerId}
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/system-settings/replication-partners"
    item_id = replicationpartnerId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType2GetReplicationPartnersById", dict())
    return static_val

@app.put("/api/v1/storage-systems/device-type2/{systemId}/system-settings/replication-partners/{replicationpartnerId}")
def DeviceType2EditReplicationPartnersById(systemId: str, replicationpartnerId: str, payload: Devicetype2editreplicationpartnersbyidRequest):
    """
    Dynamic CRUD Route: PUT /api/v1/storage-systems/device-type2/{systemId}/system-settings/replication-partners/{replicationpartnerId}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/system-settings/replication-partners"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    item_id = replicationpartnerId
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.post("/api/v1/storage-systems/device-type2/{systemId}/system-settings/replication-partners/actions/pause")
def DeviceType2PauseReplicationPartner(systemId: str, payload: Devicetype2pausereplicationpartnerRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type2/{systemId}/system-settings/replication-partners/actions/pause
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/system-settings/replication-partners/actions/pause"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.post("/api/v1/storage-systems/device-type2/{systemId}/system-settings/replication-partners/actions/resume")
def DeviceType2ResumeReplicationPartner(systemId: str, payload: Devicetype2resumereplicationpartnerRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type2/{systemId}/system-settings/replication-partners/actions/resume
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/system-settings/replication-partners/actions/resume"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.post("/api/v1/storage-systems/device-type2/{systemId}/system-settings/replication-partners/actions/test")
def DeviceType2TestReplicationConfiguration(systemId: str, payload: Devicetype2testreplicationconfigurationRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type2/{systemId}/system-settings/replication-partners/actions/test
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/system-settings/replication-partners/actions/test"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.post("/api/v1/storage-systems/device-type2/{systemId}/system-settings/replication-partners/remove")
def DeviceType2RemoveReplicationPartner(systemId: str, payload: Devicetype2removereplicationpartnerRequest):
    return MOCK_DB.get("DeviceType2RemoveReplicationPartner", dict())

@app.get("/api/v1/storage-systems/device-type2/{systemId}/system-settings/witnesses")
def DeviceType2GetWitnesses(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}/system-settings/witnesses
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/system-settings/witnesses"
    static_data = MOCK_DB.get("DeviceType2GetWitnesses", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.post("/api/v1/storage-systems/device-type2/{systemId}/system-settings/witnesses")
def DeviceType2CreateWitness(systemId: str, payload: Devicetype2createwitnessRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type2/{systemId}/system-settings/witnesses
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/system-settings/witnesses"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.delete("/api/v1/storage-systems/device-type2/{systemId}/system-settings/witnesses/{witnessId}")
def DeviceType2RemoveWitnessesById(systemId: str, witnessId: str):
    """
    Dynamic CRUD Route: DELETE /api/v1/storage-systems/device-type2/{systemId}/system-settings/witnesses/{witnessId}
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/system-settings/witnesses"
    item_id = witnessId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        deleted = MOCK_DB["dynamic_store"][collection_path].pop(item_id)
        return {"message": "Deleted successfully", "id": item_id, "item": deleted}
    return MOCK_DB.get("DeviceType2RemoveWitnessesById", dict())

@app.get("/api/v1/storage-systems/device-type2/{systemId}/system-settings/witnesses/{witnessId}")
def DeviceType2GetWitnessesById(systemId: str, witnessId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}/system-settings/witnesses/{witnessId}
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/system-settings/witnesses"
    item_id = witnessId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType2GetWitnessesById", dict())
    return static_val

@app.post("/api/v1/storage-systems/device-type2/{systemId}/system-settings/witnesses/{witnessId}/actions/test")
def DeviceType2TestWitnessesById(systemId: str, witnessId: str):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type2/{systemId}/system-settings/witnesses/{witnessId}/actions/test
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/system-settings/witnesses/{witnessId}/actions/test"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = {}
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.post("/api/v1/storage-systems/device-type2/{systemId}/uninitialized-arrays")
def GetDeviceType2UninitializedArrays(systemId: str):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type2/{systemId}/uninitialized-arrays
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/uninitialized-arrays"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = {}
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.post("/api/v1/storage-systems/device-type2/{systemId}/uninitialized-arrays/{uninitializedArrayId}")
def GetDeviceType2UninitializedArrayById(systemId: str, uninitializedArrayId: str, payload: Getdevicetype2uninitializedarraybyidRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type2/{systemId}/uninitialized-arrays/{uninitializedArrayId}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/uninitialized-arrays"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type2/{systemId}/volume-collections")
def DeviceType2GetAllVolumeCollections(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}/volume-collections
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/volume-collections"
    static_data = MOCK_DB.get("DeviceType2GetAllVolumeCollections", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.post("/api/v1/storage-systems/device-type2/{systemId}/volume-collections")
def DeviceType2VolumeCollectionCreate(systemId: str, payload: Devicetype2volumecollectioncreateRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type2/{systemId}/volume-collections
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/volume-collections"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.delete("/api/v1/storage-systems/device-type2/{systemId}/volume-collections/{volumeCollectionId}")
def DeviceType2RemoveVolumeCollectionById(systemId: str, volumeCollectionId: str):
    """
    Dynamic CRUD Route: DELETE /api/v1/storage-systems/device-type2/{systemId}/volume-collections/{volumeCollectionId}
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/volume-collections"
    item_id = volumeCollectionId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        deleted = MOCK_DB["dynamic_store"][collection_path].pop(item_id)
        return {"message": "Deleted successfully", "id": item_id, "item": deleted}
    return MOCK_DB.get("DeviceType2RemoveVolumeCollectionById", dict())

@app.get("/api/v1/storage-systems/device-type2/{systemId}/volume-collections/{volumeCollectionId}")
def DeviceType2GetVolumeCollectionById(systemId: str, volumeCollectionId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}/volume-collections/{volumeCollectionId}
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/volume-collections"
    item_id = volumeCollectionId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType2GetVolumeCollectionById", dict())
    return static_val

@app.put("/api/v1/storage-systems/device-type2/{systemId}/volume-collections/{volumeCollectionId}")
def DeviceType2EditVolumeCollectionById(systemId: str, volumeCollectionId: str, payload: Devicetype2editvolumecollectionbyidRequest):
    """
    Dynamic CRUD Route: PUT /api/v1/storage-systems/device-type2/{systemId}/volume-collections/{volumeCollectionId}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/volume-collections"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    item_id = volumeCollectionId
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.post("/api/v1/storage-systems/device-type2/{systemId}/volume-collections/{volumeCollectionId}/actions/abort-handover")
def DeviceType2ActiononVolumeCollection(systemId: str, volumeCollectionId: str):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type2/{systemId}/volume-collections/{volumeCollectionId}/actions/abort-handover
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/volume-collections/{volumeCollectionId}/actions/abort-handover"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = {}
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.post("/api/v1/storage-systems/device-type2/{systemId}/volume-collections/{volumeCollectionId}/actions/add-volumes")
def DeviceType2AddVolumesToVolumeCollections(systemId: str, volumeCollectionId: str, payload: Devicetype2addvolumestovolumecollectionsRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type2/{systemId}/volume-collections/{volumeCollectionId}/actions/add-volumes
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/volume-collections/{volumeCollectionId}/actions/add-volumes"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.post("/api/v1/storage-systems/device-type2/{systemId}/volume-collections/{volumeCollectionId}/actions/demote")
def DeviceType2ActionOnVolumeCollectionId(systemId: str, volumeCollectionId: str, payload: Devicetype2actiononvolumecollectionidRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type2/{systemId}/volume-collections/{volumeCollectionId}/actions/demote
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/volume-collections/{volumeCollectionId}/actions/demote"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.post("/api/v1/storage-systems/device-type2/{systemId}/volume-collections/{volumeCollectionId}/actions/handover")
def DeviceType2ActionOnVolumeCollection(systemId: str, volumeCollectionId: str, payload: Devicetype2actiononvolumecollectionRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type2/{systemId}/volume-collections/{volumeCollectionId}/actions/handover
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/volume-collections/{volumeCollectionId}/actions/handover"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.post("/api/v1/storage-systems/device-type2/{systemId}/volume-collections/{volumeCollectionId}/actions/promote")
def DeviceType2PromoteActionOnVolumeCollection(systemId: str, volumeCollectionId: str):
    return MOCK_DB.get("DeviceType2PromoteActionOnVolumeCollection", dict())

@app.post("/api/v1/storage-systems/device-type2/{systemId}/volume-collections/{volumeCollectionId}/actions/remove-volumes")
def DeviceType2RemoveVolumesFromVolumeCollection(systemId: str, volumeCollectionId: str, payload: Devicetype2removevolumesfromvolumecollectionRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type2/{systemId}/volume-collections/{volumeCollectionId}/actions/remove-volumes
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/volume-collections/{volumeCollectionId}/actions/remove-volumes"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type2/{systemId}/volume-collections/{volumeCollectionId}/snapshot-collections")
def DeviceType2GetSnapshotsByVolumeCollectionId(systemId: str, volumeCollectionId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}/volume-collections/{volumeCollectionId}/snapshot-collections
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/volume-collections/{volumeCollectionId}/snapshot-collections"
    static_data = MOCK_DB.get("DeviceType2GetSnapshotsByVolumeCollectionId", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.post("/api/v1/storage-systems/device-type2/{systemId}/volume-collections/{volumeCollectionId}/snapshot-collections")
def DeviceType2CreateSnapshotCollections(systemId: str, volumeCollectionId: str, payload: Devicetype2createsnapshotcollectionsRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type2/{systemId}/volume-collections/{volumeCollectionId}/snapshot-collections
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/volume-collections/{volumeCollectionId}/snapshot-collections"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type2/{systemId}/volume-collections/{volumeCollectionId}/snapshot-collections/{snapshotCollectionId}")
def DeviceType2GetSnapshotCollectionsById(systemId: str, volumeCollectionId: str, snapshotCollectionId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}/volume-collections/{volumeCollectionId}/snapshot-collections/{snapshotCollectionId}
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/volume-collections/{volumeCollectionId}/snapshot-collections"
    item_id = snapshotCollectionId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType2GetSnapshotCollectionsById", dict())
    return static_val

@app.post("/api/v1/storage-systems/device-type2/{systemId}/volume-collections/{volumeCollectionId}/snapshot-collections/remove")
def DeviceType2RemoveSnapShotCollection(systemId: str, volumeCollectionId: str, payload: Devicetype2removesnapshotcollectionRequest):
    return MOCK_DB.get("DeviceType2RemoveSnapShotCollection", dict())

@app.post("/api/v1/storage-systems/device-type2/{systemId}/volume-collections/{volumeCollectionId}/snapshot-collections/update")
def DeviceType2ActionOnSnapshotCollection(systemId: str, volumeCollectionId: str, payload: Devicetype2actiononsnapshotcollectionRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type2/{systemId}/volume-collections/{volumeCollectionId}/snapshot-collections/update
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/volume-collections/{volumeCollectionId}/snapshot-collections/update"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type2/{systemId}/volumes")
def DeviceType2GetAllVolumes(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}/volumes
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/volumes"
    static_data = MOCK_DB.get("DeviceType2GetAllVolumes", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.post("/api/v1/storage-systems/device-type2/{systemId}/volumes")
def DeviceType2VolumesCreate(systemId: str, payload: Devicetype2volumescreateRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type2/{systemId}/volumes
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/volumes"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type2/{systemId}/volumes-performance")
def DeviceType2GetVolumesPerformanceHistory(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}/volumes-performance
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/volumes-performance"
    static_data = MOCK_DB.get("DeviceType2GetVolumesPerformanceHistory", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.delete("/api/v1/storage-systems/device-type2/{systemId}/volumes/{volumeId}")
def DeviceType2RemoveVolumeById(systemId: str, volumeId: str):
    """
    Dynamic CRUD Route: DELETE /api/v1/storage-systems/device-type2/{systemId}/volumes/{volumeId}
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/volumes"
    item_id = volumeId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        deleted = MOCK_DB["dynamic_store"][collection_path].pop(item_id)
        return {"message": "Deleted successfully", "id": item_id, "item": deleted}
    return MOCK_DB.get("DeviceType2RemoveVolumeById", dict())

@app.get("/api/v1/storage-systems/device-type2/{systemId}/volumes/{volumeId}")
def DeviceType2GetVolumeById(systemId: str, volumeId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}/volumes/{volumeId}
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/volumes"
    item_id = volumeId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType2GetVolumeById", dict())
    return static_val

@app.put("/api/v1/storage-systems/device-type2/{systemId}/volumes/{volumeId}")
def DeviceType2EditVolumeById(systemId: str, volumeId: str, payload: Devicetype2editvolumebyidRequest):
    """
    Dynamic CRUD Route: PUT /api/v1/storage-systems/device-type2/{systemId}/volumes/{volumeId}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/volumes"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    item_id = volumeId
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.post("/api/v1/storage-systems/device-type2/{systemId}/volumes/{volumeId}/actions/move")
def DeviceType2MoveVolume(systemId: str, volumeId: str, payload: Devicetype2movevolumeRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type2/{systemId}/volumes/{volumeId}/actions/move
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/volumes/{volumeId}/actions/move"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.post("/api/v1/storage-systems/device-type2/{systemId}/volumes/{volumeId}/actions/restore")
def DeviceType2RestoreVolumeById(systemId: str, volumeId: str, payload: Devicetype2restorevolumebyidRequest):
    return MOCK_DB.get("DeviceType2RestoreVolumeById", dict())

@app.get("/api/v1/storage-systems/device-type2/{systemId}/volumes/{volumeId}/capacity-history")
def DeviceType2GetVolumeCapacityHistory(systemId: str, volumeId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}/volumes/{volumeId}/capacity-history
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/volumes/{volumeId}/capacity-history"
    static_data = MOCK_DB.get("DeviceType2GetVolumeCapacityHistory", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.post("/api/v1/storage-systems/device-type2/{systemId}/volumes/{volumeId}/clone")
def DeviceType2CloneVolumeById(systemId: str, volumeId: str, payload: Devicetype2clonevolumebyidRequest):
    return MOCK_DB.get("DeviceType2CloneVolumeById", dict())

@app.post("/api/v1/storage-systems/device-type2/{systemId}/volumes/{volumeId}/export")
def DeviceType2VolumesExport(systemId: str, volumeId: str, payload: Devicetype2volumesexportRequest):
    return MOCK_DB.get("DeviceType2VolumesExport", dict())

@app.get("/api/v1/storage-systems/device-type2/{systemId}/volumes/{volumeId}/performance-history")
def DeviceType2GetVolumePerformanceHistory(systemId: str, volumeId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}/volumes/{volumeId}/performance-history
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/volumes/{volumeId}/performance-history"
    static_data = MOCK_DB.get("DeviceType2GetVolumePerformanceHistory", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type2/{systemId}/volumes/{volumeId}/performance-statistics")
def DeviceType2GetVolumePerformanceStatistics(systemId: str, volumeId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}/volumes/{volumeId}/performance-statistics
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/volumes/{volumeId}/performance-statistics"
    static_data = MOCK_DB.get("DeviceType2GetVolumePerformanceStatistics", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type2/{systemId}/volumes/{volumeId}/snapshots")
def DeviceType2GetAllSnapshotsByVolumeId(systemId: str, volumeId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}/volumes/{volumeId}/snapshots
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/volumes/{volumeId}/snapshots"
    static_data = MOCK_DB.get("DeviceType2GetAllSnapshotsByVolumeId", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.post("/api/v1/storage-systems/device-type2/{systemId}/volumes/{volumeId}/snapshots")
def DeviceType2SnapshotCreate(systemId: str, volumeId: str, payload: Devicetype2snapshotcreateRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type2/{systemId}/volumes/{volumeId}/snapshots
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/volumes/{volumeId}/snapshots"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.delete("/api/v1/storage-systems/device-type2/{systemId}/volumes/{volumeId}/snapshots/{snapshotId}")
def DeviceType2RemoveSnapshotById(systemId: str, volumeId: str, snapshotId: str):
    """
    Dynamic CRUD Route: DELETE /api/v1/storage-systems/device-type2/{systemId}/volumes/{volumeId}/snapshots/{snapshotId}
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/volumes/{volumeId}/snapshots"
    item_id = snapshotId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        deleted = MOCK_DB["dynamic_store"][collection_path].pop(item_id)
        return {"message": "Deleted successfully", "id": item_id, "item": deleted}
    return MOCK_DB.get("DeviceType2RemoveSnapshotById", dict())

@app.get("/api/v1/storage-systems/device-type2/{systemId}/volumes/{volumeId}/snapshots/{snapshotId}")
def DeviceType2GetSnapshotById(systemId: str, volumeId: str, snapshotId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type2/{systemId}/volumes/{volumeId}/snapshots/{snapshotId}
    """
    collection_path = f"/api/v1/storage-systems/device-type2/{systemId}/volumes/{volumeId}/snapshots"
    item_id = snapshotId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType2GetSnapshotById", dict())
    return static_val

@app.post("/api/v1/storage-systems/device-type2/{systemId}/volumes/{volumeId}/snapshots/{snapshotId}/export")
def DeviceType2SnapshotExport(systemId: str, volumeId: str, snapshotId: str, payload: Devicetype2snapshotexportRequest):
    return MOCK_DB.get("DeviceType2SnapshotExport", dict())

@app.post("/api/v1/storage-systems/device-type2/{systemId}/volumes/{volumeId}/snapshots/{snapshotId}/un-export")
def DeviceType2DeleteSnapshotAccessById(systemId: str, volumeId: str, snapshotId: str, payload: Devicetype2deletesnapshotaccessbyidRequest):
    return MOCK_DB.get("DeviceType2DeleteSnapshotAccessById", dict())

@app.post("/api/v1/storage-systems/device-type2/{systemId}/volumes/{volumeId}/un-export")
def DeviceType2DeleteVolumeAccessById(systemId: str, volumeId: str, payload: Devicetype2deletevolumeaccessbyidRequest):
    return MOCK_DB.get("DeviceType2DeleteVolumeAccessById", dict())

@app.get("/api/v1/storage-systems/device-type4")
def DeviceType4SystemsList():
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4
    """
    collection_path = f"/api/v1/storage-systems/device-type4"
    static_data = MOCK_DB.get("DeviceType4SystemsList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type4/{id}")
def DeviceType4SystemGetById(id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{id}
    """
    collection_path = f"/api/v1/storage-systems/device-type4"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType4SystemGetById", dict())
    return static_val

@app.post("/api/v1/storage-systems/device-type4/{id}")
def DeviceType4SystemLocate(id: str, payload: Devicetype4systemlocateRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type4/{id}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type4"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type4/{systemId}/alert-contacts")
def DeviceType4AlertContactsList(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/alert-contacts
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/alert-contacts"
    static_data = MOCK_DB.get("DeviceType4AlertContactsList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.post("/api/v1/storage-systems/device-type4/{systemId}/alert-contacts")
def DeviceType4AlertContactsCreate(systemId: str, payload: Devicetype4alertcontactscreateRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type4/{systemId}/alert-contacts
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/alert-contacts"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.delete("/api/v1/storage-systems/device-type4/{systemId}/alert-contacts/{id}")
def DeviceType4AlertContactsDelete(systemId: str, id: str):
    """
    Dynamic CRUD Route: DELETE /api/v1/storage-systems/device-type4/{systemId}/alert-contacts/{id}
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/alert-contacts"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        deleted = MOCK_DB["dynamic_store"][collection_path].pop(item_id)
        return {"message": "Deleted successfully", "id": item_id, "item": deleted}
    return MOCK_DB.get("DeviceType4AlertContactsDelete", dict())

@app.get("/api/v1/storage-systems/device-type4/{systemId}/alert-contacts/{id}")
def DeviceType4AlertContactsGetById(systemId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/alert-contacts/{id}
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/alert-contacts"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType4AlertContactsGetById", dict())
    return static_val

@app.put("/api/v1/storage-systems/device-type4/{systemId}/alert-contacts/{id}")
def DeviceType4AlertContactsUpdate(systemId: str, id: str, payload: Devicetype4alertcontactsupdateRequest):
    """
    Dynamic CRUD Route: PUT /api/v1/storage-systems/device-type4/{systemId}/alert-contacts/{id}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/alert-contacts"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    item_id = id
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type4/{systemId}/application-summary")
def DeviceType4ApplicationSummaryGet(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/application-summary
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/application-summary"
    static_data = MOCK_DB.get("DeviceType4ApplicationSummaryGet", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type4/{systemId}/applicationsets")
def DeviceType4VolumeSetsList(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/applicationsets
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/applicationsets"
    static_data = MOCK_DB.get("DeviceType4VolumeSetsList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.post("/api/v1/storage-systems/device-type4/{systemId}/applicationsets")
def DeviceType4VolumeSetsCreate(systemId: str, payload: Devicetype4volumesetscreateRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type4/{systemId}/applicationsets
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/applicationsets"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.post("/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{appsetId}/export")
def DeviceType4VolumeSetExport(systemId: str, appsetId: str, payload: Devicetype4volumesetexportRequest):
    return MOCK_DB.get("DeviceType4VolumeSetExport", dict())

@app.get("/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{appsetId}/replication-partners")
def DeviceType4GetReplicationPartnersByAppSetId(systemId: str, appsetId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/applicationsets/{appsetId}/replication-partners
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{appsetId}/replication-partners"
    static_data = MOCK_DB.get("DeviceType4GetReplicationPartnersByAppSetId", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{appsetId}/replication-partners/{replicationPartnerId}/volumes")
def DeviceType4GetReplicationPartnerVolumesByAppSetId(systemId: str, appsetId: str, replicationPartnerId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/applicationsets/{appsetId}/replication-partners/{replicationPartnerId}/volumes
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{appsetId}/replication-partners/{replicationPartnerId}/volumes"
    static_data = MOCK_DB.get("DeviceType4GetReplicationPartnerVolumesByAppSetId", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.delete("/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{appsetId}/snapsets/{snapsetId}")
def DeviceType4VolumeSetSnapshotGetById(systemId: str, appsetId: str, snapsetId: str):
    """
    Dynamic CRUD Route: DELETE /api/v1/storage-systems/device-type4/{systemId}/applicationsets/{appsetId}/snapsets/{snapsetId}
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{appsetId}/snapsets"
    item_id = snapsetId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        deleted = MOCK_DB["dynamic_store"][collection_path].pop(item_id)
        return {"message": "Deleted successfully", "id": item_id, "item": deleted}
    return MOCK_DB.get("DeviceType4VolumeSetSnapshotGetById", dict())

@app.get("/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{appsetId}/snapsets/{snapsetId}")
def DeviceType4SnapsetsGetById(systemId: str, appsetId: str, snapsetId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/applicationsets/{appsetId}/snapsets/{snapsetId}
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{appsetId}/snapsets"
    item_id = snapsetId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType4SnapsetsGetById", dict())
    return static_val

@app.post("/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{appsetId}/un-export")
def DeviceType4VolumeSetUnexport(systemId: str, appsetId: str, payload: Devicetype4volumesetunexportRequest):
    return MOCK_DB.get("DeviceType4VolumeSetUnexport", dict())

@app.get("/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{appsetId}/volumes")
def DeviceType4VolumeSetVolumesList(systemId: str, appsetId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/applicationsets/{appsetId}/volumes
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{appsetId}/volumes"
    static_data = MOCK_DB.get("DeviceType4VolumeSetVolumesList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.delete("/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}")
def DeviceType4VolumeSetsDeleteById(systemId: str, id: str):
    """
    Dynamic CRUD Route: DELETE /api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/applicationsets"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        deleted = MOCK_DB["dynamic_store"][collection_path].pop(item_id)
        return {"message": "Deleted successfully", "id": item_id, "item": deleted}
    return MOCK_DB.get("DeviceType4VolumeSetsDeleteById", dict())

@app.get("/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}")
def DeviceType4VolumeSetsGetById(systemId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/applicationsets"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType4VolumeSetsGetById", dict())
    return static_val

@app.put("/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}")
def DeviceType4VolumeSetsEditById(systemId: str, id: str, payload: Devicetype4volumesetseditbyidRequest):
    """
    Dynamic CRUD Route: PUT /api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/applicationsets"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    item_id = id
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}/capacity-statistics")
def DeviceType4VolumeSetCapacityStatisticsGetById(systemId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}/capacity-statistics
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}/capacity-statistics"
    static_data = MOCK_DB.get("DeviceType4VolumeSetCapacityStatisticsGetById", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}/performance")
def DeviceType4GetAppSetVolumesPerformanceHistory(systemId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}/performance
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}/performance"
    static_data = MOCK_DB.get("DeviceType4GetAppSetVolumesPerformanceHistory", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}/protection-policies")
def DeviceType4GetProtectionPolicies(systemId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}/protection-policies
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}/protection-policies"
    static_data = MOCK_DB.get("DeviceType4GetProtectionPolicies", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.post("/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}/protection-policies")
def DeviceType4CreateProtectionPolicy(systemId: str, id: str, payload: Devicetype4createprotectionpolicyRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}/protection-policies
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}/protection-policies"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.put("/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}/protection-policies")
def DeviceType4EditProtectionPolicies(systemId: str, id: str, payload: Devicetype4editprotectionpoliciesRequest):
    """
    Dynamic CRUD Route: PUT /api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}/protection-policies
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}/protection-policies"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})

    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.post("/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}/protection-policies/fix")
def DeviceType4FixProtectionPolicy(systemId: str, id: str, payload: Devicetype4fixprotectionpolicyRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}/protection-policies/fix
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}/protection-policies/fix"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.post("/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}/protection-policies/remove")
def DeviceType4removeProtectionPolicies(systemId: str, id: str, payload: Devicetype4removeprotectionpoliciesRequest):
    return MOCK_DB.get("DeviceType4removeProtectionPolicies", dict())

@app.get("/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}/proximity-settings")
def DeviceType4GetProximitySettings(systemId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}/proximity-settings
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}/proximity-settings"
    static_data = MOCK_DB.get("DeviceType4GetProximitySettings", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.put("/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}/proximity-settings")
def DeviceType4EditProximitySettings(systemId: str, id: str, payload: Devicetype4editproximitysettingsRequest):
    """
    Dynamic CRUD Route: PUT /api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}/proximity-settings
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}/proximity-settings"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})

    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.post("/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}/remote-protection/actions")
def DeviceType4actionOnVolumeSets(systemId: str, id: str, payload: Devicetype4actiononvolumesetsRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}/remote-protection/actions
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}/remote-protection/actions"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}/snapsets")
def DeviceType4VolumeSetSnapshotsList(systemId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}/snapsets
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}/snapsets"
    static_data = MOCK_DB.get("DeviceType4VolumeSetSnapshotsList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.post("/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}/snapsets")
def DeviceType4VolumeSetsSnapshotCreate(systemId: str, id: str, payload: Devicetype4volumesetssnapshotcreateRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}/snapsets
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}/snapsets"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}/supported-protection")
def DeviceType4getSupportedProtectionTypes(systemId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}/supported-protection
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}/supported-protection"
    static_data = MOCK_DB.get("DeviceType4getSupportedProtectionTypes", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type4/{systemId}/capacity-forecast")
def DeviceType4SystemCapacityForecastGet(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/capacity-forecast
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/capacity-forecast"
    static_data = MOCK_DB.get("DeviceType4SystemCapacityForecastGet", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type4/{systemId}/capacity-history")
def DeviceType4SystemCapacityHistoryGet(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/capacity-history
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/capacity-history"
    static_data = MOCK_DB.get("DeviceType4SystemCapacityHistoryGet", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type4/{systemId}/capacity-summary")
def DeviceType4SystemCapacitySummaryGet(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/capacity-summary
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/capacity-summary"
    static_data = MOCK_DB.get("DeviceType4SystemCapacitySummaryGet", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type4/{systemId}/capacity-timeuntilfull")
def DeviceType4SystemCapacityTimeUntilFull(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/capacity-timeuntilfull
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/capacity-timeuntilfull"
    static_data = MOCK_DB.get("DeviceType4SystemCapacityTimeUntilFull", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type4/{systemId}/certificates")
def DeviceType4CertificatesList(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/certificates
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/certificates"
    static_data = MOCK_DB.get("DeviceType4CertificatesList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.post("/api/v1/storage-systems/device-type4/{systemId}/certificates")
def DeviceType4PostCertificate(systemId: str, payload: Devicetype4postcertificateRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type4/{systemId}/certificates
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/certificates"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type4/{systemId}/certificates/{id}")
def DeviceType4CertificatesGetById(systemId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/certificates/{id}
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/certificates"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType4CertificatesGetById", dict())
    return static_val

@app.put("/api/v1/storage-systems/device-type4/{systemId}/certificates/{id}")
def DeviceType4PutCertificate(systemId: str, id: str, payload: Devicetype4putcertificateRequest):
    """
    Dynamic CRUD Route: PUT /api/v1/storage-systems/device-type4/{systemId}/certificates/{id}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/certificates"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    item_id = id
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.post("/api/v1/storage-systems/device-type4/{systemId}/certificates/remove")
def DeviceType4RemoveCertificates(systemId: str, payload: Devicetype4removecertificatesRequest):
    return MOCK_DB.get("DeviceType4RemoveCertificates", dict())

@app.post("/api/v1/storage-systems/device-type4/{systemId}/collect-support-data")
def DeviceType4SupportDataCollect(systemId: str):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type4/{systemId}/collect-support-data
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/collect-support-data"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = {}
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type4/{systemId}/component-performance-statistics")
def DeviceType4SystemComponentPerformanceStatisticsGet(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/component-performance-statistics
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/component-performance-statistics"
    static_data = MOCK_DB.get("DeviceType4SystemComponentPerformanceStatisticsGet", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type4/{systemId}/enclosure-cards")
def DeviceType4EnclosureCardList(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/enclosure-cards
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/enclosure-cards"
    static_data = MOCK_DB.get("DeviceType4EnclosureCardList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type4/{systemId}/enclosure-connectors")
def DeviceType4EnclosureConnectorsList(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/enclosure-connectors
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/enclosure-connectors"
    static_data = MOCK_DB.get("DeviceType4EnclosureConnectorsList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type4/{systemId}/enclosures")
def DeviceType4EnclosuresList(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/enclosures
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/enclosures"
    static_data = MOCK_DB.get("DeviceType4EnclosuresList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type4/{systemId}/enclosures/{cageId}/disks")
def DeviceType4DisksList(systemId: str, cageId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/enclosures/{cageId}/disks
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/enclosures/{cageId}/disks"
    static_data = MOCK_DB.get("DeviceType4DisksList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type4/{systemId}/enclosures/{cageId}/disks/{id}")
def DeviceType4DisksGetById(systemId: str, cageId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/enclosures/{cageId}/disks/{id}
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/enclosures/{cageId}/disks"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType4DisksGetById", dict())
    return static_val

@app.get("/api/v1/storage-systems/device-type4/{systemId}/enclosures/{enclosureId}/enclosure-card-ports")
def DeviceType4EnclosureCardPortsList(systemId: str, enclosureId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/enclosures/{enclosureId}/enclosure-card-ports
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/enclosures/{enclosureId}/enclosure-card-ports"
    static_data = MOCK_DB.get("DeviceType4EnclosureCardPortsList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type4/{systemId}/enclosures/{enclosureId}/enclosure-card-ports/{id}")
def DeviceType4EnclosureCardPortsGetById(systemId: str, enclosureId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/enclosures/{enclosureId}/enclosure-card-ports/{id}
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/enclosures/{enclosureId}/enclosure-card-ports"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType4EnclosureCardPortsGetById", dict())
    return static_val

@app.get("/api/v1/storage-systems/device-type4/{systemId}/enclosures/{enclosureId}/enclosure-cards")
def DeviceType4EnclosureCardsList(systemId: str, enclosureId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/enclosures/{enclosureId}/enclosure-cards
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/enclosures/{enclosureId}/enclosure-cards"
    static_data = MOCK_DB.get("DeviceType4EnclosureCardsList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type4/{systemId}/enclosures/{enclosureId}/enclosure-cards/{id}")
def DeviceType4EnclosureCardsGetById(systemId: str, enclosureId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/enclosures/{enclosureId}/enclosure-cards/{id}
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/enclosures/{enclosureId}/enclosure-cards"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType4EnclosureCardsGetById", dict())
    return static_val

@app.post("/api/v1/storage-systems/device-type4/{systemId}/enclosures/{enclosureId}/enclosure-cards/{id}")
def DeviceType4EnclosureCardsLocateIOById(systemId: str, enclosureId: str, id: str, payload: Devicetype4enclosurecardslocateiobyidRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type4/{systemId}/enclosures/{enclosureId}/enclosure-cards/{id}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/enclosures/{enclosureId}/enclosure-cards"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type4/{systemId}/enclosures/{enclosureId}/enclosure-connectors")
def DeviceType4EnclosureConnectorList(systemId: str, enclosureId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/enclosures/{enclosureId}/enclosure-connectors
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/enclosures/{enclosureId}/enclosure-connectors"
    static_data = MOCK_DB.get("DeviceType4EnclosureConnectorList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type4/{systemId}/enclosures/{enclosureId}/enclosure-connectors/{enclosureConnectorId}")
def DeviceType4EnclosureConnectorsGetById(systemId: str, enclosureId: str, enclosureConnectorId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/enclosures/{enclosureId}/enclosure-connectors/{enclosureConnectorId}
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/enclosures/{enclosureId}/enclosure-connectors"
    item_id = enclosureConnectorId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType4EnclosureConnectorsGetById", dict())
    return static_val

@app.get("/api/v1/storage-systems/device-type4/{systemId}/enclosures/{enclosureId}/enclosure-disks")
def DeviceType4EnclosureDisksList(systemId: str, enclosureId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/enclosures/{enclosureId}/enclosure-disks
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/enclosures/{enclosureId}/enclosure-disks"
    static_data = MOCK_DB.get("DeviceType4EnclosureDisksList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type4/{systemId}/enclosures/{enclosureId}/enclosure-disks/{id}")
def DeviceType4EnclosureDisksGetById(systemId: str, enclosureId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/enclosures/{enclosureId}/enclosure-disks/{id}
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/enclosures/{enclosureId}/enclosure-disks"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType4EnclosureDisksGetById", dict())
    return static_val

@app.get("/api/v1/storage-systems/device-type4/{systemId}/enclosures/{enclosureId}/enclosure-powers")
def DeviceType4EnclosurePowersList(systemId: str, enclosureId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/enclosures/{enclosureId}/enclosure-powers
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/enclosures/{enclosureId}/enclosure-powers"
    static_data = MOCK_DB.get("DeviceType4EnclosurePowersList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type4/{systemId}/enclosures/{enclosureId}/enclosure-powers/{id}")
def DeviceType4EnclosurePowersGetById(systemId: str, enclosureId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/enclosures/{enclosureId}/enclosure-powers/{id}
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/enclosures/{enclosureId}/enclosure-powers"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType4EnclosurePowersGetById", dict())
    return static_val

@app.get("/api/v1/storage-systems/device-type4/{systemId}/enclosures/{enclosureId}/enclosure-sleds")
def DeviceType4EnclosureSledsList(systemId: str, enclosureId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/enclosures/{enclosureId}/enclosure-sleds
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/enclosures/{enclosureId}/enclosure-sleds"
    static_data = MOCK_DB.get("DeviceType4EnclosureSledsList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type4/{systemId}/enclosures/{enclosureId}/enclosure-sleds/{id}")
def DeviceType4EnclosureSledsGetById(systemId: str, enclosureId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/enclosures/{enclosureId}/enclosure-sleds/{id}
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/enclosures/{enclosureId}/enclosure-sleds"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType4EnclosureSledsGetById", dict())
    return static_val

@app.post("/api/v1/storage-systems/device-type4/{systemId}/enclosures/{enclosureId}/enclosure-sleds/{id}")
def DeviceType4EnclosureSledsLocateDriveById(systemId: str, enclosureId: str, id: str, payload: Devicetype4enclosuresledslocatedrivebyidRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type4/{systemId}/enclosures/{enclosureId}/enclosure-sleds/{id}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/enclosures/{enclosureId}/enclosure-sleds"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type4/{systemId}/enclosures/{id}")
def DeviceType4EnclosuresGetById(systemId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/enclosures/{id}
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/enclosures"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType4EnclosuresGetById", dict())
    return static_val

@app.post("/api/v1/storage-systems/device-type4/{systemId}/enclosures/{id}")
def DeviceType4EnclosuresLocateById(systemId: str, id: str, payload: Devicetype4enclosureslocatebyidRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type4/{systemId}/enclosures/{id}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/enclosures"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.put("/api/v1/storage-systems/device-type4/{systemId}/enclosures/{id}")
def DeviceType4EnclosuresEditById(systemId: str, id: str, payload: Devicetype4enclosureseditbyidRequest):
    """
    Dynamic CRUD Route: PUT /api/v1/storage-systems/device-type4/{systemId}/enclosures/{id}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/enclosures"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    item_id = id
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.post("/api/v1/storage-systems/device-type4/{systemId}/encryption/backup")
def DeviceType4backupActionOnEncryption(systemId: str, payload: Devicetype4backupactiononencryptionRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type4/{systemId}/encryption/backup
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/encryption/backup"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.post("/api/v1/storage-systems/device-type4/{systemId}/encryption/checkekm")
def DeviceType4checkEKMConfiguration(systemId: str):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type4/{systemId}/encryption/checkekm
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/encryption/checkekm"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = {}
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.post("/api/v1/storage-systems/device-type4/{systemId}/encryption/enable")
def DeviceType4enableActionOnEncryption(systemId: str, payload: Devicetype4enableactiononencryptionRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type4/{systemId}/encryption/enable
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/encryption/enable"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.post("/api/v1/storage-systems/device-type4/{systemId}/encryption/rekey")
def DeviceType4rekeyActionOnEncryption(systemId: str, payload: Devicetype4rekeyactiononencryptionRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type4/{systemId}/encryption/rekey
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/encryption/rekey"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.post("/api/v1/storage-systems/device-type4/{systemId}/encryption/restore")
def DeviceType4restoreActionOnEncryption(systemId: str, payload: Devicetype4restoreactiononencryptionRequest):
    return MOCK_DB.get("DeviceType4restoreActionOnEncryption", dict())

@app.post("/api/v1/storage-systems/device-type4/{systemId}/encryption/setekm")
def DeviceType4setEKMConfiguration(systemId: str, payload: Devicetype4setekmconfigurationRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type4/{systemId}/encryption/setekm
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/encryption/setekm"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.post("/api/v1/storage-systems/device-type4/{systemId}/encryption/setekm/backup")
def DeviceType4setekmbackupActionOnEncryption(systemId: str, payload: Devicetype4setekmbackupactiononencryptionRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type4/{systemId}/encryption/setekm/backup
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/encryption/setekm/backup"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type4/{systemId}/file-shares")
def DeviceType4FileSharesList(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/file-shares
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/file-shares"
    static_data = MOCK_DB.get("DeviceType4FileSharesList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.post("/api/v1/storage-systems/device-type4/{systemId}/file-shares")
def DeviceType4FileshareCreate(systemId: str, payload: Devicetype4filesharecreateRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type4/{systemId}/file-shares
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/file-shares"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.delete("/api/v1/storage-systems/device-type4/{systemId}/file-shares/{fileShareId}")
def DeviceType4FileShareDeleteById(systemId: str, fileShareId: str):
    """
    Dynamic CRUD Route: DELETE /api/v1/storage-systems/device-type4/{systemId}/file-shares/{fileShareId}
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/file-shares"
    item_id = fileShareId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        deleted = MOCK_DB["dynamic_store"][collection_path].pop(item_id)
        return {"message": "Deleted successfully", "id": item_id, "item": deleted}
    return MOCK_DB.get("DeviceType4FileShareDeleteById", dict())

@app.get("/api/v1/storage-systems/device-type4/{systemId}/file-shares/{fileShareId}")
def DeviceType4FileShareGetById(systemId: str, fileShareId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/file-shares/{fileShareId}
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/file-shares"
    item_id = fileShareId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType4FileShareGetById", dict())
    return static_val

@app.patch("/api/v1/storage-systems/device-type4/{systemId}/file-shares/{fileShareId}")
def DeviceType4FileshareUpdate(systemId: str, fileShareId: str, payload: Devicetype4fileshareupdateRequest):
    """
    Dynamic CRUD Route: PATCH /api/v1/storage-systems/device-type4/{systemId}/file-shares/{fileShareId}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/file-shares"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    item_id = fileShareId
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = MOCK_DB["dynamic_store"][collection_path].get(item_id, {})
    existing.update(payload_dict)
    MOCK_DB["dynamic_store"][collection_path][item_id] = existing
    return existing

@app.get("/api/v1/storage-systems/device-type4/{systemId}/filesystems")
def DeviceType4FilesystemsList(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/filesystems
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/filesystems"
    static_data = MOCK_DB.get("DeviceType4FilesystemsList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.delete("/api/v1/storage-systems/device-type4/{systemId}/filesystems/{filesystemId}")
def FilesystemsDelete(systemId: str, filesystemId: str):
    """
    Dynamic CRUD Route: DELETE /api/v1/storage-systems/device-type4/{systemId}/filesystems/{filesystemId}
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/filesystems"
    item_id = filesystemId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        deleted = MOCK_DB["dynamic_store"][collection_path].pop(item_id)
        return {"message": "Deleted successfully", "id": item_id, "item": deleted}
    return MOCK_DB.get("FilesystemsDelete", dict())

@app.get("/api/v1/storage-systems/device-type4/{systemId}/filesystems/{filesystemId}")
def DeviceType4FilesystemGetById(systemId: str, filesystemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/filesystems/{filesystemId}
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/filesystems"
    item_id = filesystemId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType4FilesystemGetById", dict())
    return static_val

@app.get("/api/v1/storage-systems/device-type4/{systemId}/filesystems/{filesystemId}/capacity-history")
def DeviceType4FilesystemCapacityHistory(systemId: str, filesystemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/filesystems/{filesystemId}/capacity-history
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/filesystems/{filesystemId}/capacity-history"
    static_data = MOCK_DB.get("DeviceType4FilesystemCapacityHistory", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type4/{systemId}/filesystems/{filesystemId}/performance-history")
def DeviceType4FilesystemPerformanceHistory(systemId: str, filesystemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/filesystems/{filesystemId}/performance-history
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/filesystems/{filesystemId}/performance-history"
    static_data = MOCK_DB.get("DeviceType4FilesystemPerformanceHistory", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type4/{systemId}/host-paths")
def DeviceType4GetAllHostPaths(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/host-paths
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/host-paths"
    static_data = MOCK_DB.get("DeviceType4GetAllHostPaths", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type4/{systemId}/host-paths/{hostPathId}")
def DeviceType4GetHostPathsById(systemId: str, hostPathId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/host-paths/{hostPathId}
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/host-paths"
    item_id = hostPathId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType4GetHostPathsById", dict())
    return static_val

@app.get("/api/v1/storage-systems/device-type4/{systemId}/host-sets")
def DeviceType4GetAllHostSets(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/host-sets
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/host-sets"
    static_data = MOCK_DB.get("DeviceType4GetAllHostSets", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type4/{systemId}/host-sets/{hostSetId}")
def DeviceType4GetHostSetsById(systemId: str, hostSetId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/host-sets/{hostSetId}
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/host-sets"
    item_id = hostSetId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType4GetHostSetsById", dict())
    return static_val

@app.get("/api/v1/storage-systems/device-type4/{systemId}/hosts")
def DeviceType4GetAllHosts(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/hosts
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/hosts"
    static_data = MOCK_DB.get("DeviceType4GetAllHosts", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type4/{systemId}/hosts/{hostId}")
def DeviceType4GetHostById(systemId: str, hostId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/hosts/{hostId}
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/hosts"
    item_id = hostId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType4GetHostById", dict())
    return static_val

@app.get("/api/v1/storage-systems/device-type4/{systemId}/insights/headroom-contribution")
def DeviceType4GetHeadroomContribution(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/insights/headroom-contribution
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/insights/headroom-contribution"
    static_data = MOCK_DB.get("DeviceType4GetHeadroomContribution", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type4/{systemId}/insights/hotspots")
def DeviceType4GetHotspots(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/insights/hotspots
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/insights/hotspots"
    static_data = MOCK_DB.get("DeviceType4GetHotspots", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type4/{systemId}/insights/latencyfactors")
def Device4LatencyFactorsGet(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/insights/latencyfactors
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/insights/latencyfactors"
    static_data = MOCK_DB.get("Device4LatencyFactorsGet", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type4/{systemId}/insights/resource-contention")
def DeviceType4GetResourceContentionData(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/insights/resource-contention
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/insights/resource-contention"
    static_data = MOCK_DB.get("DeviceType4GetResourceContentionData", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type4/{systemId}/inventory-history")
def DeviceType4GetAllInventoryHistory(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/inventory-history
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/inventory-history"
    static_data = MOCK_DB.get("DeviceType4GetAllInventoryHistory", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type4/{systemId}/inventory-history/{inventoryUpdateId}")
def DeviceType4GetInventoryUpdateById(systemId: str, inventoryUpdateId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/inventory-history/{inventoryUpdateId}
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/inventory-history"
    item_id = inventoryUpdateId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType4GetInventoryUpdateById", dict())
    return static_val

@app.get("/api/v1/storage-systems/device-type4/{systemId}/licenses")
def DeviceType4LicensesGetById(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/licenses
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/licenses"
    static_data = MOCK_DB.get("DeviceType4LicensesGetById", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.post("/api/v1/storage-systems/device-type4/{systemId}/licenses")
def DeviceType4SetLicense(systemId: str, payload: Devicetype4setlicenseRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type4/{systemId}/licenses
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/licenses"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.delete("/api/v1/storage-systems/device-type4/{systemId}/mail-settings")
def DeviceType4MailSettingsDelete(systemId: str):
    """
    Dynamic CRUD Route: DELETE /api/v1/storage-systems/device-type4/{systemId}/mail-settings
    """
    return MOCK_DB.get("DeviceType4MailSettingsDelete", dict())

@app.get("/api/v1/storage-systems/device-type4/{systemId}/mail-settings")
def DeviceType4MailSettingsGet(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/mail-settings
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/mail-settings"
    static_data = MOCK_DB.get("DeviceType4MailSettingsGet", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.post("/api/v1/storage-systems/device-type4/{systemId}/mail-settings")
def DeviceType4MailSettingsAssociate(systemId: str, payload: Devicetype4mailsettingsassociateRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type4/{systemId}/mail-settings
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/mail-settings"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.put("/api/v1/storage-systems/device-type4/{systemId}/mail-settings")
def DeviceType4MailSettingsUpdate(systemId: str, payload: Devicetype4mailsettingsupdateRequest):
    """
    Dynamic CRUD Route: PUT /api/v1/storage-systems/device-type4/{systemId}/mail-settings
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/mail-settings"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})

    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type4/{systemId}/network-services/cim")
def DeviceType4NetworkServiceCimGet(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/network-services/cim
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/network-services/cim"
    static_data = MOCK_DB.get("DeviceType4NetworkServiceCimGet", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.put("/api/v1/storage-systems/device-type4/{systemId}/network-services/cim")
def DeviceType4NetworkServiceCimUpdate(systemId: str, payload: Devicetype4networkservicecimupdateRequest):
    """
    Dynamic CRUD Route: PUT /api/v1/storage-systems/device-type4/{systemId}/network-services/cim
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/network-services/cim"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})

    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type4/{systemId}/network-services/snmp-mgr")
def DeviceType4NetworkServiceSnmpMgrList(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/network-services/snmp-mgr
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/network-services/snmp-mgr"
    static_data = MOCK_DB.get("DeviceType4NetworkServiceSnmpMgrList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.post("/api/v1/storage-systems/device-type4/{systemId}/network-services/snmp-mgr")
def DeviceType4NetworkServiceSnmpMgrCreate(systemId: str, payload: Devicetype4networkservicesnmpmgrcreateRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type4/{systemId}/network-services/snmp-mgr
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/network-services/snmp-mgr"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.delete("/api/v1/storage-systems/device-type4/{systemId}/network-services/snmp-mgr/{id}")
def DeviceType4NetworkServiceSnmpMgrDelete(systemId: str, id: str):
    """
    Dynamic CRUD Route: DELETE /api/v1/storage-systems/device-type4/{systemId}/network-services/snmp-mgr/{id}
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/network-services/snmp-mgr"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        deleted = MOCK_DB["dynamic_store"][collection_path].pop(item_id)
        return {"message": "Deleted successfully", "id": item_id, "item": deleted}
    return MOCK_DB.get("DeviceType4NetworkServiceSnmpMgrDelete", dict())

@app.get("/api/v1/storage-systems/device-type4/{systemId}/network-services/snmp-mgr/{id}")
def DeviceType4NetworkServiceSnmpMgrGetById(systemId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/network-services/snmp-mgr/{id}
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/network-services/snmp-mgr"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType4NetworkServiceSnmpMgrGetById", dict())
    return static_val

@app.put("/api/v1/storage-systems/device-type4/{systemId}/network-services/snmp-mgr/{id}")
def DeviceType4NetworkServiceSnmpMgrUpdate(systemId: str, id: str, payload: Devicetype4networkservicesnmpmgrupdateRequest):
    """
    Dynamic CRUD Route: PUT /api/v1/storage-systems/device-type4/{systemId}/network-services/snmp-mgr/{id}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/network-services/snmp-mgr"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    item_id = id
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type4/{systemId}/network-services/snmp-users")
def DeviceType4SnmpUsersList(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/network-services/snmp-users
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/network-services/snmp-users"
    static_data = MOCK_DB.get("DeviceType4SnmpUsersList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type4/{systemId}/network-services/snmp-users/{id}")
def DeviceType4SnmpUsersGetById(systemId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/network-services/snmp-users/{id}
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/network-services/snmp-users"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType4SnmpUsersGetById", dict())
    return static_val

@app.get("/api/v1/storage-systems/device-type4/{systemId}/network-services/vasa")
def DeviceType4NetworkServiceVasaGet(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/network-services/vasa
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/network-services/vasa"
    static_data = MOCK_DB.get("DeviceType4NetworkServiceVasaGet", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.post("/api/v1/storage-systems/device-type4/{systemId}/network-services/vasa/{vasaId}")
def DeviceType4NetworkServiceVasaConfigure(systemId: str, vasaId: str, payload: Devicetype4networkservicevasaconfigureRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type4/{systemId}/network-services/vasa/{vasaId}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/network-services/vasa"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.post("/api/v1/storage-systems/device-type4/{systemId}/network-services/vasa/{vasaId}/services")
def DeviceType4NetworkServiceConfigureVasaService(systemId: str, vasaId: str, payload: Devicetype4networkserviceconfigurevasaserviceRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type4/{systemId}/network-services/vasa/{vasaId}/services
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/network-services/vasa/{vasaId}/services"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type4/{systemId}/network-settings")
def DeviceType4NetworkSettingsGet(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/network-settings
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/network-settings"
    static_data = MOCK_DB.get("DeviceType4NetworkSettingsGet", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.post("/api/v1/storage-systems/device-type4/{systemId}/network-settings")
def DeviceType4NetworkSettingsAssociate(systemId: str, payload: Devicetype4networksettingsassociateRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type4/{systemId}/network-settings
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/network-settings"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.post("/api/v1/storage-systems/device-type4/{systemId}/network-settings/vasaprovider")
def DeviceType4VasaProviderAddressConfigure(systemId: str, payload: Devicetype4vasaprovideraddressconfigureRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type4/{systemId}/network-settings/vasaprovider
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/network-settings/vasaprovider"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.post("/api/v1/storage-systems/device-type4/{systemId}/network-settings/vasaprovider/clear")
def DeviceType4VasaProviderAddressClear(systemId: str, payload: Devicetype4vasaprovideraddressclearRequest):
    return MOCK_DB.get("DeviceType4VasaProviderAddressClear", dict())

@app.get("/api/v1/storage-systems/device-type4/{systemId}/nodes")
def DeviceType4NodesList(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/nodes
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/nodes"
    static_data = MOCK_DB.get("DeviceType4NodesList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type4/{systemId}/nodes/{id}")
def DeviceType4NodesGetById(systemId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/nodes/{id}
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/nodes"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType4NodesGetById", dict())
    return static_val

@app.post("/api/v1/storage-systems/device-type4/{systemId}/nodes/{id}")
def DeviceType4NodesLocateById(systemId: str, id: str, payload: Devicetype4nodeslocatebyidRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type4/{systemId}/nodes/{id}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/nodes"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type4/{systemId}/nodes/{nodeId}/component-performance-statistics")
def DeviceType4NodeComponentPerformanceStatisticsGet(systemId: str, nodeId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/nodes/{nodeId}/component-performance-statistics
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/nodes/{nodeId}/component-performance-statistics"
    static_data = MOCK_DB.get("DeviceType4NodeComponentPerformanceStatisticsGet", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type4/{systemId}/nodes/{nodeId}/service-ports")
def DeviceType4NodeServicePortsGetById(systemId: str, nodeId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/nodes/{nodeId}/service-ports
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/nodes/{nodeId}/service-ports"
    static_data = MOCK_DB.get("DeviceType4NodeServicePortsGetById", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type4/{systemId}/nodes/service-ports")
def DeviceType4NodeServicePortsList(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/nodes/service-ports
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/nodes/service-ports"
    static_data = MOCK_DB.get("DeviceType4NodeServicePortsList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type4/{systemId}/performance-history")
def DeviceType4SystemPerformanceHistoryGet(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/performance-history
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/performance-history"
    static_data = MOCK_DB.get("DeviceType4SystemPerformanceHistoryGet", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type4/{systemId}/performance-statistics")
def DeviceType4GetSystemPerformanceStatistics(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/performance-statistics
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/performance-statistics"
    static_data = MOCK_DB.get("DeviceType4GetSystemPerformanceStatistics", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type4/{systemId}/physicaldrives-performance")
def DeviceType4PhysicalDrivePerformanceHistoryGet(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/physicaldrives-performance
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/physicaldrives-performance"
    static_data = MOCK_DB.get("DeviceType4PhysicalDrivePerformanceHistoryGet", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type4/{systemId}/ports")
def DeviceType4PortsList(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/ports
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/ports"
    static_data = MOCK_DB.get("DeviceType4PortsList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type4/{systemId}/ports-performance")
def DeviceType4PortsPerformanceHistoryGet(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/ports-performance
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/ports-performance"
    static_data = MOCK_DB.get("DeviceType4PortsPerformanceHistoryGet", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type4/{systemId}/ports/{id}")
def DeviceType4PortsGetById(systemId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/ports/{id}
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/ports"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType4PortsGetById", dict())
    return static_val

@app.post("/api/v1/storage-systems/device-type4/{systemId}/ports/{id}")
def DeviceType4PortEnable(systemId: str, id: str, payload: Devicetype4portenableRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type4/{systemId}/ports/{id}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/ports"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.post("/api/v1/storage-systems/device-type4/{systemId}/ports/{id}/clear")
def DeviceType4PortsClear(systemId: str, id: str, payload: Devicetype4portsclearRequest):
    return MOCK_DB.get("DeviceType4PortsClear", dict())

@app.put("/api/v1/storage-systems/device-type4/{systemId}/ports/{id}/edit-file")
def DeviceType4FilePortEdit(systemId: str, id: str, payload: Devicetype4fileporteditRequest):
    """
    Dynamic CRUD Route: PUT /api/v1/storage-systems/device-type4/{systemId}/ports/{id}/edit-file
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/ports/{id}/edit-file"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})

    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.put("/api/v1/storage-systems/device-type4/{systemId}/ports/{id}/edit-iscsi")
def DeviceType4IscsiPortEdit(systemId: str, id: str, payload: Devicetype4iscsiporteditRequest):
    """
    Dynamic CRUD Route: PUT /api/v1/storage-systems/device-type4/{systemId}/ports/{id}/edit-iscsi
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/ports/{id}/edit-iscsi"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})

    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.put("/api/v1/storage-systems/device-type4/{systemId}/ports/{id}/edit-nvme")
def DeviceType4NVMePortEdit(systemId: str, id: str, payload: Devicetype4nvmeporteditRequest):
    """
    Dynamic CRUD Route: PUT /api/v1/storage-systems/device-type4/{systemId}/ports/{id}/edit-nvme
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/ports/{id}/edit-nvme"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})

    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.put("/api/v1/storage-systems/device-type4/{systemId}/ports/{id}/edit-rcip")
def DeviceType4RcipPortEdit(systemId: str, id: str, payload: Devicetype4rcipporteditRequest):
    """
    Dynamic CRUD Route: PUT /api/v1/storage-systems/device-type4/{systemId}/ports/{id}/edit-rcip
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/ports/{id}/edit-rcip"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})

    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.put("/api/v1/storage-systems/device-type4/{systemId}/ports/{id}/fc")
def DeviceType4FcPortEdit(systemId: str, id: str, payload: Devicetype4fcporteditRequest):
    """
    Dynamic CRUD Route: PUT /api/v1/storage-systems/device-type4/{systemId}/ports/{id}/fc
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/ports/{id}/fc"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})

    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.post("/api/v1/storage-systems/device-type4/{systemId}/ports/{id}/initialize")
def DeviceType4initialisePorts(systemId: str, id: str):
    return MOCK_DB.get("DeviceType4initialisePorts", dict())

@app.post("/api/v1/storage-systems/device-type4/{systemId}/ports/{id}/ping-file")
def DeviceType4FilePortPing(systemId: str, id: str, payload: Devicetype4fileportpingRequest):
    return MOCK_DB.get("DeviceType4FilePortPing", dict())

@app.post("/api/v1/storage-systems/device-type4/{systemId}/ports/{id}/ping-iscsi")
def DeviceType4IscsiPortPing(systemId: str, id: str, payload: Devicetype4iscsiportpingRequest):
    return MOCK_DB.get("DeviceType4IscsiPortPing", dict())

@app.post("/api/v1/storage-systems/device-type4/{systemId}/ports/{id}/ping-nvme")
def DeviceType4NVMePortPing(systemId: str, id: str, payload: Devicetype4nvmeportpingRequest):
    return MOCK_DB.get("DeviceType4NVMePortPing", dict())

@app.post("/api/v1/storage-systems/device-type4/{systemId}/ports/{id}/ping-rcip")
def DeviceType4RcipPortPing(systemId: str, id: str, payload: Devicetype4rcipportpingRequest):
    return MOCK_DB.get("DeviceType4RcipPortPing", dict())

@app.get("/api/v1/storage-systems/device-type4/{systemId}/remotecopylinks-performance")
def DeviceType4RemoteCopyLinksPerformanceHistoryGet(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/remotecopylinks-performance
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/remotecopylinks-performance"
    static_data = MOCK_DB.get("DeviceType4RemoteCopyLinksPerformanceHistoryGet", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type4/{systemId}/share-settings")
def DeviceType4ShareSettingsList(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/share-settings
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/share-settings"
    static_data = MOCK_DB.get("DeviceType4ShareSettingsList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type4/{systemId}/share-settings/{sharesettingsId}")
def DeviceType4ShareSettingsGetById(systemId: str, sharesettingsId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/share-settings/{sharesettingsId}
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/share-settings"
    item_id = sharesettingsId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType4ShareSettingsGetById", dict())
    return static_val

@app.get("/api/v1/storage-systems/device-type4/{systemId}/snapshots/{childSnapshotId}/restore-options")
def DeviceType4GetSnapshotRestoreOptions(systemId: str, childSnapshotId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/snapshots/{childSnapshotId}/restore-options
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/snapshots/{childSnapshotId}/restore-options"
    static_data = MOCK_DB.get("DeviceType4GetSnapshotRestoreOptions", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.post("/api/v1/storage-systems/device-type4/{systemId}/snapshots/{parentSnapshotId}/snapshots/{childSnapshotId}/restore")
def DeviceType4RestoreSnapshotOfSnapshot(systemId: str, parentSnapshotId: str, childSnapshotId: str, payload: Devicetype4restoresnapshotofsnapshotRequest):
    return MOCK_DB.get("DeviceType4RestoreSnapshotOfSnapshot", dict())

@app.post("/api/v1/storage-systems/device-type4/{systemId}/snapshots/{snapshotId}/clone")
def DeviceType4SnapshotCloneCreate(systemId: str, snapshotId: str, payload: Devicetype4snapshotclonecreateRequest):
    return MOCK_DB.get("DeviceType4SnapshotCloneCreate", dict())

@app.post("/api/v1/storage-systems/device-type4/{systemId}/snapshots/{snapshotId}/export")
def DeviceType4VlunExportForSnapshot(systemId: str, snapshotId: str, payload: Devicetype4vlunexportforsnapshotRequest):
    return MOCK_DB.get("DeviceType4VlunExportForSnapshot", dict())

@app.post("/api/v1/storage-systems/device-type4/{systemId}/snapshots/{snapshotId}/snapshots")
def DeviceType4SnapshotOfSnapshotCreate(systemId: str, snapshotId: str, payload: Devicetype4snapshotofsnapshotcreateRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type4/{systemId}/snapshots/{snapshotId}/snapshots
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/snapshots/{snapshotId}/snapshots"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.post("/api/v1/storage-systems/device-type4/{systemId}/snapshots/{snapshotId}/un-export")
def DeviceType4VlunUnexportForSnapshot(systemId: str, snapshotId: str, payload: Devicetype4vlununexportforsnapshotRequest):
    return MOCK_DB.get("DeviceType4VlunUnexportForSnapshot", dict())

@app.get("/api/v1/storage-systems/device-type4/{systemId}/snapshots/{snapshotId}/vluns")
def DeviceType4GetSnapshotVlunsList(systemId: str, snapshotId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/snapshots/{snapshotId}/vluns
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/snapshots/{snapshotId}/vluns"
    static_data = MOCK_DB.get("DeviceType4GetSnapshotVlunsList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type4/{systemId}/snapshots/{snapshotId}/vluns/{id}")
def DeviceType4GetsnapshotVlunsById(systemId: str, snapshotId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/snapshots/{snapshotId}/vluns/{id}
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/snapshots/{snapshotId}/vluns"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType4GetsnapshotVlunsById", dict())
    return static_val

@app.get("/api/v1/storage-systems/device-type4/{systemId}/storage-pools")
def DeviceType4StoragePoolList(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/storage-pools
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/storage-pools"
    static_data = MOCK_DB.get("DeviceType4StoragePoolList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type4/{systemId}/storage-pools/{id}")
def DeviceType4StoragePoolGetById(systemId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/storage-pools/{id}
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/storage-pools"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType4StoragePoolGetById", dict())
    return static_val

@app.get("/api/v1/storage-systems/device-type4/{systemId}/storage-pools/{id}/volumes")
def DeviceType4StoragePoolVolumeGetById(systemId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/storage-pools/{id}/volumes
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/storage-pools/{id}/volumes"
    static_data = MOCK_DB.get("DeviceType4StoragePoolVolumeGetById", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type4/{systemId}/support-settings")
def DeviceType4SupportSettingsGet(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/support-settings
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/support-settings"
    static_data = MOCK_DB.get("DeviceType4SupportSettingsGet", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.post("/api/v1/storage-systems/device-type4/{systemId}/support-settings")
def DeviceType4SupportSettingsAssociate(systemId: str, payload: Devicetype4supportsettingsassociateRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type4/{systemId}/support-settings
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/support-settings"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.put("/api/v1/storage-systems/device-type4/{systemId}/support-settings")
def DeviceType4SupportSettingsUpdate(systemId: str, payload: Devicetype4supportsettingsupdateRequest):
    """
    Dynamic CRUD Route: PUT /api/v1/storage-systems/device-type4/{systemId}/support-settings
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/support-settings"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})

    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type4/{systemId}/sustainabilityMetrics")
def DeviceType4EnclosurePowersSustainability(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/sustainabilityMetrics
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/sustainabilityMetrics"
    static_data = MOCK_DB.get("DeviceType4EnclosurePowersSustainability", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type4/{systemId}/switch-ports")
def DeviceType4SwitchPortsList(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/switch-ports
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/switch-ports"
    static_data = MOCK_DB.get("DeviceType4SwitchPortsList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type4/{systemId}/switches")
def DeviceType4SwitchesList(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/switches
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/switches"
    static_data = MOCK_DB.get("DeviceType4SwitchesList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type4/{systemId}/switches/{id}")
def DeviceType4SwitchesGetById(systemId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/switches/{id}
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/switches"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType4SwitchesGetById", dict())
    return static_val

@app.post("/api/v1/storage-systems/device-type4/{systemId}/switches/{id}")
def DeviceType4SwitchLocateById(systemId: str, id: str, payload: Devicetype4switchlocatebyidRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type4/{systemId}/switches/{id}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/switches"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type4/{systemId}/switches/{switchId}/switch-fans")
def DeviceType4SwitchFanList(systemId: str, switchId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/switches/{switchId}/switch-fans
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/switches/{switchId}/switch-fans"
    static_data = MOCK_DB.get("DeviceType4SwitchFanList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type4/{systemId}/switches/{switchId}/switch-fans/{id}")
def DeviceType4SwitchFanGetById(systemId: str, switchId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/switches/{switchId}/switch-fans/{id}
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/switches/{switchId}/switch-fans"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType4SwitchFanGetById", dict())
    return static_val

@app.get("/api/v1/storage-systems/device-type4/{systemId}/switches/{switchId}/switch-ports")
def DeviceType4SwitchPortList(systemId: str, switchId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/switches/{switchId}/switch-ports
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/switches/{switchId}/switch-ports"
    static_data = MOCK_DB.get("DeviceType4SwitchPortList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type4/{systemId}/switches/{switchId}/switch-ports/{id}")
def DeviceType4SwitchPortGetById(systemId: str, switchId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/switches/{switchId}/switch-ports/{id}
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/switches/{switchId}/switch-ports"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType4SwitchPortGetById", dict())
    return static_val

@app.get("/api/v1/storage-systems/device-type4/{systemId}/switches/{switchId}/switch-ps")
def DeviceType4SwitchPSList(systemId: str, switchId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/switches/{switchId}/switch-ps
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/switches/{switchId}/switch-ps"
    static_data = MOCK_DB.get("DeviceType4SwitchPSList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type4/{systemId}/switches/{switchId}/switch-ps/{id}")
def DeviceType4SwitchPSGetById(systemId: str, switchId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/switches/{switchId}/switch-ps/{id}
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/switches/{switchId}/switch-ps"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType4SwitchPSGetById", dict())
    return static_val

@app.get("/api/v1/storage-systems/device-type4/{systemId}/system-settings")
def DeviceType4SystemSettingsList(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/system-settings
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/system-settings"
    static_data = MOCK_DB.get("DeviceType4SystemSettingsList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.post("/api/v1/storage-systems/device-type4/{systemId}/system-settings")
def DeviceType4SystemSettingsAssociate(systemId: str, payload: Devicetype4systemsettingsassociateRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type4/{systemId}/system-settings
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/system-settings"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.put("/api/v1/storage-systems/device-type4/{systemId}/system-settings")
def DeviceType4SystemSettingsUpdate(systemId: str, payload: Devicetype4systemsettingsupdateRequest):
    """
    Dynamic CRUD Route: PUT /api/v1/storage-systems/device-type4/{systemId}/system-settings
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/system-settings"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})

    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type4/{systemId}/system-settings/management-services/vvol")
def DeviceType4vVolGet(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/system-settings/management-services/vvol
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/system-settings/management-services/vvol"
    static_data = MOCK_DB.get("DeviceType4vVolGet", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type4/{systemId}/system-settings/management-services/vvolscs")
def DeviceType4StorageContainerGet(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/system-settings/management-services/vvolscs
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/system-settings/management-services/vvolscs"
    static_data = MOCK_DB.get("DeviceType4StorageContainerGet", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.post("/api/v1/storage-systems/device-type4/{systemId}/system-settings/management-services/vvolscs")
def DeviceType4CreatevVolSC(systemId: str, payload: Devicetype4createvvolscRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type4/{systemId}/system-settings/management-services/vvolscs
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/system-settings/management-services/vvolscs"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.delete("/api/v1/storage-systems/device-type4/{systemId}/system-settings/management-services/vvolscs/{vvolscId}")
def DeviceType4StorageContainerDeleteById(systemId: str, vvolscId: str):
    """
    Dynamic CRUD Route: DELETE /api/v1/storage-systems/device-type4/{systemId}/system-settings/management-services/vvolscs/{vvolscId}
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/system-settings/management-services/vvolscs"
    item_id = vvolscId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        deleted = MOCK_DB["dynamic_store"][collection_path].pop(item_id)
        return {"message": "Deleted successfully", "id": item_id, "item": deleted}
    return MOCK_DB.get("DeviceType4StorageContainerDeleteById", dict())

@app.put("/api/v1/storage-systems/device-type4/{systemId}/system-settings/management-services/vvolscs/{vvolscId}")
def DeviceType4StorageContainerEditById(systemId: str, vvolscId: str, payload: Devicetype4storagecontainereditbyidRequest):
    """
    Dynamic CRUD Route: PUT /api/v1/storage-systems/device-type4/{systemId}/system-settings/management-services/vvolscs/{vvolscId}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/system-settings/management-services/vvolscs"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    item_id = vvolscId
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.post("/api/v1/storage-systems/device-type4/{systemId}/system-settings/management-services/vvolscs/{vvolscId}/attach")
def DeviceType4AttachVolSC(systemId: str, vvolscId: str, payload: Devicetype4attachvolscRequest):
    return MOCK_DB.get("DeviceType4AttachVolSC", dict())

@app.post("/api/v1/storage-systems/device-type4/{systemId}/system-settings/management-services/vvolscs/{vvolscId}/detach")
def DeviceType4DetachVolSC(systemId: str, vvolscId: str, payload: Devicetype4detachvolscRequest):
    return MOCK_DB.get("DeviceType4DetachVolSC", dict())

@app.get("/api/v1/storage-systems/device-type4/{systemId}/system-settings/quorum-witness")
def DeviceType4GetQuorumWitness(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/system-settings/quorum-witness
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/system-settings/quorum-witness"
    static_data = MOCK_DB.get("DeviceType4GetQuorumWitness", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.post("/api/v1/storage-systems/device-type4/{systemId}/system-settings/quorum-witness")
def DeviceType4PostQuorumWitness(systemId: str, payload: Devicetype4postquorumwitnessRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type4/{systemId}/system-settings/quorum-witness
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/system-settings/quorum-witness"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.delete("/api/v1/storage-systems/device-type4/{systemId}/system-settings/quorum-witness/{replicationPartnerId}")
def DeviceType4DeleteQuorumWitness(systemId: str, replicationPartnerId: str):
    """
    Dynamic CRUD Route: DELETE /api/v1/storage-systems/device-type4/{systemId}/system-settings/quorum-witness/{replicationPartnerId}
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/system-settings/quorum-witness"
    item_id = replicationPartnerId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        deleted = MOCK_DB["dynamic_store"][collection_path].pop(item_id)
        return {"message": "Deleted successfully", "id": item_id, "item": deleted}
    return MOCK_DB.get("DeviceType4DeleteQuorumWitness", dict())

@app.get("/api/v1/storage-systems/device-type4/{systemId}/system-settings/quorum-witness/{replicationPartnerId}")
def DeviceType4GetQuorumWitnessWithId(systemId: str, replicationPartnerId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/system-settings/quorum-witness/{replicationPartnerId}
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/system-settings/quorum-witness"
    item_id = replicationPartnerId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType4GetQuorumWitnessWithId", dict())
    return static_val

@app.put("/api/v1/storage-systems/device-type4/{systemId}/system-settings/quorum-witness/{replicationPartnerId}")
def DeviceType4PutQuorumWitness(systemId: str, replicationPartnerId: str, payload: Devicetype4putquorumwitnessRequest):
    """
    Dynamic CRUD Route: PUT /api/v1/storage-systems/device-type4/{systemId}/system-settings/quorum-witness/{replicationPartnerId}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/system-settings/quorum-witness"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    item_id = replicationPartnerId
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type4/{systemId}/system-settings/replication-partners")
def DeviceType4GetReplicationPartners(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/system-settings/replication-partners
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/system-settings/replication-partners"
    static_data = MOCK_DB.get("DeviceType4GetReplicationPartners", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.post("/api/v1/storage-systems/device-type4/{systemId}/system-settings/replication-partners")
def DeviceType4PostReplicationPartners(systemId: str, payload: Devicetype4postreplicationpartnersRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type4/{systemId}/system-settings/replication-partners
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/system-settings/replication-partners"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type4/{systemId}/system-settings/replication-partners/{replicationPartnerId}")
def DeviceType4GetReplicationPartnerWithId(systemId: str, replicationPartnerId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/system-settings/replication-partners/{replicationPartnerId}
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/system-settings/replication-partners"
    item_id = replicationPartnerId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType4GetReplicationPartnerWithId", dict())
    return static_val

@app.put("/api/v1/storage-systems/device-type4/{systemId}/system-settings/replication-partners/{replicationPartnerId}")
def DeviceType4PutReplicationPartner(systemId: str, replicationPartnerId: str, payload: Devicetype4putreplicationpartnerRequest):
    """
    Dynamic CRUD Route: PUT /api/v1/storage-systems/device-type4/{systemId}/system-settings/replication-partners/{replicationPartnerId}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/system-settings/replication-partners"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    item_id = replicationPartnerId
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.post("/api/v1/storage-systems/device-type4/{systemId}/system-settings/replication-partners/remove")
def DeviceType4PostRemoveReplicationPartners(systemId: str, payload: Devicetype4postremovereplicationpartnersRequest):
    return MOCK_DB.get("DeviceType4PostRemoveReplicationPartners", dict())

@app.get("/api/v1/storage-systems/device-type4/{systemId}/telemetry")
def DeviceType4TelemetryGet(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/telemetry
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/telemetry"
    static_data = MOCK_DB.get("DeviceType4TelemetryGet", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type4/{systemId}/trust-certificates")
def DeviceType4TrustedCertificatesList(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/trust-certificates
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/trust-certificates"
    static_data = MOCK_DB.get("DeviceType4TrustedCertificatesList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.post("/api/v1/storage-systems/device-type4/{systemId}/trust-certificates")
def DeviceType4AddTrustedCertificates(systemId: str, payload: Devicetype4addtrustedcertificatesRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type4/{systemId}/trust-certificates
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/trust-certificates"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type4/{systemId}/trust-certificates/{id}")
def DeviceType4TrustedCertificatesGetById(systemId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/trust-certificates/{id}
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/trust-certificates"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType4TrustedCertificatesGetById", dict())
    return static_val

@app.post("/api/v1/storage-systems/device-type4/{systemId}/trust-certificates/remove")
def DeviceType4RemoveTrustedCertificates(systemId: str, payload: Devicetype4removetrustedcertificatesRequest):
    return MOCK_DB.get("DeviceType4RemoveTrustedCertificates", dict())

@app.get("/api/v1/storage-systems/device-type4/{systemId}/vm-manager-settings")
def DeviceType4VMManagerSettingsList(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/vm-manager-settings
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/vm-manager-settings"
    static_data = MOCK_DB.get("DeviceType4VMManagerSettingsList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.post("/api/v1/storage-systems/device-type4/{systemId}/vm-manager-settings")
def DeviceType4PostVCenterSettings(systemId: str, payload: Devicetype4postvcentersettingsRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type4/{systemId}/vm-manager-settings
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/vm-manager-settings"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.delete("/api/v1/storage-systems/device-type4/{systemId}/vm-manager-settings/{vcenterSettingId}")
def DeviceType4DeleteVCenterSettings(systemId: str, vcenterSettingId: str):
    """
    Dynamic CRUD Route: DELETE /api/v1/storage-systems/device-type4/{systemId}/vm-manager-settings/{vcenterSettingId}
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/vm-manager-settings"
    item_id = vcenterSettingId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        deleted = MOCK_DB["dynamic_store"][collection_path].pop(item_id)
        return {"message": "Deleted successfully", "id": item_id, "item": deleted}
    return MOCK_DB.get("DeviceType4DeleteVCenterSettings", dict())

@app.get("/api/v1/storage-systems/device-type4/{systemId}/vm-manager-settings/{vcenterSettingId}")
def DeviceType4VMManagerSettingsGetById(systemId: str, vcenterSettingId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/vm-manager-settings/{vcenterSettingId}
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/vm-manager-settings"
    item_id = vcenterSettingId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType4VMManagerSettingsGetById", dict())
    return static_val

@app.put("/api/v1/storage-systems/device-type4/{systemId}/vm-manager-settings/{vcenterSettingId}")
def DeviceType4PutVCenterSettings(systemId: str, vcenterSettingId: str, payload: Devicetype4putvcentersettingsRequest):
    """
    Dynamic CRUD Route: PUT /api/v1/storage-systems/device-type4/{systemId}/vm-manager-settings/{vcenterSettingId}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/vm-manager-settings"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    item_id = vcenterSettingId
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type4/{systemId}/vme-manager-settings")
def DeviceType4VMEManagerSettingsList(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/vme-manager-settings
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/vme-manager-settings"
    static_data = MOCK_DB.get("DeviceType4VMEManagerSettingsList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.post("/api/v1/storage-systems/device-type4/{systemId}/vme-manager-settings")
def DeviceType4PostVMESettings(systemId: str, payload: Devicetype4postvmesettingsRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type4/{systemId}/vme-manager-settings
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/vme-manager-settings"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.delete("/api/v1/storage-systems/device-type4/{systemId}/vme-manager-settings/{vmeSettingId}")
def DeviceType4DeleteVMESettings(systemId: str, vmeSettingId: str):
    """
    Dynamic CRUD Route: DELETE /api/v1/storage-systems/device-type4/{systemId}/vme-manager-settings/{vmeSettingId}
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/vme-manager-settings"
    item_id = vmeSettingId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        deleted = MOCK_DB["dynamic_store"][collection_path].pop(item_id)
        return {"message": "Deleted successfully", "id": item_id, "item": deleted}
    return MOCK_DB.get("DeviceType4DeleteVMESettings", dict())

@app.get("/api/v1/storage-systems/device-type4/{systemId}/vme-manager-settings/{vmeSettingId}")
def DeviceType4VMEManagerSettingsGetById(systemId: str, vmeSettingId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/vme-manager-settings/{vmeSettingId}
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/vme-manager-settings"
    item_id = vmeSettingId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType4VMEManagerSettingsGetById", dict())
    return static_val

@app.put("/api/v1/storage-systems/device-type4/{systemId}/vme-manager-settings/{vmeSettingId}")
def DeviceType4PutVMESettings(systemId: str, vmeSettingId: str, payload: Devicetype4putvmesettingsRequest):
    """
    Dynamic CRUD Route: PUT /api/v1/storage-systems/device-type4/{systemId}/vme-manager-settings/{vmeSettingId}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/vme-manager-settings"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    item_id = vmeSettingId
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type4/{systemId}/volumes")
def DeviceType4VolumesList(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/volumes
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/volumes"
    static_data = MOCK_DB.get("DeviceType4VolumesList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.post("/api/v1/storage-systems/device-type4/{systemId}/volumes")
def DeviceType4VolumeCreate(systemId: str, payload: Devicetype4volumecreateRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type4/{systemId}/volumes
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/volumes"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type4/{systemId}/volumes-performance")
def DeviceType4GetVolumesPerformanceHistory(systemId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/volumes-performance
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/volumes-performance"
    static_data = MOCK_DB.get("DeviceType4GetVolumesPerformanceHistory", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.delete("/api/v1/storage-systems/device-type4/{systemId}/volumes/{id}")
def DeviceType4VolumeDelete(systemId: str, id: str):
    """
    Dynamic CRUD Route: DELETE /api/v1/storage-systems/device-type4/{systemId}/volumes/{id}
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/volumes"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        deleted = MOCK_DB["dynamic_store"][collection_path].pop(item_id)
        return {"message": "Deleted successfully", "id": item_id, "item": deleted}
    return MOCK_DB.get("DeviceType4VolumeDelete", dict())

@app.get("/api/v1/storage-systems/device-type4/{systemId}/volumes/{id}")
def DeviceType4VolumeGetById(systemId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/volumes/{id}
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/volumes"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType4VolumeGetById", dict())
    return static_val

@app.put("/api/v1/storage-systems/device-type4/{systemId}/volumes/{id}")
def DeviceType4VolumeEdit(systemId: str, id: str, payload: Devicetype4volumeeditRequest):
    """
    Dynamic CRUD Route: PUT /api/v1/storage-systems/device-type4/{systemId}/volumes/{id}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/volumes"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    item_id = id
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/device-type4/{systemId}/volumes/{id}/capacity-history")
def DeviceType4VolumeCapacityHistoryGetById(systemId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/volumes/{id}/capacity-history
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/volumes/{id}/capacity-history"
    static_data = MOCK_DB.get("DeviceType4VolumeCapacityHistoryGetById", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.post("/api/v1/storage-systems/device-type4/{systemId}/volumes/{id}/clone")
def DeviceType4VolumeCloneCreate(systemId: str, id: str, payload: Devicetype4volumeclonecreateRequest):
    return MOCK_DB.get("DeviceType4VolumeCloneCreate", dict())

@app.post("/api/v1/storage-systems/device-type4/{systemId}/volumes/{id}/export")
def DeviceType4VlunExport(systemId: str, id: str, payload: Devicetype4vlunexportRequest):
    return MOCK_DB.get("DeviceType4VlunExport", dict())

@app.get("/api/v1/storage-systems/device-type4/{systemId}/volumes/{id}/performance-histogram")
def DeviceType4GetPerformanceHistogram(systemId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/volumes/{id}/performance-histogram
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/volumes/{id}/performance-histogram"
    static_data = MOCK_DB.get("DeviceType4GetPerformanceHistogram", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type4/{systemId}/volumes/{id}/performance-history")
def DeviceType4VolumePerformanceHistoryGetById(systemId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/volumes/{id}/performance-history
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/volumes/{id}/performance-history"
    static_data = MOCK_DB.get("DeviceType4VolumePerformanceHistoryGetById", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type4/{systemId}/volumes/{id}/performance-statistics")
def DeviceType4VolumePerformanceStatisticsGetById(systemId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/volumes/{id}/performance-statistics
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/volumes/{id}/performance-statistics"
    static_data = MOCK_DB.get("DeviceType4VolumePerformanceStatisticsGetById", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type4/{systemId}/volumes/{id}/snapshots")
def DeviceType4VolumeSnapshotsList(systemId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/volumes/{id}/snapshots
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/volumes/{id}/snapshots"
    static_data = MOCK_DB.get("DeviceType4VolumeSnapshotsList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.post("/api/v1/storage-systems/device-type4/{systemId}/volumes/{id}/snapshots")
def DeviceType4VolumeSnapshotCreate(systemId: str, id: str, payload: Devicetype4volumesnapshotcreateRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type4/{systemId}/volumes/{id}/snapshots
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/volumes/{id}/snapshots"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.post("/api/v1/storage-systems/device-type4/{systemId}/volumes/{id}/un-export")
def DeviceType4VlunUnexport(systemId: str, id: str, payload: Devicetype4vlununexportRequest):
    return MOCK_DB.get("DeviceType4VlunUnexport", dict())

@app.get("/api/v1/storage-systems/device-type4/{systemId}/volumes/{id}/vluns")
def DeviceType4VlunsList(systemId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/volumes/{id}/vluns
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/volumes/{id}/vluns"
    static_data = MOCK_DB.get("DeviceType4VlunsList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/clones")
def DeviceType4GetClones(systemId: str, volumeId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/clones
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/clones"
    static_data = MOCK_DB.get("DeviceType4GetClones", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.put("/api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/clones/{cloneId}")
def DeviceType4EditCloneVolume(systemId: str, volumeId: str, cloneId: str, payload: Devicetype4editclonevolumeRequest):
    """
    Dynamic CRUD Route: PUT /api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/clones/{cloneId}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/clones"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    item_id = cloneId
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.post("/api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/clones/{cloneId}/promote")
def DeviceType4PromoteCloneVolume(systemId: str, volumeId: str, cloneId: str, payload: Devicetype4promoteclonevolumeRequest):
    return MOCK_DB.get("DeviceType4PromoteCloneVolume", dict())

@app.post("/api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/clones/{cloneId}/resync")
def DeviceType4ResyncCloneVolume(systemId: str, volumeId: str, cloneId: str, payload: Devicetype4resyncclonevolumeRequest):
    return MOCK_DB.get("DeviceType4ResyncCloneVolume", dict())

@app.get("/api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/insights/latency-annotations")
def DeviceType4GetVolumeLatencyAnnotations(systemId: str, volumeId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/insights/latency-annotations
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/insights/latency-annotations"
    static_data = MOCK_DB.get("DeviceType4GetVolumeLatencyAnnotations", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/insights/performance-drifts")
def DeviceType4GetPerformanceDrifts(systemId: str, volumeId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/insights/performance-drifts
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/insights/performance-drifts"
    static_data = MOCK_DB.get("DeviceType4GetPerformanceDrifts", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/schedules")
def DeviceType4VolumeSnapshotSchedulesList(systemId: str, volumeId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/schedules
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/schedules"
    static_data = MOCK_DB.get("DeviceType4VolumeSnapshotSchedulesList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.post("/api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/schedules")
def DeviceType4VolumeSnapshotScheduleCreate(systemId: str, volumeId: str, payload: Devicetype4volumesnapshotschedulecreateRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/schedules
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/schedules"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.delete("/api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/schedules/{scheduleId}")
def DeviceType4VolumeSnapshotScheduleDelete(systemId: str, volumeId: str, scheduleId: str):
    """
    Dynamic CRUD Route: DELETE /api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/schedules/{scheduleId}
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/schedules"
    item_id = scheduleId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        deleted = MOCK_DB["dynamic_store"][collection_path].pop(item_id)
        return {"message": "Deleted successfully", "id": item_id, "item": deleted}
    return MOCK_DB.get("DeviceType4VolumeSnapshotScheduleDelete", dict())

@app.get("/api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/schedules/{scheduleId}")
def DeviceType4VolumeSnapshotScheduleGetById(systemId: str, volumeId: str, scheduleId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/schedules/{scheduleId}
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/schedules"
    item_id = scheduleId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType4VolumeSnapshotScheduleGetById", dict())
    return static_val

@app.put("/api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/schedules/{scheduleId}")
def arcusEditVolumeSnapshotSchedule(systemId: str, volumeId: str, scheduleId: str, payload: ArcuseditvolumesnapshotscheduleRequest):
    """
    Dynamic CRUD Route: PUT /api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/schedules/{scheduleId}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/schedules"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    item_id = scheduleId
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.delete("/api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/snapshots/{snapshotId}")
def DeviceType4VolumeSnapshotGetById(systemId: str, volumeId: str, snapshotId: str):
    """
    Dynamic CRUD Route: DELETE /api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/snapshots/{snapshotId}
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/snapshots"
    item_id = snapshotId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        deleted = MOCK_DB["dynamic_store"][collection_path].pop(item_id)
        return {"message": "Deleted successfully", "id": item_id, "item": deleted}
    return MOCK_DB.get("DeviceType4VolumeSnapshotGetById", dict())

@app.get("/api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/snapshots/{snapshotId}")
def DeviceType4SnapshotsGetById(systemId: str, volumeId: str, snapshotId: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/snapshots/{snapshotId}
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/snapshots"
    item_id = snapshotId
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType4SnapshotsGetById", dict())
    return static_val

@app.post("/api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/snapshots/{snapshotId}")
def DeviceType4PromoteSnapshot(systemId: str, volumeId: str, snapshotId: str, payload: Devicetype4promotesnapshotRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/snapshots/{snapshotId}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/snapshots"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.put("/api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/snapshots/{snapshotId}")
def DeviceType4EditSnapshot(systemId: str, volumeId: str, snapshotId: str, payload: Devicetype4editsnapshotRequest):
    """
    Dynamic CRUD Route: PUT /api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/snapshots/{snapshotId}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/snapshots"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    item_id = snapshotId
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.delete("/api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/vluns/{id}")
def DeviceType4VlunsDelete(systemId: str, volumeId: str, id: str):
    """
    Dynamic CRUD Route: DELETE /api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/vluns/{id}
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/vluns"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        deleted = MOCK_DB["dynamic_store"][collection_path].pop(item_id)
        return {"message": "Deleted successfully", "id": item_id, "item": deleted}
    return MOCK_DB.get("DeviceType4VlunsDelete", dict())

@app.get("/api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/vluns/{id}")
def DeviceType4VlunsGetById(systemId: str, volumeId: str, id: str):
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/vluns/{id}
    """
    collection_path = f"/api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/vluns"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("DeviceType4VlunsGetById", dict())
    return static_val

@app.get("/api/v1/storage-systems/device-type4/systemInsights/insights")
def DeviceType4Insights():
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/device-type4/systemInsights/insights
    """
    collection_path = f"/api/v1/storage-systems/device-type4/systemInsights/insights"
    static_data = MOCK_DB.get("DeviceType4Insights", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.post("/api/v1/storage-systems/provisioning-recommendations")
def ProvisioningRecommendations(payload: ProvisioningrecommendationsRequest):
    """
    Dynamic CRUD Route: POST /api/v1/storage-systems/provisioning-recommendations
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/api/v1/storage-systems/provisioning-recommendations"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/api/v1/storage-systems/storage-types")
def GetDeviceType():
    """
    Dynamic CRUD Route: GET /api/v1/storage-systems/storage-types
    """
    collection_path = f"/api/v1/storage-systems/storage-types"
    static_data = MOCK_DB.get("GetDeviceType", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/tasks")
def ListTasks():
    """
    Dynamic CRUD Route: GET /api/v1/tasks
    """
    collection_path = f"/api/v1/tasks"
    static_data = MOCK_DB.get("ListTasks", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/tasks/{id}")
def GetTask(id: str):
    """
    Dynamic CRUD Route: GET /api/v1/tasks/{id}
    """
    collection_path = f"/api/v1/tasks"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("GetTask", dict())
    return static_val

@app.get("/api/v1/volume-sets")
def VolumesetList():
    """
    Dynamic CRUD Route: GET /api/v1/volume-sets
    """
    collection_path = f"/api/v1/volume-sets"
    static_data = MOCK_DB.get("VolumesetList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/volume-sets/{id}")
def VolumesetGetById(id: str):
    """
    Dynamic CRUD Route: GET /api/v1/volume-sets/{id}
    """
    collection_path = f"/api/v1/volume-sets"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("VolumesetGetById", dict())
    return static_val

@app.get("/api/v1/volume-sets/{id}/volumes")
def VolumesetGetByvolumesetId(id: str):
    """
    Dynamic CRUD Route: GET /api/v1/volume-sets/{id}/volumes
    """
    collection_path = f"/api/v1/volume-sets/{id}/volumes"
    static_data = MOCK_DB.get("VolumesetGetByvolumesetId", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/volumes")
def VolumesList():
    """
    Dynamic CRUD Route: GET /api/v1/volumes
    """
    collection_path = f"/api/v1/volumes"
    static_data = MOCK_DB.get("VolumesList", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
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

@app.get("/api/v1/volumes/{id}")
def VolumeGetById(id: str):
    """
    Dynamic CRUD Route: GET /api/v1/volumes/{id}
    """
    collection_path = f"/api/v1/volumes"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("VolumeGetById", dict())
    return static_val