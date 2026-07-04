import os
import sqlite3
import glob

workspace = r"c:\AgenticAI_HPE"
mock_dirs = glob.glob(os.path.join(workspace, "mock_server(*)"))

for d in mock_dirs:
    print(f"\n--- {os.path.basename(d)} ---")
    db_files = glob.glob(os.path.join(d, "*.sqlite"))
    for db_file in db_files:
        print(f"DB: {os.path.basename(db_file)}")
        try:
            conn = sqlite3.connect(db_file)
            tables = [t[0] for t in conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()]
            print(f"Tables: {tables}")
            for t in tables:
                if 'endpoint' in t.lower() or 'route' in t.lower() or 'api' in t.lower():
                    print(f"  Found potential endpoint table: {t}")
                    columns = [c[1] for c in conn.execute(f"PRAGMA table_info({t});").fetchall()]
                    print(f"  Columns: {columns}")
                    rows = conn.execute(f"SELECT * FROM {t} LIMIT 5").fetchall()
                    for r in rows:
                        print(f"  Row: {r}")
        except Exception as e:
            print(f"Error: {e}")
