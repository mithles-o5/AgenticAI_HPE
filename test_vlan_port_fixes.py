"""
Live validation tests for VLAN add and port status persistence.
Run AFTER the network mock server is started on port 8002.
"""
import httpx
import json
import sys

BASE = "http://127.0.0.1:8002"

def hdr(title):
    print(f"\n{'='*65}")
    print(f"  {title}")
    print('='*65)

def get_device(dev_id):
    r = httpx.get(f"{BASE}/network/v1/devices/{dev_id}", timeout=5)
    r.raise_for_status()
    return r.json()

DEVICE = "aruba-cx-017"
passed = 0
failed = 0

# ── 1. Add VLAN 200 "Production" ─────────────────────────────────────────────
hdr("TEST 1: Add VLAN 200 'Production'")
r = httpx.post(
    f"{BASE}/network/v1/devices/{DEVICE}/vlans",
    json={"vlan_id": 200, "name": "Production"},
    timeout=5
)
print(f"  POST status: {r.status_code}")
resp = r.json()
print(f"  configured_vlans in response: {resp.get('configured_vlans')}")

# Verify it persisted
dev = get_device(DEVICE)
vlans = dev.get("configured_vlans") or []
if isinstance(vlans, str):
    vlans = json.loads(vlans)
vlan_ids = [v.get("vlan_id") if isinstance(v, dict) else v for v in vlans]
ok = 200 in vlan_ids
print(f"  VLAN IDs stored: {vlan_ids}")
print(f"  VLAN 200 persisted? {'✅ YES' if ok else '❌ NO'}")
if ok: passed += 1
else: failed += 1

# ── 2. Add another VLAN to same device and check both are there ───────────────
hdr("TEST 2: Add VLAN 300 'Backup' (cumulative, both 200 and 300 must exist)")
httpx.post(f"{BASE}/network/v1/devices/{DEVICE}/vlans",
           json={"vlan_id": 300, "name": "Backup"}, timeout=5)
dev = get_device(DEVICE)
vlans2 = dev.get("configured_vlans") or []
if isinstance(vlans2, str):
    vlans2 = json.loads(vlans2)
ids2 = [v.get("vlan_id") if isinstance(v, dict) else v for v in vlans2]
ok2 = (200 in ids2) and (300 in ids2)
print(f"  VLAN IDs stored: {ids2}")
print(f"  Both 200 & 300 present? {'✅ YES' if ok2 else '❌ NO'}")
if ok2: passed += 1
else: failed += 1

# ── 3. GET /network/v1/devices/{id}/vlans endpoint ─────────────────────────────
hdr("TEST 3: GET /network/v1/devices/{id}/vlans returns VLAN list")
r3 = httpx.get(f"{BASE}/network/v1/devices/{DEVICE}/vlans", timeout=5)
print(f"  GET status: {r3.status_code}")
data3 = r3.json()
print(f"  Response: {data3}")
ok3 = r3.status_code == 200 and isinstance(data3.get("configured_vlans"), list)
print(f"  VLAN GET works? {'✅ YES' if ok3 else '❌ NO'}")
if ok3: passed += 1
else: failed += 1

# ── 4. Bring port UP (with slash in name) ─────────────────────────────────────
hdr("TEST 4: Bring port GigabitEthernet1/0/3 UP")
# First check current state
dev_before = get_device(DEVICE)
ports_before = dev_before.get("ports") or {}
if isinstance(ports_before, str):
    ports_before = json.loads(ports_before)
print(f"  Port state before: {ports_before.get('GigabitEthernet1/0/3')}")

# Post the status change
r4 = httpx.post(
    f"{BASE}/network/v1/devices/{DEVICE}/ports/GigabitEthernet1/0/3/status",
    json={"status": "UP"},
    timeout=5
)
print(f"  POST status: {r4.status_code}")
resp4 = r4.json()
ports_in_resp = resp4.get("ports") or {}
if isinstance(ports_in_resp, str):
    ports_in_resp = json.loads(ports_in_resp)
print(f"  Port in response: GigabitEthernet1/0/3 = {ports_in_resp.get('GigabitEthernet1/0/3')}")

# Verify persistence via GET
dev_after = get_device(DEVICE)
ports_after = dev_after.get("ports") or {}
if isinstance(ports_after, str):
    ports_after = json.loads(ports_after)
ok4 = ports_after.get("GigabitEthernet1/0/3") == "UP"
print(f"  Port state after GET: {ports_after.get('GigabitEthernet1/0/3')}")
print(f"  Port UP persisted? {'✅ YES' if ok4 else '❌ NO'}")
if ok4: passed += 1
else: failed += 1

# ── 5. Bring port DOWN ────────────────────────────────────────────────────────
hdr("TEST 5: Bring port GigabitEthernet1/0/3 DOWN")
r5 = httpx.post(
    f"{BASE}/network/v1/devices/{DEVICE}/ports/GigabitEthernet1/0/3/status",
    json={"status": "DOWN"},
    timeout=5
)
dev5 = get_device(DEVICE)
ports5 = dev5.get("ports") or {}
if isinstance(ports5, str):
    ports5 = json.loads(ports5)
ok5 = ports5.get("GigabitEthernet1/0/3") == "DOWN"
print(f"  Port state: {ports5.get('GigabitEthernet1/0/3')}")
print(f"  Port DOWN persisted? {'✅ YES' if ok5 else '❌ NO'}")
if ok5: passed += 1
else: failed += 1

# ── 6. Bring port back UP (via Aruba monitoring endpoint) ─────────────────────
hdr("TEST 6: Aruba monitoring endpoint port status (/monitoring/v1/switches)")
r6 = httpx.post(
    f"{BASE}/monitoring/v1/switches/{DEVICE}/ports/GigabitEthernet1/0/3/status",
    json={"status": "UP"},
    timeout=5
)
print(f"  POST status: {r6.status_code}")
dev6 = get_device(DEVICE)
ports6 = dev6.get("ports") or {}
if isinstance(ports6, str):
    ports6 = json.loads(ports6)
ok6 = ports6.get("GigabitEthernet1/0/3") == "UP"
print(f"  Port state via monitoring endpoint: {ports6.get('GigabitEthernet1/0/3')}")
print(f"  Port UP via Aruba endpoint? {'✅ YES' if ok6 else '❌ NO'}")
if ok6: passed += 1
else: failed += 1

print(f"\n{'='*65}")
print(f"  RESULTS: {passed}/{passed+failed} passed  |  {failed} failed")
print(f"{'='*65}")
sys.exit(0 if failed == 0 else 1)
