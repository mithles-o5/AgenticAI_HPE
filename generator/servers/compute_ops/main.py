import uuid
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
import os
from models import *

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from db_store import MOCK_DB

app = FastAPI(title='Generated Mock Server', description='Generated automatically from API docs.')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/compute-ops-mgmt/v1beta2/appliances/{device_id}")
def get_compute_ops_mgmt_v1beta2_appliances_device_id(device_id: str):
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1beta2/appliances/{device_id}
    """
    collection_path = f"/compute-ops-mgmt/v1beta2/appliances"
    item_id = device_id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("get_compute_ops_mgmt_v1beta2_appliances_device_id", dict())
    return static_val

@app.delete("/compute-ops-mgmt/v1beta2/appliances/{device_id}")
def delete_compute_ops_mgmt_v1beta2_appliances_device_id(device_id: str):
    """
    Dynamic CRUD Route: DELETE /compute-ops-mgmt/v1beta2/appliances/{device_id}
    """
    collection_path = f"/compute-ops-mgmt/v1beta2/appliances"
    item_id = device_id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        deleted = MOCK_DB["dynamic_store"][collection_path].pop(item_id)
        return {"message": "Deleted successfully", "id": item_id, "item": deleted}
    return MOCK_DB.get("delete_compute_ops_mgmt_v1beta2_appliances_device_id", dict())

@app.get("/compute-ops-mgmt/v1beta2/appliances/{device_id}/certificate")
def get_compute_ops_mgmt_v1beta2_appliances_device_id_certificate(device_id: str):
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1beta2/appliances/{device_id}/certificate
    """
    collection_path = f"/compute-ops-mgmt/v1beta2/appliances/{device_id}/certificate"
    static_data = MOCK_DB.get("get_compute_ops_mgmt_v1beta2_appliances_device_id_certificate", dict())
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

@app.get("/compute-ops-mgmt/v1/appliance-firmware-bundles")
def get_compute_ops_mgmt_v1_appliance_firmware_bundles():
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1/appliance-firmware-bundles
    """
    collection_path = f"/compute-ops-mgmt/v1/appliance-firmware-bundles"
    static_data = MOCK_DB.get("get_compute_ops_mgmt_v1_appliance_firmware_bundles", dict())
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

@app.get("/compute-ops-mgmt/v1/appliance-firmware-bundles/{id}")
def get_compute_ops_mgmt_v1_appliance_firmware_bundles_id(id: str):
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1/appliance-firmware-bundles/{id}
    """
    collection_path = f"/compute-ops-mgmt/v1/appliance-firmware-bundles"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("get_compute_ops_mgmt_v1_appliance_firmware_bundles_id", dict())
    return static_val

@app.get("/compute-ops-mgmt/v1beta1/appliance-firmware-bundles")
def get_compute_ops_mgmt_v1beta1_appliance_firmware_bundles():
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1beta1/appliance-firmware-bundles
    """
    collection_path = f"/compute-ops-mgmt/v1beta1/appliance-firmware-bundles"
    static_data = MOCK_DB.get("get_compute_ops_mgmt_v1beta1_appliance_firmware_bundles", dict())
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

@app.get("/compute-ops-mgmt/v1beta1/appliance-firmware-bundles/{id}")
def get_compute_ops_mgmt_v1beta1_appliance_firmware_bundles_id(id: str):
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1beta1/appliance-firmware-bundles/{id}
    """
    collection_path = f"/compute-ops-mgmt/v1beta1/appliance-firmware-bundles"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("get_compute_ops_mgmt_v1beta1_appliance_firmware_bundles_id", dict())
    return static_val

@app.post("/compute-ops-mgmt/v1beta2/approval-policies")
def post_compute_ops_mgmt_v1beta2_approval_policies(payload: PostComputeOpsMgmtV1beta2ApprovalPoliciesRequest):
    """
    Dynamic CRUD Route: POST /compute-ops-mgmt/v1beta2/approval-policies
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/compute-ops-mgmt/v1beta2/approval-policies"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/compute-ops-mgmt/v1beta2/approval-policies")
def get_compute_ops_mgmt_v1beta2_approval_policies():
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1beta2/approval-policies
    """
    collection_path = f"/compute-ops-mgmt/v1beta2/approval-policies"
    static_data = MOCK_DB.get("get_compute_ops_mgmt_v1beta2_approval_policies", dict())
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

@app.get("/compute-ops-mgmt/v1beta2/approval-policies/{policy_id}")
def get_compute_ops_mgmt_v1beta2_approval_policies_policy_id(policy_id: str):
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1beta2/approval-policies/{policy_id}
    """
    collection_path = f"/compute-ops-mgmt/v1beta2/approval-policies"
    item_id = policy_id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("get_compute_ops_mgmt_v1beta2_approval_policies_policy_id", dict())
    return static_val

@app.patch("/compute-ops-mgmt/v1beta2/approval-policies/{policy_id}")
def patch_compute_ops_mgmt_v1beta2_approval_policies_policy_id(policy_id: str, payload: PatchComputeOpsMgmtV1beta2ApprovalPoliciesPolicyIdRequest):
    """
    Dynamic CRUD Route: PATCH /compute-ops-mgmt/v1beta2/approval-policies/{policy_id}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/compute-ops-mgmt/v1beta2/approval-policies"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    item_id = policy_id
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = MOCK_DB["dynamic_store"][collection_path].get(item_id, {})
    existing.update(payload_dict)
    MOCK_DB["dynamic_store"][collection_path][item_id] = existing
    return existing

@app.delete("/compute-ops-mgmt/v1beta2/approval-policies/{policy_id}")
def delete_compute_ops_mgmt_v1beta2_approval_policies_policy_id(policy_id: str):
    """
    Dynamic CRUD Route: DELETE /compute-ops-mgmt/v1beta2/approval-policies/{policy_id}
    """
    collection_path = f"/compute-ops-mgmt/v1beta2/approval-policies"
    item_id = policy_id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        deleted = MOCK_DB["dynamic_store"][collection_path].pop(item_id)
        return {"message": "Deleted successfully", "id": item_id, "item": deleted}
    return MOCK_DB.get("delete_compute_ops_mgmt_v1beta2_approval_policies_policy_id", dict())

@app.get("/compute-ops-mgmt/v1beta2/approval-requests")
def get_compute_ops_mgmt_v1beta2_approval_requests():
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1beta2/approval-requests
    """
    collection_path = f"/compute-ops-mgmt/v1beta2/approval-requests"
    static_data = MOCK_DB.get("get_compute_ops_mgmt_v1beta2_approval_requests", dict())
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

@app.get("/compute-ops-mgmt/v1beta2/approval-requests/{request_id}")
def get_compute_ops_mgmt_v1beta2_approval_requests_request_id(request_id: str):
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1beta2/approval-requests/{request_id}
    """
    collection_path = f"/compute-ops-mgmt/v1beta2/approval-requests"
    item_id = request_id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("get_compute_ops_mgmt_v1beta2_approval_requests_request_id", dict())
    return static_val

@app.patch("/compute-ops-mgmt/v1beta2/approval-requests/{request_id}")
def patch_compute_ops_mgmt_v1beta2_approval_requests_request_id(request_id: str, payload: PatchComputeOpsMgmtV1beta2ApprovalRequestsRequestIdRequest):
    """
    Dynamic CRUD Route: PATCH /compute-ops-mgmt/v1beta2/approval-requests/{request_id}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/compute-ops-mgmt/v1beta2/approval-requests"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    item_id = request_id
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = MOCK_DB["dynamic_store"][collection_path].get(item_id, {})
    existing.update(payload_dict)
    MOCK_DB["dynamic_store"][collection_path][item_id] = existing
    return existing

@app.post("/compute-ops-mgmt/v1beta2/approval-requests/{request_id}/approve")
def post_compute_ops_mgmt_v1beta2_approval_requests_request_id_approve(request_id: str, payload: PostComputeOpsMgmtV1beta2ApprovalRequestsRequestIdApproveRequest):
    return MOCK_DB.get("post_compute_ops_mgmt_v1beta2_approval_requests_request_id_approve", dict())

@app.get("/compute-ops-mgmt/v1/async-operations")
def get_compute_ops_mgmt_v1_async_operations():
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1/async-operations
    """
    collection_path = f"/compute-ops-mgmt/v1/async-operations"
    static_data = MOCK_DB.get("get_compute_ops_mgmt_v1_async_operations", dict())
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

@app.get("/compute-ops-mgmt/v1/async-operations/{id}")
def get_compute_ops_mgmt_v1_async_operations_id(id: str):
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1/async-operations/{id}
    """
    collection_path = f"/compute-ops-mgmt/v1/async-operations"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("get_compute_ops_mgmt_v1_async_operations_id", dict())
    return static_val

@app.get("/compute-ops-mgmt/v1beta1/async-operations")
def get_compute_ops_mgmt_v1beta1_async_operations():
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1beta1/async-operations
    """
    collection_path = f"/compute-ops-mgmt/v1beta1/async-operations"
    static_data = MOCK_DB.get("get_compute_ops_mgmt_v1beta1_async_operations", dict())
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

@app.get("/compute-ops-mgmt/v1beta1/async-operations/{id}")
def get_compute_ops_mgmt_v1beta1_async_operations_id(id: str):
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1beta1/async-operations/{id}
    """
    collection_path = f"/compute-ops-mgmt/v1beta1/async-operations"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("get_compute_ops_mgmt_v1beta1_async_operations_id", dict())
    return static_val

@app.get("/compute-ops-mgmt/v1beta1/accounts/{id}")
def get_compute_ops_mgmt_v1beta1_accounts_id(id: str):
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1beta1/accounts/{id}
    """
    collection_path = f"/compute-ops-mgmt/v1beta1/accounts"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("get_compute_ops_mgmt_v1beta1_accounts_id", dict())
    return static_val

