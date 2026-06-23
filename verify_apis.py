import sys
import os
import json
from fastapi.testclient import TestClient

workspace = "d:\\AgenticAI_HPE"

def verify_network():
    print("\n--- Verifying Network Server ---")
    sys.path.insert(0, os.path.join(workspace, "mock_server(network)"))
    from main import app as network_app
    client = TestClient(network_app)
    
    # 1. List devices
    resp = client.get("/network/v1/devices")
    assert resp.status_code == 200, f"List failed: {resp.text}"
    devices = resp.json()
    assert len(devices) > 0, "No network devices found"
    print(f"Success: Found {len(devices)} network devices.")
    
    device_id = devices[0]["id"]
    
    # 2. Get device by ID
    resp = client.get(f"/network/v1/devices/{device_id}")
    assert resp.status_code == 200, f"Get failed: {resp.text}"
    device = resp.json()
    assert device["id"] == device_id
    print("Success: Get device by ID matches.")
    
    # 3. Patch device
    resp = client.patch(f"/network/v1/devices/{device_id}", json={"name": "New Network Name"})
    assert resp.status_code == 200, f"Patch failed: {resp.text}"
    device = resp.json()
    assert device["name"] == "New Network Name"
    print("Success: Patch name matches.")
    
    # 4. Power ON / OFF
    resp = client.post(f"/network/v1/devices/{device_id}/power", json={"action": "ON"})
    assert resp.status_code == 200, f"Power ON failed: {resp.text}"
    device = resp.json()
    assert device["power_state"] == "ON"
    assert float(device["cpu_utilization_percent"]) > 0.0
    print("Success: Power ON sets state and metrics.")
    
    resp = client.post(f"/network/v1/devices/{device_id}/power", json={"action": "OFF"})
    assert resp.status_code == 200, f"Power OFF failed: {resp.text}"
    device = resp.json()
    assert device["power_state"] == "OFF"
    assert float(device["cpu_utilization_percent"]) == 0.0
    print("Success: Power OFF zeroes out metrics.")
    
    # 5. Configure VLAN
    resp = client.post(f"/network/v1/devices/{device_id}/vlans", json={"vlan_id": 99, "name": "TestVLAN"})
    assert resp.status_code == 200, f"VLAN config failed: {resp.text}"
    device = resp.json()
    vlans = device["configured_vlans"]
    if isinstance(vlans, str):
        vlans = json.loads(vlans)
    assert any(v["vlan_id"] == 99 for v in vlans), f"VLAN 99 not found in {vlans}"
    print("Success: VLAN configured and persisted.")
    
    # 6. Port Status change
    resp = client.post(f"/network/v1/devices/{device_id}/ports/eth9/status", json={"status": "down"})
    assert resp.status_code == 200, f"Port config failed: {resp.text}"
    device = resp.json()
    ports = device["ports"]
    if isinstance(ports, str):
        ports = json.loads(ports)
    assert ports.get("eth9") == "down", f"Port eth9 not down in {ports}"
    print("Success: Port status configured and persisted.")
    
    # 6.5 Test Aruba Central REST APIs
    # List switches
    resp = client.get("/monitoring/v1/switches")
    assert resp.status_code == 200, f"List Aruba switches failed: {resp.text}"
    switches = resp.json()["switches"]
    assert len(switches) > 0, "No Aruba switches returned"
    print("Success: Aruba Central list switches returned results.")

    # Get single switch
    resp = client.get(f"/monitoring/v1/switches/{device_id}")
    assert resp.status_code == 200, f"Get Aruba switch failed: {resp.text}"
    sw_data = resp.json()
    assert sw_data["serial"] == device_id
    assert isinstance(sw_data["model"], str)

    print("Success: Aruba Central get switch by serial returned correct details.")

    # Get switch ports
    resp = client.get(f"/monitoring/v1/switches/{device_id}/ports")
    assert resp.status_code == 200, f"Get Aruba ports failed: {resp.text}"
    ports_data = resp.json()["ports"]
    assert ports_data.get("eth9") == "down"
    print("Success: Aruba Central get switch ports returned correct ports config.")

    # Get switch VLANs
    resp = client.get(f"/monitoring/v1/switches/{device_id}/vlan")
    assert resp.status_code == 200, f"Get Aruba VLANs failed: {resp.text}"
    vlans_data = resp.json()["vlans"]
    assert any(v["vlan_id"] == 99 for v in vlans_data)
    print("Success: Aruba Central get switch VLANs returned correct configuration.")

    # Configure a VLAN via Aruba Endpoint
    resp = client.post(f"/monitoring/v1/switches/{device_id}/vlan", json={"vlan_id": 100, "name": "ArubaVLAN"})
    assert resp.status_code == 200, f"Configure Aruba VLAN failed: {resp.text}"
    assert any(v["vlan_id"] == 100 for v in resp.json()["vlans"])
    print("Success: Aruba Central configure VLAN works.")

    # Configure port status via Aruba Endpoint
    resp = client.post(f"/monitoring/v1/switches/{device_id}/ports/eth10/status", json={"status": "up"})
    assert resp.status_code == 200, f"Configure Aruba port status failed: {resp.text}"
    assert resp.json()["ports"].get("eth10") == "up"
    print("Success: Aruba Central configure port status works.")

    # 7. Delete device
    resp = client.delete(f"/network/v1/devices/{device_id}")

    assert resp.status_code == 200, f"Delete failed: {resp.text}"
    print("Success: Device deleted.")
    
    resp = client.get(f"/network/v1/devices/{device_id}")
    assert resp.status_code == 404, "Device was not deleted"
    
    # Clean up sys.path
    sys.path.remove(os.path.join(workspace, "mock_server(network)"))
    # Remove from sys.modules to avoid collision
    for key in list(sys.modules.keys()):
        if key == "main" or key.startswith("models") or key.startswith("database"):
            del sys.modules[key]


