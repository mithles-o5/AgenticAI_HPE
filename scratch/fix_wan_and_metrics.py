"""
Fix wan-r08-10017 and all routers in oneview SQLite:
1. Add wan-r08-10017 if missing
2. Fix unrealistic cpu/memory values (>100%) to be realistic
3. Verify mock server can find it
"""
import sqlite3, json, random, uuid, httpx

DB = 'd:/HPE CPP/MCP_Integrated/mock_server(oneview)/oneview_db.sqlite'
TABLE = 'dynamic_rest_server_hardware'

conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row

# ── Step 1: Fix all wan-r08 routers with unrealistic CPU/memory values ─────────
print("=== Fixing unrealistic CPU/memory values for all routers ===")
rows = conn.execute(f'SELECT id, serial_number, cpu_utilization_percent, memory_utilization_percent FROM "{TABLE}" WHERE cpu_utilization_percent > 100 OR memory_utilization_percent > 100').fetchall()
print(f"Found {len(rows)} rows with values > 100%")

fixed = 0
for row in rows:
    new_cpu = round(random.uniform(5.0, 95.0), 1)
    new_mem = round(random.uniform(10.0, 90.0), 1)
    conn.execute(
        f'UPDATE "{TABLE}" SET cpu_utilization_percent = ?, memory_utilization_percent = ? WHERE id = ?',
        (new_cpu, new_mem, row["id"])
    )
    fixed += 1

conn.commit()
print(f"Fixed {fixed} rows")

# ── Step 2: Check if wan-r08-10017 exists ─────────────────────────────────────
print("\n=== Checking wan-r08-10017 ===")
existing = conn.execute(
    f'SELECT * FROM "{TABLE}" WHERE serial_number = ? OR name = ?',
    ('wan-r08-10017', 'wan-r08-10017')
).fetchone()

if existing:
    print("wan-r08-10017 already exists with id:", existing["id"])
else:
    print("wan-r08-10017 NOT FOUND — inserting now")

    # Generate a deterministic UUID for this device
    device_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, 'wan-r08-10017.datacenter.local'))
    source_device_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, 'wan-r08-10017-source'))

    new_row = {
        "id": device_id,
        "serial_number": "wan-r08-10017",
        "ip_address": "10.100.1.17",
        "fqdn": "wan-r08-10017.datacenter.local",
        "management_source": "coms",
        "source_host": "oneview-01.mgmt.local",
        "source_device_id": source_device_id,
        "device_type": "router",
        "last_seen": "2026-06-18 10:00:12.696281+05:30",
        "created_at": "2026-06-18 10:00:12.696281+05:30",
        "updated_at": "2026-06-18 10:00:12.696281+05:30",
        "name": "wan-r08-10017",
        "firmware_version": "15.4(3)M3",
        "total_capacity_gb": 500,
        "free_capacity_gb": 348,
        "temperature_celsius": round(random.uniform(28.0, 45.0), 1),
        "storage_capacity_gb": 500,
        "free_storage_gb": 348,
        "memory_gb": 32,
        "cpu_cores": 4,
        "health_status": "OK",
        "power_state": "ON",
        "active_vms": 0,
        "allocated_vcpu": 4,
        "allocated_ram_gb": 16,
        "ports": json.dumps({
            "GigabitEthernet0/0": "UP",
            "GigabitEthernet0/1": "UP",
            "GigabitEthernet0/2": "DOWN",
            "Serial0/0/0": "UP"
        }),
        "configured_vlans": json.dumps([
            {"vlan_id": 1, "name": "Management"},
            {"vlan_id": 10, "name": "WAN-Link"},
            {"vlan_id": 100, "name": "Corp-LAN"}
        ]),
        "type": "router",
        "serialNumber": "wan-r08-10017",
        "model": "Cisco ISR 4431",
        "powerState": "On",
        "status": "OK",
        "state": "Configured",
        "memoryMb": 32768,
        "processorCount": 1,
        "processorCoreCount": 4,
        "processorSpeedMhz": 1700,
        "uri": f"/rest/server-hardware/{device_id}",
        "ipAddress": "10.100.1.17",
        "firmwareVersion": "15.4(3)M3",
        "cpu_utilization_percent": round(random.uniform(15.0, 65.0), 1),
        "memory_utilization_percent": round(random.uniform(20.0, 70.0), 1),
        "power_draw_watts": round(random.uniform(100.0, 250.0), 1),
    }

    columns = list(new_row.keys())
    placeholders = ", ".join(["?"] * len(columns))
    cols_str = ", ".join([f'"{c}"' for c in columns])
    values = [json.dumps(v) if isinstance(v, (dict, list)) else v for v in new_row.values()]

    conn.execute(f'INSERT OR REPLACE INTO "{TABLE}" ({cols_str}) VALUES ({placeholders})', values)
    conn.commit()
    print(f"Inserted wan-r08-10017 with id={device_id}")

# ── Step 3: Verify ─────────────────────────────────────────────────────────────
print("\n=== Verifying wan-r08-10017 ===")
row = conn.execute(
    f'SELECT serial_number, management_source, cpu_utilization_percent, memory_utilization_percent, power_draw_watts, temperature_celsius, power_state, health_status FROM "{TABLE}" WHERE serial_number = ?',
    ('wan-r08-10017',)
).fetchone()
if row:
    print(json.dumps(dict(row), default=str))
else:
    print("ERROR: Still not found!")

conn.close()

# ── Step 4: Test the mock server can find it via HTTP ─────────────────────────
print("\n=== Testing mock server HTTP lookup ===")
try:
    r = httpx.get("http://127.0.0.1:8000/rest/server-hardware/wan-r08-10017", timeout=5)
    print(f"GET /rest/server-hardware/wan-r08-10017 => {r.status_code}")
    if r.status_code == 200:
        d = r.json()
        print(f"  power_state={d.get('power_state')} cpu={d.get('cpu_utilization_percent')} mem={d.get('memory_utilization_percent')}")
    else:
        print(f"  Response: {r.text[:200]}")
except Exception as e:
    print(f"  Error: {e}")
