"""
Restore 199 deleted device records from devices.csv back into ilo_db.sqlite
Skips rows already present (by id) to avoid duplicates.
"""
import sqlite3
import csv

DB_PATH = "mock_server(iLO)/ilo_db.sqlite"
CSV_PATH = "mock_server(iLO)/devices.csv"

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# Get existing IDs
c.execute("SELECT id FROM dynamic_redfish_v1_systems")
existing_ids = {row[0] for row in c.fetchall()}
print(f"Existing records in DB: {len(existing_ids)}")

inserted = 0
skipped = 0

with open(CSV_PATH, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        rid = row["id"]
        if rid in existing_ids:
            skipped += 1
            continue

        odata_id = f"/redfish/v1/systems/{rid}"

        c.execute("""
            INSERT INTO dynamic_redfish_v1_systems (
                action, name, id, "@odata.id", "@odata.type",
                SystemType, Manufacturer, Model, SerialNumber, UUID,
                PowerState, Status, Bios, Processors, Memory, Storage,
                power_state, ip_address, fqdn, management_source,
                source_host, source_device_id, device_type,
                last_seen, created_at, updated_at,
                firmware_version, total_capacity, free_capacity,
                temperature, storage_utilization, free_storage,
                memory_utilization, cpu_cores, health_status,
                active_vms, allocated_cpu, allocated_memory,
                ports, configured_vlans, cpu_utilization,
                memory_usage, power_draw, serial_number, temperature_celsius
            ) VALUES (
                NULL, ?, ?, ?, NULL,
                NULL, 'HPE', NULL, ?, ?,
                ?, NULL, NULL, NULL, NULL, NULL,
                ?, ?, ?, ?,
                ?, ?, ?,
                ?, ?, ?,
                ?, ?, ?,
                ?, ?, ?,
                ?, ?, ?,
                ?, ?, ?,
                ?, ?, ?,
                ?, ?, ?, NULL
            )
        """, (
            row["serial_number"],           # name
            rid,                            # id
            odata_id,                       # @odata.id
            row["serial_number"],           # SerialNumber
            rid,                            # UUID
            row["power_state"].upper(),     # PowerState (Redfish style)
            row["power_state"],             # power_state
            row["ip_address"],              # ip_address
            row["fqdn"],                    # fqdn
            row["management_source"],       # management_source
            row["source_host"],             # source_host
            row["source_device_id"],        # source_device_id
            row["device_type"],             # device_type
            row["last_seen"],               # last_seen
            row["created_at"],              # created_at
            row["updated_at"],              # updated_at
            row["firmware_version"],        # firmware_version
            row["total_capacity"],          # total_capacity
            row["free_capacity"],           # free_capacity
            row["temperature"],             # temperature
            row["storage_utilization"],     # storage_utilization
            row["free_storage"],            # free_storage
            row["memory_utilization"],      # memory_utilization
            row["cpu_cores"],               # cpu_cores
            row["health_status"],           # health_status
            row["active_vms"],              # active_vms
            row["allocated_cpu"],           # allocated_cpu
            row["allocated_memory"],        # allocated_memory
            row["ports"],                   # ports
            row["configured_vlans"],        # configured_vlans
            row["cpu_utilization"],         # cpu_utilization
            row["memory_usage"],            # memory_usage
            row["power_draw"],              # power_draw
            row["serial_number"],           # serial_number
        ))
        inserted += 1

conn.commit()

# Final count
c.execute("SELECT COUNT(*) FROM dynamic_redfish_v1_systems")
total = c.fetchone()[0]

# Verify esx-host-155 is back
c.execute("SELECT id, name, ip_address, power_state, health_status FROM dynamic_redfish_v1_systems WHERE name LIKE '%esx-host-155%' OR id LIKE '%esx-host-155%'")
esx = c.fetchall()
print(f"esx-host-155 found: {esx}")

conn.close()

print(f"Inserted: {inserted}")
print(f"Skipped (already existed): {skipped}")
print(f"Total records now: {total}")
