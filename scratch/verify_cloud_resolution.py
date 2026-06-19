import sys
import os

# Add root directory to sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.normpath(os.path.join(BASE_DIR, ".."))
sys.path.insert(0, ROOT_DIR)
sys.path.insert(0, os.path.join(ROOT_DIR, "resource_resolver"))

# Enable Mock Database Cache
import mock_db_cache
mock_db_cache.setup()

from resolver import ResourceResolver
from registry import ResourceRegistry
from cache import ResourceCache
from db_loader import load_registry_from_db

def main():
    print("--- TESTING RESOLUTION FOR CLOUD DEVICES ---")
    
    registry = load_registry_from_db()
    cache = ResourceCache()
    resolver = ResourceResolver(registry=registry, cache=cache)
    
    # Test STATUS action on a mock cloud VM
    print("\n[+] Resolving STATUS of demo-vm-001:")
    try:
        res = resolver.resolve({
            "identifier": "demo-vm-001",
            "action": "STATUS",
            "category": "Operational"
        })
        print(f"Device: {res.device.serial_number} ({res.device.device_type})")
        print(f"Management Source: {res.management_source}")
        print(f"Action: {res.action}")
        print(f"API Endpoint: {res.api_endpoint}")
        
        # Check correctness
        expected_path = "/api/v1/devices/cloud-uuid-001"
        if expected_path in res.api_endpoint:
            print("[SUCCESS] Resolved correct endpoint for STATUS")
        else:
            print(f"[FAILED] Expected path {expected_path} not found in {res.api_endpoint}")
    except Exception as e:
        print(f"[ERROR] {e}")
        
    # Test ON power action on a mock cloud VM
    print("\n[+] Resolving ON power action of demo-vm-001:")
    try:
        res = resolver.resolve({
            "identifier": "demo-vm-001",
            "action": "ON",
            "category": "Operational"
        })
        print(f"API Endpoint: {res.api_endpoint}")
        
        # Check correctness
        expected_path = "/api/v1/devices/cloud-uuid-001/power"
        if expected_path in res.api_endpoint:
            print("[SUCCESS] Resolved correct endpoint for ON power action")
        else:
            print(f"[FAILED] Expected path {expected_path} not found in {res.api_endpoint}")
    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    main()
