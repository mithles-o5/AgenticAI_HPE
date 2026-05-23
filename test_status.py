import asyncio
from mcp_server.mcp_server import manage_oneview_server, manage_comops_server
from authentication.token_store import save_token

async def main():
    # Inject a local token
    save_token("test-token", "local")

    print("\n--- Getting Status for OneView Server ---")
    res1 = await manage_oneview_server("status of OV1-RackServer-001")
    print(res1)
    
    print("\n--- Getting Status for ComOps Server ---")
    res2 = await manage_comops_server("status of CoM-CloudNode-001")
    print(res2)

if __name__ == "__main__":
    asyncio.run(main())
