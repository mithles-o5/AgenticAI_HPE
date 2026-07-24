import sqlite3
conn = sqlite3.connect('d:/HPE CPP/MCP_Integrated/mock_server(cloud)/cloud_db.sqlite')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
print([t[0] for t in cursor.fetchall()])
