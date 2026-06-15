import os
import requests
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Cloud")

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

@mcp.tool(description="Retun a list of user permissions.  The returned list of permissions will be based upon the supplied filter.  If no filter was supplied, all user permissions will be returned. It is also possible to request all resource type with certain permission type (ex. ALL.read)")
def get_access_controls():
    try:
        url = f"{API_BASE_URL}/api/v1/access-controls"
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

@mcp.tool(description="returns the audit events")
def AuditEventsGet():
    try:
        url = f"{API_BASE_URL}/api/v1/audit-events"
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

@mcp.tool(description="Get the list of host groups")
def HostGroupList():
    try:
        url = f"{API_BASE_URL}/api/v1/host-initiator-groups"
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

@mcp.tool(description="Create a host group with hosts having same protocol initiators")
def HostGroupCreate(comment: str = None, hostIds: str = None, hostsToCreate: str = None, name: str = None, userCreated: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/host-initiator-groups"
        params = {}
        payload = {
            "comment": comment,
            "hostIds": hostIds,
            "hostsToCreate": hostsToCreate,
            "name": name,
            "userCreated": userCreated,
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

@mcp.tool(description="Delete a host group by {hostGroupId}")
def HostGroupDelete(hostGroupId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/host-initiator-groups/{hostGroupId}"
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

@mcp.tool(description="Get the host group details by {hostGroupId}")
def HostGroupGetById(hostGroupId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/host-initiator-groups/{hostGroupId}"
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

@mcp.tool(description="Update host group details by {hostGroupId}. Hostgroup can be updated with hosts containing same protocol initiators")
def HostGroupUpdateById(hostGroupId: str, hostProximityValues: str = None, hostsToCreate: str = None, name: str = None, removedHosts: str = None, updatedHosts: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/host-initiator-groups/{hostGroupId}"
        params = {}
        payload = {
            "hostProximityValues": hostProximityValues,
            "hostsToCreate": hostsToCreate,
            "name": name,
            "removedHosts": removedHosts,
            "updatedHosts": updatedHosts,
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

@mcp.tool(description="Get details of a host group identified by {hostGroupId} across its associated systems")
def HostGroupMappedDevice(hostGroupId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/host-initiator-groups/{hostGroupId}/mappedDevices"
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

@mcp.tool(description="Get the list of host groups which have identical duplicates or are unique across different systems.")
def findBulkMergeCandidatesForHostGroups():
    try:
        url = f"{API_BASE_URL}/api/v1/host-initiator-groups/bulkmerge"
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

@mcp.tool(description="Bulk Merge hosts into user created host")
def BulkMergeHostGroup(items: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/host-initiator-groups/bulkmerge"
        params = {}
        payload = {
            "items": items,
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

@mcp.tool(description="Merge a host group")
def HostGroupMerge(hostGroupIds: str = None, name: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/host-initiator-groups/merge"
        params = {}
        payload = {
            "hostGroupIds": hostGroupIds,
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

@mcp.tool(description="Get the list of hosts")
def HostList():
    try:
        url = f"{API_BASE_URL}/api/v1/host-initiators"
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

@mcp.tool(description="Create a host with same protocol initiators")
def HostCreate(comment: str = None, contact: str = None, fqdn: str = None, hostGroupIds: str = None, initiatorIds: str = None, initiatorsToCreate: str = None, ipAddress: str = None, isVvolHost: str = None, location: str = None, model: str = None, name: str = None, operatingSystem: str = None, persona: str = None, protocol: str = None, subnet: str = None, userCreated: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/host-initiators"
        params = {}
        payload = {
            "comment": comment,
            "contact": contact,
            "fqdn": fqdn,
            "hostGroupIds": hostGroupIds,
            "initiatorIds": initiatorIds,
            "initiatorsToCreate": initiatorsToCreate,
            "ipAddress": ipAddress,
            "isVvolHost": isVvolHost,
            "location": location,
            "model": model,
            "name": name,
            "operatingSystem": operatingSystem,
            "persona": persona,
            "protocol": protocol,
            "subnet": subnet,
            "userCreated": userCreated,
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

@mcp.tool(description="Delete a host by {hostId}")
def HostDelete(hostId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/host-initiators/{hostId}"
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

@mcp.tool(description="Get the host details by {hostId}")
def HostGetById(hostId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/host-initiators/{hostId}"
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

@mcp.tool(description="Update host details by {hostId}. Host can only be updated with the same protocol initiators")
def HostUpdateById(hostId: str, initiatorsToCreate: str = None, name: str = None, updatedInitiators: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/host-initiators/{hostId}"
        params = {}
        payload = {
            "initiatorsToCreate": initiatorsToCreate,
            "name": name,
            "updatedInitiators": updatedInitiators,
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

@mcp.tool(description="Get Host CHAP details by {hostId}")
def GetHostChapById(hostId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/host-initiators/{hostId}/chap"
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

@mcp.tool(description="CHAP can be updated only on iSCSI host on HPE Alletra Storage MP B10000 10.4.0 or later and NVMe/TCP host on HPE Alletra Storage MP B10000 10.5.0 or later.")
def UpdateHostChapById(hostId: str, items: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/host-initiators/{hostId}/chap"
        params = {}
        payload = {
            "items": items,
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

@mcp.tool(description="CHAP key can be generated only on NVMe/TCP host on HPE Alletra Storage MP B10000 10.5.0 and above system OS versions.")
def GenerateChapKeyById(hostId: str, hmacNum: str = None, secret: str = None, system: str = None, type: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/host-initiators/{hostId}/chapkey"
        params = {}
        payload = {
            "hmacNum": hmacNum,
            "secret": secret,
            "system": system,
            "type": type,
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

@mcp.tool(description="Get details of a host identified by {hostId} across its associated systems")
def HostMappedDevice(hostId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/host-initiators/{hostId}/mappedDevices"
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

@mcp.tool(description="Get the volume performance history data associated with a host identified by {uid}")
def HostVolumePerformanceHistoryGet(hostId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/host-initiators/{hostId}/storage-performance-history"
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

@mcp.tool(description="Get details of volumes associated with a host identified by {uid}")
def HostVolumesGet(hostId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/host-initiators/{hostId}/volumes"
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

@mcp.tool(description="Get details volume/snapshot exported to host identified by {hostId} across its associated HPE Alletra Storage MP B10000 storage-systems")
def HostMappedVolSnaps(hostId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/host-initiators/{hostId}/volumes-snapshots"
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

@mcp.tool(description="Get the list of hosts which have identical duplicates or are unique across different systems.")
def findBulkMergeCandidatesForHosts():
    try:
        url = f"{API_BASE_URL}/api/v1/host-initiators/bulkmerge"
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

@mcp.tool(description="Bulk Merge hosts into user created host")
def BulkMergeHost(items: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/host-initiators/bulkmerge"
        params = {}
        payload = {
            "items": items,
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

@mcp.tool(description="Merge hosts into user created host")
def MergeHost(hostIds: str = None, name: str = None, operatingSystem: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/host-initiators/merge"
        params = {}
        payload = {
            "hostIds": hostIds,
            "name": name,
            "operatingSystem": operatingSystem,
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

@mcp.tool(description="Get the list of initiators")
def HostInitiatorList():
    try:
        url = f"{API_BASE_URL}/api/v1/initiators"
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

@mcp.tool(description="Create initiator")
def HostInitiatorCreate(address: str = None, driverVersion: str = None, firmwareVersion: str = None, hbaModel: str = None, hostSpeed: str = None, ipAddress: str = None, name: str = None, protocol: str = None, vendor: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/initiators"
        params = {}
        payload = {
            "address": address,
            "driverVersion": driverVersion,
            "firmwareVersion": firmwareVersion,
            "hbaModel": hbaModel,
            "hostSpeed": hostSpeed,
            "ipAddress": ipAddress,
            "name": name,
            "protocol": protocol,
            "vendor": vendor,
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

@mcp.tool(description="Delete initiator by {initiatorId}")
def HostInitiatorDelete(initiatorId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/initiators/{initiatorId}"
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

@mcp.tool(description="Get the initiator details by {initiatorId}")
def HostInitiatorGetById(initiatorId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/initiators/{initiatorId}"
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

@mcp.tool(description="Returns the active (state='CREATED') issues for the account, which are associated with the resource-types for which the user has access. The user should also have the permission to view issues.
Eg: if there are issues associated with 50 resources (of different resource-types) for a customer (obtained from the request header),
and the user (obtained from the request headers), who has correct permissions to view the issues but has acceess to only 20 of those resources (ie access to their resource types),
this API will return only the issues associated with those 20 resources. The grouped issues are places next to each other. The client will have to process them for any desired grouping
")
def ListIssues():
    try:
        url = f"{API_BASE_URL}/api/v1/issues"
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

@mcp.tool(description="Returns the active issue (state='CREATED') associated with the account (retrieved from the request headers) and with given Id")
def GetIssue(id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/issues/{id}"
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

@mcp.tool(description="Return resource types on which the user has a read permission.  The returned list will be based upon the supplied filter.  If no filter was provided, all resource types for which the user has a read permission on will be returned")
def get_resource_types():
    try:
        url = f"{API_BASE_URL}/api/v1/resource-types"
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

@mcp.tool(description="Get all storage systems")
def SystemsList():
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems"
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

@mcp.tool(description="Get storage system object identified by {id}")
def SystemGetById(id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/{id}"
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

@mcp.tool(description="Get all storage pools for a device {systemId}")
def StoragePoolsList(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/{systemId}/storage-pools"
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

@mcp.tool(description="Get details of storage pools identified by {id}")
def StoragePoolsGetById(systemId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/{systemId}/storage-pools/{id}"
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

@mcp.tool(description="Get all volumes for storage-pool identified by {id}")
def StoragePoolVolumesList(systemId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/{systemId}/storage-pools/{id}/volumes"
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

@mcp.tool(description="Get all volume sets for a systemId")
def VolumesetListForSystemBySystemId(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/{systemId}/volume-sets"
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

@mcp.tool(description="Get volume-set identified by id")
def VolumesetSystemGetById(systemId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/{systemId}/volume-sets/{id}"
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

@mcp.tool(description="Get details of volumes identified with {systemId}")
def VolumeListForSystemBySystemId(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/{systemId}/volumes"
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

@mcp.tool(description="Get all Primera / Alletra 9K storage systems")
def DeviceType1SystemsList():
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1"
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

@mcp.tool(description="Get Primera / Alletra 9K object identified by {id}")
def DeviceType1SystemGetById(id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{id}"
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

@mcp.tool(description="Locate system of Primera / Alletra 9K")
def SystemLocate(id: str, locateEnabled: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{id}"
        params = {}
        payload = {
            "locateEnabled": locateEnabled,
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

@mcp.tool(description="Get alert-contact details for a storage system Primera / Alletra 9K")
def DeviceType1AlertContactsList(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/alert-contacts"
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

@mcp.tool(description="Add Alert/Mail contact details")
def AlertContactsCreate(systemId: str, company: str = None, companyCode: str = None, country: str = None, fax: str = None, firstName: str = None, includeSvcAlerts: str = None, lastName: str = None, notificationSeverities: str = None, preferredLanguage: str = None, primaryEmail: str = None, primaryPhone: str = None, receiveEmail: str = None, receiveGrouped: str = None, secondaryEmail: str = None, secondaryPhone: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/alert-contacts"
        params = {}
        payload = {
            "company": company,
            "companyCode": companyCode,
            "country": country,
            "fax": fax,
            "firstName": firstName,
            "includeSvcAlerts": includeSvcAlerts,
            "lastName": lastName,
            "notificationSeverities": notificationSeverities,
            "preferredLanguage": preferredLanguage,
            "primaryEmail": primaryEmail,
            "primaryPhone": primaryPhone,
            "receiveEmail": receiveEmail,
            "receiveGrouped": receiveGrouped,
            "secondaryEmail": secondaryEmail,
            "secondaryPhone": secondaryPhone,
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

@mcp.tool(description="Delete Alert/Email contact of storage system Primera / Alletra 9K identified by {id}")
def AlertContactsDelete(systemId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/alert-contacts/{id}"
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

@mcp.tool(description="Get alert-contact details for a storage system Primera / Alletra 9K identified by {id}")
def DeviceType1AlertContactsGetById(systemId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/alert-contacts/{id}"
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

@mcp.tool(description="Edit Alert/Email contact details of storage system Primera / Alletra 9K identified by {id}")
def AlertContactsUpdate(systemId: str, id: str, company: str = None, companyCode: str = None, country: str = None, fax: str = None, firstName: str = None, includeSvcAlerts: str = None, lastName: str = None, notificationSeverities: str = None, preferredLanguage: str = None, primaryEmail: str = None, primaryPhone: str = None, receiveEmail: str = None, receiveGrouped: str = None, secondaryEmail: str = None, secondaryPhone: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/alert-contacts/{id}"
        params = {}
        payload = {
            "company": company,
            "companyCode": companyCode,
            "country": country,
            "fax": fax,
            "firstName": firstName,
            "includeSvcAlerts": includeSvcAlerts,
            "lastName": lastName,
            "notificationSeverities": notificationSeverities,
            "preferredLanguage": preferredLanguage,
            "primaryEmail": primaryEmail,
            "primaryPhone": primaryPhone,
            "receiveEmail": receiveEmail,
            "receiveGrouped": receiveGrouped,
            "secondaryEmail": secondaryEmail,
            "secondaryPhone": secondaryPhone,
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

@mcp.tool(description="Get Application Summary for a storage system Primera / Alletra 9K")
def DeviceType1ApplicationSummaryGet(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/application-summary"
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

@mcp.tool(description="Get all applicationset details for Primera / Alletra 9K")
def DeviceType1VolumeSetsList(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/applicationsets"
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

@mcp.tool(description="Create Application Set for a storage system Primera / Alletra 9K")
def DeviceType1VolumeSetsCreate(systemId: str, appSetBusinessUnit: str = None, appSetComments: str = None, appSetImportance: str = None, appSetName: str = None, appSetType: str = None, createAppSetQosConfigInput: str = None, customAppType: str = None, members: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/applicationsets"
        params = {}
        payload = {
            "appSetBusinessUnit": appSetBusinessUnit,
            "appSetComments": appSetComments,
            "appSetImportance": appSetImportance,
            "appSetName": appSetName,
            "appSetType": appSetType,
            "createAppSetQosConfigInput": createAppSetQosConfigInput,
            "customAppType": customAppType,
            "members": members,
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

@mcp.tool(description="Export applicationset identified by {appsetId} from Primera / Alletra 9K identified by {systemId}")
def DeviceType1VolumeSetExport(systemId: str, appsetId: str, hostGroupIds: str = None, proximity: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{appsetId}/export"
        params = {}
        payload = {
            "hostGroupIds": hostGroupIds,
            "proximity": proximity,
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

@mcp.tool(description="Get details of Primera / Alletra 9K replication partners identified by {systemId} and {appsetId}")
def DeviceType1GetReplicationPartnersByAppSetId(systemId: str, appsetId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{appsetId}/replication-partners"
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

@mcp.tool(description="Get volume details of replication partners identified by {appsetId} and {replicationPartnerId} for Primera / Alletra 9K")
def DeviceType1GetReplicationPartnerVolumesByAppSetId(systemId: str, appsetId: str, replicationPartnerId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{appsetId}/replication-partners/{replicationPartnerId}/volumes"
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

@mcp.tool(description="Remove Primera / Alletra 9K snapset in system identified by {snapsetId}")
def DeviceType1VolumeSetSnapshotDeleteById(systemId: str, appsetId: str, snapsetId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{appsetId}/snapsets/{snapsetId}"
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

@mcp.tool(description="Get details of snapset identified by {snapsetId} for Applicationset identified by {appsetId} for Primera / Alletra 9K")
def DeviceType1SnapsetsGetById(systemId: str, appsetId: str, snapsetId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{appsetId}/snapsets/{snapsetId}"
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

@mcp.tool(description="Unexport applicationset identified by {appsetId} from Primera / Alletra 9K identified by {systemId}")
def DeviceType1VolumeSetUnexport(systemId: str, appsetId: str, hostGroupIds: str = None, hostIds: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{appsetId}/un-export"
        params = {}
        payload = {
            "hostGroupIds": hostGroupIds,
            "hostIds": hostIds,
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

@mcp.tool(description="Get volumes for an applicationset identified by appsetUid")
def DeviceType1VolumeSetVolumesList(systemId: str, appsetId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{appsetId}/volumes"
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

@mcp.tool(description="Delete applicationset identified by {id} from Primera / Alletra 9K identified by {systemId}. Member volumes will not be deleted.")
def DeviceType1VolumeSetsDeleteById(systemId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}"
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

@mcp.tool(description="Get applicationset details for an applicationset identified by appsetUid")
def DeviceType1VolumeSetsGetById(systemId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}"
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

@mcp.tool(description="Edit applicationset identified by {id} from Primera / Alletra 9K identified by {systemId}")
def DeviceType1VolumeSetsEditById(systemId: str, id: str, addMembers: str = None, appSetBusinessUnit: str = None, appSetComments: str = None, appSetImportance: str = None, appSetName: str = None, appSetType: str = None, customAppType: str = None, editAppSetQosConfigInput: str = None, removeMembers: str = None, retainVolumeExportsOnRemoval: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}"
        params = {}
        payload = {
            "addMembers": addMembers,
            "appSetBusinessUnit": appSetBusinessUnit,
            "appSetComments": appSetComments,
            "appSetImportance": appSetImportance,
            "appSetName": appSetName,
            "appSetType": appSetType,
            "customAppType": customAppType,
            "editAppSetQosConfigInput": editAppSetQosConfigInput,
            "removeMembers": removeMembers,
            "retainVolumeExportsOnRemoval": retainVolumeExportsOnRemoval,
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

@mcp.tool(description="Get capacity details for an applicationset identified by appsetUid")
def DeviceType1VolumeSetCapacityStatisticsGetById(systemId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}/capacity-statistics"
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

@mcp.tool(description="Get the performance history data for the HPE Primera / Alletra 9K volume set identified by {id}, including the QOS configuration history and the top/bottom 5-10 volumes based on a metric or up to 10 selected volume's performance history on a storage system identified by {systemid}.")
def DeviceType1GetVolumeSetPerformanceHistory(systemId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}/performance"
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

@mcp.tool(description="Get details of protection policies configured on application set identified by {id} created on Primera / Alletra 9K identified by {systemId}")
def DeviceType1GetProtectionPolicies(systemId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}/protection-policies"
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

@mcp.tool(description="Add protection policy on application set identified by {id} for a storage system Primera / Alletra 9K identified by {systemId}")
def DeviceType1CreateProtectionPolicy(systemId: str, id: str, policy: str = None, protectionPolicyType: str = None, schedules: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}/protection-policies"
        params = {}
        payload = {
            "policy": policy,
            "protectionPolicyType": protectionPolicyType,
            "schedules": schedules,
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

@mcp.tool(description="Edit protection policy on application set identified by {id} for a storage system Primera / Alletra 9K identified by {systemId}")
def DeviceType1EditProtectionPolicies(systemId: str, id: str, createSchedules: str = None, modifySchedules: str = None, policy: str = None, protectionPolicyType: str = None, removeSchedules: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}/protection-policies"
        params = {}
        payload = {
            "createSchedules": createSchedules,
            "modifySchedules": modifySchedules,
            "policy": policy,
            "protectionPolicyType": protectionPolicyType,
            "removeSchedules": removeSchedules,
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

@mcp.tool(description="Remedies issues caused in protection policy configuration on application set identified by {id} for a storage system Primera / Alletra 9K identified by {systemId}")
def DeviceType1FixProtectionPolicy(systemId: str, id: str, policy: str = None, protectionPolicyType: str = None, schedules: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}/protection-policies/fix"
        params = {}
        payload = {
            "policy": policy,
            "protectionPolicyType": protectionPolicyType,
            "schedules": schedules,
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

@mcp.tool(description="Remove protection policy on application set identified by {id} for a storage system Primera / Alletra 9K identified by {systemId}")
def DeviceType1removeProtectionPolicies(systemId: str, id: str, policies: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}/protection-policies/remove"
        params = {}
        payload = {
            "policies": policies,
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

@mcp.tool(description="Get hosts and proximity details identified by application set {id} for Primera / Alletra 9K identified by {systemId}")
def DeviceType1GetProximitySettings(systemId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}/proximity-settings"
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

@mcp.tool(description="Change proximity settings of hosts where volume sets are exported identified by {id} and {systemId} from Primera / Alletra 9K")
def DeviceType1EditProximitySettings(systemId: str, id: str, hosts: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}/proximity-settings"
        params = {}
        payload = {
            "hosts": hosts,
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

@mcp.tool(description="Actions on volume set identified by {id} and {systemId} from Primera / Alletra 9K")
def DeviceType1actionOnVolumeSets(systemId: str, id: str, action: str = None, parameters: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}/remote-protection/actions"
        params = {}
        payload = {
            "action": action,
            "parameters": parameters,
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

@mcp.tool(description="Get snapshot details of volume sets identified by {id} for Primera / Alletra 9K")
def DeviceType1VolumeSetSnapshotsList(systemId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}/snapsets"
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

@mcp.tool(description="Create snapshot for application set identified by {id}")
def DeviceType1VolumeSetsSnapshotCreate(systemId: str, id: str, comment: str = None, expireSecs: str = None, readOnly: str = None, retainSecs: str = None, snapshotName: str = None, vvNamePattern: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}/snapsets"
        params = {}
        payload = {
            "comment": comment,
            "expireSecs": expireSecs,
            "readOnly": readOnly,
            "retainSecs": retainSecs,
            "snapshotName": snapshotName,
            "vvNamePattern": vvNamePattern,
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

@mcp.tool(description="Get supported protection types for application set identified by {id} on storage system Primera / Alletra 9K identified by {systemId}")
def DeviceType1getSupportedProtectionTypes(systemId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/applicationsets/{id}/supported-protection"
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

@mcp.tool(description="Get capacity trend data for a storage system Primera / Alletra 9K")
def DeviceType1SystemCapacityHistoryGet(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/capacity-history"
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

@mcp.tool(description="Get system capacity for a storage system Primera / Alletra 9K")
def DeviceType1SystemCapacitySummaryGet(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/capacity-summary"
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

@mcp.tool(description="Get array certificates by Primera / Alletra 9K")
def DeviceType1CertificatesList(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/certificates"
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

@mcp.tool(description="Create certificate on storage system Primera / Alletra 9K identified by {systemId}")
def PostCertificate(systemId: str, authorityChain: str = None, commonName: str = None, country: str = None, days: str = None, keyLength: str = None, locality: str = None, organization: str = None, organizationUnit: str = None, province: str = None, service: str = None, subjectAltName: str = None, type: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/certificates"
        params = {}
        payload = {
            "authorityChain": authorityChain,
            "commonName": commonName,
            "country": country,
            "days": days,
            "keyLength": keyLength,
            "locality": locality,
            "organization": organization,
            "organizationUnit": organizationUnit,
            "province": province,
            "service": service,
            "subjectAltName": subjectAltName,
            "type": type,
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

@mcp.tool(description="Get array certificates by Primera / Alletra 9K identified by {id}")
def DeviceType1CertificatesGetById(systemId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/certificates/{id}"
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

@mcp.tool(description="Import certificate identified by {id} on storage system Primera / Alletra 9K identified by {systemId}")
def PutCertificate(systemId: str, id: str, authorityChain: str = None, certificate: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/certificates/{id}"
        params = {}
        payload = {
            "authorityChain": authorityChain,
            "certificate": certificate,
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

@mcp.tool(description="Delete certificates from storage system Primera / Alletra 9K identified by {systemId}")
def RemoveCertificates(systemId: str, certificates: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/certificates/remove"
        params = {}
        payload = {
            "certificates": certificates,
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

@mcp.tool(description="Trigger a collection on the storage system Primera / Alletra 9K")
def DeviceType1SupportDataCollect(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/collect-support-data"
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

@mcp.tool(description="Get component performance statistics details for a storage system Primera / Alletra 9K idenfified by {systemId}")
def DeviceType1SystemComponentPerformanceStatisticsGet(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/component-performance-statistics"
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

@mcp.tool(description="Get details of Primera / Alletra 9K Enclosures")
def DeviceType1EnclosuresList(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/enclosures"
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

@mcp.tool(description="Get details of Primera / Alletra 9K disks identified by {cageId}")
def DeviceType1DisksList(systemId: str, cageId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/enclosures/{cageId}/disks"
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

@mcp.tool(description="Get details of Primera / Alletra 9K disk identified by {cageId} and {id}")
def DeviceType1DisksGetById(systemId: str, cageId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/enclosures/{cageId}/disks/{id}"
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

@mcp.tool(description="Get details of Primera / Alletra 9K Enclosure Card Ports identified by {enclosureId}")
def DeviceType1EnclosureCardPortsList(systemId: str, enclosureId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-card-ports"
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

@mcp.tool(description="Get details of Primera / Alletra 9K Enclosure Card Port identified by {enclosureId} and {id}")
def DeviceType1EnclosureCardPortsGetById(systemId: str, enclosureId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-card-ports/{id}"
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

@mcp.tool(description="Get details of Primera / Alletra 9K Enclosure Cards identified by {enclosureId}")
def DeviceType1EnclosureCardsList(systemId: str, enclosureId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-cards"
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

@mcp.tool(description="Get details of Primera / Alletra 9K Enclosure Card identified by {enclosureId} and {id}")
def DeviceType1EnclosureCardsGetById(systemId: str, enclosureId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-cards/{id}"
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

@mcp.tool(description="Locate IO Module of Primera / Alletra 9K identified by {id}. This API endpoint is deprecated.")
def EnclosureCardsLocateIOById(systemId: str, enclosureId: str, id: str, locate: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-cards/{id}"
        params = {}
        payload = {
            "locate": locate,
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

@mcp.tool(description="Get details of Primera / Alletra 9K Enclosure Disks identified by {enclosureId}")
def DeviceType1EnclosureDisksList(systemId: str, enclosureId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-disks"
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

@mcp.tool(description="Get details of Primera / Alletra 9K Enclosure Disk identified by {enclosureId} and {id}")
def DeviceType1EnclosureDisksGetById(systemId: str, enclosureId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-disks/{id}"
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

@mcp.tool(description="Get details of Primera / Alletra 9K Enclosure Expanders identified by {enclosureId}")
def DeviceType1EnclosureExpandersList(systemId: str, enclosureId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-expanders"
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

@mcp.tool(description="Get details of Primera / Alletra 9K Enclosure Expander identified by {enclosureId} and {id}")
def DeviceType1EnclosureExpandersGetById(systemId: str, enclosureId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-expanders/{id}"
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

@mcp.tool(description="Get details of Primera / Alletra 9K Enclosure Fans identified by {enclosureId}")
def DeviceType1EnclosureFansList(systemId: str, enclosureId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-fans"
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

@mcp.tool(description="Get details of Primera / Alletra 9K Enclosure Fan identified by {enclosureId} and {id}")
def DeviceType1EnclosureFansGetById(systemId: str, enclosureId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-fans/{id}"
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

@mcp.tool(description="Get details of Primera / Alletra 9K Enclosure Powers identified by {enclosureId}")
def DeviceType1EnclosurePowersList(systemId: str, enclosureId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-powers"
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

@mcp.tool(description="Get details of Primera / Alletra 9K Enclosure Power identified by {enclosureId} and {id}")
def DeviceType1EnclosurePowersGetById(systemId: str, enclosureId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-powers/{id}"
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

@mcp.tool(description="Locate PCM of Primera / Alletra 9K identified by {id}")
def EnclosurePowersLocatePCMById(systemId: str, enclosureId: str, id: str, locate: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-powers/{id}"
        params = {}
        payload = {
            "locate": locate,
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

@mcp.tool(description="Get details of Primera / Alletra 9K Enclosure Sleds identified by {enclosureId}")
def DeviceType1EnclosureSledsList(systemId: str, enclosureId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-sleds"
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

@mcp.tool(description="Get details of Primera / Alletra 9K Enclosure Sled identified by {enclosureId} and {id}")
def DeviceType1EnclosureSledsGetById(systemId: str, enclosureId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-sleds/{id}"
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

@mcp.tool(description="Locate drive of Primera / Alletra 9K identified by {id}")
def EnclosureSledsLocateDriveById(systemId: str, enclosureId: str, id: str, locate: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/enclosures/{enclosureId}/enclosure-sleds/{id}"
        params = {}
        payload = {
            "locate": locate,
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

@mcp.tool(description="Get details of Primera / Alletra 9K Enclosure identified by {id}")
def DeviceType1EnclosuresGetById(systemId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/enclosures/{id}"
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

@mcp.tool(description="Locate enclosure drive of Primera / Alletra 9K identified by {id}")
def EnclosuresLocateById(systemId: str, id: str, locate: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/enclosures/{id}"
        params = {}
        payload = {
            "locate": locate,
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

@mcp.tool(description="Edit details of Primera / Alletra 9K Enclosure identified by {id}")
def EnclosuresEditById(systemId: str, id: str, id: str = None, location: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/enclosures/{id}"
        params = {}
        payload = {
            "id": id,
            "location": location,
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

@mcp.tool(description="Encryption Backup Action on storage system Primera / Alletra 9K identified by {systemId}")
def DeviceType1backupActionOnEncryption(systemId: str, parameters: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/encryption/backup"
        params = {}
        payload = {
            "parameters": parameters,
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

@mcp.tool(description="Check EKM configuration on storage system Primera / Alletra 9K identified by {systemId}")
def DeviceType1checkEKMConfiguration(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/encryption/checkekm"
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

@mcp.tool(description="Encryption Enable Action on storage system Primera / Alletra 9K identified by {systemId}")
def DeviceType1enableActionOnEncryption(systemId: str, parameters: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/encryption/enable"
        params = {}
        payload = {
            "parameters": parameters,
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

@mcp.tool(description="Encryption Rekey Action on storage system Primera / Alletra 9K identified by {systemId}")
def DeviceType1rekeyActionOnEncryption(systemId: str, parameters: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/encryption/rekey"
        params = {}
        payload = {
            "parameters": parameters,
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

@mcp.tool(description="Encryption Restore Action on  storage system Primera / Alletra 9K identified by {systemId}")
def DeviceType1restoreActionOnEncryption(systemId: str, key: str = None, parameters: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/encryption/restore"
        params = {}
        payload = {
            "key": key,
            "parameters": parameters,
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

@mcp.tool(description="Set EKM configuration on storage system Primera / Alletra 9K identified by {systemId}")
def DeviceType1setEKMConfiguration(systemId: str, parameters: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/encryption/setekm"
        params = {}
        payload = {
            "parameters": parameters,
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

@mcp.tool(description="Set EKM configuration and Encryption Backup Action on storage system Primera / Alletra 9K identified by {systemId}")
def DeviceType1setekmbackupActionOnEncryption(systemId: str, parameters: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/encryption/setekm/backup"
        params = {}
        payload = {
            "parameters": parameters,
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

@mcp.tool(description="Get system level saturation details of system identified by {systemId}")
def Device1headroomUtilizationGet(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/headroom-utilization"
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

@mcp.tool(description="Get details of Primera / Alletra 9K Host Paths")
def DeviceType1GetAllHostPaths(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/host-paths"
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

@mcp.tool(description="Get details of Primera / Alletra 9K Host Path identified by {HostPathId}")
def DeviceType1GetHostPathsById(systemId: str, hostPathId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/host-paths/{hostPathId}"
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

@mcp.tool(description="Get details of Primera / Alletra 9K Host Sets")
def DeviceType1GetAllHostSets(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/host-sets"
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

@mcp.tool(description="Get details of Primera / Alletra 9K Host Set identified by {HostSetId}")
def DeviceType1GetHostSetsById(systemId: str, hostSetId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/host-sets/{hostSetId}"
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

@mcp.tool(description="Get details of Primera / Alletra 9K Hosts")
def DeviceType1GetAllHosts(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/hosts"
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

@mcp.tool(description="Get details of Primera / Alletra 9K Host identified by {HostId}")
def DeviceType1GetHostById(systemId: str, hostId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/hosts/{hostId}"
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

@mcp.tool(description="Get system level latency factors of system identified by {systemId}")
def Device1LatencyFactorsGet(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/insights/latencyfactors"
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

@mcp.tool(description="Delete SMTP/mail server settings")
def MailSettingsDelete(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/mail-settings"
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

@mcp.tool(description="Get the system's SMTP/Mail server settigs")
def DeviceType1MailSettingsGet(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/mail-settings"
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

@mcp.tool(description="Add SMTP/Mail server settigs")
def MailSettingsAssociate(systemId: str, authenticationRequired: str = None, mailHostDomain: str = None, mailHostServer: str = None, password: str = None, port: str = None, senderEmailId: str = None, username: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/mail-settings"
        params = {}
        payload = {
            "authenticationRequired": authenticationRequired,
            "mailHostDomain": mailHostDomain,
            "mailHostServer": mailHostServer,
            "password": password,
            "port": port,
            "senderEmailId": senderEmailId,
            "username": username,
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

@mcp.tool(description="Edit SMTP/Mail server settigs")
def MailSettingsUpdate(systemId: str, authenticationRequired: str = None, mailHostDomain: str = None, mailHostServer: str = None, password: str = None, port: str = None, senderEmailId: str = None, username: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/mail-settings"
        params = {}
        payload = {
            "authenticationRequired": authenticationRequired,
            "mailHostDomain": mailHostDomain,
            "mailHostServer": mailHostServer,
            "password": password,
            "port": port,
            "senderEmailId": senderEmailId,
            "username": username,
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

@mcp.tool(description="Get CIM Network-Service details for a storage system Primera / Alletra 9K")
def DeviceType1NetworkServiceCimGet(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/network-services/cim"
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

@mcp.tool(description="Edit CIM network service configuration")
def NetworkServiceCimUpdate(systemId: str, cim: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/network-services/cim"
        params = {}
        payload = {
            "cim": cim,
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

@mcp.tool(description="Get SNMP-Manager Network-Service details for a storage system Primera / Alletra 9K")
def DeviceType1NetworkServiceSnmpMgrList(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/network-services/snmp-mgr"
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

@mcp.tool(description="Add SNMP Manager settings")
def NetworkServiceSnmpMgrCreate(systemId: str, snmpConfig: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/network-services/snmp-mgr"
        params = {}
        payload = {
            "snmpConfig": snmpConfig,
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

@mcp.tool(description="Delete SNMP manager settings identified by {id}")
def NetworkServiceSnmpMgrDelete(systemId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/network-services/snmp-mgr/{id}"
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

@mcp.tool(description="Get a specific SNMP-Manager Network-Service details for a storage system Primera / Alletra 9K")
def DeviceType1NetworkServiceSnmpMgrGetById(systemId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/network-services/snmp-mgr/{id}"
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

@mcp.tool(description="Edit SNMP Manager settings for the specified Id")
def NetworkServiceSnmpMgrUpdate(systemId: str, id: str, managerIP: str = None, notify: str = None, port: str = None, retry: str = None, timeoutSecs: str = None, user: str = None, version: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/network-services/snmp-mgr/{id}"
        params = {}
        payload = {
            "managerIP": managerIP,
            "notify": notify,
            "port": port,
            "retry": retry,
            "timeoutSecs": timeoutSecs,
            "user": user,
            "version": version,
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

@mcp.tool(description="Get VASA Network-Service details for a storage system Primera / Alletra 9K")
def DeviceType1NetworkServiceVasaGet(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/network-services/vasa"
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

@mcp.tool(description="Enables, disable or reset vasa service on a storage system Primera / Alletra 9K")
def DeviceType1NetworkServiceVasaConfigure(systemId: str, vasaId: str, action: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/network-services/vasa/{vasaId}"
        params = {}
        payload = {
            "action": action,
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

@mcp.tool(description="Enables, disable and updates the cert management mode for vasa services on a storage system Primera / Alletra 9K")
def DeviceType1NetworkServiceConfigureVasaService(systemId: str, vasaId: str, certMgmt: str = None, vasaStateEnabled: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/network-services/vasa/{vasaId}/services"
        params = {}
        payload = {
            "certMgmt": certMgmt,
            "vasaStateEnabled": vasaStateEnabled,
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

@mcp.tool(description="Get Network-Settings details for a storage system Primera / Alletra 9K")
def DeviceType1NetworkSettingsGet(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/network-settings"
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

@mcp.tool(description="Post Network-Settings details for a storage system Primera / Alletra 9K")
def NetworkSettingsAssociate(systemId: str, dnsAddresses: str = None, ipv4Address: str = None, ipv4Gateway: str = None, ipv4SubnetMask: str = None, ipv6Address: str = None, ipv6Gateway: str = None, ipv6PrefixLen: str = None, proxyParams: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/network-settings"
        params = {}
        payload = {
            "dnsAddresses": dnsAddresses,
            "ipv4Address": ipv4Address,
            "ipv4Gateway": ipv4Gateway,
            "ipv4SubnetMask": ipv4SubnetMask,
            "ipv6Address": ipv6Address,
            "ipv6Gateway": ipv6Gateway,
            "ipv6PrefixLen": ipv6PrefixLen,
            "proxyParams": proxyParams,
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

@mcp.tool(description="Get details of Primera / Alletra 9K Nodes")
def DeviceType1NodesList(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/nodes"
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

@mcp.tool(description="Get details of Primera / Alletra 9K Node identified by {id}")
def DeviceType1NodesGetById(systemId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/nodes/{id}"
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

@mcp.tool(description="Locate node of Primera / Alletra 9K identified by {id}")
def NodesLocateById(systemId: str, id: str, locate: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/nodes/{id}"
        params = {}
        payload = {
            "locate": locate,
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

@mcp.tool(description="Get component performance statistics details of Primera / Alletra 9K node idenfified by {nodeId}")
def DeviceType1NodeComponentPerformanceStatisticsGet(systemId: str, nodeId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/component-performance-statistics"
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

@mcp.tool(description="Get details of Primera / Alletra 9K Node Cards identified by {nodeId}")
def DeviceType1NodeCardsList(systemId: str, nodeId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/node-cards"
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

@mcp.tool(description="Get details of Primera / Alletra 9K Node Card identified by {nodeId} and {id}")
def DeviceType1NodeCardsGetById(systemId: str, nodeId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/node-cards/{id}"
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

@mcp.tool(description="Locate Node Card of Primera / Alletra 9K identified by {nodeId} and {id}")
def NodeCardLocateById(systemId: str, nodeId: str, id: str, locate: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/node-cards/{id}"
        params = {}
        payload = {
            "locate": locate,
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

@mcp.tool(description="Get details of Primera / Alletra 9K Node Cpus identified by {nodeId}")
def DeviceType1NodeCpusList(systemId: str, nodeId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/node-cpus"
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

@mcp.tool(description="Get details of Primera / Alletra 9K Node Cpu identified by {nodeId} and {id}")
def DeviceType1NodeCpusGetById(systemId: str, nodeId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/node-cpus/{id}"
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

@mcp.tool(description="Get details of Primera / Alletra 9K Node Drives identified by {nodeId}")
def DeviceType1NodeDrivesList(systemId: str, nodeId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/node-drives"
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

@mcp.tool(description="Get details of Primera / Alletra 9K Node Drive identified by {nodeId} and {id}")
def DeviceType1NodeDrivesGetById(systemId: str, nodeId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/node-drives/{id}"
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

@mcp.tool(description="Get details of Primera / Alletra 9K Node Mcus identified by {nodeId}")
def DeviceType1NodeMcusList(systemId: str, nodeId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/node-mcus"
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

@mcp.tool(description="Get details of Primera / Alletra 9K Node Mcu identified by {nodeId} and {id}")
def DeviceType1NodeMcusGetById(systemId: str, nodeId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/node-mcus/{id}"
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

@mcp.tool(description="Get details of Primera / Alletra 9K Node Memories identified by {nodeId}")
def DeviceType1NodeMemsList(systemId: str, nodeId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/node-mems"
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

@mcp.tool(description="Get details of Primera / Alletra 9K Node Memory identified by {nodeId} and {id}")
def DeviceType1NodeMemsGetById(systemId: str, nodeId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/node-mems/{id}"
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

@mcp.tool(description="Get details of Primera / Alletra 9K Node Power Supplies identified by {nodeId}")
def DeviceType1NodePowersList(systemId: str, nodeId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/node-powers"
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

@mcp.tool(description="Get details of Primera / Alletra 9K Node Power Supply identified by {nodeId} and {id}")
def DeviceType1NodePowersGetById(systemId: str, nodeId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/node-powers/{id}"
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

@mcp.tool(description="Locate PCBM of Primera / Alletra 9K identified by {id}")
def NodePowersLocatePCMBById(systemId: str, nodeId: str, id: str, locate: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/node-powers/{id}"
        params = {}
        payload = {
            "locate": locate,
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

@mcp.tool(description="Get details of Primera / Alletra 9K Node Batteries identified by {nodeId}")
def DeviceType1NodeBatteriesList(systemId: str, nodeId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/nodes-batteries"
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

@mcp.tool(description="Get details of Primera / Alletra 9K Node Battery identified by {nodeId} and {id}")
def DeviceType1NodeBatteriesGetById(systemId: str, nodeId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/nodes-batteries/{id}"
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

@mcp.tool(description="Get service ports for nodes of all storage systems of Primera / Alletra 9K identified by {systemId} and {nodeId }")
def DeviceType1NodeServicePortsGetById(systemId: str, nodeId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/nodes/{nodeId}/service-ports"
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

@mcp.tool(description="Get service ports for nodes of all storage systems of Primera / Alletra 9K identified by {systemId}")
def DeviceType1NodeServicePortsList(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/nodes/service-ports"
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

@mcp.tool(description="Get performance trend data for a storage system Primera / Alletra 9K")
def DeviceType1SystemPerformanceHistoryGet(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/performance-history"
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

@mcp.tool(description="Get performance statistics for a storage system Primera / Alletra 9K")
def DeviceType1GetSystemPerformanceStatistics(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/performance-statistics"
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

@mcp.tool(description="Get details of performance metrics of Primera/ Alletra 9K physicalDrives on storage system identified by {systemid}")
def DeviceType1PhysicalDrivePerformanceHistoryGet(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/physicaldrives-performance"
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

@mcp.tool(description="Get details of Primera / Alletra 9K Ports")
def DeviceType1PortsList(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/ports"
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

@mcp.tool(description="Get details of performance metrics of Primera/ Alletra 9K host ports on storage system identified by {systemid}")
def DeviceType1PortsPerformanceHistoryGet(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/ports-performance"
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

@mcp.tool(description="Get details of Primera / Alletra 9K Port identified by {id}")
def DeviceType1PortsGetById(systemId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/ports/{id}"
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

@mcp.tool(description="Port enable disable identified by {id} from Primera / Alletra 9K identified by {systemId}")
def PortEnable(systemId: str, id: str, portEnable: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/ports/{id}"
        params = {}
        payload = {
            "portEnable": portEnable,
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

@mcp.tool(description="Clear the details of the ports identified by {id} from Primera / Alletra 9K identified by {systemId}")
def DeviceType1PortsClear(systemId: str, id: str, ipType: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/ports/{id}/clear"
        params = {}
        payload = {
            "ipType": ipType,
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

@mcp.tool(description="Edit iscsi ports identified by {id} from Primera / Alletra 9K identified by {systemId}")
def DeviceType1IscsiPortEdit(systemId: str, id: str, gatewayAddress: str = None, ipAddress: str = None, label: str = None, mtu: str = None, netMask: str = None, sendTargetGroupTag: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/ports/{id}/edit-iscsi"
        params = {}
        payload = {
            "gatewayAddress": gatewayAddress,
            "ipAddress": ipAddress,
            "label": label,
            "mtu": mtu,
            "netMask": netMask,
            "sendTargetGroupTag": sendTargetGroupTag,
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

@mcp.tool(description="Edit rcip ports identified by {id} from Primera / Alletra 9K identified by {systemId}")
def DeviceType1RcipPortEdit(systemId: str, id: str, gatewayAddress: str = None, gatewayAddressV6: str = None, ipAddress: str = None, ipAddressV6: str = None, label: str = None, mtu: str = None, netMask: str = None, netMaskV6: str = None, speedConfigured: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/ports/{id}/edit-rcip"
        params = {}
        payload = {
            "gatewayAddress": gatewayAddress,
            "gatewayAddressV6": gatewayAddressV6,
            "ipAddress": ipAddress,
            "ipAddressV6": ipAddressV6,
            "label": label,
            "mtu": mtu,
            "netMask": netMask,
            "netMaskV6": netMaskV6,
            "speedConfigured": speedConfigured,
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

@mcp.tool(description="Edit ports identified by {id} from Primera / Alletra 9K identified by {systemId}")
def DeviceType1FcPortEdit(systemId: str, id: str, configMode: str = None, connectionType: str = None, interuptCoalesce: str = None, label: str = None, speedConfigured: str = None, uniqueWWN: str = None, vcn: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/ports/{id}/fc"
        params = {}
        payload = {
            "configMode": configMode,
            "connectionType": connectionType,
            "interuptCoalesce": interuptCoalesce,
            "label": label,
            "speedConfigured": speedConfigured,
            "uniqueWWN": uniqueWWN,
            "vcn": vcn,
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

@mcp.tool(description="Initialize the details of the ports identified by {id} from Primera / Alletra 9K identified by {systemId}")
def initialisePorts(systemId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/ports/{id}/initialize"
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

@mcp.tool(description="Ping iscsi ports identified by {id} from Primera / Alletra 9K identified by {systemId}")
def DeviceType1IscsiPortPing(systemId: str, id: str, ipAddress: str = None, ipAddressv6: str = None, pingCount: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/ports/{id}/ping-iscsi"
        params = {}
        payload = {
            "ipAddress": ipAddress,
            "ipAddressv6": ipAddressv6,
            "pingCount": pingCount,
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

@mcp.tool(description="Ping rcip ports identified by {id} from Primera / Alletra 9K identified by {systemId}")
def DeviceType1RcipPortPing(systemId: str, id: str, PacketSize: str = None, WaitTime: str = None, ipAddress: str = None, ipAddressv6: str = None, pingCount: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/ports/{id}/ping-rcip"
        params = {}
        payload = {
            "PacketSize": PacketSize,
            "WaitTime": WaitTime,
            "ipAddress": ipAddress,
            "ipAddressv6": ipAddressv6,
            "pingCount": pingCount,
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

@mcp.tool(description="Get QoS policy data for a storage system Primera / Alletra 9K identified by {systemId}")
def DeviceType1QoSPolicyGetBySystemId(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/qos-policy"
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

@mcp.tool(description="Get details of performance metrics of Primera/ Alletra 9K remote copy links on storage system identified by {systemid}")
def DeviceType1RemoteCopyLinksPerformanceHistoryGet(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/remotecopylinks-performance"
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

@mcp.tool(description="Create a clone of a snapshot identified by {snapshotId} for Primera / Alletra 9K systems.")
def SnapshotCloneCreate(systemId: str, snapshotId: str, autoLun: str = None, destinationCpg: str = None, destinationSnapshotCpg: str = None, destinationVolume: str = None, hostGroupId: str = None, lun: str = None, priority: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/snapshots/{snapshotId}/clone"
        params = {}
        payload = {
            "autoLun": autoLun,
            "destinationCpg": destinationCpg,
            "destinationSnapshotCpg": destinationSnapshotCpg,
            "destinationVolume": destinationVolume,
            "hostGroupId": hostGroupId,
            "lun": lun,
            "priority": priority,
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

@mcp.tool(description="Export vlun for snapshot identified by {id} from Primera / Alletra 9K identified by {systemId}")
def DeviceType1VlunExportForSnapshot(systemId: str, snapshotId: str, LUN: str = None, autoLun: str = None, hostGroupIds: str = None, maxAutoLun: str = None, noVcn: str = None, override: str = None, position: str = None, proximity: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/snapshots/{snapshotId}/export"
        params = {}
        payload = {
            "LUN": LUN,
            "autoLun": autoLun,
            "hostGroupIds": hostGroupIds,
            "maxAutoLun": maxAutoLun,
            "noVcn": noVcn,
            "override": override,
            "position": position,
            "proximity": proximity,
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

@mcp.tool(description="Unexport vlun for snapshot identified by {id} from Primera / Alletra 9K identified by {systemId}")
def DeviceType1VlunUnexportForSnapshot(systemId: str, snapshotId: str, hostGroupIds: str = None, hostIds: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/snapshots/{snapshotId}/un-export"
        params = {}
        payload = {
            "hostGroupIds": hostGroupIds,
            "hostIds": hostIds,
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

@mcp.tool(description="Get details of vluns for Snapshot identified by {snapshotId} for Primera / Alletra 9K")
def DeviceType1GetSnapshotVlunsList(systemId: str, snapshotId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/snapshots/{snapshotId}/vluns"
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

@mcp.tool(description="Get details of vlun identified by {id} for Snapshot identified by {snapshotId} for Primera / Alletra 9K")
def DeviceType1GetSnapshotVlunsById(systemId: str, snapshotId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/snapshots/{snapshotId}/vluns/{id}"
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

@mcp.tool(description="Get all storage-pools details by Primera / Alletra 9K")
def DeviceType1StoragePoolList(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/storage-pools"
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

@mcp.tool(description="Get details of Primera / Alletra 9K storage-pool identified by {id}")
def DeviceType1StoragePoolGetById(systemId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/storage-pools/{id}"
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

@mcp.tool(description="Get all volumes for storage-pool identified by {uuid} of Primera / Alletra 9K")
def DeviceType1StoragePoolVolumeGetById(systemId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/storage-pools/{id}/volumes"
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

@mcp.tool(description="Get support settings for a storage system Primera / Alletra 9K")
def DeviceType1SupportSettingsGet(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/support-settings"
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

@mcp.tool(description="Add support settings for a storage system Primera / Alletra 9K")
def SupportSettingsAssociate(systemId: str, connectToHPE: str = None, deviceId: str = None, enterpriseServerURL: str = None, miniInsploreEnabled: str = None, rapForwarding: str = None, remoteAccess: str = None, remoteRequestAcknowledge: str = None, rtsEnabled: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/support-settings"
        params = {}
        payload = {
            "connectToHPE": connectToHPE,
            "deviceId": deviceId,
            "enterpriseServerURL": enterpriseServerURL,
            "miniInsploreEnabled": miniInsploreEnabled,
            "rapForwarding": rapForwarding,
            "remoteAccess": remoteAccess,
            "remoteRequestAcknowledge": remoteRequestAcknowledge,
            "rtsEnabled": rtsEnabled,
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

@mcp.tool(description="Edit support settings for a storage system Primera / Alletra 9K")
def SupportSettingsUpdate(systemId: str, connectToHPE: str = None, deviceId: str = None, enterpriseServerURL: str = None, miniInsploreEnabled: str = None, rapForwarding: str = None, remoteAccess: str = None, remoteRequestAcknowledge: str = None, rtsEnabled: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/support-settings"
        params = {}
        payload = {
            "connectToHPE": connectToHPE,
            "deviceId": deviceId,
            "enterpriseServerURL": enterpriseServerURL,
            "miniInsploreEnabled": miniInsploreEnabled,
            "rapForwarding": rapForwarding,
            "remoteAccess": remoteAccess,
            "remoteRequestAcknowledge": remoteRequestAcknowledge,
            "rtsEnabled": rtsEnabled,
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

@mcp.tool(description="Get the system settings configuration details")
def DeviceType1SystemSettingsList(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/system-settings"
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

@mcp.tool(description="Edit system settings configuration")
def SystemSettingsAssociate(systemId: str, authMode: str = None, dateTime: str = None, installationSites: str = None, name: str = None, ntpAddresses: str = None, remoteSyslogSettings: str = None, srinfo: str = None, supportContact: str = None, systemParameters: str = None, timezone: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/system-settings"
        params = {}
        payload = {
            "authMode": authMode,
            "dateTime": dateTime,
            "installationSites": installationSites,
            "name": name,
            "ntpAddresses": ntpAddresses,
            "remoteSyslogSettings": remoteSyslogSettings,
            "srinfo": srinfo,
            "supportContact": supportContact,
            "systemParameters": systemParameters,
            "timezone": timezone,
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

@mcp.tool(description="Edit system settings configuration")
def SystemSettingsUpdate(systemId: str, authMode: str = None, dateTime: str = None, installationSites: str = None, name: str = None, ntpAddresses: str = None, remoteSyslogSettings: str = None, srinfo: str = None, supportContact: str = None, systemParameters: str = None, timezone: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/system-settings"
        params = {}
        payload = {
            "authMode": authMode,
            "dateTime": dateTime,
            "installationSites": installationSites,
            "name": name,
            "ntpAddresses": ntpAddresses,
            "remoteSyslogSettings": remoteSyslogSettings,
            "srinfo": srinfo,
            "supportContact": supportContact,
            "systemParameters": systemParameters,
            "timezone": timezone,
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

@mcp.tool(description="Get Storage Container details for a storage system Primera / Alletra 9K")
def DeviceType1StorageContainerGet(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/system-settings/management-services/vvolscs"
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

@mcp.tool(description="Creates VMware storage container on storage system Primera / Alletra 9K identified by {systemId}")
def DeviceType1CreatevVolSC(systemId: str, comment: str = None, domain: str = None, hostIDs: str = None, hostSetIDs: str = None, keep: str = None, members: str = None, name: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/system-settings/management-services/vvolscs"
        params = {}
        payload = {
            "comment": comment,
            "domain": domain,
            "hostIDs": hostIDs,
            "hostSetIDs": hostSetIDs,
            "keep": keep,
            "members": members,
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

@mcp.tool(description="Delete storage container of storage system Primera / Alletra 9K identified by {id}")
def DeviceType1StorageContainerDeleteById(systemId: str, vvolscId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/system-settings/management-services/vvolscs/{vvolscId}"
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

@mcp.tool(description="Edit Storage container identified by {volumeId} from Primera / Alletra 9K")
def DeviceType1EditVolSC(systemId: str, vvolscId: str, comment: str = None, hostProximity: str = None, members: str = None, name: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/system-settings/management-services/vvolscs/{vvolscId}"
        params = {}
        payload = {
            "comment": comment,
            "hostProximity": hostProximity,
            "members": members,
            "name": name,
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

@mcp.tool(description="Attach host to Storage container identified by {vvolscId} from Primera / Alletra 9K")
def DeviceType1AttachDetachVolSC(systemId: str, vvolscId: str, action: str = None, hostIDs: str = None, hostSetIDs: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/system-settings/management-services/vvolscs/{vvolscId}/attach"
        params = {}
        payload = {
            "action": action,
            "hostIDs": hostIDs,
            "hostSetIDs": hostSetIDs,
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

@mcp.tool(description="Get quorum witness configuration details from storage system Primera / Alletra 9K identified by {systemId}")
def DeviceType1GetQuorumWitness(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/system-settings/quorum-witness"
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

@mcp.tool(description="Create quorum witness on storage system Primera / Alletra 9K identified by {systemId}")
def DeviceType1PostQuorumWitness(systemId: str, parameters: str = None, replicationPartnerSystemId: str = None, srcReplicationId: str = None, startQuorumWitness: str = None, targetReplicationId: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/system-settings/quorum-witness"
        params = {}
        payload = {
            "parameters": parameters,
            "replicationPartnerSystemId": replicationPartnerSystemId,
            "srcReplicationId": srcReplicationId,
            "startQuorumWitness": startQuorumWitness,
            "targetReplicationId": targetReplicationId,
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

@mcp.tool(description="Delete quorum witness identified by {replicationPartnerId} on storage system Primera / Alletra 9K identified by {systemId}")
def DeviceType1DeleteQuorumWitness(systemId: str, replicationPartnerId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/system-settings/quorum-witness/{replicationPartnerId}"
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

@mcp.tool(description="Get details of quorum witness configured on replication partner identified by {replicationPartnerId} on storage system Primera / Alletra 9K identified by {systemId}")
def DeviceType1GetQuorumWitnessWithId(systemId: str, replicationPartnerId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/system-settings/quorum-witness/{replicationPartnerId}"
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

@mcp.tool(description="Edit quorum witness identified by {replicationPartnerId} on storage system Primera / Alletra 9K identified by {systemId}")
def DeviceType1PutQuorumWitness(systemId: str, replicationPartnerId: str, replicationPartnerSystemId: str = None, startQuorumWitness: str = None, targetReplicationId: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/system-settings/quorum-witness/{replicationPartnerId}"
        params = {}
        payload = {
            "replicationPartnerSystemId": replicationPartnerSystemId,
            "startQuorumWitness": startQuorumWitness,
            "targetReplicationId": targetReplicationId,
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

@mcp.tool(description="Get details of replication partners on storage system Primera / Alletra 9K identified by {systemId}")
def DeviceType1GetReplicationPartners(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/system-settings/replication-partners"
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

@mcp.tool(description="Create replication partners on Primera / Alletra 9K identified by {systemId}")
def DeviceType1PostReplicationPartners(systemId: str, replicationPartners: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/system-settings/replication-partners"
        params = {}
        payload = {
            "replicationPartners": replicationPartners,
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

@mcp.tool(description="Get details of replication partner identified by {replicationPartnerId} on storage system Primera / Alletra 9K identified by {systemId}")
def DeviceType1GetReplicationPartnerWithId(systemId: str, replicationPartnerId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/system-settings/replication-partners/{replicationPartnerId}"
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

@mcp.tool(description="Edit replication partner identified by {replicationPartnerId} on Primera / Alletra 9K identified by {systemId}")
def DeviceType1PutReplicationPartner(systemId: str, replicationPartnerId: str, addRcLinks: str = None, removeRcLinks: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/system-settings/replication-partners/{replicationPartnerId}"
        params = {}
        payload = {
            "addRcLinks": addRcLinks,
            "removeRcLinks": removeRcLinks,
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

@mcp.tool(description="Delete replication partner from storage system Primera / Alletra 9K identified by {systemId}")
def DeviceType1PostRemoveReplicationPartners(systemId: str, replicationPartners: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/system-settings/replication-partners/remove"
        params = {}
        payload = {
            "replicationPartners": replicationPartners,
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

@mcp.tool(description="Get QoS performance trend data of Primera / Alletra 9K target identified by {targetName}")
def DeviceType1QoSPerformanceStatisticsGetByTargetName(systemId: str, targetName: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/targets/{targetName}/performance-history"
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

@mcp.tool(description="Get telemetry status for a storage system Primera / Alletra 9K")
def DeviceType1TelemetryGet(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/telemetry"
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

@mcp.tool(description="Get certificates trusted by Primera / Alletra 9K")
def DeviceType1TrustedCertificatesList(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/trust-certificates"
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

@mcp.tool(description="Add trusted certificates for storage system Primera / Alletra 9K identified by {systemId}")
def AddTrustedCertificates(systemId: str, action: str = None, parameters: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/trust-certificates"
        params = {}
        payload = {
            "action": action,
            "parameters": parameters,
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

@mcp.tool(description="Get certificates trusted by Primera / Alletra 9K identified by {id}")
def DeviceType1TrustedCertificatesGetById(systemId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/trust-certificates/{id}"
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

@mcp.tool(description="Delete trusted certificates from storage system Primera / Alletra 9K identified by {systemId}")
def RemoveTrustedCertificates(systemId: str, trustedCertificates: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/trust-certificates/remove"
        params = {}
        payload = {
            "trustedCertificates": trustedCertificates,
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

@mcp.tool(description="Get vcenter settings for a storage system Primera / Alletra 9K")
def DeviceType1VMManagerSettingsList(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/vm-manager-settings"
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

@mcp.tool(description="Add vCenter settings to storage system Primera / Alletra 9K")
def DeviceType1PostVCenterSettings(systemId: str, certChainPem: str = None, description: str = None, inetaddress: str = None, name: str = None, password: str = None, port: str = None, username: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/vm-manager-settings"
        params = {}
        payload = {
            "certChainPem": certChainPem,
            "description": description,
            "inetaddress": inetaddress,
            "name": name,
            "password": password,
            "port": port,
            "username": username,
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

@mcp.tool(description="Delete vcenter setting identified by {vcenterSettingId} on storage system Primera / Alletra 9K identified by {systemId}")
def DeviceType1DeleteVCenterSettings(systemId: str, vcenterSettingId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/vm-manager-settings/{vcenterSettingId}"
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

@mcp.tool(description="Get vcenter setting detail for a given vcenter setting of a storage system Primera / Alletra 9K")
def DeviceType1VMManagerSettingsGetById(systemId: str, vcenterSettingId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/vm-manager-settings/{vcenterSettingId}"
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

@mcp.tool(description="Edit vCenter setting identified by {vcenterSettingId} on Primera / Alletra 9K identified by {systemId}")
def DeviceType1PutVCenterSettings(systemId: str, vcenterSettingId: str, certChainPem: str = None, description: str = None, inetaddress: str = None, name: str = None, password: str = None, port: str = None, username: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/vm-manager-settings/{vcenterSettingId}"
        params = {}
        payload = {
            "certChainPem": certChainPem,
            "description": description,
            "inetaddress": inetaddress,
            "name": name,
            "password": password,
            "port": port,
            "username": username,
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

@mcp.tool(description="Get all volumes details for Primera / Alletra 9K")
def DeviceType1VolumesList(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/volumes"
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

@mcp.tool(description="Create volume for a storage system Primera / Alletra 9K")
def VolumeCreate(systemId: str, comments: str = None, count: str = None, dataReduction: str = None, name: str = None, sizeMib: str = None, snapCpg: str = None, snapshotAllocWarning: str = None, userAllocWarning: str = None, userCpg: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/volumes"
        params = {}
        payload = {
            "comments": comments,
            "count": count,
            "dataReduction": dataReduction,
            "name": name,
            "sizeMib": sizeMib,
            "snapCpg": snapCpg,
            "snapshotAllocWarning": snapshotAllocWarning,
            "userAllocWarning": userAllocWarning,
            "userCpg": userCpg,
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

@mcp.tool(description="Get performance history of Primera / Alletra 9K Volumes")
def DeviceType1GetVolumesPerformanceHistory(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/volumes-performance"
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

@mcp.tool(description="Remove volume identified by {volumeId} from Primera / Alletra 9K")
def VolumeDelete(systemId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/volumes/{id}"
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

@mcp.tool(description="Get details of Primera / Alletra 9K Volume identified by {id}")
def DeviceType1VolumeGetById(systemId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/volumes/{id}"
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

@mcp.tool(description="Edit volume identified by {volumeId} from Primera / Alletra 9K")
def VolumeEdit(systemId: str, id: str, conversionType: str = None, dataReduction: str = None, name: str = None, sizeMib: str = None, snapshotAllocWarning: str = None, snapshotCpgName: str = None, userAllocWarning: str = None, userCpgName: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/volumes/{id}"
        params = {}
        payload = {
            "conversionType": conversionType,
            "dataReduction": dataReduction,
            "name": name,
            "sizeMib": sizeMib,
            "snapshotAllocWarning": snapshotAllocWarning,
            "snapshotCpgName": snapshotCpgName,
            "userAllocWarning": userAllocWarning,
            "userCpgName": userCpgName,
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

@mcp.tool(description="Get volume capacity trend data of Primera / Alletra 9K Volume identified by {id}")
def DeviceType1VolumeCapacityHistoryGetById(systemId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/volumes/{id}/capacity-history"
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

@mcp.tool(description="Create a clone volume identified by {id} for Primera / Alletra 9K systems.")
def VolumeCloneCreate(systemId: str, id: str, destinationVolume: str = None, offlineClone: str = None, online: str = None, onlineClone: str = None, priority: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/volumes/{id}/clone"
        params = {}
        payload = {
            "destinationVolume": destinationVolume,
            "offlineClone": offlineClone,
            "online": online,
            "onlineClone": onlineClone,
            "priority": priority,
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

@mcp.tool(description="Export vlun for volume identified by {id} from Primera / Alletra 9K identified by {systemId}")
def DeviceType1VlunExport(systemId: str, id: str, LUN: str = None, autoLun: str = None, hostGroupIds: str = None, maxAutoLun: str = None, noVcn: str = None, override: str = None, position: str = None, proximity: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/volumes/{id}/export"
        params = {}
        payload = {
            "LUN": LUN,
            "autoLun": autoLun,
            "hostGroupIds": hostGroupIds,
            "maxAutoLun": maxAutoLun,
            "noVcn": noVcn,
            "override": override,
            "position": position,
            "proximity": proximity,
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

@mcp.tool(description="Get performance trend data of Primera / Alletra 9K Volume identified by {id}")
def DeviceType1VolumePerformanceHistoryGetById(systemId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/volumes/{id}/performance-history"
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

@mcp.tool(description="Get performance statistics of Primera / Alletra 9K Volume identified by {id}")
def DeviceType1VolumePerformanceStatisticsGetById(systemId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/volumes/{id}/performance-statistics"
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

@mcp.tool(description="Get snapshot details of volume identified by {id} for Primera / Alletra 9K")
def DeviceType1VolumeSnapshotsList(systemId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/volumes/{id}/snapshots"
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

@mcp.tool(description="Create snapshot for volumes identified by {id}")
def VolumeSnapshotCreate(systemId: str, id: str, comment: str = None, customName: str = None, expireSecs: str = None, namePattern: str = None, readOnly: str = None, retainSecs: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/volumes/{id}/snapshots"
        params = {}
        payload = {
            "comment": comment,
            "customName": customName,
            "expireSecs": expireSecs,
            "namePattern": namePattern,
            "readOnly": readOnly,
            "retainSecs": retainSecs,
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

@mcp.tool(description="Unexport vlun for volume identified by {id} from Primera / Alletra 9K identified by {systemId}")
def DeviceType1VlunUnexport(systemId: str, id: str, hostGroupIds: str = None, hostIds: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/volumes/{id}/un-export"
        params = {}
        payload = {
            "hostGroupIds": hostGroupIds,
            "hostIds": hostIds,
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

@mcp.tool(description="Get details of vluns for Volume identified by {volumeId} for Primera / Alletra 9K")
def DeviceType1VlunsList(systemId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/volumes/{id}/vluns"
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

@mcp.tool(description="Get the details of the clone volumes associated with a base volume identified by {volumeId} for Primera / Alletra 9K systems.")
def DeviceType1GetClones(systemId: str, volumeId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/volumes/{volumeId}/clones"
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

@mcp.tool(description="Promote a clone volume identified by {cloneId} of a volume identified by {volumeId} on storage system Primera / Alletra 9K identified by {systemId}")
def DeviceType1PromoteCloneVolume(systemId: str, volumeId: str, cloneId: str, priority: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/volumes/{volumeId}/clones/{cloneId}/promote"
        params = {}
        payload = {
            "priority": priority,
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

@mcp.tool(description="Resynchronize a clone volume identified by {cloneId} of a volume identified by {volumeId} on storage system Primera / Alletra 9K identified by {systemId}")
def DeviceType1ResyncCloneVolume(systemId: str, volumeId: str, cloneId: str, priority: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/volumes/{volumeId}/clones/{cloneId}/resync"
        params = {}
        payload = {
            "priority": priority,
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

@mcp.tool(description="Remove Primera / Alletra 9K snapshot in system identified by {snapshotId}")
def VolumeSnapshotGetById(systemId: str, volumeId: str, snapshotId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/volumes/{volumeId}/snapshots/{snapshotId}"
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

@mcp.tool(description="Get details of vlun identified by {id} for Volume identified by {volumeId} for Primera / Alletra 9K")
def DeviceType1SnapshotsGetById(systemId: str, volumeId: str, snapshotId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/volumes/{volumeId}/snapshots/{snapshotId}"
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

@mcp.tool(description="Promote a snapshot identified by {snapshotId} of a volume identified by {volumeId} on storage system Primera / Alletra 9K identified by {systemId}")
def DeviceType1PromoteSnapshot(systemId: str, volumeId: str, snapshotId: str, priority: str = None, target: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/volumes/{volumeId}/snapshots/{snapshotId}"
        params = {}
        payload = {
            "priority": priority,
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

@mcp.tool(description="Remove vlun idenfied by {id} form volume identified by {volumeId} from Primera / Alletra 9K")
def VlunsDelete(systemId: str, volumeId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/volumes/{volumeId}/vluns/{id}"
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

@mcp.tool(description="Get details of vlun identified by {id} for Volume identified by {volumeId} for Primera / Alletra 9K")
def DeviceType1VlunsGetById(systemId: str, volumeId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type1/{systemId}/volumes/{volumeId}/vluns/{id}"
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

@mcp.tool(description="Get all storage systems by Nimble / Alletra 6K")
def DeviceType2GetStorageSystem():
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2"
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

@mcp.tool(description="Get Nimble / Alletra 6K object identified by {systemId}")
def DeviceType2GetStorageSystemById(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}"
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

@mcp.tool(description="Edit settings of Nimble / Alletra 6K system identified by {systemId}")
def DeviceType2EditStorageSystemSettingsById(systemId: str, auto_switchover_enabled: str = None, autoclean_unmanaged_snapshots_enabled: str = None, autoclean_unmanaged_snapshots_ttl_unit: str = None, cc_mode_enabled: str = None, date: str = None, default_iscsi_target_scope: str = None, group_snapshot_ttl: str = None, group_target_name: str = None, max_lock_period: str = None, name: str = None, ntp_server: str = None, tdz_enabled: str = None, tdz_prefix: str = None, timezone: str = None, tlsv1_enabled: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}"
        params = {}
        payload = {
            "auto_switchover_enabled": auto_switchover_enabled,
            "autoclean_unmanaged_snapshots_enabled": autoclean_unmanaged_snapshots_enabled,
            "autoclean_unmanaged_snapshots_ttl_unit": autoclean_unmanaged_snapshots_ttl_unit,
            "cc_mode_enabled": cc_mode_enabled,
            "date": date,
            "default_iscsi_target_scope": default_iscsi_target_scope,
            "group_snapshot_ttl": group_snapshot_ttl,
            "group_target_name": group_target_name,
            "max_lock_period": max_lock_period,
            "name": name,
            "ntp_server": ntp_server,
            "tdz_enabled": tdz_enabled,
            "tdz_prefix": tdz_prefix,
            "timezone": timezone,
            "tlsv1_enabled": tlsv1_enabled,
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

@mcp.tool(description="Get all access-control-records details by Nimble / Alletra 6K")
def DeviceType2GetAllAccessControlRecords(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/access-control-records"
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

@mcp.tool(description="Create Nimble / Alletra 6K access control record in system identified by {systemId}")
def DeviceType2AccessControlRecordCreate(systemId: str, apply_to: str = None, chap_user_id: str = None, initiator_group_id: str = None, lun: str = None, pe_id: str = None, pe_ids: str = None, snap_id: str = None, systemUid: str = None, vol_id: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/access-control-records"
        params = {}
        payload = {
            "apply_to": apply_to,
            "chap_user_id": chap_user_id,
            "initiator_group_id": initiator_group_id,
            "lun": lun,
            "pe_id": pe_id,
            "pe_ids": pe_ids,
            "snap_id": snap_id,
            "systemUid": systemUid,
            "vol_id": vol_id,
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

@mcp.tool(description="Remove access-control-record identified by {accessControlRecordId} from Nimble / Alletra 6K")
def DeviceType2RemoveAccessControlRecordById(systemId: str, accessControlRecordId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/access-control-records/{accessControlRecordId}"
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

@mcp.tool(description="Get details of Nimble / Alletra 6K access-control-records identified by {accessControlRecordId}")
def DeviceType2GetAccessControlRecordById(systemId: str, accessControlRecordId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/access-control-records/{accessControlRecordId}"
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

@mcp.tool(description="Edit access-control-record identified by {accessControlRecordId} for Nimble / Alletra 6K")
def DeviceType2EditAccessControlRecordById(systemId: str, accessControlRecordId: str, apply_to: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/access-control-records/{accessControlRecordId}"
        params = {}
        payload = {
            "apply_to": apply_to,
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

@mcp.tool(description="Perform group merge with the specified group.")
def DeviceType2MergeGroups(systemId: str, force: str = None, skip_secondary_mgmt_ip: str = None, src_group_ip: str = None, src_group_name: str = None, src_passphrase: str = None, src_password: str = None, src_username: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/actions/merge"
        params = {}
        payload = {
            "force": force,
            "skip_secondary_mgmt_ip": skip_secondary_mgmt_ip,
            "src_group_ip": src_group_ip,
            "src_group_name": src_group_name,
            "src_passphrase": src_passphrase,
            "src_password": src_password,
            "src_username": src_username,
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

@mcp.tool(description="Get all alarms of Nimble / Alletra 6K")
def DeviceType2GetAlarms(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/alarms"
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

@mcp.tool(description="Get all alarms of Nimble / Alletra 6K identified by {alarmId}")
def DeviceType2GetAlarmsUsingAlarmId(systemId: str, alarmId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/alarms/{alarmId}"
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

@mcp.tool(description="Get all application servers details by Nimble / Alletra 6K")
def DeviceType2GetAllApplicationServers(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/application-servers"
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

@mcp.tool(description="Create Nimble / Alletra 6K application server in system identified by {systemId}")
def DeviceType2ApplicationServerCreate(systemId: str, description: str = None, hostname: str = None, metadata: str = None, name: str = None, password: str = None, port: str = None, server_type: str = None, username: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/application-servers"
        params = {}
        payload = {
            "description": description,
            "hostname": hostname,
            "metadata": metadata,
            "name": name,
            "password": password,
            "port": port,
            "server_type": server_type,
            "username": username,
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

@mcp.tool(description="Remove application server identified by {applicationServerId} from Nimble / Alletra 6K")
def DeviceType2RemoveApplicationServerById(systemId: str, applicationServerId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/application-servers/{applicationServerId}"
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

@mcp.tool(description="Get details of Nimble / Alletra 6K application server identified by {applicationServerId}")
def DeviceType2GetApplicationServerById(systemId: str, applicationServerId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/application-servers/{applicationServerId}"
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

@mcp.tool(description="Modify Nimble / Alletra 6K application server in system identified by {systemId}")
def DeviceType2ApplicationServerEdit(systemId: str, applicationServerId: str, description: str = None, hostname: str = None, metadata: str = None, name: str = None, port: str = None, server_type: str = None, username: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/application-servers/{applicationServerId}"
        params = {}
        payload = {
            "description": description,
            "hostname": hostname,
            "metadata": metadata,
            "name": name,
            "port": port,
            "server_type": server_type,
            "username": username,
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

@mcp.tool(description="Get Application Summary for Nimble / Alletra 6K")
def DeviceType2GetApplicationSummary(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/application-summary"
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

@mcp.tool(description="Get capacity stats of Application identified by {id} for a storage system Nimble / Alletra 6K")
def DeviceType2GetApplicationCapacityStatisticsById(systemId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/applications/{id}/capacity-stats"
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

@mcp.tool(description="Get capacity stats of Applications for a storage system Nimble / Alletra 6K")
def DeviceType2GetApplicationsCapacityStatistics(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/applications/capacity-stats"
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

@mcp.tool(description="Get all arrays details by Nimble / Alletra 6K")
def GetDeviceType2Arrays(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/arrays"
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

@mcp.tool(description="Create Nimble / Alletra 6K array identified by {systemId}")
def DeviceType2CreateArray(systemId: str, allow_lower_limits: str = None, create_pool: str = None, ctrlr_a_support_ip: str = None, ctrlr_b_support_ip: str = None, dedupe_disabled: str = None, name: str = None, nic_list: str = None, pool_description: str = None, pool_name: str = None, secondary_mgmt_ip: str = None, serial: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/arrays"
        params = {}
        payload = {
            "allow_lower_limits": allow_lower_limits,
            "create_pool": create_pool,
            "ctrlr_a_support_ip": ctrlr_a_support_ip,
            "ctrlr_b_support_ip": ctrlr_b_support_ip,
            "dedupe_disabled": dedupe_disabled,
            "name": name,
            "nic_list": nic_list,
            "pool_description": pool_description,
            "pool_name": pool_name,
            "secondary_mgmt_ip": secondary_mgmt_ip,
            "serial": serial,
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

@mcp.tool(description="Delete Nimble / Alletra 6K array identified by {arrayId}")
def DeviceType2DeleteArrayById(systemId: str, arrayId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/arrays/{arrayId}"
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

@mcp.tool(description="Get details of Nimble / Alletra 6K array identified by {arrayId}")
def GetDeviceType2ArrayById(systemId: str, arrayId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/arrays/{arrayId}"
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

@mcp.tool(description="Edit  details of Nimble / Alletra 6K array identified by {arrayId}")
def DeviceType2EditArrayById(systemId: str, arrayId: str, name: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/arrays/{arrayId}"
        params = {}
        payload = {
            "name": name,
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

@mcp.tool(description="Perform failover of Nimble / Alletra 6K array identified by {arrayId}")
def DeviceType2ArrayFailover(systemId: str, arrayId: str, force: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/arrays/{arrayId}/actions/failover"
        params = {}
        payload = {
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

@mcp.tool(description="Send auto support information of Nimble / Alletra 6K identified by {systemId}")
def DeviceType2SendAutoSupport(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/autosupport/actions/send"
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

@mcp.tool(description="Get capacity trend data for a storage system Nimble / Alletra 6K")
def DeviceType2GetStorageSystemCapacityHistory(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/capacity-history"
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

@mcp.tool(description="Get all controllers details by Nimble / Alletra 6K")
def DeviceType2GetAllControllers(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/controllers"
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

@mcp.tool(description="Get details of Nimble / Alletra 6K Controller identified by {controllerId}")
def DeviceType2GetControllerById(systemId: str, controllerId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/controllers/{controllerId}"
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

@mcp.tool(description="Perform halt of Nimble / Alletra 6K controller identified by {controllerId}")
def DeviceType2ControllerHalt(systemId: str, controllerId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/controllers/{controllerId}/actions/halt"
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

@mcp.tool(description="Get all disks details by Nimble / Alletra 6K")
def DeviceType2GetAllDisks(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/disks"
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

@mcp.tool(description="Get details of Nimble / Alletra 6K disk identified by {diskId}")
def DeviceType2GetDiskById(systemId: str, diskId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/disks/{diskId}"
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

@mcp.tool(description="Edit details of Nimble / Alletra 6K disk identified by {diskId}")
def DeviceType2DiskEdit(systemId: str, diskId: str, disk_op: str = None, force: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/disks/{diskId}"
        params = {}
        payload = {
            "disk_op": disk_op,
            "force": force,
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

@mcp.tool(description="Get all events of Nimble / Alletra 6K")
def DeviceType2GetEvents(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/events"
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

@mcp.tool(description="Get all events of Nimble / Alletra 6K indentified by {eventId}")
def DeviceType2GetEventsUsingEventId(systemId: str, eventId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/events/{eventId}"
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

@mcp.tool(description="Get details of Nimble / Alletra 6K external-key-manager")
def DeviceType2GetExternalKeyManager(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/external-key-manager"
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

@mcp.tool(description="Create external key manager for a Nimble / Alletra 6K storage system")
def DeviceType2CreateExternalKeyManager(systemId: str, description: str = None, hostname: str = None, name: str = None, password: str = None, port: str = None, protocol: str = None, username: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/external-key-manager"
        params = {}
        payload = {
            "description": description,
            "hostname": hostname,
            "name": name,
            "password": password,
            "port": port,
            "protocol": protocol,
            "username": username,
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

@mcp.tool(description="Delete Nimble / Alletra 6K external key manager identified by {externalKeyManagerId}. This API is deprecated, use Remove external key manager API for delete functionality.")
def DeviceType2DeleteExternalKeyManagerById(systemId: str, externalKeyManagerId: str, passphrase: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/external-key-manager/{externalKeyManagerId}"
        params = {}
        payload = {
            "passphrase": passphrase,
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

@mcp.tool(description="Get details of Nimble / Alletra 6K external-key-manager identified by {externalKeyManagerId}")
def DeviceType2GetExternalKeyManagerById(systemId: str, externalKeyManagerId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/external-key-manager/{externalKeyManagerId}"
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

@mcp.tool(description="Edit external key manager for a Nimble / Alletra 6K identified by {externalKeyManagerId}")
def DeviceType2EditExternalKeyManagerById(systemId: str, externalKeyManagerId: str, description: str = None, hostname: str = None, id: str = None, name: str = None, password: str = None, port: str = None, protocol: str = None, username: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/external-key-manager/{externalKeyManagerId}"
        params = {}
        payload = {
            "description": description,
            "hostname": hostname,
            "id": id,
            "name": name,
            "password": password,
            "port": port,
            "protocol": protocol,
            "username": username,
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

@mcp.tool(description="Migrate external key manager for a Nimble / Alletra 6K identified by {externalKeyManagerId}")
def DeviceType2MigrateExternalKeyManagerById(systemId: str, externalKeyManagerId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/external-key-manager/{externalKeyManagerId}/actions/migrate"
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

@mcp.tool(description="Remove Nimble / Alletra 6K external key manager identified by {externalKeyManagerId}")
def DeviceType2RemoveExternalKeyManagerById(systemId: str, externalKeyManagerId: str, passphrase: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/external-key-manager/{externalKeyManagerId}/actions/remove"
        params = {}
        payload = {
            "passphrase": passphrase,
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

@mcp.tool(description="Get all fibre channel configs details of Nimble / Alletra 6K")
def DeviceType2GetAllFibreChannelConfigs(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/fibre-channel-configs"
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

@mcp.tool(description="Get fibre channel configs details of Nimble / Alletra 6K identified by {fcConfigId}.")
def DeviceType2GetFibreChannelConfigById(systemId: str, fcConfigId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/fibre-channel-configs/{fcConfigId}"
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

@mcp.tool(description="Get details of all fibre channel interfaces of Nimble / Alletra 6K storage system identified by {systemId}")
def GetDeviceType2FibreChannelInterfaces(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/fibre-channel-interfaces"
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

@mcp.tool(description="Get all fibre channel sessions details of Nimble / Alletra 6K")
def DeviceType2GetAllFibreChannelSessions(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/fibre-channel-sessions"
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

@mcp.tool(description="Get fibre channel session details of Nimble / Alletra 6K identified by {fcSessionId}.")
def DeviceType2GetFibreChannelSessionById(systemId: str, fcSessionId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/fibre-channel-sessions/{fcSessionId}"
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

@mcp.tool(description="Get all folders details by Nimble / Alletra 6K")
def DeviceType2GetAllFolders(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/folders"
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

@mcp.tool(description="Create Nimble / Alletra 6K folder in system identified by {systemId}")
def DeviceType2FolderCreate(systemId: str, access_protocol: str = None, agent_type: str = None, appserver_id: str = None, description: str = None, hostInitiatorGroupIDs: str = None, hostInitiatorsIDs: str = None, inherited_vol_perfpol_id: str = None, limit_iops: str = None, limit_mbps: str = None, limit_size_bytes: str = None, name: str = None, overdraft_limit_pct: str = None, pool_id: str = None, provisioned_limit_size_bytes: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/folders"
        params = {}
        payload = {
            "access_protocol": access_protocol,
            "agent_type": agent_type,
            "appserver_id": appserver_id,
            "description": description,
            "hostInitiatorGroupIDs": hostInitiatorGroupIDs,
            "hostInitiatorsIDs": hostInitiatorsIDs,
            "inherited_vol_perfpol_id": inherited_vol_perfpol_id,
            "limit_iops": limit_iops,
            "limit_mbps": limit_mbps,
            "limit_size_bytes": limit_size_bytes,
            "name": name,
            "overdraft_limit_pct": overdraft_limit_pct,
            "pool_id": pool_id,
            "provisioned_limit_size_bytes": provisioned_limit_size_bytes,
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

@mcp.tool(description="Remove Nimble / Alletra 6K folder identified by {folderId}")
def DeviceType2RemoveFolderById(systemId: str, folderId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/folders/{folderId}"
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

@mcp.tool(description="Get details of Nimble / Alletra 6K Folders identified by {folderId}")
def DeviceType2GetFolderById(systemId: str, folderId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/folders/{folderId}"
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

@mcp.tool(description="Edit details of Nimble / Alletra 6K folder identified by {folderId}")
def DeviceType2FolderEdit(systemId: str, folderId: str, appserver_id: str = None, description: str = None, inherited_vol_perfpol_id: str = None, limit_iops: str = None, limit_mbps: str = None, limit_size_bytes: str = None, name: str = None, overdraft_limit_pct: str = None, provisioned_limit_size_bytes: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/folders/{folderId}"
        params = {}
        payload = {
            "appserver_id": appserver_id,
            "description": description,
            "inherited_vol_perfpol_id": inherited_vol_perfpol_id,
            "limit_iops": limit_iops,
            "limit_mbps": limit_mbps,
            "limit_size_bytes": limit_size_bytes,
            "name": name,
            "overdraft_limit_pct": overdraft_limit_pct,
            "provisioned_limit_size_bytes": provisioned_limit_size_bytes,
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

@mcp.tool(description="Attach hosts to Storage container identified by {folderId} from Nimble / Alletra 6K")
def DeviceType2AttachDetachVvolbyID(systemId: str, folderId: str, action: str = None, hostInitiatorGroupIDs: str = None, hostInitiatorsIDs: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/folders/{folderId}/attach"
        params = {}
        payload = {
            "action": action,
            "hostInitiatorGroupIDs": hostInitiatorGroupIDs,
            "hostInitiatorsIDs": hostInitiatorsIDs,
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

@mcp.tool(description="Get details of  Nimble / Alletra 6K health status")
def DeviceType2GetHealthStatus(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/health-status"
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

@mcp.tool(description="Get details of Nimble / Alletra 6K health status identified by {healthStatusId}")
def DeviceType2GetHealthStatusUsingHealthId(systemId: str, healthStatusId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/health-status/{healthStatusId}"
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

@mcp.tool(description="Get all nimble host initiator groups details by Nimble / Alletra 6K")
def DeviceType2GetAllHostInitiatorGroups(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/host-groups"
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

@mcp.tool(description="Create Nimble / Alletra 6K initiator group in system identified by {systemId}")
def DeviceType2HostInitiatorGroupCreate(systemId: str, access_protocol: str = None, app_uuid: str = None, description: str = None, fc_initiators: str = None, fc_tdz_ports: str = None, host_type: str = None, iscsi_initiators: str = None, metadata: str = None, name: str = None, target_subnets: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/host-groups"
        params = {}
        payload = {
            "access_protocol": access_protocol,
            "app_uuid": app_uuid,
            "description": description,
            "fc_initiators": fc_initiators,
            "fc_tdz_ports": fc_tdz_ports,
            "host_type": host_type,
            "iscsi_initiators": iscsi_initiators,
            "metadata": metadata,
            "name": name,
            "target_subnets": target_subnets,
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

@mcp.tool(description="Remove initiator-groups identified by {hostInitiatorGroupId} from Nimble / Alletra 6K")
def DeviceType2RemoveHostInitiatorGroupById(systemId: str, hostInitiatorGroupId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/host-groups/{hostInitiatorGroupId}"
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

@mcp.tool(description="Get details of Nimble / Alletra 6K Nimble Initiators identified by {hostInitiatorGroupId}")
def DeviceType2GetHostInitiatorGroupById(systemId: str, hostInitiatorGroupId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/host-groups/{hostInitiatorGroupId}"
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

@mcp.tool(description="Update initiator-groups identified by {hostInitiatorGroupId}")
def DeviceType2UpdateHostInitiatorGroupById(systemId: str, hostInitiatorGroupId: str, app_uuid: str = None, description: str = None, fc_initiators: str = None, fc_tdz_ports: str = None, host_type: str = None, iscsi_initiators: str = None, metadata: str = None, name: str = None, target_subnets: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/host-groups/{hostInitiatorGroupId}"
        params = {}
        payload = {
            "app_uuid": app_uuid,
            "description": description,
            "fc_initiators": fc_initiators,
            "fc_tdz_ports": fc_tdz_ports,
            "host_type": host_type,
            "iscsi_initiators": iscsi_initiators,
            "metadata": metadata,
            "name": name,
            "target_subnets": target_subnets,
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

@mcp.tool(description="Get all nimble initiators details by Nimble / Alletra 6K")
def DeviceType2GetAllInitiators(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/host-initiators"
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

@mcp.tool(description="Get all nimble initiators details by Nimble / Alletra 6K")
def DeviceType2InitiatorsCreate(systemId: str, access_protocol: str = None, alias: str = None, chapuser_id: str = None, initiator_group_id: str = None, ip_address: str = None, iqn: str = None, label: str = None, override_existing_alias: str = None, wwpn: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/host-initiators"
        params = {}
        payload = {
            "access_protocol": access_protocol,
            "alias": alias,
            "chapuser_id": chapuser_id,
            "initiator_group_id": initiator_group_id,
            "ip_address": ip_address,
            "iqn": iqn,
            "label": label,
            "override_existing_alias": override_existing_alias,
            "wwpn": wwpn,
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

@mcp.tool(description="Remove Nimble Initiator identified by {hostInitiatorId} from Nimble / Alletra 6K")
def DeviceType2RemoveInitiatorsById(systemId: str, hostInitiatorId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/host-initiators/{hostInitiatorId}"
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

@mcp.tool(description="Get details of Nimble / Alletra 6K Nimble Initiators identified by {hostInitiatorId}")
def DeviceType2GetInitiatorsById(systemId: str, hostInitiatorId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/host-initiators/{hostInitiatorId}"
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

@mcp.tool(description="Get details of Nimble / Alletra 6K local-key-manager")
def DeviceType2GetLocalKeyManager(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/local-key-manager"
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

@mcp.tool(description="Create local key manager for a Nimble / Alletra 6K storage system")
def DeviceType2CreateLocalKeyManager(systemId: str, passphrase: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/local-key-manager"
        params = {}
        payload = {
            "passphrase": passphrase,
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

@mcp.tool(description="Delete Nimble / Alletra 6K local key manager identified by {localKeyManagerId}")
def DeviceType2DeleteLocalKeyManagerById(systemId: str, localKeyManagerId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/local-key-manager/{localKeyManagerId}"
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

@mcp.tool(description="Get details of Nimble / Alletra 6K local-key-manager identified by {localKeyManagerId}")
def DeviceType2GetLocalKeyManagerById(systemId: str, localKeyManagerId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/local-key-manager/{localKeyManagerId}"
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

@mcp.tool(description="Edit local key manager for a Nimble / Alletra 6K identified by {localKeyManagerId}")
def DeviceType2EditLocalKeyManagerById(systemId: str, localKeyManagerId: str, active: str = None, new_passphrase: str = None, passphrase: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/local-key-manager/{localKeyManagerId}"
        params = {}
        payload = {
            "active": active,
            "new_passphrase": new_passphrase,
            "passphrase": passphrase,
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

@mcp.tool(description="Edit Nimble Mail Settings of Nimble / Alletra 6K")
def DeviceType2EditMailSettings(systemId: str, smtp_port: str = None, smtp_server: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/mail-settings"
        params = {}
        payload = {
            "smtp_port": smtp_port,
            "smtp_server": smtp_server,
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

@mcp.tool(description="Get all network interfaces details by Nimble / Alletra 6K")
def GetDeviceType2NetworkInterfaces(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/network-interfaces"
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

@mcp.tool(description="Get all network interfaces details by Nimble / Alletra 6K identified by {networkInterfaceId}")
def GetDeviceType2NetworkInterfaceById(systemId: str, networkInterfaceId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/network-interfaces/{networkInterfaceId}"
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

@mcp.tool(description="Get all network settings details by Nimble / Alletra 6K")
def DeviceType2GetAllNetworkSettings(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/network-settings"
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

@mcp.tool(description="Get details of Nimble / Alletra 6K network setting identified by {networkSettingId}")
def DeviceType2GetNetworkSettingById(systemId: str, networkSettingId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/network-settings/{networkSettingId}"
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

@mcp.tool(description="Edit Nimble / Alletra 6K network setting identified by {networkSettingId}")
def DeviceType2EditNetworkSettingById(systemId: str, networkSettingId: str, array_list: str = None, iscsi_automatic_connection_method: str = None, iscsi_connection_rebalancing: str = None, mgmt_ip: str = None, name: str = None, route_list: str = None, secondary_mgmt_ip: str = None, subnet_list: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/network-settings/{networkSettingId}"
        params = {}
        payload = {
            "array_list": array_list,
            "iscsi_automatic_connection_method": iscsi_automatic_connection_method,
            "iscsi_connection_rebalancing": iscsi_connection_rebalancing,
            "mgmt_ip": mgmt_ip,
            "name": name,
            "route_list": route_list,
            "secondary_mgmt_ip": secondary_mgmt_ip,
            "subnet_list": subnet_list,
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

@mcp.tool(description="Get performance trend data for a storage system Nimble / Alletra 6K")
def DeviceType2GetStorageSystemPerformanceHistory(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/performance-history"
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

@mcp.tool(description="Get all performance-policies details by Nimble / Alletra 6K")
def DeviceType2GetAllPerformancePolicies(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/performance-policies"
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

@mcp.tool(description="Create Nimble / Alletra 6K performance policy in a system identified by {systemId}")
def DeviceType2PerformancePolicyCreate(systemId: str, app_category: str = None, block_size: str = None, cache: str = None, cache_policy: str = None, compress: str = None, dedupe_enabled: str = None, description: str = None, name: str = None, space_policy: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/performance-policies"
        params = {}
        payload = {
            "app_category": app_category,
            "block_size": block_size,
            "cache": cache,
            "cache_policy": cache_policy,
            "compress": compress,
            "dedupe_enabled": dedupe_enabled,
            "description": description,
            "name": name,
            "space_policy": space_policy,
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

@mcp.tool(description="Remove performance-policies identified by {performancePolicyId} from Nimble / Alletra 6K")
def DeviceType2RemovePerfPolicyId(systemId: str, performancePolicyId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/performance-policies/{performancePolicyId}"
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

@mcp.tool(description="Get details of Nimble / Alletra 6K performance-policy identified by {performancePolicyId}")
def DeviceType2GetPerformancePolicyById(systemId: str, performancePolicyId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/performance-policies/{performancePolicyId}"
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

@mcp.tool(description="Edit details of Nimble / Alletra 6K performance policy identified by {performancePolicyId}")
def DeviceType2PerformancePolicyEdit(systemId: str, performancePolicyId: str, app_category: str = None, cache: str = None, cache_policy: str = None, compress: str = None, dedupe_enabled: str = None, description: str = None, name: str = None, space_policy: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/performance-policies/{performancePolicyId}"
        params = {}
        payload = {
            "app_category": app_category,
            "cache": cache,
            "cache_policy": cache_policy,
            "compress": compress,
            "dedupe_enabled": dedupe_enabled,
            "description": description,
            "name": name,
            "space_policy": space_policy,
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

@mcp.tool(description="Get performance history of Nimble / Alletra 6K Pools")
def DeviceType2GetPoolsPerformanceHistory(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/pools-performance"
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

@mcp.tool(description="Get all ports details of Nimble / Alletra 6K")
def DeviceType2GetAllPorts(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/ports"
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

@mcp.tool(description="Get details of Nimble / Alletra 6K Port identified by {portId}.")
def DeviceType2GetPortById(systemId: str, portId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/ports/{portId}"
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

@mcp.tool(description="Edit Nimble FC Port of Nimble / Alletra 6K")
def DeviceType2EditFCPort(systemId: str, portId: str, online: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/ports/{portId}"
        params = {}
        payload = {
            "online": online,
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

@mcp.tool(description="Get all protection-templates details by Nimble / Alletra 6K")
def DeviceType2GetAllProtectionTemplates(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/protection-templates"
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

@mcp.tool(description="Create protection template on Nimble / Alletra 6K in system identified by {systemId}")
def DeviceType2CreateProtectionTemplate(systemId: str, app_cluster_name: str = None, app_id: str = None, app_server: str = None, app_service_name: str = None, app_sync: str = None, description: str = None, name: str = None, schedules: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/protection-templates"
        params = {}
        payload = {
            "app_cluster_name": app_cluster_name,
            "app_id": app_id,
            "app_server": app_server,
            "app_service_name": app_service_name,
            "app_sync": app_sync,
            "description": description,
            "name": name,
            "schedules": schedules,
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

@mcp.tool(description="Get details of Nimble / Alletra 6K protection-templates identified by {protectionTemplateId}")
def DeviceType2GetProtectionTemplateById(systemId: str, protectionTemplateId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/protection-templates/{protectionTemplateId}"
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

@mcp.tool(description="Edit  details of Nimble / Alletra 6K Protection-templates identified by {protectionTemplateId}")
def DeviceType2EditProtectionTemplate(systemId: str, protectionTemplateId: str, addSchedules: str = None, app_cluster_name: str = None, app_id: str = None, app_server: str = None, app_service_name: str = None, app_sync: str = None, description: str = None, editSchedules: str = None, name: str = None, removeSchedules: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/protection-templates/{protectionTemplateId}"
        params = {}
        payload = {
            "addSchedules": addSchedules,
            "app_cluster_name": app_cluster_name,
            "app_id": app_id,
            "app_server": app_server,
            "app_service_name": app_service_name,
            "app_sync": app_sync,
            "description": description,
            "editSchedules": editSchedules,
            "name": name,
            "removeSchedules": removeSchedules,
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

@mcp.tool(description="Remove protection templates for Nimble / Alletra 6K")
def DeviceType2RemoveProtectionTemplate(systemId: str, protectionTemplates: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/protection-templates/remove"
        params = {}
        payload = {
            "protectionTemplates": protectionTemplates,
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

@mcp.tool(description="Create provisioning workflow for a Nimble / Alletra 6K storage system identified by {systemId}")
def DeviceType2ProvisioningWorklow(systemId: str, agent_type: str = None, app_uuid: str = None, appSetName: str = None, count: str = None, dedupe_enabled: str = None, downstreamPartner: str = None, downstreamPartnerId: str = None, encryption_cipher: str = None, folder_id: str = None, host_groups: str = None, limit: str = None, limit_iops: str = None, limit_mbps: str = None, name: str = None, perfpolicy: str = None, perfpolicy_id: str = None, pool_id: str = None, protectionPolicyId: str = None, protectionPolicySchedules: str = None, replicationStartTime: str = None, size: str = None, suffix: str = None, volColId: str = None, volColName: str = None, warn_level: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/provisioning"
        params = {}
        payload = {
            "agent_type": agent_type,
            "app_uuid": app_uuid,
            "appSetName": appSetName,
            "count": count,
            "dedupe_enabled": dedupe_enabled,
            "downstreamPartner": downstreamPartner,
            "downstreamPartnerId": downstreamPartnerId,
            "encryption_cipher": encryption_cipher,
            "folder_id": folder_id,
            "host_groups": host_groups,
            "limit": limit,
            "limit_iops": limit_iops,
            "limit_mbps": limit_mbps,
            "name": name,
            "perfpolicy": perfpolicy,
            "perfpolicy_id": perfpolicy_id,
            "pool_id": pool_id,
            "protectionPolicyId": protectionPolicyId,
            "protectionPolicySchedules": protectionPolicySchedules,
            "replicationStartTime": replicationStartTime,
            "size": size,
            "suffix": suffix,
            "volColId": volColId,
            "volColName": volColName,
            "warn_level": warn_level,
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

@mcp.tool(description="Provisioning review for a storage system Nimble / Alletra 6K")
def DeviceType2ProvisioningReview(systemId: str, host_groups: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/provisioning-review"
        params = {}
        payload = {
            "host_groups": host_groups,
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

@mcp.tool(description="Get all shelves details by Nimble / Alletra 6K")
def DeviceType2GetAllShelves(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/shelves"
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

@mcp.tool(description="Get details of Nimble / Alletra 6K Shelf identified by {shelfId}")
def DeviceType2GetShelfById(systemId: str, shelfId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/shelves/{shelfId}"
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

@mcp.tool(description="Locate chassis of Nimble / Alletra 6K shelf identified by {shelfId}")
def DeviceType2LocateShelfChassis(systemId: str, shelfId: str, cid: str = None, status: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/shelves/{shelfId}/actions/locate"
        params = {}
        payload = {
            "cid": cid,
            "status": status,
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

@mcp.tool(description="Activate shelves of a Nimble / Alletra 6K storage system identified by {systemId}")
def DeviceType2ActivateShelf(systemId: str, shelf_list: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/shelves/actions/activate"
        params = {}
        payload = {
            "shelf_list": shelf_list,
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

@mcp.tool(description="Perform action clone Nimble / Alletra 6K on a snapshot collection identified by {snapshotCollectionId} in system identified by {systemId}")
def DeviceType2CloneActionOnSnapshotCollections(systemId: str, snapshotCollectionId: str, clone_volumes: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/snapshot-collections/{snapshotCollectionId}/actions/clone"
        params = {}
        payload = {
            "clone_volumes": clone_volumes,
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

@mcp.tool(description="Edit Multiple Nimble / Alletra 6K snapshots in system identified by {systemId}")
def DeviceType2EditSnapshotById(systemId: str, snapshot_list: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/snapshots/actions/update"
        params = {}
        payload = {
            "snapshot_list": snapshot_list,
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

@mcp.tool(description="Get all pools details by Nimble / Alletra 6K")
def DeviceType2GetAllPoolDetails(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/storage-pools"
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

@mcp.tool(description="Create storage pool from Nimble / Alletra 6K  system identified by {systemId}")
def DeviceType2CreatePool(systemId: str, array_list: str = None, dedupe_all_volumes: str = None, description: str = None, name: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/storage-pools"
        params = {}
        payload = {
            "array_list": array_list,
            "dedupe_all_volumes": dedupe_all_volumes,
            "description": description,
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

@mcp.tool(description="Delete pool identified by {storagePoolId} from Nimble / Alletra 6K")
def DeviceType2RemovePoolById(systemId: str, storagePoolId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/storage-pools/{storagePoolId}"
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

@mcp.tool(description="Get details of Nimble / Alletra 6K pool identified by {storagePoolId}")
def DeviceType2GetPoolDetailById(systemId: str, storagePoolId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/storage-pools/{storagePoolId}"
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

@mcp.tool(description="Edit details of Nimble / Alletra 6K pool identified by {storagePoolId}")
def DeviceType2EditPoolDetailById(systemId: str, storagePoolId: str, array_list: str = None, dedupe_all_volumes: str = None, dedupe_capable: str = None, description: str = None, force: str = None, is_default: str = None, name: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/storage-pools/{storagePoolId}"
        params = {}
        payload = {
            "array_list": array_list,
            "dedupe_all_volumes": dedupe_all_volumes,
            "dedupe_capable": dedupe_capable,
            "description": description,
            "force": force,
            "is_default": is_default,
            "name": name,
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

@mcp.tool(description="Merge pool identified by {storagePoolId} from Nimble / Alletra 6K")
def DeviceType2MergePoolById(systemId: str, storagePoolId: str, force: str = None, target_pool_id: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/storage-pools/{storagePoolId}/actions/merge"
        params = {}
        payload = {
            "force": force,
            "target_pool_id": target_pool_id,
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

@mcp.tool(description="Get storage pool capacity trend data of Nimble / Alletra 6K storage pool identified by {storagePoolId}")
def DeviceType2GetPoolCapacityHistory(systemId: str, storagePoolId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/storage-pools/{storagePoolId}/capacity-history"
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

@mcp.tool(description="Get performance trend data of Nimble / Alletra 6K storage pool identified by {storagePoolId}")
def DeviceType2GetPoolPerformanceHistory(systemId: str, storagePoolId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/storage-pools/{storagePoolId}/performance-history"
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

@mcp.tool(description="Get performance statistics of Nimble / Alletra 6K storage pool identified by {storagePoolId}")
def DeviceType2GetPoolPerformanceStatistics(systemId: str, storagePoolId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/storage-pools/{storagePoolId}/performance-statistics"
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

@mcp.tool(description="Edit system settings of Nimble / Alletra 6K")
def DeviceType2EditSystemSettings(systemId: str, alert_settings: str = None, date_timezone_settings: str = None, dns_settings: str = None, encryption_config: str = None, isns_settings: str = None, name: str = None, proxy_settings: str = None, security_settings: str = None, smtp_settings: str = None, snmp_settings: str = None, support_settings: str = None, syslogd_settings: str = None, system_parameters: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/system-settings"
        params = {}
        payload = {
            "alert_settings": alert_settings,
            "date_timezone_settings": date_timezone_settings,
            "dns_settings": dns_settings,
            "encryption_config": encryption_config,
            "isns_settings": isns_settings,
            "name": name,
            "proxy_settings": proxy_settings,
            "security_settings": security_settings,
            "smtp_settings": smtp_settings,
            "snmp_settings": snmp_settings,
            "support_settings": support_settings,
            "syslogd_settings": syslogd_settings,
            "system_parameters": system_parameters,
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

@mcp.tool(description="Get all replication-partners details for Nimble / Alletra 6K")
def DeviceType2GetReplicationPartners(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/system-settings/replication-partners"
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

@mcp.tool(description="Create replication partner pair for Nimble / Alletra 6K")
def DeviceType2CreateReplicationPartners(systemId: str, replicationPartners: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/system-settings/replication-partners"
        params = {}
        payload = {
            "replicationPartners": replicationPartners,
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

@mcp.tool(description="Get details of Nimble / Alletra 6K replication-partner identified by {replicationpartnerId}")
def DeviceType2GetReplicationPartnersById(systemId: str, replicationpartnerId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/system-settings/replication-partners/{replicationpartnerId}"
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

@mcp.tool(description="Edit a replication partner for Nimble / Alletra 6K given by replicationpartnerId")
def DeviceType2EditReplicationPartnersById(systemId: str, replicationpartnerId: str, replicationPartners: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/system-settings/replication-partners/{replicationpartnerId}"
        params = {}
        payload = {
            "replicationPartners": replicationPartners,
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

@mcp.tool(description="Pause the replication pair of Nimble / Alletra 6K")
def DeviceType2PauseReplicationPartner(systemId: str, replicationPartners: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/system-settings/replication-partners/actions/pause"
        params = {}
        payload = {
            "replicationPartners": replicationPartners,
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

@mcp.tool(description="Resume the replication pair of Nimble / Alletra 6K")
def DeviceType2ResumeReplicationPartner(systemId: str, replicationPartners: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/system-settings/replication-partners/actions/resume"
        params = {}
        payload = {
            "replicationPartners": replicationPartners,
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

@mcp.tool(description="Test the replication partner pair of Nimble / Alletra 6K")
def DeviceType2TestReplicationConfiguration(systemId: str, replicationPartners: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/system-settings/replication-partners/actions/test"
        params = {}
        payload = {
            "replicationPartners": replicationPartners,
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

@mcp.tool(description="Remove list of replication partner for Nimble / Alletra 6K")
def DeviceType2RemoveReplicationPartner(systemId: str, replicationPartners: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/system-settings/replication-partners/remove"
        params = {}
        payload = {
            "replicationPartners": replicationPartners,
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

@mcp.tool(description="Get all witness configuration details by Nimble / Alletra 6K")
def DeviceType2GetWitnesses(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/system-settings/witnesses"
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

@mcp.tool(description="Create a new witness configuration Nimble / Alletra 6K")
def DeviceType2CreateWitness(systemId: str, host: str = None, password: str = None, port: str = None, username: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/system-settings/witnesses"
        params = {}
        payload = {
            "host": host,
            "password": password,
            "port": port,
            "username": username,
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

@mcp.tool(description="Remove witness identified by {witnessId} from Nimble / Alletra 6K")
def DeviceType2RemoveWitnessesById(systemId: str, witnessId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/system-settings/witnesses/{witnessId}"
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

@mcp.tool(description="Get details of Nimble / Alletra 6K witness configuration identified by {witnessId}")
def DeviceType2GetWitnessesById(systemId: str, witnessId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/system-settings/witnesses/{witnessId}"
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

@mcp.tool(description="Test and validate the witness configuration between the host identified by {witnessId} from Nimble / Alletra 6K identified by {systemId}")
def DeviceType2TestWitnessesById(systemId: str, witnessId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/system-settings/witnesses/{witnessId}/actions/test"
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

@mcp.tool(description="Get all uninitialized arrays details by Nimble / Alletra 6K")
def GetDeviceType2UninitializedArrays(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/uninitialized-arrays"
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

@mcp.tool(description="Get uninitialized arrays details by Nimble / Alletra 6K identified  by {uninitializedArrayId}")
def GetDeviceType2UninitializedArrayById(systemId: str, uninitializedArrayId: str, id: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/uninitialized-arrays/{uninitializedArrayId}"
        params = {}
        payload = {
            "id": id,
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

@mcp.tool(description="Get all volume-collections details by Nimble / Alletra 6K")
def DeviceType2GetAllVolumeCollections(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/volume-collections"
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

@mcp.tool(description="Create Nimble / Alletra 6K volume collection in system identified by {systemId}")
def DeviceType2VolumeCollectionCreate(systemId: str, agent_hostname: str = None, agent_username: str = None, app_cluster_name: str = None, app_id: str = None, app_server: str = None, app_service_name: str = None, app_sync: str = None, description: str = None, is_standalone_volcoll: str = None, metadata: str = None, name: str = None, prottmpl_id: str = None, replication_type: str = None, vcenter_hostname: str = None, vcenter_username: str = None, volume_list: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/volume-collections"
        params = {}
        payload = {
            "agent_hostname": agent_hostname,
            "agent_username": agent_username,
            "app_cluster_name": app_cluster_name,
            "app_id": app_id,
            "app_server": app_server,
            "app_service_name": app_service_name,
            "app_sync": app_sync,
            "description": description,
            "is_standalone_volcoll": is_standalone_volcoll,
            "metadata": metadata,
            "name": name,
            "prottmpl_id": prottmpl_id,
            "replication_type": replication_type,
            "vcenter_hostname": vcenter_hostname,
            "vcenter_username": vcenter_username,
            "volume_list": volume_list,
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

@mcp.tool(description="Remove Volume-collection identified by {volumeCollectionId} from Nimble / Alletra 6K")
def DeviceType2RemoveVolumeCollectionById(systemId: str, volumeCollectionId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/volume-collections/{volumeCollectionId}"
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

@mcp.tool(description="Get details of Nimble / Alletra 6K volume-collections identified by {volumeCollectionId}")
def DeviceType2GetVolumeCollectionById(systemId: str, volumeCollectionId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/volume-collections/{volumeCollectionId}"
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

@mcp.tool(description="Edit  details of Nimble / Alletra 6K Volume-collections identified by {volumeCollectionId}")
def DeviceType2EditVolumeCollectionById(systemId: str, volumeCollectionId: str, agent_hostname: str = None, agent_username: str = None, app_cluster_name: str = None, app_id: str = None, app_server: str = None, app_service_name: str = None, app_sync: str = None, description: str = None, name: str = None, vcenter_hostname: str = None, vcenter_username: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/volume-collections/{volumeCollectionId}"
        params = {}
        payload = {
            "agent_hostname": agent_hostname,
            "agent_username": agent_username,
            "app_cluster_name": app_cluster_name,
            "app_id": app_id,
            "app_server": app_server,
            "app_service_name": app_service_name,
            "app_sync": app_sync,
            "description": description,
            "name": name,
            "vcenter_hostname": vcenter_hostname,
            "vcenter_username": vcenter_username,
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

@mcp.tool(description="Perform abort handover action Nimble / Alletra 6K on a volume collection identified by {volumeCollectionId} in system identified by {systemId}")
def DeviceType2ActiononVolumeCollection(systemId: str, volumeCollectionId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/volume-collections/{volumeCollectionId}/actions/abort-handover"
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

@mcp.tool(description="Add volumes to Nimble / Alletra 6K volumes collection in system identified by {systemId")
def DeviceType2AddVolumesToVolumeCollections(systemId: str, volumeCollectionId: str, volume_ids: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/volume-collections/{volumeCollectionId}/actions/add-volumes"
        params = {}
        payload = {
            "volume_ids": volume_ids,
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

@mcp.tool(description="Perform demote action Nimble / Alletra 6K on a volume collection identified by {volumeCollectionId} in system identified by {systemId}")
def DeviceType2ActionOnVolumeCollectionId(systemId: str, volumeCollectionId: str, invoke_on_upstream_partner: str = None, replication_partner_id: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/volume-collections/{volumeCollectionId}/actions/demote"
        params = {}
        payload = {
            "invoke_on_upstream_partner": invoke_on_upstream_partner,
            "replication_partner_id": replication_partner_id,
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

@mcp.tool(description="Perform handover action Nimble / Alletra 6K on a volume collection identified by {volumeCollectionId} in system identified by {systemId}")
def DeviceType2ActionOnVolumeCollection(systemId: str, volumeCollectionId: str, invoke_on_upstream_partner: str = None, no_reverse: str = None, override_upstream_down: str = None, replication_partner_id: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/volume-collections/{volumeCollectionId}/actions/handover"
        params = {}
        payload = {
            "invoke_on_upstream_partner": invoke_on_upstream_partner,
            "no_reverse": no_reverse,
            "override_upstream_down": override_upstream_down,
            "replication_partner_id": replication_partner_id,
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

@mcp.tool(description="Perform promote action Nimble / Alletra 6K on a volume collection identified by {volumeCollectionId} in system identified by {systemId}")
def DeviceType2PromoteActionOnVolumeCollection(systemId: str, volumeCollectionId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/volume-collections/{volumeCollectionId}/actions/promote"
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

@mcp.tool(description="Remove volumes from Nimble / Alletra 6K volumes collection in system identified by {systemId}")
def DeviceType2RemoveVolumesFromVolumeCollection(systemId: str, volumeCollectionId: str, volume_ids: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/volume-collections/{volumeCollectionId}/actions/remove-volumes"
        params = {}
        payload = {
            "volume_ids": volume_ids,
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

@mcp.tool(description="Get all snapshot collections' details of Nimble / Alletra 6K Volume collection identified by {volumeCollectionId}")
def DeviceType2GetSnapshotsByVolumeCollectionId(systemId: str, volumeCollectionId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/volume-collections/{volumeCollectionId}/snapshot-collections"
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

@mcp.tool(description="Create Nimble / Alletra 6K snapshot collection in system identified by {systemId}")
def DeviceType2CreateSnapshotCollections(systemId: str, volumeCollectionId: str, agent_type: str = None, allow_writes: str = None, description: str = None, disable_appsync: str = None, invoke_on_upstream_partner: str = None, is_external_trigger: str = None, lock_period: str = None, metadata: str = None, name: str = None, replicate: str = None, replicate_to: str = None, skip_db_consistency_check: str = None, snap_verify: str = None, start_online: str = None, vol_snap_attr_list: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/volume-collections/{volumeCollectionId}/snapshot-collections"
        params = {}
        payload = {
            "agent_type": agent_type,
            "allow_writes": allow_writes,
            "description": description,
            "disable_appsync": disable_appsync,
            "invoke_on_upstream_partner": invoke_on_upstream_partner,
            "is_external_trigger": is_external_trigger,
            "lock_period": lock_period,
            "metadata": metadata,
            "name": name,
            "replicate": replicate,
            "replicate_to": replicate_to,
            "skip_db_consistency_check": skip_db_consistency_check,
            "snap_verify": snap_verify,
            "start_online": start_online,
            "vol_snap_attr_list": vol_snap_attr_list,
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

@mcp.tool(description="Get details of snapshot collection of Nimble / Alletra 6K Volume collection identified by {volumeCollectionId} by {snapshotId}")
def DeviceType2GetSnapshotCollectionsById(systemId: str, volumeCollectionId: str, snapshotCollectionId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/volume-collections/{volumeCollectionId}/snapshot-collections/{snapshotCollectionId}"
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

@mcp.tool(description="Remove multiple snapshot collections identified by {volumeCollectionId} from Nimble / Alletra 6K")
def DeviceType2RemoveSnapShotCollection(systemId: str, volumeCollectionId: str, force: str = None, snapshot_collections: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/volume-collections/{volumeCollectionId}/snapshot-collections/remove"
        params = {}
        payload = {
            "force": force,
            "snapshot_collections": snapshot_collections,
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

@mcp.tool(description="Perform offline/online action on  snapshot collections of Nimble / Alletra 6K and associated with volume collection {volumeCollectionId}  in the system identified by {systemId}")
def DeviceType2ActionOnSnapshotCollection(systemId: str, volumeCollectionId: str, online: str = None, snapshot_collection_ids: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/volume-collections/{volumeCollectionId}/snapshot-collections/update"
        params = {}
        payload = {
            "online": online,
            "snapshot_collection_ids": snapshot_collection_ids,
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

@mcp.tool(description="Get all volumes details for Nimble / Alletra 6K")
def DeviceType2GetAllVolumes(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/volumes"
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

@mcp.tool(description="Create Nimble / Alletra 6K volume in system identified by {systemId}")
def DeviceType2VolumesCreate(systemId: str, agent_type: str = None, app_uuid: str = None, base_snap_id: str = None, block_size: str = None, cache_pinned: str = None, clone: str = None, dedupe_enabled: str = None, description: str = None, dest_pool_id: str = None, encryption_cipher: str = None, folder_id: str = None, limit: str = None, limit_iops: str = None, limit_mbps: str = None, metadata: str = None, multi_initiator: str = None, name: str = None, online: str = None, owned_by_group_id: str = None, perfpolicy_id: str = None, pool_id: str = None, read_only: str = None, reserve: str = None, size: str = None, snap_reserve: str = None, snap_warn_level: str = None, suffix: str = None, warn_level: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/volumes"
        params = {}
        payload = {
            "agent_type": agent_type,
            "app_uuid": app_uuid,
            "base_snap_id": base_snap_id,
            "block_size": block_size,
            "cache_pinned": cache_pinned,
            "clone": clone,
            "dedupe_enabled": dedupe_enabled,
            "description": description,
            "dest_pool_id": dest_pool_id,
            "encryption_cipher": encryption_cipher,
            "folder_id": folder_id,
            "limit": limit,
            "limit_iops": limit_iops,
            "limit_mbps": limit_mbps,
            "metadata": metadata,
            "multi_initiator": multi_initiator,
            "name": name,
            "online": online,
            "owned_by_group_id": owned_by_group_id,
            "perfpolicy_id": perfpolicy_id,
            "pool_id": pool_id,
            "read_only": read_only,
            "reserve": reserve,
            "size": size,
            "snap_reserve": snap_reserve,
            "snap_warn_level": snap_warn_level,
            "suffix": suffix,
            "warn_level": warn_level,
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

@mcp.tool(description="Get performance history of Nimble / Alletra 6K Volumes")
def DeviceType2GetVolumesPerformanceHistory(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/volumes-performance"
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

@mcp.tool(description="Remove volume identified by {volumeId} from Nimble / Alletra 6K")
def DeviceType2RemoveVolumeById(systemId: str, volumeId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/volumes/{volumeId}"
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

@mcp.tool(description="Get details of Nimble / Alletra 6K Volume identified by {volumeId}")
def DeviceType2GetVolumeById(systemId: str, volumeId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/volumes/{volumeId}"
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

@mcp.tool(description="Edit  details of Nimble / Alletra 6K Volume identified by {volumeId}")
def DeviceType2EditVolumeById(systemId: str, volumeId: str, app_uuid: str = None, caching_enabled: str = None, dedupe_enabled: str = None, description: str = None, folder_id: str = None, force: str = None, limit: str = None, limit_iops: str = None, limit_mbps: str = None, name: str = None, online: str = None, owned_by_group_id: str = None, perfpolicy_id: str = None, size: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/volumes/{volumeId}"
        params = {}
        payload = {
            "app_uuid": app_uuid,
            "caching_enabled": caching_enabled,
            "dedupe_enabled": dedupe_enabled,
            "description": description,
            "folder_id": folder_id,
            "force": force,
            "limit": limit,
            "limit_iops": limit_iops,
            "limit_mbps": limit_mbps,
            "name": name,
            "online": online,
            "owned_by_group_id": owned_by_group_id,
            "perfpolicy_id": perfpolicy_id,
            "size": size,
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

@mcp.tool(description="Move Nimble / Alletra 6K volume identified by {volumeId} to another pool.")
def DeviceType2MoveVolume(systemId: str, volumeId: str, dest_pool_id: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/volumes/{volumeId}/actions/move"
        params = {}
        payload = {
            "dest_pool_id": dest_pool_id,
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

@mcp.tool(description="Restore Nimble / Alletra 6K volume identified by {volumeId} from a previous snapshot.")
def DeviceType2RestoreVolumeById(systemId: str, volumeId: str, base_snap_id: str = None, enable_vol_offline: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/volumes/{volumeId}/actions/restore"
        params = {}
        payload = {
            "base_snap_id": base_snap_id,
            "enable_vol_offline": enable_vol_offline,
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

@mcp.tool(description="Get volume capacity trend data of Nimble / Alletra 6K Volume identified by {volumeId}")
def DeviceType2GetVolumeCapacityHistory(systemId: str, volumeId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/volumes/{volumeId}/capacity-history"
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

@mcp.tool(description="Create Nimble / Alletra 6K clone volume identified by {volumeId}.")
def DeviceType2CloneVolumeById(systemId: str, volumeId: str, clone_volume_name: str = None, host_group_id: str = None, lun: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/volumes/{volumeId}/clone"
        params = {}
        payload = {
            "clone_volume_name": clone_volume_name,
            "host_group_id": host_group_id,
            "lun": lun,
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

@mcp.tool(description="Configure access for volume identified by {volumeId} from Nimble / Alletra 6K identified by {systemId}")
def DeviceType2VolumesExport(systemId: str, volumeId: str, apply_to: str = None, force_apply_to: str = None, host_groups: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/volumes/{volumeId}/export"
        params = {}
        payload = {
            "apply_to": apply_to,
            "force_apply_to": force_apply_to,
            "host_groups": host_groups,
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

@mcp.tool(description="Get performance trend data of Nimble / Alletra 6K Volume identified by {id}")
def DeviceType2GetVolumePerformanceHistory(systemId: str, volumeId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/volumes/{volumeId}/performance-history"
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

@mcp.tool(description="Get performance statistics of Nimble / Alletra 6K Volume identified by {volumeId}")
def DeviceType2GetVolumePerformanceStatistics(systemId: str, volumeId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/volumes/{volumeId}/performance-statistics"
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

@mcp.tool(description="Get all snapshots' details of Nimble / Alletra 6K Volume identified by {volumeId}")
def DeviceType2GetAllSnapshotsByVolumeId(systemId: str, volumeId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/volumes/{volumeId}/snapshots"
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

@mcp.tool(description="Create Nimble / Alletra 6K snapshot in system identified by {systemId}")
def DeviceType2SnapshotCreate(systemId: str, volumeId: str, app_uuid: str = None, description: str = None, lock_period: str = None, metadata: str = None, name: str = None, online: str = None, writable: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/volumes/{volumeId}/snapshots"
        params = {}
        payload = {
            "app_uuid": app_uuid,
            "description": description,
            "lock_period": lock_period,
            "metadata": metadata,
            "name": name,
            "online": online,
            "writable": writable,
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

@mcp.tool(description="Remove Nimble / Alletra 6K snapshot in system identified by {snapshotId}")
def DeviceType2RemoveSnapshotById(systemId: str, volumeId: str, snapshotId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/volumes/{volumeId}/snapshots/{snapshotId}"
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

@mcp.tool(description="Get details of snapshot of Nimble / Alletra 6K Volume identified by {volumeId} by {snapshotId}")
def DeviceType2GetSnapshotById(systemId: str, volumeId: str, snapshotId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/volumes/{volumeId}/snapshots/{snapshotId}"
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

@mcp.tool(description="Configure access for snapshot identified by {snapshotId} from Nimble / Alletra 6K identified by {systemId}")
def DeviceType2SnapshotExport(systemId: str, volumeId: str, snapshotId: str, apply_to: str = None, force_apply_to: str = None, host_groups: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/volumes/{volumeId}/snapshots/{snapshotId}/export"
        params = {}
        payload = {
            "apply_to": apply_to,
            "force_apply_to": force_apply_to,
            "host_groups": host_groups,
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

@mcp.tool(description="Delete access for snapshot identified by {snapshotId} from Nimble / Alletra 6K identified by {systemId}")
def DeviceType2DeleteSnapshotAccessById(systemId: str, volumeId: str, snapshotId: str, host_groups: str = None, hosts: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/volumes/{volumeId}/snapshots/{snapshotId}/un-export"
        params = {}
        payload = {
            "host_groups": host_groups,
            "hosts": hosts,
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

@mcp.tool(description="Delete access for volume identified by {volumeId} from Nimble / Alletra 6K identified by {systemId}")
def DeviceType2DeleteVolumeAccessById(systemId: str, volumeId: str, host_groups: str = None, hosts: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type2/{systemId}/volumes/{volumeId}/un-export"
        params = {}
        payload = {
            "host_groups": host_groups,
            "hosts": hosts,
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

@mcp.tool(description="Get all HPE Alletra Storage MP B10000 storage systems")
def DeviceType4SystemsList():
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4"
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

@mcp.tool(description="Get HPE Alletra Storage MP B10000 object identified by {id}")
def DeviceType4SystemGetById(id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{id}"
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

@mcp.tool(description="Locate system of HPE Alletra Storage MP B10000")
def DeviceType4SystemLocate(id: str, locateEnabled: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{id}"
        params = {}
        payload = {
            "locateEnabled": locateEnabled,
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

@mcp.tool(description="Get alert-contact details for a storage system HPE Alletra Storage MP B10000")
def DeviceType4AlertContactsList(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/alert-contacts"
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

@mcp.tool(description="Add Alert/Mail contact details")
def DeviceType4AlertContactsCreate(systemId: str, company: str = None, companyCode: str = None, country: str = None, fax: str = None, firstName: str = None, includeSvcAlerts: str = None, lastName: str = None, notificationSeverities: str = None, preferredLanguage: str = None, primaryEmail: str = None, primaryPhone: str = None, receiveEmail: str = None, receiveGrouped: str = None, secondaryEmail: str = None, secondaryPhone: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/alert-contacts"
        params = {}
        payload = {
            "company": company,
            "companyCode": companyCode,
            "country": country,
            "fax": fax,
            "firstName": firstName,
            "includeSvcAlerts": includeSvcAlerts,
            "lastName": lastName,
            "notificationSeverities": notificationSeverities,
            "preferredLanguage": preferredLanguage,
            "primaryEmail": primaryEmail,
            "primaryPhone": primaryPhone,
            "receiveEmail": receiveEmail,
            "receiveGrouped": receiveGrouped,
            "secondaryEmail": secondaryEmail,
            "secondaryPhone": secondaryPhone,
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

@mcp.tool(description="Delete Alert/Email contact of storage system HPE Alletra Storage MP B10000 identified by {id}")
def DeviceType4AlertContactsDelete(systemId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/alert-contacts/{id}"
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

@mcp.tool(description="Get alert-contact details for a storage system HPE Alletra Storage MP B10000 identified by {id}")
def DeviceType4AlertContactsGetById(systemId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/alert-contacts/{id}"
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

@mcp.tool(description="Edit Alert/Email contact details of storage system HPE Alletra Storage MP B10000 identified by {id}")
def DeviceType4AlertContactsUpdate(systemId: str, id: str, company: str = None, companyCode: str = None, country: str = None, fax: str = None, firstName: str = None, includeSvcAlerts: str = None, lastName: str = None, notificationSeverities: str = None, preferredLanguage: str = None, primaryEmail: str = None, primaryPhone: str = None, receiveEmail: str = None, receiveGrouped: str = None, secondaryEmail: str = None, secondaryPhone: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/alert-contacts/{id}"
        params = {}
        payload = {
            "company": company,
            "companyCode": companyCode,
            "country": country,
            "fax": fax,
            "firstName": firstName,
            "includeSvcAlerts": includeSvcAlerts,
            "lastName": lastName,
            "notificationSeverities": notificationSeverities,
            "preferredLanguage": preferredLanguage,
            "primaryEmail": primaryEmail,
            "primaryPhone": primaryPhone,
            "receiveEmail": receiveEmail,
            "receiveGrouped": receiveGrouped,
            "secondaryEmail": secondaryEmail,
            "secondaryPhone": secondaryPhone,
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

@mcp.tool(description="Get Application Summary for a storage system HPE Alletra Storage MP B10000")
def DeviceType4ApplicationSummaryGet(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/application-summary"
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

@mcp.tool(description="Get all applicationset details for HPE Alletra Storage MP B10000")
def DeviceType4VolumeSetsList(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/applicationsets"
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

@mcp.tool(description="Create Application Set for a storage system HPE Alletra Storage MP B10000")
def DeviceType4VolumeSetsCreate(systemId: str, appSetBusinessUnit: str = None, appSetComments: str = None, appSetImportance: str = None, appSetName: str = None, appSetType: str = None, createAppSetQosConfigInput: str = None, customAppType: str = None, members: str = None, ransomware: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/applicationsets"
        params = {}
        payload = {
            "appSetBusinessUnit": appSetBusinessUnit,
            "appSetComments": appSetComments,
            "appSetImportance": appSetImportance,
            "appSetName": appSetName,
            "appSetType": appSetType,
            "createAppSetQosConfigInput": createAppSetQosConfigInput,
            "customAppType": customAppType,
            "members": members,
            "ransomware": ransomware,
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

@mcp.tool(description="Export applicationset identified by {appsetId} from HPE Alletra Storage MP B10000 identified by {systemId}")
def DeviceType4VolumeSetExport(systemId: str, appsetId: str, hostGroupDataMap: str = None, hostGroupIds: str = None, proximity: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{appsetId}/export"
        params = {}
        payload = {
            "hostGroupDataMap": hostGroupDataMap,
            "hostGroupIds": hostGroupIds,
            "proximity": proximity,
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

@mcp.tool(description="Get details of HPE Alletra Storage MP B10000 replication partners identified by {systemId} and {appsetId}")
def DeviceType4GetReplicationPartnersByAppSetId(systemId: str, appsetId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{appsetId}/replication-partners"
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

@mcp.tool(description="Get volume details of replication partners identified by {appsetId} and {replicationPartnerId} for HPE Alletra Storage MP B10000")
def DeviceType4GetReplicationPartnerVolumesByAppSetId(systemId: str, appsetId: str, replicationPartnerId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{appsetId}/replication-partners/{replicationPartnerId}/volumes"
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

@mcp.tool(description="Remove HPE Alletra Storage MP B10000 snapset in system identified by {snapsetId}")
def DeviceType4VolumeSetSnapshotGetById(systemId: str, appsetId: str, snapsetId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{appsetId}/snapsets/{snapsetId}"
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

@mcp.tool(description="Get details of snapset identified by {snapsetId} for Applicationset identified by {appsetId} for HPE Alletra Storage MP B10000")
def DeviceType4SnapsetsGetById(systemId: str, appsetId: str, snapsetId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{appsetId}/snapsets/{snapsetId}"
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

@mcp.tool(description="Unexport applicationset identified by {appsetId} from HPE Alletra Storage MP B10000 identified by {systemId}")
def DeviceType4VolumeSetUnexport(systemId: str, appsetId: str, hostGroupIds: str = None, hostIds: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{appsetId}/un-export"
        params = {}
        payload = {
            "hostGroupIds": hostGroupIds,
            "hostIds": hostIds,
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

@mcp.tool(description="Get volumes for an applicationset identified by appsetUid")
def DeviceType4VolumeSetVolumesList(systemId: str, appsetId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{appsetId}/volumes"
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

@mcp.tool(description="Remove applicationset identified by {id} from HPE Alletra Storage MP B10000 identified by {systemId}. Member volumes will not be removed.")
def DeviceType4VolumeSetsDeleteById(systemId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}"
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

@mcp.tool(description="Get applicationset details for an applicationset identified by appsetUid")
def DeviceType4VolumeSetsGetById(systemId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}"
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

@mcp.tool(description="Edit applicationset identified by {id} from HPE Alletra Storage MP B10000 identified by {systemId}")
def DeviceType4VolumeSetsEditById(systemId: str, id: str, addMembers: str = None, appSetBusinessUnit: str = None, appSetComments: str = None, appSetImportance: str = None, appSetName: str = None, appSetType: str = None, customAppType: str = None, editAppSetQosConfigInput: str = None, ransomware: str = None, removeMembers: str = None, retainVolumeExportsOnRemoval: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}"
        params = {}
        payload = {
            "addMembers": addMembers,
            "appSetBusinessUnit": appSetBusinessUnit,
            "appSetComments": appSetComments,
            "appSetImportance": appSetImportance,
            "appSetName": appSetName,
            "appSetType": appSetType,
            "customAppType": customAppType,
            "editAppSetQosConfigInput": editAppSetQosConfigInput,
            "ransomware": ransomware,
            "removeMembers": removeMembers,
            "retainVolumeExportsOnRemoval": retainVolumeExportsOnRemoval,
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

@mcp.tool(description="Get capacity details for an applicationset identified by appsetUid")
def DeviceType4VolumeSetCapacityStatisticsGetById(systemId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}/capacity-statistics"
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

@mcp.tool(description="Get the performance history data for the HPE Alletra Storage MP B10000 volume set identified by {id}, including the QOS configuration history and the top/bottom 5-10 volumes based on a metric or up to 10 selected volume's performance history on a storage system identified by {systemid}.")
def DeviceType4GetAppSetVolumesPerformanceHistory(systemId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}/performance"
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

@mcp.tool(description="Get details of protection policies configured on application set identified by {id} created on HPE Alletra Storage MP B10000 identified by {systemId}")
def DeviceType4GetProtectionPolicies(systemId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}/protection-policies"
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

@mcp.tool(description="Add protection policy on application set identified by {id} for a storage system HPE Alletra Storage MP B10000 identified by {systemId}")
def DeviceType4CreateProtectionPolicy(systemId: str, id: str, policy: str = None, policyId: str = None, protectionPolicyType: str = None, protectionStoreId: str = None, schedules: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}/protection-policies"
        params = {}
        payload = {
            "policy": policy,
            "policyId": policyId,
            "protectionPolicyType": protectionPolicyType,
            "protectionStoreId": protectionStoreId,
            "schedules": schedules,
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

@mcp.tool(description="Edit protection policy on application set identified by {id} for a storage system HPE Alletra Storage MP B10000 identified by {systemId}")
def DeviceType4EditProtectionPolicies(systemId: str, id: str, createSchedules: str = None, modifySchedules: str = None, policy: str = None, protectionPolicyType: str = None, removeSchedules: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}/protection-policies"
        params = {}
        payload = {
            "createSchedules": createSchedules,
            "modifySchedules": modifySchedules,
            "policy": policy,
            "protectionPolicyType": protectionPolicyType,
            "removeSchedules": removeSchedules,
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

@mcp.tool(description="Remedies issues caused in protection policy configuration on application set identified by {id} for a storage system HPE Alletra Storage MP B10000 identified by {systemId}")
def DeviceType4FixProtectionPolicy(systemId: str, id: str, policy: str = None, policyId: str = None, protectionPolicyType: str = None, protectionStoreId: str = None, schedules: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}/protection-policies/fix"
        params = {}
        payload = {
            "policy": policy,
            "policyId": policyId,
            "protectionPolicyType": protectionPolicyType,
            "protectionStoreId": protectionStoreId,
            "schedules": schedules,
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

@mcp.tool(description="Remove protection policy on application set identified by {id} for a storage system HPE Alletra Storage MP B10000 identified by {systemId}")
def DeviceType4removeProtectionPolicies(systemId: str, id: str, policies: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}/protection-policies/remove"
        params = {}
        payload = {
            "policies": policies,
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

@mcp.tool(description="Get hosts and proximity details identified by application set {id} for HPE Alletra Storage MP B10000 identified by {systemId}")
def DeviceType4GetProximitySettings(systemId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}/proximity-settings"
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

@mcp.tool(description="Change proximity settings of hosts where volume sets are exported identified by {id} and {systemId} from HPE Alletra Storage MP B10000")
def DeviceType4EditProximitySettings(systemId: str, id: str, hostGroups: str = None, hosts: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}/proximity-settings"
        params = {}
        payload = {
            "hostGroups": hostGroups,
            "hosts": hosts,
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

@mcp.tool(description="Actions on volume set identified by {id} and {systemId} from HPE Alletra Storage MP B10000")
def DeviceType4actionOnVolumeSets(systemId: str, id: str, action: str = None, parameters: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}/remote-protection/actions"
        params = {}
        payload = {
            "action": action,
            "parameters": parameters,
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

@mcp.tool(description="Get snapshot details of volume sets identified by {id} for HPE Alletra Storage MP B10000")
def DeviceType4VolumeSetSnapshotsList(systemId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}/snapsets"
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

@mcp.tool(description="Create snapshot for application set identified by {id}")
def DeviceType4VolumeSetsSnapshotCreate(systemId: str, id: str, comment: str = None, expireSecs: str = None, readOnly: str = None, retainSecs: str = None, snapshotName: str = None, vvNamePattern: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}/snapsets"
        params = {}
        payload = {
            "comment": comment,
            "expireSecs": expireSecs,
            "readOnly": readOnly,
            "retainSecs": retainSecs,
            "snapshotName": snapshotName,
            "vvNamePattern": vvNamePattern,
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

@mcp.tool(description="Get supported protection types for application set identified by {id} on storage system HPE Alletra Storage MP B10000 identified by {systemId}")
def DeviceType4getSupportedProtectionTypes(systemId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/applicationsets/{id}/supported-protection"
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

@mcp.tool(description="Get latest capacity trend data and forecasted data")
def DeviceType4SystemCapacityForecastGet(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/capacity-forecast"
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

@mcp.tool(description="Get capacity trend data for a storage system HPE Alletra Storage MP B10000")
def DeviceType4SystemCapacityHistoryGet(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/capacity-history"
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

@mcp.tool(description="Get system capacity for a storage system HPE Alletra Storage MP B10000")
def DeviceType4SystemCapacitySummaryGet(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/capacity-summary"
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

@mcp.tool(description="Get capacity time until full data for a storage system HPE Alletra Storage MP B10000")
def DeviceType4SystemCapacityTimeUntilFull(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/capacity-timeuntilfull"
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

@mcp.tool(description="Get array certificates by HPE Alletra Storage MP B10000")
def DeviceType4CertificatesList(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/certificates"
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

@mcp.tool(description="Create certificate on storage system HPE Alletra Storage MP B10000 identified by {systemId}")
def DeviceType4PostCertificate(systemId: str, authorityChain: str = None, commonName: str = None, country: str = None, days: str = None, keyLength: str = None, locality: str = None, organization: str = None, organizationUnit: str = None, province: str = None, service: str = None, subjectAltName: str = None, type: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/certificates"
        params = {}
        payload = {
            "authorityChain": authorityChain,
            "commonName": commonName,
            "country": country,
            "days": days,
            "keyLength": keyLength,
            "locality": locality,
            "organization": organization,
            "organizationUnit": organizationUnit,
            "province": province,
            "service": service,
            "subjectAltName": subjectAltName,
            "type": type,
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

@mcp.tool(description="Get array certificates by HPE Alletra Storage MP B10000 identified by {id}")
def DeviceType4CertificatesGetById(systemId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/certificates/{id}"
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

@mcp.tool(description="Import certificate identified by {id} on storage system HPE Alletra Storage MP B10000 identified by {systemId}")
def DeviceType4PutCertificate(systemId: str, id: str, authorityChain: str = None, certificate: str = None, vcGuid: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/certificates/{id}"
        params = {}
        payload = {
            "authorityChain": authorityChain,
            "certificate": certificate,
            "vcGuid": vcGuid,
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

@mcp.tool(description="Delete certificates from storage system HPE Alletra Storage MP B10000 identified by {systemId}")
def DeviceType4RemoveCertificates(systemId: str, certificates: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/certificates/remove"
        params = {}
        payload = {
            "certificates": certificates,
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

@mcp.tool(description="Trigger a collection on the storage system HPE Alletra Storage MP B10000")
def DeviceType4SupportDataCollect(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/collect-support-data"
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

@mcp.tool(description="Get component performance statistics details for a storage system HPE Alletra Storage MP B10000 idenfified by {systemId}")
def DeviceType4SystemComponentPerformanceStatisticsGet(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/component-performance-statistics"
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

@mcp.tool(description="Get details of HPE Alletra Storage MP B10000 Enclosure Cards identified by {systemId}")
def DeviceType4EnclosureCardList(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/enclosure-cards"
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

@mcp.tool(description="Get details of HPE Alletra Storage MP B10000 Enclosure Connectors")
def DeviceType4EnclosureConnectorsList(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/enclosure-connectors"
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

@mcp.tool(description="Get details of HPE Alletra Storage MP B10000 Enclosures")
def DeviceType4EnclosuresList(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/enclosures"
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

@mcp.tool(description="Get details of HPE Alletra Storage MP B10000 disks identified by {cageId}")
def DeviceType4DisksList(systemId: str, cageId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/enclosures/{cageId}/disks"
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

@mcp.tool(description="Get details of HPE Alletra Storage MP B10000 disk identified by {cageId} and {id}")
def DeviceType4DisksGetById(systemId: str, cageId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/enclosures/{cageId}/disks/{id}"
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

@mcp.tool(description="Get details of HPE Alletra Storage MP B10000 Enclosure Card Ports identified by {enclosureId}")
def DeviceType4EnclosureCardPortsList(systemId: str, enclosureId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/enclosures/{enclosureId}/enclosure-card-ports"
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

@mcp.tool(description="Get details of HPE Alletra Storage MP B10000 Enclosure Card Port identified by {enclosureId} and {id}")
def DeviceType4EnclosureCardPortsGetById(systemId: str, enclosureId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/enclosures/{enclosureId}/enclosure-card-ports/{id}"
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

@mcp.tool(description="Get details of HPE Alletra Storage MP B10000 Enclosure Cards identified by {enclosureId}")
def DeviceType4EnclosureCardsList(systemId: str, enclosureId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/enclosures/{enclosureId}/enclosure-cards"
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

@mcp.tool(description="Get details of HPE Alletra Storage MP B10000 Enclosure Card identified by {enclosureId} and {id}")
def DeviceType4EnclosureCardsGetById(systemId: str, enclosureId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/enclosures/{enclosureId}/enclosure-cards/{id}"
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

@mcp.tool(description="Locate IO Module of HPE Alletra Storage MP B10000 identified by {id}")
def DeviceType4EnclosureCardsLocateIOById(systemId: str, enclosureId: str, id: str, locate: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/enclosures/{enclosureId}/enclosure-cards/{id}"
        params = {}
        payload = {
            "locate": locate,
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

@mcp.tool(description="Get details of HPE Alletra Storage MP B10000 Enclosure Connectors identified by {enclosureId}")
def DeviceType4EnclosureConnectorList(systemId: str, enclosureId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/enclosures/{enclosureId}/enclosure-connectors"
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

@mcp.tool(description="Get details of HPE Alletra Storage MP B10000 Enclosure Connector identified by {enclosureId} and {enclosureConnectorId}")
def DeviceType4EnclosureConnectorsGetById(systemId: str, enclosureId: str, enclosureConnectorId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/enclosures/{enclosureId}/enclosure-connectors/{enclosureConnectorId}"
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

@mcp.tool(description="Get details of HPE Alletra Storage MP B10000 Enclosure Disks identified by {enclosureId}")
def DeviceType4EnclosureDisksList(systemId: str, enclosureId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/enclosures/{enclosureId}/enclosure-disks"
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

@mcp.tool(description="Get details of HPE Alletra Storage MP B10000 Enclosure Disk identified by {enclosureId} and {id}")
def DeviceType4EnclosureDisksGetById(systemId: str, enclosureId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/enclosures/{enclosureId}/enclosure-disks/{id}"
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

@mcp.tool(description="Get details of HPE Alletra Storage MP B10000 Enclosure Powers identified by {enclosureId}")
def DeviceType4EnclosurePowersList(systemId: str, enclosureId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/enclosures/{enclosureId}/enclosure-powers"
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

@mcp.tool(description="Get details of HPE Alletra Storage MP B10000 Enclosure Power identified by {enclosureId} and {id}")
def DeviceType4EnclosurePowersGetById(systemId: str, enclosureId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/enclosures/{enclosureId}/enclosure-powers/{id}"
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

@mcp.tool(description="Get details of HPE Alletra Storage MP B10000 Enclosure Sleds identified by {enclosureId}")
def DeviceType4EnclosureSledsList(systemId: str, enclosureId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/enclosures/{enclosureId}/enclosure-sleds"
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

@mcp.tool(description="Get details of HPE Alletra Storage MP B10000 Enclosure Sled identified by {enclosureId} and {id}")
def DeviceType4EnclosureSledsGetById(systemId: str, enclosureId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/enclosures/{enclosureId}/enclosure-sleds/{id}"
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

@mcp.tool(description="Locate drive of HPE Alletra Storage MP B10000 identified by {id}")
def DeviceType4EnclosureSledsLocateDriveById(systemId: str, enclosureId: str, id: str, locate: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/enclosures/{enclosureId}/enclosure-sleds/{id}"
        params = {}
        payload = {
            "locate": locate,
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

@mcp.tool(description="Get details of HPE Alletra Storage MP B10000 Enclosure identified by {id}")
def DeviceType4EnclosuresGetById(systemId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/enclosures/{id}"
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

@mcp.tool(description="Locate enclosure drive of HPE Alletra Storage MP B10000 identified by {id}")
def DeviceType4EnclosuresLocateById(systemId: str, id: str, locate: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/enclosures/{id}"
        params = {}
        payload = {
            "locate": locate,
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

@mcp.tool(description="Edit details of HPE Alletra Storage MP B10000 Enclosure identified by {id}")
def DeviceType4EnclosuresEditById(systemId: str, id: str, id: str = None, location: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/enclosures/{id}"
        params = {}
        payload = {
            "id": id,
            "location": location,
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

@mcp.tool(description="Encryption Backup Action on HPE Alletra Storage MP B10000 identified by {systemId}")
def DeviceType4backupActionOnEncryption(systemId: str, parameters: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/encryption/backup"
        params = {}
        payload = {
            "parameters": parameters,
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

@mcp.tool(description="Check EKM configuration on HPE Alletra Storage MP B10000 identified by {systemId}")
def DeviceType4checkEKMConfiguration(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/encryption/checkekm"
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

@mcp.tool(description="Encryption Enable Action on HPE Alletra Storage MP B10000 identified by {systemId}")
def DeviceType4enableActionOnEncryption(systemId: str, parameters: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/encryption/enable"
        params = {}
        payload = {
            "parameters": parameters,
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

@mcp.tool(description="Encryption Rekey Action on HPE Alletra Storage MP B10000 identified by {systemId}")
def DeviceType4rekeyActionOnEncryption(systemId: str, parameters: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/encryption/rekey"
        params = {}
        payload = {
            "parameters": parameters,
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

@mcp.tool(description="Encryption Restore Action on HPE Alletra Storage MP B10000 identified by {systemId}")
def DeviceType4restoreActionOnEncryption(systemId: str, key: str = None, parameters: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/encryption/restore"
        params = {}
        payload = {
            "key": key,
            "parameters": parameters,
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

@mcp.tool(description="Set EKM configuration on HPE Alletra Storage MP B10000 identified by {systemId}")
def DeviceType4setEKMConfiguration(systemId: str, parameters: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/encryption/setekm"
        params = {}
        payload = {
            "parameters": parameters,
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

@mcp.tool(description="Set EKM configuration and Encryption Backup Action on HPE Alletra Storage MP B10000 identified by {systemId}")
def DeviceType4setekmbackupActionOnEncryption(systemId: str, parameters: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/encryption/setekm/backup"
        params = {}
        payload = {
            "parameters": parameters,
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

@mcp.tool(description="Calls GET /api/v1/storage-systems/device-type4/{systemId}/file-shares")
def DeviceType4FileSharesList(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/file-shares"
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

@mcp.tool(description="Create Fileshare for a storage system HPE Alletra Storage MP")
def DeviceType4FileshareCreate(systemId: str, filesystemName: str = None, hostAccess: str = None, name: str = None, protocol: str = None, reduce: str = None, settingName: str = None, sizeInMiB: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/file-shares"
        params = {}
        payload = {
            "filesystemName": filesystemName,
            "hostAccess": hostAccess,
            "name": name,
            "protocol": protocol,
            "reduce": reduce,
            "settingName": settingName,
            "sizeInMiB": sizeInMiB,
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

@mcp.tool(description="This API endpoint deletes the specified file share")
def DeviceType4FileShareDeleteById(systemId: str, fileShareId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/file-shares/{fileShareId}"
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

@mcp.tool(description="Calls GET /api/v1/storage-systems/device-type4/{systemId}/file-shares/{fileShareId}")
def DeviceType4FileShareGetById(systemId: str, fileShareId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/file-shares/{fileShareId}"
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

@mcp.tool(description="Update Fileshare for a storage system HPE Alletra Storage MP")
def DeviceType4FileshareUpdate(systemId: str, fileShareId: str, additionalSizeInMiB: str = None, hostAccess: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/file-shares/{fileShareId}"
        params = {}
        payload = {
            "additionalSizeInMiB": additionalSizeInMiB,
            "hostAccess": hostAccess,
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

@mcp.tool(description="Calls GET /api/v1/storage-systems/device-type4/{systemId}/filesystems")
def DeviceType4FilesystemsList(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/filesystems"
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

@mcp.tool(description="This API endpoint deletes the specified filesystem")
def FilesystemsDelete(systemId: str, filesystemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/filesystems/{filesystemId}"
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

@mcp.tool(description="Calls GET /api/v1/storage-systems/device-type4/{systemId}/filesystems/{filesystemId}")
def DeviceType4FilesystemGetById(systemId: str, filesystemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/filesystems/{filesystemId}"
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

@mcp.tool(description="Get filesystem capacity trend data of HPE Alletra Storage MP Filesystem identified by {filesystemId}")
def DeviceType4FilesystemCapacityHistory(systemId: str, filesystemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/filesystems/{filesystemId}/capacity-history"
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

@mcp.tool(description="Get performance trend data of HPE Alletra Storage MP filesystem identified by {filesystemId}")
def DeviceType4FilesystemPerformanceHistory(systemId: str, filesystemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/filesystems/{filesystemId}/performance-history"
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

@mcp.tool(description="Get details of HPE Alletra Storage MP B10000 Host Paths")
def DeviceType4GetAllHostPaths(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/host-paths"
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

@mcp.tool(description="Get details of HPE Alletra Storage MP B10000 Host Path identified by {HostPathId}")
def DeviceType4GetHostPathsById(systemId: str, hostPathId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/host-paths/{hostPathId}"
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

@mcp.tool(description="Get details of HPE Alletra Storage MP B10000 Host Sets")
def DeviceType4GetAllHostSets(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/host-sets"
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

@mcp.tool(description="Get details of HPE Alletra Storage MP B10000 Host Set identified by {HostSetId}")
def DeviceType4GetHostSetsById(systemId: str, hostSetId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/host-sets/{hostSetId}"
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

@mcp.tool(description="Get details of HPE Alletra Storage MP B10000 Hosts")
def DeviceType4GetAllHosts(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/hosts"
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

@mcp.tool(description="Get details of HPE Alletra Storage MP B10000 Host identified by {HostId}")
def DeviceType4GetHostById(systemId: str, hostId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/hosts/{hostId}"
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

@mcp.tool(description="Get Top headroom contribution by volumes/Apps for device-type4")
def DeviceType4GetHeadroomContribution(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/insights/headroom-contribution"
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

@mcp.tool(description="Get the top hotspots segregated into read and write categories")
def DeviceType4GetHotspots(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/insights/hotspots"
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

@mcp.tool(description="Get system level latency factors of system identified by {systemId}")
def Device4LatencyFactorsGet(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/insights/latencyfactors"
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

@mcp.tool(description="Get the top volume contributors and timeseries data for disk and cpu resource contention")
def DeviceType4GetResourceContentionData(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/insights/resource-contention"
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

@mcp.tool(description="Get details of HPE Alletra Storage MP B10000 Inventory history")
def DeviceType4GetAllInventoryHistory(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/inventory-history"
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

@mcp.tool(description="Get details of HPE Alletra Storage MP B10000 InventoryUpdate identified by {inventoryUpdateId}")
def DeviceType4GetInventoryUpdateById(systemId: str, inventoryUpdateId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/inventory-history/{inventoryUpdateId}"
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

@mcp.tool(description="Get licenses of the storage system identified by {systemId}")
def DeviceType4LicensesGetById(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/licenses"
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

@mcp.tool(description="Set license of the storage system identified by {systemId}")
def DeviceType4SetLicense(systemId: str, parameters: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/licenses"
        params = {}
        payload = {
            "parameters": parameters,
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

@mcp.tool(description="Delete SMTP/mail server settings")
def DeviceType4MailSettingsDelete(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/mail-settings"
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

@mcp.tool(description="Get the system's SMTP/Mail server settigs")
def DeviceType4MailSettingsGet(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/mail-settings"
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

@mcp.tool(description="Add SMTP/Mail server settigs")
def DeviceType4MailSettingsAssociate(systemId: str, authenticationRequired: str = None, mailHostDomain: str = None, mailHostServer: str = None, password: str = None, port: str = None, senderEmailId: str = None, username: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/mail-settings"
        params = {}
        payload = {
            "authenticationRequired": authenticationRequired,
            "mailHostDomain": mailHostDomain,
            "mailHostServer": mailHostServer,
            "password": password,
            "port": port,
            "senderEmailId": senderEmailId,
            "username": username,
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

@mcp.tool(description="Edit SMTP/Mail server settigs")
def DeviceType4MailSettingsUpdate(systemId: str, authenticationRequired: str = None, mailHostDomain: str = None, mailHostServer: str = None, password: str = None, port: str = None, senderEmailId: str = None, username: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/mail-settings"
        params = {}
        payload = {
            "authenticationRequired": authenticationRequired,
            "mailHostDomain": mailHostDomain,
            "mailHostServer": mailHostServer,
            "password": password,
            "port": port,
            "senderEmailId": senderEmailId,
            "username": username,
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

@mcp.tool(description="Get CIM Network-Service details for a storage system HPE Alletra Storage MP B10000")
def DeviceType4NetworkServiceCimGet(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/network-services/cim"
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

@mcp.tool(description="Edit CIM network service configuration")
def DeviceType4NetworkServiceCimUpdate(systemId: str, cim: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/network-services/cim"
        params = {}
        payload = {
            "cim": cim,
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

@mcp.tool(description="Get SNMP-Manager Network-Service details for a storage system HPE Alletra Storage MP B10000")
def DeviceType4NetworkServiceSnmpMgrList(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/network-services/snmp-mgr"
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

@mcp.tool(description="Add SNMP Manager settings")
def DeviceType4NetworkServiceSnmpMgrCreate(systemId: str, snmpConfig: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/network-services/snmp-mgr"
        params = {}
        payload = {
            "snmpConfig": snmpConfig,
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

@mcp.tool(description="Delete SNMP manager settings identified by {id}")
def DeviceType4NetworkServiceSnmpMgrDelete(systemId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/network-services/snmp-mgr/{id}"
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

@mcp.tool(description="Get a specific SNMP-Manager Network-Service details for a storage system HPE Alletra Storage MP B10000")
def DeviceType4NetworkServiceSnmpMgrGetById(systemId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/network-services/snmp-mgr/{id}"
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

@mcp.tool(description="Edit SNMP Manager settings for the specified Id")
def DeviceType4NetworkServiceSnmpMgrUpdate(systemId: str, id: str, authenticationPassword: str = None, managerIP: str = None, notify: str = None, port: str = None, privPassword: str = None, retry: str = None, timeoutSecs: str = None, user: str = None, userMode: str = None, version: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/network-services/snmp-mgr/{id}"
        params = {}
        payload = {
            "authenticationPassword": authenticationPassword,
            "managerIP": managerIP,
            "notify": notify,
            "port": port,
            "privPassword": privPassword,
            "retry": retry,
            "timeoutSecs": timeoutSecs,
            "user": user,
            "userMode": userMode,
            "version": version,
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

@mcp.tool(description="Get SNMP users")
def DeviceType4SnmpUsersList(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/network-services/snmp-users"
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

@mcp.tool(description="Get SNMP users identified by {id}")
def DeviceType4SnmpUsersGetById(systemId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/network-services/snmp-users/{id}"
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

@mcp.tool(description="Get VASA Network-Service details for a storage system Primera / Alletra 9K")
def DeviceType4NetworkServiceVasaGet(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/network-services/vasa"
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

@mcp.tool(description="Enables or disable vasa service  on a HPE Alletra Storage MP B10000 storage system")
def DeviceType4NetworkServiceVasaConfigure(systemId: str, vasaId: str, action: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/network-services/vasa/{vasaId}"
        params = {}
        payload = {
            "action": action,
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

@mcp.tool(description="Enables, disable, updates the cert management mode for VASA services on a HPE Alletra Storage MP B10000 storage system. It also provides the ability to configure the batch parameters for VASA services and set up the second VASA Provider (VP) on a HPE Alletra Storage MP B10000 storage system from OS version 10.5.0 and above.")
def DeviceType4NetworkServiceConfigureVasaService(systemId: str, vasaId: str, certMgmt: str = None, cfgList: str = None, nodeId: str = None, vasaStateEnabled: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/network-services/vasa/{vasaId}/services"
        params = {}
        payload = {
            "certMgmt": certMgmt,
            "cfgList": cfgList,
            "nodeId": nodeId,
            "vasaStateEnabled": vasaStateEnabled,
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

@mcp.tool(description="Get Network-Settings details for a storage system HPE Alletra Storage MP B10000")
def DeviceType4NetworkSettingsGet(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/network-settings"
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

@mcp.tool(description="Post Network-Settings details for a storage system HPE Alletra Storage MP B10000")
def DeviceType4NetworkSettingsAssociate(systemId: str, dnsAddresses: str = None, ipv4Address: str = None, ipv4Gateway: str = None, ipv4SubnetMask: str = None, ipv6Address: str = None, ipv6Gateway: str = None, ipv6PrefixLen: str = None, proxyParams: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/network-settings"
        params = {}
        payload = {
            "dnsAddresses": dnsAddresses,
            "ipv4Address": ipv4Address,
            "ipv4Gateway": ipv4Gateway,
            "ipv4SubnetMask": ipv4SubnetMask,
            "ipv6Address": ipv6Address,
            "ipv6Gateway": ipv6Gateway,
            "ipv6PrefixLen": ipv6PrefixLen,
            "proxyParams": proxyParams,
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

@mcp.tool(description="Add a VASA Provider IP address on the specified node. After associating the VASA Provider (VP) to the specific node then this information is used to start second instance of the VP to achieve VPHA. This configuration will provide high availability of the connection between storage device and vSphere client and minimize service downtime during failures. Applicable for HPE Alletra Storage MP B10000 storage system with 10.5.0 version and above.")
def DeviceType4VasaProviderAddressConfigure(systemId: str, configVpAddress: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/network-settings/vasaprovider"
        params = {}
        payload = {
            "configVpAddress": configVpAddress,
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

@mcp.tool(description="Clear VASA Provider IP Address Configuration from a node at HPE Alletra Storage MP B10000 storage system. Applicable for HPE Alletra Storage MP B10000 storage system with 10.5.0 version and above.")
def DeviceType4VasaProviderAddressClear(systemId: str, clearVpAddress: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/network-settings/vasaprovider/clear"
        params = {}
        payload = {
            "clearVpAddress": clearVpAddress,
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

@mcp.tool(description="Get details of HPE Alletra Storage MP B10000 Nodes")
def DeviceType4NodesList(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/nodes"
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

@mcp.tool(description="Get details of HPE Alletra Storage MP B10000 Node identified by {id}")
def DeviceType4NodesGetById(systemId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/nodes/{id}"
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

@mcp.tool(description="Locate node of HPE Alletra Storage MP B10000 identified by {id}")
def DeviceType4NodesLocateById(systemId: str, id: str, locate: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/nodes/{id}"
        params = {}
        payload = {
            "locate": locate,
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

@mcp.tool(description="Get component performance statistics details of HPE Alletra Storage MP B10000 node idenfified by {nodeId}")
def DeviceType4NodeComponentPerformanceStatisticsGet(systemId: str, nodeId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/nodes/{nodeId}/component-performance-statistics"
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

@mcp.tool(description="Get service ports for nodes of all storage systems of HPE Alletra Storage MP B10000 identified by {systemId} and {nodeId }")
def DeviceType4NodeServicePortsGetById(systemId: str, nodeId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/nodes/{nodeId}/service-ports"
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

@mcp.tool(description="Get service ports for nodes of all storage systems of HPE Alletra Storage MP B10000 identified by {systemId}")
def DeviceType4NodeServicePortsList(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/nodes/service-ports"
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

@mcp.tool(description="Get performance trend data for a storage system HPE Alletra Storage MP B10000")
def DeviceType4SystemPerformanceHistoryGet(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/performance-history"
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

@mcp.tool(description="Get performance statistics for a storage system HPE Alletra Storage MP B10000")
def DeviceType4GetSystemPerformanceStatistics(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/performance-statistics"
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

@mcp.tool(description="Get details of performance metrics of physical drives on storage system identified by {systemid}")
def DeviceType4PhysicalDrivePerformanceHistoryGet(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/physicaldrives-performance"
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

@mcp.tool(description="Get details of HPE Alletra Storage MP B10000 Ports")
def DeviceType4PortsList(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/ports"
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

@mcp.tool(description="Get details of performance metrics of host ports on storage system identified by {systemid}")
def DeviceType4PortsPerformanceHistoryGet(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/ports-performance"
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

@mcp.tool(description="Get details of HPE Alletra Storage MP B10000 Port identified by {id}")
def DeviceType4PortsGetById(systemId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/ports/{id}"
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

@mcp.tool(description="Port enable disable identified by {id} from HPE Alletra Storage MP B10000 identified by {systemId}")
def DeviceType4PortEnable(systemId: str, id: str, portEnable: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/ports/{id}"
        params = {}
        payload = {
            "portEnable": portEnable,
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

@mcp.tool(description="Clear the details of the ports identified by {id} from HPE Alletra Storage MP B10000 identified by {systemId}")
def DeviceType4PortsClear(systemId: str, id: str, ipType: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/ports/{id}/clear"
        params = {}
        payload = {
            "ipType": ipType,
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

@mcp.tool(description="Edit file ports identified by {id} from HPE Alletra Storage MP B10000 identified by {systemId}. This operation is supported from OS version 10.5.0 and later.")
def DeviceType4FilePortEdit(systemId: str, id: str, ipAddress: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/ports/{id}/edit-file"
        params = {}
        payload = {
            "ipAddress": ipAddress,
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

@mcp.tool(description="Edit iscsi ports identified by {id} from HPE Alletra Storage MP B10000 identified by {systemId}")
def DeviceType4IscsiPortEdit(systemId: str, id: str, enablePeer: str = None, ethernetFlowControl: str = None, label: str = None, mtu: str = None, targetProtocol: str = None, vlans: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/ports/{id}/edit-iscsi"
        params = {}
        payload = {
            "enablePeer": enablePeer,
            "ethernetFlowControl": ethernetFlowControl,
            "label": label,
            "mtu": mtu,
            "targetProtocol": targetProtocol,
            "vlans": vlans,
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

@mcp.tool(description="Edit nvme ports identified by {id} from HPE Alletra Storage MP B10000 identified by {systemId}")
def DeviceType4NVMePortEdit(systemId: str, id: str, ethernetFlowControl: str = None, label: str = None, mtu: str = None, targetProtocol: str = None, vlans: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/ports/{id}/edit-nvme"
        params = {}
        payload = {
            "ethernetFlowControl": ethernetFlowControl,
            "label": label,
            "mtu": mtu,
            "targetProtocol": targetProtocol,
            "vlans": vlans,
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

@mcp.tool(description="Edit rcip ports identified by {id} from HPE Alletra Storage MP B10000 identified by {systemId}")
def DeviceType4RcipPortEdit(systemId: str, id: str, gatewayAddress: str = None, gatewayAddressV6: str = None, ipAddress: str = None, ipAddressV6: str = None, label: str = None, mtu: str = None, netMask: str = None, netMaskV6: str = None, speedConfigured: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/ports/{id}/edit-rcip"
        params = {}
        payload = {
            "gatewayAddress": gatewayAddress,
            "gatewayAddressV6": gatewayAddressV6,
            "ipAddress": ipAddress,
            "ipAddressV6": ipAddressV6,
            "label": label,
            "mtu": mtu,
            "netMask": netMask,
            "netMaskV6": netMaskV6,
            "speedConfigured": speedConfigured,
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

@mcp.tool(description="Edit ports identified by {id} from HPE Alletra Storage MP B10000 identified by {systemId}")
def DeviceType4FcPortEdit(systemId: str, id: str, configMode: str = None, connectionType: str = None, interuptCoalesce: str = None, label: str = None, speedConfigured: str = None, uniqueWWN: str = None, vcn: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/ports/{id}/fc"
        params = {}
        payload = {
            "configMode": configMode,
            "connectionType": connectionType,
            "interuptCoalesce": interuptCoalesce,
            "label": label,
            "speedConfigured": speedConfigured,
            "uniqueWWN": uniqueWWN,
            "vcn": vcn,
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

@mcp.tool(description="Initialize the details of the ports identified by {id} from HPE Alletra Storage MP B10000 identified by {systemId}")
def DeviceType4initialisePorts(systemId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/ports/{id}/initialize"
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

@mcp.tool(description="Ping file ports identified by {id} from HPE Alletra Storage MP B10000 identified by {systemId}. This operation is supported from OS version 10.5.0 and later.")
def DeviceType4FilePortPing(systemId: str, id: str, PacketSize: str = None, WaitTime: str = None, ipAddress: str = None, pingCount: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/ports/{id}/ping-file"
        params = {}
        payload = {
            "PacketSize": PacketSize,
            "WaitTime": WaitTime,
            "ipAddress": ipAddress,
            "pingCount": pingCount,
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

@mcp.tool(description="Ping iscsi ports identified by {id} from HPE Alletra Storage MP B10000 identified by {systemId}")
def DeviceType4IscsiPortPing(systemId: str, id: str, ipAddress: str = None, ipAddressv6: str = None, pingCount: str = None, vlanId: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/ports/{id}/ping-iscsi"
        params = {}
        payload = {
            "ipAddress": ipAddress,
            "ipAddressv6": ipAddressv6,
            "pingCount": pingCount,
            "vlanId": vlanId,
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

@mcp.tool(description="Ping nvme ports identified by {id} from HPE Alletra Storage MP B10000 identified by {systemId}")
def DeviceType4NVMePortPing(systemId: str, id: str, PacketSize: str = None, WaitTime: str = None, ipAddress: str = None, ipAddressv6: str = None, pingCount: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/ports/{id}/ping-nvme"
        params = {}
        payload = {
            "PacketSize": PacketSize,
            "WaitTime": WaitTime,
            "ipAddress": ipAddress,
            "ipAddressv6": ipAddressv6,
            "pingCount": pingCount,
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

@mcp.tool(description="Ping rcip ports identified by {id} from HPE Alletra Storage MP B10000 identified by {systemId}")
def DeviceType4RcipPortPing(systemId: str, id: str, PacketSize: str = None, WaitTime: str = None, ipAddress: str = None, ipAddressv6: str = None, pingCount: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/ports/{id}/ping-rcip"
        params = {}
        payload = {
            "PacketSize": PacketSize,
            "WaitTime": WaitTime,
            "ipAddress": ipAddress,
            "ipAddressv6": ipAddressv6,
            "pingCount": pingCount,
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

@mcp.tool(description="Get details of performance metrics of remote copy links on storage system identified by {systemid}")
def DeviceType4RemoteCopyLinksPerformanceHistoryGet(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/remotecopylinks-performance"
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

@mcp.tool(description="Calls GET /api/v1/storage-systems/device-type4/{systemId}/share-settings")
def DeviceType4ShareSettingsList(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/share-settings"
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

@mcp.tool(description="Calls GET /api/v1/storage-systems/device-type4/{systemId}/share-settings/{sharesettingsId}")
def DeviceType4ShareSettingsGetById(systemId: str, sharesettingsId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/share-settings/{sharesettingsId}"
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

@mcp.tool(description="Get the details of all read-write parent snapshots and base volume to which the child snapshot identified by {childSnapshotId} can be restored on HPE Alletra Storage MP B10000 system identified by {systemId}.")
def DeviceType4GetSnapshotRestoreOptions(systemId: str, childSnapshotId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/snapshots/{childSnapshotId}/restore-options"
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

@mcp.tool(description="Restore a child snapshot identified by {childSnapshotId} to a read-write parent snapshot identified by {parentSnapshotId} on HPE Alletra Storage MP B10000 storage system identified by {systemId}")
def DeviceType4RestoreSnapshotOfSnapshot(systemId: str, parentSnapshotId: str, childSnapshotId: str, priority: str = None, target: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/snapshots/{parentSnapshotId}/snapshots/{childSnapshotId}/restore"
        params = {}
        payload = {
            "priority": priority,
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

@mcp.tool(description="Create a clone of a snapshot identified by {snapshotId} for HPE Alletra Storage MP B10000 systems.")
def DeviceType4SnapshotCloneCreate(systemId: str, snapshotId: str, autoLun: str = None, destinationCpg: str = None, destinationVolume: str = None, hostGroupId: str = None, lun: str = None, priority: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/snapshots/{snapshotId}/clone"
        params = {}
        payload = {
            "autoLun": autoLun,
            "destinationCpg": destinationCpg,
            "destinationVolume": destinationVolume,
            "hostGroupId": hostGroupId,
            "lun": lun,
            "priority": priority,
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

@mcp.tool(description="Export vlun for snapshot identified by {id} from HPE Alletra Storage MP B10000 identified by {systemId}")
def DeviceType4VlunExportForSnapshot(systemId: str, snapshotId: str, LUN: str = None, autoLun: str = None, hostGroupIds: str = None, maxAutoLun: str = None, noVcn: str = None, override: str = None, position: str = None, proximity: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/snapshots/{snapshotId}/export"
        params = {}
        payload = {
            "LUN": LUN,
            "autoLun": autoLun,
            "hostGroupIds": hostGroupIds,
            "maxAutoLun": maxAutoLun,
            "noVcn": noVcn,
            "override": override,
            "position": position,
            "proximity": proximity,
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

@mcp.tool(description="Create snapshot of snapshot identified by {snapshotId} on a HPE Alletra storage MP B10000 system identified by {systemId}")
def DeviceType4SnapshotOfSnapshotCreate(systemId: str, snapshotId: str, comment: str = None, customName: str = None, expireSecs: str = None, namePattern: str = None, readOnly: str = None, retainSecs: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/snapshots/{snapshotId}/snapshots"
        params = {}
        payload = {
            "comment": comment,
            "customName": customName,
            "expireSecs": expireSecs,
            "namePattern": namePattern,
            "readOnly": readOnly,
            "retainSecs": retainSecs,
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

@mcp.tool(description="Unexport vlun for snapshot identified by {id} from HPE Alletra Storage MP B10000 identified by {systemId}")
def DeviceType4VlunUnexportForSnapshot(systemId: str, snapshotId: str, hostGroupIds: str = None, hostIds: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/snapshots/{snapshotId}/un-export"
        params = {}
        payload = {
            "hostGroupIds": hostGroupIds,
            "hostIds": hostIds,
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

@mcp.tool(description="Get details of vluns for Snapshot identified by {snapshotId} for HPE Alletra Storage MP B10000")
def DeviceType4GetSnapshotVlunsList(systemId: str, snapshotId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/snapshots/{snapshotId}/vluns"
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

@mcp.tool(description="Get details of vlun identified by {id} for Snapshot identified by {snapshotId} for HPE Alletra Storage MP B10000")
def DeviceType4GetsnapshotVlunsById(systemId: str, snapshotId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/snapshots/{snapshotId}/vluns/{id}"
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

@mcp.tool(description="Get all storage-pools details by HPE Alletra Storage MP B10000")
def DeviceType4StoragePoolList(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/storage-pools"
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

@mcp.tool(description="Get details of HPE Alletra Storage MP B10000 storage-pool identified by {id}")
def DeviceType4StoragePoolGetById(systemId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/storage-pools/{id}"
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

@mcp.tool(description="Get all volumes for storage-pool identified by {uuid} of HPE Alletra Storage MP B10000")
def DeviceType4StoragePoolVolumeGetById(systemId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/storage-pools/{id}/volumes"
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

@mcp.tool(description="Get support settings for a storage system HPE Alletra Storage MP B10000")
def DeviceType4SupportSettingsGet(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/support-settings"
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

@mcp.tool(description="Add support settings for a storage system HPE Alletra Storage MP B10000")
def DeviceType4SupportSettingsAssociate(systemId: str, connectToHPE: str = None, deviceId: str = None, enterpriseServerURL: str = None, miniInsploreEnabled: str = None, remoteAccess: str = None, remoteRequestAcknowledge: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/support-settings"
        params = {}
        payload = {
            "connectToHPE": connectToHPE,
            "deviceId": deviceId,
            "enterpriseServerURL": enterpriseServerURL,
            "miniInsploreEnabled": miniInsploreEnabled,
            "remoteAccess": remoteAccess,
            "remoteRequestAcknowledge": remoteRequestAcknowledge,
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

@mcp.tool(description="Edit support settings for a storage system HPE Alletra Storage MP B10000")
def DeviceType4SupportSettingsUpdate(systemId: str, connectToHPE: str = None, deviceId: str = None, enterpriseServerURL: str = None, miniInsploreEnabled: str = None, remoteAccess: str = None, remoteRequestAcknowledge: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/support-settings"
        params = {}
        payload = {
            "connectToHPE": connectToHPE,
            "deviceId": deviceId,
            "enterpriseServerURL": enterpriseServerURL,
            "miniInsploreEnabled": miniInsploreEnabled,
            "remoteAccess": remoteAccess,
            "remoteRequestAcknowledge": remoteRequestAcknowledge,
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

@mcp.tool(description="Get details of sustainability metrics of enclosure and system power supplies in Watts on storage system identified by {systemid}")
def DeviceType4EnclosurePowersSustainability(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/sustainabilityMetrics"
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

@mcp.tool(description="Get details of HPE Alletra Storage MP B10000 Switch ports")
def DeviceType4SwitchPortsList(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/switch-ports"
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

@mcp.tool(description="Get details of HPE Alletra Storage MP B10000 Switches")
def DeviceType4SwitchesList(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/switches"
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

@mcp.tool(description="Get details of HPE Alletra Storage MP B10000 Switch identified by {id}")
def DeviceType4SwitchesGetById(systemId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/switches/{id}"
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

@mcp.tool(description="Locate switch  of HPE Alletra Storage MP B10000 identified by {id}")
def DeviceType4SwitchLocateById(systemId: str, id: str, locate: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/switches/{id}"
        params = {}
        payload = {
            "locate": locate,
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

@mcp.tool(description="Get details of HPE Alletra Storage MP B10000 Switch Fans identified by switch id")
def DeviceType4SwitchFanList(systemId: str, switchId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/switches/{switchId}/switch-fans"
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

@mcp.tool(description="Get details of HPE Alletra Storage MP B10000 Switch Fan identified by switchId and Fan id")
def DeviceType4SwitchFanGetById(systemId: str, switchId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/switches/{switchId}/switch-fans/{id}"
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

@mcp.tool(description="Get details of HPE Alletra Storage MP B10000 Switch ports identified by {switchId}")
def DeviceType4SwitchPortList(systemId: str, switchId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/switches/{switchId}/switch-ports"
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

@mcp.tool(description="Get details of HPE Alletra Storage MP B10000 Switch identified by {switchId} and {id}")
def DeviceType4SwitchPortGetById(systemId: str, switchId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/switches/{switchId}/switch-ports/{id}"
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

@mcp.tool(description="Get details of HPE Alletra Storage MP B10000 Switch power supplies identified by {switchId}")
def DeviceType4SwitchPSList(systemId: str, switchId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/switches/{switchId}/switch-ps"
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

@mcp.tool(description="Get details of HPE Alletra Storage MP B10000 Switch Power Supplies identified by {switchId} and {id}")
def DeviceType4SwitchPSGetById(systemId: str, switchId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/switches/{switchId}/switch-ps/{id}"
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

@mcp.tool(description="Get the system settings configuration details")
def DeviceType4SystemSettingsList(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/system-settings"
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

@mcp.tool(description="Edit system settings configuration. Only one type of system settings i.e. either 'authMode or dateTime or installationSites or name or ntpAddresses or remoteSyslogSettings or srinfo or supportContact or systemParameters or enableFile (This operation is supported from OS version 10.5.0 and later.)' is allowed to be configured at a time.")
def DeviceType4SystemSettingsAssociate(systemId: str, authMode: str = None, dateTime: str = None, enableFile: str = None, installationSites: str = None, name: str = None, ntpAddresses: str = None, remoteSyslogSettings: str = None, srinfo: str = None, supportContact: str = None, systemParameters: str = None, timezone: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/system-settings"
        params = {}
        payload = {
            "authMode": authMode,
            "dateTime": dateTime,
            "enableFile": enableFile,
            "installationSites": installationSites,
            "name": name,
            "ntpAddresses": ntpAddresses,
            "remoteSyslogSettings": remoteSyslogSettings,
            "srinfo": srinfo,
            "supportContact": supportContact,
            "systemParameters": systemParameters,
            "timezone": timezone,
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

@mcp.tool(description="Edit system settings configuration. Only one type of system settings i.e. either 'authMode or dateTime or installationSites or name or ntpAddresses or remoteSyslogSettings or srinfo or supportContact or systemParameters or enableFile This operation is supported from OS version 10.5.0 and later.)' is allowed to be configured at a time.")
def DeviceType4SystemSettingsUpdate(systemId: str, authMode: str = None, dateTime: str = None, enableFile: str = None, installationSites: str = None, name: str = None, ntpAddresses: str = None, remoteSyslogSettings: str = None, srinfo: str = None, supportContact: str = None, systemParameters: str = None, timezone: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/system-settings"
        params = {}
        payload = {
            "authMode": authMode,
            "dateTime": dateTime,
            "enableFile": enableFile,
            "installationSites": installationSites,
            "name": name,
            "ntpAddresses": ntpAddresses,
            "remoteSyslogSettings": remoteSyslogSettings,
            "srinfo": srinfo,
            "supportContact": supportContact,
            "systemParameters": systemParameters,
            "timezone": timezone,
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

@mcp.tool(description="Get vVol details for a storage system HPE Alletra Storage MP B10000")
def DeviceType4vVolGet(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/system-settings/management-services/vvol"
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

@mcp.tool(description="Get Storage Container details for a storage system HPE Alletra Storage MP B10000")
def DeviceType4StorageContainerGet(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/system-settings/management-services/vvolscs"
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

@mcp.tool(description="Creates VMware storage container on storage system HPE Alletra Storage MP B10000 identified by {systemId}")
def DeviceType4CreatevVolSC(systemId: str, domain: str = None, hostIDs: str = None, hostSetIDs: str = None, name: str = None, scType: str = None, transportType: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/system-settings/management-services/vvolscs"
        params = {}
        payload = {
            "domain": domain,
            "hostIDs": hostIDs,
            "hostSetIDs": hostSetIDs,
            "name": name,
            "scType": scType,
            "transportType": transportType,
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

@mcp.tool(description="Delete storage container of storage system HPE Alletra Storage MP B10000 identified by {id}")
def DeviceType4StorageContainerDeleteById(systemId: str, vvolscId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/system-settings/management-services/vvolscs/{vvolscId}"
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

@mcp.tool(description="Edit storage container of storage system HPE Alletra Storage MP B10000 identified by {id}")
def DeviceType4StorageContainerEditById(systemId: str, vvolscId: str, comment: str = None, growthLimitMiB: str = None, growthSizeMiB: str = None, growthWarnMiB: str = None, name: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/system-settings/management-services/vvolscs/{vvolscId}"
        params = {}
        payload = {
            "comment": comment,
            "growthLimitMiB": growthLimitMiB,
            "growthSizeMiB": growthSizeMiB,
            "growthWarnMiB": growthWarnMiB,
            "name": name,
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

@mcp.tool(description="Attach host to Storage container identified by {volumeId} from HPE Alletra Storage MP B10000")
def DeviceType4AttachVolSC(systemId: str, vvolscId: str, action: str = None, parameter: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/system-settings/management-services/vvolscs/{vvolscId}/attach"
        params = {}
        payload = {
            "action": action,
            "parameter": parameter,
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

@mcp.tool(description="Detach host to Storage container identified by {volumeId} from HPE Alletra Storage MP B10000")
def DeviceType4DetachVolSC(systemId: str, vvolscId: str, action: str = None, parameter: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/system-settings/management-services/vvolscs/{vvolscId}/detach"
        params = {}
        payload = {
            "action": action,
            "parameter": parameter,
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

@mcp.tool(description="Get quorum witness configuration details from storage system HPE Alletra Storage MP B10000 identified by {systemId}")
def DeviceType4GetQuorumWitness(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/system-settings/quorum-witness"
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

@mcp.tool(description="Create quorum witness on storage system HPE Alletra Storage MP B10000 identified by {systemId}")
def DeviceType4PostQuorumWitness(systemId: str, parameters: str = None, replicationPartnerSystemId: str = None, srcReplicationId: str = None, startQuorumWitness: str = None, targetReplicationId: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/system-settings/quorum-witness"
        params = {}
        payload = {
            "parameters": parameters,
            "replicationPartnerSystemId": replicationPartnerSystemId,
            "srcReplicationId": srcReplicationId,
            "startQuorumWitness": startQuorumWitness,
            "targetReplicationId": targetReplicationId,
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

@mcp.tool(description="Delete quorum witness identified by {replicationPartnerId} on storage system HPE Alletra Storage MP B10000 identified by {systemId}")
def DeviceType4DeleteQuorumWitness(systemId: str, replicationPartnerId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/system-settings/quorum-witness/{replicationPartnerId}"
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

@mcp.tool(description="Get details of quorum witness configured on replication partner identified by {replicationPartnerId} on storage system HPE Alletra Storage MP B10000 identified by {systemId}")
def DeviceType4GetQuorumWitnessWithId(systemId: str, replicationPartnerId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/system-settings/quorum-witness/{replicationPartnerId}"
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

@mcp.tool(description="Edit quorum witness identified by {replicationPartnerId} on storage system HPE Alletra Storage MP B10000 identified by {systemId}")
def DeviceType4PutQuorumWitness(systemId: str, replicationPartnerId: str, replicationPartnerSystemId: str = None, startQuorumWitness: str = None, targetReplicationId: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/system-settings/quorum-witness/{replicationPartnerId}"
        params = {}
        payload = {
            "replicationPartnerSystemId": replicationPartnerSystemId,
            "startQuorumWitness": startQuorumWitness,
            "targetReplicationId": targetReplicationId,
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

@mcp.tool(description="Get details of replication partners on storage system HPE Alletra Storage MP B10000 identified by {systemId}")
def DeviceType4GetReplicationPartners(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/system-settings/replication-partners"
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

@mcp.tool(description="Create replication partners on HPE Alletra Storage MP B10000 identified by {systemId}")
def DeviceType4PostReplicationPartners(systemId: str, replicationPartners: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/system-settings/replication-partners"
        params = {}
        payload = {
            "replicationPartners": replicationPartners,
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

@mcp.tool(description="Get details of replication partner identified by {replicationPartnerId} on storage system HPE Alletra Storage MP B10000 identified by {systemId}")
def DeviceType4GetReplicationPartnerWithId(systemId: str, replicationPartnerId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/system-settings/replication-partners/{replicationPartnerId}"
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

@mcp.tool(description="Edit replication partner identified by {replicationPartnerId} on HPE Alletra Storage MP B10000 identified by {systemId}")
def DeviceType4PutReplicationPartner(systemId: str, replicationPartnerId: str, addRcLinks: str = None, removeRcLinks: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/system-settings/replication-partners/{replicationPartnerId}"
        params = {}
        payload = {
            "addRcLinks": addRcLinks,
            "removeRcLinks": removeRcLinks,
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

@mcp.tool(description="Delete replication partner from storage system HPE Alletra Storage MP B10000 identified by {systemId}")
def DeviceType4PostRemoveReplicationPartners(systemId: str, replicationPartners: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/system-settings/replication-partners/remove"
        params = {}
        payload = {
            "replicationPartners": replicationPartners,
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

@mcp.tool(description="Get telemetry status for a storage system HPE Alletra Storage MP B10000")
def DeviceType4TelemetryGet(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/telemetry"
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

@mcp.tool(description="Get certificates trusted by HPE Alletra Storage MP B10000")
def DeviceType4TrustedCertificatesList(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/trust-certificates"
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

@mcp.tool(description="Add trusted certificates for storage system HPE Alletra Storage MP B10000 identified by {systemId}")
def DeviceType4AddTrustedCertificates(systemId: str, action: str = None, parameters: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/trust-certificates"
        params = {}
        payload = {
            "action": action,
            "parameters": parameters,
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

@mcp.tool(description="Get certificates trusted by HPE Alletra Storage MP B10000 identified by {id}")
def DeviceType4TrustedCertificatesGetById(systemId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/trust-certificates/{id}"
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

@mcp.tool(description="Delete trusted certificates from storage system HPE Alletra Storage MP B10000 identified by {systemId}")
def DeviceType4RemoveTrustedCertificates(systemId: str, trustedCertificates: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/trust-certificates/remove"
        params = {}
        payload = {
            "trustedCertificates": trustedCertificates,
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

@mcp.tool(description="Get vcenter settings for a storage system HPE Alletra Storage MP B10000")
def DeviceType4VMManagerSettingsList(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/vm-manager-settings"
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

@mcp.tool(description="Add vCenter settings to storage system HPE Alletra Storage MP B10000")
def DeviceType4PostVCenterSettings(systemId: str, certChainPem: str = None, description: str = None, inetaddress: str = None, name: str = None, password: str = None, port: str = None, username: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/vm-manager-settings"
        params = {}
        payload = {
            "certChainPem": certChainPem,
            "description": description,
            "inetaddress": inetaddress,
            "name": name,
            "password": password,
            "port": port,
            "username": username,
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

@mcp.tool(description="Delete vcenter setting identified by {vcenterSettingId} on storage system HPE Alletra Storage MP B10000 identified by {systemId}")
def DeviceType4DeleteVCenterSettings(systemId: str, vcenterSettingId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/vm-manager-settings/{vcenterSettingId}"
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

@mcp.tool(description="Get vcenter setting detail for a given vcenter setting of a storage system HPE Alletra Storage MP B10000")
def DeviceType4VMManagerSettingsGetById(systemId: str, vcenterSettingId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/vm-manager-settings/{vcenterSettingId}"
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

@mcp.tool(description="Edit vCenter setting identified by {vcenterSettingId} on HPE Alletra Storage MP B10000 identified by {systemId}")
def DeviceType4PutVCenterSettings(systemId: str, vcenterSettingId: str, certChainPem: str = None, description: str = None, inetaddress: str = None, name: str = None, password: str = None, port: str = None, username: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/vm-manager-settings/{vcenterSettingId}"
        params = {}
        payload = {
            "certChainPem": certChainPem,
            "description": description,
            "inetaddress": inetaddress,
            "name": name,
            "password": password,
            "port": port,
            "username": username,
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

@mcp.tool(description="Get vme settings for a storage system HPE Alletra Storage MP B10000")
def DeviceType4VMEManagerSettingsList(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/vme-manager-settings"
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

@mcp.tool(description="Add vme settings to storage system HPE Alletra Storage MP B10000")
def DeviceType4PostVMESettings(systemId: str, accessToken: str = None, address: str = None, certificateVerification: str = None, description: str = None, name: str = None, port: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/vme-manager-settings"
        params = {}
        payload = {
            "accessToken": accessToken,
            "address": address,
            "certificateVerification": certificateVerification,
            "description": description,
            "name": name,
            "port": port,
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

@mcp.tool(description="Delete vme setting identified by {vmeSettingId} on storage system HPE Alletra Storage MP B10000 identified by {systemId}")
def DeviceType4DeleteVMESettings(systemId: str, vmeSettingId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/vme-manager-settings/{vmeSettingId}"
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

@mcp.tool(description="Get details for a given vme-setting of a storage system HPE Alletra Storage MP B10000")
def DeviceType4VMEManagerSettingsGetById(systemId: str, vmeSettingId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/vme-manager-settings/{vmeSettingId}"
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

@mcp.tool(description="Edit vme setting identified by {vmeSettingId} on HPE Alletra Storage MP B10000 identified by {systemId}")
def DeviceType4PutVMESettings(systemId: str, vmeSettingId: str, accessToken: str = None, address: str = None, certificateVerification: str = None, description: str = None, name: str = None, port: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/vme-manager-settings/{vmeSettingId}"
        params = {}
        payload = {
            "accessToken": accessToken,
            "address": address,
            "certificateVerification": certificateVerification,
            "description": description,
            "name": name,
            "port": port,
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

@mcp.tool(description="Get all volumes details for HPE Alletra Storage MP B10000")
def DeviceType4VolumesList(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/volumes"
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

@mcp.tool(description="Create volume for a storage system HPE Alletra Storage MP B10000")
def DeviceType4VolumeCreate(systemId: str, comments: str = None, count: str = None, dataReduction: str = None, name: str = None, ransomware: str = None, sizeMib: str = None, snapshotAllocWarning: str = None, userAllocWarning: str = None, userCpg: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/volumes"
        params = {}
        payload = {
            "comments": comments,
            "count": count,
            "dataReduction": dataReduction,
            "name": name,
            "ransomware": ransomware,
            "sizeMib": sizeMib,
            "snapshotAllocWarning": snapshotAllocWarning,
            "userAllocWarning": userAllocWarning,
            "userCpg": userCpg,
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

@mcp.tool(description="Get performance history of Volumes on storage system identified by {systemid}")
def DeviceType4GetVolumesPerformanceHistory(systemId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/volumes-performance"
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

@mcp.tool(description="Remove volume identified by {volumeId} from HPE Alletra Storage MP B10000")
def DeviceType4VolumeDelete(systemId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/volumes/{id}"
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

@mcp.tool(description="Get details of HPE Alletra Storage MP B10000 Volume identified by {id}")
def DeviceType4VolumeGetById(systemId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/volumes/{id}"
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

@mcp.tool(description="Edit volume identified by {volumeId} from HPE Alletra Storage MP B10000")
def DeviceType4VolumeEdit(systemId: str, id: str, conversionType: str = None, dataReduction: str = None, name: str = None, ransomware: str = None, sizeMib: str = None, snapshotAllocWarning: str = None, userAllocWarning: str = None, userCpgName: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/volumes/{id}"
        params = {}
        payload = {
            "conversionType": conversionType,
            "dataReduction": dataReduction,
            "name": name,
            "ransomware": ransomware,
            "sizeMib": sizeMib,
            "snapshotAllocWarning": snapshotAllocWarning,
            "userAllocWarning": userAllocWarning,
            "userCpgName": userCpgName,
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

@mcp.tool(description="Get volume capacity trend data of HPE Alletra Storage MP B10000 Volume identified by {id}")
def DeviceType4VolumeCapacityHistoryGetById(systemId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/volumes/{id}/capacity-history"
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

@mcp.tool(description="Create a clone volume identified by {id} for HPE Alletra Storage MP B10000 systems.")
def DeviceType4VolumeCloneCreate(systemId: str, id: str, destinationVolume: str = None, offlineClone: str = None, online: str = None, onlineClone: str = None, priority: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/volumes/{id}/clone"
        params = {}
        payload = {
            "destinationVolume": destinationVolume,
            "offlineClone": offlineClone,
            "online": online,
            "onlineClone": onlineClone,
            "priority": priority,
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

@mcp.tool(description="Export vlun for volume identified by {id} from HPE Alletra Storage MP B10000 identified by {systemId}")
def DeviceType4VlunExport(systemId: str, id: str, LUN: str = None, autoLun: str = None, hostGroupIds: str = None, maxAutoLun: str = None, noVcn: str = None, override: str = None, position: str = None, proximity: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/volumes/{id}/export"
        params = {}
        payload = {
            "LUN": LUN,
            "autoLun": autoLun,
            "hostGroupIds": hostGroupIds,
            "maxAutoLun": maxAutoLun,
            "noVcn": noVcn,
            "override": override,
            "position": position,
            "proximity": proximity,
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

@mcp.tool(description="Get histogram buckets distribution of I/Os of a volume for a given duration. buckets query param must be one or more combination of the following values: Size512B, Size1k, Size2k, Size4k, Size8k, Size16k, Size32k, Size64k, Size128k, Size256k, Size512k, Size1m, Size2m")
def DeviceType4GetPerformanceHistogram(systemId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/volumes/{id}/performance-histogram"
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

@mcp.tool(description="Get performance trend data of HPE Alletra Storage MP B10000 Volume identified by {id}")
def DeviceType4VolumePerformanceHistoryGetById(systemId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/volumes/{id}/performance-history"
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

@mcp.tool(description="Get performance statistics of HPE Alletra Storage MP B10000 Volume identified by {id}")
def DeviceType4VolumePerformanceStatisticsGetById(systemId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/volumes/{id}/performance-statistics"
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

@mcp.tool(description="Get snapshot details of volume identified by {id} for HPE Alletra Storage MP B10000")
def DeviceType4VolumeSnapshotsList(systemId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/volumes/{id}/snapshots"
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

@mcp.tool(description="Create snapshot for volumes identified by {id}")
def DeviceType4VolumeSnapshotCreate(systemId: str, id: str, comment: str = None, customName: str = None, expireSecs: str = None, namePattern: str = None, readOnly: str = None, retainSecs: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/volumes/{id}/snapshots"
        params = {}
        payload = {
            "comment": comment,
            "customName": customName,
            "expireSecs": expireSecs,
            "namePattern": namePattern,
            "readOnly": readOnly,
            "retainSecs": retainSecs,
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

@mcp.tool(description="Unexport vlun for volume identified by {id} from HPE Alletra Storage MP B10000 identified by {systemId}")
def DeviceType4VlunUnexport(systemId: str, id: str, hostGroupIds: str = None, hostIds: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/volumes/{id}/un-export"
        params = {}
        payload = {
            "hostGroupIds": hostGroupIds,
            "hostIds": hostIds,
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

@mcp.tool(description="Get details of vluns for Volume identified by {volumeId} for HPE Alletra Storage MP B10000")
def DeviceType4VlunsList(systemId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/volumes/{id}/vluns"
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

@mcp.tool(description="Get the details of the clone volumes associated with a base volume identified by {volumeId} for HPE Alletra Storage MP B10000 systems.")
def DeviceType4GetClones(systemId: str, volumeId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/clones"
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

@mcp.tool(description="Edit a clone volume identified by {cloneId} of a volume identified by {volumeId} on storage system HPE Alletra Storage MP B10000 identified by {systemId}")
def DeviceType4EditCloneVolume(systemId: str, volumeId: str, cloneId: str, ransomware: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/clones/{cloneId}"
        params = {}
        payload = {
            "ransomware": ransomware,
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

@mcp.tool(description="Promote a clone volume identified by {cloneId} of a volume identified by {volumeId} on storage system HPE Alletra Storage MP B10000 identified by {systemId}")
def DeviceType4PromoteCloneVolume(systemId: str, volumeId: str, cloneId: str, priority: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/clones/{cloneId}/promote"
        params = {}
        payload = {
            "priority": priority,
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

@mcp.tool(description="Resynchronize a clone volume identified by {cloneId} of a volume identified by {volumeId} on storage system HPE Alletra Storage MP B10000 identified by {systemId}")
def DeviceType4ResyncCloneVolume(systemId: str, volumeId: str, cloneId: str, priority: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/clones/{cloneId}/resync"
        params = {}
        payload = {
            "priority": priority,
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

@mcp.tool(description="Get the high latency points to be annotated segregated into read and write categories")
def DeviceType4GetVolumeLatencyAnnotations(systemId: str, volumeId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/insights/latency-annotations"
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

@mcp.tool(description="Get latency drifts of a volume for a give duration.The minimum duration supported is 8 hours and a maximum duration of 2 days. Drifts are detected in both read and write latency metrics")
def DeviceType4GetPerformanceDrifts(systemId: str, volumeId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/insights/performance-drifts"
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

@mcp.tool(description="Get snapshot schedules of a volume identified by {volumeId} on HPE Alletra Storage MP B10000 storage system identified by {systemId}")
def DeviceType4VolumeSnapshotSchedulesList(systemId: str, volumeId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/schedules"
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

@mcp.tool(description="Create snapshot schedule for a volume identified by {volumeId} on HPE Alletra Storage MP B10000 storage system identified by {systemId}")
def DeviceType4VolumeSnapshotScheduleCreate(systemId: str, volumeId: str, allowSysOffsetMinute: str = None, atTime: str = None, dayOfMonth: str = None, days: str = None, expireSecs: str = None, name: str = None, period: str = None, periodUnit: str = None, readOnly: str = None, retainSecs: str = None, untilTime: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/schedules"
        params = {}
        payload = {
            "allowSysOffsetMinute": allowSysOffsetMinute,
            "atTime": atTime,
            "dayOfMonth": dayOfMonth,
            "days": days,
            "expireSecs": expireSecs,
            "name": name,
            "period": period,
            "periodUnit": periodUnit,
            "readOnly": readOnly,
            "retainSecs": retainSecs,
            "untilTime": untilTime,
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

@mcp.tool(description="Delete snapshot Schedule identified by {scheduleId} of a volume identified by {volumeId} on HPE Alletra Storage MP B10000 storage system identified by {systemId}")
def DeviceType4VolumeSnapshotScheduleDelete(systemId: str, volumeId: str, scheduleId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/schedules/{scheduleId}"
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

@mcp.tool(description="Get details of snapshot schedule identified by {scheduleId} for a volume identified by {volumeId} on HPE Alletra Storage MP B10000 storage system identified by {systemId}")
def DeviceType4VolumeSnapshotScheduleGetById(systemId: str, volumeId: str, scheduleId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/schedules/{scheduleId}"
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

@mcp.tool(description="Edit Snapshot Schedule identified by {scheduleId} of a volume identified by {volumeId} on storage system HPE Alletra Storage MP B10000 identified by {systemId}")
def arcusEditVolumeSnapshotSchedule(systemId: str, volumeId: str, scheduleId: str, allowSysOffsetMinute: str = None, atTime: str = None, dayOfMonth: str = None, days: str = None, name: str = None, period: str = None, periodUnit: str = None, untilTime: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/schedules/{scheduleId}"
        params = {}
        payload = {
            "allowSysOffsetMinute": allowSysOffsetMinute,
            "atTime": atTime,
            "dayOfMonth": dayOfMonth,
            "days": days,
            "name": name,
            "period": period,
            "periodUnit": periodUnit,
            "untilTime": untilTime,
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

@mcp.tool(description="Remove HPE Alletra Storage MP B10000 snapshot in system identified by {snapshotId}")
def DeviceType4VolumeSnapshotGetById(systemId: str, volumeId: str, snapshotId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/snapshots/{snapshotId}"
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

@mcp.tool(description="Get details of vlun identified by {id} for Volume identified by {volumeId} for HPE Alletra Storage MP B10000")
def DeviceType4SnapshotsGetById(systemId: str, volumeId: str, snapshotId: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/snapshots/{snapshotId}"
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

@mcp.tool(description="Promote a snapshot identified by {snapshotId} of a volume identified by {volumeId} on storage system HPE Alletra Storage MP B10000 identified by {systemId}")
def DeviceType4PromoteSnapshot(systemId: str, volumeId: str, snapshotId: str, priority: str = None, target: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/snapshots/{snapshotId}"
        params = {}
        payload = {
            "priority": priority,
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

@mcp.tool(description="Edit a snapshot identified by {snapshotId} of a volume identified by {volumeId} on storage system HPE Alletra Storage MP B10000 identified by {systemId}")
def DeviceType4EditSnapshot(systemId: str, volumeId: str, snapshotId: str, ransomware: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/snapshots/{snapshotId}"
        params = {}
        payload = {
            "ransomware": ransomware,
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

@mcp.tool(description="Remove vlun idenfied by {id} form volume identified by {volumeId} from HPE Alletra Storage MP B10000")
def DeviceType4VlunsDelete(systemId: str, volumeId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/vluns/{id}"
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

@mcp.tool(description="Get details of vlun identified by {id} for Volume identified by {volumeId} for HPE Alletra Storage MP B10000")
def DeviceType4VlunsGetById(systemId: str, volumeId: str, id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/{systemId}/volumes/{volumeId}/vluns/{id}"
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

@mcp.tool(description="List all insights.")
def DeviceType4Insights():
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/device-type4/systemInsights/insights"
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

@mcp.tool(description="provisioning recommendations")
def ProvisioningRecommendations(hostGroupId: str = None, productFamily: str = None, sizeMib: str = None):
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/provisioning-recommendations"
        params = {}
        payload = {
            "hostGroupId": hostGroupId,
            "productFamily": productFamily,
            "sizeMib": sizeMib,
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

@mcp.tool(description="Get all device types")
def GetDeviceType():
    try:
        url = f"{API_BASE_URL}/api/v1/storage-systems/storage-types"
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

@mcp.tool(description="Returns a list of tasks that are visible to the user. The response can
be paged by using the limit
and offset query parameters and filtered, sorted and ordered by using
the filter, sortby and orderby query parameters.
")
def ListTasks():
    try:
        url = f"{API_BASE_URL}/api/v1/tasks"
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

@mcp.tool(description="Returns the task with the given id.")
def GetTask(id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/tasks/{id}"
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

@mcp.tool(description="Get all volume sets")
def VolumesetList():
    try:
        url = f"{API_BASE_URL}/api/v1/volume-sets"
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

@mcp.tool(description="Get volume-set identified by id")
def VolumesetGetById(id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/volume-sets/{id}"
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

@mcp.tool(description="Get volumes  identified by volume set id")
def VolumesetGetByvolumesetId(id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/volume-sets/{id}/volumes"
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

@mcp.tool(description="Get all volumes")
def VolumesList():
    try:
        url = f"{API_BASE_URL}/api/v1/volumes"
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

@mcp.tool(description="Get details of Volume identified by {id}")
def VolumeGetById(id: str):
    try:
        url = f"{API_BASE_URL}/api/v1/volumes/{id}"
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
