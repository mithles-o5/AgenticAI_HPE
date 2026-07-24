import sqlite3, os
from pathlib import Path
for p in Path('d:/HPE CPP/MCP_Integrated').rglob('*.sqlite'):
    if 'cloud' not in str(p).lower() and 'com' not in str(p).lower(): continue
    print(f'Checking {p}')
    try:
        conn = sqlite3.connect(p)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        for t in tables:
            cursor.execute(f'SELECT COUNT(*) FROM {t[0]}')
            count = cursor.fetchone()[0]
            print(f'  {t[0]}: {count} rows')
    except Exception as e:
        print(f'Error: {e}')
