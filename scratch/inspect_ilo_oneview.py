import sqlite3, os

base = r'd:\HPE CPP\MCP_Integrated'

# iLO
for d in ['mock_server(iLO)']:
    full = os.path.join(base, d)
    for f in os.listdir(full):
        if f.endswith(('.db', '.sqlite', '.sqlite3')):
            db = os.path.join(full, f)
            conn = sqlite3.connect(db)
            q = "SELECT name FROM sqlite_master WHERE type='table'"
            tables = [r[0] for r in conn.execute(q).fetchall()]
            print(f'{d}/{f} -> tables: {tables[:10]}')
            for t in tables[:5]:
                cols = [c[1] for c in conn.execute(f'PRAGMA table_info("{t}")').fetchall()]
                count = conn.execute(f'SELECT COUNT(*) FROM "{t}"').fetchone()[0]
                print(f'  {t}: cols={cols}, count={count}')
                row = conn.execute(f'SELECT * FROM "{t}" LIMIT 1').fetchone()
                if row:
                    print(f'  SAMPLE: {row}')
            conn.close()

# Oneview
for d in ['mock_server(oneview)']:
    full = os.path.join(base, d)
    for f in os.listdir(full):
        if f.endswith(('.db', '.sqlite', '.sqlite3')):
            db = os.path.join(full, f)
            conn = sqlite3.connect(db)
            q = "SELECT name FROM sqlite_master WHERE type='table'"
            tables = [r[0] for r in conn.execute(q).fetchall()]
            print(f'\n{d}/{f} -> tables: {tables[:10]}')
            for t in tables[:5]:
                cols = [c[1] for c in conn.execute(f'PRAGMA table_info("{t}")').fetchall()]
                count = conn.execute(f'SELECT COUNT(*) FROM "{t}"').fetchone()[0]
                print(f'  {t}: cols={cols}, count={count}')
                row = conn.execute(f'SELECT * FROM "{t}" LIMIT 1').fetchone()
                if row:
                    print(f'  SAMPLE: {row}')
            conn.close()
