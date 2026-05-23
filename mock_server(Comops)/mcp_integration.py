import os
import requests
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("compute_ops")

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

@mcp.tool(description="Retrieve details of a specific secure gateway appliance by its ID.")
def get_secure_gateway_appliance_by_id(device_id: str):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta2/appliances/{device_id}"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Delete a specific secure gateway appliance by its ID.")
def delete_secure_gateway_appliance_by_id(device_id: str):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta2/appliances/{device_id}"
        params = {}
        payload = {}
        response = requests.delete(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Retrieve the certificate for a specific secure gateway appliance by its ID.")
def get_secure_gateway_appliance_certificate_by_id(device_id: str):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta2/appliances/{device_id}/certificate"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Retrieve a list of all appliance firmware bundles.")
def list_appliance_firmware_bundles_v1():
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1/appliance-firmware-bundles"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Retrieve details of a specific appliance firmware bundle by its ID.")
def get_appliance_firmware_bundle_by_id_v1(id: str):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1/appliance-firmware-bundles/{id}"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Retrieve a list of all appliance firmware bundles (beta).")
def list_appliance_firmware_bundles_v1beta1():
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta1/appliance-firmware-bundles"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Retrieve details of a specific appliance firmware bundle by its ID (beta).")
def get_appliance_firmware_bundle_by_id_v1beta1(id: str):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta1/appliance-firmware-bundles/{id}"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Create a new approval policy.")
def create_approval_policy(name: str = None, description: str = None, policyData: str = None):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta2/approval-policies"
        params = {}
        payload = {
            "name": name,
            "description": description,
            "policyData": policyData,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        response = requests.post(url, params=params, json=payload)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Retrieve a list of all active approval policies.")
def list_approval_policies():
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta2/approval-policies"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Retrieve a specific approval policy by its ID.")
def get_approval_policy_by_id(policy_id: str):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta2/approval-policies/{policy_id}"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Update an existing approval policy by its ID.")
def update_approval_policy_by_id(policy_id: str, name: str = None, description: str = None, policyData: str = None):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta2/approval-policies/{policy_id}"
        params = {}
        payload = {
            "name": name,
            "description": description,
            "policyData": policyData,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        response = requests.patch(url, params=params, json=payload)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Delete a specific approval policy by its ID.")
def delete_approval_policy_by_id(policy_id: str):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta2/approval-policies/{policy_id}"
        params = {}
        payload = {}
        response = requests.delete(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Retrieve a list of all active approval requests.")
def list_approval_requests():
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta2/approval-requests"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Retrieve a specific approval request by its ID.")
def get_approval_request_by_id(request_id: str):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta2/approval-requests/{request_id}"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Update an existing approval request by its ID, such as changing its state.")
def update_approval_request_by_id(request_id: str, approvalState: str = None, requestRemarks: str = None):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta2/approval-requests/{request_id}"
        params = {}
        payload = {
            "approvalState": approvalState,
            "requestRemarks": requestRemarks,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        response = requests.patch(url, params=params, json=payload)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Approve or decline an approval request.")
def approve_approval_request(request_id: str, approvalState: str = None, remarks: str = None):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta2/approval-requests/{request_id}/approve"
        params = {}
        payload = {
            "approvalState": approvalState,
            "remarks": remarks,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        response = requests.post(url, params=params, json=payload)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Retrieve a list of async operations for the last 7 days.")
def list_async_operations_v1():
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1/async-operations"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Retrieve a specific async operation by its ID for the last 7 days.")
def get_async_operation_by_id_v1(id: str):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1/async-operations/{id}"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Retrieve a list of async operations (beta).")
def list_async_operations_v1beta1():
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta1/async-operations"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Retrieve a specific async operation by its ID (beta).")
def get_async_operation_by_id_v1beta1(id: str):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta1/async-operations/{id}"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Retrieve details of a specific account by ID.")
def get_account_by_id_v1beta1(id: str):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta1/accounts/{id}"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="List tenants associated with a specific account.")
def list_account_tenants_v1beta1(id: str):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta1/accounts/{id}/tenants"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Create a new activation key.")
def create_activation_key_v1beta1(description: str = None):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta1/activation-keys"
        params = {}
        payload = {
            "description": description,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        response = requests.post(url, params=params, json=payload)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="List all activation keys.")
