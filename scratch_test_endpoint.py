import sys
sys.path.append('d:\\HPE CPP\\MCP_Integrated')
sys.path.append('d:\\HPE CPP\\MCP_Integrated\\resource_resolver')

import mock_db_cache
mock_db_cache.setup()

from resource_resolver.db_queries import EndpointRegistryQueries

print("Switch STATUS:")
try:
    print(EndpointRegistryQueries.get_endpoint("oneview", "switch", "STATUS"))
except Exception as e:
    print(f"Error: {e}")

print("Storage STATUS:")
try:
    print(EndpointRegistryQueries.get_endpoint("oneview", "storage", "STATUS"))
except Exception as e:
    print(f"Error: {e}")

