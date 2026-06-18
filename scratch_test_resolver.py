import sys
sys.path.append('d:\\HPE CPP\\MCP_Integrated')
sys.path.append('d:\\HPE CPP\\MCP_Integrated\\resource_resolver')



from resource_resolver.query_agent import QueryAgent
from resource_resolver.resolver import ResourceResolver
from resource_resolver.registry import ResourceRegistry
from resource_resolver.cache import ResourceCache

print(QueryAgent.parse_query("status of core-sw-01"))
print(QueryAgent.parse_query("status of prod-vol-001"))
print(QueryAgent.parse_query("status of demo-vm-001"))

registry = ResourceRegistry()
cache = ResourceCache()
resolver = ResourceResolver(registry, cache)

try:
    print(resolver.resolve({"identifier": "core-sw-01", "action": "STATUS"}))
except Exception as e:
    print(f"Error core-sw-01: {e}")

try:
    print(resolver.resolve({"identifier": "prod-vol-001", "action": "STATUS"}))
except Exception as e:
    print(f"Error prod-vol-001: {e}")

try:
    print(resolver.resolve({"identifier": "demo-vm-001", "action": "STATUS"}))
except Exception as e:
    print(f"Error demo-vm-001: {e}")

print("Testing db_queries.ANY list...")
from resource_resolver.db_queries import DeviceQueries
try:
    print(DeviceQueries.list_devices_by_management_source("oneview"))
except Exception as e:
    print(f"Error list devices: {e}")