def list_activation_keys_v1beta1():
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta1/activation-keys"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Delete an activation key by its ID.")
def delete_activation_key_v1beta1(activation_key: str):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta1/activation-keys/{activation_key}"
        params = {}
        payload = {}
        response = requests.delete(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Create a new activation token (Deprecated).")
def create_activation_token_v1beta1(deviceId: str = None, durationMinutes: str = None):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta1/activation-tokens"
        params = {}
        payload = {
            "deviceId": deviceId,
            "durationMinutes": durationMinutes,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        response = requests.post(url, params=params, json=payload)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="List all activities.")
def list_activities_v1beta2():
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta2/activities"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Upload an AHS file.")
def upload_ahs_file_v1beta1(filename: str = None, description: str = None):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta1/ahs-files"
        params = {}
        payload = {
            "filename": filename,
            "description": description,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        response = requests.post(url, params=params, json=payload)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="List all AHS files.")
def list_ahs_files_v1beta1():
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta1/ahs-files"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Retrieve an AHS file by its ID.")
def get_ahs_file_by_id_v1beta1(id: str):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta1/ahs-files/{id}"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Update an AHS file by its ID.")
def update_ahs_file_v1beta1(id: str, description: str = None):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta1/ahs-files/{id}"
        params = {}
        payload = {
            "description": description,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        response = requests.patch(url, params=params, json=payload)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Initiate parsing of an AHS file.")
def parse_ahs_file_v1beta1(id: str):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta1/ahs-files/{id}/parse"
        params = {}
        payload = {}
        response = requests.post(url, params=params, json=payload)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Download an AHS file by its ID.")
def download_ahs_file_v1beta1(id: str):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta1/ahs-files/{id}/download"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="List all secure gateway appliances.")
def list_secure_gateway_appliances_v1beta2():
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta2/appliances"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Retrieve energy consumption metrics over a specified time period.")
def get_energy_over_time_v1beta1():
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta1/energy-over-time"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Retrieve energy consumption metrics aggregated by entity.")
def get_energy_by_entity_v1beta1():
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta1/energy-by-entity"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="List all external services.")
def list_external_services_v1beta1():
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta1/external-services"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Create a new external service integration.")
def create_external_service_v1beta1(name: str = None, endpoint: str = None, apiKey: str = None):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta1/external-services"
        params = {}
        payload = {
            "name": name,
            "endpoint": endpoint,
            "apiKey": apiKey,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        response = requests.post(url, params=params, json=payload)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Retrieve an external service by its ID.")
def get_external_service_by_id_v1beta1(id: str):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta1/external-services/{id}"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Delete an external service by its ID.")
def delete_external_service_v1beta1(id: str):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta1/external-services/{id}"
        params = {}
        payload = {}
        response = requests.delete(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Update an external service by its ID.")
def update_external_service_v1beta1(id: str, status: str = None):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta1/external-services/{id}"
        params = {}
        payload = {
            "status": status,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        response = requests.patch(url, params=params, json=payload)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Test the connection for an external service.")
def test_external_service_v1beta1(id: str):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta1/external-services/{id}/test"
        params = {}
        payload = {}
        response = requests.post(url, params=params, json=payload)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="List all saved filters.")
def list_filters_v1beta1():
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta1/filters"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Create a new filter.")
def create_filter_v1beta1(name: str = None, criteria: str = None):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta1/filters"
        params = {}
        payload = {
            "name": name,
            "criteria": criteria,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        response = requests.post(url, params=params, json=payload)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="List available properties for creating filters.")
