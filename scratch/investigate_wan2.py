import sqlite3, json, httpx

# Check what table contains wan-r08-10017 and what the oneview DB has
print("=== OneView DB: dynamic_network_v1_devices rows ===")
conn = sqlite3.connect('d:/HPE CPP/MCP_Integrated/mock_server(oneview)/oneview_db.sqlite')
conn.row_factory = sqlite3.Row
rows = conn.execute('SELECT * FROM "dynamic_network_v1_devices"').fetchall()
for row in rows:
    d = dict(row)
    if "wan" in str(d).lower() or "10017" in str(d) or "r08" in str(d).lower() or "coms" in str(d).lower():
        print("  MATCH:", json.dumps(d, default=str))

print("\n=== ALL rows in dynamic_network_v1_devices (first 5) ===")
for row in rows[:5]:
    print(json.dumps(dict(row), default=str)[:200])

conn.close()

# Check mock_server(network) SQLite
print("\n\n=== mock_server(network) network_db.sqlite ===")
try:
    conn2 = sqlite3.connect('d:/HPE CPP/MCP_Integrated/mock_server(network)/network_db.sqlite')
    conn2.row_factory = sqlite3.Row
    tables2 = conn2.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    for t in tables2:
        print(f"  Table: {t['name']}")
        rows2 = conn2.execute(f'SELECT * FROM "{t["name"]}"').fetchall()
        for row in rows2:
            d = dict(row)
            if "wan" in str(d).lower() or "10017" in str(d) or "r08" in str(d).lower():
                print("    MATCH:", json.dumps(d, default=str)[:300])
    conn2.close()
except Exception as e:
    print(f"  Error: {e}")

# Check the live network mock server
print("\n=== Live network mock server calls ===")
try:
    r = httpx.get("http://127.0.0.1:8002/network/v1/devices", timeout=5)
    print("GET /network/v1/devices =>", r.status_code)
    data = r.json()
    if isinstance(data, list):
        for item in data:
            if "wan" in str(item).lower() or "10017" in str(item) or "r08" in str(item).lower():
                print("  MATCH:", json.dumps(item, default=str)[:300])
        print(f"  Total devices: {len(data)}")
    else:
        print("  Response:", str(data)[:200])
except Exception as e:
    print(f"  Error: {e}")

try:
    r2 = httpx.get("http://127.0.0.1:8002/network/v1/devices/wan-r08-10017", timeout=5)
    print("GET /network/v1/devices/wan-r08-10017 =>", r2.status_code, r2.text[:300])
except Exception as e:
    print(f"  Error: {e}")