@app.get("/compute-ops-mgmt/v1beta1/accounts/{id}/tenants")
def get_compute_ops_mgmt_v1beta1_accounts_id_tenants(id: str):
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1beta1/accounts/{id}/tenants
    """
    collection_path = f"/compute-ops-mgmt/v1beta1/accounts/{id}/tenants"
    static_data = MOCK_DB.get("get_compute_ops_mgmt_v1beta1_accounts_id_tenants", dict())
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

@app.post("/compute-ops-mgmt/v1beta1/activation-keys")
def post_compute_ops_mgmt_v1beta1_activation_keys(payload: PostComputeOpsMgmtV1beta1ActivationKeysRequest):
    """
    Dynamic CRUD Route: POST /compute-ops-mgmt/v1beta1/activation-keys
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/compute-ops-mgmt/v1beta1/activation-keys"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/compute-ops-mgmt/v1beta1/activation-keys")
def get_compute_ops_mgmt_v1beta1_activation_keys():
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1beta1/activation-keys
    """
    collection_path = f"/compute-ops-mgmt/v1beta1/activation-keys"
    static_data = MOCK_DB.get("get_compute_ops_mgmt_v1beta1_activation_keys", dict())
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

@app.delete("/compute-ops-mgmt/v1beta1/activation-keys/{activation_key}")
def delete_compute_ops_mgmt_v1beta1_activation_keys_activation_key(activation_key: str):
    """
    Dynamic CRUD Route: DELETE /compute-ops-mgmt/v1beta1/activation-keys/{activation_key}
    """
    collection_path = f"/compute-ops-mgmt/v1beta1/activation-keys"
    item_id = activation_key
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        deleted = MOCK_DB["dynamic_store"][collection_path].pop(item_id)
        return {"message": "Deleted successfully", "id": item_id, "item": deleted}
    return MOCK_DB.get("delete_compute_ops_mgmt_v1beta1_activation_keys_activation_key", dict())

@app.post("/compute-ops-mgmt/v1beta1/activation-tokens")
def post_compute_ops_mgmt_v1beta1_activation_tokens(payload: PostComputeOpsMgmtV1beta1ActivationTokensRequest):
    """
    Dynamic CRUD Route: POST /compute-ops-mgmt/v1beta1/activation-tokens
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/compute-ops-mgmt/v1beta1/activation-tokens"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/compute-ops-mgmt/v1beta2/activities")
def get_compute_ops_mgmt_v1beta2_activities():
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1beta2/activities
    """
    collection_path = f"/compute-ops-mgmt/v1beta2/activities"
    static_data = MOCK_DB.get("get_compute_ops_mgmt_v1beta2_activities", dict())
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

@app.post("/compute-ops-mgmt/v1beta1/ahs-files")
def post_compute_ops_mgmt_v1beta1_ahs_files(payload: PostComputeOpsMgmtV1beta1AhsFilesRequest):
    """
    Dynamic CRUD Route: POST /compute-ops-mgmt/v1beta1/ahs-files
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/compute-ops-mgmt/v1beta1/ahs-files"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/compute-ops-mgmt/v1beta1/ahs-files")
def get_compute_ops_mgmt_v1beta1_ahs_files():
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1beta1/ahs-files
    """
    collection_path = f"/compute-ops-mgmt/v1beta1/ahs-files"
    static_data = MOCK_DB.get("get_compute_ops_mgmt_v1beta1_ahs_files", dict())
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

@app.get("/compute-ops-mgmt/v1beta1/ahs-files/{id}")
def get_compute_ops_mgmt_v1beta1_ahs_files_id(id: str):
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1beta1/ahs-files/{id}
    """
    collection_path = f"/compute-ops-mgmt/v1beta1/ahs-files"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("get_compute_ops_mgmt_v1beta1_ahs_files_id", dict())
    return static_val

@app.patch("/compute-ops-mgmt/v1beta1/ahs-files/{id}")
def patch_compute_ops_mgmt_v1beta1_ahs_files_id(id: str, payload: PatchComputeOpsMgmtV1beta1AhsFilesIdRequest):
    """
    Dynamic CRUD Route: PATCH /compute-ops-mgmt/v1beta1/ahs-files/{id}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/compute-ops-mgmt/v1beta1/ahs-files"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    item_id = id
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = MOCK_DB["dynamic_store"][collection_path].get(item_id, {})
    existing.update(payload_dict)
    MOCK_DB["dynamic_store"][collection_path][item_id] = existing
    return existing

@app.post("/compute-ops-mgmt/v1beta1/ahs-files/{id}/parse")
def post_compute_ops_mgmt_v1beta1_ahs_files_id_parse(id: str):
    """
    Dynamic CRUD Route: POST /compute-ops-mgmt/v1beta1/ahs-files/{id}/parse
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/compute-ops-mgmt/v1beta1/ahs-files/{id}/parse"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = {}
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/compute-ops-mgmt/v1beta1/ahs-files/{id}/download")
def get_compute_ops_mgmt_v1beta1_ahs_files_id_download(id: str):
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta1_ahs_files_id_download", dict())

@app.get("/compute-ops-mgmt/v1beta2/appliances")
def get_compute_ops_mgmt_v1beta2_appliances():
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1beta2/appliances
    """
    collection_path = f"/compute-ops-mgmt/v1beta2/appliances"
    static_data = MOCK_DB.get("get_compute_ops_mgmt_v1beta2_appliances", dict())
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

@app.get("/compute-ops-mgmt/v1beta1/energy-over-time")
def get_compute_ops_mgmt_v1beta1_energy_over_time():
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1beta1/energy-over-time
    """
    collection_path = f"/compute-ops-mgmt/v1beta1/energy-over-time"
    static_data = MOCK_DB.get("get_compute_ops_mgmt_v1beta1_energy_over_time", dict())
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

@app.get("/compute-ops-mgmt/v1beta1/energy-by-entity")
def get_compute_ops_mgmt_v1beta1_energy_by_entity():
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1beta1/energy-by-entity
    """
    collection_path = f"/compute-ops-mgmt/v1beta1/energy-by-entity"
    static_data = MOCK_DB.get("get_compute_ops_mgmt_v1beta1_energy_by_entity", dict())
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

@app.get("/compute-ops-mgmt/v1beta1/external-services")
def get_compute_ops_mgmt_v1beta1_external_services():
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1beta1/external-services
    """
    collection_path = f"/compute-ops-mgmt/v1beta1/external-services"
    static_data = MOCK_DB.get("get_compute_ops_mgmt_v1beta1_external_services", dict())
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

@app.post("/compute-ops-mgmt/v1beta1/external-services")
def post_compute_ops_mgmt_v1beta1_external_services(payload: PostComputeOpsMgmtV1beta1ExternalServicesRequest):
    """
    Dynamic CRUD Route: POST /compute-ops-mgmt/v1beta1/external-services
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/compute-ops-mgmt/v1beta1/external-services"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/compute-ops-mgmt/v1beta1/external-services/{id}")
def get_compute_ops_mgmt_v1beta1_external_services_id(id: str):
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1beta1/external-services/{id}
    """
    collection_path = f"/compute-ops-mgmt/v1beta1/external-services"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("get_compute_ops_mgmt_v1beta1_external_services_id", dict())
    return static_val

@app.delete("/compute-ops-mgmt/v1beta1/external-services/{id}")
def delete_compute_ops_mgmt_v1beta1_external_services_id(id: str):
    """
    Dynamic CRUD Route: DELETE /compute-ops-mgmt/v1beta1/external-services/{id}
    """
    collection_path = f"/compute-ops-mgmt/v1beta1/external-services"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        deleted = MOCK_DB["dynamic_store"][collection_path].pop(item_id)
        return {"message": "Deleted successfully", "id": item_id, "item": deleted}
    return MOCK_DB.get("delete_compute_ops_mgmt_v1beta1_external_services_id", dict())

@app.patch("/compute-ops-mgmt/v1beta1/external-services/{id}")
def patch_compute_ops_mgmt_v1beta1_external_services_id(id: str, payload: PatchComputeOpsMgmtV1beta1ExternalServicesIdRequest):
    """
    Dynamic CRUD Route: PATCH /compute-ops-mgmt/v1beta1/external-services/{id}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/compute-ops-mgmt/v1beta1/external-services"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    item_id = id
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = MOCK_DB["dynamic_store"][collection_path].get(item_id, {})
    existing.update(payload_dict)
    MOCK_DB["dynamic_store"][collection_path][item_id] = existing
    return existing

@app.post("/compute-ops-mgmt/v1beta1/external-services/{id}/test")
def post_compute_ops_mgmt_v1beta1_external_services_id_test(id: str):
    """
    Dynamic CRUD Route: POST /compute-ops-mgmt/v1beta1/external-services/{id}/test
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/compute-ops-mgmt/v1beta1/external-services/{id}/test"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = {}
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/compute-ops-mgmt/v1beta1/filters")
def get_compute_ops_mgmt_v1beta1_filters():
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1beta1/filters
    """
    collection_path = f"/compute-ops-mgmt/v1beta1/filters"
    static_data = MOCK_DB.get("get_compute_ops_mgmt_v1beta1_filters", dict())
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

@app.post("/compute-ops-mgmt/v1beta1/filters")
def post_compute_ops_mgmt_v1beta1_filters(payload: PostComputeOpsMgmtV1beta1FiltersRequest):
    """
    Dynamic CRUD Route: POST /compute-ops-mgmt/v1beta1/filters
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/compute-ops-mgmt/v1beta1/filters"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/compute-ops-mgmt/v1beta1/filters/properties")
def get_compute_ops_mgmt_v1beta1_filters_properties():
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1beta1/filters/properties
    """
    collection_path = f"/compute-ops-mgmt/v1beta1/filters/properties"
    static_data = MOCK_DB.get("get_compute_ops_mgmt_v1beta1_filters_properties", dict())
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

@app.get("/compute-ops-mgmt/v1beta1/filters/{id}")
def get_compute_ops_mgmt_v1beta1_filters_id(id: str):
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1beta1/filters/{id}
    """
    collection_path = f"/compute-ops-mgmt/v1beta1/filters"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("get_compute_ops_mgmt_v1beta1_filters_id", dict())
    return static_val

