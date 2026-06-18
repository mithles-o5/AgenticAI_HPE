import sys
import os
import subprocess
import time

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
AGENTS_DIR = os.path.join(ROOT_DIR, "agents")

def main():
    print("=" * 60)
    print("STARTING ALL HPE MCP SERVICES & AGENTS")
    print("=" * 60)

    processes = []

    try:
        # 1. Start OASF Capability Registry
        print("\n[+] Starting Capability Registry on port 8020...")
        processes.append(subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "main:app", "--port", "8020", "--log-level", "error"],
            cwd=os.path.join(ROOT_DIR, "capability_registry")
        ))

        # 2. Start Mock Servers
        print("[+] Starting OneView Mock Server on port 8000...")
        processes.append(subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "main:app", "--port", "8000", "--log-level", "error"],
            cwd=os.path.join(ROOT_DIR, "mock_server(oneview)")
        ))

        print("[+] Starting Compute Ops Mock Server on port 8001...")
        processes.append(subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "main:app", "--port", "8001", "--log-level", "error"],
            cwd=os.path.join(ROOT_DIR, "mock_server(Comops)")
        ))

        print("[+] Starting Network Mock Server on port 8002...")
        processes.append(subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "main:app", "--port", "8002", "--log-level", "error"],
            cwd=os.path.join(ROOT_DIR, "mock_server(network)")
        ))

        print("[+] Starting Cloud Mock API Server on port 8003...")
        processes.append(subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "main:app", "--port", "8003", "--log-level", "error"],
            cwd=os.path.join(ROOT_DIR, "mock_server(cloud)")
        ))

        print("[+] Starting Storage Mock API Server on port 8004...")
        processes.append(subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "main:app", "--port", "8004", "--log-level", "error"],
            cwd=os.path.join(ROOT_DIR, "mock_server(storage)")
        ))

        # 3. Start OASF Agents
        print("[+] Starting Cloud Agent on port 8005...")
        processes.append(subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "main:app", "--port", "8005", "--log-level", "error"],
            cwd=os.path.join(AGENTS_DIR, "cloud_agent")
        ))

        print("[+] Starting Network Agent on port 8006...")
        processes.append(subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "main:app", "--port", "8006", "--log-level", "error"],
            cwd=os.path.join(AGENTS_DIR, "network_agent")
        ))

        print("[+] Starting Storage Agent on port 8007...")
        processes.append(subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "main:app", "--port", "8007", "--log-level", "error"],
            cwd=os.path.join(AGENTS_DIR, "storage_agent")
        ))

        print("[+] Starting On-Premise Agent on port 8008...")
        processes.append(subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "main:app", "--port", "8008", "--log-level", "error"],
            cwd=os.path.join(AGENTS_DIR, "onprem_agent")
        ))

        print("[+] Starting Server Agent on port 8009...")
        processes.append(subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "main:app", "--port", "8009", "--log-level", "error"],
            cwd=os.path.join(AGENTS_DIR, "server_agent")
        ))

        print("\n" + "=" * 60)
        print("✅ ALL SERVICES RUNNING SUCCESSFULLY!")
        print("You can now enter commands in your Claude app to test them.")
        print("Press Ctrl+C in this terminal window to stop all services.")
        print("=" * 60)

        # Keep running
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n[+] Shutting down all services...")
    finally:
        for proc in processes:
            try:
                proc.terminate()
            except Exception:
                pass
        print("[OK] All processes stopped.")

if __name__ == "__main__":
    main()
