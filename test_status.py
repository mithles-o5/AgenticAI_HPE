"""Quick smoke test — inject a local token and call all five MCP tools."""
import sys
import os
import mock_db_cache
mock_db_cache.setup()

import asyncio
import subprocess
import time

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from mcp_server.mcp_server import (
    manage_oneview_resource,
    manage_comops_resource,
    manage_cloud_resource,
    manage_network_resource,
    manage_storage_resource,
    manage_server_resource,
    _trigger_login,
)

AGENTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "agents")


async def main():
    # Authorize using local SSO
    _trigger_login("local", username="devasksr", password="password123")

    # Start mock servers and OASF agent microservices
    procs = []
    
    # 0. Capability Registry
    cap_proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--port", "8020", "--log-level", "error"],
        cwd="capability_registry",
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    procs.append(cap_proc)

    # On-premises mock servers
    for name, port, cwd in [
        ("oneview", 8000, os.path.join("generator", "servers", "oneview")),
        ("coms", 8001, os.path.join("generator", "servers", "compute_ops"))
    ]:
        proc = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "main:app", "--port", str(port), "--log-level", "error"],
            cwd=cwd,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        procs.append(proc)

    # OASF agents
    for name, port in [("cloud_agent", 8005), ("network_agent", 8006), ("storage_agent", 8007), ("onprem_agent", 8008), ("server_agent", 8009)]:
        proc = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "main:app", "--port", str(port), "--log-level", "error"],
            cwd=os.path.join(AGENTS_DIR, name),
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        procs.append(proc)
        
    time.sleep(8)

    try:
        print("\n--- [1] Status: OneView Server ---")
        print(await manage_oneview_resource("status OV1-RackServer-001"))

        print("\n--- [2] Status: ComOps Server ---")
        print(await manage_comops_resource("status CoM-CloudNode-001"))

        print("\n--- [3] Status: Cloud VM ---")
        print(await manage_cloud_resource("status demo-vm-001", provider="mock", resource_type="vm"))

        print("\n--- [4] Metrics: Network Switch ---")
        print(await manage_network_resource("status core-sw-01", protocol="mock", resource_type="switch"))

        print("\n--- [5] Capacity: Storage Volume ---")
        print(await manage_storage_resource("status prod-vol-001", provider="mock", resource_type="volume"))

        print("\n--- [6] Status: Bare-metal Server ---")
        print(await manage_server_resource("status OV1-RackServer-001", provider="mock", resource_type="server"))

    finally:
        for proc in procs:
            proc.terminate()
        print("\n[OK] Smoke test complete.")


if __name__ == "__main__":
    asyncio.run(main())
