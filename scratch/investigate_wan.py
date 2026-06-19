import sqlite3, json

# ── 1. Check OneView DB tables ────────────────────────────────────────────────
conn = sqlite3.connect('d:/HPE CPP/MCP_Integrated/mock_server(oneview)/oneview_db.sqlite')
conn.row_factory = sqlite3.Row
tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
print("=== OneView SQLite tables ===")
for t in tables:
    print(" ", t["name"])

# ── 2. Look for wan-r08-10017 in ALL tables ───────────────────────────────────
print("\n=== Searching for wan-r08-10017 in every table ===")
for t in tables:
    rows = conn.execute(f'SELECT * FROM "{t["name"]}"').fetchall()
    for row in rows:
        d = dict(row)
        if any("wan" in str(v).lower() or "10017" in str(v) for v in d.values()):
            print(f"  Found in [{t['name']}]:", json.dumps(d, default=str)[:300])

conn.close()

# ── 3. Check network mock DB ──────────────────────────────────────────────────
try:
    conn2 = sqlite3.connect('d:/HPE CPP/MCP_Integrated/mock_server(network)/network_db.sqlite')
    conn2.row_factory = sqlite3.Row
    tables2 = conn2.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    print("\n=== Network SQLite tables ===")
    for t in tables2:
        print(" ", t["name"])
    print("\n=== Searching for wan-r08-10017 ===")
    for t in tables2:
        rows = conn2.execute(f'SELECT * FROM "{t["name"]}"').fetchall()
        for row in rows:
            d = dict(row)
            if any("wan" in str(v).lower() or "10017" in str(v) for v in d.values()):
                print(f"  Found in [{t['name']}]:", json.dumps(d, default=str)[:300])
    conn2.close()
except Exception as e:
    print(f"\n[Network DB error]: {e}")

# ── 4. Check what the API returns live for wan-r08-10017 ──────────────────────
import httpx
print("\n=== Live API call to OneView mock server ===")
try:
    r = httpx.get("http://127.0.0.1:8000/api/v1/resources", timeout=5)
    print("GET /api/v1/resources =>", r.status_code)
    data = r.json()
    if isinstance(data, list):
        for item in data:
            if "wan" in str(item).lower() or "10017" in str(item):
                print("  Found:", json.dumps(item, default=str)[:300])
except Exception as e:
    print(f"  Error: {e}")

try:
    r2 = httpx.get("http://127.0.0.1:8000/api/v1/resources/wan-r08-10017", timeout=5)
    print("GET /api/v1/resources/wan-r08-10017 =>", r2.status_code, r2.text[:300])
except Exception as e:
    print(f"  Error: {e}")
