import sqlite3

db_path = r'd:\HPE CPP\MCP_Integrated\mock_server(network)\network_db.sqlite'
conn = sqlite3.connect(db_path)
print("Tables:", conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall())

print("\nIs fw-east-04-113 in dynamic_network_v1_devices?")
print(conn.execute("SELECT id FROM dynamic_network_v1_devices WHERE id='fw-east-04-113'").fetchall())