def list_filter_properties_v1beta1():
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta1/filters/properties"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Retrieve a filter by its ID.")
def get_filter_by_id_v1beta1(id: str):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta1/filters/{id}"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Delete a filter by its ID.")
def delete_filter_v1beta1(id: str):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta1/filters/{id}"
        params = {}
        payload = {}
        response = requests.delete(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Update a filter by its ID.")
def update_filter_v1beta1(id: str, name: str = None):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta1/filters/{id}"
        params = {}
        payload = {
            "name": name,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        response = requests.patch(url, params=params, json=payload)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Retrieve resources that match a specific filter's criteria.")
def get_filter_matches_v1beta1(id: str):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta1/filters/{id}/matches"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="List all firmware bundles.")
def list_firmware_bundles_v1():
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1/firmware-bundles"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Retrieve a firmware bundle by its ID.")
def get_firmware_bundle_by_id_v1(id: str):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1/firmware-bundles/{id}"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Retrieve details of a specific firmware bundle.")
def get_firmware_bundle_details_v1(id: str):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1/firmware-bundles/{id}/bundle-details"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="List all firmware bundles (beta).")
def list_firmware_bundles_v1beta2():
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta2/firmware-bundles"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Retrieve a firmware bundle by its ID (beta).")
def get_firmware_bundle_by_id_v1beta2(id: str):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta2/firmware-bundles/{id}"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="List all groups.")
def list_groups_v1():
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1/groups"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Create a new group.")
def create_group_v1(name: str = None):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1/groups"
        params = {}
        payload = {
            "name": name,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        response = requests.post(url, params=params, json=payload)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Retrieve a group by its ID.")
def get_group_by_id_v1():
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1/groups/{group-id}"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Delete a group by its ID.")
def delete_group_v1():
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1/groups/{group-id}"
        params = {}
        payload = {}
        response = requests.delete(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Update a group by its ID.")
def update_group_v1(name: str = None):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1/groups/{group-id}"
        params = {}
        payload = {
            "name": name,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        response = requests.patch(url, params=params, json=payload)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Retrieve compliance status for a group.")
def get_group_compliance_v1():
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1/groups/{group-id}/compliance"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Retrieve a specific compliance report for a group.")
def get_group_compliance_report_v1():
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1/groups/{group-id}/compliance/{compliance-id}"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="List devices within a group.")
def list_group_devices_v1():
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1/groups/{group-id}/devices"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="List all groups (beta3).")
def list_groups_v1beta3():
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta3/groups"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Create a new group (beta3).")
def create_group_v1beta3(name: str = None):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta3/groups"
        params = {}
        payload = {
            "name": name,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        response = requests.post(url, params=params, json=payload)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Retrieve a group by its ID (beta3).")
def get_group_by_id_v1beta3():
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta3/groups/{group-id}"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Delete a group by its ID (beta3).")
def delete_group_v1beta3():
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta3/groups/{group-id}"
        params = {}
        payload = {}
        response = requests.delete(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Update a group by its ID (beta3).")
def update_group_v1beta3(name: str = None):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta3/groups/{group-id}"
        params = {}
        payload = {
            "name": name,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        response = requests.patch(url, params=params, json=payload)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Retrieve compliance status for a group (beta3).")
def get_group_compliance_v1beta3():
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta3/groups/{group-id}/compliance"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Retrieve a specific compliance report for a group (beta3).")
def get_group_compliance_report_v1beta3():
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta3/groups/{group-id}/compliance/{compliance-id}"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="List devices within a group (beta3).")
def list_group_devices_v1beta3():
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta3/groups/{group-id}/devices"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="List all groups (compute-ops, beta2).")
def list_groups_compute_ops_v1beta2():
    try:
        url = f"{API_BASE_URL}/compute-ops/v1beta2/groups"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Create a new group (compute-ops, beta2).")
def create_group_compute_ops_v1beta2(name: str = None):
    try:
        url = f"{API_BASE_URL}/compute-ops/v1beta2/groups"
        params = {}
        payload = {
            "name": name,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        response = requests.post(url, params=params, json=payload)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Retrieve a group by its ID (compute-ops, beta2).")
def get_group_by_id_compute_ops_v1beta2():
    try:
        url = f"{API_BASE_URL}/compute-ops/v1beta2/groups/{group-id}"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Delete a group by its ID (compute-ops, beta2).")
def delete_group_compute_ops_v1beta2():
    try:
        url = f"{API_BASE_URL}/compute-ops/v1beta2/groups/{group-id}"
        params = {}
        payload = {}
        response = requests.delete(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Update a group by its ID (compute-ops, beta2).")
def update_group_compute_ops_v1beta2(name: str = None):
    try:
        url = f"{API_BASE_URL}/compute-ops/v1beta2/groups/{group-id}"
        params = {}
        payload = {
            "name": name,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        response = requests.patch(url, params=params, json=payload)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Retrieve compliance status for a group (compute-ops, beta2).")
def get_group_compliance_compute_ops_v1beta2():
    try:
        url = f"{API_BASE_URL}/compute-ops/v1beta2/groups/{group-id}/compliance"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Retrieve a specific compliance report for a group (compute-ops, beta2).")
def get_group_compliance_report_compute_ops_v1beta2():
    try:
        url = f"{API_BASE_URL}/compute-ops/v1beta2/groups/{group-id}/compliance/{compliance-id}"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="List devices within a group (compute-ops, beta2).")
def list_group_devices_compute_ops_v1beta2():
    try:
        url = f"{API_BASE_URL}/compute-ops/v1beta2/groups/{group-id}/devices"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="List all job templates.")
def list_job_templates_v1beta2():
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta2/job-templates"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Retrieve a job template by its ID.")
def get_job_template_by_id_v1beta2(id: str):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta2/job-templates/{id}"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="List all jobs.")
def list_jobs_v1():
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1/jobs"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Create a new job.")
def create_job_v1(name: str = None, targetResource: str = None):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1/jobs"
        params = {}
        payload = {
            "name": name,
            "targetResource": targetResource,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        response = requests.post(url, params=params, json=payload)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Retrieve a job by its ID.")
def get_job_by_id_v1(id: str):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1/jobs/{id}"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Update a job by its ID.")
def update_job_v1(id: str, status: str = None):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1/jobs/{id}"
        params = {}
        payload = {
            "status": status,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        response = requests.patch(url, params=params, json=payload)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="List all jobs (beta3, Deprecated).")
