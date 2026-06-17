import sys
import os
import json

# Setup sys.path to find mock_db_cache
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))



from resource_resolver.db_loader import load_registry_from_db
registry = load_registry_from_db()

# Check devices
# devices = registry.list_devices_by_management_source("oneview")
# print(f"Total OneView devices in CMDB: {len(devices)}")
# for d in devices[:10]:
#     print(f"ID: {d.id}, Serial: {d.serial_number}, IP: {d.ip_address}")

# Search for OV1-RackServer-001 in CMDB
# match = [d for d in devices if "OV1-RackServer-001" in d.serial_number]
# print(f"CMDB matches for 'OV1-RackServer-001': {[(d.id, d.serial_number) for d in match]}")

# Load mock_data.json from mock_server(oneview)
mock_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "mock_server(oneview)", "mock_data.json")
with open(mock_file, "r") as f:
    data = json.load(f)

servers = data.get("server_hardware", {})
print(f"Total server_hardware in OneView mock data: {len(servers)}")

# Find keys or names matching OV1-RackServer-001
matches = []
for k, v in servers.items():
    if "OV1-RackServer-001" in k or "OV1-RackServer-001" in v.get("name", "") or "OV1-RackServer-001" in v.get("serialNumber", ""):
        matches.append((k, v.get("name"), v.get("serialNumber")))

print(f"Mock data matches for 'OV1-RackServer-001': {matches}")
