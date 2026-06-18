import sys
import os


import asyncio
import subprocess
import time

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from mcp_server.mcp_server import (
    manage_oneview_resource,
    manage_comops_resource,
    manage_cloud_resource,
    manage_network_resource,
    manage_storage_resource,
    _trigger_login,
    logout,
    check_access,
)

AGENTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "agents")

async def main():
    print("=" * 60)
    print("HPE INTEGRATED MCP - FULL SYSTEM DEMO")
    print("=" * 60)

    # Start OASF Capability Registry first
    print("\n[+] Starting Capability Registry on port 8020...")
    cap_registry = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--port", "8020", "--log-level", "error"],
        cwd="capability_registry", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )

    # Start on-premises mock servers
    print("[+] Starting OneView Mock Server on port 8000...")
    ov_server = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--port", "8000", "--log-level", "error"],
        cwd="mock_server(oneview)", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )

    print("[+] Starting Compute Ops Mock Server on port 8001...")
    com_server = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--port", "8001", "--log-level", "error"],
        cwd="mock_server(Comops)", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )

    # Start Cloud and Storage Mock API servers
    print("[+] Starting Cloud Mock API Server on port 8003...")
    cloud_mock = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--port", "8003", "--log-level", "error"],
        cwd="mock_server(cloud)", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )

    print("[+] Starting Storage Mock API Server on port 8004...")
    storage_mock = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--port", "8004", "--log-level", "error"],
        cwd="mock_server(storage)", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )

    # Start OASF agent microservices
    print("[+] Starting Cloud Agent on port 8005...")
    cloud_proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--port", "8005", "--log-level", "error"],
        cwd=os.path.join(AGENTS_DIR, "cloud_agent"),
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    print("[+] Starting Network Agent on port 8006...")
    net_proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--port", "8006", "--log-level", "error"],
        cwd=os.path.join(AGENTS_DIR, "network_agent"),
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    print("[+] Starting Storage Agent on port 8007...")
    stor_proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--port", "8007", "--log-level", "error"],
        cwd=os.path.join(AGENTS_DIR, "storage_agent"),
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    print("[+] Starting On-Premise Agent on port 8008...")
    onprem_proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--port", "8008", "--log-level", "error"],
        cwd=os.path.join(AGENTS_DIR, "onprem_agent"),
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    print("[+] Starting Server Agent on port 8009...")
    server_proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--port", "8009", "--log-level", "error"],
        cwd=os.path.join(AGENTS_DIR, "server_agent"),
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )

    time.sleep(8)

    try:
        # ── Step 1: Unauthenticated call (expect failure) ─────────────────────
        print("\n" + "=" * 50)
        print("STEP 1: NON-AUTHORIZED USER ACTION (EXPECT FAILURE)")
        print("=" * 50)
        logout()
        res1 = await manage_oneview_resource("turn on OV1-RackServer-001")
        print(f"Result:\n{res1}")

        # ── Step 2: SSO Login ─────────────────────────────────────────────────
        print("\n" + "=" * 50)
        print("STEP 2: AUTHORIZE USING SSO")
        print("=" * 50)
        _trigger_login("local", username="devasksr", password="password123")
        res2 = check_access()
        print(f"Result:\n{res2}")

        # ── Step 3: OneView server command ────────────────────────────────────
        print("\n" + "=" * 50)
        print("STEP 3: ONEVIEW — POWER ON SERVER")
        print("=" * 50)
        ov_res = await manage_oneview_resource("power on OV1-RackServer-045")
        print(f"Result:\n{ov_res}")

        # ── Step 4: Compute Ops command ───────────────────────────────────────
        print("\n" + "=" * 50)
        print("STEP 4: COMPUTE OPS — POWER ON SERVER")
        print("=" * 50)
        com_res = await manage_comops_resource("power on CoM-CloudNode-128")
        print(f"Result:\n{com_res}")

        # ── Step 5: Cloud Agent ───────────────────────────────────────────────
        print("\n" + "=" * 50)
        print("STEP 5: CLOUD AGENT — STATUS OF VM")
        print("=" * 50)
        cloud_res = await manage_cloud_resource(
            "status of demo-vm-001", provider="mock", resource_type="vm"
        )
        print(f"Result:\n{cloud_res}")

        # ── Step 6: Network Agent ─────────────────────────────────────────────
        print("\n" + "=" * 50)
        print("STEP 6: NETWORK AGENT — DISCOVER TOPOLOGY")
        print("=" * 50)
        net_res = await manage_network_resource(
            "rescan core-switch-01", protocol="mock", resource_type="switch"
        )
        print(f"Result:\n{net_res}")

        # ── Step 7: Storage Agent ─────────────────────────────────────────────
        print("\n" + "=" * 50)
        print("STEP 7: STORAGE AGENT — CAPACITY CHECK")
        print("=" * 50)
        stor_res = await manage_storage_resource(
            "status of prod-vol-001", provider="mock", resource_type="volume"
        )
        print(f"Result:\n{stor_res}")

    finally:
        print("\n[+] Shutting down all servers and agents...")
        for proc in [ov_server, com_server, cloud_mock, storage_mock, cloud_proc, net_proc, stor_proc, onprem_proc, server_proc, cap_registry]:
            try:
                proc.terminate()
            except Exception:
                pass
        print("[OK] Demo complete!")

if __name__ == "__main__":
    asyncio.run(main())
