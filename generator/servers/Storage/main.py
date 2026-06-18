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
MOCK_DB = get_db_store("storage", mock_file)

app = FastAPI(title='Generated Mock Server', description='Generated automatically from API docs.')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/data-services/v1beta1/async-operations")
def get_data_services_v1beta1_async_operations():
    """
    Dynamic CRUD Route: GET /data-services/v1beta1/async-operations
    """
    collection_path = f"/data-services/v1beta1/async-operations"
    static_data = MOCK_DB.get("get_data_services_v1beta1_async_operations", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
    if not dynamic_items:
        return static_data
    if isinstance(static_data, list):
        res = list(static_data)
        existing = {item.get("id") or item.get("uuid") or item.get("name") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name")
            if iid not in existing:
                res.append(item)
        return res
    elif isinstance(static_data, dict):
        res = dict(static_data)
        for key in ["items", "members"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    return static_data

@app.get("/data-services/v1beta1/async-operations/{id}")
def get_data_services_v1beta1_async_operations_id(id: str):
    """
    Dynamic CRUD Route: GET /data-services/v1beta1/async-operations/{id}
    """
    collection_path = f"/data-services/v1beta1/async-operations"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("get_data_services_v1beta1_async_operations_id", dict())
    return static_val

@app.get("/data-services/v1beta1/dual-auth-operations")
def get_data_services_v1beta1_dual_auth_operations():
    """
    Dynamic CRUD Route: GET /data-services/v1beta1/dual-auth-operations
    """
    collection_path = f"/data-services/v1beta1/dual-auth-operations"
    static_data = MOCK_DB.get("get_data_services_v1beta1_dual_auth_operations", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
    if not dynamic_items:
        return static_data
    if isinstance(static_data, list):
        res = list(static_data)
        existing = {item.get("id") or item.get("uuid") or item.get("name") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name")
            if iid not in existing:
                res.append(item)
        return res
    elif isinstance(static_data, dict):
        res = dict(static_data)
        for key in ["items", "members"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    return static_data

@app.get("/data-services/v1beta1/dual-auth-operations/{id}")
def get_data_services_v1beta1_dual_auth_operations_id(id: str):
    """
    Dynamic CRUD Route: GET /data-services/v1beta1/dual-auth-operations/{id}
    """
    collection_path = f"/data-services/v1beta1/dual-auth-operations"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("get_data_services_v1beta1_dual_auth_operations_id", dict())
    return static_val

@app.patch("/data-services/v1beta1/dual-auth-operations/{id}")
def patch_data_services_v1beta1_dual_auth_operations_id(id: str, payload: PatchDataServicesV1beta1DualAuthOperationsIdRequest):
    """
    Dynamic CRUD Route: PATCH /data-services/v1beta1/dual-auth-operations/{id}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/data-services/v1beta1/dual-auth-operations"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    item_id = id
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = MOCK_DB["dynamic_store"][collection_path].get(item_id, {})
    existing.update(payload_dict)
    MOCK_DB["dynamic_store"][collection_path][item_id] = existing
    return existing

@app.get("/data-services/v1beta1/issues")
def get_data_services_v1beta1_issues():
    """
    Dynamic CRUD Route: GET /data-services/v1beta1/issues
    """
    collection_path = f"/data-services/v1beta1/issues"
    static_data = MOCK_DB.get("get_data_services_v1beta1_issues", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
    if not dynamic_items:
        return static_data
    if isinstance(static_data, list):
        res = list(static_data)
        existing = {item.get("id") or item.get("uuid") or item.get("name") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name")
            if iid not in existing:
                res.append(item)
        return res
    elif isinstance(static_data, dict):
        res = dict(static_data)
        for key in ["items", "members"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    return static_data

@app.get("/data-services/v1beta1/issues/{id}")
def get_data_services_v1beta1_issues_id(id: str):
    """
    Dynamic CRUD Route: GET /data-services/v1beta1/issues/{id}
    """
    collection_path = f"/data-services/v1beta1/issues"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("get_data_services_v1beta1_issues_id", dict())
    return static_val

@app.patch("/data-services/v1beta1/issues/{id}")
def patch_data_services_v1beta1_issues_id(id: str, payload: PatchDataServicesV1beta1IssuesIdRequest):
    """
    Dynamic CRUD Route: PATCH /data-services/v1beta1/issues/{id}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/data-services/v1beta1/issues"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    item_id = id
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = MOCK_DB["dynamic_store"][collection_path].get(item_id, {})
    existing.update(payload_dict)
    MOCK_DB["dynamic_store"][collection_path][item_id] = existing
    return existing

@app.delete("/data-services/v1beta1/issues/{id}")
def delete_data_services_v1beta1_issues_id(id: str):
    """
    Dynamic CRUD Route: DELETE /data-services/v1beta1/issues/{id}
    """
    collection_path = f"/data-services/v1beta1/issues"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        deleted = MOCK_DB["dynamic_store"][collection_path].pop(item_id)
        return {"message": "Deleted successfully", "id": item_id, "item": deleted}
    return MOCK_DB.get("delete_data_services_v1beta1_issues_id", dict())

@app.get("/data-services/v1beta1/issues-metadata")
def get_data_services_v1beta1_issues_metadata():
    """
    Dynamic CRUD Route: GET /data-services/v1beta1/issues-metadata
    """
    collection_path = f"/data-services/v1beta1/issues-metadata"
    static_data = MOCK_DB.get("get_data_services_v1beta1_issues_metadata", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
    if not dynamic_items:
        return static_data
    if isinstance(static_data, list):
        res = list(static_data)
        existing = {item.get("id") or item.get("uuid") or item.get("name") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name")
            if iid not in existing:
                res.append(item)
        return res
    elif isinstance(static_data, dict):
        res = dict(static_data)
        for key in ["items", "members"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    return static_data

@app.get("/data-services/v1beta1/secrets/{id}")
def get_data_services_v1beta1_secrets_id(id: str):
    """
    Dynamic CRUD Route: GET /data-services/v1beta1/secrets/{id}
    """
    collection_path = f"/data-services/v1beta1/secrets"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("get_data_services_v1beta1_secrets_id", dict())
    return static_val

@app.get("/data-services/v1beta1/secrets")
def get_data_services_v1beta1_secrets():
    """
    Dynamic CRUD Route: GET /data-services/v1beta1/secrets
    """
    collection_path = f"/data-services/v1beta1/secrets"
    static_data = MOCK_DB.get("get_data_services_v1beta1_secrets", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
    if not dynamic_items:
        return static_data
    if isinstance(static_data, list):
        res = list(static_data)
        existing = {item.get("id") or item.get("uuid") or item.get("name") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name")
            if iid not in existing:
                res.append(item)
        return res
    elif isinstance(static_data, dict):
        res = dict(static_data)
        for key in ["items", "members"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    return static_data

@app.post("/data-services/v1beta1/secrets")
def post_data_services_v1beta1_secrets(payload: PostDataServicesV1beta1SecretsRequest):
    """
    Dynamic CRUD Route: POST /data-services/v1beta1/secrets
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/data-services/v1beta1/secrets"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload_dict
    return payload_dict

@app.patch("/data-services/v1beta1/secrets/{id}")
def patch_data_services_v1beta1_secrets_id(id: str, payload: PatchDataServicesV1beta1SecretsIdRequest):
    """
    Dynamic CRUD Route: PATCH /data-services/v1beta1/secrets/{id}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/data-services/v1beta1/secrets"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    item_id = id
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = MOCK_DB["dynamic_store"][collection_path].get(item_id, {})
    existing.update(payload_dict)
    MOCK_DB["dynamic_store"][collection_path][item_id] = existing
    return existing

@app.delete("/data-services/v1beta1/secrets/{id}")
def delete_data_services_v1beta1_secrets_id(id: str):
    """
    Dynamic CRUD Route: DELETE /data-services/v1beta1/secrets/{id}
    """
    collection_path = f"/data-services/v1beta1/secrets"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        deleted = MOCK_DB["dynamic_store"][collection_path].pop(item_id)
        return {"message": "Deleted successfully", "id": item_id, "item": deleted}
    return MOCK_DB.get("delete_data_services_v1beta1_secrets_id", dict())

@app.get("/data-services/v1beta1/secret-assignments/{id}")
def get_data_services_v1beta1_secret_assignments_id(id: str):
    """
    Dynamic CRUD Route: GET /data-services/v1beta1/secret-assignments/{id}
    """
    collection_path = f"/data-services/v1beta1/secret-assignments"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("get_data_services_v1beta1_secret_assignments_id", dict())
    return static_val

@app.get("/data-services/v1beta1/secret-assignments")
def get_data_services_v1beta1_secret_assignments():
    """
    Dynamic CRUD Route: GET /data-services/v1beta1/secret-assignments
    """
    collection_path = f"/data-services/v1beta1/secret-assignments"
    static_data = MOCK_DB.get("get_data_services_v1beta1_secret_assignments", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
    if not dynamic_items:
        return static_data
    if isinstance(static_data, list):
        res = list(static_data)
        existing = {item.get("id") or item.get("uuid") or item.get("name") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name")
            if iid not in existing:
                res.append(item)
        return res
    elif isinstance(static_data, dict):
        res = dict(static_data)
        for key in ["items", "members"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    return static_data

@app.get("/data-services/v1beta1/settings")
def get_data_services_v1beta1_settings():
    """
    Dynamic CRUD Route: GET /data-services/v1beta1/settings
    """
    collection_path = f"/data-services/v1beta1/settings"
    static_data = MOCK_DB.get("get_data_services_v1beta1_settings", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
    if not dynamic_items:
        return static_data
    if isinstance(static_data, list):
        res = list(static_data)
        existing = {item.get("id") or item.get("uuid") or item.get("name") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name")
            if iid not in existing:
                res.append(item)
        return res
    elif isinstance(static_data, dict):
        res = dict(static_data)
        for key in ["items", "members"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    return static_data

@app.get("/data-services/v1beta1/settings/{id}")
def get_data_services_v1beta1_settings_id(id: str):
    """
    Dynamic CRUD Route: GET /data-services/v1beta1/settings/{id}
    """
    collection_path = f"/data-services/v1beta1/settings"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("get_data_services_v1beta1_settings_id", dict())
    return static_val

@app.patch("/data-services/v1beta1/settings/{id}")
def patch_data_services_v1beta1_settings_id(id: str, payload: PatchDataServicesV1beta1SettingsIdRequest):
    """
    Dynamic CRUD Route: PATCH /data-services/v1beta1/settings/{id}
    """
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    collection_path = f"/data-services/v1beta1/settings"
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    item_id = id
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = MOCK_DB["dynamic_store"][collection_path].get(item_id, {})
    existing.update(payload_dict)
    MOCK_DB["dynamic_store"][collection_path][item_id] = existing
    return existing

@app.get("/data-services/v1beta1/software-components/{id}/install-release")
def get_data_services_v1beta1_software_components_id_install_release(id: str):
    """
    Dynamic CRUD Route: GET /data-services/v1beta1/software-components/{id}/install-release
    """
    collection_path = f"/data-services/v1beta1/software-components/{id}/install-release"
    static_data = MOCK_DB.get("get_data_services_v1beta1_software_components_id_install_release", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
    if not dynamic_items:
        return static_data
    if isinstance(static_data, list):
        res = list(static_data)
        existing = {item.get("id") or item.get("uuid") or item.get("name") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name")
            if iid not in existing:
                res.append(item)
        return res
    elif isinstance(static_data, dict):
        res = dict(static_data)
        for key in ["items", "members"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    return static_data

@app.get("/data-services/v1beta1/software-releases/{id}")
def get_data_services_v1beta1_software_releases_id(id: str):
    """
    Dynamic CRUD Route: GET /data-services/v1beta1/software-releases/{id}
    """
    collection_path = f"/data-services/v1beta1/software-releases"
    item_id = id
    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:
        return MOCK_DB["dynamic_store"][collection_path][item_id]
    static_val = MOCK_DB.get("get_data_services_v1beta1_software_releases_id", dict())
    return static_val

@app.get("/data-services/v1beta1/software-releases")
def get_data_services_v1beta1_software_releases():
    """
    Dynamic CRUD Route: GET /data-services/v1beta1/software-releases
    """
    collection_path = f"/data-services/v1beta1/software-releases"
    static_data = MOCK_DB.get("get_data_services_v1beta1_software_releases", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
    if not dynamic_items:
        return static_data
    if isinstance(static_data, list):
        res = list(static_data)
        existing = {item.get("id") or item.get("uuid") or item.get("name") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name")
            if iid not in existing:
                res.append(item)
        return res
    elif isinstance(static_data, dict):
        res = dict(static_data)
        for key in ["items", "members"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    return static_data

@app.post("/data-services/v1beta1/software-releases/{id}/download")
def post_data_services_v1beta1_software_releases_id_download(id: str, payload: PostDataServicesV1beta1SoftwareReleasesIdDownloadRequest):
    return MOCK_DB.get("post_data_services_v1beta1_software_releases_id_download", dict())

@app.get("/data-services/v1beta1/software-upgrades")
def get_data_services_v1beta1_software_upgrades():
    """
    Dynamic CRUD Route: GET /data-services/v1beta1/software-upgrades
    """
    collection_path = f"/data-services/v1beta1/software-upgrades"
    static_data = MOCK_DB.get("get_data_services_v1beta1_software_upgrades", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
    if not dynamic_items:
        return static_data
    if isinstance(static_data, list):
        res = list(static_data)
        existing = {item.get("id") or item.get("uuid") or item.get("name") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name")
            if iid not in existing:
                res.append(item)
        return res
    elif isinstance(static_data, dict):
        res = dict(static_data)
        for key in ["items", "members"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    return static_data

@app.get("/data-services/v1beta1/storage-locations")
def get_data_services_v1beta1_storage_locations():
    """
    Dynamic CRUD Route: GET /data-services/v1beta1/storage-locations
    """
    collection_path = f"/data-services/v1beta1/storage-locations"
    static_data = MOCK_DB.get("get_data_services_v1beta1_storage_locations", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
    if not dynamic_items:
        return static_data
    if isinstance(static_data, list):
        res = list(static_data)
        existing = {item.get("id") or item.get("uuid") or item.get("name") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name")
            if iid not in existing:
                res.append(item)
        return res
    elif isinstance(static_data, dict):
        res = dict(static_data)
        for key in ["items", "members"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    return static_data

@app.get("/data-services/v1beta1/tags")
def get_data_services_v1beta1_tags():
    """
    Dynamic CRUD Route: GET /data-services/v1beta1/tags
    """
    collection_path = f"/data-services/v1beta1/tags"
    static_data = MOCK_DB.get("get_data_services_v1beta1_tags", dict())
    dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
    if not dynamic_items:
        return static_data
    if isinstance(static_data, list):
        res = list(static_data)
        existing = {item.get("id") or item.get("uuid") or item.get("name") for item in res if isinstance(item, dict)}
        for item in dynamic_items:
            iid = item.get("id") or item.get("uuid") or item.get("name")
            if iid not in existing:
                res.append(item)
        return res
    elif isinstance(static_data, dict):
        res = dict(static_data)
        for key in ["items", "members"]:
            if key in res and isinstance(res[key], list):
                res[key] = list(res[key])
                existing = {item.get("id") or item.get("uuid") or item.get("name") for item in res[key] if isinstance(item, dict)}
                for item in dynamic_items:
                    iid = item.get("id") or item.get("uuid") or item.get("name")
                    if iid not in existing:
                        res[key].append(item)
                res["count"] = len(res[key])
                if "total" in res:
                    res["total"] = len(res[key])
        return res
    return static_data


# --- CRUD Endpoints for Storage Devices ---

@app.get("/data-services/v1beta1/devices")
def get_storage_devices():
    """
    CRUD Route: GET /data-services/v1beta1/devices
    """
    collection_path = "/data-services/v1beta1/devices"
    return list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())

@app.get("/data-services/v1beta1/devices/{id}")
def get_storage_device_by_id(id: str):
    """
    CRUD Route: GET /data-services/v1beta1/devices/{id}
    """
    from fastapi import HTTPException
    collection_path = "/data-services/v1beta1/devices"
    store = MOCK_DB.get("dynamic_store", {}).get(collection_path, {})
    if id not in store:
        raise HTTPException(status_code=404, detail="Device not found")
    return store[id]

@app.post("/data-services/v1beta1/devices")
def create_storage_device(payload: dict):
    """
    CRUD Route: POST /data-services/v1beta1/devices
    """
    collection_path = "/data-services/v1beta1/devices"
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}
    
    item_id = payload.get("id") or payload.get("serial_number") or str(uuid.uuid4())
    payload["id"] = item_id
    MOCK_DB["dynamic_store"][collection_path][item_id] = payload
    return payload

@app.put("/data-services/v1beta1/devices/{id}")
def update_storage_device(id: str, payload: dict):
    """
    CRUD Route: PUT /data-services/v1beta1/devices/{id}
    """
    from fastapi import HTTPException
    collection_path = "/data-services/v1beta1/devices"
    store = MOCK_DB.get("dynamic_store", {}).get(collection_path, {})
    if id not in store:
        raise HTTPException(status_code=404, detail="Device not found")
    
    existing = store[id]
    payload_dict = {k: v for k, v in payload.items() if v is not None}
    existing.update(payload_dict)
    MOCK_DB["dynamic_store"][collection_path][id] = existing
    return existing

@app.delete("/data-services/v1beta1/devices/{id}")
def delete_storage_device(id: str):
    """
    CRUD Route: DELETE /data-services/v1beta1/devices/{id}
    """
    from fastapi import HTTPException
    collection_path = "/data-services/v1beta1/devices"
    store = MOCK_DB.get("dynamic_store", {}).get(collection_path, {})
    if id not in store:
        raise HTTPException(status_code=404, detail="Device not found")
    deleted = MOCK_DB["dynamic_store"][collection_path].pop(id)
    return {"message": "Deleted successfully", "id": id, "item": deleted}


@app.post("/data-services/v1beta1/devices/{id}/volumes")
def post_storage_device_volumes(id: str, payload: StorageVolumeCreateRequest):
    """
    Action Route: POST /data-services/v1beta1/devices/{id}/volumes
    """
    from fastapi import HTTPException
    import uuid
    device_path = "/data-services/v1beta1/devices"
    volume_path = "/data-services/v1beta1/volumes"
    
    device_store = MOCK_DB.get("dynamic_store", {}).get(device_path, {})
    if id not in device_store:
        raise HTTPException(status_code=404, detail="Device not found")
        
    device = dict(device_store[id])
    
    # Initialize capacity fields if they don't exist or are None
    if device.get("total_capacity_gb") is None:
        device["total_capacity_gb"] = 10000
    if device.get("free_capacity_gb") is None:
        device["free_capacity_gb"] = 10000
        
    if device["free_capacity_gb"] < payload.size_gb:
        raise HTTPException(status_code=400, detail="Insufficient storage capacity")
        
    device["free_capacity_gb"] -= payload.size_gb
    MOCK_DB["dynamic_store"][device_path][id] = device
    
    # Create volume
    volume_id = str(uuid.uuid4())
    volume = {
        "id": volume_id,
        "device_id": id,
        "volume_name": payload.volume_name,
        "size_gb": payload.size_gb,
        "status": "HEALTHY"
    }
    
    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    if volume_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][volume_path] = {}
        
    MOCK_DB["dynamic_store"][volume_path][volume_id] = volume
    return volume


@app.delete("/data-services/v1beta1/devices/{id}/volumes/{volume_id}")
def delete_storage_device_volume(id: str, volume_id: str):
    """
    Action Route: DELETE /data-services/v1beta1/devices/{id}/volumes/{volume_id}
    """
    from fastapi import HTTPException
    device_path = "/data-services/v1beta1/devices"
    volume_path = "/data-services/v1beta1/volumes"
    
    device_store = MOCK_DB.get("dynamic_store", {}).get(device_path, {})
    if id not in device_store:
        raise HTTPException(status_code=404, detail="Device not found")
        
    volume_store = MOCK_DB.get("dynamic_store", {}).get(volume_path, {})
    if volume_id not in volume_store:
        raise HTTPException(status_code=404, detail="Volume not found")
        
    volume = volume_store[volume_id]
    if volume.get("device_id") != id:
        raise HTTPException(status_code=400, detail="Volume does not belong to this device")
        
    size_gb = volume.get("size_gb") or 0
    device = dict(device_store[id])
    if "free_capacity_gb" in device:
        device["free_capacity_gb"] += size_gb
        MOCK_DB["dynamic_store"][device_path][id] = device
        
    MOCK_DB["dynamic_store"][volume_path].pop(volume_id)
    return {"message": "Volume deleted successfully", "volume_id": volume_id}


@app.patch("/data-services/v1beta1/devices/{id}")
def patch_storage_device(id: str, payload: dict):
    """
    CRUD Route: PATCH /data-services/v1beta1/devices/{id}
    """
    from fastapi import HTTPException
    collection_path = "/data-services/v1beta1/devices"
    store = MOCK_DB.get("dynamic_store", {}).get(collection_path, {})
    if id not in store:
        raise HTTPException(status_code=404, detail="Device not found")
    
    existing = dict(store[id])
    payload_dict = {k: v for k, v in payload.items() if v is not None}
    existing.update(payload_dict)
    MOCK_DB["dynamic_store"][collection_path][id] = existing
    return existing


class StoragePowerRequest(BaseModel):
    action: str


@app.post("/data-services/v1beta1/devices/{id}/power")
def post_storage_device_power(id: str, payload: StoragePowerRequest):
    """
    Action Route: POST /data-services/v1beta1/devices/{id}/power
    """
    from fastapi import HTTPException
    import datetime
    collection_path = "/data-services/v1beta1/devices"
    store = MOCK_DB.get("dynamic_store", {}).get(collection_path, {})
    if id not in store:
        raise HTTPException(status_code=404, detail="Device not found")
        
    action_upper = payload.action.upper()
    if action_upper not in ["ON", "OFF"]:
        raise HTTPException(status_code=400, detail="Invalid action. Only 'ON' or 'OFF' are allowed.")
        
    device = dict(store[id])
    device["power_state"] = action_upper
    device["updated_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S+05:30")
    MOCK_DB["dynamic_store"][collection_path][id] = device
    return device

