import sys
import os
import asyncio
import subprocess
import time

sys.path.insert(0, os.path.abspath('.'))
from mcp_server.mcp_server import (
    manage_oneview_resource,
    manage_comops_resource,
    _trigger_login,
    logout,
    check_access
)

async def main():
    print("="*60)
    print("🚀 STARTING INTEGRATED DEMO")
    print("="*60)

    # Start mock servers as subprocesses
    print("\n[+] Starting OneView Mock Server on port 8000...")
    ov_server = subprocess.Popen([sys.executable, "-m", "uvicorn", "main:app", "--port", "8000"], cwd="mock_server(oneview)", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    print("[+] Starting Compute Ops Mock Server on port 8001...")
    com_server = subprocess.Popen([sys.executable, "-m", "uvicorn", "main:app", "--port", "8001"], cwd="mock_server(Comops)", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    time.sleep(3) # Wait for servers to start
    
    try:
        # Step 1: Start from non authorized user show failure
        print("\n" + "="*50)
        print("STEP 1: NON-AUTHORIZED USER ACTION (EXPECT FAILURE)")
        print("="*50)
        logout()
        res1 = await manage_oneview_resource("turn on OV1-RackServer-001")
        print(f"Action: 'turn on OV1-RackServer-001'")
        print(f"Result:\n{res1}")
        
        # Step 2: Authorize using SSO
        print("\n" + "="*50)
        print("STEP 2: AUTHORIZE USING SSO")
        print("="*50)
        print("Triggering login (using local provider for automated demo)...")
        _trigger_login("local", username="devasksr", password="password123")
        res2 = check_access()
        print(f"Result:\n{res2}")

        # Step 3: Show executing commands and servers
        print("\n" + "="*50)
        print("STEP 3: SHOW REGISTRY (1000 OneView + 500 CoM)")
        print("="*50)
        res3 = await manage_oneview_resource("list all servers")
        print(f"Result:\n{res3}")
        
        # Step 4: Invoke power on, on both type of servers using different mcp tools
        print("\n" + "="*50)
        print("STEP 4: INVOKE POWER ON USING DIFFERENT MCP TOOLS")
        print("="*50)
        
        print("\n--- Tool 1: manage_oneview_resource ---")
        print("Query: 'power on OV1-RackServer-045'")
        ov_res = await manage_oneview_resource("power on OV1-RackServer-045")
        print(f"Result:\n{ov_res}")

        print("\n--- Tool: manage_comops_resource ---")
        print("Query: 'power on CoM-CloudNode-128'")
        com_res = await manage_comops_resource("power on CoM-CloudNode-128")
        print(f"Result:\n{com_res}")

        print("\n--- Tool: manage_comops_resource (list firmware-bundles) ---")
        print("Query: 'list all' with resource_category='firmware-bundles'")
        fw_res = await manage_comops_resource("list all", resource_category="firmware-bundles")
        print(f"Result:\n{fw_res}")

    finally:
        print("\n[+] Shutting down mock servers...")
        ov_server.terminate()
        com_server.terminate()
        print("✅ Demo Complete!")

if __name__ == "__main__":
    asyncio.run(main())
