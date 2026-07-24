import sqlite3, os, json
from pathlib import Path

total_vms = 0
for p in Path('d:/HPE CPP/MCP_Integrated').rglob('*.sqlite'):
    try:
        conn = sqlite3.connect(p)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [t[0] for t in cursor.fetchall()]
        
        db_vms = 0
        for table in tables:
            if table in ('static_store', 'collection_metadata'): continue
            try:
                cursor.execute(f"SELECT content FROM {table}")
                rows = cursor.fetchall()
                for row in rows:
                    try:
                        data = json.loads(row[0])
                        dt = data.get('device_type') or data.get('type') or ''
                        dt = dt.lower()
                        if dt == 'virtual_machine' or dt == 'vm':
                            db_vms += 1
                    except: pass
            except: pass
        if db_vms > 0:
            print(f"{p.name} has {db_vms} VMs")
            total_vms += db_vms
    except Exception as e:
        pass
print(f"Total VMs found: {total_vms}")
