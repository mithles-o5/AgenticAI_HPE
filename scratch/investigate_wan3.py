import sqlite3, json, httpx

# ── Show ALL OneView tables matching "network" or "devices"
print("=== OneView tables containing 'network' or 'device' ===")
conn = sqlite3.connect('d:/HPE CPP/MCP_Integrated/mock_server(oneview)/oneview_db.sqlite')
conn.row_factory = sqlite3.Row
tables = [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
net_tables = [t for t in tables if 'network' in t or 'device' in t or 'server_hardware' in t]
for t in net_tables:
    print(f"  {t}")

# ── Scan ALL rows in ALL tables for wan
print("\n=== Scanning ALL tables for wan-r08 ===")
for t in tables:
    rows = conn.execute(f'SELECT * FROM "{t}"').fetchall()
    for row in rows:
        d = dict(row)
        vals = " ".join(str(v) for v in d.values()).lower()
        if "wan-r08" in vals or "10017" in vals:
            print(f"  [{t}]: {json.dumps(d, default=str)[:300]}")
conn.close()

# ── Check network mock DB path
import os, glob
print("\n=== Searching for .sqlite files in mock_server(network) ===")
for f in glob.glob('d:/HPE CPP/MCP_Integrated/mock_server(network)/*.sqlite'):
    print(f"  {f} ({os.path.getsize(f)} bytes)")
    conn2 = sqlite3.connect(f)
    conn2.row_factory = sqlite3.Row
    tables2 = [r[0] for r in conn2.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
    for t in tables2:
        rows = conn2.execute(f'SELECT * FROM "{t}"').fetchall()
        for row in rows:
            d = dict(row)
            vals = " ".join(str(v) for v in d.values()).lower()
            if "wan-r08" in vals or "10017" in vals or "coms" in vals:
                print(f"    [{t}] MATCH:", json.dumps(d, default=str)[:300])
    # Print first row of each table to understand schema
    print(f"  Tables: {tables2}")
    for t in tables2[:3]:
        first = conn2.execute(f'SELECT * FROM "{t}" LIMIT 1').fetchone()
        if first:
            print(f"    [{t}] sample:", json.dumps(dict(first), default=str)[:200])
    conn2.close()

# ── Check what the onprem_agent adapter calls
print("\n=== What does mock_adapter in onprem_agent call? ===")
try:
    r = httpx.get("http://127.0.0.1:8000/rest/server-hardware", timeout=5)
    print("/rest/server-hardware =>", r.status_code, "items:", len(r.json()) if isinstance(r.json(), list) else "not list")
except Exception as e:
    print(f"  Error: {e}")

# List what URLs are available on port 8000
try:
    r2 = httpx.get("http://127.0.0.1:8000/docs", timeout=5)
    print("/docs =>", r2.status_code)
except Exception as e:
    print(f"  /docs Error: {e}")
