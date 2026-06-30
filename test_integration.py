import sys, os
sys.path.append('.')
os.environ['PYTHONIOENCODING'] = 'utf-8'

from mcp_server.mcp_server import manage_infrastructure_resource
import asyncio

async def main():
    print("=== Testing Network STATUS: ap-floor-022 ===")
    res = await manage_infrastructure_resource('{"action": "STATUS", "identifier": "ap-floor-022"}')
    print(res)

    print("\n=== Testing Network VLAN ADD ===")
    res = await manage_infrastructure_resource('{"action": "ADD_VLAN", "identifier": "vlan", "device": "aruba-cx-017", "vlan_id": 111, "name": "Production"}')
    print(res)

    # Let's try some newly merged server commands if any exist in the CMDB
    print("\n=== Testing Server STATUS: ilo-mock-01 ===")
    res = await manage_infrastructure_resource('{"action": "STATUS", "identifier": "ilo-mock-01"}')
    print(res)

if __name__ == "__main__":
    asyncio.run(main())
