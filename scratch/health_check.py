import httpx, sys

services = {
    8000: "OneView mock",
    8001: "ComOps mock",
    8002: "Network mock",
    8003: "Cloud mock",
    8004: "Storage mock",
    8005: "Cloud agent",
    8006: "Network agent",
    8007: "Storage agent",
    8008: "OnPrem agent",
    8009: "Server agent",
    8020: "Capability Registry",
}

print("=== Service Health Check ===")
all_ok = True
for port, name in services.items():
    try:
        r = httpx.get(f"http://127.0.0.1:{port}/health", timeout=3)
        status = "UP" if r.status_code in (200, 404) else f"ERR({r.status_code})"
    except Exception as e:
        status = f"DOWN ({str(e)[:30]})"
        all_ok = False
    print(f"  {name:25s} :{port}  {status}")

print(f"\n{'All services UP!' if all_ok else 'Some services DOWN - check above'}")

# Quick data check for wan-r08-10017
print("\n=== wan-r08-10017 data from ComOps mock ===")
try:
    r = httpx.get("http://127.0.0.1:8001/compute-ops-mgmt/v1/devices/wan-r08-10017", timeout=5)
    if r.status_code == 200:
        d = r.json()
        print(f"  cpu={d.get('cpu_utilization_percent')}%  mem={d.get('memory_utilization_percent')}%  power={d.get('power_draw_watts')}W  temp={d.get('temperature_celsius')}C  state={d.get('power_state')}")
    else:
        print(f"  ERROR: {r.status_code} {r.text[:100]}")
except Exception as e:
    print(f"  ERROR: {e}")
