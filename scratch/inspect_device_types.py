import sqlite3, os

base = r'd:\HPE CPP\MCP_Integrated'
dirs = [
    'mock_server(iLO)',
    'mock_server(Comops)',
    'mock_server(cloud)',
    'mock_server(oneview)',
    'mock_server(network)',
    'mock_server(storage)',
]

for d in dirs:
    full = os.path.join(base, d)
    for f in os.listdir(full):
        if f.endswith(('.db', '.sqlite', '.sqlite3')):
            db = os.path.join(full, f)
            conn = sqlite3.connect(db)
            q = "SELECT name FROM sqlite_master WHERE type='table'"
            tables = [r[0] for r in conn.execute(q).fetchall()]
            for t in tables:
                if 'device' in t.lower():
                    cols_q = f'PRAGMA table_info("{t}")'
                    cols = [c[1] for c in conn.execute(cols_q).fetchall()]
                    if 'device_type' in cols:
                        types_q = f'SELECT DISTINCT device_type FROM "{t}"'
                        types = [r[0] for r in conn.execute(types_q).fetchall()]
                        count_q = f'SELECT COUNT(*) FROM "{t}"'
                        count = conn.execute(count_q).fetchone()[0]
                        print(f'{d}/{f} -> table={t} count={count}')
                        print(f'  device_types: {types}')
            conn.close()