@app.delete("/compute-ops-mgmt/v1beta1/filters/{id}")
def delete_compute_ops_mgmt_v1beta1_filters_id(id: str):
    """
    Dynamic CRUD Route: DELETE /compute-ops-mgmt/v1beta1/filters/{id}
    """
    collection_path = f"/compute-ops-mgmt/v1beta1/filters"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        deleted = MOCK_DB["dynamic_store"][collection_path].pop(item_id)
        return {"message": "Deleted successfully", "id": item_id, "item": deleted}
    return MOCK_DB.get("delete_compute_ops_mgmt_v1beta1_filters_id", dict())

@app.patch("/compute-ops-mgmt/v1beta1/filters/{id}")
def patch_compute_ops_mgmt_v1beta1_filters_id(id: str, payload: PatchComputeOpsMgmtV1beta1FiltersIdRequest):
    """
    Dynamic CRUD Route: PATCH /compute-ops-mgmt/v1beta1/filters/{id}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/compute-ops-mgmt/v1beta1/filters"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    item_id = id
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = MOCK_DB["dynamic_store"][collection_path].get(item_id, {})
    existing.update(payload_dict)
    MOCK_DB["dynamic_store"][collection_path][item_id] = existing
    return existing

@app.get("/compute-ops-mgmt/v1beta1/filters/{id}/matches")
def get_compute_ops_mgmt_v1beta1_filters_id_matches(id: str):
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1beta1/filters/{id}/matches
    """
    collection_path = f"/compute-ops-mgmt/v1beta1/filters/{id}/matches"
    static_data = MOCK_DB.get("get_compute_ops_mgmt_v1beta1_filters_id_matches", dict())
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

@app.get("/compute-ops-mgmt/v1/firmware-bundles")
def get_compute_ops_mgmt_v1_firmware_bundles():
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1/firmware-bundles
    """
    collection_path = f"/compute-ops-mgmt/v1/firmware-bundles"
    static_data = MOCK_DB.get("get_compute_ops_mgmt_v1_firmware_bundles", dict())
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

@app.get("/compute-ops-mgmt/v1/firmware-bundles/{id}")
def get_compute_ops_mgmt_v1_firmware_bundles_id(id: str):
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1/firmware-bundles/{id}
    """
    collection_path = f"/compute-ops-mgmt/v1/firmware-bundles"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("get_compute_ops_mgmt_v1_firmware_bundles_id", dict())
    return static_val

@app.get("/compute-ops-mgmt/v1/firmware-bundles/{id}/bundle-details")
def get_compute_ops_mgmt_v1_firmware_bundles_id_bundle_details(id: str):
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1/firmware-bundles/{id}/bundle-details
    """
    collection_path = f"/compute-ops-mgmt/v1/firmware-bundles/{id}/bundle-details"
    static_data = MOCK_DB.get("get_compute_ops_mgmt_v1_firmware_bundles_id_bundle_details", dict())
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

@app.get("/compute-ops-mgmt/v1beta2/firmware-bundles")
def get_compute_ops_mgmt_v1beta2_firmware_bundles():
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1beta2/firmware-bundles
    """
    collection_path = f"/compute-ops-mgmt/v1beta2/firmware-bundles"
    static_data = MOCK_DB.get("get_compute_ops_mgmt_v1beta2_firmware_bundles", dict())
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

@app.get("/compute-ops-mgmt/v1beta2/firmware-bundles/{id}")
def get_compute_ops_mgmt_v1beta2_firmware_bundles_id(id: str):
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1beta2/firmware-bundles/{id}
    """
    collection_path = f"/compute-ops-mgmt/v1beta2/firmware-bundles"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("get_compute_ops_mgmt_v1beta2_firmware_bundles_id", dict())
    return static_val

@app.get("/compute-ops-mgmt/v1/groups")
def get_compute_ops_mgmt_v1_groups():
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1/groups
    """
    collection_path = f"/compute-ops-mgmt/v1/groups"
    static_data = MOCK_DB.get("get_compute_ops_mgmt_v1_groups", dict())
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

@app.post("/compute-ops-mgmt/v1/groups")
def post_compute_ops_mgmt_v1_groups(payload: PostComputeOpsMgmtV1GroupsRequest):
    """
    Dynamic CRUD Route: POST /compute-ops-mgmt/v1/groups
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/compute-ops-mgmt/v1/groups"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/compute-ops-mgmt/v1/groups/{group-id}")
def get_compute_ops_mgmt_v1_groups_group_id():
    return MOCK_DB.get("get_compute_ops_mgmt_v1_groups_group_id", dict())

@app.delete("/compute-ops-mgmt/v1/groups/{group-id}")
def delete_compute_ops_mgmt_v1_groups_group_id():
    return MOCK_DB.get("delete_compute_ops_mgmt_v1_groups_group_id", dict())

@app.patch("/compute-ops-mgmt/v1/groups/{group-id}")
def patch_compute_ops_mgmt_v1_groups_group_id(payload: PatchComputeOpsMgmtV1GroupsGroupIdRequest):
    return MOCK_DB.get("patch_compute_ops_mgmt_v1_groups_group_id", dict())

@app.get("/compute-ops-mgmt/v1/groups/{group-id}/compliance")
def get_compute_ops_mgmt_v1_groups_group_id_compliance():
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1/groups/{group-id}/compliance
    """
    collection_path = f"/compute-ops-mgmt/v1/groups/{{group-id}}/compliance"
    static_data = MOCK_DB.get("get_compute_ops_mgmt_v1_groups_group_id_compliance", dict())
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

@app.get("/compute-ops-mgmt/v1/groups/{group-id}/compliance/{compliance-id}")
def get_compute_ops_mgmt_v1_groups_group_id_compliance_compliance_id():
    return MOCK_DB.get("get_compute_ops_mgmt_v1_groups_group_id_compliance_compliance_id", dict())

@app.get("/compute-ops-mgmt/v1/groups/{group-id}/devices")
def get_compute_ops_mgmt_v1_groups_group_id_devices():
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1/groups/{group-id}/devices
    """
    collection_path = f"/compute-ops-mgmt/v1/groups/{{group-id}}/devices"
    static_data = MOCK_DB.get("get_compute_ops_mgmt_v1_groups_group_id_devices", dict())
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

@app.get("/compute-ops-mgmt/v1beta3/groups")
def get_compute_ops_mgmt_v1beta3_groups():
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1beta3/groups
    """
    collection_path = f"/compute-ops-mgmt/v1beta3/groups"
    static_data = MOCK_DB.get("get_compute_ops_mgmt_v1beta3_groups", dict())
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

@app.post("/compute-ops-mgmt/v1beta3/groups")
def post_compute_ops_mgmt_v1beta3_groups(payload: PostComputeOpsMgmtV1beta3GroupsRequest):
    """
    Dynamic CRUD Route: POST /compute-ops-mgmt/v1beta3/groups
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/compute-ops-mgmt/v1beta3/groups"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/compute-ops-mgmt/v1beta3/groups/{group-id}")
def get_compute_ops_mgmt_v1beta3_groups_group_id():
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta3_groups_group_id", dict())

@app.delete("/compute-ops-mgmt/v1beta3/groups/{group-id}")
def delete_compute_ops_mgmt_v1beta3_groups_group_id():
    return MOCK_DB.get("delete_compute_ops_mgmt_v1beta3_groups_group_id", dict())

@app.patch("/compute-ops-mgmt/v1beta3/groups/{group-id}")
def patch_compute_ops_mgmt_v1beta3_groups_group_id(payload: PatchComputeOpsMgmtV1beta3GroupsGroupIdRequest):
    return MOCK_DB.get("patch_compute_ops_mgmt_v1beta3_groups_group_id", dict())

@app.get("/compute-ops-mgmt/v1beta3/groups/{group-id}/compliance")
def get_compute_ops_mgmt_v1beta3_groups_group_id_compliance():
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1beta3/groups/{group-id}/compliance
    """
    collection_path = f"/compute-ops-mgmt/v1beta3/groups/{{group-id}}/compliance"
    static_data = MOCK_DB.get("get_compute_ops_mgmt_v1beta3_groups_group_id_compliance", dict())
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

@app.get("/compute-ops-mgmt/v1beta3/groups/{group-id}/compliance/{compliance-id}")
def get_compute_ops_mgmt_v1beta3_groups_group_id_compliance_compliance_id():
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta3_groups_group_id_compliance_compliance_id", dict())

@app.get("/compute-ops-mgmt/v1beta3/groups/{group-id}/devices")
def get_compute_ops_mgmt_v1beta3_groups_group_id_devices():
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1beta3/groups/{group-id}/devices
    """
    collection_path = f"/compute-ops-mgmt/v1beta3/groups/{{group-id}}/devices"
    static_data = MOCK_DB.get("get_compute_ops_mgmt_v1beta3_groups_group_id_devices", dict())
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

@app.get("/compute-ops/v1beta2/groups")
def get_compute_ops_v1beta2_groups():
    """
    Dynamic CRUD Route: GET /compute-ops/v1beta2/groups
    """
    collection_path = f"/compute-ops/v1beta2/groups"
    static_data = MOCK_DB.get("get_compute_ops_v1beta2_groups", dict())
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

@app.post("/compute-ops/v1beta2/groups")
def post_compute_ops_v1beta2_groups(payload: PostComputeOpsV1beta2GroupsRequest):
    """
    Dynamic CRUD Route: POST /compute-ops/v1beta2/groups
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/compute-ops/v1beta2/groups"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/compute-ops/v1beta2/groups/{group-id}")
def get_compute_ops_v1beta2_groups_group_id():
    return MOCK_DB.get("get_compute_ops_v1beta2_groups_group_id", dict())

