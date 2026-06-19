import httpx, json

# Full device data - wan-r08-10017
r = httpx.get('http://127.0.0.1:8001/compute-ops-mgmt/v1/devices/wan-r08-10017', timeout=5)
d = r.json()
print('=== wan-r08-10017 from ComOps API ===')
print(f'  Status: {r.status_code}')
print(f'  power_state: {d.get("power_state")}')
print(f'  health_status: {d.get("health_status")}')
print(f'  cpu_utilization_percent: {d.get("cpu_utilization_percent")}')
print(f'  memory_utilization_percent: {d.get("memory_utilization_percent")}')
print(f'  power_draw_watts: {d.get("power_draw_watts")}')
print(f'  temperature_celsius: {d.get("temperature_celsius")}')

# Also by source_device_id UUID
r2 = httpx.get('http://127.0.0.1:8001/compute-ops-mgmt/v1/devices/f1d0f059-629f-46ae-8afb-ffc80f4f5e26', timeout=5)
print(f'\n=== By source_device_id: {r2.status_code} ===')
if r2.status_code == 200:
    d2 = r2.json()
    print(f'  cpu={d2.get("cpu_utilization_percent")} mem={d2.get("memory_utilization_percent")}')
else:
    print(f'  Response: {r2.text[:100]}')

# Test power-off PUT
print('\n=== Test PUT power OFF ===')
r3 = httpx.put(
    'http://127.0.0.1:8001/compute-ops-mgmt/v1/devices/wan-r08-10017',
    json={"power_state": "OFF"},
    timeout=5
)
print(f'  Status: {r3.status_code}')
if r3.status_code == 200:
    d3 = r3.json()
    print(f'  power_state: {d3.get("power_state")}')
    print(f'  cpu: {d3.get("cpu_utilization_percent")}')
    print(f'  mem: {d3.get("memory_utilization_percent")}')

# Restore ON
print('\n=== Restore to ON ===')
r4 = httpx.put(
    'http://127.0.0.1:8001/compute-ops-mgmt/v1/devices/wan-r08-10017',
    json={"power_state": "ON"},
    timeout=5
)
print(f'  Status: {r4.status_code}')
if r4.status_code == 200:
    d4 = r4.json()
    print(f'  power_state: {d4.get("power_state")}')
    print(f'  cpu: {d4.get("cpu_utilization_percent")}')
    print(f'  mem: {d4.get("memory_utilization_percent")}')
