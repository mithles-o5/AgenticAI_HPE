import sqlite3, json, httpx

# The data is in dynamic_rest_server_hardware. Let's find wan-r08-10017 specifically
conn = sqlite3.connect('d:/HPE CPP/MCP_Integrated/mock_server(oneview)/oneview_db.sqlite')
conn.row_factory = sqlite3.Row

# Find all wan-r08-100xx devices (close to wan-r08-10017)
print("=== Find wan-r08-100xx devices in dynamic_rest_server_hardware ===")
rows = conn.execute('SELECT * FROM "dynamic_rest_server_hardware" WHERE "serial_number" LIKE ?', ('wan-r08-100%',)).fetchall()
for row in rows:
    print(json.dumps(dict(row), default=str)[:400])

# Check the exact serial_number = wan-r08-10017
print("\n=== Exact: serial_number = wan-r08-10017 ===")
row = conn.execute('SELECT * FROM "dynamic_rest_server_hardware" WHERE "serial_number" = ?', ('wan-r08-10017',)).fetchone()
print(json.dumps(dict(row), default=str) if row else "NOT FOUND")

# Check by the source_device_id the postgres CMDB lookup would have
print("\n=== Check what source_device_id postgres says for wan-r08-10017 ===")
# We can't access postgres directly but check network mock DB which has entries
# Check the /rest/server-hardware endpoint for wan-r08-10017 member
r = httpx.get("http://127.0.0.1:8000/rest/server-hardware", timeout=10, params={"filter": "name='wan-r08-10017'"})
print("GET /rest/server-hardware?filter=name=... =>", r.status_code, r.text[:200])

# Look for the entry with serial_number wan-r08-10017 by scanning list response
data = httpx.get("http://127.0.0.1:8000/rest/server-hardware", timeout=10).json()
members = data.get("members", [])
for m in members:
    if "wan-r08-10017" in str(m).lower():
        print("FOUND in /rest/server-hardware:", json.dumps(m)[:400])

# Now try what url the agent is actually building for wan-r08-10017
# The management_source for wan routers is 'oneview', source_host is 'oneview-01.mgmt.local'
# The API path from endpoint_registry is /rest/server-hardware/{id}
# source_device_id is the UUID used as {id}
# We need to find wan-r08-10017's source_device_id

# From the CMDB data embedded in the SQLite, we know it's in dynamic_rest_server_hardware
# Let's find any row near index 10017
rows_all = conn.execute('SELECT serial_number, source_device_id, cpu_utilization_percent, memory_utilization_percent, power_draw_watts, temperature_celsius, power_state FROM "dynamic_rest_server_hardware" WHERE "serial_number" LIKE ? LIMIT 20', ('wan-r08%',)).fetchall()
print("\n=== wan-r08 devices and their metrics in DB ===")
for row in rows_all:
    print(json.dumps(dict(row), default=str))

conn.close()
