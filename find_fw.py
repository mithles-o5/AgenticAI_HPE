import sqlite3
import os

base_dir = r'd:\HPE CPP\MCP_Integrated'
mock_servers = ["mock_server(cloud)", "mock_server(Comops)", "mock_server(network)", "mock_server(oneview)", "mock_server(storage)"]

for srv in mock_servers:
    db_name = srv.replace("mock_server(", "").replace(")", "").lower() + "_db.sqlite"
    if srv == "mock_server(Comops)":
        # special case for compute ops? Wait, it has two DBs maybe.
        pass
    db_path = os.path.join(base_dir, srv, db_name)
    if not os.path.exists(db_path):
        continue
    conn = sqlite3.connect(db_path)
    tables = [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
    for t in tables:
        if t.startswith('dynamic_'):
            try:
                ids = [r[0] for r in conn.execute(f"SELECT id FROM {t}").fetchall()]
                if 'fw-east-04-113' in ids:
                    print(f"FOUND in {srv} -> {t}")
            except Exception as e:
                pass
