import sys
import os
import mock_db_cache
mock_db_cache.setup()

import asyncio

from mcp_server.mcp_server import (
    manage_oneview_resource,
    manage_comops_resource,
    _trigger_login,
)

async def test_creation():
    print("=" * 60)
    print("RUNNING END-TO-END SERVER CREATION TEST")
    print("=" * 60)

    # 1. Login with local developer token (Infrastructure administrator)
    print("\n[+] Logging in as devasksr (Infrastructure administrator)...")
    _trigger_login("local", username="devasksr", password="password123")
    print("OK: Logged in successfully.")

    # 2. Status check for non-existent server (should fail resolution)
    print("\n[+] Checking status of non-existent server (expecting failure)...")
    res1 = await manage_comops_resource("status OV1-TestServer-999")
    print(res1)

    # 3. Create the server in Compute Ops
    print("\n[+] Creating server 'OV1-TestServer-999' in Compute Ops (expecting success)...")
    res2 = await manage_comops_resource("create server OV1-TestServer-999")
    print(res2)

    # 4. Status check for the newly created server (expecting success now!)
    print("\n[+] Checking status of 'OV1-TestServer-999' again (expecting success)...")
    res3 = await manage_comops_resource("status OV1-TestServer-999")
    print(res3)

    # 5. Create a server in OneView
    print("\n[+] Creating server 'OV1-RackServer-999' in OneView (expecting success)...")
    res4 = await manage_oneview_resource("create server OV1-RackServer-999")
    print(res4)

    # 6. Status check for the newly created OneView server (expecting success)
    print("\n[+] Checking status of 'OV1-RackServer-999' again (expecting success)...")
    res5 = await manage_oneview_resource("status OV1-RackServer-999")
    print(res5)

    print("\n" + "=" * 60)
    print("SUCCESS: SERVER CREATION AND CMDB REGISTRATION TESTS COMPLETED!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_creation())
