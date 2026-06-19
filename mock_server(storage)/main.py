import uuid
from fastapi import FastAPI, Query
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

@app.get("/data-services/v1beta1/async-operations")
def get_data_services_v1beta1_async_operations():
    """
    Dynamic CRUD Route: GET /data-services/v1beta1/async-operations
    """
    collection_path = f"/data-services/v1beta1/async-operations"
    static_data = db.get_static("get_data_services_v1beta1_async_operations", dict())
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

@app.get("/data-services/v1beta1/async-operations/{id}")
def get_data_services_v1beta1_async_operations_id(id: str):
    """
    Dynamic CRUD Route: GET /data-services/v1beta1/async-operations/{id}
    """
    collection_path = f"/data-services/v1beta1/async-operations"
    item_id = id
    item = db.get_item(collection_path, item_id)
    if item:
        return item
    static_val = db.get_static("get_data_services_v1beta1_async_operations_id", dict())
    return static_val

@app.get("/data-services/v1beta1/dual-auth-operations")
def get_data_services_v1beta1_dual_auth_operations():
    """
    Dynamic CRUD Route: GET /data-services/v1beta1/dual-auth-operations
    """
    collection_path = f"/data-services/v1beta1/dual-auth-operations"
    static_data = db.get_static("get_data_services_v1beta1_dual_auth_operations", dict())
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

@app.get("/data-services/v1beta1/dual-auth-operations/{id}")
def get_data_services_v1beta1_dual_auth_operations_id(id: str):
    """
    Dynamic CRUD Route: GET /data-services/v1beta1/dual-auth-operations/{id}
    """
    collection_path = f"/data-services/v1beta1/dual-auth-operations"
    item_id = id
    item = db.get_item(collection_path, item_id)
    if item:
        return item
    static_val = db.get_static("get_data_services_v1beta1_dual_auth_operations_id", dict())
    return static_val

@app.patch("/data-services/v1beta1/dual-auth-operations/{id}")
def patch_data_services_v1beta1_dual_auth_operations_id(id: str, payload: PatchDataServicesV1beta1DualAuthOperationsIdRequest):
    """
    Dynamic CRUD Route: PATCH /data-services/v1beta1/dual-auth-operations/{id}
    """
    collection_path = f"/data-services/v1beta1/dual-auth-operations"
    item_id = id
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = db.get_item(collection_path, item_id) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, item_id, existing)
    return existing

@app.get("/data-services/v1beta1/issues")
def get_data_services_v1beta1_issues():
    """
    Dynamic CRUD Route: GET /data-services/v1beta1/issues
    """
    collection_path = f"/data-services/v1beta1/issues"
    static_data = db.get_static("get_data_services_v1beta1_issues", dict())
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

@app.get("/data-services/v1beta1/issues/{id}")
def get_data_services_v1beta1_issues_id(id: str):
    """
    Dynamic CRUD Route: GET /data-services/v1beta1/issues/{id}
    """
    collection_path = f"/data-services/v1beta1/issues"
    item_id = id
    item = db.get_item(collection_path, item_id)
    if item:
        return item
    static_val = db.get_static("get_data_services_v1beta1_issues_id", dict())
    return static_val

@app.patch("/data-services/v1beta1/issues/{id}")
def patch_data_services_v1beta1_issues_id(id: str, payload: PatchDataServicesV1beta1IssuesIdRequest):
    """
    Dynamic CRUD Route: PATCH /data-services/v1beta1/issues/{id}
    """
    collection_path = f"/data-services/v1beta1/issues"
    item_id = id
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = db.get_item(collection_path, item_id) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, item_id, existing)
    return existing

@app.delete("/data-services/v1beta1/issues/{id}")
def delete_data_services_v1beta1_issues_id(id: str):
    """
    Dynamic CRUD Route: DELETE /data-services/v1beta1/issues/{id}
    """
    collection_path = f"/data-services/v1beta1/issues"
    item_id = id
    item = db.get_item(collection_path, item_id)
    if item:
        deleted = db.delete_item(collection_path, item_id)
        return {"message": "Deleted successfully", "id": item_id, "item": deleted}
    return db.get_static("delete_data_services_v1beta1_issues_id", dict())

@app.get("/data-services/v1beta1/issues-metadata")
def get_data_services_v1beta1_issues_metadata():
    """
    Dynamic CRUD Route: GET /data-services/v1beta1/issues-metadata
    """
    collection_path = f"/data-services/v1beta1/issues-metadata"
    static_data = db.get_static("get_data_services_v1beta1_issues_metadata", dict())
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

