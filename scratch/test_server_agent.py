import httpx
import json

url = "http://localhost:8009/server-agent/execute-task"
payload = {
  "task_id": "manual-server-status",
  "task_type": "operational",
  "agent_type": "server",
  "resource_type": "server",
  "resource_id": "OV1-RackServer-001",
  "provider": "redfish",
  "action": "fetch_metrics",
  "parameters": {
    "api_path": "/rest/server-hardware/{id}",
    "user_email": "mithles@student.tce.edu"
  },
  "credentials_ref": "mock"
}

def test():
    try:
        resp = httpx.post(url, json=payload, timeout=10.0)
        print(f"Status Code: {resp.status_code}")
        print("Response Text:")
        print(resp.text)
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    test()