def verify_cloud():
    print("\n--- Verifying Cloud Server ---")
    sys.path.insert(0, os.path.join(workspace, "mock_server(cloud)"))
    from main import app as cloud_app
    client = TestClient(cloud_app)
    
    # 1. List devices
    resp = client.get("/api/v1/devices")
    assert resp.status_code == 200, f"List failed: {resp.text}"
    devices = resp.json()
    assert len(devices) > 0, "No cloud devices found"
    print(f"Success: Found {len(devices)} cloud devices.")
    
    device_id = devices[0]["id"]
    
    # 2. Get device by ID
    resp = client.get(f"/api/v1/devices/{device_id}")
    assert resp.status_code == 200, f"Get failed: {resp.text}"
    device = resp.json()
    assert device["id"] == device_id
    print("Success: Get device by ID matches.")
    
    # 3. Patch device
    resp = client.patch(f"/api/v1/devices/{device_id}", json={"name": "New Cloud Name"})
    assert resp.status_code == 200, f"Patch failed: {resp.text}"
    device = resp.json()
    assert device["name"] == "New Cloud Name"
    print("Success: Patch name matches.")
    
    # 4. Power ON / OFF
    resp = client.post(f"/api/v1/devices/{device_id}/power", json={"action": "ON"})
    assert resp.status_code == 200, f"Power ON failed: {resp.text}"
    device = resp.json()
    assert device["power_state"] == "ON"
    print("Success: Power ON succeeded.")
    
    # 5. Create VM
    resp = client.get(f"/api/v1/devices/{device_id}")
    initial_device = resp.json()
    initial_vms = int(initial_device.get("active_vms") or 0)
    initial_vcpu = int(initial_device.get("allocated_vcpu") or 0)
    initial_ram = int(initial_device.get("allocated_ram_gb") or 0)

    resp = client.post(f"/api/v1/devices/{device_id}/vms", json={"vm_name": "TestVM", "vcpu": 4, "ram_gb": 16})
    assert resp.status_code == 200, f"VM creation failed: {resp.text}"
    vm = resp.json()
    vm_id = vm["id"]
    assert vm["vm_name"] == "TestVM"
    print("Success: VM created.")
    
    # Verify resources on host device
    resp = client.get(f"/api/v1/devices/{device_id}")
    device = resp.json()
    assert int(device["active_vms"]) == initial_vms + 1
    assert int(device["allocated_vcpu"]) == initial_vcpu + 4
    assert int(device["allocated_ram_gb"]) == initial_ram + 16
    print("Success: Host device metrics incremented.")
    
    # 6. Delete VM
    resp = client.delete(f"/api/v1/devices/{device_id}/vms/{vm_id}")
    assert resp.status_code == 200, f"VM deletion failed: {resp.text}"
    print("Success: VM terminated.")
    
    # Verify resources decremented
    resp = client.get(f"/api/v1/devices/{device_id}")
    device = resp.json()
    assert int(device["active_vms"]) == initial_vms
    assert int(device["allocated_vcpu"]) == initial_vcpu
    assert int(device["allocated_ram_gb"]) == initial_ram
    print("Success: Host device metrics decremented.")
    
    # 7. Delete device
    resp = client.delete(f"/api/v1/devices/{device_id}")
    assert resp.status_code == 200, f"Delete failed: {resp.text}"
    print("Success: Device deleted.")
    
    # Clean up sys.path
    sys.path.remove(os.path.join(workspace, "mock_server(cloud)"))
    for key in list(sys.modules.keys()):
        if key == "main" or key.startswith("models") or key.startswith("database"):
            del sys.modules[key]


