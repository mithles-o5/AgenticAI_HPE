import sqlite3, json, httpx

# Find wan-r08-10017 specifically in the oneview server_hardware table
conn = sqlite3.connect('d:/HPE CPP/MCP_Integrated/mock_server(oneview)/oneview_db.sqlite')
conn.row_factory = sqlite3.Row

print("=== Searching for wan-r08-10017 in dynamic_rest_server_hardware ===")
rows = conn.execute('SELECT * FROM "dynamic_rest_server_hardware" WHERE "serial_number" = ? OR "name" = ? OR "id" = ?',
                    ('wan-r08-10017', 'wan-r08-10017', 'wan-r08-10017')).fetchall()
for row in rows:
    print(json.dumps(dict(row), default=str))

print("\n=== Searching by source_device_id pattern ===")
rows2 = conn.execute('SELECT id, serial_number, name, management_source, source_device_id, device_type, power_state, cpu_utilization_percent FROM "dynamic_rest_server_hardware" WHERE "device_type" = ? LIMIT 5',
                    ('router',)).fetchall()
for row in rows2:
    print(json.dumps(dict(row), default=str))

print("\n=== Check device_type values ===")
types = conn.execute('SELECT DISTINCT device_type FROM "dynamic_rest_server_hardware"').fetchall()
print("Types:", [r[0] for r in types])

# Check the management_source for wan devices
print("\n=== wan-r08 devices - what's their management_source? ===")
rows3 = conn.execute('SELECT serial_number, management_source, source_host, source_device_id, device_type, cpu_utilization_percent FROM "dynamic_rest_server_hardware" WHERE "serial_number" LIKE ? LIMIT 3',
                    ('wan-r08%',)).fetchall()
for row in rows3:
    print(json.dumps(dict(row), default=str))

conn.close()

# Now find wan-r08-10017 specifically
print("\n=== Query the endpoint for wan-r08-10017 ===")
# Try by serial_number
try:
    r = httpx.get("http://127.0.0.1:8000/rest/server-hardware/wan-r08-10017", timeout=5)
    print("GET /rest/server-hardware/wan-r08-10017 =>", r.status_code, r.text[:200])
except Exception as e:
    print(f"  Error: {e}")

# Try listing all and finding it  
try:
    r2 = httpx.get("http://127.0.0.1:8000/rest/server-hardware", timeout=5)
    data = r2.json()
    items = data.get("members", []) if isinstance(data, dict) else data
    print(f"\nTotal server-hardware items: {len(items)}")
    for item in items:
        if "wan-r08-10017" in str(item):
            print("FOUND:", json.dumps(item, default=str)[:400])
            break
    # Show first item schema
    if items:
        print("First item keys:", list(items[0].keys()) if isinstance(items[0], dict) else "not dict")
except Exception as e:
    print(f"  Error listing: {e}")
