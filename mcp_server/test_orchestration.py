import sys, os
sys.path.append('.')
os.environ['PYTHONIOENCODING'] = 'utf-8'

from mcp_server import manage_infrastructure_resource
import asyncio

async def main():
    print("=== Testing STATUS: ap-floor-022 ===")
    res = await manage_infrastructure_resource('{"action": "STATUS", "identifier": "ap-floor-022"}')
    print(res)

    print("\n=== Testing VLAN ADD ===")
    res = await manage_infrastructure_resource('{"action": "ADD_VLAN", "identifier": "vlan", "device": "aruba-cx-017", "vlan_id": 111, "name": "Production"}')
    print(res)

    print("\n=== Testing PORT UPDATE ===")
    res = await manage_infrastructure_resource('{"action": "UPDATE", "identifier": "interface", "device": "aruba-cx-017", "interface": "eth1", "status": "UP"}')
    print(res)
    
    print("\n=== Testing TOPOLOGY DISCOVERY ===")
    res = await manage_infrastructure_resource('{"action": "DISCOVER", "identifier": "topology", "device": "aruba-cx-017"}')
    print(res)

if __name__ == "__main__":
    asyncio.run(main())
