import os
import requests
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("mock_v4")

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

@mcp.tool(description="Request a session token for user authentication.")
def create_login_session(userName: str = None, password: str = None):
    try:
        url = f"{API_BASE_URL}/rest/login-sessions"
        params = {}
        payload = {
            "userName": userName,
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

@mcp.tool(description="Create a new session token with a subset of user permissions.")
def create_restricted_login_session(sessionToken: str = None, scopeUris: str = None):
    try:
        url = f"{API_BASE_URL}/rest/login-sessions/auth-token"
        params = {}
        payload = {
            "sessionToken": sessionToken,
            "scopeUris": scopeUris,
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

@mcp.tool(description="Retrieve a list of server hardware resources, with optional filters and sorting.")
def get_server_hardware_list():
    try:
        url = f"{API_BASE_URL}/rest/server-hardware"
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

@mcp.tool(description="Add a rack-mount server for management by the appliance.")
def add_rack_mount_server(hostname: str = None, username: str = None, password: str = None, force: str = None, licensingIntent: str = None, configurationState: str = None, initialScopeUris: str = None):
    try:
        url = f"{API_BASE_URL}/rest/server-hardware"
        params = {}
        payload = {
            "hostname": hostname,
            "username": username,
            "password": password,
            "force": force,
            "licensingIntent": licensingIntent,
            "configurationState": configurationState,
            "initialScopeUris": initialScopeUris,
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

@mcp.tool(description="Retrieve firmware inventory across all servers, with optional filtering.")
def get_all_server_firmware_inventory():
    try:
        url = f"{API_BASE_URL}/rest/server-hardware/*/firmware"
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

@mcp.tool(description="Add multiple rack-mount servers for management by the appliance.")
def discover_rack_mount_servers(mpHostsAndRanges: str = None, username: str = None, password: str = None, licensingIntent: str = None, configurationState: str = None, initialScopeUris: str = None):
    try:
        url = f"{API_BASE_URL}/rest/server-hardware/discovery"
        params = {}
        payload = {
            "mpHostsAndRanges": mpHostsAndRanges,
            "username": username,
            "password": password,
            "licensingIntent": licensingIntent,
            "configurationState": configurationState,
            "initialScopeUris": initialScopeUris,
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

@mcp.tool(description="Check firmware compliance of a server with a selected firmware baseline.")
def check_server_firmware_compliance(firmwareBaselineId: str = None, serverUUID: str = None):
    try:
        url = f"{API_BASE_URL}/rest/server-hardware/firmware-compliance"
        params = {}
        payload = {
            "firmwareBaselineId": firmwareBaselineId,
            "serverUUID": serverUUID,
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

@mcp.tool(description="Retrieve the JSON schema definition for the server hardware resource.")
def get_server_hardware_schema():
    try:
        url = f"{API_BASE_URL}/rest/server-hardware/schema"
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

@mcp.tool(description="Retrieve a specific server hardware resource by its URI.")
def get_server_hardware_by_id(id: str):
    try:
        url = f"{API_BASE_URL}/rest/server-hardware/{id}"
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

@mcp.tool(description="Perform partial updates on a server hardware resource, such as changing UID light state or power state.")
def patch_server_hardware(id: str):
    try:
        url = f"{API_BASE_URL}/rest/server-hardware/{id}"
        params = {}
        payload = {}
        response = requests.patch(url, params=params, json=payload)
        response.raise_for_status()
        return response.json() if response.content else {"status": "success"}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Resource not found"}
        return {"error": f"API error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Remove a rack-server from management by the appliance.")
def remove_rack_server(id: str):
    try:
        url = f"{API_BASE_URL}/rest/server-hardware/{id}"
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

@mcp.tool(description="Retrieve advanced memory protection settings and status for a specific server.")
def get_server_advanced_memory_protection(id: str):
    try:
        url = f"{API_BASE_URL}/rest/server-hardware/{id}/advancedMemoryProtection"
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

@mcp.tool(description="Retrieve the list of BIOS/UEFI values currently set on the physical server.")
def get_server_bios_settings(id: str):
    try:
        url = f"{API_BASE_URL}/rest/server-hardware/{id}/bios"
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

@mcp.tool(description="Retrieve chassis resource information for a specific server.")
def get_server_chassis_info(id: str):
    try:
        url = f"{API_BASE_URL}/rest/server-hardware/{id}/chassis"
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

@mcp.tool(description="Retrieve information for all devices installed on a specific server.")
def get_server_devices(id: str):
    try:
        url = f"{API_BASE_URL}/rest/server-hardware/{id}/devices"
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

@mcp.tool(description="Retrieve environmental configuration settings for a specific server hardware resource.")
def get_server_environmental_configuration(id: str):
    try:
        url = f"{API_BASE_URL}/rest/server-hardware/{id}/environmentalConfiguration"
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

@mcp.tool(description="Set the calibrated maximum power for an unmanaged or unsupported server hardware resource.")
def update_server_calibrated_max_power(id: str, calibratedMaxPower: str = None):
    try:
        url = f"{API_BASE_URL}/rest/server-hardware/{id}/environmentalConfiguration"
        params = {}
        payload = {
            "calibratedMaxPower": calibratedMaxPower,
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

@mcp.tool(description="Retrieve the firmware inventory for a specific server hardware resource.")
def get_server_firmware_inventory_by_id(id: str):
    try:
        url = f"{API_BASE_URL}/rest/server-hardware/{id}/firmware"
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

@mcp.tool(description="Retrieve the firmware inventory subresource for a specific server.")
def get_server_firmware_inventory_subresource(id: str):
    try:
        url = f"{API_BASE_URL}/rest/server-hardware/{id}/firmwareInventory"
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
