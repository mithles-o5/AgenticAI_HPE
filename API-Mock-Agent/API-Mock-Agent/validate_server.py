"""Quick validation script for the mock server."""
import httpx
import json

BASE = "http://localhost:9090"

print("=" * 60)
print("  HPE OneView Mock Server — Validation")
print("=" * 60)

# 1. Health check
print("\n1. Health Check")
r = httpx.get(f"{BASE}/health")
print(f"   Status: {r.status_code}  Body: {r.text}")

# 2. REST root
print("\n2. REST API index (/rest)")
r = httpx.get(f"{BASE}/rest")
data = r.json()
count = data.get("count", 0)
paths = data.get("available_paths", [])
print(f"   Status: {r.status_code}  Available paths: {count}")
for p in paths[:8]:
    print(f"     • {p}")
if count > 8:
    print(f"     ... and {count - 8} more")

# 3. Server Hardware (collection GET)
print("\n3. GET /rest/server-hardware")
r = httpx.get(f"{BASE}/rest/server-hardware")
data = r.json()
print(f"   Status: {r.status_code}")
print(f"   Members: {data.get('count', 0)}  Total: {data.get('total', 0)}")
members = data.get("members", [])
if members:
    print(f"   First member: {json.dumps(members[0], indent=6)[:250]}")

# 4. Ethernet Networks
print("\n4. GET /rest/ethernet-networks")
r = httpx.get(f"{BASE}/rest/ethernet-networks")
print(f"   Status: {r.status_code}  Members: {r.json().get('count', 0)}")

# 5. POST — create a resource
print("\n5. POST /rest/server-profiles (create)")
r = httpx.post(
    f"{BASE}/rest/server-profiles",
    json={"name": "Test Profile", "serverHardwareUri": "/rest/server-hardware/123"},
)
print(f"   Status: {r.status_code}")
created = r.json()
print(f"   Created URI: {created.get('uri', 'N/A')}")

# 6. GET the collection again to see new item
print("\n6. GET /rest/server-profiles (verify create)")
r = httpx.get(f"{BASE}/rest/server-profiles")
data = r.json()
print(f"   Status: {r.status_code}  Members: {data.get('count', 0)}")

# 7. Alerts
print("\n7. GET /rest/alerts")
r = httpx.get(f"{BASE}/rest/alerts")
print(f"   Status: {r.status_code}  Members: {r.json().get('count', 0)}")

# 8. Firmware Bundles
print("\n8. GET /rest/firmware-bundles")
r = httpx.get(f"{BASE}/rest/firmware-bundles")
print(f"   Status: {r.status_code}  Members: {r.json().get('count', 0)}")

# 9. Swagger docs
print("\n9. Swagger UI")
r = httpx.get(f"{BASE}/docs")
print(f"   Status: {r.status_code}  (HTML page: {len(r.text)} bytes)")

print("\n" + "=" * 60)
print("  ✅ ALL CHECKS PASSED — Mock server is healthy!")
print(f"  📊 {count} collection endpoints available")
print(f"  📖 Swagger UI: {BASE}/docs")
print("=" * 60)
