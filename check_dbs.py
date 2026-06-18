import psycopg2
import sqlite3

print("--- POSTGRES DB ---")
try:
    conn = psycopg2.connect(dbname='hpe_agentic_ai', user='postgres', host='localhost')
    cur = conn.cursor()
    cur.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'devices';")
    print([row[0] for row in cur.fetchall()])
    conn.close()
except Exception as e:
    print(f"Postgres Error: {e}")

dbs = {
    "Comops": r"d:\HPE CPP\MCP_Integrated\mock_server(Comops)\compute_ops_db.sqlite",
    "Storage": r"d:\HPE CPP\MCP_Integrated\mock_server(storage)\storage_db.sqlite",
    "Cloud": r"d:\HPE CPP\MCP_Integrated\mock_server(cloud)\cloud_db.sqlite",
    "Network": r"d:\HPE CPP\MCP_Integrated\mock_server(network)\network_db.sqlite"
}

for name, path in dbs.items():
    print(f"\n--- {name} SQLITE DB ---")
    try:
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cur.fetchall()]
        for table in tables:
            cur.execute(f"PRAGMA table_info({table});")
            cols = [row[1] for row in cur.fetchall()]
            print(f"Table '{table}': {cols}")
        conn.close()
    except Exception as e:
        print(f"SQLite Error: {e}")
