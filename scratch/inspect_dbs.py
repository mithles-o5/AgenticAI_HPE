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
            print(f'\n=== {d}/{f} ===  tables={tables}')
            for t in tables:
                cols_q = f'PRAGMA table_info("{t}")'
                cols = [c[1] for c in conn.execute(cols_q).fetchall()]
                row_q = f'SELECT * FROM "{t}" LIMIT 1'
                row = conn.execute(row_q).fetchone()
                print(f'  TABLE: {t}')
                print(f'  COLS:   {cols}')
                if row:
                    print(f'  SAMPLE: {row}')
            conn.close()
