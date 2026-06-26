import psycopg2
import psycopg2.extras
import sqlite3
import os

PG_DB = "hpe_agentic_ai"
PG_USER = "postgres"
PG_HOST = "localhost"

# Map of SQLite DBs
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQLITE_DBS = {
    "Comops": os.path.join(BASE_DIR, "mock_server(Comops)", "compute_ops_db.sqlite"),
    "Storage": os.path.join(BASE_DIR, "mock_server(storage)", "storage_db.sqlite"),
    "Cloud": os.path.join(BASE_DIR, "mock_server(cloud)", "cloud_db.sqlite"),
    "Network": os.path.join(BASE_DIR, "mock_server(network)", "network_db.sqlite"),
    "OneView": os.path.join(BASE_DIR, "mock_server(oneview)", "oneview_db.sqlite"),
    "iLO": os.path.join(BASE_DIR, "mock_server(iLO)", "ilo_db.sqlite")
}

# Column mappings: if SQLite has the right-side column, update it using Postgres's left-side column
COL_MAPPING = {
    'ip_address': ['ip_address', 'ipAddress'],
    'serial_number': ['serial_number', 'serialNumber', 'id'], # Map to id for Redfish systems where id contains the serial
    'device_type': ['device_type', 'type'],
    'fqdn': ['fqdn', 'hostname'],
    'management_source': ['management_source'],
    'source_host': ['source_host'],
    'source_device_id': ['source_device_id'],
    'last_seen': ['last_seen'],
    'created_at': ['created_at'],
    'updated_at': ['updated_at']
}

def get_postgres_data():
    conn = psycopg2.connect(dbname=PG_DB, user=PG_USER, password="mithles", host=PG_HOST)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM devices")
    rows = cur.fetchall()
    
    pg_data = {}
    for row in rows:
        row_dict = dict(row)
        if 'serial_number' in row_dict and row_dict['serial_number']:
            pg_data[row_dict['serial_number']] = row_dict
            
    conn.close()
    return pg_data

def sync_sqlite_db(name, path, pg_data):
    if not os.path.exists(path):
        print(f"[{name}] File not found: {path}")
        return 0

    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [r[0] for r in cur.fetchall() if not r[0].startswith('sqlite_')]
    
    total_updated = 0
    
    for table in tables:
        cur.execute(f"PRAGMA table_info({table})")
        columns = [r[1] for r in cur.fetchall()]
        
        # Determine which column serves as the serial identifier in this table
        serial_col = None
        for cand in ['serial_number', 'serialNumber', 'SerialNumber']:
            if cand in columns:
                serial_col = cand
                break
                
        if not serial_col:
            continue
            
        # Determine which columns to update
        updates = []  # List of tuples: (sqlite_col_name, pg_col_name)
        for pg_col, sqlite_candidates in COL_MAPPING.items():
            if pg_col == 'serial_number': 
                continue # don't update the PK
            for cand in sqlite_candidates:
                if cand in columns:
                    updates.append((cand, pg_col))
                    
        if not updates:
            print(f"[{name}] No overlapping columns to update in '{table}'.")
            continue
            
        cur.execute(f"SELECT {serial_col} FROM {table}")
        sqlite_serials = [r[serial_col] for r in cur.fetchall() if r[serial_col]]
        
        table_updates = 0
        for serial in sqlite_serials:
            if serial in pg_data:
                pg_row = pg_data[serial]
                
                set_clause = ", ".join([f"{sqlite_col} = ?" for sqlite_col, _ in updates])
                values = [pg_row[pg_col] for _, pg_col in updates]
                values.append(serial)
                
                query = f"UPDATE {table} SET {set_clause} WHERE {serial_col} = ?"
                cur.execute(query, values)
                table_updates += 1
                total_updated += 1
                
        print(f"[{name}] Updated {table_updates} rows in '{table}'.")
                
    conn.commit()
    conn.close()
    print(f"[{name}] Total updated: {total_updated} rows.")
    return total_updated

if __name__ == "__main__":
    try:
        print("Fetching CMDB data from Postgres...")
        pg_data = get_postgres_data()
        print(f"Found {len(pg_data)} records in Postgres with valid serial_number.")
        
        grand_total = 0
        for name, path in SQLITE_DBS.items():
            print(f"\n--- Syncing {name} ---")
            updated = sync_sqlite_db(name, path, pg_data)
            if updated:
                grand_total += updated
                
        print(f"\nSynchronization complete. Total records updated across all DBs: {grand_total}")
        
    except Exception as e:
        print(f"Error: {e}")