@app.delete("/compute-ops/v1beta2/groups/{group-id}")
def delete_compute_ops_v1beta2_groups_group_id():
    return MOCK_DB.get("delete_compute_ops_v1beta2_groups_group_id", dict())

@app.patch("/compute-ops/v1beta2/groups/{group-id}")
def patch_compute_ops_v1beta2_groups_group_id(payload: PatchComputeOpsV1beta2GroupsGroupIdRequest):
    return MOCK_DB.get("patch_compute_ops_v1beta2_groups_group_id", dict())

@app.get("/compute-ops/v1beta2/groups/{group-id}/compliance")
def get_compute_ops_v1beta2_groups_group_id_compliance():
    """
    Dynamic CRUD Route: GET /compute-ops/v1beta2/groups/{group-id}/compliance
    """
    collection_path = f"/compute-ops/v1beta2/groups/{{group-id}}/compliance"
    static_data = MOCK_DB.get("get_compute_ops_v1beta2_groups_group_id_compliance", dict())
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

@app.get("/compute-ops/v1beta2/groups/{group-id}/compliance/{compliance-id}")
def get_compute_ops_v1beta2_groups_group_id_compliance_compliance_id():
    return MOCK_DB.get("get_compute_ops_v1beta2_groups_group_id_compliance_compliance_id", dict())

@app.get("/compute-ops/v1beta2/groups/{group-id}/devices")
def get_compute_ops_v1beta2_groups_group_id_devices():
    """
    Dynamic CRUD Route: GET /compute-ops/v1beta2/groups/{group-id}/devices
    """
    collection_path = f"/compute-ops/v1beta2/groups/{{group-id}}/devices"
    static_data = MOCK_DB.get("get_compute_ops_v1beta2_groups_group_id_devices", dict())
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

@app.get("/compute-ops-mgmt/v1beta2/job-templates")
def get_compute_ops_mgmt_v1beta2_job_templates():
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1beta2/job-templates
    """
    collection_path = f"/compute-ops-mgmt/v1beta2/job-templates"
    static_data = MOCK_DB.get("get_compute_ops_mgmt_v1beta2_job_templates", dict())
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

@app.get("/compute-ops-mgmt/v1beta2/job-templates/{id}")
def get_compute_ops_mgmt_v1beta2_job_templates_id(id: str):
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1beta2/job-templates/{id}
    """
    collection_path = f"/compute-ops-mgmt/v1beta2/job-templates"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("get_compute_ops_mgmt_v1beta2_job_templates_id", dict())
    return static_val

@app.get("/compute-ops-mgmt/v1/jobs")
def get_compute_ops_mgmt_v1_jobs():
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1/jobs
    """
    collection_path = f"/compute-ops-mgmt/v1/jobs"
    static_data = MOCK_DB.get("get_compute_ops_mgmt_v1_jobs", dict())
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

@app.post("/compute-ops-mgmt/v1/jobs")
def post_compute_ops_mgmt_v1_jobs(payload: PostComputeOpsMgmtV1JobsRequest):
    """
    Dynamic CRUD Route: POST /compute-ops-mgmt/v1/jobs
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/compute-ops-mgmt/v1/jobs"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/compute-ops-mgmt/v1/jobs/{id}")
def get_compute_ops_mgmt_v1_jobs_id(id: str):
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1/jobs/{id}
    """
    collection_path = f"/compute-ops-mgmt/v1/jobs"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("get_compute_ops_mgmt_v1_jobs_id", dict())
    return static_val

@app.patch("/compute-ops-mgmt/v1/jobs/{id}")
def patch_compute_ops_mgmt_v1_jobs_id(id: str, payload: PatchComputeOpsMgmtV1JobsIdRequest):
    """
    Dynamic CRUD Route: PATCH /compute-ops-mgmt/v1/jobs/{id}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/compute-ops-mgmt/v1/jobs"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    item_id = id
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = MOCK_DB["dynamic_store"][collection_path].get(item_id, {})
    existing.update(payload_dict)
    MOCK_DB["dynamic_store"][collection_path][item_id] = existing
    return existing

@app.get("/compute-ops-mgmt/v1beta3/jobs")
def get_compute_ops_mgmt_v1beta3_jobs():
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1beta3/jobs
    """
    collection_path = f"/compute-ops-mgmt/v1beta3/jobs"
    static_data = MOCK_DB.get("get_compute_ops_mgmt_v1beta3_jobs", dict())
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

@app.post("/compute-ops-mgmt/v1beta3/jobs")
def post_compute_ops_mgmt_v1beta3_jobs(payload: PostComputeOpsMgmtV1beta3JobsRequest):
    """
    Dynamic CRUD Route: POST /compute-ops-mgmt/v1beta3/jobs
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/compute-ops-mgmt/v1beta3/jobs"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/compute-ops-mgmt/v1beta3/jobs/{id}")
def get_compute_ops_mgmt_v1beta3_jobs_id(id: str):
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1beta3/jobs/{id}
    """
    collection_path = f"/compute-ops-mgmt/v1beta3/jobs"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("get_compute_ops_mgmt_v1beta3_jobs_id", dict())
    return static_val

@app.patch("/compute-ops-mgmt/v1beta3/jobs/{id}")
def patch_compute_ops_mgmt_v1beta3_jobs_id(id: str, payload: PatchComputeOpsMgmtV1beta3JobsIdRequest):
    """
    Dynamic CRUD Route: PATCH /compute-ops-mgmt/v1beta3/jobs/{id}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/compute-ops-mgmt/v1beta3/jobs"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    item_id = id
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = MOCK_DB["dynamic_store"][collection_path].get(item_id, {})
    existing.update(payload_dict)
    MOCK_DB["dynamic_store"][collection_path][item_id] = existing
    return existing

@app.get("/compute-ops-mgmt/v1beta2/jobs")
def get_compute_ops_mgmt_v1beta2_jobs():
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1beta2/jobs
    """
    collection_path = f"/compute-ops-mgmt/v1beta2/jobs"
    static_data = MOCK_DB.get("get_compute_ops_mgmt_v1beta2_jobs", dict())
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

@app.post("/compute-ops-mgmt/v1beta2/jobs")
def post_compute_ops_mgmt_v1beta2_jobs(payload: PostComputeOpsMgmtV1beta2JobsRequest):
    """
    Dynamic CRUD Route: POST /compute-ops-mgmt/v1beta2/jobs
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/compute-ops-mgmt/v1beta2/jobs"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/compute-ops-mgmt/v1beta2/jobs/{id}")
def get_compute_ops_mgmt_v1beta2_jobs_id(id: str):
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1beta2/jobs/{id}
    """
    collection_path = f"/compute-ops-mgmt/v1beta2/jobs"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("get_compute_ops_mgmt_v1beta2_jobs_id", dict())
    return static_val

@app.patch("/compute-ops-mgmt/v1beta2/jobs/{id}")
def patch_compute_ops_mgmt_v1beta2_jobs_id(id: str, payload: PatchComputeOpsMgmtV1beta2JobsIdRequest):
    """
    Dynamic CRUD Route: PATCH /compute-ops-mgmt/v1beta2/jobs/{id}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/compute-ops-mgmt/v1beta2/jobs"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    item_id = id
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = MOCK_DB["dynamic_store"][collection_path].get(item_id, {})
    existing.update(payload_dict)
    MOCK_DB["dynamic_store"][collection_path][item_id] = existing
    return existing

@app.get("/compute-ops-mgmt/v1/metrics-configurations")
def get_compute_ops_mgmt_v1_metrics_configurations():
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1/metrics-configurations
    """
    collection_path = f"/compute-ops-mgmt/v1/metrics-configurations"
    static_data = MOCK_DB.get("get_compute_ops_mgmt_v1_metrics_configurations", dict())
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

@app.post("/compute-ops-mgmt/v1/metrics-configurations")
def post_compute_ops_mgmt_v1_metrics_configurations(payload: PostComputeOpsMgmtV1MetricsConfigurationsRequest):
    """
    Dynamic CRUD Route: POST /compute-ops-mgmt/v1/metrics-configurations
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/compute-ops-mgmt/v1/metrics-configurations"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/compute-ops-mgmt/v1/metrics-configurations/{id}")
def get_compute_ops_mgmt_v1_metrics_configurations_id(id: str):
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1/metrics-configurations/{id}
    """
    collection_path = f"/compute-ops-mgmt/v1/metrics-configurations"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("get_compute_ops_mgmt_v1_metrics_configurations_id", dict())
    return static_val

@app.delete("/compute-ops-mgmt/v1/metrics-configurations/{id}")
def delete_compute_ops_mgmt_v1_metrics_configurations_id(id: str):
    """
    Dynamic CRUD Route: DELETE /compute-ops-mgmt/v1/metrics-configurations/{id}
    """
    collection_path = f"/compute-ops-mgmt/v1/metrics-configurations"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        deleted = MOCK_DB["dynamic_store"][collection_path].pop(item_id)
        return {"message": "Deleted successfully", "id": item_id, "item": deleted}
    return MOCK_DB.get("delete_compute_ops_mgmt_v1_metrics_configurations_id", dict())

@app.patch("/compute-ops-mgmt/v1/metrics-configurations/{id}")
def patch_compute_ops_mgmt_v1_metrics_configurations_id(id: str, payload: PatchComputeOpsMgmtV1MetricsConfigurationsIdRequest):
    """
    Dynamic CRUD Route: PATCH /compute-ops-mgmt/v1/metrics-configurations/{id}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/compute-ops-mgmt/v1/metrics-configurations"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    item_id = id
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = MOCK_DB["dynamic_store"][collection_path].get(item_id, {})
    existing.update(payload_dict)
    MOCK_DB["dynamic_store"][collection_path][item_id] = existing
    return existing

