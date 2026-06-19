"""
End-to-end verification:
1. What does compute_ops_db.sqlite have for wan-r08-10017?
2. What does the ComOps mock server return via HTTP?
3. Do the values match?
"""
import sqlite3, json, httpx

DB = 'd:/HPE CPP/MCP_Integrated/mock_server(Comops)/compute_ops_db.sqlite'
TABLE = 'dynamic_compute_ops_mgmt_v1_devices'

# ── 1. Ground truth from SQLite ───────────────────────────────────────────────
print("=== SQLite ground truth ===")
conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
row = conn.execute(
    f'SELECT serial_number, power_state, health_status, '
    f'cpu_utilization_percent, memory_utilization_percent, '
    f'power_draw_watts, temperature_celsius '
    f'FROM "{TABLE}" WHERE serial_number = ?',
    ('wan-r08-10017',)
).fetchone()
conn.close()

if row:
    sqlite_data = dict(row)
    print(json.dumps(sqlite_data, default=str))
else:
    print("ERROR: not found in SQLite!")
    exit(1)

# ── 2. What mock server returns ───────────────────────────────────────────────
print("\n=== Mock server HTTP response ===")
r = httpx.get('http://127.0.0.1:8001/compute-ops-mgmt/v1/devices/wan-r08-10017', timeout=5)
print(f"Status: {r.status_code}")
if r.status_code == 200:
    api_data = r.json()
    print(f"  cpu_utilization_percent:    {api_data.get('cpu_utilization_percent')}")
    print(f"  memory_utilization_percent: {api_data.get('memory_utilization_percent')}")
    print(f"  power_draw_watts:           {api_data.get('power_draw_watts')}")
    print(f"  temperature_celsius:        {api_data.get('temperature_celsius')}")
    print(f"  power_state:                {api_data.get('power_state')}")
    print(f"  health_status:              {api_data.get('health_status')}")
else:
    print(f"  Error: {r.text[:200]}")
    exit(1)

# ── 3. Compare ────────────────────────────────────────────────────────────────
print("\n=== Match check ===")
fields = ['cpu_utilization_percent', 'memory_utilization_percent',
          'power_draw_watts', 'temperature_celsius', 'power_state']
all_match = True
for f in fields:
    sqlite_val = sqlite_data.get(f)
    api_val = api_data.get(f)
    # Compare as floats where possible
    try:
        match = abs(float(sqlite_val) - float(api_val)) < 0.01
    except (TypeError, ValueError):
        match = str(sqlite_val).upper() == str(api_val).upper()
    status = "✅" if match else "❌"
    print(f"  {status} {f}: SQLite={sqlite_val} | API={api_val}")
    if not match:
        all_match = False

print(f"\n{'✅ All values match!' if all_match else '❌ MISMATCH DETECTED!'}")

# ── 4. Simulate what com_adapter.fetch_metrics() will return ──────────────────
print("\n=== Simulated com_adapter.fetch_metrics() output ===")
metrics = {
    "cpu_utilization_percent": float(api_data.get("cpu_utilization_percent") or 0.0),
    "memory_utilization_percent": float(api_data.get("memory_utilization_percent") or 0.0),
    "power_draw_watts": float(api_data.get("power_draw_watts") or 0.0),
    "temperature_celsius": float(api_data.get("temperature_celsius") or 0.0),
    "power_state": api_data.get("power_state", "Unknown"),
}
print(json.dumps(metrics, indent=2))
