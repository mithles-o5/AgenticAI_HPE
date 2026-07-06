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
    elif management_source in ("storage", "mock_storage"):
        parts = api_path.strip("/").split("/")
        if len(parts) >= 4 and parts[0] == "data-services":
            dt = parts[3]
    elif management_source in ("cloud", "mock_cloud"):
        parts = api_path.strip("/").split("/")
        if len(parts) >= 4 and parts[0] == "api":
            dt = parts[3]
    else:
        parts = api_path.strip("/").split("/")
        if len(parts) >= 3 and parts[0] == "redfish":
            dt = parts[2]
        elif len(parts) > 0:
            dt = parts[-1]
    return dt.lower()

conn = db_manager.get_connection()
cur = conn.cursor()
cur.execute("SELECT DISTINCT management_source, api_path, device_type FROM endpoint_registry ORDER BY management_source, api_path;")
mapping_groups = {}
for mgmt, path, cmdb_dt in cur.fetchall():
    extracted = _extract_dt(path, mgmt)
    key = f"{mgmt} | {extracted}"
    if key not in mapping_groups:
        mapping_groups[key] = set()
    mapping_groups[key].add(cmdb_dt)

for k, v in mapping_groups.items():
    print(f"{k.ljust(40)} -> {v}")