@app.get("/compute-ops-mgmt/v1beta1/oneview-appliances")
def get_compute_ops_mgmt_v1beta1_oneview_appliances():
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1beta1/oneview-appliances
    """
    collection_path = f"/compute-ops-mgmt/v1beta1/oneview-appliances"
    static_data = MOCK_DB.get("get_compute_ops_mgmt_v1beta1_oneview_appliances", dict())
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

@app.post("/compute-ops-mgmt/v1beta1/oneview-appliances")
def post_compute_ops_mgmt_v1beta1_oneview_appliances(payload: PostComputeOpsMgmtV1beta1OneviewAppliancesRequest):
    """
    Dynamic CRUD Route: POST /compute-ops-mgmt/v1beta1/oneview-appliances
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/compute-ops-mgmt/v1beta1/oneview-appliances"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/compute-ops-mgmt/v1beta1/oneview-appliances/{device-id}")
def get_compute_ops_mgmt_v1beta1_oneview_appliances_device_id():
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta1_oneview_appliances_device_id", dict())

@app.delete("/compute-ops-mgmt/v1beta1/oneview-appliances/{device-id}")
def delete_compute_ops_mgmt_v1beta1_oneview_appliances_device_id():
    return MOCK_DB.get("delete_compute_ops_mgmt_v1beta1_oneview_appliances_device_id", dict())

@app.get("/compute-ops-mgmt/v1beta1/oneview-settings")
def get_compute_ops_mgmt_v1beta1_oneview_settings():
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1beta1/oneview-settings
    """
    collection_path = f"/compute-ops-mgmt/v1beta1/oneview-settings"
    static_data = MOCK_DB.get("get_compute_ops_mgmt_v1beta1_oneview_settings", dict())
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

@app.get("/compute-ops-mgmt/v1beta1/oneview-server-templates")
def get_compute_ops_mgmt_v1beta1_oneview_server_templates():
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1beta1/oneview-server-templates
    """
    collection_path = f"/compute-ops-mgmt/v1beta1/oneview-server-templates"
    static_data = MOCK_DB.get("get_compute_ops_mgmt_v1beta1_oneview_server_templates", dict())
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

@app.get("/compute-ops-mgmt/v1beta1/oneview-server-templates/{id}")
def get_compute_ops_mgmt_v1beta1_oneview_server_templates_id(id: str):
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1beta1/oneview-server-templates/{id}
    """
    collection_path = f"/compute-ops-mgmt/v1beta1/oneview-server-templates"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("get_compute_ops_mgmt_v1beta1_oneview_server_templates_id", dict())
    return static_val

@app.get("/compute-ops-mgmt/v1beta2/reports")
def get_compute_ops_mgmt_v1beta2_reports():
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1beta2/reports
    """
    collection_path = f"/compute-ops-mgmt/v1beta2/reports"
    static_data = MOCK_DB.get("get_compute_ops_mgmt_v1beta2_reports", dict())
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

@app.post("/compute-ops-mgmt/v1beta2/reports")
def post_compute_ops_mgmt_v1beta2_reports(payload: PostComputeOpsMgmtV1beta2ReportsRequest):
    """
    Dynamic CRUD Route: POST /compute-ops-mgmt/v1beta2/reports
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/compute-ops-mgmt/v1beta2/reports"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/compute-ops-mgmt/v1beta2/reports/{id}")
def get_compute_ops_mgmt_v1beta2_reports_id(id: str):
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1beta2/reports/{id}
    """
    collection_path = f"/compute-ops-mgmt/v1beta2/reports"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("get_compute_ops_mgmt_v1beta2_reports_id", dict())
    return static_val

@app.get("/compute-ops-mgmt/v1beta2/reports/{id}/data")
def get_compute_ops_mgmt_v1beta2_reports_id_data(id: str):
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1beta2/reports/{id}/data
    """
    collection_path = f"/compute-ops-mgmt/v1beta2/reports/{id}/data"
    static_data = MOCK_DB.get("get_compute_ops_mgmt_v1beta2_reports_id_data", dict())
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

@app.get("/compute-ops-mgmt/v1beta2/schedules")
def get_compute_ops_mgmt_v1beta2_schedules():
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1beta2/schedules
    """
    collection_path = f"/compute-ops-mgmt/v1beta2/schedules"
    static_data = MOCK_DB.get("get_compute_ops_mgmt_v1beta2_schedules", dict())
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

@app.post("/compute-ops-mgmt/v1beta2/schedules")
def post_compute_ops_mgmt_v1beta2_schedules(payload: PostComputeOpsMgmtV1beta2SchedulesRequest):
    """
    Dynamic CRUD Route: POST /compute-ops-mgmt/v1beta2/schedules
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/compute-ops-mgmt/v1beta2/schedules"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/compute-ops-mgmt/v1beta2/schedules/{id}")
def get_compute_ops_mgmt_v1beta2_schedules_id(id: str):
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1beta2/schedules/{id}
    """
    collection_path = f"/compute-ops-mgmt/v1beta2/schedules"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("get_compute_ops_mgmt_v1beta2_schedules_id", dict())
    return static_val

@app.delete("/compute-ops-mgmt/v1beta2/schedules/{id}")
def delete_compute_ops_mgmt_v1beta2_schedules_id(id: str):
    """
    Dynamic CRUD Route: DELETE /compute-ops-mgmt/v1beta2/schedules/{id}
    """
    collection_path = f"/compute-ops-mgmt/v1beta2/schedules"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        deleted = MOCK_DB["dynamic_store"][collection_path].pop(item_id)
        return {"message": "Deleted successfully", "id": item_id, "item": deleted}
    return MOCK_DB.get("delete_compute_ops_mgmt_v1beta2_schedules_id", dict())

@app.patch("/compute-ops-mgmt/v1beta2/schedules/{id}")
def patch_compute_ops_mgmt_v1beta2_schedules_id(id: str, payload: PatchComputeOpsMgmtV1beta2SchedulesIdRequest):
    """
    Dynamic CRUD Route: PATCH /compute-ops-mgmt/v1beta2/schedules/{id}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/compute-ops-mgmt/v1beta2/schedules"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    item_id = id
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = MOCK_DB["dynamic_store"][collection_path].get(item_id, {})
    existing.update(payload_dict)
    MOCK_DB["dynamic_store"][collection_path][item_id] = existing
    return existing

@app.get("/compute-ops-mgmt/v1beta2/schedules/{id}/history")
def get_compute_ops_mgmt_v1beta2_schedules_id_history(id: str):
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1beta2/schedules/{id}/history
    """
    collection_path = f"/compute-ops-mgmt/v1beta2/schedules/{id}/history"
    static_data = MOCK_DB.get("get_compute_ops_mgmt_v1beta2_schedules_id_history", dict())
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

@app.get("/compute-ops-mgmt/v1beta2/schedules/{id}/history/{history-id}")
def get_compute_ops_mgmt_v1beta2_schedules_id_history_history_id(id: str):
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta2_schedules_id_history_history_id", dict())

@app.get("/compute-ops-mgmt/v1beta1/server-locations/{location_id}")
def get_compute_ops_mgmt_v1beta1_server_locations_location_id(location_id: str):
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1beta1/server-locations/{location_id}
    """
    collection_path = f"/compute-ops-mgmt/v1beta1/server-locations"
    item_id = location_id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("get_compute_ops_mgmt_v1beta1_server_locations_location_id", dict())
    return static_val

@app.post("/compute-ops-mgmt/v1beta1/server-locations/{location_id}/servers")
def post_compute_ops_mgmt_v1beta1_server_locations_location_id_servers(location_id: str, payload: PostComputeOpsMgmtV1beta1ServerLocationsLocationIdServersRequest):
    """
    Dynamic CRUD Route: POST /compute-ops-mgmt/v1beta1/server-locations/{location_id}/servers
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/compute-ops-mgmt/v1beta1/server-locations/{location_id}/servers"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.delete("/compute-ops-mgmt/v1beta1/server-locations/{location_id}/servers")
def delete_compute_ops_mgmt_v1beta1_server_locations_location_id_servers(location_id: str):
    """
    Dynamic CRUD Route: DELETE /compute-ops-mgmt/v1beta1/server-locations/{location_id}/servers
    """
    return MOCK_DB.get("delete_compute_ops_mgmt_v1beta1_server_locations_location_id_servers", dict())

@app.get("/compute-ops/v1beta1/server-settings")
def get_compute_ops_v1beta1_server_settings():
    """
    Dynamic CRUD Route: GET /compute-ops/v1beta1/server-settings
    """
    collection_path = f"/compute-ops/v1beta1/server-settings"
    static_data = MOCK_DB.get("get_compute_ops_v1beta1_server_settings", dict())
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

