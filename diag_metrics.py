import requests
ID = "agg-sw02-1"
BASE = "http://127.0.0.1:8000"

print("=== Base device ===")
r = requests.get(f"{BASE}/rest/server-hardware/{ID}")
d = r.json()
print("power_state:", d.get("power_state"))
print("cpu_utilization_percent:", d.get("cpu_utilization_percent"))
print("memory_utilization_percent:", d.get("memory_utilization_percent"))
print("power_draw_watts:", d.get("power_draw_watts"))
print("temperature_celsius:", d.get("temperature_celsius"))

print("\n=== /utilization ===")
r2 = requests.get(f"{BASE}/rest/server-hardware/{ID}/utilization")
print("status:", r2.status_code)
print(r2.json())

print("\n=== /thermal ===")
r3 = requests.get(f"{BASE}/rest/server-hardware/{ID}/thermal")
print("status:", r3.status_code)
print(r3.json())
