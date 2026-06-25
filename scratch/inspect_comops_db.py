import sqlite3, json

# ── Inspect compute_ops_db.sqlite ─────────────────────────────────────────────
DB = 'd:/HPE CPP/MCP_Integrated/mock_server(Comops)/compute_ops_db.sqlite'
conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row

# Show tables
tables = [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
print("=== Tables in compute_ops_db.sqlite ===")
for t in tables:
    count = conn.execute(f'SELECT COUNT(*) FROM "{t}"').fetchone()[0]
    print(f"  {t}  ({count} rows)")

# Find wan-r08-10017
print("\n=== Searching for wan-r08-10017 ===")
for t in tables:
    rows = conn.execute(f'SELECT * FROM "{t}"').fetchall()
    for row in rows:
        d = dict(row)
        vals = " ".join(str(v) for v in d.values()).lower()
        if "wan-r08-10017" in vals:
            print(f"\n  TABLE: {t}")
            print(f"  ROW: {json.dumps(d, default=str)}")
            break

# Show schema of the table that has wan-r08-10017
print("\n=== Schema of first matching table ===")
for t in tables:
    rows = conn.execute(f'SELECT * FROM "{t}"').fetchall()
    for row in rows:
        d = dict(row)
        vals = " ".join(str(v) for v in d.values()).lower()
        if "wan-r08-10017" in vals:
            print(f"  Columns: {list(d.keys())}")
            break
    else:
        continue
    break

conn.close()
