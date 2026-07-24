import sqlite3

conn = sqlite3.connect('mock_server(storage)/storage_db.sqlite')
cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cur.fetchall()
print('Tables:', tables)
for t in tables:
    cur.execute(f"SELECT count(1) FROM {t[0]}")
    print(f"{t[0]}: {cur.fetchone()[0]}")
    
    cur.execute(f"PRAGMA table_info({t[0]})")
    cols = [c[1] for c in cur.fetchall()]
    
    where_clauses = []
    if 'name' in cols:
        where_clauses.append("name LIKE '%nimble-prod-009%'")
    if 'id' in cols:
        where_clauses.append("id LIKE '%nimble-prod-009%'")
        
    if where_clauses:
        query = f"SELECT * FROM {t[0]} WHERE " + " OR ".join(where_clauses)
        cur.execute(query)
        res = cur.fetchall()
        if res:
            print(f"Found in {t[0]}: {res}")
            
    # Also just dump all rows from dynamic_data_services_v1beta1_devices to see what is there
    if t[0] == 'dynamic_data_services_v1beta1_devices':
        print(f"--- DUMP {t[0]} ---")
        cur.execute(f"SELECT * FROM {t[0]} LIMIT 10")
        for r in cur.fetchall():
            print(r)

conn.close()
