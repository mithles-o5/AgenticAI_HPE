"""
Cleanup script for ilo_db.sqlite:
1. Remove old 199 device records (created 2026-06-25)
2. Keep the newer record (dl360-prod-101, created 2026-06-26)
3. The newer record already follows the correct schema columns
"""
import sqlite3
import json
from datetime import datetime

DB_PATH = "mock_server(iLO)/ilo_db.sqlite"
OLD_CREATED_AT = "2026-06-25 21:48:53.77919+05:30"

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

print("=" * 60)
print("iLO Database Cleanup")
print("=" * 60)

# 1. Count before
c.execute("SELECT COUNT(*) FROM dynamic_redfish_v1_systems")
count_before = c.fetchone()[0]
print(f"\nBefore cleanup: {count_before} records")

# 2. Show what we're keeping
c.execute("SELECT id, name, ip_address, created_at FROM dynamic_redfish_v1_systems WHERE created_at != ?", (OLD_CREATED_AT,))
keepers = c.fetchall()
print(f"\nRecords to KEEP ({len(keepers)}):")
for row in keepers:
    print(f"  id={row[0]}, name={row[1]}, ip={row[2]}, created_at={row[3]}")

# 3. Delete old records
c.execute("DELETE FROM dynamic_redfish_v1_systems WHERE created_at = ?", (OLD_CREATED_AT,))
deleted = c.rowcount
print(f"\nDeleted {deleted} old records.")

# 4. Count after
c.execute("SELECT COUNT(*) FROM dynamic_redfish_v1_systems")
count_after = c.fetchone()[0]
print(f"After cleanup: {count_after} records")

# 5. Show remaining records
print("\nRemaining records in dynamic_redfish_v1_systems:")
c.execute("SELECT id, name, ip_address, power_state, health_status, created_at FROM dynamic_redfish_v1_systems")
rows = c.fetchall()
for row in rows:
    print(f"  id={row[0]}, name={row[1]}, ip={row[2]}, power={row[3]}, health={row[4]}, created={row[5]}")

conn.commit()
conn.close()

print("\n✅ Cleanup complete. Database committed.")
