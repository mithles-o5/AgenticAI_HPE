import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, r"c:\AgenticAI_HPE\resource_resolver")
from db import db_manager

def _extract_dt(api_path: str, management_source: str) -> str:
    management_source = management_source.lower()
    dt = "generic"
    if management_source == "oneview":
        parts = api_path.strip("/").split("/")
        if len(parts) >= 2 and parts[0] == "rest":
            dt = parts[1]
    elif management_source in ("network", "mock_network"):
        parts = api_path.strip("/").split("/")
        if len(parts) >= 4 and parts[0] == "v1":
            dt = parts[3]
        elif len(parts) > 0:
            dt = parts[-1]
    return dt.lower()

conn = db_manager.get_connection()
cur = conn.cursor()
cur.execute("SELECT DISTINCT api_path FROM endpoint_registry WHERE management_source IN ('network', 'mock_network');")
paths = [r[0] for r in cur.fetchall()]

dts = set()
for p in paths:
    dts.add(_extract_dt(p, "network"))

for dt in sorted(dts):
    print(dt)
