
import sys
import json
import logging
sys.path.insert(0, r"c:\AgenticAI_HPE\resource_resolver")
from resolver import ResourceResolver
from registry import ResourceRegistry
from cache import ResourceCache
from query_agent import QueryAgent
from db import db_manager
from dataclasses import asdict

logging.getLogger().setLevel(logging.CRITICAL)

sources = ["oneview", "mock_network", "comops", "mock_server", "mock_storage"]
devices = {}
for src in sources:
    row = db_manager.execute_query(f"SELECT serial_number FROM devices WHERE management_source = '{src}' LIMIT 1", fetch_all=True)
    if row:
        devices[src] = row[0]["serial_number"]

queries = [
    f"power on {devices.get('oneview')}",
    f"power off {devices.get('oneview')}",
    f"check status of {devices.get('mock_network')}",
    f"delete {devices.get('mock_network')}",
    f"fetch event logs from {devices.get('comops')}",
    f"clear event log for {devices.get('comops')}",
    f"check sensors of {devices.get('mock_server')}",
    f"discover hardware inventory of {devices.get('mock_server')}",
    f"create volume on {devices.get('mock_storage')}",
    f"update {devices.get('mock_storage')}"
]

registry = ResourceRegistry()
cache = ResourceCache()
resolver = ResourceResolver(registry, cache)
agent = QueryAgent()

results = {}
for q in queries:
    try:
        parsed = agent.parse_query(q)
        res = resolver.resolve(parsed)
        d = asdict(res)
        results[q] = {
            "action": parsed.get("action"),
            "target": parsed.get("identifier"),
            "endpoint": d.get("api_endpoint"),
            "source": d.get("management_source")
        }
    except Exception as e:
        results[q] = {"error": str(e), "action": parsed.get("action") if "parsed" in locals() else None}

print(json.dumps(results, indent=2))

