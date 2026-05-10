import httpx
import time
import subprocess
import os
from utils import DEMO_TOKENS

def test_flow():
    print("Starting Unified Backend...")
    # Start the server in a separate process
    server_process = subprocess.Popen(
        ["python", "main.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    time.sleep(3) # Wait for server to boot
    
    try:
        # 1. Test List Servers (Operator - Should Pass in Dev)
        print("\n[TEST 1] Operator listing servers (Dev environment)...")
        token = DEMO_TOKENS["operator"]
        # In a real MCP call, this would go through the MCP tool which calls the API.
        # Here we'll simulate the tool's check logic or hit the API if we had the auth header logic there.
        # Since the API itself isn't protected (only the MCP tools are), we'll test the MCP tools
        # by calling a helper that uses the same logic.
        
        from mcp_server import _authorize
        import asyncio

        async def check_auth(token, action, env):
            allowed, reason, trace = await _authorize(token, action, "server01", env, "HPE", "12:00")
            print(f"Action: {action}, Env: {env}, Allowed: {allowed}, Reason: {reason}")
            return allowed

        loop = asyncio.get_event_loop()
        
        # Operator wants to power_on in dev (Map to restart)
        # RBAC: operator has ["view", "monitor", "start"]. 
        # Wait, 'start' isn't mapped in ACTION_MAP or RBAC doesn't allow 'restart' for operator.
        # RBAC: operator only allows ["view", "monitor", "start"]. 
        # ACTION_MAP maps power_on to 'restart'.
        # So Operator should be DENIED power_on.
        loop.run_until_complete(check_auth(DEMO_TOKENS["operator"], "power_on", "dev"))

        # Admin wants to power_on in dev (Map to restart)
        # RBAC: admin has ["restart", "view", "shutdown", "create"].
        # PBAC: admin allows restart if env != production.
        # Should ALLOW.
        loop.run_until_complete(check_auth(DEMO_TOKENS["admin"], "power_on", "dev"))

        # Admin wants to power_on in production (Map to restart)
        # ABAC: production restricted to senior_admin.
        # PBAC: admin restricted from restart in production.
        # Should DENY.
        loop.run_until_complete(check_auth(DEMO_TOKENS["admin"], "power_on", "production"))

        # Senior Admin wants to power_on in production
        # Should ALLOW.
        loop.run_until_complete(check_auth(DEMO_TOKENS["senior_admin"], "power_on", "production"))

    finally:
        print("\nShutting down server...")
        server_process.terminate()

if __name__ == "__main__":
    test_flow()
