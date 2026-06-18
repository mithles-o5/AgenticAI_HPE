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

@app.get("/compute-ops-mgmt/v1beta2/appliances/{device_id}")
def get_compute_ops_mgmt_v1beta2_appliances_device_id(device_id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta2_appliances_device_id", dict())

@app.delete("/compute-ops-mgmt/v1beta2/appliances/{device_id}")
def delete_compute_ops_mgmt_v1beta2_appliances_device_id(device_id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("delete_compute_ops_mgmt_v1beta2_appliances_device_id", dict())

@app.get("/compute-ops-mgmt/v1beta2/appliances/{device_id}/certificate")
def get_compute_ops_mgmt_v1beta2_appliances_device_id_certificate(device_id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta2_appliances_device_id_certificate", dict())

@app.get("/compute-ops-mgmt/v1/appliance-firmware-bundles")
def get_compute_ops_mgmt_v1_appliance_firmware_bundles():
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1_appliance_firmware_bundles", dict())

@app.get("/compute-ops-mgmt/v1/appliance-firmware-bundles/{id}")
def get_compute_ops_mgmt_v1_appliance_firmware_bundles_id(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1_appliance_firmware_bundles_id", dict())

@app.get("/compute-ops-mgmt/v1beta1/appliance-firmware-bundles")
def get_compute_ops_mgmt_v1beta1_appliance_firmware_bundles():
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta1_appliance_firmware_bundles", dict())

@app.get("/compute-ops-mgmt/v1beta1/appliance-firmware-bundles/{id}")
def get_compute_ops_mgmt_v1beta1_appliance_firmware_bundles_id(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta1_appliance_firmware_bundles_id", dict())

@app.post("/compute-ops-mgmt/v1beta2/approval-policies")
def post_compute_ops_mgmt_v1beta2_approval_policies(payload: PostComputeOpsMgmtV1beta2ApprovalPoliciesRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("post_compute_ops_mgmt_v1beta2_approval_policies", dict())

@app.get("/compute-ops-mgmt/v1beta2/approval-policies")
def get_compute_ops_mgmt_v1beta2_approval_policies():
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta2_approval_policies", dict())

@app.get("/compute-ops-mgmt/v1beta2/approval-policies/{policy_id}")
def get_compute_ops_mgmt_v1beta2_approval_policies_policy_id(policy_id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta2_approval_policies_policy_id", dict())

@app.patch("/compute-ops-mgmt/v1beta2/approval-policies/{policy_id}")
def patch_compute_ops_mgmt_v1beta2_approval_policies_policy_id(policy_id: str, payload: PatchComputeOpsMgmtV1beta2ApprovalPoliciesPolicyIdRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("patch_compute_ops_mgmt_v1beta2_approval_policies_policy_id", dict())

@app.delete("/compute-ops-mgmt/v1beta2/approval-policies/{policy_id}")
def delete_compute_ops_mgmt_v1beta2_approval_policies_policy_id(policy_id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("delete_compute_ops_mgmt_v1beta2_approval_policies_policy_id", dict())

@app.get("/compute-ops-mgmt/v1beta2/approval-requests")
def get_compute_ops_mgmt_v1beta2_approval_requests():
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta2_approval_requests", dict())

@app.get("/compute-ops-mgmt/v1beta2/approval-requests/{request_id}")
def get_compute_ops_mgmt_v1beta2_approval_requests_request_id(request_id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta2_approval_requests_request_id", dict())

@app.patch("/compute-ops-mgmt/v1beta2/approval-requests/{request_id}")
def patch_compute_ops_mgmt_v1beta2_approval_requests_request_id(request_id: str, payload: PatchComputeOpsMgmtV1beta2ApprovalRequestsRequestIdRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("patch_compute_ops_mgmt_v1beta2_approval_requests_request_id", dict())

@app.post("/compute-ops-mgmt/v1beta2/approval-requests/{request_id}/approve")
def post_compute_ops_mgmt_v1beta2_approval_requests_request_id_approve(request_id: str, payload: PostComputeOpsMgmtV1beta2ApprovalRequestsRequestIdApproveRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("post_compute_ops_mgmt_v1beta2_approval_requests_request_id_approve", dict())

@app.get("/compute-ops-mgmt/v1/async-operations")
def get_compute_ops_mgmt_v1_async_operations():
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1_async_operations", dict())

@app.get("/compute-ops-mgmt/v1/async-operations/{id}")
def get_compute_ops_mgmt_v1_async_operations_id(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1_async_operations_id", dict())

@app.get("/compute-ops-mgmt/v1beta1/async-operations")
def get_compute_ops_mgmt_v1beta1_async_operations():
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta1_async_operations", dict())

@app.get("/compute-ops-mgmt/v1beta1/async-operations/{id}")
def get_compute_ops_mgmt_v1beta1_async_operations_id(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta1_async_operations_id", dict())

@app.get("/compute-ops-mgmt/v1beta1/accounts/{id}")
def get_compute_ops_mgmt_v1beta1_accounts_id(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta1_accounts_id", dict())

@app.get("/compute-ops-mgmt/v1beta1/accounts/{id}/tenants")
def get_compute_ops_mgmt_v1beta1_accounts_id_tenants(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta1_accounts_id_tenants", dict())

@app.post("/compute-ops-mgmt/v1beta1/activation-keys")
def post_compute_ops_mgmt_v1beta1_activation_keys(payload: PostComputeOpsMgmtV1beta1ActivationKeysRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("post_compute_ops_mgmt_v1beta1_activation_keys", dict())

@app.get("/compute-ops-mgmt/v1beta1/activation-keys")
def get_compute_ops_mgmt_v1beta1_activation_keys():
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta1_activation_keys", dict())

@app.delete("/compute-ops-mgmt/v1beta1/activation-keys/{activation_key}")
def delete_compute_ops_mgmt_v1beta1_activation_keys_activation_key(activation_key: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("delete_compute_ops_mgmt_v1beta1_activation_keys_activation_key", dict())

@app.post("/compute-ops-mgmt/v1beta1/activation-tokens")
def post_compute_ops_mgmt_v1beta1_activation_tokens(payload: PostComputeOpsMgmtV1beta1ActivationTokensRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("post_compute_ops_mgmt_v1beta1_activation_tokens", dict())

@app.get("/compute-ops-mgmt/v1beta2/activities")
def get_compute_ops_mgmt_v1beta2_activities():
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta2_activities", dict())

@app.post("/compute-ops-mgmt/v1beta1/ahs-files")
def post_compute_ops_mgmt_v1beta1_ahs_files(payload: PostComputeOpsMgmtV1beta1AhsFilesRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("post_compute_ops_mgmt_v1beta1_ahs_files", dict())

@app.get("/compute-ops-mgmt/v1beta1/ahs-files")
def get_compute_ops_mgmt_v1beta1_ahs_files():
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta1_ahs_files", dict())

@app.get("/compute-ops-mgmt/v1beta1/ahs-files/{id}")
def get_compute_ops_mgmt_v1beta1_ahs_files_id(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta1_ahs_files_id", dict())

@app.patch("/compute-ops-mgmt/v1beta1/ahs-files/{id}")
def patch_compute_ops_mgmt_v1beta1_ahs_files_id(id: str, payload: PatchComputeOpsMgmtV1beta1AhsFilesIdRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("patch_compute_ops_mgmt_v1beta1_ahs_files_id", dict())

@app.post("/compute-ops-mgmt/v1beta1/ahs-files/{id}/parse")
def post_compute_ops_mgmt_v1beta1_ahs_files_id_parse(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("post_compute_ops_mgmt_v1beta1_ahs_files_id_parse", dict())

@app.get("/compute-ops-mgmt/v1beta1/ahs-files/{id}/download")
def get_compute_ops_mgmt_v1beta1_ahs_files_id_download(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta1_ahs_files_id_download", dict())

@app.get("/compute-ops-mgmt/v1beta2/appliances")
def get_compute_ops_mgmt_v1beta2_appliances():
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta2_appliances", dict())

@app.get("/compute-ops-mgmt/v1beta1/energy-over-time")
def get_compute_ops_mgmt_v1beta1_energy_over_time(serverId: str = None):
    """
    Returns energy utilization. Returns standby energy if server is off.
    """
    if serverId:
        server = find_server(serverId)
        if server and server.get("powerState") == "Off":
            return {"averagePowerWatts": 5.2}
    return {
        "averagePowerWatts": 205.5
    }

@app.get("/compute-ops-mgmt/v1beta1/energy-by-entity")
def get_compute_ops_mgmt_v1beta1_energy_by_entity(serverId: str = None):
    """
    Returns energy consumption by server.
    """
    if serverId:
        server = find_server(serverId)
        if server and server.get("powerState") == "Off":
            return {"entityPowerWatts": 5.2}
    return {
        "entityPowerWatts": 205.5
    }

@app.get("/compute-ops-mgmt/v1beta1/external-services")
def get_compute_ops_mgmt_v1beta1_external_services():
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta1_external_services", dict())

@app.post("/compute-ops-mgmt/v1beta1/external-services")
def post_compute_ops_mgmt_v1beta1_external_services(payload: PostComputeOpsMgmtV1beta1ExternalServicesRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("post_compute_ops_mgmt_v1beta1_external_services", dict())

@app.get("/compute-ops-mgmt/v1beta1/external-services/{id}")
def get_compute_ops_mgmt_v1beta1_external_services_id(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta1_external_services_id", dict())

@app.delete("/compute-ops-mgmt/v1beta1/external-services/{id}")
def delete_compute_ops_mgmt_v1beta1_external_services_id(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("delete_compute_ops_mgmt_v1beta1_external_services_id", dict())

@app.patch("/compute-ops-mgmt/v1beta1/external-services/{id}")
def patch_compute_ops_mgmt_v1beta1_external_services_id(id: str, payload: PatchComputeOpsMgmtV1beta1ExternalServicesIdRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("patch_compute_ops_mgmt_v1beta1_external_services_id", dict())

@app.post("/compute-ops-mgmt/v1beta1/external-services/{id}/test")
def post_compute_ops_mgmt_v1beta1_external_services_id_test(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("post_compute_ops_mgmt_v1beta1_external_services_id_test", dict())

@app.get("/compute-ops-mgmt/v1beta1/filters")
def get_compute_ops_mgmt_v1beta1_filters():
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta1_filters", dict())

@app.post("/compute-ops-mgmt/v1beta1/filters")
def post_compute_ops_mgmt_v1beta1_filters(payload: PostComputeOpsMgmtV1beta1FiltersRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("post_compute_ops_mgmt_v1beta1_filters", dict())

@app.get("/compute-ops-mgmt/v1beta1/filters/properties")
def get_compute_ops_mgmt_v1beta1_filters_properties():
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta1_filters_properties", dict())

@app.get("/compute-ops-mgmt/v1beta1/filters/{id}")
def get_compute_ops_mgmt_v1beta1_filters_id(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta1_filters_id", dict())

@app.delete("/compute-ops-mgmt/v1beta1/filters/{id}")
def delete_compute_ops_mgmt_v1beta1_filters_id(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("delete_compute_ops_mgmt_v1beta1_filters_id", dict())

@app.patch("/compute-ops-mgmt/v1beta1/filters/{id}")
def patch_compute_ops_mgmt_v1beta1_filters_id(id: str, payload: PatchComputeOpsMgmtV1beta1FiltersIdRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("patch_compute_ops_mgmt_v1beta1_filters_id", dict())

@app.get("/compute-ops-mgmt/v1beta1/filters/{id}/matches")
def get_compute_ops_mgmt_v1beta1_filters_id_matches(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta1_filters_id_matches", dict())

@app.get("/compute-ops-mgmt/v1/firmware-bundles")
def get_compute_ops_mgmt_v1_firmware_bundles():
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1_firmware_bundles", dict())

@app.get("/compute-ops-mgmt/v1/firmware-bundles/{id}")
def get_compute_ops_mgmt_v1_firmware_bundles_id(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1_firmware_bundles_id", dict())

@app.get("/compute-ops-mgmt/v1/firmware-bundles/{id}/bundle-details")
def get_compute_ops_mgmt_v1_firmware_bundles_id_bundle_details(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1_firmware_bundles_id_bundle_details", dict())

@app.get("/compute-ops-mgmt/v1beta2/firmware-bundles")
def get_compute_ops_mgmt_v1beta2_firmware_bundles():
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta2_firmware_bundles", dict())

@app.get("/compute-ops-mgmt/v1beta2/firmware-bundles/{id}")
def get_compute_ops_mgmt_v1beta2_firmware_bundles_id(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta2_firmware_bundles_id", dict())

@app.get("/compute-ops-mgmt/v1/groups")
def get_compute_ops_mgmt_v1_groups():
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1_groups", dict())

@app.post("/compute-ops-mgmt/v1/groups")
def post_compute_ops_mgmt_v1_groups(payload: PostComputeOpsMgmtV1GroupsRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("post_compute_ops_mgmt_v1_groups", dict())

@app.get("/compute-ops-mgmt/v1/groups/{group_id}")
def get_compute_ops_mgmt_v1_groups_group_id(group_id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1_groups_group_id", dict())

@app.delete("/compute-ops-mgmt/v1/groups/{group_id}")
def delete_compute_ops_mgmt_v1_groups_group_id(group_id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("delete_compute_ops_mgmt_v1_groups_group_id", dict())

@app.patch("/compute-ops-mgmt/v1/groups/{group_id}")
def patch_compute_ops_mgmt_v1_groups_group_id(group_id: str, payload: PatchComputeOpsMgmtV1GroupsGroupIdRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("patch_compute_ops_mgmt_v1_groups_group_id", dict())

@app.get("/compute-ops-mgmt/v1/groups/{group_id}/compliance")
def get_compute_ops_mgmt_v1_groups_group_id_compliance(group_id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1_groups_group_id_compliance", dict())

@app.get("/compute-ops-mgmt/v1/groups/{group_id}/compliance/{compliance_id}")
def get_compute_ops_mgmt_v1_groups_group_id_compliance_compliance_id(group_id: str, compliance_id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1_groups_group_id_compliance_compliance_id", dict())

@app.get("/compute-ops-mgmt/v1/groups/{group_id}/devices")
def get_compute_ops_mgmt_v1_groups_group_id_devices(group_id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1_groups_group_id_devices", dict())

@app.get("/compute-ops-mgmt/v1beta3/groups")
def get_compute_ops_mgmt_v1beta3_groups():
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta3_groups", dict())

@app.post("/compute-ops-mgmt/v1beta3/groups")
def post_compute_ops_mgmt_v1beta3_groups(payload: PostComputeOpsMgmtV1beta3GroupsRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("post_compute_ops_mgmt_v1beta3_groups", dict())

@app.get("/compute-ops-mgmt/v1beta3/groups/{group_id}")
def get_compute_ops_mgmt_v1beta3_groups_group_id(group_id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta3_groups_group_id", dict())

@app.delete("/compute-ops-mgmt/v1beta3/groups/{group_id}")
def delete_compute_ops_mgmt_v1beta3_groups_group_id(group_id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("delete_compute_ops_mgmt_v1beta3_groups_group_id", dict())

@app.patch("/compute-ops-mgmt/v1beta3/groups/{group_id}")
def patch_compute_ops_mgmt_v1beta3_groups_group_id(group_id: str, payload: PatchComputeOpsMgmtV1beta3GroupsGroupIdRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("patch_compute_ops_mgmt_v1beta3_groups_group_id", dict())

@app.get("/compute-ops-mgmt/v1beta3/groups/{group_id}/compliance")
def get_compute_ops_mgmt_v1beta3_groups_group_id_compliance(group_id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta3_groups_group_id_compliance", dict())

@app.get("/compute-ops-mgmt/v1beta3/groups/{group_id}/compliance/{compliance_id}")
def get_compute_ops_mgmt_v1beta3_groups_group_id_compliance_compliance_id(group_id: str, compliance_id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta3_groups_group_id_compliance_compliance_id", dict())

@app.get("/compute-ops-mgmt/v1beta3/groups/{group_id}/devices")
def get_compute_ops_mgmt_v1beta3_groups_group_id_devices(group_id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta3_groups_group_id_devices", dict())

@app.get("/compute-ops/v1beta2/groups")
def get_compute_ops_v1beta2_groups():
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_v1beta2_groups", dict())

@app.post("/compute-ops/v1beta2/groups")
def post_compute_ops_v1beta2_groups(payload: PostComputeOpsV1beta2GroupsRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("post_compute_ops_v1beta2_groups", dict())

@app.get("/compute-ops/v1beta2/groups/{group_id}")
def get_compute_ops_v1beta2_groups_group_id(group_id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_v1beta2_groups_group_id", dict())

@app.delete("/compute-ops/v1beta2/groups/{group_id}")
def delete_compute_ops_v1beta2_groups_group_id(group_id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("delete_compute_ops_v1beta2_groups_group_id", dict())

@app.patch("/compute-ops/v1beta2/groups/{group_id}")
def patch_compute_ops_v1beta2_groups_group_id(group_id: str, payload: PatchComputeOpsV1beta2GroupsGroupIdRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("patch_compute_ops_v1beta2_groups_group_id", dict())

@app.get("/compute-ops/v1beta2/groups/{group_id}/compliance")
def get_compute_ops_v1beta2_groups_group_id_compliance(group_id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_v1beta2_groups_group_id_compliance", dict())

@app.get("/compute-ops/v1beta2/groups/{group_id}/compliance/{compliance_id}")
def get_compute_ops_v1beta2_groups_group_id_compliance_compliance_id(group_id: str, compliance_id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_v1beta2_groups_group_id_compliance_compliance_id", dict())

@app.get("/compute-ops/v1beta2/groups/{group_id}/devices")
def get_compute_ops_v1beta2_groups_group_id_devices(group_id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_v1beta2_groups_group_id_devices", dict())

@app.get("/compute-ops-mgmt/v1beta2/job-templates")
def get_compute_ops_mgmt_v1beta2_job_templates():
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta2_job_templates", dict())

@app.get("/compute-ops-mgmt/v1beta2/job-templates/{id}")
def get_compute_ops_mgmt_v1beta2_job_templates_id(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta2_job_templates_id", dict())

@app.get("/compute-ops-mgmt/v1/jobs")
def get_compute_ops_mgmt_v1_jobs():
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1_jobs", dict())

@app.post("/compute-ops-mgmt/v1/jobs")
def post_compute_ops_mgmt_v1_jobs(payload: PostComputeOpsMgmtV1JobsRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("post_compute_ops_mgmt_v1_jobs", dict())

@app.get("/compute-ops-mgmt/v1/jobs/{id}")
def get_compute_ops_mgmt_v1_jobs_id(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1_jobs_id", dict())

@app.patch("/compute-ops-mgmt/v1/jobs/{id}")
def patch_compute_ops_mgmt_v1_jobs_id(id: str, payload: PatchComputeOpsMgmtV1JobsIdRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("patch_compute_ops_mgmt_v1_jobs_id", dict())

@app.get("/compute-ops-mgmt/v1beta3/jobs")
def get_compute_ops_mgmt_v1beta3_jobs():
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta3_jobs", dict())

@app.post("/compute-ops-mgmt/v1beta3/jobs")
def post_compute_ops_mgmt_v1beta3_jobs(payload: PostComputeOpsMgmtV1beta3JobsRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("post_compute_ops_mgmt_v1beta3_jobs", dict())

@app.get("/compute-ops-mgmt/v1beta3/jobs/{id}")
def get_compute_ops_mgmt_v1beta3_jobs_id(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta3_jobs_id", dict())

@app.patch("/compute-ops-mgmt/v1beta3/jobs/{id}")
def patch_compute_ops_mgmt_v1beta3_jobs_id(id: str, payload: PatchComputeOpsMgmtV1beta3JobsIdRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("patch_compute_ops_mgmt_v1beta3_jobs_id", dict())

@app.get("/compute-ops-mgmt/v1beta2/jobs")
def get_compute_ops_mgmt_v1beta2_jobs():
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta2_jobs", dict())

@app.post("/compute-ops-mgmt/v1beta2/jobs")
def post_compute_ops_mgmt_v1beta2_jobs(payload: PostComputeOpsMgmtV1beta2JobsRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("post_compute_ops_mgmt_v1beta2_jobs", dict())

@app.get("/compute-ops-mgmt/v1beta2/jobs/{id}")
def get_compute_ops_mgmt_v1beta2_jobs_id(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta2_jobs_id", dict())

@app.patch("/compute-ops-mgmt/v1beta2/jobs/{id}")
def patch_compute_ops_mgmt_v1beta2_jobs_id(id: str, payload: PatchComputeOpsMgmtV1beta2JobsIdRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("patch_compute_ops_mgmt_v1beta2_jobs_id", dict())

@app.get("/compute-ops-mgmt/v1/metrics-configurations")
def get_compute_ops_mgmt_v1_metrics_configurations():
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1_metrics_configurations", dict())

@app.post("/compute-ops-mgmt/v1/metrics-configurations")
def post_compute_ops_mgmt_v1_metrics_configurations(payload: PostComputeOpsMgmtV1MetricsConfigurationsRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("post_compute_ops_mgmt_v1_metrics_configurations", dict())

@app.get("/compute-ops-mgmt/v1/metrics-configurations/{id}")
def get_compute_ops_mgmt_v1_metrics_configurations_id(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1_metrics_configurations_id", dict())

@app.delete("/compute-ops-mgmt/v1/metrics-configurations/{id}")
def delete_compute_ops_mgmt_v1_metrics_configurations_id(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("delete_compute_ops_mgmt_v1_metrics_configurations_id", dict())

@app.patch("/compute-ops-mgmt/v1/metrics-configurations/{id}")
def patch_compute_ops_mgmt_v1_metrics_configurations_id(id: str, payload: PatchComputeOpsMgmtV1MetricsConfigurationsIdRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("patch_compute_ops_mgmt_v1_metrics_configurations_id", dict())

@app.get("/compute-ops-mgmt/v1beta1/oneview-appliances")
def get_compute_ops_mgmt_v1beta1_oneview_appliances():
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta1_oneview_appliances", dict())

@app.post("/compute-ops-mgmt/v1beta1/oneview-appliances")
def post_compute_ops_mgmt_v1beta1_oneview_appliances(payload: PostComputeOpsMgmtV1beta1OneviewAppliancesRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("post_compute_ops_mgmt_v1beta1_oneview_appliances", dict())

@app.get("/compute-ops-mgmt/v1beta1/oneview-appliances/{device_id}")
def get_compute_ops_mgmt_v1beta1_oneview_appliances_device_id(device_id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta1_oneview_appliances_device_id", dict())

@app.delete("/compute-ops-mgmt/v1beta1/oneview-appliances/{device_id}")
def delete_compute_ops_mgmt_v1beta1_oneview_appliances_device_id(device_id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("delete_compute_ops_mgmt_v1beta1_oneview_appliances_device_id", dict())

@app.get("/compute-ops-mgmt/v1beta1/oneview-settings")
def get_compute_ops_mgmt_v1beta1_oneview_settings():
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta1_oneview_settings", dict())

@app.get("/compute-ops-mgmt/v1beta1/oneview-server-templates")
def get_compute_ops_mgmt_v1beta1_oneview_server_templates():
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta1_oneview_server_templates", dict())

@app.get("/compute-ops-mgmt/v1beta1/oneview-server-templates/{id}")
def get_compute_ops_mgmt_v1beta1_oneview_server_templates_id(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta1_oneview_server_templates_id", dict())

@app.get("/compute-ops-mgmt/v1beta2/reports")
def get_compute_ops_mgmt_v1beta2_reports():
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta2_reports", dict())

@app.post("/compute-ops-mgmt/v1beta2/reports")
def post_compute_ops_mgmt_v1beta2_reports(payload: PostComputeOpsMgmtV1beta2ReportsRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("post_compute_ops_mgmt_v1beta2_reports", dict())

@app.get("/compute-ops-mgmt/v1beta2/reports/{id}")
def get_compute_ops_mgmt_v1beta2_reports_id(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta2_reports_id", dict())

@app.get("/compute-ops-mgmt/v1beta2/reports/{id}/data")
def get_compute_ops_mgmt_v1beta2_reports_id_data(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta2_reports_id_data", dict())

@app.get("/compute-ops-mgmt/v1beta2/schedules")
def get_compute_ops_mgmt_v1beta2_schedules():
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta2_schedules", dict())

@app.post("/compute-ops-mgmt/v1beta2/schedules")
def post_compute_ops_mgmt_v1beta2_schedules(payload: PostComputeOpsMgmtV1beta2SchedulesRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("post_compute_ops_mgmt_v1beta2_schedules", dict())

@app.get("/compute-ops-mgmt/v1beta2/schedules/{id}")
def get_compute_ops_mgmt_v1beta2_schedules_id(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta2_schedules_id", dict())

@app.delete("/compute-ops-mgmt/v1beta2/schedules/{id}")
def delete_compute_ops_mgmt_v1beta2_schedules_id(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("delete_compute_ops_mgmt_v1beta2_schedules_id", dict())

@app.patch("/compute-ops-mgmt/v1beta2/schedules/{id}")
def patch_compute_ops_mgmt_v1beta2_schedules_id(id: str, payload: PatchComputeOpsMgmtV1beta2SchedulesIdRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("patch_compute_ops_mgmt_v1beta2_schedules_id", dict())

@app.get("/compute-ops-mgmt/v1beta2/schedules/{id}/history")
def get_compute_ops_mgmt_v1beta2_schedules_id_history(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta2_schedules_id_history", dict())

@app.get("/compute-ops-mgmt/v1beta2/schedules/{id}/history/{history_id}")
def get_compute_ops_mgmt_v1beta2_schedules_id_history_history_id(history_id: str, id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta2_schedules_id_history_history_id", dict())

@app.get("/compute-ops-mgmt/v1beta1/server-locations/{location_id}")
def get_compute_ops_mgmt_v1beta1_server_locations_location_id(location_id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta1_server_locations_location_id", dict())

@app.post("/compute-ops-mgmt/v1beta1/server-locations/{location_id}/servers")
def post_compute_ops_mgmt_v1beta1_server_locations_location_id_servers(location_id: str, payload: PostComputeOpsMgmtV1beta1ServerLocationsLocationIdServersRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("post_compute_ops_mgmt_v1beta1_server_locations_location_id_servers", dict())

@app.delete("/compute-ops-mgmt/v1beta1/server-locations/{location_id}/servers")
def delete_compute_ops_mgmt_v1beta1_server_locations_location_id_servers(location_id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("delete_compute_ops_mgmt_v1beta1_server_locations_location_id_servers", dict())

@app.get("/compute-ops/v1beta1/server-settings")
def get_compute_ops_v1beta1_server_settings():
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_v1beta1_server_settings", dict())

@app.post("/compute-ops/v1beta1/server-settings")
def post_compute_ops_v1beta1_server_settings(payload: PostComputeOpsV1beta1ServerSettingsRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("post_compute_ops_v1beta1_server_settings", dict())

@app.get("/compute-ops/v1beta1/server-settings/{id}")
def get_compute_ops_v1beta1_server_settings_id(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_v1beta1_server_settings_id", dict())

@app.delete("/compute-ops/v1beta1/server-settings/{id}")
def delete_compute_ops_v1beta1_server_settings_id(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("delete_compute_ops_v1beta1_server_settings_id", dict())

@app.patch("/compute-ops/v1beta1/server-settings/{id}")
def patch_compute_ops_v1beta1_server_settings_id(id: str, payload: PatchComputeOpsV1beta1ServerSettingsIdRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("patch_compute_ops_v1beta1_server_settings_id", dict())

def find_server(id: str):
    servers = MOCK_DB.get("servers", {})
    if id in servers:
        return servers[id]
    
    import re
    match = re.search(r"(\d+)$", id)
    if match:
        suffix = match.group(1)
        suffix_val = int(suffix)
        for s_id, s_data in servers.items():
            name = s_data.get("name", "")
            if name.endswith(f"-{suffix}") or name.endswith(f"-{suffix_val}"):
                return s_data
            if s_id.startswith(id) or id.startswith(s_id):
                return s_data

    for s_id, s_data in servers.items():
        if s_data.get("name", "").lower() == id.lower():
            return s_data
        if s_data.get("ip_address") == id:
            return s_data

    return None

@app.get("/compute-ops-mgmt/v1/servers/{id}")
def get_compute_ops_mgmt_v1_servers_id(id: str):
    server = find_server(id)
    if server:
        return server
    from fastapi import HTTPException
    raise HTTPException(status_code=404, detail="Resource not found")

# --- Added specifically for 1500-server scaling Demo ---
@app.post("/compute-ops-mgmt/v1/servers/{id}/power-on")
def post_compute_ops_mgmt_v1_servers_id_power_on(id: str):
    """
    Handles power-on commands for ANY dynamically generated ComOps server.
    """
    server = find_server(id)
    if server:
        server["powerState"] = "On"
        try:
            with open(mock_file, "w", encoding="utf-8") as f:
                json.dump(MOCK_DB, f, indent=4)
        except Exception as e:
            print(f"Error writing to mock_data.json: {e}")
            
        return {
            "status": "success",
            "message": f"Cloud Node {id} powered ON successfully.",
            "action": "power-on",
            "uuid": server.get("uuid", id),
            "server_details": server
        }
    return {
        "status": "success",
        "message": f"Cloud Node {id} powered ON successfully.",
        "action": "power-on",
        "uuid": id
    }

@app.post("/compute-ops-mgmt/v1/servers/{id}/power-off")
def post_compute_ops_mgmt_v1_servers_id_power_off(id: str):
    """
    Handles power-off commands for ANY dynamically generated ComOps server.
    """
    server = find_server(id)
    if server:
        server["powerState"] = "Off"
        try:
            with open(mock_file, "w", encoding="utf-8") as f:
                json.dump(MOCK_DB, f, indent=4)
        except Exception as e:
            print(f"Error writing to mock_data.json: {e}")
            
        return {
            "status": "success",
            "message": f"Cloud Node {id} powered OFF successfully.",
            "action": "power-off",
            "uuid": server.get("uuid", id),
            "server_details": server
        }
    return {
        "status": "success",
        "message": f"Cloud Node {id} powered OFF successfully.",
        "action": "power-off",
        "uuid": id
    }

@app.get("/compute-ops-mgmt/v1/settings")
def get_compute_ops_mgmt_v1_settings():
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1_settings", dict())

@app.post("/compute-ops-mgmt/v1/settings")
def post_compute_ops_mgmt_v1_settings(payload: PostComputeOpsMgmtV1SettingsRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("post_compute_ops_mgmt_v1_settings", dict())

@app.get("/compute-ops-mgmt/v1/settings/{id}")
def get_compute_ops_mgmt_v1_settings_id(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1_settings_id", dict())

@app.delete("/compute-ops-mgmt/v1/settings/{id}")
def delete_compute_ops_mgmt_v1_settings_id(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("delete_compute_ops_mgmt_v1_settings_id", dict())

@app.patch("/compute-ops-mgmt/v1/settings/{id}")
def patch_compute_ops_mgmt_v1_settings_id(id: str, payload: PatchComputeOpsMgmtV1SettingsIdRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("patch_compute_ops_mgmt_v1_settings_id", dict())

@app.get("/compute-ops-mgmt/v1beta1/settings")
def get_compute_ops_mgmt_v1beta1_settings():
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta1_settings", dict())

@app.post("/compute-ops-mgmt/v1beta1/settings")
def post_compute_ops_mgmt_v1beta1_settings(payload: PostComputeOpsMgmtV1beta1SettingsRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("post_compute_ops_mgmt_v1beta1_settings", dict())

@app.get("/compute-ops-mgmt/v1beta1/settings/{id}")
def get_compute_ops_mgmt_v1beta1_settings_id(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta1_settings_id", dict())

@app.delete("/compute-ops-mgmt/v1beta1/settings/{id}")
def delete_compute_ops_mgmt_v1beta1_settings_id(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("delete_compute_ops_mgmt_v1beta1_settings_id", dict())

@app.patch("/compute-ops-mgmt/v1beta1/settings/{id}")
def patch_compute_ops_mgmt_v1beta1_settings_id(id: str, payload: PatchComputeOpsMgmtV1beta1SettingsIdRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("patch_compute_ops_mgmt_v1beta1_settings_id", dict())

@app.get("/compute-ops-mgmt/v1/servers")
def get_compute_ops_mgmt_v1_servers():
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1_servers", dict())

@app.patch("/compute-ops-mgmt/v1/servers")
def patch_compute_ops_mgmt_v1_servers(payload: PatchComputeOpsMgmtV1ServersRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("patch_compute_ops_mgmt_v1_servers", dict())

@app.post("/compute-ops-mgmt/v1/servers")
def post_compute_ops_mgmt_v1_servers(payload: PostComputeOpsMgmtV1ServersRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("post_compute_ops_mgmt_v1_servers", dict())

@app.get("/compute-ops-mgmt/v1/servers/{id}")
def get_compute_ops_mgmt_v1_servers_id(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1_servers_id", dict())

@app.patch("/compute-ops-mgmt/v1/servers/{id}")
def patch_compute_ops_mgmt_v1_servers_id(id: str, payload: PatchComputeOpsMgmtV1ServersIdRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("patch_compute_ops_mgmt_v1_servers_id", dict())

@app.delete("/compute-ops-mgmt/v1/servers/{id}")
def delete_compute_ops_mgmt_v1_servers_id(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("delete_compute_ops_mgmt_v1_servers_id", dict())

@app.get("/compute-ops-mgmt/v1/servers/{id}/alerts")
def get_compute_ops_mgmt_v1_servers_id_alerts(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1_servers_id_alerts", dict())

@app.post("/compute-ops-mgmt/v1/servers/{id}/clear-alert")
def post_compute_ops_mgmt_v1_servers_id_clear_alert(id: str, payload: PostComputeOpsMgmtV1ServersIdClearAlertRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("post_compute_ops_mgmt_v1_servers_id_clear_alert", dict())

@app.get("/compute-ops-mgmt/v1beta2/servers")
def get_compute_ops_mgmt_v1beta2_servers():
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta2_servers", dict())

@app.patch("/compute-ops-mgmt/v1beta2/servers")
def patch_compute_ops_mgmt_v1beta2_servers(payload: PatchComputeOpsMgmtV1beta2ServersRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("patch_compute_ops_mgmt_v1beta2_servers", dict())

@app.post("/compute-ops-mgmt/v1beta2/servers")
def post_compute_ops_mgmt_v1beta2_servers(payload: PostComputeOpsMgmtV1beta2ServersRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("post_compute_ops_mgmt_v1beta2_servers", dict())

@app.get("/compute-ops-mgmt/v1beta2/servers/{id}")
def get_compute_ops_mgmt_v1beta2_servers_id(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta2_servers_id", dict())

@app.patch("/compute-ops-mgmt/v1beta2/servers/{id}")
def patch_compute_ops_mgmt_v1beta2_servers_id(id: str, payload: PatchComputeOpsMgmtV1beta2ServersIdRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("patch_compute_ops_mgmt_v1beta2_servers_id", dict())

@app.delete("/compute-ops-mgmt/v1beta2/servers/{id}")
def delete_compute_ops_mgmt_v1beta2_servers_id(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("delete_compute_ops_mgmt_v1beta2_servers_id", dict())

@app.get("/compute-ops-mgmt/v1beta2/servers/{id}/alerts")
def get_compute_ops_mgmt_v1beta2_servers_id_alerts(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta2_servers_id_alerts", dict())

@app.post("/compute-ops-mgmt/v1beta2/servers/{id}/clear-alert")
def post_compute_ops_mgmt_v1beta2_servers_id_clear_alert(id: str, payload: PostComputeOpsMgmtV1beta2ServersIdClearAlertRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("post_compute_ops_mgmt_v1beta2_servers_id_clear_alert", dict())

@app.get("/compute-ops-mgmt/v1beta2/server-warranty")
def get_compute_ops_mgmt_v1beta2_server_warranty():
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta2_server_warranty", dict())

@app.get("/compute-ops-mgmt/v1beta2/server-warranty/{id}")
def get_compute_ops_mgmt_v1beta2_server_warranty_id(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta2_server_warranty_id", dict())

@app.get("/compute-ops-mgmt/v1/user-preferences")
def get_compute_ops_mgmt_v1_user_preferences():
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1_user_preferences", dict())

@app.post("/compute-ops-mgmt/v1/user-preferences")
def post_compute_ops_mgmt_v1_user_preferences(payload: PostComputeOpsMgmtV1UserPreferencesRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("post_compute_ops_mgmt_v1_user_preferences", dict())

@app.get("/compute-ops-mgmt/v1/user-preferences/{id}")
def get_compute_ops_mgmt_v1_user_preferences_id(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1_user_preferences_id", dict())

@app.put("/compute-ops-mgmt/v1/user-preferences/{id}")
def put_compute_ops_mgmt_v1_user_preferences_id(id: str, payload: PutComputeOpsMgmtV1UserPreferencesIdRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("put_compute_ops_mgmt_v1_user_preferences_id", dict())

@app.post("/compute-ops-mgmt/v1/user-preferences/subscribe")
def post_compute_ops_mgmt_v1_user_preferences_subscribe(payload: PostComputeOpsMgmtV1UserPreferencesSubscribeRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("post_compute_ops_mgmt_v1_user_preferences_subscribe", dict())

@app.post("/compute-ops-mgmt/v1/user-preferences/unsubscribe")
def post_compute_ops_mgmt_v1_user_preferences_unsubscribe(payload: PostComputeOpsMgmtV1UserPreferencesUnsubscribeRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("post_compute_ops_mgmt_v1_user_preferences_unsubscribe", dict())

@app.get("/compute-ops-mgmt/v1beta1/user-preferences")
def get_compute_ops_mgmt_v1beta1_user_preferences():
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta1_user_preferences", dict())

@app.post("/compute-ops-mgmt/v1beta1/user-preferences")
def post_compute_ops_mgmt_v1beta1_user_preferences(payload: PostComputeOpsMgmtV1beta1UserPreferencesRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("post_compute_ops_mgmt_v1beta1_user_preferences", dict())

@app.get("/compute-ops-mgmt/v1beta1/user-preferences/{id}")
def get_compute_ops_mgmt_v1beta1_user_preferences_id(id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta1_user_preferences_id", dict())

@app.put("/compute-ops-mgmt/v1beta1/user-preferences/{id}")
def put_compute_ops_mgmt_v1beta1_user_preferences_id(id: str, payload: PutComputeOpsMgmtV1beta1UserPreferencesIdRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("put_compute_ops_mgmt_v1beta1_user_preferences_id", dict())

@app.get("/compute-ops-mgmt/v1beta1/utilization-over-time")
def get_compute_ops_mgmt_v1beta1_utilization_over_time(serverId: str = None):
    """
    Returns utilization over time. If server is off, utilization averages are 0.
    """
    if serverId:
        server = find_server(serverId)
        if server and server.get("powerState") == "Off":
            return {
                "cpuAveragePercent": 0.0,
                "memoryAveragePercent": 0.0
            }
    return {
        "cpuAveragePercent": 40.5,
        "memoryAveragePercent": 55.2
    }

@app.get("/compute-ops-mgmt/v1beta1/utilization-by-entity")
def get_compute_ops_mgmt_v1beta1_utilization_by_entity():
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta1_utilization_by_entity", dict())

@app.get("/compute-ops-mgmt/v1beta1/webhooks")
def get_compute_ops_mgmt_v1beta1_webhooks():
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta1_webhooks", dict())

@app.post("/compute-ops-mgmt/v1beta1/webhooks")
def post_compute_ops_mgmt_v1beta1_webhooks(payload: PostComputeOpsMgmtV1beta1WebhooksRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("post_compute_ops_mgmt_v1beta1_webhooks", dict())

@app.get("/compute-ops-mgmt/v1beta1/webhooks/{webhook_id}")
def get_compute_ops_mgmt_v1beta1_webhooks_webhook_id(webhook_id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta1_webhooks_webhook_id", dict())

@app.patch("/compute-ops-mgmt/v1beta1/webhooks/{webhook_id}")
def patch_compute_ops_mgmt_v1beta1_webhooks_webhook_id(webhook_id: str, payload: PatchComputeOpsMgmtV1beta1WebhooksWebhookIdRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("patch_compute_ops_mgmt_v1beta1_webhooks_webhook_id", dict())

@app.delete("/compute-ops-mgmt/v1beta1/webhooks/{webhook_id}")
def delete_compute_ops_mgmt_v1beta1_webhooks_webhook_id(webhook_id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("delete_compute_ops_mgmt_v1beta1_webhooks_webhook_id", dict())

@app.get("/compute-ops-mgmt/v1beta1/webhooks/{webhook_id}/deliveries")
def get_compute_ops_mgmt_v1beta1_webhooks_webhook_id_deliveries(webhook_id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta1_webhooks_webhook_id_deliveries", dict())

@app.get("/compute-ops-mgmt/v1beta1/webhooks/{webhook_id}/deliveries/{delivery_id}")
def get_compute_ops_mgmt_v1beta1_webhooks_webhook_id_deliveries_delivery_id(webhook_id: str, delivery_id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta1_webhooks_webhook_id_deliveries_delivery_id", dict())

@app.post("/compute-ops-mgmt/v1/groups/{group_id}/devices")
def post_compute_ops_mgmt_v1_groups_group_id_devices(group_id: str, payload: PostComputeOpsMgmtV1GroupsGroupIdDevicesRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("post_compute_ops_mgmt_v1_groups_group_id_devices", dict())

@app.post("/compute-ops-mgmt/v1/groups/{group_id}/devices/unassign")
def post_compute_ops_mgmt_v1_groups_group_id_devices_unassign(group_id: str, payload: PostComputeOpsMgmtV1GroupsGroupIdDevicesUnassignRequest):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("post_compute_ops_mgmt_v1_groups_group_id_devices_unassign", dict())

@app.get("/compute-ops-mgmt/v1/groups/{group_id}/external-storage-compliance")
def get_compute_ops_mgmt_v1_groups_group_id_external_storage_compliance(group_id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1_groups_group_id_external_storage_compliance", dict())

@app.post("/compute-ops-mgmt/v1beta3/groups/{group_id}/devices")
def post_compute_ops_mgmt_v1beta3_groups_group_id_devices(group_id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("post_compute_ops_mgmt_v1beta3_groups_group_id_devices", dict())

@app.post("/compute-ops-mgmt/v1beta3/groups/{group_id}/devices/unassign")
def post_compute_ops_mgmt_v1beta3_groups_group_id_devices_unassign(group_id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("post_compute_ops_mgmt_v1beta3_groups_group_id_devices_unassign", dict())

@app.get("/compute-ops-mgmt/v1beta3/groups/{group_id}/external-storage-compliance")
def get_compute_ops_mgmt_v1beta3_groups_group_id_external_storage_compliance(group_id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta3_groups_group_id_external_storage_compliance", dict())

@app.get("/compute-ops-mgmt/v1beta3/groups/{group_id}/ilo-settings-compliance")
def get_compute_ops_mgmt_v1beta3_groups_group_id_ilo_settings_compliance(group_id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta3_groups_group_id_ilo_settings_compliance", dict())

@app.get("/compute-ops-mgmt/v1beta3/groups/{group_id}/ilo-settings-compliance/{ilo_settings_compliance_id}")
def get_compute_ops_mgmt_v1beta3_groups_group_id_ilo_settings_compliance_ilo_settings_compliance_id(group_id: str, ilo_settings_compliance_id: str):
    """
    Auto-generated Route
    Original Doc: Batch Extracted
    """
    return MOCK_DB.get("get_compute_ops_mgmt_v1beta3_groups_group_id_ilo_settings_compliance_ilo_settings_compliance_id", dict())
