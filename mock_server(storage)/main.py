from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import json
import os
from models import *

mock_file = os.path.join(os.path.dirname(__file__), "mock_data.json")
try:
    with open(mock_file, "r", encoding="utf-8") as f:
        MOCK_DB = json.load(f)
except Exception:
    MOCK_DB = {}

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
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_data_services_v1beta1_async_operations", dict())

@app.get("/data-services/v1beta1/async-operations/{id}")
def get_data_services_v1beta1_async_operations_id(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_data_services_v1beta1_async_operations_id", dict())

@app.get("/data-services/v1beta1/dual-auth-operations")
def get_data_services_v1beta1_dual_auth_operations():
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_data_services_v1beta1_dual_auth_operations", dict())

@app.get("/data-services/v1beta1/dual-auth-operations/{id}")
def get_data_services_v1beta1_dual_auth_operations_id(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_data_services_v1beta1_dual_auth_operations_id", dict())

@app.patch("/data-services/v1beta1/dual-auth-operations/{id}")
def patch_data_services_v1beta1_dual_auth_operations_id(id: str, payload: PatchDataServicesV1beta1DualAuthOperationsIdRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("patch_data_services_v1beta1_dual_auth_operations_id", dict())

@app.get("/data-services/v1beta1/issues")
def get_data_services_v1beta1_issues():
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_data_services_v1beta1_issues", dict())

@app.get("/data-services/v1beta1/issues/{id}")
def get_data_services_v1beta1_issues_id(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_data_services_v1beta1_issues_id", dict())

@app.patch("/data-services/v1beta1/issues/{id}")
def patch_data_services_v1beta1_issues_id(id: str, payload: PatchDataServicesV1beta1IssuesIdRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("patch_data_services_v1beta1_issues_id", dict())

@app.delete("/data-services/v1beta1/issues/{id}")
def delete_data_services_v1beta1_issues_id(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("delete_data_services_v1beta1_issues_id", dict())

@app.get("/data-services/v1beta1/issues-metadata")
def get_data_services_v1beta1_issues_metadata():
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_data_services_v1beta1_issues_metadata", dict())

@app.get("/data-services/v1beta1/secrets/{id}")
def get_data_services_v1beta1_secrets_id(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_data_services_v1beta1_secrets_id", dict())

@app.get("/data-services/v1beta1/secrets")
def get_data_services_v1beta1_secrets():
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_data_services_v1beta1_secrets", dict())

@app.post("/data-services/v1beta1/secrets")
def post_data_services_v1beta1_secrets(payload: PostDataServicesV1beta1SecretsRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("post_data_services_v1beta1_secrets", dict())

@app.patch("/data-services/v1beta1/secrets/{id}")
def patch_data_services_v1beta1_secrets_id(id: str, payload: PatchDataServicesV1beta1SecretsIdRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("patch_data_services_v1beta1_secrets_id", dict())

@app.delete("/data-services/v1beta1/secrets/{id}")
def delete_data_services_v1beta1_secrets_id(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("delete_data_services_v1beta1_secrets_id", dict())

@app.get("/data-services/v1beta1/secret-assignments/{id}")
def get_data_services_v1beta1_secret_assignments_id(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_data_services_v1beta1_secret_assignments_id", dict())

@app.get("/data-services/v1beta1/secret-assignments")
def get_data_services_v1beta1_secret_assignments():
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_data_services_v1beta1_secret_assignments", dict())

@app.get("/data-services/v1beta1/settings")
def get_data_services_v1beta1_settings():
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_data_services_v1beta1_settings", dict())

@app.get("/data-services/v1beta1/settings/{id}")
def get_data_services_v1beta1_settings_id(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_data_services_v1beta1_settings_id", dict())

@app.patch("/data-services/v1beta1/settings/{id}")
def patch_data_services_v1beta1_settings_id(id: str, payload: PatchDataServicesV1beta1SettingsIdRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("patch_data_services_v1beta1_settings_id", dict())

@app.get("/data-services/v1beta1/software-components/{id}/install-release")
def get_data_services_v1beta1_software_components_id_install_release(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_data_services_v1beta1_software_components_id_install_release", dict())

@app.get("/data-services/v1beta1/software-releases/{id}")
def get_data_services_v1beta1_software_releases_id(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_data_services_v1beta1_software_releases_id", dict())

@app.get("/data-services/v1beta1/software-releases")
def get_data_services_v1beta1_software_releases():
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_data_services_v1beta1_software_releases", dict())

@app.post("/data-services/v1beta1/software-releases/{id}/download")
def post_data_services_v1beta1_software_releases_id_download(id: str, payload: PostDataServicesV1beta1SoftwareReleasesIdDownloadRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("post_data_services_v1beta1_software_releases_id_download", dict())

@app.get("/data-services/v1beta1/software-upgrades")
def get_data_services_v1beta1_software_upgrades():
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_data_services_v1beta1_software_upgrades", dict())

@app.get("/data-services/v1beta1/storage-locations")
def get_data_services_v1beta1_storage_locations():
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_data_services_v1beta1_storage_locations", dict())

@app.get("/data-services/v1beta1/tags")
def get_data_services_v1beta1_tags():
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_data_services_v1beta1_tags", dict())