def verify_storage():
    print("\n--- Verifying Storage Server ---")
    sys.path.insert(0, os.path.join(workspace, "mock_server(storage)"))
    from main import app as storage_app
    client = TestClient(storage_app)
    
    # 1. List devices
    resp = client.get("/data-services/v1beta1/devices")
    assert resp.status_code == 200, f"List failed: {resp.text}"
    devices = resp.json()
    assert len(devices) > 0, "No storage devices found"
    print(f"Success: Found {len(devices)} storage devices.")
    
    device_id = devices[0]["id"]
    
    # 2. Get device by ID
    resp = client.get(f"/data-services/v1beta1/devices/{device_id}")
    assert resp.status_code == 200, f"Get failed: {resp.text}"
    device = resp.json()
    assert device["id"] == device_id
    
    initial_free = float(device.get("free_capacity_gb") or 10000)

    # 3. Create Volume
    resp = client.post(f"/data-services/v1beta1/devices/{device_id}/volumes", json={"volume_name": "TestVol", "size_gb": 100})
    assert resp.status_code == 200, f"Volume creation failed: {resp.text}"
    vol = resp.json()
    vol_id = vol["id"]
    assert vol["volume_name"] == "TestVol"
    print("Success: Volume created.")
    
    # Verify free capacity decremented
    resp = client.get(f"/data-services/v1beta1/devices/{device_id}")
    device_new = resp.json()
    assert float(device_new["free_capacity_gb"]) == initial_free - 100
    print("Success: Free capacity decremented.")
    
    # 4. Delete Volume
    resp = client.delete(f"/data-services/v1beta1/devices/{device_id}/volumes/{vol_id}")
    assert resp.status_code == 200, f"Volume deletion failed: {resp.text}"
    print("Success: Volume deleted.")
    
    # Verify free capacity restored
    resp = client.get(f"/data-services/v1beta1/devices/{device_id}")
    device_restored = resp.json()
    assert float(device_restored["free_capacity_gb"]) == initial_free
    print("Success: Free capacity restored.")
    
    # Clean up sys.path
    sys.path.remove(os.path.join(workspace, "mock_server(storage)"))
    for key in list(sys.modules.keys()):
        if key == "main" or key.startswith("models") or key.startswith("database"):
            del sys.modules[key]


def verify_compute_ops():
    print("\n--- Verifying Compute Ops Server ---")
    sys.path.insert(0, os.path.join(workspace, "mock_server(Comops)"))
    from main import app as comops_app
    client = TestClient(comops_app)
    
    # 1. List devices
    resp = client.get("/compute-ops-mgmt/v1/devices")
    assert resp.status_code == 200, f"List failed: {resp.text}"
    devices = resp.json()
    assert len(devices) > 0, "No compute ops devices found"
    print(f"Success: Found {len(devices)} compute ops devices.")
    
    device_id = devices[0]["id"]
    
    # 2. Power Control
    resp = client.post(f"/compute-ops-mgmt/v1/devices/{device_id}/power", json={"action": "ON"})
    assert resp.status_code == 200, f"Power ON failed: {resp.text}"
    device = resp.json()
    assert device["power_state"] == "ON"
    print("Success: Power ON succeeded.")
    
    # 3. Firmware Update
    resp = client.post(f"/compute-ops-mgmt/v1/devices/{device_id}/firmware", json={"firmware_version": "1.2.3.4"})
    assert resp.status_code == 200, f"Firmware update failed: {resp.text}"
    device = resp.json()
    assert device["firmware_version"] == "1.2.3.4"
    print("Success: Firmware updated.")
    
    # Clean up sys.path
    sys.path.remove(os.path.join(workspace, "mock_server(Comops)"))
    for key in list(sys.modules.keys()):
        if key == "main" or key.startswith("models") or key.startswith("database"):
            del sys.modules[key]


