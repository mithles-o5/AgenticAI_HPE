import sys
import os
import json

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

# 1. Fetch from mock DB cache
import mock_db_cache
mock_db_cache.setup()
conn = mock_db_cache._shared_conn
conn.row_factory = mock_db_cache.dict_factory
cur = conn.cursor()
cur.execute("SELECT * FROM devices")
devices = cur.fetchall()

print(f"Fetched {len(devices)} devices from CMDB registry")

# 2. Read OneView mock_data.json
oneview_mock_file = os.path.join(ROOT_DIR, "generator", "servers", "oneview", "mock_data.json")
try:
    with open(oneview_mock_file, "r", encoding="utf-8") as f:
        oneview_db = json.load(f)
except Exception as e:
    print(f"Error reading OneView mock_data.json: {e}")
    oneview_db = {}

if "server_hardware" not in oneview_db:
    oneview_db["server_hardware"] = {}

# 3. Read ComOps mock_data.json
comops_mock_file = os.path.join(ROOT_DIR, "generator", "servers", "compute_ops", "mock_data.json")
try:
    with open(comops_mock_file, "r", encoding="utf-8") as f:
        comops_db = json.load(f)
except Exception as e:
    print(f"Error reading ComOps mock_data.json: {e}")
    comops_db = {}

if "servers" not in comops_db:
    comops_db["servers"] = {}

# 4. Inject devices
ov_count = 0
comops_count = 0

# Also include missing test devices dynamically just to be sure
test_devices = ["core-sw-01", "prod-vol-001", "dsk-007", "demo-vm-001", "ms-2112", "dc1-a7", "compute-22", "rack42-n3", "edge-r1", "wan-r2", "leaf-sw12", "fw-core-01", "fw-edge-02", "ms-123", "com-cloudnode-001", "ov1-rackserver-001"]

for dev in devices:
    src = dev.get("management_source", "").lower()
    device_id = dev.get("source_device_id") or dev.get("id")
    
    # We create a generic mock representation
    mock_obj = {
        "uuid": device_id,  # For OneView usually
        "id": device_id,    # For Comops usually
        "name": dev.get("fqdn") or dev.get("serial_number"),
        "serialNumber": dev.get("serial_number"),
        "ip_address": dev.get("ip_address"),
        "powerState": "On",
        "status": "OK",
        "healthStatus": "OK",
        "model": "Mocked DB Device",
        "processorCoreCount": 16,
        "memoryMb": 32768,
        "device_type": dev.get("device_type", "server")
    }

    if src == "oneview":
        # Don't overwrite if existing
        if device_id not in oneview_db["server_hardware"]:
            oneview_db["server_hardware"][device_id] = mock_obj
            ov_count += 1
    elif src == "coms":
        if device_id not in comops_db["servers"]:
            comops_db["servers"][device_id] = mock_obj
            comops_count += 1

# Manually add the custom test devices to both just in case they aren't seeded
for td in test_devices:
    obj = {
        "uuid": td, "id": td, "name": td, "serialNumber": td,
        "powerState": "On", "status": "OK", "healthStatus": "OK",
        "model": "Test Device"
    }
    if td not in oneview_db["server_hardware"]:
        oneview_db["server_hardware"][td] = obj
    if td not in comops_db["servers"]:
        comops_db["servers"][td] = obj

print(f"Added {ov_count} new devices to OneView")
print(f"Added {comops_count} new devices to ComOps")

# 5. Write back to disk
with open(oneview_mock_file, "w", encoding="utf-8") as f:
    json.dump(oneview_db, f, indent=4)
print("Updated OneView mock_data.json")

with open(comops_mock_file, "w", encoding="utf-8") as f:
    json.dump(comops_db, f, indent=4)
print("Updated ComOps mock_data.json")
