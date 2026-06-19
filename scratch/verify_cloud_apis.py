import httpx
import json

BASE_URL = "http://127.0.0.1:8003"
DEVICE_ID = "gl-db-011"

def test_apis():
    print("=== Testing Mock Cloud Server APIs ===")

    # 1. GET /api/v1/devices
    print("\n1. Testing GET /api/v1/devices...")
    resp = httpx.get(f"{BASE_URL}/api/v1/devices")
    print(f"Status: {resp.status_code}")
    devices = resp.json()
    print(f"Total devices found: {len(devices)}")
    if devices:
        print(f"First device sample: {devices[0]['serial_number']} (ID: {devices[0]['id']})")

    # 2. GET /api/v1/devices/{id}
    print(f"\n2. Testing GET /api/v1/devices/{DEVICE_ID}...")
    resp = httpx.get(f"{BASE_URL}/api/v1/devices/{DEVICE_ID}")
    print(f"Status: {resp.status_code}")
    device_details = resp.json()
    print(f"Device name: {device_details.get('name')}")
    print(f"Current Power State: {device_details.get('power_state')}")

    # 3. PATCH /api/v1/devices/{id} (Modify allocations/configurations)
    print(f"\n3. Testing PATCH /api/v1/devices/{DEVICE_ID}...")
    patch_payload = {
        "firmware_version": "1.2.3-patch",
        "cpu_cores": 32
    }
    resp = httpx.patch(f"{BASE_URL}/api/v1/devices/{DEVICE_ID}", json=patch_payload)
    print(f"Status: {resp.status_code}")
    updated_device = resp.json()
    print(f"Updated firmware_version: {updated_device.get('firmware_version')}")
    print(f"Updated cpu_cores: {updated_device.get('cpu_cores')}")

    # 4. POST /api/v1/devices/{id}/power (Power Control)
    print(f"\n4. Testing POST /api/v1/devices/{DEVICE_ID}/power (Power OFF)...")
    power_payload = {"state": "Off"}
    resp = httpx.post(f"{BASE_URL}/api/v1/devices/{DEVICE_ID}/power", json=power_payload)
    print(f"Status: {resp.status_code}")
    powered_off_device = resp.json()
    print(f"Power state after OFF: {powered_off_device.get('power_state')}")
    print(f"CPU Utilization: {powered_off_device.get('cpu_utilization_percent')}%")

if __name__ == "__main__":
    test_apis()
