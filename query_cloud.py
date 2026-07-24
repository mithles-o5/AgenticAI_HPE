import sqlite3, json
conn = sqlite3.connect('d:/HPE CPP/MCP_Integrated/mock_server(cloud)/cloud_db.sqlite')
cursor = conn.cursor()
try:
    cursor.execute('SELECT content FROM dynamic_cloud_v1_inventory')
    types = {}
    for row in cursor.fetchall():
        data = json.loads(row[0])
        dt = data.get('device_type') or data.get('type')
        types[dt] = types.get(dt, 0) + 1
    print(types)
except Exception as e:
    cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='dynamic_cloud_v1_inventory'")
    print(cursor.fetchone())