def list_jobs_v1beta3():
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta3/jobs"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Create a new job (beta3, Deprecated).")
def create_job_v1beta3(name: str = None):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta3/jobs"
        params = {}
        payload = {
            "name": name,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        response = requests.post(url, params=params, json=payload)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Retrieve a job by its ID (beta3, Deprecated).")
def get_job_by_id_v1beta3(id: str):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta3/jobs/{id}"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Update a job by its ID (beta3, Deprecated).")
def update_job_v1beta3(id: str, status: str = None):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta3/jobs/{id}"
        params = {}
        payload = {
            "status": status,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        response = requests.patch(url, params=params, json=payload)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="List all jobs (beta2, Deprecated).")
def list_jobs_v1beta2():
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta2/jobs"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Create a new job (beta2, Deprecated).")
def create_job_v1beta2(name: str = None):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta2/jobs"
        params = {}
        payload = {
            "name": name,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        response = requests.post(url, params=params, json=payload)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Retrieve a job by its ID (beta2, Deprecated).")
def get_job_by_id_v1beta2(id: str):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta2/jobs/{id}"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Update a job by its ID (beta2, Deprecated).")
def update_job_v1beta2(id: str, status: str = None):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta2/jobs/{id}"
        params = {}
        payload = {
            "status": status,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        response = requests.patch(url, params=params, json=payload)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="List all metrics configurations.")
