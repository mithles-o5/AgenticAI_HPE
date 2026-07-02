import asyncio
import os
os.environ["AUTH_DISABLED"] = "1"
from mcp_server.mcp_server import manage_infrastructure_resource

async def main():
    print("Testing 'list all servers'...")
    res = await manage_infrastructure_resource('list all servers')
    print(res)

if __name__ == "__main__":
    asyncio.run(main())
