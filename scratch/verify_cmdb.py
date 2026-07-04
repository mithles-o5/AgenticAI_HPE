import sys
import os

sys.path.insert(0, r"c:\AgenticAI_HPE\resource_resolver")
from db import db_manager

def main():
    conn = db_manager.get_connection()
    if not conn:
        print("Failed to connect to database.")
        return

    cur = conn.cursor()
    
    print("--- CMDB DEVICES TABLE ---")
    cur.execute("SELECT DISTINCT management_source FROM devices;")
    sources = [r[0] for r in cur.fetchall()]
    print(f"Distinct management_source: {sources}")
    
    cur.execute("SELECT DISTINCT device_type FROM devices;")
    dtypes = [r[0] for r in cur.fetchall()]
    print(f"Distinct device_type: {dtypes}")
    
    print("\n--- ENDPOINT REGISTRY TABLE ---")
    cur.execute("SELECT DISTINCT vendor FROM endpoint_registry;")
    vendors = [r[0] for r in cur.fetchall()]
    print(f"Distinct vendor: {vendors}")
    
    cur.execute("SELECT DISTINCT device_type FROM endpoint_registry;")
    ep_dtypes = [r[0] for r in cur.fetchall()]
    print(f"Distinct device_type (registry): {len(ep_dtypes)} items, e.g. {ep_dtypes[:10]}")
    
    cur.execute("SELECT DISTINCT action_key FROM endpoint_registry;")
    action_keys = [r[0] for r in cur.fetchall()]
    print(f"Distinct action_key: {action_keys}")
    
    cur.execute("SELECT vendor, COUNT(*) FROM endpoint_registry GROUP BY vendor;")
    counts = cur.fetchall()
    print("\nEndpoint count per provider:")
    for row in counts:
        print(f"  {row[0]}: {row[1]}")
        
    cur.close()
    db_manager.return_connection(conn)

if __name__ == "__main__":
    main()
