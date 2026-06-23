import subprocess
import time
import httpx
import sys
import os

def main():
    print("==================================================")
    print("RUNNING END-TO-END AGENT VERIFICATION")
    print("==================================================")

    # Resolve project root dir
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    print(f"Project root directory: {root_dir}")

    # Spin up mock servers and agent
    print("[+] Starting OneView Mock Server on port 8000...")
    ov_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--port", "8000"],
        cwd=os.path.join(root_dir, "mock_server(oneview)"),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    print("[+] Starting On-Prem Agent Microservice on port 8008...")
    agent_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--port", "8008"],
        cwd=os.path.join(root_dir, "agents", "onprem_agent"),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    # Allow servers 4 seconds to bind and initialize
    time.sleep(4)

    try:
        # Test 1: Health Check OneView Server
        print("\n[Test 1] Health Check OneView Server:")
        payload = {
            "task_id": "manual-task-1",
            "task_type": "monitoring",
            "agent_type": "onprem",
            "resource_type": "server_hardware",
            "resource_id": "OV1-RackServer-001",
            "provider": "oneview",
            "action": "health_check"
        }
        resp = httpx.post("http://localhost:8008/tasks", json=payload, timeout=10.0)
        print(f"Status Code: {resp.status_code}")
        print(f"Response:\n{resp.text}\n")
        assert resp.status_code == 200
        assert resp.json()["status"] == "success"

        # Test 4: Execute Power Action OV
        print("[Test 4] Power Action OneView Server:")
        payload = {
            "task_id": "manual-task-4",
            "task_type": "lifecycle",
            "agent_type": "onprem",
            "resource_type": "server_hardware",
            "resource_id": "OV1-RackServer-045",
            "provider": "oneview",
            "action": "execute_action",
            "parameters": {"action_type": "power", "state": "On"}
        }
        resp = httpx.post("http://localhost:8008/tasks", json=payload, timeout=10.0)
        print(f"Status Code: {resp.status_code}")
        print(f"Response:\n{resp.text}\n")
        assert resp.status_code == 200
        assert resp.json()["actions_taken"] == ["power_on"]

        # Test 5: Verify default provider error block
        print("[Test 5] Verify default/missing provider error block:")
        payload = {
            "task_id": "manual-task-5",
            "task_type": "monitoring",
            "agent_type": "onprem",
            "resource_type": "server_hardware",
            "resource_id": "OV1-RackServer-001",
            "provider": "default",
            "action": "health_check"
        }
        resp = httpx.post("http://localhost:8008/tasks", json=payload, timeout=10.0)
        print(f"Status Code: {resp.status_code}")
        print(f"Response:\n{resp.text}\n")
        assert resp.status_code == 200
        assert resp.json()["status"] == "failed"
        assert "Provider must be supplied" in resp.json()["errors"][0]

        print("==================================================")
        print("VERIFICATION COMPLETE: ALL INTEGRATION TESTS PASSED")
        print("==================================================")

    except Exception as e:
        print(f"Verification encountered error: {e}")
        sys.exit(1)
    finally:
        print("[+] Shutting down backend processes and agent...")
        ov_process.terminate()
        agent_process.terminate()
        print("[+] Cleanup complete.")

if __name__ == "__main__":
    main()
