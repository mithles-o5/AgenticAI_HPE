import sqlite3

conn = sqlite3.connect(r'd:\HPE CPP\MCP_Integrated\mock_server(Comops)\compute_ops_db.sqlite')
tables = [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
for t in tables:
    if t.startswith('dynamic_'):
        try:
            ids = [r[0] for r in conn.execute(f"SELECT id FROM {t}").fetchall()]
            if 'fw-east-04-113' in ids:
                print(f"FOUND in {t}")
        except Exception as e:
            pass
