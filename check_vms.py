import sqlite3, json, os
from pathlib import Path
conn = sqlite3.connect('d:/HPE CPP/MCP_Integrated/mock_server(cloud)/cloud_db.sqlite')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()
cursor.execute('SELECT * FROM dynamic_api_v1_devices')
for row in cursor.fetchall():
    item = dict(row)
    if 'content' in item:
        try: item.update(json.loads(item['content']))
        except: pass
    dt = str(item.get('device_type') or item.get('type') or '').lower()
    if dt in ('virtual_machine', 'vm'):
        print(f"{item.get('id', 'unknown')}: {dt}")
