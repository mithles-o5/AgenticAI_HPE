import sqlite3, json, httpx, glob, os

# ── Show where wan-r08-10017 actually lives (resource_resolver cmdb context)
print("=== Check resource resolver CMDB info via API ===")
try:
    r = httpx.get("http://127.0.0.1:8010/resolve", params={"identifier": "wan-r08-10017", "action": "STATUS"}, timeout=5)
    print("Resolver =>", r.status_code, r.text[:500])
except Exception as e:
    print(f"  Error: {e}")

# Check from capability registry what agent handles coms
try:
    r2 = httpx.get("http://127.0.0.1:8020/agents/lookup", params={"provider": "coms"}, timeout=5)
    print("\nCapability registry coms =>", r2.status_code, r2.text[:300])
except Exception as e:
    print(f"  Error: {e}")

# ── Check the network_db.sqlite in mock_server(network)
print("\n=== mock_server(network) .sqlite files ===")
net_path = "d:/HPE CPP/MCP_Integrated/mock_server(network)"
for f in glob.glob(f"{net_path}/*.sqlite"):
    print(f"  File: {f} ({os.path.getsize(f)} bytes)")

# ── Check ALL .sqlite files for wan-r08
print("\n=== Search ALL sqlite files for wan-r08-10017 ===")
base = "d:/HPE CPP/MCP_Integrated"
for f in glob.glob(f"{base}/**/*.sqlite", recursive=True):
    try:
        conn = sqlite3.connect(f)
        conn.row_factory = sqlite3.Row
        tables = [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
        for t in tables:
            rows = conn.execute(f'SELECT * FROM "{t}"').fetchall()
            for row in rows:
                d = dict(row)
                vals = " ".join(str(v) for v in d.values()).lower()
                if "wan-r08" in vals or "r08" in vals:
                    print(f"\n  FILE: {f}")
                    print(f"  TABLE: {t}")
                    print(f"  ROW: {json.dumps(d, default=str)[:400]}")
        conn.close()
    except:
        pass

# ── Show the resource resolver's device details for wan-r08-10017
print("\n=== Live API: resolve wan-r08-10017 ===")
try:
    r3 = httpx.get("http://127.0.0.1:8010/devices/wan-r08-10017", timeout=5)
    print("=>", r3.status_code, r3.text[:500])
except Exception as e:
    print(f"  Error: {e}")

# ── What URL does onprem_agent actually build for wan-r08-10017?
# Get the management_source, source_host, source_device_id from any DB
print("\n=== Check device details via all mock servers on port 8000 ===")
for url in [
    "http://127.0.0.1:8000/rest/server-hardware",
    "http://127.0.0.1:8002/network/v1/devices",
]:
    try:
        r4 = httpx.get(url, timeout=5)
        data = r4.json()
        items = data if isinstance(data, list) else data.get("members", [])
        matches = [i for i in items if "wan-r08" in str(i).lower() or "r08" in str(i).lower()]
        print(f"\n{url} => {r4.status_code}, {len(items)} items, {len(matches)} matches")
        for m in matches:
            print("  MATCH:", json.dumps(m, default=str)[:300])
    except Exception as e:
        print(f"  {url} Error: {e}")
