import sqlite3
db = sqlite3.connect('network_db.sqlite')
cur = db.cursor()
cur.execute("SELECT device_type, COUNT(*) FROM dynamic_network_v1_devices GROUP BY device_type ORDER BY COUNT(*) DESC")
print("Device types:")
for r in cur.fetchall():
    print(f"  {r[0]}: {r[1]}")
print()
# Get sample device IDs per type
for dtype in ['switch', 'router', 'gateway', 'access_point', 'firewall']:
    cur.execute(f"SELECT id, serial_number, ip_address, health_status, power_state FROM dynamic_network_v1_devices WHERE device_type=? LIMIT 3", (dtype,))
    rows = cur.fetchall()
    if rows:
        print(f"{dtype} samples:")
        for r in rows:
            print(f"  id={r[0]}, sn={r[1]}, ip={r[2]}, health={r[3]}, power={r[4]}")
db.close()
