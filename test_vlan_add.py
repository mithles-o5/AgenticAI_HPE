import httpx, json

BASE = "http://127.0.0.1:8002"
DEVICE = "port-channel-cfg-016"

# 1. Check current VLANs
resp = httpx.get(f"{BASE}/network/v1/devices/{DEVICE}/vlans")
print("BEFORE:", json.dumps(resp.json(), indent=2))

# 2. POST VLAN 200
resp2 = httpx.post(f"{BASE}/network/v1/devices/{DEVICE}/vlans",
                   json={"vlan_id": 200, "name": "production-2"})
print(f"\nPOST status: {resp2.status_code}")
result = resp2.json()
print("POST response configured_vlans:", json.dumps(result.get("configured_vlans"), indent=2))

# 3. GET again
resp3 = httpx.get(f"{BASE}/network/v1/devices/{DEVICE}/vlans")
print("\nAFTER:", json.dumps(resp3.json(), indent=2))

# 4. Simulate what mock_adapter does
vlans = result.get("configured_vlans") or []
if isinstance(vlans, str):
    vlans = json.loads(vlans)
body_vlan_id = 200
vlan_ids = [v.get("vlan_id") if isinstance(v, dict) else v for v in vlans]
print(f"\nadded_vlan={body_vlan_id!r}, vlan_ids={vlan_ids}")
print(f"vlan_added={body_vlan_id in vlan_ids}")