@app.post("/compute-ops/v1beta1/server-settings")
def post_compute_ops_v1beta1_server_settings(payload: PostComputeOpsV1beta1ServerSettingsRequest):
    """
    Dynamic CRUD Route: POST /compute-ops/v1beta1/server-settings
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/compute-ops/v1beta1/server-settings"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/compute-ops/v1beta1/server-settings/{id}")
def get_compute_ops_v1beta1_server_settings_id(id: str):
    """
    Dynamic CRUD Route: GET /compute-ops/v1beta1/server-settings/{id}
    """
    collection_path = f"/compute-ops/v1beta1/server-settings"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("get_compute_ops_v1beta1_server_settings_id", dict())
    return static_val

@app.delete("/compute-ops/v1beta1/server-settings/{id}")
def delete_compute_ops_v1beta1_server_settings_id(id: str):
    """
    Dynamic CRUD Route: DELETE /compute-ops/v1beta1/server-settings/{id}
    """
    collection_path = f"/compute-ops/v1beta1/server-settings"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        deleted = MOCK_DB["dynamic_store"][collection_path].pop(item_id)
        return {"message": "Deleted successfully", "id": item_id, "item": deleted}
    return MOCK_DB.get("delete_compute_ops_v1beta1_server_settings_id", dict())

@app.patch("/compute-ops/v1beta1/server-settings/{id}")
def patch_compute_ops_v1beta1_server_settings_id(id: str, payload: PatchComputeOpsV1beta1ServerSettingsIdRequest):
    """
    Dynamic CRUD Route: PATCH /compute-ops/v1beta1/server-settings/{id}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/compute-ops/v1beta1/server-settings"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    item_id = id
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = MOCK_DB["dynamic_store"][collection_path].get(item_id, {})
    existing.update(payload_dict)
    MOCK_DB["dynamic_store"][collection_path][item_id] = existing
    return existing

@app.get("/compute-ops-mgmt/v1/settings")
def get_compute_ops_mgmt_v1_settings():
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1/settings
    """
    collection_path = f"/compute-ops-mgmt/v1/settings"
    static_data = MOCK_DB.get("get_compute_ops_mgmt_v1_settings", dict())
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

@app.post("/compute-ops-mgmt/v1/settings")
def post_compute_ops_mgmt_v1_settings(payload: PostComputeOpsMgmtV1SettingsRequest):
    """
    Dynamic CRUD Route: POST /compute-ops-mgmt/v1/settings
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/compute-ops-mgmt/v1/settings"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/compute-ops-mgmt/v1/settings/{id}")
def get_compute_ops_mgmt_v1_settings_id(id: str):
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1/settings/{id}
    """
    collection_path = f"/compute-ops-mgmt/v1/settings"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("get_compute_ops_mgmt_v1_settings_id", dict())
    return static_val

@app.delete("/compute-ops-mgmt/v1/settings/{id}")
def delete_compute_ops_mgmt_v1_settings_id(id: str):
    """
    Dynamic CRUD Route: DELETE /compute-ops-mgmt/v1/settings/{id}
    """
    collection_path = f"/compute-ops-mgmt/v1/settings"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        deleted = MOCK_DB["dynamic_store"][collection_path].pop(item_id)
        return {"message": "Deleted successfully", "id": item_id, "item": deleted}
    return MOCK_DB.get("delete_compute_ops_mgmt_v1_settings_id", dict())

@app.patch("/compute-ops-mgmt/v1/settings/{id}")
def patch_compute_ops_mgmt_v1_settings_id(id: str, payload: PatchComputeOpsMgmtV1SettingsIdRequest):
    """
    Dynamic CRUD Route: PATCH /compute-ops-mgmt/v1/settings/{id}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/compute-ops-mgmt/v1/settings"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    item_id = id
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = MOCK_DB["dynamic_store"][collection_path].get(item_id, {})
    existing.update(payload_dict)
    MOCK_DB["dynamic_store"][collection_path][item_id] = existing
    return existing

@app.get("/compute-ops-mgmt/v1beta1/settings")
def get_compute_ops_mgmt_v1beta1_settings():
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1beta1/settings
    """
    collection_path = f"/compute-ops-mgmt/v1beta1/settings"
    static_data = MOCK_DB.get("get_compute_ops_mgmt_v1beta1_settings", dict())
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

@app.post("/compute-ops-mgmt/v1beta1/settings")
def post_compute_ops_mgmt_v1beta1_settings(payload: PostComputeOpsMgmtV1beta1SettingsRequest):
    """
    Dynamic CRUD Route: POST /compute-ops-mgmt/v1beta1/settings
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/compute-ops-mgmt/v1beta1/settings"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/compute-ops-mgmt/v1beta1/settings/{id}")
def get_compute_ops_mgmt_v1beta1_settings_id(id: str):
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1beta1/settings/{id}
    """
    collection_path = f"/compute-ops-mgmt/v1beta1/settings"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("get_compute_ops_mgmt_v1beta1_settings_id", dict())
    return static_val

@app.delete("/compute-ops-mgmt/v1beta1/settings/{id}")
def delete_compute_ops_mgmt_v1beta1_settings_id(id: str):
    """
    Dynamic CRUD Route: DELETE /compute-ops-mgmt/v1beta1/settings/{id}
    """
    collection_path = f"/compute-ops-mgmt/v1beta1/settings"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        deleted = MOCK_DB["dynamic_store"][collection_path].pop(item_id)
        return {"message": "Deleted successfully", "id": item_id, "item": deleted}
    return MOCK_DB.get("delete_compute_ops_mgmt_v1beta1_settings_id", dict())

@app.patch("/compute-ops-mgmt/v1beta1/settings/{id}")
def patch_compute_ops_mgmt_v1beta1_settings_id(id: str, payload: PatchComputeOpsMgmtV1beta1SettingsIdRequest):
    """
    Dynamic CRUD Route: PATCH /compute-ops-mgmt/v1beta1/settings/{id}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/compute-ops-mgmt/v1beta1/settings"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    item_id = id
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = MOCK_DB["dynamic_store"][collection_path].get(item_id, {})
    existing.update(payload_dict)
    MOCK_DB["dynamic_store"][collection_path][item_id] = existing
    return existing

@app.get("/compute-ops-mgmt/v1/servers")
def get_compute_ops_mgmt_v1_servers():
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1/servers
    """
    collection_path = f"/compute-ops-mgmt/v1/servers"
    static_data = MOCK_DB.get("get_compute_ops_mgmt_v1_servers", dict())
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

@app.patch("/compute-ops-mgmt/v1/servers")
def patch_compute_ops_mgmt_v1_servers(payload: PatchComputeOpsMgmtV1ServersRequest):
    """
    Dynamic CRUD Route: PATCH /compute-ops-mgmt/v1/servers
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/compute-ops-mgmt/v1/servers"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})

    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    existing = MOCK_DB["dynamic_store"][collection_path].get(item_id, {})
    existing.update(payload_dict)
    MOCK_DB["dynamic_store"][collection_path][item_id] = existing
    return existing

@app.post("/compute-ops-mgmt/v1/servers")
def post_compute_ops_mgmt_v1_servers(payload: PostComputeOpsMgmtV1ServersRequest):
    """
    Dynamic CRUD Route: POST /compute-ops-mgmt/v1/servers
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/compute-ops-mgmt/v1/servers"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/compute-ops-mgmt/v1/servers/{id}")
def get_compute_ops_mgmt_v1_servers_id(id: str):
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1/servers/{id}
    """
    collection_path = f"/compute-ops-mgmt/v1/servers"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("get_compute_ops_mgmt_v1_servers_id", dict())
    return static_val

@app.patch("/compute-ops-mgmt/v1/servers/{id}")
def patch_compute_ops_mgmt_v1_servers_id(id: str, payload: PatchComputeOpsMgmtV1ServersIdRequest):
    """
    Dynamic CRUD Route: PATCH /compute-ops-mgmt/v1/servers/{id}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/compute-ops-mgmt/v1/servers"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    item_id = id
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = MOCK_DB["dynamic_store"][collection_path].get(item_id, {})
    existing.update(payload_dict)
    MOCK_DB["dynamic_store"][collection_path][item_id] = existing
    return existing

@app.delete("/compute-ops-mgmt/v1/servers/{id}")
def delete_compute_ops_mgmt_v1_servers_id(id: str):
    """
    Dynamic CRUD Route: DELETE /compute-ops-mgmt/v1/servers/{id}
    """
    collection_path = f"/compute-ops-mgmt/v1/servers"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        deleted = MOCK_DB["dynamic_store"][collection_path].pop(item_id)
        return {"message": "Deleted successfully", "id": item_id, "item": deleted}
    return MOCK_DB.get("delete_compute_ops_mgmt_v1_servers_id", dict())

@app.get("/compute-ops-mgmt/v1/servers/{id}/alerts")
def get_compute_ops_mgmt_v1_servers_id_alerts(id: str):
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1/servers/{id}/alerts
    """
    collection_path = f"/compute-ops-mgmt/v1/servers/{id}/alerts"
    static_data = MOCK_DB.get("get_compute_ops_mgmt_v1_servers_id_alerts", dict())
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

@app.post("/compute-ops-mgmt/v1/servers/{id}/clear-alert")
def post_compute_ops_mgmt_v1_servers_id_clear_alert(id: str, payload: PostComputeOpsMgmtV1ServersIdClearAlertRequest):
    return MOCK_DB.get("post_compute_ops_mgmt_v1_servers_id_clear_alert", dict())

@app.get("/compute-ops-mgmt/v1beta2/servers")
def get_compute_ops_mgmt_v1beta2_servers():
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1beta2/servers
    """
    collection_path = f"/compute-ops-mgmt/v1beta2/servers"
    static_data = MOCK_DB.get("get_compute_ops_mgmt_v1beta2_servers", dict())
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

@app.patch("/compute-ops-mgmt/v1beta2/servers")
def patch_compute_ops_mgmt_v1beta2_servers(payload: PatchComputeOpsMgmtV1beta2ServersRequest):
    """
    Dynamic CRUD Route: PATCH /compute-ops-mgmt/v1beta2/servers
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/compute-ops-mgmt/v1beta2/servers"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})

    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    existing = MOCK_DB["dynamic_store"][collection_path].get(item_id, {})
    existing.update(payload_dict)
    MOCK_DB["dynamic_store"][collection_path][item_id] = existing
    return existing

