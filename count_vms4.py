import sqlite3, json, os
from pathlib import Path

total_vms = 0
for p in Path('d:/HPE CPP/MCP_Integrated').rglob('*.sqlite'):
    try:
        conn = sqlite3.connect(p)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [t[0] for t in cursor.fetchall()]
        
        for table in tables:
            if table in ('static_store', 'collection_metadata'): continue
            try:
                cursor.execute(f"SELECT * FROM {table}")
                rows = cursor.fetchall()
                table_vms = 0
                for row in rows:
                    item = dict(row)
                    
                    if 'content' in item:
                        try:
                            data = json.loads(item['content'])
                            item.update(data)
                        except: pass
                    
                    dt = item.get('device_type') or item.get('type') or ''
                    dt = str(dt).lower()
                    if dt == 'virtual_machine' or dt == 'vm':
                        table_vms += 1
                if table_vms > 0:
                    print(f"{p.name} - {table} has {table_vms} VMs")
                    total_vms += table_vms
            except: pass
    except Exception as e:
        pass
print(f"Total VMs found: {total_vms}")
