import sqlite3
import random
import os

DB_PATHS = [
    r"d:\HPE CPP\MCP_Integrated\mock_server(Comops)\compute_ops_db.sqlite",
    r"d:\HPE CPP\MCP_Integrated\mock_server(cloud)\cloud_db.sqlite",
    r"d:\HPE CPP\MCP_Integrated\mock_server(network)\network_db.sqlite",
    r"d:\HPE CPP\MCP_Integrated\mock_server(oneview)\oneview_db.sqlite",
    r"d:\HPE CPP\MCP_Integrated\mock_server(storage)\storage_db.sqlite"
]

NEW_COLS = {
    "cpu_utilization_percent": "REAL",
    "memory_utilization_percent": "REAL",
    "power_draw_watts": "REAL",
    "temperature_celsius": "REAL"
}

def fix_db(db_path):
    if not os.path.exists(db_path):
        print(f"Skipping {db_path} - not found.")
        return

    print(f"\n=== Processing {db_path} ===")
    conn = sqlite3.connect(db_path)
    
    # Find dynamic tables
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'dynamic_%'")
    tables = [row[0] for row in cur.fetchall()]
    
    for table in tables:
        print(f"  Table: {table}")
        
        # Add columns
        existing_cols = {row[1] for row in conn.execute(f'PRAGMA table_info("{table}")').fetchall()}
        for col, col_type in NEW_COLS.items():
            if col not in existing_cols:
                conn.execute(f'ALTER TABLE "{table}" ADD COLUMN "{col}" {col_type}')
                print(f"    Added column: {col}")
        
        # Update metrics
        if "power_state" in existing_cols:
            power_col = "power_state"
        elif "powerState" in existing_cols:
            power_col = "powerState"
        else:
            power_col = None
            
        rows = conn.execute(f'SELECT id, {power_col if power_col else "NULL"}, cpu_utilization_percent FROM "{table}"').fetchall()
        
        updated = 0
        for row in rows:
            row_id, power, current_cpu = row
            
            is_off = False
            if power and str(power).upper() in ("OFF", "POWEROFF"):
                is_off = True
                
            if is_off:
                cpu, mem, watts, temp = 0.0, 0.0, 0.0, 0.0
            else:
                if current_cpu is None or current_cpu == 0.0:
                    cpu = round(random.uniform(5.0, 85.0), 1)
                    mem = round(random.uniform(10.0, 80.0), 1)
                    watts = round(random.uniform(80.0, 300.0), 1)
                    temp = round(random.uniform(25.0, 45.0), 1)
                else:
                    continue
                    
            conn.execute(
                f'UPDATE "{table}" SET cpu_utilization_percent=?, memory_utilization_percent=?, power_draw_watts=?, temperature_celsius=? WHERE id=?',
                (cpu, mem, watts, temp, row_id)
            )
            updated += 1
            
        print(f"    Updated {updated} devices.")
        
    conn.commit()
    conn.close()

if __name__ == "__main__":
    for db_path in DB_PATHS:
        fix_db(db_path)
    print("\nAll DBs fixed successfully.")
