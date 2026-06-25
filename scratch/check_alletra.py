import sqlite3
import json

dbs = [
    r'mock_server(Comops)\compute_ops_db.sqlite',
    r'mock_server(cloud)\cloud_db.sqlite',
    r'mock_server(network)\network_db.sqlite',
    r'mock_server(oneview)\oneview_db.sqlite',
    r'mock_server(storage)\storage_db.sqlite'
]

for db in dbs:
    try:
        conn = sqlite3.connect(db)
        conn.row_factory = sqlite3.Row
        tables = [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
        for table in tables:
            try:
                row = conn.execute(f"SELECT * FROM {table} WHERE serial_number='alletra-array-015'").fetchone()
                if row:
                    print(f"FOUND IN {db} -> {table}")
                    print(json.dumps(dict(row), indent=2))
            except Exception as e:
                pass
    except Exception as e:
        pass
