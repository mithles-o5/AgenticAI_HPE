import sqlite3
import json

db_path = r"c:\AgenticAI_HPE\mock_server(iLO)\ilo_db.sqlite"
conn = sqlite3.connect(db_path)
cur = conn.cursor()

cur.execute("SELECT key, length(value) FROM static_store WHERE key LIKE '%systems%' OR key LIKE '%chassis%'")
rows = cur.fetchall()
print(f"Matching keys in static_store ({len(rows)}):")
for r in rows[:20]:
    print(f"  Key: {r[0]}, value length: {r[1]}")

# Let's print the value of one key to see what a detailed Redfish system looks like
cur.execute("SELECT value FROM static_store WHERE key = 'get_redfish_v1_systems_system_id'")
val = cur.fetchone()
if val:
    data = json.loads(val[0])
    print("\n--- Example system detail (get_redfish_v1_systems_system_id) ---")
    print(json.dumps(data, indent=2))
else:
    print("\nNo key 'get_redfish_v1_systems_system_id' found.")

conn.close()
