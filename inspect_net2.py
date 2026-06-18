import sqlite3

db_path = r'd:\HPE CPP\MCP_Integrated\mock_server(network)\network_db.sqlite'
conn = sqlite3.connect(db_path)
tables = [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
print("Tables:", tables)

for t in tables:
    if t.startswith('dynamic_'):
        print(f"--- {t} ---")
        try:
            ids = [r[0] for r in conn.execute(f"SELECT id FROM {t}").fetchall()]
            print("IDs:", ids)
        except Exception as e:
            print("Error reading ids:", e)
