import sys
import json
from unittest.mock import MagicMock

# Mock out missing third-party libs in the sandbox
sys.modules['redis'] = MagicMock()
sys.modules['pydantic'] = MagicMock()
sys.modules['psycopg2'] = MagicMock()
sys.modules['psycopg2.pool'] = MagicMock()
sys.modules['psycopg2.extras'] = MagicMock()

sys.path.insert(0, r"c:\AgenticAI_HPE\resource_resolver")
from resolver import ResourceResolver
from records import RouteResolution, DeviceRecord
from errors import ResourceNotFoundError

def mock_get_device(*args, **kwargs):
    raise ResourceNotFoundError("Device not found")

def mock_get_endpoint(*args, **kwargs):
    # args: vendor, device_type, action
    return {
        "http_method": "POST",
        "api_path": "/rest/server-hardware",
        "device_type": "server"
    }

def main():
    # 1. Provide parsed natural language payload
    query = "create apollo-node-999"
    print(f"--- QUERY: {query} ---")
    parsed = {"identifier": "apollo-node-999", "action": "CREATE"}
    print(f"Parsed payload: {parsed}")

    # 2. Mock Registry & Cache
    registry = MagicMock()
    registry.lookup.return_value = None
    
    from enums import CacheStatus
    cache = MagicMock()
    cache.get_by_identifier.return_value = (None, CacheStatus.MISS)

    # We need to mock EndpointRegistryQueries inside db_queries
    import db_queries
    db_queries.EndpointRegistryQueries.get_endpoint = MagicMock(side_effect=mock_get_endpoint)

    import db
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    # Mock context manager: with conn.cursor() as cur:
    mock_conn.cursor.return_value.__enter__.return_value = mock_cur
    mock_cur.fetchall.return_value = []
    db.db_manager.get_connection = MagicMock(return_value=mock_conn)

    # 3. Resolve
    resolver = ResourceResolver(registry, cache)
    
    print("\n--- RESOLVING (No defaults) ---")
    try:
        res = resolver.resolve(parsed, requested_by="test-user")
        print(json.dumps(res.to_dict(), indent=2))
    except Exception as e:
        print(f"FAILED (Expected if no defaults provided): {type(e).__name__}: {e}")

    print("\n--- RESOLVING (No defaults provided) ---")
    try:
        res = resolver.resolve(parsed, requested_by="test-user")
        print(json.dumps(res.to_dict(), indent=2))
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
