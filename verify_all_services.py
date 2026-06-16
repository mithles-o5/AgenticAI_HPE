"""verify_all_services.py - Health check + proxy allow/block test."""
import httpx, sys

print("=== Service Health Check ===")
services = [
    ("OneView mock   :8000", "http://127.0.0.1:8000/rest/custom-servers"),
    ("Compute Ops    :8001", "http://127.0.0.1:8001/compute-ops-mgmt/v1/custom-servers"),
    ("Cloud mock     :8002", "http://127.0.0.1:8002/api/v1/access-controls"),
    ("Storage mock   :8003", "http://127.0.0.1:8003/data-services/v1beta1/async-operations"),
    ("Server Agent   :8009", "http://127.0.0.1:8009/server-agent/health"),
]
all_ok = True
for name, url in services:
    try:
        r = httpx.get(url, timeout=6)
        print(f"  [{r.status_code}] {name}")
        if r.status_code >= 400:
            print(f"       => {r.text[:200]}")
            all_ok = False
    except Exception as e:
        print(f"  [ERR] {name}: {e}")
        all_ok = False

print()
print("=== Proxy Allow/Block Tests via Server Agent ===")
AGENT = "http://127.0.0.1:8009"
tests = [
    (200, "ALLOW", "GET",  f"{AGENT}/rest/custom-servers"),
    (200, "ALLOW", "GET",  f"{AGENT}/rest/rack-managers"),
    (200, "ALLOW", "GET",  f"{AGENT}/compute-ops-mgmt/v1/custom-servers"),
    (403, "BLOCK", "GET",  f"{AGENT}/rest/ethernet-networks"),
    (403, "BLOCK", "GET",  f"{AGENT}/rest/storage-volumes"),
    (403, "BLOCK", "GET",  f"{AGENT}/rest/storage-systems"),
    (403, "BLOCK", "GET",  f"{AGENT}/compute-ops-mgmt/v1/storage"),
    (403, "BLOCK", "GET",  f"{AGENT}/compute-ops-mgmt/v1/networks"),
    (403, "BLOCK", "GET",  f"{AGENT}/compute-ops-mgmt/v1/switches"),
    (200, "ALLOW", "GET",  f"{AGENT}/compute-ops/v1/custom-servers"),
    (403, "BLOCK", "GET",  f"{AGENT}/compute-ops/v1/switches"),
    (200, "ALLOW", "GET",  f"{AGENT}/server-agent/rest/custom-servers"),
    (403, "BLOCK", "GET",  f"{AGENT}/server-agent/rest/storage-volumes"),
]
for expected, tag, method, url in tests:
    path = url.replace(AGENT, "")
    try:
        r = httpx.request(method, url, timeout=6)
        ok = r.status_code == expected
        icon = "PASS" if ok else "FAIL"
        print(f"  [{icon}] [{tag}] {method} {path} => {r.status_code} (expected {expected})")
        if not ok:
            all_ok = False
    except Exception as e:
        print(f"  [ERR] {method} {path}: {e}")
        all_ok = False

print()
print("All tests PASSED!" if all_ok else "SOME TESTS FAILED!")
sys.exit(0 if all_ok else 1)