def list_metrics_configurations_v1():
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1/metrics-configurations"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Create a new metrics configuration.")
def create_metrics_configuration_v1(name: str = None, enabled: str = None, intervalSeconds: str = None):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1/metrics-configurations"
        params = {}
        payload = {
            "name": name,
            "enabled": enabled,
            "intervalSeconds": intervalSeconds,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        response = requests.post(url, params=params, json=payload)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Retrieve a metrics configuration by its ID.")
def get_metrics_configuration_by_id_v1(id: str):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1/metrics-configurations/{id}"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Delete a metrics configuration by its ID.")
def delete_metrics_configuration_v1(id: str):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1/metrics-configurations/{id}"
        params = {}
        payload = {}
        response = requests.delete(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Update a metrics configuration by its ID.")
def update_metrics_configuration_v1(id: str, enabled: str = None):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1/metrics-configurations/{id}"
        params = {}
        payload = {
            "enabled": enabled,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        response = requests.patch(url, params=params, json=payload)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="List all OneView appliances.")
def list_oneview_appliances_v1beta1():
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta1/oneview-appliances"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Register a new OneView appliance.")
def create_oneview_appliance_v1beta1(name: str = None, ipAddress: str = None, username: str = None, password: str = None):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta1/oneview-appliances"
        params = {}
        payload = {
            "name": name,
            "ipAddress": ipAddress,
            "username": username,
            "password": password,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        response = requests.post(url, params=params, json=payload)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Retrieve a OneView appliance by its ID.")
def get_oneview_appliance_by_id_v1beta1():
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta1/oneview-appliances/{device-id}"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Delete a OneView appliance by its ID.")
def delete_oneview_appliance_v1beta1():
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta1/oneview-appliances/{device-id}"
        params = {}
        payload = {}
        response = requests.delete(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Retrieve OneView integration settings.")
def get_oneview_settings_v1beta1():
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta1/oneview-settings"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="List all OneView server profiles/templates.")
def list_oneview_server_templates_v1beta1():
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta1/oneview-server-templates"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Retrieve a OneView server profile/template by its ID.")
def get_oneview_server_template_by_id_v1beta1(id: str):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta1/oneview-server-templates/{id}"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="List all reports.")
def list_reports_v1beta2():
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta2/reports"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Create a new report.")
def create_report_v1beta2(name: str = None, reportType: str = None, schedule: str = None):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta2/reports"
        params = {}
        payload = {
            "name": name,
            "reportType": reportType,
            "schedule": schedule,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        response = requests.post(url, params=params, json=payload)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Retrieve a report by its ID.")
def get_report_by_id_v1beta2(id: str):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta2/reports/{id}"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Retrieve the data content of a report.")
def get_report_data_v1beta2(id: str):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta2/reports/{id}/data"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="List all schedules.")
def list_schedules_v1beta2():
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta2/schedules"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Create a new schedule.")
def create_schedule_v1beta2(name: str = None, frequency: str = None, target: str = None):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta2/schedules"
        params = {}
        payload = {
            "name": name,
            "frequency": frequency,
            "target": target,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        response = requests.post(url, params=params, json=payload)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Retrieve a schedule by its ID.")
def get_schedule_by_id_v1beta2(id: str):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta2/schedules/{id}"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Delete a schedule by its ID.")
def delete_schedule_v1beta2(id: str):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta2/schedules/{id}"
        params = {}
        payload = {}
        response = requests.delete(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Update a schedule by its ID.")
def update_schedule_v1beta2(id: str, status: str = None):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta2/schedules/{id}"
        params = {}
        payload = {
            "status": status,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        response = requests.patch(url, params=params, json=payload)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="List the execution history of a schedule.")
def list_schedule_history_v1beta2(id: str):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta2/schedules/{id}/history"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Retrieve a specific history entry for a schedule.")
def get_schedule_history_entry_v1beta2(id: str):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta2/schedules/{id}/history/{history-id}"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Retrieve a server location by its ID.")
def get_server_location_by_id_v1beta1(location_id: str):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta1/server-locations/{location_id}"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Add a server to a specific location.")
def add_server_to_location_v1beta1(location_id: str, serverId: str = None):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta1/server-locations/{location_id}/servers"
        params = {}
        payload = {
            "serverId": serverId,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        response = requests.post(url, params=params, json=payload)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Remove a server from a specific location.")
def remove_server_from_location_v1beta1(location_id: str, serverId: str = None):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta1/server-locations/{location_id}/servers"
        params = {}
        payload = {
            "serverId": serverId,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        response = requests.delete(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="List all server settings profiles.")
def list_server_settings_compute_ops_v1beta1():
    try:
        url = f"{API_BASE_URL}/compute-ops/v1beta1/server-settings"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Create a new server setting profile.")
def create_server_setting_compute_ops_v1beta1(name: str = None, settings: str = None):
    try:
        url = f"{API_BASE_URL}/compute-ops/v1beta1/server-settings"
        params = {}
        payload = {
            "name": name,
            "settings": settings,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        response = requests.post(url, params=params, json=payload)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Retrieve a server setting profile by its ID.")
def get_server_setting_by_id_compute_ops_v1beta1(id: str):
    try:
        url = f"{API_BASE_URL}/compute-ops/v1beta1/server-settings/{id}"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Delete a server setting profile by its ID.")
def delete_server_setting_compute_ops_v1beta1(id: str):
    try:
        url = f"{API_BASE_URL}/compute-ops/v1beta1/server-settings/{id}"
        params = {}
        payload = {}
        response = requests.delete(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Update a server setting profile by its ID.")
def update_server_setting_compute_ops_v1beta1(id: str, settings: str = None):
    try:
        url = f"{API_BASE_URL}/compute-ops/v1beta1/server-settings/{id}"
        params = {}
        payload = {
            "settings": settings,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        response = requests.patch(url, params=params, json=payload)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="List all global settings.")
def list_settings_v1():
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1/settings"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Create a new global setting.")
def create_setting_v1(name: str = None, value: str = None):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1/settings"
        params = {}
        payload = {
            "name": name,
            "value": value,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        response = requests.post(url, params=params, json=payload)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Retrieve a global setting by its ID.")
def get_setting_by_id_v1(id: str):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1/settings/{id}"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Delete a global setting by its ID.")
def delete_setting_v1(id: str):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1/settings/{id}"
        params = {}
        payload = {}
        response = requests.delete(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Update a global setting by its ID.")
def update_setting_v1(id: str, value: str = None):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1/settings/{id}"
        params = {}
        payload = {
            "value": value,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        response = requests.patch(url, params=params, json=payload)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="List all global settings (beta).")
def list_settings_v1beta1():
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta1/settings"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Create a new global setting (beta).")
def create_setting_v1beta1(name: str = None, value: str = None):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta1/settings"
        params = {}
        payload = {
            "name": name,
            "value": value,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        response = requests.post(url, params=params, json=payload)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Retrieve a global setting by its ID (beta).")
def get_setting_by_id_v1beta1(id: str):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta1/settings/{id}"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Delete a global setting by its ID (beta).")
def delete_setting_v1beta1(id: str):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta1/settings/{id}"
        params = {}
        payload = {}
        response = requests.delete(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Update a global setting by its ID (beta).")
def update_setting_v1beta1(id: str, value: str = None):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta1/settings/{id}"
        params = {}
        payload = {
            "value": value,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        response = requests.patch(url, params=params, json=payload)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="List all servers.")
def list_servers_v1():
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1/servers"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Perform a bulk update on multiple servers.")
def bulk_update_servers_v1(filter: str = None, updates: str = None):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1/servers"
        params = {}
        payload = {
            "filter": filter,
            "updates": updates,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        response = requests.patch(url, params=params, json=payload)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Add a new server.")
def create_server_v1(name: str = None, ipAddress: str = None, credentials: str = None):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1/servers"
        params = {}
        payload = {
            "name": name,
            "ipAddress": ipAddress,
            "credentials": credentials,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        response = requests.post(url, params=params, json=payload)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Retrieve a server by its ID.")
def get_server_by_id_v1(id: str):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1/servers/{id}"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Update a server by its ID.")
def update_server_v1(id: str, name: str = None):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1/servers/{id}"
        params = {}
        payload = {
            "name": name,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        response = requests.patch(url, params=params, json=payload)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Delete a server by its ID.")
def delete_server_v1(id: str):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1/servers/{id}"
        params = {}
        payload = {}
        response = requests.delete(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="List alerts for a specific server.")
def list_server_alerts_v1(id: str):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1/servers/{id}/alerts"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Clear an alert for a specific server.")
def clear_server_alert_v1(id: str, alertId: str = None):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1/servers/{id}/clear-alert"
        params = {}
        payload = {
            "alertId": alertId,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        response = requests.post(url, params=params, json=payload)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="List all servers (beta2).")
def list_servers_v1beta2():
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta2/servers"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Perform a bulk update on multiple servers (beta2).")
def bulk_update_servers_v1beta2(filter: str = None, updates: str = None):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta2/servers"
        params = {}
        payload = {
            "filter": filter,
            "updates": updates,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        response = requests.patch(url, params=params, json=payload)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Add a new server (beta2).")
def create_server_v1beta2(name: str = None, ipAddress: str = None, credentials: str = None):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta2/servers"
        params = {}
        payload = {
            "name": name,
            "ipAddress": ipAddress,
            "credentials": credentials,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        response = requests.post(url, params=params, json=payload)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Retrieve a server by its ID (beta2).")
def get_server_by_id_v1beta2(id: str):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta2/servers/{id}"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Update a server by its ID (beta2).")
def update_server_v1beta2(id: str, name: str = None):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta2/servers/{id}"
        params = {}
        payload = {
            "name": name,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        response = requests.patch(url, params=params, json=payload)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Delete a server by its ID (beta2).")
def delete_server_v1beta2(id: str):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta2/servers/{id}"
        params = {}
        payload = {}
        response = requests.delete(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="List alerts for a specific server (beta2).")
def list_server_alerts_v1beta2(id: str):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta2/servers/{id}/alerts"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Clear an alert for a specific server (beta2).")
def clear_server_alert_v1beta2(id: str, alertId: str = None):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta2/servers/{id}/clear-alert"
        params = {}
        payload = {
            "alertId": alertId,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        response = requests.post(url, params=params, json=payload)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="List all server warranties.")
def list_server_warranties_v1beta2():
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta2/server-warranty"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Retrieve a server warranty by its ID.")
def get_server_warranty_by_id_v1beta2(id: str):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta2/server-warranty/{id}"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Retrieve user preferences.")
def get_user_preferences_v1():
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1/user-preferences"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Create user preferences.")
def create_user_preferences_v1(emailNotifications: str = None, theme: str = None):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1/user-preferences"
        params = {}
        payload = {
            "emailNotifications": emailNotifications,
            "theme": theme,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        response = requests.post(url, params=params, json=payload)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Retrieve user preferences by ID.")
def get_user_preference_by_id_v1(id: str):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1/user-preferences/{id}"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Update user preferences by ID (full replacement).")
def update_user_preferences_v1(id: str, emailNotifications: str = None, theme: str = None):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1/user-preferences/{id}"
        params = {}
        payload = {
            "emailNotifications": emailNotifications,
            "theme": theme,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        response = requests.put(url, params=params, json=payload)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Subscribe to user notifications.")
def subscribe_user_preferences_v1(notificationType: str = None, email: str = None):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1/user-preferences/subscribe"
        params = {}
        payload = {
            "notificationType": notificationType,
            "email": email,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        response = requests.post(url, params=params, json=payload)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Unsubscribe from user notifications.")
def unsubscribe_user_preferences_v1(notificationType: str = None, email: str = None):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1/user-preferences/unsubscribe"
        params = {}
        payload = {
            "notificationType": notificationType,
            "email": email,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        response = requests.post(url, params=params, json=payload)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Retrieve user preferences (beta).")
def get_user_preferences_v1beta1():
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta1/user-preferences"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Create user preferences (beta).")
def create_user_preferences_v1beta1(emailNotifications: str = None):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta1/user-preferences"
        params = {}
        payload = {
            "emailNotifications": emailNotifications,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        response = requests.post(url, params=params, json=payload)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Retrieve user preferences by ID (beta).")
def get_user_preference_by_id_v1beta1(id: str):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta1/user-preferences/{id}"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Update user preferences by ID (full replacement, beta).")
def update_user_preferences_v1beta1(id: str, emailNotifications: str = None):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta1/user-preferences/{id}"
        params = {}
        payload = {
            "emailNotifications": emailNotifications,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        response = requests.put(url, params=params, json=payload)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Retrieve utilization metrics over a specified time period.")
def get_utilization_over_time_v1beta1():
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta1/utilization-over-time"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Retrieve utilization metrics aggregated by entity.")
def get_utilization_by_entity_v1beta1():
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta1/utilization-by-entity"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="List all webhooks.")
def list_webhooks_v1beta1():
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta1/webhooks"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Create a new webhook.")
def create_webhook_v1beta1(name: str = None, url: str = None, events: str = None):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta1/webhooks"
        params = {}
        payload = {
            "name": name,
            "url": url,
            "events": events,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        response = requests.post(url, params=params, json=payload)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Retrieve a webhook by its ID.")
def get_webhook_by_id_v1beta1(webhook_id: str):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta1/webhooks/{webhook_id}"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Update a webhook by its ID.")
def update_webhook_v1beta1(webhook_id: str, events: str = None):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta1/webhooks/{webhook_id}"
        params = {}
        payload = {
            "events": events,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        response = requests.patch(url, params=params, json=payload)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Delete a webhook by its ID.")
def delete_webhook_v1beta1(webhook_id: str):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta1/webhooks/{webhook_id}"
        params = {}
        payload = {}
        response = requests.delete(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="List deliveries for a specific webhook.")
def list_webhook_deliveries_v1beta1(webhook_id: str):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta1/webhooks/{webhook_id}/deliveries"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Retrieve a specific delivery for a webhook.")
def get_webhook_delivery_by_id_v1beta1(webhook_id: str, delivery_id: str):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta1/webhooks/{webhook_id}/deliveries/{delivery_id}"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Assign device(s) to a group asynchronously.")
def post_compute_ops_mgmt_v1_groups_group_id_devices(devices: str = None):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1/groups/{group-id}/devices"
        params = {}
        payload = {
            "devices": devices,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        response = requests.post(url, params=params, json=payload)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Unassign device(s) from a group asynchronously.")
def post_compute_ops_mgmt_v1_groups_group_id_devices_unassign(devices: str = None):
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1/groups/{group-id}/devices/unassign"
        params = {}
        payload = {
            "devices": devices,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        response = requests.post(url, params=params, json=payload)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="List all external storage compliance details for a group.")
def get_compute_ops_mgmt_v1_groups_group_id_external_storage_compliance():
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1/groups/{group-id}/external-storage-compliance"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Assign device(s) to a group (v1beta3).")
def post_compute_ops_mgmt_v1beta3_groups_group_id_devices():
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta3/groups/{group-id}/devices"
        params = {}
        payload = {}
        response = requests.post(url, params=params, json=payload)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Unassign device(s) from a group (v1beta3).")
def post_compute_ops_mgmt_v1beta3_groups_group_id_devices_unassign():
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta3/groups/{group-id}/devices/unassign"
        params = {}
        payload = {}
        response = requests.post(url, params=params, json=payload)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="List all external storage compliance details for a group (v1beta3).")
def get_compute_ops_mgmt_v1beta3_groups_group_id_external_storage_compliance():
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta3/groups/{group-id}/external-storage-compliance"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="List all iLO Settings compliance for devices in a group (v1beta3).")
def get_compute_ops_mgmt_v1beta3_groups_group_id_ilo_settings_compliance():
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta3/groups/{group-id}/ilo-settings-compliance"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Get a device iLO Settings compliance by compliance ID within a group (v1beta3).")
def get_compute_ops_mgmt_v1beta3_groups_group_id_ilo_settings_compliance_ilo_settings_compliance_id():
    try:
        url = f"{API_BASE_URL}/compute-ops-mgmt/v1beta3/groups/{group-id}/ilo-settings-compliance/{ilo-settings-compliance-id}"
        params = {}
        payload = {}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}


# To use these tools in another FastMCP server, you can import `mcp` from this file.
# Example: from mcp_integration import mcp