@app.post("/compute-ops-mgmt/v1beta2/servers")
def post_compute_ops_mgmt_v1beta2_servers(payload: PostComputeOpsMgmtV1beta2ServersRequest):
    """
    Dynamic CRUD Route: POST /compute-ops-mgmt/v1beta2/servers
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/compute-ops-mgmt/v1beta2/servers"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/compute-ops-mgmt/v1beta2/servers/{id}")
def get_compute_ops_mgmt_v1beta2_servers_id(id: str):
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1beta2/servers/{id}
    """
    collection_path = f"/compute-ops-mgmt/v1beta2/servers"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("get_compute_ops_mgmt_v1beta2_servers_id", dict())
    return static_val

@app.patch("/compute-ops-mgmt/v1beta2/servers/{id}")
def patch_compute_ops_mgmt_v1beta2_servers_id(id: str, payload: PatchComputeOpsMgmtV1beta2ServersIdRequest):
    """
    Dynamic CRUD Route: PATCH /compute-ops-mgmt/v1beta2/servers/{id}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/compute-ops-mgmt/v1beta2/servers"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    item_id = id
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = MOCK_DB["dynamic_store"][collection_path].get(item_id, {})
    existing.update(payload_dict)
    MOCK_DB["dynamic_store"][collection_path][item_id] = existing
    return existing

@app.delete("/compute-ops-mgmt/v1beta2/servers/{id}")
def delete_compute_ops_mgmt_v1beta2_servers_id(id: str):
    """
    Dynamic CRUD Route: DELETE /compute-ops-mgmt/v1beta2/servers/{id}
    """
    collection_path = f"/compute-ops-mgmt/v1beta2/servers"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        deleted = MOCK_DB["dynamic_store"][collection_path].pop(item_id)
        return {"message": "Deleted successfully", "id": item_id, "item": deleted}
    return MOCK_DB.get("delete_compute_ops_mgmt_v1beta2_servers_id", dict())

@app.get("/compute-ops-mgmt/v1beta2/servers/{id}/alerts")
def get_compute_ops_mgmt_v1beta2_servers_id_alerts(id: str):
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1beta2/servers/{id}/alerts
    """
    collection_path = f"/compute-ops-mgmt/v1beta2/servers/{id}/alerts"
    static_data = MOCK_DB.get("get_compute_ops_mgmt_v1beta2_servers_id_alerts", dict())
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

@app.post("/compute-ops-mgmt/v1beta2/servers/{id}/clear-alert")
def post_compute_ops_mgmt_v1beta2_servers_id_clear_alert(id: str, payload: PostComputeOpsMgmtV1beta2ServersIdClearAlertRequest):
    return MOCK_DB.get("post_compute_ops_mgmt_v1beta2_servers_id_clear_alert", dict())

@app.get("/compute-ops-mgmt/v1beta2/server-warranty")
def get_compute_ops_mgmt_v1beta2_server_warranty():
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1beta2/server-warranty
    """
    collection_path = f"/compute-ops-mgmt/v1beta2/server-warranty"
    static_data = MOCK_DB.get("get_compute_ops_mgmt_v1beta2_server_warranty", dict())
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

@app.get("/compute-ops-mgmt/v1beta2/server-warranty/{id}")
def get_compute_ops_mgmt_v1beta2_server_warranty_id(id: str):
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1beta2/server-warranty/{id}
    """
    collection_path = f"/compute-ops-mgmt/v1beta2/server-warranty"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("get_compute_ops_mgmt_v1beta2_server_warranty_id", dict())
    return static_val

@app.get("/compute-ops-mgmt/v1/user-preferences")
def get_compute_ops_mgmt_v1_user_preferences():
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1/user-preferences
    """
    collection_path = f"/compute-ops-mgmt/v1/user-preferences"
    static_data = MOCK_DB.get("get_compute_ops_mgmt_v1_user_preferences", dict())
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

@app.post("/compute-ops-mgmt/v1/user-preferences")
def post_compute_ops_mgmt_v1_user_preferences(payload: PostComputeOpsMgmtV1UserPreferencesRequest):
    """
    Dynamic CRUD Route: POST /compute-ops-mgmt/v1/user-preferences
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/compute-ops-mgmt/v1/user-preferences"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/compute-ops-mgmt/v1/user-preferences/{id}")
def get_compute_ops_mgmt_v1_user_preferences_id(id: str):
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1/user-preferences/{id}
    """
    collection_path = f"/compute-ops-mgmt/v1/user-preferences"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("get_compute_ops_mgmt_v1_user_preferences_id", dict())
    return static_val

@app.put("/compute-ops-mgmt/v1/user-preferences/{id}")
def put_compute_ops_mgmt_v1_user_preferences_id(id: str, payload: PutComputeOpsMgmtV1UserPreferencesIdRequest):
    """
    Dynamic CRUD Route: PUT /compute-ops-mgmt/v1/user-preferences/{id}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/compute-ops-mgmt/v1/user-preferences"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    item_id = id
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.post("/compute-ops-mgmt/v1/user-preferences/subscribe")
def post_compute_ops_mgmt_v1_user_preferences_subscribe(payload: PostComputeOpsMgmtV1UserPreferencesSubscribeRequest):
    return MOCK_DB.get("post_compute_ops_mgmt_v1_user_preferences_subscribe", dict())

@app.post("/compute-ops-mgmt/v1/user-preferences/unsubscribe")
def post_compute_ops_mgmt_v1_user_preferences_unsubscribe(payload: PostComputeOpsMgmtV1UserPreferencesUnsubscribeRequest):
    return MOCK_DB.get("post_compute_ops_mgmt_v1_user_preferences_unsubscribe", dict())

@app.get("/compute-ops-mgmt/v1beta1/user-preferences")
def get_compute_ops_mgmt_v1beta1_user_preferences():
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1beta1/user-preferences
    """
    collection_path = f"/compute-ops-mgmt/v1beta1/user-preferences"
    static_data = MOCK_DB.get("get_compute_ops_mgmt_v1beta1_user_preferences", dict())
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

@app.post("/compute-ops-mgmt/v1beta1/user-preferences")
def post_compute_ops_mgmt_v1beta1_user_preferences(payload: PostComputeOpsMgmtV1beta1UserPreferencesRequest):
    """
    Dynamic CRUD Route: POST /compute-ops-mgmt/v1beta1/user-preferences
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/compute-ops-mgmt/v1beta1/user-preferences"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/compute-ops-mgmt/v1beta1/user-preferences/{id}")
def get_compute_ops_mgmt_v1beta1_user_preferences_id(id: str):
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1beta1/user-preferences/{id}
    """
    collection_path = f"/compute-ops-mgmt/v1beta1/user-preferences"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("get_compute_ops_mgmt_v1beta1_user_preferences_id", dict())
    return static_val

@app.put("/compute-ops-mgmt/v1beta1/user-preferences/{id}")
def put_compute_ops_mgmt_v1beta1_user_preferences_id(id: str, payload: PutComputeOpsMgmtV1beta1UserPreferencesIdRequest):
    """
    Dynamic CRUD Route: PUT /compute-ops-mgmt/v1beta1/user-preferences/{id}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/compute-ops-mgmt/v1beta1/user-preferences"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    item_id = id
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/compute-ops-mgmt/v1beta1/utilization-over-time")
def get_compute_ops_mgmt_v1beta1_utilization_over_time():
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1beta1/utilization-over-time
    """
    collection_path = f"/compute-ops-mgmt/v1beta1/utilization-over-time"
    static_data = MOCK_DB.get("get_compute_ops_mgmt_v1beta1_utilization_over_time", dict())
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

@app.get("/compute-ops-mgmt/v1beta1/utilization-by-entity")
def get_compute_ops_mgmt_v1beta1_utilization_by_entity():
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1beta1/utilization-by-entity
    """
    collection_path = f"/compute-ops-mgmt/v1beta1/utilization-by-entity"
    static_data = MOCK_DB.get("get_compute_ops_mgmt_v1beta1_utilization_by_entity", dict())
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

@app.get("/compute-ops-mgmt/v1beta1/webhooks")
def get_compute_ops_mgmt_v1beta1_webhooks():
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1beta1/webhooks
    """
    collection_path = f"/compute-ops-mgmt/v1beta1/webhooks"
    static_data = MOCK_DB.get("get_compute_ops_mgmt_v1beta1_webhooks", dict())
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

@app.post("/compute-ops-mgmt/v1beta1/webhooks")
def post_compute_ops_mgmt_v1beta1_webhooks(payload: PostComputeOpsMgmtV1beta1WebhooksRequest):
    """
    Dynamic CRUD Route: POST /compute-ops-mgmt/v1beta1/webhooks
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/compute-ops-mgmt/v1beta1/webhooks"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.get("/compute-ops-mgmt/v1beta1/webhooks/{webhook_id}")
def get_compute_ops_mgmt_v1beta1_webhooks_webhook_id(webhook_id: str):
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1beta1/webhooks/{webhook_id}
    """
    collection_path = f"/compute-ops-mgmt/v1beta1/webhooks"
    item_id = webhook_id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("get_compute_ops_mgmt_v1beta1_webhooks_webhook_id", dict())
    return static_val

@app.patch("/compute-ops-mgmt/v1beta1/webhooks/{webhook_id}")
def patch_compute_ops_mgmt_v1beta1_webhooks_webhook_id(webhook_id: str, payload: PatchComputeOpsMgmtV1beta1WebhooksWebhookIdRequest):
    """
    Dynamic CRUD Route: PATCH /compute-ops-mgmt/v1beta1/webhooks/{webhook_id}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/compute-ops-mgmt/v1beta1/webhooks"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    item_id = webhook_id
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = MOCK_DB["dynamic_store"][collection_path].get(item_id, {})
    existing.update(payload_dict)
    MOCK_DB["dynamic_store"][collection_path][item_id] = existing
    return existing

