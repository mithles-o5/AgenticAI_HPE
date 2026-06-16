"""
Test script: Call Compute Ops custom-servers via Server Agent proxy (port 8009).
This demonstrates the full CRUD flow:
  MCP -> Server Agent (:8009) -> Compute Ops Mock Server (:8001)
"""
import requests
import json
import sys

SERVER_AGENT_URL = "http://localhost:8009"
CUSTOM_SERVERS_ENDPOINT = f"{SERVER_AGENT_URL}/compute-ops-mgmt/v1/custom-servers"

def pretty(resp):
    print(f"  Status: {resp.status_code}")
    try:
        print(f"  Body:   {json.dumps(resp.json(), indent=2)}")
    except Exception:
        print(f"  Body:   {resp.text}")
    print()

# ── 1. LIST all custom servers (should be empty) ──
print("=" * 60)
print("1) GET  /compute-ops-mgmt/v1/custom-servers  (LIST)")
print("=" * 60)
resp = requests.get(CUSTOM_SERVERS_ENDPOINT)
pretty(resp)

# ── 2. CREATE a new custom server ──
print("=" * 60)
print("2) POST /compute-ops-mgmt/v1/custom-servers  (CREATE)")
print("=" * 60)
payload = {
    "name": "HPE-ProLiant-DL360",
    "status": "OK",
    "temperature": 32.5,
    "powerState": "On",
    "serialNumber": "SN-DL360-001",
    "firmwareVersion": "2.30",
    "memoryGiB": 256,
    "cpuCores": 64
}
resp = requests.post(CUSTOM_SERVERS_ENDPOINT, json=payload)
pretty(resp)
created = resp.json()
server_id = created.get("id")
print(f"  >> Created server ID: {server_id}\n")

# ── 3. GET the server by ID ──
print("=" * 60)
print(f"3) GET  /compute-ops-mgmt/v1/custom-servers/{server_id}  (READ)")
print("=" * 60)
resp = requests.get(f"{CUSTOM_SERVERS_ENDPOINT}/{server_id}")
pretty(resp)

# ── 4. UPDATE the server (change power state to Off) ──
print("=" * 60)
print(f"4) PUT  /compute-ops-mgmt/v1/custom-servers/{server_id}  (UPDATE)")
print("=" * 60)
update_payload = {
    "powerState": "Off",
    "temperature": 22.0
}
resp = requests.put(f"{CUSTOM_SERVERS_ENDPOINT}/{server_id}", json=update_payload)
pretty(resp)

# ── 5. LIST all custom servers (should now show 1) ──
print("=" * 60)
print("5) GET  /compute-ops-mgmt/v1/custom-servers  (LIST after create)")
print("=" * 60)
resp = requests.get(CUSTOM_SERVERS_ENDPOINT)
pretty(resp)

# ── 6. DELETE the server ──
print("=" * 60)
print(f"6) DELETE /compute-ops-mgmt/v1/custom-servers/{server_id}  (DELETE)")
print("=" * 60)
resp = requests.delete(f"{CUSTOM_SERVERS_ENDPOINT}/{server_id}")
pretty(resp)

# ── 7. LIST again (should be empty) ──
print("=" * 60)
print("7) GET  /compute-ops-mgmt/v1/custom-servers  (LIST after delete)")
print("=" * 60)
resp = requests.get(CUSTOM_SERVERS_ENDPOINT)
pretty(resp)

print("=" * 60)
print("ALL TESTS COMPLETE!")
print("=" * 60)