@app.get("/data-services/v1beta1/secrets/{id}")
def get_data_services_v1beta1_secrets_id(id: str):
    """
    Dynamic CRUD Route: GET /data-services/v1beta1/secrets/{id}
    """
    collection_path = f"/data-services/v1beta1/secrets"
    item_id = id
    item = db.get_item(collection_path, item_id)
    if item:
        return item
    static_val = db.get_static("get_data_services_v1beta1_secrets_id", dict())
    return static_val

@app.get("/data-services/v1beta1/secrets")
def get_data_services_v1beta1_secrets():
    """
    Dynamic CRUD Route: GET /data-services/v1beta1/secrets
    """
    collection_path = f"/data-services/v1beta1/secrets"
    static_data = db.get_static("get_data_services_v1beta1_secrets", dict())
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

@app.post("/data-services/v1beta1/secrets")
def post_data_services_v1beta1_secrets(payload: PostDataServicesV1beta1SecretsRequest):
    """
    Dynamic CRUD Route: POST /data-services/v1beta1/secrets
    """
    collection_path = f"/data-services/v1beta1/secrets"
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    item_id = payload_dict.get("id") or payload_dict.get("uuid") or payload_dict.get("name") or str(uuid.uuid4())
    if "id" not in payload_dict and "uuid" not in payload_dict:
        payload_dict["id"] = item_id
    db.upsert_item(collection_path, item_id, payload_dict)
    return payload_dict

@app.patch("/data-services/v1beta1/secrets/{id}")
def patch_data_services_v1beta1_secrets_id(id: str, payload: PatchDataServicesV1beta1SecretsIdRequest):
    """
    Dynamic CRUD Route: PATCH /data-services/v1beta1/secrets/{id}
    """
    collection_path = f"/data-services/v1beta1/secrets"
    item_id = id
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = db.get_item(collection_path, item_id) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, item_id, existing)
    return existing

@app.delete("/data-services/v1beta1/secrets/{id}")
def delete_data_services_v1beta1_secrets_id(id: str):
    """
    Dynamic CRUD Route: DELETE /data-services/v1beta1/secrets/{id}
    """
    collection_path = f"/data-services/v1beta1/secrets"
    item_id = id
    item = db.get_item(collection_path, item_id)
    if item:
        deleted = db.delete_item(collection_path, item_id)
        return {"message": "Deleted successfully", "id": item_id, "item": deleted}
    return db.get_static("delete_data_services_v1beta1_secrets_id", dict())

@app.get("/data-services/v1beta1/secret-assignments/{id}")
def get_data_services_v1beta1_secret_assignments_id(id: str):
    """
    Dynamic CRUD Route: GET /data-services/v1beta1/secret-assignments/{id}
    """
    collection_path = f"/data-services/v1beta1/secret-assignments"
    item_id = id
    item = db.get_item(collection_path, item_id)
    if item:
        return item
    static_val = db.get_static("get_data_services_v1beta1_secret_assignments_id", dict())
    return static_val

@app.get("/data-services/v1beta1/secret-assignments")
def get_data_services_v1beta1_secret_assignments():
    """
    Dynamic CRUD Route: GET /data-services/v1beta1/secret-assignments
    """
    collection_path = f"/data-services/v1beta1/secret-assignments"
    static_data = db.get_static("get_data_services_v1beta1_secret_assignments", dict())
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

@app.get("/data-services/v1beta1/settings")
def get_data_services_v1beta1_settings():
    """
    Dynamic CRUD Route: GET /data-services/v1beta1/settings
    """
    collection_path = f"/data-services/v1beta1/settings"
    static_data = db.get_static("get_data_services_v1beta1_settings", dict())
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

@app.get("/data-services/v1beta1/settings/{id}")
def get_data_services_v1beta1_settings_id(id: str):
    """
    Dynamic CRUD Route: GET /data-services/v1beta1/settings/{id}
    """
    collection_path = f"/data-services/v1beta1/settings"
    item_id = id
    item = db.get_item(collection_path, item_id)
    if item:
        return item
    static_val = db.get_static("get_data_services_v1beta1_settings_id", dict())
    return static_val