@app.delete("/compute-ops-mgmt/v1beta1/webhooks/{webhook_id}")
def delete_compute_ops_mgmt_v1beta1_webhooks_webhook_id(webhook_id: str):
    """
    Dynamic CRUD Route: DELETE /compute-ops-mgmt/v1beta1/webhooks/{webhook_id}
    """
    collection_path = f"/compute-ops-mgmt/v1beta1/webhooks"
    item_id = webhook_id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        deleted = MOCK_DB["dynamic_store"][collection_path].pop(item_id)
        return {"message": "Deleted successfully", "id": item_id, "item": deleted}
    return MOCK_DB.get("delete_compute_ops_mgmt_v1beta1_webhooks_webhook_id", dict())

@app.get("/compute-ops-mgmt/v1beta1/webhooks/{webhook_id}/deliveries")
def get_compute_ops_mgmt_v1beta1_webhooks_webhook_id_deliveries(webhook_id: str):
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1beta1/webhooks/{webhook_id}/deliveries
    """
    collection_path = f"/compute-ops-mgmt/v1beta1/webhooks/{webhook_id}/deliveries"
    static_data = MOCK_DB.get("get_compute_ops_mgmt_v1beta1_webhooks_webhook_id_deliveries", dict())
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

@app.get("/compute-ops-mgmt/v1beta1/webhooks/{webhook_id}/deliveries/{delivery_id}")
def get_compute_ops_mgmt_v1beta1_webhooks_webhook_id_deliveries_delivery_id(webhook_id: str, delivery_id: str):
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1beta1/webhooks/{webhook_id}/deliveries/{delivery_id}
    """
    collection_path = f"/compute-ops-mgmt/v1beta1/webhooks/{webhook_id}/deliveries"
    item_id = delivery_id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("get_compute_ops_mgmt_v1beta1_webhooks_webhook_id_deliveries_delivery_id", dict())
    return static_val

@app.post("/compute-ops-mgmt/v1/groups/{group-id}/devices")
def post_compute_ops_mgmt_v1_groups_group_id_devices(payload: PostComputeOpsMgmtV1GroupsGroupIdDevicesRequest):
    """
    Dynamic CRUD Route: POST /compute-ops-mgmt/v1/groups/{group-id}/devices
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/compute-ops-mgmt/v1/groups/{{group-id}}/devices"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.post("/compute-ops-mgmt/v1/groups/{group-id}/devices/unassign")
def post_compute_ops_mgmt_v1_groups_group_id_devices_unassign(payload: PostComputeOpsMgmtV1GroupsGroupIdDevicesUnassignRequest):
    return MOCK_DB.get("post_compute_ops_mgmt_v1_groups_group_id_devices_unassign", dict())

@app.get("/compute-ops-mgmt/v1/groups/{group-id}/external-storage-compliance")
def get_compute_ops_mgmt_v1_groups_group_id_external_storage_compliance():
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1/groups/{group-id}/external-storage-compliance
    """
    collection_path = f"/compute-ops-mgmt/v1/groups/{{group-id}}/external-storage-compliance"
    static_data = MOCK_DB.get("get_compute_ops_mgmt_v1_groups_group_id_external_storage_compliance", dict())
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

@app.post("/compute-ops-mgmt/v1beta3/groups/{group-id}/devices")
def post_compute_ops_mgmt_v1beta3_groups_group_id_devices():
    """
    Dynamic CRUD Route: POST /compute-ops-mgmt/v1beta3/groups/{group-id}/devices
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/compute-ops-mgmt/v1beta3/groups/{{group-id}}/devices"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = {}
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.post("/compute-ops-mgmt/v1beta3/groups/{group-id}/devices/unassign")
def post_compute_ops_mgmt_v1beta3_groups_group_id_devices_unassign():
    return MOCK_DB.get("post_compute_ops_mgmt_v1beta3_groups_group_id_devices_unassign", dict())

@app.get("/compute-ops-mgmt/v1beta3/groups/{group-id}/external-storage-compliance")
def get_compute_ops_mgmt_v1beta3_groups_group_id_external_storage_compliance():
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1beta3/groups/{group-id}/external-storage-compliance
    """
    collection_path = f"/compute-ops-mgmt/v1beta3/groups/{{group-id}}/external-storage-compliance"
    static_data = MOCK_DB.get("get_compute_ops_mgmt_v1beta3_groups_group_id_external_storage_compliance", dict())
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

@app.get("/compute-ops-mgmt/v1beta3/groups/{group-id}/ilo-settings-compliance")
def get_compute_ops_mgmt_v1beta3_groups_group_id_ilo_settings_compliance():
    """
    Dynamic CRUD Route: GET /compute-ops-mgmt/v1beta3/groups/{group-id}/ilo-settings-compliance
    """
    collection_path = f"/compute-ops-mgmt/v1beta3/groups/{{group-id}}/ilo-settings-compliance"
    static_data = MOCK_DB.get("get_compute_ops_mgmt_v1beta3_groups_group_id_ilo_settings_compliance", dict())
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

@app.get("/compute-ops-mgmt/v1beta3/groups/{group-id}/ilo-settings-compliance/{ilo-settings-compliance-id}")
def get_compute_ops_mgmt_v1beta3_groups_group_id_ilo_settings_compliance_ilo_settings_compliance_id():
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta3_groups_group_id_ilo_settings_compliance_ilo_settings_compliance_id", dict())


# --- CRUD Endpoints for Compute Ops Devices ---

@app.get("/compute-ops-mgmt/v1/devices")
def get_compute_ops_devices():
    """
    CRUD Route: GET /compute-ops-mgmt/v1/devices
    """
    collection_path = "/compute-ops-mgmt/v1/devices"
    return list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())

@app.get("/compute-ops-mgmt/v1/devices/{id}")
def get_compute_ops_device_by_id(id: str):
    """
    CRUD Route: GET /compute-ops-mgmt/v1/devices/{id}
    """
    from fastapi import HTTPException
    collection_path = "/compute-ops-mgmt/v1/devices"
    store = MOCK_DB.get("dynamic_store", {}).get(collection_path, {})
    if id not in store:
        raise HTTPException(status_code=404, detail="Device not found")
    return store[id]

@app.post("/compute-ops-mgmt/v1/devices")
def create_compute_ops_device(payload: dict):
    """
    CRUD Route: POST /compute-ops-mgmt/v1/devices
    """
    collection_path = "/compute-ops-mgmt/v1/devices"
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    
    item_id = payload.get("id") or payload.get("serial_number") or str(uuid.uuid4())
    payload["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload
    return payload

@app.put("/compute-ops-mgmt/v1/devices/{id}")
def update_compute_ops_device(id: str, payload: dict):
    """
    CRUD Route: PUT /compute-ops-mgmt/v1/devices/{id}
    """
    from fastapi import HTTPException
    collection_path = "/compute-ops-mgmt/v1/devices"
    store = MOCK_DB.get("dynamic_store", {}).get(collection_path, {})
    if id not in store:
        raise HTTPException(status_code=404, detail="Device not found")
    
    existing = store[id]
    payload_dict = {k: v for k, v in payload.items() if v is not None}
    existing.update(payload_dict)
    MOCK_DB["dynamic_store"][collection_path][id] = existing
    return existing

@app.delete("/compute-ops-mgmt/v1/devices/{id}")
def delete_compute_ops_device(id: str):
    """
    CRUD Route: DELETE /compute-ops-mgmt/v1/devices/{id}
    """
    from fastapi import HTTPException
    collection_path = "/compute-ops-mgmt/v1/devices"
    store = MOCK_DB.get("dynamic_store", {}).get(collection_path, {})
    if id not in store:
        raise HTTPException(status_code=404, detail="Device not found")
    deleted = MOCK_DB["dynamic_store"][collection_path].pop(id)
    return {"message": "Deleted successfully", "id": id, "item": deleted}


@app.post("/compute-ops-mgmt/v1/devices/{id}/power")
def post_compute_ops_device_power(id: str, payload: ServerPowerActionRequest):
    """
    Action Route: POST /compute-ops-mgmt/v1/devices/{id}/power
    """
    collection_path = "/compute-ops-mgmt/v1/devices"
    store = MOCK_DB.get("dynamic_store", {}).get(collection_path, {})
    if id not in store:
        raise HTTPException(status_code=404, detail="Device not found")
    
    device = dict(store[id])
    device["power_state"] = payload.action
    import datetime
    device["updated_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S+05:30")
    MOCK_DB["dynamic_store"][collection_path][id] = device
    return device


@app.post("/compute-ops-mgmt/v1/devices/{id}/firmware")
def post_compute_ops_device_firmware(id: str, payload: ServerFirmwareUpdateRequest):
    """
    Action Route: POST /compute-ops-mgmt/v1/devices/{id}/firmware
    """
    collection_path = "/compute-ops-mgmt/v1/devices"
    store = MOCK_DB.get("dynamic_store", {}).get(collection_path, {})
    if id not in store:
        raise HTTPException(status_code=404, detail="Device not found")
    
    device = dict(store[id])
    device["firmware_version"] = payload.firmware_version
    import datetime
    device["updated_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S+05:30")
    MOCK_DB["dynamic_store"][collection_path][id] = device
    return device
