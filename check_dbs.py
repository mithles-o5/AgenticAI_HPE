import sqlite3
import os

def check_db(name, path):
    print(f"--- Checking {name} ---")
    if not os.path.exists(path):
        print(path, 'does not exist')
        return
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cur.fetchall()
    print('Tables:', tables)
    for t in tables:
        cur.execute(f"SELECT count(1) FROM {t[0]}")
        print(f"{t[0]}: {cur.fetchone()[0]}")
    conn.close()

check_db("OneView", "mock_server(oneview)/oneview_db.sqlite")
check_db("iLO", "mock_server(iLO)/ilo_mock_db.sqlite")
check_db("ComOps", "mock_server(Comops)/comops_mock_db.sqlite")
check_db("Storage", "mock_server(Storage)/storage_mock_db.sqlite")
check_db("Cloud", "mock_server(Cloud)/cloud_mock_db.sqlite")
check_db("Network", "mock_server(Network)/network_mock_db.sqlite")
