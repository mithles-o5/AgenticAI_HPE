import sqlite3
db = sqlite3.connect('network_db.sqlite')
cur = db.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [r[0] for r in cur.fetchall()]
print("TABLES:", tables)
for t in tables[:5]:
    cur.execute(f"SELECT COUNT(*) FROM [{t}]")
    count = cur.fetchone()[0]
    print(f"  {t}: {count} rows")
    if count > 0:
        cur.execute(f"SELECT * FROM [{t}] LIMIT 1")
        row = cur.fetchone()
        cols = [d[0] for d in cur.description]
        print(f"  Columns: {cols}")
        print(f"  Sample: {dict(zip(cols, row))}")
db.close()
