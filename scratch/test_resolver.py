import sys
sys.path.insert(0, r'c:\AgenticAI_HPE\resource_resolver')
from db_queries import EndpointRegistryQueries
from errors import EndpointNotFoundError

test_cases = [
    # 1. Generic device on comops
    ('comops', 'server', 'LIST'),
    ('comops', 'switch', 'LIST'),
    
    # 2. Specific device on comops
    ('comops', 'storage', 'get_compute_ops_mgmt_v1beta3_storage_systems_systemid'),
    
    # 3. Generic mock_cloud
    ('mock_cloud', 'database_service', 'STATUS'),
    ('mock_cloud', 'vm', 'ON'),
    
    # 4. Mock server
    ('mock_server', 'server', 'STATUS'),
    ('mock_server', 'server-hardware', 'COLD_BOOT'),
    
    # 5. OneView specific
    ('oneview', 'server', 'STATUS'),
    
    # 6. Fallback test: If we ask for device_type='firewall' but the action is only mapped to 'server', does it fallback?
    ('oneview', 'firewall', 'get_rest_server_hardware_id_bios'),
    
    # 7. Error test
    ('bad_vendor', 'server', 'ON')
]

print(f"{'Vendor':<12} | {'Device':<18} | {'Action Key':<50} | {'Result (Method + Path)':<50}")
print('-'*135)
for vendor, dtype, action in test_cases:
    try:
        ep = EndpointRegistryQueries.get_endpoint(vendor, dtype, action)
        res = f"{ep['http_method']} {ep['api_path']}"
    except EndpointNotFoundError:
        res = "ERROR: EndpointNotFoundError"
    except Exception as e:
        res = f"ERROR: {type(e).__name__}"
    
    print(f"{vendor:<12} | {dtype:<18} | {action:<50} | {res:<50}")
