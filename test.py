import os
import sys
import asyncio

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from mcp_server.mcp_server import manage_infrastructure_resource

async def main():
    devices = ["stg-array-10014", "gl-ns-008"]
    for d in devices:
        query = f'{{"identifier": "{d}", "action": "STATUS", "category": "Operational"}}'
        print(f"Testing {d}...")
        result = await manage_infrastructure_resource(query)
        print(result)

asyncio.run(main())
