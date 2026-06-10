import os
import requests
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Storage")

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

@mcp.tool(description="List all asynchronous operations with optional filtering, sorting, and pagination.")
def list_asynchronous_operations():
    try:
        url = f"{API_BASE_URL}/data-services/v1beta1/async-operations"
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

@mcp.tool(description="Get details of a specific asynchronous operation by its ID.")
def get_asynchronous_operation(id: str):
    try:
        url = f"{API_BASE_URL}/data-services/v1beta1/async-operations/{id}"
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

@mcp.tool(description="List all dual authorization operations, allowing for filtering and pagination.")
def list_dual_authorization_operations():
    try:
        url = f"{API_BASE_URL}/data-services/v1beta1/dual-auth-operations"
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

@mcp.tool(description="Retrieve details of a specific dual authorization operation by its ID.")
def get_dual_authorization_operation(id: str):
    try:
        url = f"{API_BASE_URL}/data-services/v1beta1/dual-auth-operations/{id}"
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

@mcp.tool(description="Update the state or attributes of a specific dual authorization operation.")
def patch_dual_authorization_operation(id: str, state: str = None, checkedByEmail: str = None, checkedByUri: str = None, checkedAt: str = None):
    try:
        url = f"{API_BASE_URL}/data-services/v1beta1/dual-auth-operations/{id}"
        params = {}
        payload = {
            "state": state,
            "checkedByEmail": checkedByEmail,
            "checkedByUri": checkedByUri,
            "checkedAt": checkedAt,
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

@mcp.tool(description="Returns all active issues related to the current user, filtered by user access and permissions.")
def list_issues():
    try:
        url = f"{API_BASE_URL}/data-services/v1beta1/issues"
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

@mcp.tool(description="Returns a specific active issue by its given ID.")
def get_issue(id: str):
    try:
        url = f"{API_BASE_URL}/data-services/v1beta1/issues/{id}"
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

@mcp.tool(description="Changes the attributes of an existing Issue object.")
def patch_issue(id: str, state: str = None, resolutionDetails: str = None):
    try:
        url = f"{API_BASE_URL}/data-services/v1beta1/issues/{id}"
        params = {}
        payload = {
            "state": state,
            "resolutionDetails": resolutionDetails,
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

@mcp.tool(description="Deletes a specific Issue object from the database.")
def delete_issue(id: str):
    try:
        url = f"{API_BASE_URL}/data-services/v1beta1/issues/{id}"
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

@mcp.tool(description="Returns metadata for issues, including supported categories, services, and severities.")
def get_issues_metadata():
    try:
        url = f"{API_BASE_URL}/data-services/v1beta1/issues-metadata"
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

@mcp.tool(description="Reports the contents of a specific secret resource by its ID, excluding sensitive properties.")
def report_specific_secret(id: str):
    try:
        url = f"{API_BASE_URL}/data-services/v1beta1/secrets/{id}"
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

@mcp.tool(description="Reports all secret resources owned by the customer, subject to filtering query parameters.")
def report_filtered_secrets():
    try:
        url = f"{API_BASE_URL}/data-services/v1beta1/secrets"
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

@mcp.tool(description="Creates a new secret resource based on the provided specification in the request body.")
def add_secret(service: str = None, name: str = None, secret: str = None):
    try:
        url = f"{API_BASE_URL}/data-services/v1beta1/secrets"
        params = {}
        payload = {
            "service": service,
            "name": name,
            "secret": secret,
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

@mcp.tool(description="Updates an existing secret resource with the provided redefinition in the request body.")
def change_secret(id: str, secret: str = None, description: str = None):
    try:
        url = f"{API_BASE_URL}/data-services/v1beta1/secrets/{id}"
        params = {}
        payload = {
            "secret": secret,
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

@mcp.tool(description="Deletes the specified secret resource and all its associated secret-assignment resources.")
def remove_secret(id: str):
    try:
        url = f"{API_BASE_URL}/data-services/v1beta1/secrets/{id}"
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

@mcp.tool(description="Reports the contents of a specific secret-assignment resource by its ID.")
def report_specific_assignment(id: str):
    try:
        url = f"{API_BASE_URL}/data-services/v1beta1/secret-assignments/{id}"
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

@mcp.tool(description="Reports all secret-assignment resources owned by the customer, subject to filtering.")
def report_filtered_assignments():
    try:
        url = f"{API_BASE_URL}/data-services/v1beta1/secret-assignments"
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

@mcp.tool(description="Gets all the system setting values for the current account.")
def list_all_settings_of_service():
    try:
        url = f"{API_BASE_URL}/data-services/v1beta1/settings"
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

@mcp.tool(description="Gets the value for the current account for a specific input setting.")
def get_specific_setting_of_service(id: str):
    try:
        url = f"{API_BASE_URL}/data-services/v1beta1/settings/{id}"
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

@mcp.tool(description="Changes the value of a given system setting for the current account.")
def patch_specific_setting_of_service(id: str, value: str = None):
    try:
        url = f"{API_BASE_URL}/data-services/v1beta1/settings/{id}"
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

@mcp.tool(description="Retrieves the install release information for a specific software component.")
def get_software_component_install_release(id: str):
    try:
        url = f"{API_BASE_URL}/data-services/v1beta1/software-components/{id}/install-release"
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

@mcp.tool(description="Retrieve a specific software release by its ID.")
def get_software_release(id: str):
    try:
        url = f"{API_BASE_URL}/data-services/v1beta1/software-releases/{id}"
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

@mcp.tool(description="List software releases with support for filters, sorting, and pagination.")
def list_software_releases():
    try:
        url = f"{API_BASE_URL}/data-services/v1beta1/software-releases"
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

@mcp.tool(description="Initiates the download process for a specific software release file.")
def download_software_release(id: str, file: str = None):
    try:
        url = f"{API_BASE_URL}/data-services/v1beta1/software-releases/{id}/download"
        params = {}
        payload = {
            "file": file,
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

@mcp.tool(description="Lists all available software upgrades.")
def list_software_upgrades():
    try:
        url = f"{API_BASE_URL}/data-services/v1beta1/software-upgrades"
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

@mcp.tool(description="Provides a list of all supported cloud service provider storage locations.")
def list_storage_locations():
    try:
        url = f"{API_BASE_URL}/data-services/v1beta1/storage-locations"
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

@mcp.tool(description="Provides a list of available key-value pair tags for Data Services Cloud Console managed resources.")
def list_tags():
    try:
        url = f"{API_BASE_URL}/data-services/v1beta1/tags"
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
