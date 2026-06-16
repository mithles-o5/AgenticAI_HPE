import httpx
import json

base_url = "http://127.0.0.1:8000"

def test():
    # 1. Get current state of OV1-RackServer-001
    resp = httpx.get(f"{base_url}/rest/server-hardware/OV1-RackServer-001")
    print(f"Initial GET Status: {resp.status_code}")
    if resp.status_code == 200:
        data = resp.json()
        print(f"Initial Power State: {data.get('powerState')}")
        print(f"UUID: {data.get('uuid')}")
    else:
        print(f"Error details: {resp.text}")
        return

    # 2. Put power state to Off
    payload = {"powerState": "Off"}
    resp_put = httpx.put(f"{base_url}/rest/server-hardware/OV1-RackServer-001/powerState", json=payload)
    print(f"PUT Status: {resp_put.status_code}")
    print(f"PUT Response: {resp_put.text}")

    # 3. Get updated state
    resp_get2 = httpx.get(f"{base_url}/rest/server-hardware/OV1-RackServer-001")
    print(f"Second GET Status: {resp_get2.status_code}")
    if resp_get2.status_code == 200:
        print(f"Updated Power State: {resp_get2.json().get('powerState')}")

    # 4. Get thermal/metrics
    resp_thermal = httpx.get(f"{base_url}/rest/server-hardware/OV1-RackServer-001/thermal")
    print(f"Thermal Status: {resp_thermal.status_code}")
    print(f"Thermal Response: {resp_thermal.text}")

if __name__ == "__main__":
    test()