def verify_oneview():
    print("\n--- Verifying OneView Server ---")
    sys.path.insert(0, os.path.join(workspace, "mock_server(oneview)"))
    from main import app as oneview_app
    client = TestClient(oneview_app)
    
    # 1. List server hardware
    resp = client.get("/rest/server-hardware")
    assert resp.status_code == 200, f"List failed: {resp.text}"
    devices = resp.json()
    # Check members if returned as dict or list
    members = devices.get("members") if isinstance(devices, dict) else devices
    assert len(members) > 0, "No oneview server hardware found"
    print(f"Success: Found {len(members)} oneview server hardware.")
    
    device_id = members[0]["id"]
    
    # 2. Patch device
    resp = client.patch(f"/rest/server-hardware/{device_id}", json={"name": "New OneView Name"})
    assert resp.status_code == 200, f"Patch failed: {resp.text}"
    device = resp.json()
    assert device["name"] == "New OneView Name"
    print("Success: Patch name matches.")
    
    # 3. Power Control
    resp = client.post(f"/rest/server-hardware/{device_id}/power", json={"powerState": "On", "action": "On"})
    assert resp.status_code == 200, f"Power ON failed: {resp.text}"
    device = resp.json()
    assert device["power_state"] == "ON"
    print("Success: Power ON succeeded.")
    
    # Clean up sys.path
    sys.path.remove(os.path.join(workspace, "mock_server(oneview)"))
    for key in list(sys.modules.keys()):
        if key == "main" or key.startswith("models") or key.startswith("database"):
            del sys.modules[key]


def verify_ilo():
    print("\n--- Verifying iLO Server ---")
    sys.path.insert(0, os.path.join(workspace, "mock_server(ilo)"))
    from main import app as ilo_app
    client = TestClient(ilo_app)
    
    # 1. GET ServiceRoot
    resp = client.get("/redfish/v1/")
    assert resp.status_code == 200, f"Service root failed: {resp.text}"
    root = resp.json()
    assert "UUID" in root, "UUID missing in ServiceRoot"
    print("Success: ServiceRoot accessed successfully.")
    
    # 2. GET accounts collection
    resp = client.get("/redfish/v1/accountservice/accounts")
    assert resp.status_code == 200, f"Accounts collection failed: {resp.text}"
    accounts_collection = resp.json()
    assert "Members" in accounts_collection, "Members missing in accounts collection"
    print("Success: Accounts collection accessed successfully.")
    
    # 3. POST to create a new manager account
    new_acc = {
        "UserName": "test_admin",
        "Password": "SecretPassword123!",
        "RoleId": "Administrator",
        "Enabled": True
    }
    resp = client.post("/redfish/v1/accountservice/accounts", json=new_acc)
    assert resp.status_code == 200, f"Account creation failed: {resp.text}"
    created_acc = resp.json()
    acc_id = created_acc["Id"]
    assert created_acc["UserName"] == "test_admin"
    print(f"Success: Created new manager account with ID {acc_id}.")
    
    # 4. GET the created account
    resp = client.get(f"/redfish/v1/accountservice/accounts/{acc_id}")
    assert resp.status_code == 200, f"Get account failed: {resp.text}"
    acc = resp.json()
    assert acc["UserName"] == "test_admin"
    print("Success: Retrieved newly created account.")
    
    # 5. PATCH the account
    resp = client.patch(f"/redfish/v1/accountservice/accounts/{acc_id}", json={"Enabled": False})
    assert resp.status_code == 200, f"Patch account failed: {resp.text}"
    patched_acc = resp.json()
    assert patched_acc["Enabled"] is False
    print("Success: Patched account property (Enabled=False).")
    
    # 6. DELETE the account
    resp = client.delete(f"/redfish/v1/accountservice/accounts/{acc_id}")
    assert resp.status_code == 200, f"Delete account failed: {resp.text}"
    print("Success: Account deleted.")
    
    # 7. GET deleted account should return 404
    resp = client.get(f"/redfish/v1/accountservice/accounts/{acc_id}")
    assert resp.status_code == 404, f"Get deleted account should be 404, got {resp.status_code}"
    print("Success: Deleted account returns 404 as expected.")
    
    # Clean up sys.path
    sys.path.remove(os.path.join(workspace, "mock_server(ilo)"))
    for key in list(sys.modules.keys()):
        if key == "main" or key.startswith("models") or key.startswith("database"):
            del sys.modules[key]


if __name__ == "__main__":
    try:
        verify_network()
        verify_cloud()
        verify_storage()
        verify_compute_ops()
        verify_oneview()
        verify_ilo()
        print("\n==============================")
        print("ALL TESTS PASSED SUCCESSFULLY!")
        print("==============================")
    except Exception as e:
        print(f"\nAn error occurred during verification: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

