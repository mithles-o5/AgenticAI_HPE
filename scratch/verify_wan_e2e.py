"""
Verify the full end-to-end flow for wan-r08-10017:
1. What source_device_id does the CMDB say for wan-r08-10017?
2. Does the mock server find it by that UUID?
3. What does the onprem_agent return?
"""
import sqlite3, json, httpx

# ── 1. Find source_device_id from the oneview DB ──────────────────────────────
DB = 'd:/HPE CPP/MCP_Integrated/mock_server(oneview)/oneview_db.sqlite'
TABLE = 'dynamic_rest_server_hardware'
conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row

row = conn.execute(f'SELECT * FROM "{TABLE}" WHERE serial_number = ?', ('wan-r08-10017',)).fetchone()
d = dict(row)
print("=== wan-r08-10017 from SQLite ===")
print(f"  id              = {d['id']}")
print(f"  source_device_id= {d['source_device_id']}")
print(f"  management_src  = {d['management_source']}")
print(f"  cpu             = {d['cpu_utilization_percent']}%")
print(f"  memory          = {d['memory_utilization_percent']}%")
print(f"  power           = {d['power_state']}")
print(f"  temp            = {d['temperature_celsius']}°C")
print(f"  power_draw      = {d['power_draw_watts']}W")
conn.close()

# ── 2. Test mock server lookup by source_device_id (UUID) ─────────────────────
print("\n=== Mock server lookup by source_device_id (UUID) ===")
source_uuid = d['source_device_id']
r = httpx.get(f"http://127.0.0.1:8000/rest/server-hardware/{source_uuid}", timeout=5)
print(f"  GET /rest/server-hardware/{source_uuid} => {r.status_code}")
if r.status_code == 200:
    rd = r.json()
    print(f"  Found: name={rd.get('name')} cpu={rd.get('cpu_utilization_percent')} power={rd.get('power_state')}")
else:
    print(f"  NOT FOUND: {r.text[:100]}")

# ── 3. Test mock server lookup by name ────────────────────────────────────────
print("\n=== Mock server lookup by name wan-r08-10017 ===")
r2 = httpx.get(f"http://127.0.0.1:8000/rest/server-hardware/wan-r08-10017", timeout=5)
print(f"  GET /rest/server-hardware/wan-r08-10017 => {r2.status_code}")
if r2.status_code == 200:
    rd2 = r2.json()
    print(f"  Found: name={rd2.get('name')} cpu={rd2.get('cpu_utilization_percent')} power={rd2.get('power_state')}")
else:
    print(f"  NOT FOUND: {r2.text[:100]}")

# ── 4. Check the CMDB resolver what source_device_id it uses ──────────────────
print("\n=== What does resource_resolver say about wan-r08-10017? ===")
try:
    r3 = httpx.get("http://127.0.0.1:8010/devices", timeout=5)
    data = r3.json()
    if isinstance(data, list):
        for item in data:
            if "wan-r08-10017" in str(item):
                print(f"  Found: {json.dumps(item, default=str)[:400]}")
    else:
        print(f"  Response type: {type(data)}, status: {r3.status_code}")
except Exception as e:
    print(f"  Error: {e}")

# ── 5. Test the onprem_agent directly ────────────────────────────────────────
print("\n=== Test onprem_agent task ===")
try:
    r4 = httpx.post(
        "http://127.0.0.1:8011/execute",
        json={
            "skill": "STATUS",
            "resource_type": "router",
            "resource_id": "wan-r08-10017",
            "provider": "coms",
            "parameters": {
                "api_path": "http://oneview-01.mgmt.local/rest/server-hardware/wan-r08-10017",
                "http_method": "GET"
            }
        },
        timeout=10
    )
    print(f"  POST /execute => {r4.status_code}")
    print(f"  Response: {r4.text[:400]}")
except Exception as e:
    print(f"  Error: {e}")
