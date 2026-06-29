"""End-to-end power cycle test for OneView mock server + onprem_agent."""
import requests

BASE = "http://127.0.0.1:8000"
AGENT = "http://127.0.0.1:8008"
ID   = "agg-sw02-1"

def check_db(label):
    r = requests.get(f"{BASE}/rest/server-hardware/{ID}", timeout=5)
    d = r.json()
    print(f"[{label}] power_state={d.get('power_state')} cpu={d.get('cpu_utilization_percent')} mem={d.get('memory_utilization_percent')} power_draw={d.get('power_draw_watts')}")
    return d

# --- Direct mock server tests ---
print("=== Direct Mock Server Tests ===")

# Power OFF via mock
r = requests.put(f"{BASE}/rest/server-hardware/{ID}/powerState", json={"powerState": "Off"}, timeout=5)
print(f"[PUT powerState=Off] HTTP {r.status_code}")
check_db("VERIFY OFF")

# Power ON via mock
r = requests.put(f"{BASE}/rest/server-hardware/{ID}/powerState", json={"powerState": "On"}, timeout=5)
print(f"[PUT powerState=On] HTTP {r.status_code}")
d = check_db("VERIFY ON")

mock_works = d.get("power_state") == "ON" and float(d.get("cpu_utilization_percent") or 0) > 0
print(f"\nMock server power cycle: {'PASS' if mock_works else 'FAIL'}")

# --- Test onprem agent execute_action directly ---
print("\n=== Onprem Agent Tests ===")

import uuid

# Test turn_off via agent
payload_off = {
    "task_id": str(uuid.uuid4()),
    "task_type": "operational",
    "agent_type": "onprem",
    "resource_type": "server",
    "resource_id": ID,
    "provider": "oneview",
    "action": "execute_action",
    "parameters": {
        "action_type": "power",
        "action_verb": "turn_off",
        "state": "Off"
    }
}
r = requests.post(f"{AGENT}/tasks", json=payload_off, timeout=10)
print(f"[Agent turn_off] HTTP {r.status_code}: {r.json().get('status')} actions={r.json().get('actions_taken')}")
check_db("AFTER AGENT TURN_OFF")

# Test turn_on via agent
payload_on = {
    "task_id": str(uuid.uuid4()),
    "task_type": "operational",
    "agent_type": "onprem",
    "resource_type": "server",
    "resource_id": ID,
    "provider": "oneview",
    "action": "execute_action",
    "parameters": {
        "action_type": "power",
        "action_verb": "turn_on",
        "state": "On"
    }
}
r = requests.post(f"{AGENT}/tasks", json=payload_on, timeout=10)
print(f"[Agent turn_on] HTTP {r.status_code}: {r.json().get('status')} actions={r.json().get('actions_taken')}")
d = check_db("AFTER AGENT TURN_ON")

agent_works = d.get("power_state") == "ON" and float(d.get("cpu_utilization_percent") or 0) > 0
print(f"\nAgent power cycle: {'PASS' if agent_works else 'FAIL'}")

if mock_works and agent_works:
    print("\n✅ ALL TESTS PASSED — Power ON/OFF works end-to-end!")
else:
    print("\n❌ SOME TESTS FAILED")