@app.patch("/data-services/v1beta1/settings/{id}")
def patch_data_services_v1beta1_settings_id(id: str, payload: PatchDataServicesV1beta1SettingsIdRequest):
    """
    Dynamic CRUD Route: PATCH /data-services/v1beta1/settings/{id}
    """
    collection_path = f"/data-services/v1beta1/settings"
    item_id = id
    payload_dict = payload.dict() if hasattr(payload, "dict") else (payload if isinstance(payload, dict) else {})
    existing = db.get_item(collection_path, item_id) or {}
    existing.update(payload_dict)
    db.upsert_item(collection_path, item_id, existing)
    return existing

@app.get("/data-services/v1beta1/software-components/{id}/install-release")
def get_data_services_v1beta1_software_components_id_install_release(id: str):
    """
    Dynamic CRUD Route: GET /data-services/v1beta1/software-components/{id}/install-release
    """
    collection_path = f"/data-services/v1beta1/software-components/{id}/install-release"
    static_data = db.get_static("get_data_services_v1beta1_software_components_id_install_release", dict())
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

@app.get("/data-services/v1beta1/software-releases/{id}")
def get_data_services_v1beta1_software_releases_id(id: str):
    """
    Dynamic CRUD Route: GET /data-services/v1beta1/software-releases/{id}
    """
    collection_path = f"/data-services/v1beta1/software-releases"
    item_id = id
    item = db.get_item(collection_path, item_id)
    if item:
        return item
    static_val = db.get_static("get_data_services_v1beta1_software_releases_id", dict())
    return static_val

@app.get("/data-services/v1beta1/software-releases")
def get_data_services_v1beta1_software_releases():
    """
    Dynamic CRUD Route: GET /data-services/v1beta1/software-releases
    """
    collection_path = f"/data-services/v1beta1/software-releases"
    static_data = db.get_static("get_data_services_v1beta1_software_releases", dict())
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

@app.post("/data-services/v1beta1/software-releases/{id}/download")
def post_data_services_v1beta1_software_releases_id_download(id: str, payload: PostDataServicesV1beta1SoftwareReleasesIdDownloadRequest):
    return db.get_static("post_data_services_v1beta1_software_releases_id_download", dict())

@app.get("/data-services/v1beta1/software-upgrades")
def get_data_services_v1beta1_software_upgrades():
    """
    Dynamic CRUD Route: GET /data-services/v1beta1/software-upgrades
    """
    collection_path = f"/data-services/v1beta1/software-upgrades"
    static_data = db.get_static("get_data_services_v1beta1_software_upgrades", dict())
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

@app.get("/data-services/v1beta1/storage-locations")
def get_data_services_v1beta1_storage_locations():
    """
    Dynamic CRUD Route: GET /data-services/v1beta1/storage-locations
    """
    collection_path = f"/data-services/v1beta1/storage-locations"
    static_data = db.get_static("get_data_services_v1beta1_storage_locations", dict())
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

@app.get("/data-services/v1beta1/tags")
def get_data_services_v1beta1_tags():
    """
    Dynamic CRUD Route: GET /data-services/v1beta1/tags
    """
    collection_path = f"/data-services/v1beta1/tags"
    static_data = db.get_static("get_data_services_v1beta1_tags", dict())
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


# --- CRUD Endpoints for Storage Devices ---

@app.get("/data-services/v1beta1/devices")
def get_storage_devices():
    """
    CRUD Route: GET /data-services/v1beta1/devices
    """
    collection_path = "/data-services/v1beta1/devices"
    return db.get_all(collection_path)

@app.get("/data-services/v1beta1/devices/{id}")
def get_storage_device_by_id(id: str):
    """
    CRUD Route: GET /data-services/v1beta1/devices/{id}
    """
    from fastapi import HTTPException
    collection_path = "/data-services/v1beta1/devices"
    item = db.get_item(collection_path, id)
    if item:
        return item
    raise HTTPException(status_code=404, detail="Device not found")

@app.post("/data-services/v1beta1/devices")
def create_storage_device(payload: dict):
    """
    CRUD Route: POST /data-services/v1beta1/devices
    """
    collection_path = "/data-services/v1beta1/devices"
    
    item_id = payload.get("id") or payload.get("serial_number") or str(uuid.uuid4())
    payload["id"] = item_id
    db.upsert_item(collection_path, item_id, payload)
    return payload

@app.put("/data-services/v1beta1/devices/{id}")
def update_storage_device(id: str, payload: dict):
    """
    CRUD Route: PUT /data-services/v1beta1/devices/{id}
    """
    from fastapi import HTTPException
    collection_path = "/data-services/v1beta1/devices"
    item = db.get_item(collection_path, id)
    if item:
        return item
    raise HTTPException(status_code=404, detail="Device not found")