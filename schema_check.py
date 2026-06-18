import psycopg2
import sqlite3
import pprint

dbs = [
    'mock_server(Comops)/compute_ops_db.sqlite',
    'mock_server(storage)/storage_db.sqlite',
    'mock_server(cloud)/cloud_db.sqlite',
    'mock_server(network)/network_db.sqlite',
    'mock_server(oneview)/oneview_db.sqlite'
]

print("--- Postgres CMDB ---")
conn = psycopg2.connect(dbname="hpe_agentic_ai", user="postgres", password="Mithles", host="localhost")
cur = conn.cursor()
cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'devices'")
pg_cols = [r[0] for r in cur.fetchall()]
print(pg_cols)
conn.close()

for db in dbs:
    print(f"\n--- {db} ---")
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [r[0] for r in cur.fetchall() if not r[0].startswith('sqlite_')]
        for table in tables:
            cur.execute(f"PRAGMA table_info({table})")
            sqlite_cols = [r[1] for r in cur.fetchall()]
            
            missing_in_sqlite = set(pg_cols) - set(sqlite_cols)
            missing_in_pg = set(sqlite_cols) - set(pg_cols)
            
            print(f"Table '{table}' columns:")
            print(f"   Common: {set(pg_cols) & set(sqlite_cols)}")
            print(f"   In PG but NOT in SQLite: {missing_in_sqlite}")
            print(f"   In SQLite but NOT in PG: {missing_in_pg}")
            print(f"   Raw SQLite cols: {sqlite_cols}")
        conn.close()
    except Exception as e:
        print(f"Error: {e}")
