import sqlite3, json
conn = sqlite3.connect('d:/HPE CPP/MCP_Integrated/mock_server(storage)/storage_db.sqlite')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()
cursor.execute('SELECT name FROM sqlite_master WHERE type="table"')
tables = [t[0] for t in cursor.fetchall()]
for table in tables:
    if table in ('static_store', 'collection_metadata'): continue
    cursor.execute(f'SELECT * FROM {table}')
    for row in cursor.fetchall():
        item = dict(row)
        if 'content' in item:
            try: item.update(json.loads(item['content']))
            except: pass
        if item.get('name') == 'nimble-prod-009' or item.get('id') == 'nimble-prod-009':
            print(f"Found in {table}! device_type: {item.get('device_type')}, type: {item.get('type')}")
