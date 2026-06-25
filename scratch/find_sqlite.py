import sqlite3

dbs = [
    r'mock_server(Comops)\compute_ops_db.sqlite',
    r'mock_server(cloud)\cloud_db.sqlite',
    r'mock_server(network)\network_db.sqlite',
    r'mock_server(oneview)\oneview_db.sqlite',
    r'mock_server(storage)\storage_db.sqlite'
]

found = False
for db in dbs:
    try:
        conn = sqlite3.connect(db)
        tables = [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'dynamic_%'").fetchall()]
        for table in tables:
            try:
                if conn.execute(f'SELECT 1 FROM "{table}" WHERE serial_number="ms-dsk-219"').fetchone():
                    print(f'Found in {db} -> {table}')
                    found = True
            except:
                pass
    except Exception as e:
        pass

if not found:
    print('Not found in any SQLite DB')
