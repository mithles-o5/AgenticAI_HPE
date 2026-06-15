import os
import requests
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("oneview")

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

@mcp.tool(description="Requests a session token for user authentication.")
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

@mcp.tool(description="Creates a session with a subset of user permissions enabled.")
def create_scoped_session_token(sessionID: str = None, enabledPermissions: str = None):
    try:
        url = f"{API_BASE_URL}/rest/login-sessions/auth-token"
        params = {}
        payload = {
            "sessionID": sessionID,
            "enabledPermissions": enabledPermissions,
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

@mcp.tool(description="Creates a client certificate for RabbitMQ.")
def create_rabbitmq_client_certificate(type: str = None, commonName: str = None, alternativeNames: str = None):
    try:
        url = f"{API_BASE_URL}/rest/certificates/client/rabbitmq"
        params = {}
        payload = {
            "type": type,
            "commonName": commonName,
            "alternativeNames": alternativeNames,
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

@mcp.tool(description="Downloads the RabbitMQ client certificate and private key.")
def download_rabbitmq_client_keypair():
    try:
        url = f"{API_BASE_URL}/rest/certificates/client/rabbitmq/keypair/default"
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

@mcp.tool(description="Downloads the internal root CA certificate filtered by type.")
def download_internal_ca_certificate():
    try:
        url = f"{API_BASE_URL}/rest/certificates/ca"
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

@mcp.tool(description="Revokes the RabbitMQ client CA certificate, triggering regeneration.")
def revoke_rabbitmq_ca_certificate():
    try:
        url = f"{API_BASE_URL}/rest/certificates/ca/rabbitmq_readonly"
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

@mcp.tool(description="Retrieves chassis information for a specific server hardware.")
def get_server_hardware_chassis(id: str):
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

@mcp.tool(description="Retrieves firmware inventory for a specific server hardware.")
def get_server_hardware_firmware_inventory(id: str):
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

@mcp.tool(description="Retrieves network adapter information for a specific server hardware.")
def get_server_hardware_network_adapters(id: str):
    try:
        url = f"{API_BASE_URL}/rest/server-hardware/{id}/networkAdapters"
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

@mcp.tool(description="Retrieves power supply information for a specific server hardware.")
def get_server_hardware_power_supplies(id: str):
    try:
        url = f"{API_BASE_URL}/rest/server-hardware/{id}/powerSupplies"
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

@mcp.tool(description="Retrieves processor information for a specific server hardware.")
def get_server_hardware_processors(id: str):
    try:
        url = f"{API_BASE_URL}/rest/server-hardware/{id}/processors"
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

@mcp.tool(description="Retrieves software inventory for a specific server hardware.")
def get_server_hardware_software_inventory(id: str):
    try:
        url = f"{API_BASE_URL}/rest/server-hardware/{id}/softwareInventory"
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

@mcp.tool(description="Retrieves thermal information (fans, temperatures) for a specific server hardware.")
def get_server_hardware_thermal_data(id: str):
    try:
        url = f"{API_BASE_URL}/rest/server-hardware/{id}/thermal"
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

@mcp.tool(description="Retrieves a specific chassis resource within a rack manager, including remote support URI.")
def get_rack_manager_chassis_by_uuid(id: str, uuid: str):
    try:
        url = f"{API_BASE_URL}/rest/rack-managers/{id}/chassis/{uuid}"
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

@mcp.tool(description="Creates multiple Ethernet network resources in bulk, with IPv6 and subnet options.")
def create_bulk_ethernet_networks(type: str = None, namePrefix: str = None, vlanIdRange: str = None, purpose: str = None, privateNetwork: str = None, connectionTemplateUri: str = None, ipv6SubnetUri: str = None, subnetUri: str = None, initialScopeUris: str = None, smartLink: str = None):
    try:
        url = f"{API_BASE_URL}/rest/ethernet-networks/bulk"
        params = {}
        payload = {
            "type": type,
            "namePrefix": namePrefix,
            "vlanIdRange": vlanIdRange,
            "purpose": purpose,
            "privateNetwork": privateNetwork,
            "connectionTemplateUri": connectionTemplateUri,
            "ipv6SubnetUri": ipv6SubnetUri,
            "subnetUri": subnetUri,
            "initialScopeUris": initialScopeUris,
            "smartLink": smartLink,
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

@mcp.tool(description="Updates a specific storage volume resource, with an optional query parameter to suppress device updates.")
def update_storage_volume(id: str, name: str = None, description: str = None, capacityBytes: str = None, provisioningType: str = None, isShareable: str = None):
    try:
        url = f"{API_BASE_URL}/rest/storage-volumes/{id}"
        params = {}
        payload = {
            "name": name,
            "description": description,
            "capacityBytes": capacityBytes,
            "provisioningType": provisioningType,
            "isShareable": isShareable,
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

@mcp.tool(description="Retrieves a collection of updates, including bundle generation information.")
def get_all_updates():
    try:
        url = f"{API_BASE_URL}/rest/updates"
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

@mcp.tool(description="Retrieves a specific update resource by ID, including bundle generation information.")
def get_update_by_id(id: str):
    try:
        url = f"{API_BASE_URL}/rest/updates/{id}"
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

@mcp.tool(description="Fetches a collection of rack managers managed by the appliance.")
def get_all_rack_managers():
    try:
        url = f"{API_BASE_URL}/rest/rack-managers"
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

@mcp.tool(description="Adds a new rack manager to the OneView appliance using provided credentials.")
def add_rack_manager(hostname: str = None, username: str = None, password: str = None, force: str = None, fwBaselineUri: str = None, fwExcludeNpars: str = None, fwReinstall: str = None, initialScopeUris: str = None, licensingIntent: str = None, name: str = None):
    try:
        url = f"{API_BASE_URL}/rest/rack-managers"
        params = {}
        payload = {
            "hostname": hostname,
            "username": username,
            "password": password,
            "force": force,
            "fwBaselineUri": fwBaselineUri,
            "fwExcludeNpars": fwExcludeNpars,
            "fwReinstall": fwReinstall,
            "initialScopeUris": initialScopeUris,
            "licensingIntent": licensingIntent,
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

@mcp.tool(description="Retrieves a collection of chassis resources from all rack managers.")
def get_all_rack_manager_chassis():
    try:
        url = f"{API_BASE_URL}/rest/rack-managers/chassis"
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

@mcp.tool(description="Retrieves a collection of manager resources from all rack managers.")
def get_all_rack_manager_managers():
    try:
        url = f"{API_BASE_URL}/rest/rack-managers/managers"
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

@mcp.tool(description="Retrieves a collection of partition resources from all rack managers.")
def get_all_rack_manager_partitions():
    try:
        url = f"{API_BASE_URL}/rest/rack-managers/partitions"
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

@mcp.tool(description="Retrieves a specific rack manager resource by its identifier.")
def get_rack_manager_by_id(id: str):
    try:
        url = f"{API_BASE_URL}/rest/rack-managers/{id}"
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

@mcp.tool(description="Refreshes the specified rack manager, optionally forcing the operation with credentials.")
def refresh_rack_manager(id: str):
    try:
        url = f"{API_BASE_URL}/rest/rack-managers/{id}"
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

@mcp.tool(description="Deletes the specified rack manager resource.")
def delete_rack_manager(id: str):
    try:
        url = f"{API_BASE_URL}/rest/rack-managers/{id}"
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

@mcp.tool(description="Retrieves a collection of chassis that are part of the specified rack manager.")
def get_rack_manager_chassis_collection(id: str):
    try:
        url = f"{API_BASE_URL}/rest/rack-managers/{id}/chassis"
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

@mcp.tool(description="Retrieves historical utilization data for the chassis collection of a specified rack manager.")
def get_rack_manager_chassis_utilization(id: str):
    try:
        url = f"{API_BASE_URL}/rest/rack-managers/{id}/chassis/utilization"
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

@mcp.tool(description="Retrieves the environmental configuration settings for a specific rack manager.")
def get_rack_manager_environmental_configuration(id: str):
    try:
        url = f"{API_BASE_URL}/rest/rack-managers/{id}/environmentalConfiguration"
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

@mcp.tool(description="Retrieves a collection of managers that are part of the specified rack manager.")
def get_rack_manager_managers_collection(id: str):
    try:
        url = f"{API_BASE_URL}/rest/rack-managers/{id}/managers"
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

@mcp.tool(description="Retrieves a specific manager resource that is managing the specified rack manager.")
def get_specific_rack_manager_manager(id: str, managerid: str):
    try:
        url = f"{API_BASE_URL}/rest/rack-managers/{id}/managers/{managerid}"
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

@mcp.tool(description="Retrieves a collection of partitions that are part of the specified rack manager.")
def get_rack_manager_partitions_collection(id: str):
    try:
        url = f"{API_BASE_URL}/rest/rack-managers/{id}/partitions"
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

@mcp.tool(description="Retrieves a specific partition resource within a given rack manager.")
def get_specific_rack_manager_partition(id: str, uuid: str):
    try:
        url = f"{API_BASE_URL}/rest/rack-managers/{id}/partitions/{uuid}"
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

@mcp.tool(description="Retrieves the associated remote support settings for a specific rack manager.")
def get_rack_manager_remote_support_settings(id: str):
    try:
        url = f"{API_BASE_URL}/rest/rack-managers/{id}/remoteSupportSettings"
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

@mcp.tool(description="Gets a list of server hardware resources, with optional sorting and filtering.")
def get_all_server_hardware():
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

@mcp.tool(description="Adds a rack-mount server for management by the appliance.")
def add_rack_mount_server(hostname: str = None, username: str = None, password: str = None, force: str = None, licensingIntent: str = None, configurationState: str = None, initialScopeUris: str = None, name: str = None):
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

@mcp.tool(description="Gets a list of firmware inventory across all servers, with filtering options.")
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

@mcp.tool(description="Adds multiple rack-mount servers or IP ranges for management by the appliance.")
def discover_and_add_multiple_servers(mpHostsAndRanges: str = None, username: str = None, password: str = None, licensingIntent: str = None, configurationState: str = None, initialScopeUris: str = None, force: str = None):
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
            "force": force,
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

@mcp.tool(description="Checks the firmware compliance of a server against a selected firmware baseline.")
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

@mcp.tool(description="Gets the JSON schema of the server hardware resource.")
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

@mcp.tool(description="Gets a specific server hardware resource by its ID.")
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


# To use these tools in another FastMCP server, you can import `mcp` from this file.
# Example: from mcp_integration import mcp
