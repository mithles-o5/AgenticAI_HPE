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

@app.post("/rest/login-sessions")
def post_rest_login_sessions(payload: PostRestLoginSessionsRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("post_rest_login_sessions", dict())

@app.post("/rest/login-sessions/auth-token")
def post_rest_login_sessions_auth_token(payload: PostRestLoginSessionsAuthTokenRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("post_rest_login_sessions_auth_token", dict())

@app.get("/rest/server-hardware")
def get_rest_server_hardware():
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_rest_server_hardware", dict())

@app.post("/rest/server-hardware")
def post_rest_server_hardware(payload: PostRestServerHardwareRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("post_rest_server_hardware", dict())

@app.get("/rest/server-hardware/*/firmware")
def get_rest_server_hardware_firmware():
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_rest_server_hardware_firmware", dict())

@app.post("/rest/server-hardware/discovery")
def post_rest_server_hardware_discovery(payload: PostRestServerHardwareDiscoveryRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("post_rest_server_hardware_discovery", dict())

@app.post("/rest/server-hardware/firmware-compliance")
def post_rest_server_hardware_firmware_compliance(payload: PostRestServerHardwareFirmwareComplianceRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("post_rest_server_hardware_firmware_compliance", dict())

@app.get("/rest/server-hardware/schema")
def get_rest_server_hardware_schema():
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_rest_server_hardware_schema", dict())

@app.get("/rest/server-hardware/{id}")
def get_rest_server_hardware_id(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_rest_server_hardware_id", dict())

@app.patch("/rest/server-hardware/{id}")
def patch_rest_server_hardware_id(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("patch_rest_server_hardware_id", dict())

@app.delete("/rest/server-hardware/{id}")
def delete_rest_server_hardware_id(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("delete_rest_server_hardware_id", dict())

@app.get("/rest/server-hardware/{id}/advancedMemoryProtection")
def get_rest_server_hardware_id_advancedmemoryprotection(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_rest_server_hardware_id_advancedmemoryprotection", dict())

@app.get("/rest/server-hardware/{id}/bios")
def get_rest_server_hardware_id_bios(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_rest_server_hardware_id_bios", dict())

@app.get("/rest/server-hardware/{id}/chassis")
def get_rest_server_hardware_id_chassis(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_rest_server_hardware_id_chassis", dict())

@app.get("/rest/server-hardware/{id}/devices")
def get_rest_server_hardware_id_devices(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_rest_server_hardware_id_devices", dict())

@app.get("/rest/server-hardware/{id}/environmentalConfiguration")
def get_rest_server_hardware_id_environmentalconfiguration(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_rest_server_hardware_id_environmentalconfiguration", dict())

@app.put("/rest/server-hardware/{id}/environmentalConfiguration")
def put_rest_server_hardware_id_environmentalconfiguration(id: str, payload: PutRestServerHardwareIdEnvironmentalconfigurationRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("put_rest_server_hardware_id_environmentalconfiguration", dict())

@app.get("/rest/server-hardware/{id}/firmware")
def get_rest_server_hardware_id_firmware(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_rest_server_hardware_id_firmware", dict())

@app.get("/rest/server-hardware/{id}/firmwareInventory")
def get_rest_server_hardware_id_firmwareinventory(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_rest_server_hardware_id_firmwareinventory", dict())
