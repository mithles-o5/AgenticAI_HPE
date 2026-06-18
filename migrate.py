import os
import re
import sys

DATABASE_PY_TEMPLATE = '''import sqlite3
import json
import os
import threading

class Database:
    def __init__(self, db_path):
        self.db_path = db_path
        self._lock = threading.RLock()
        self._init_db()

    def _init_db(self):
        with self._lock:
            conn = sqlite3.connect(self.db_path, check_same_thread=False)
            conn.execute("CREATE TABLE IF NOT EXISTS static_store (key TEXT PRIMARY KEY, value TEXT)")
            conn.execute("CREATE TABLE IF NOT EXISTS collection_metadata (table_name TEXT PRIMARY KEY, collection_path TEXT)")
            conn.commit()
            conn.close()

    def _get_table_name(self, collection_path):
        parts = [p for p in collection_path.split('/') if p]
        return "dynamic_" + "_".join(parts).replace("-", "_")

    def _ensure_table(self, conn, table_name, data):
        if not data:
            return
        keys = list(data.keys())
        if "id" not in keys: keys.append("id")
        
        # Create table if not exists
        cols = []
        for k in keys:
            primary_key = " PRIMARY KEY" if k == "id" else ""
            cols.append(f'"{k}" TEXT{primary_key}')
        conn.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(cols)})")
        
        # Add missing columns
        cursor = conn.execute(f"PRAGMA table_info({table_name})")
        existing_cols = {row[1] for row in cursor.fetchall()}
        for k in data.keys():
            if k not in existing_cols:
                conn.execute(f'ALTER TABLE {table_name} ADD COLUMN "{k}" TEXT')

    def get_collection(self, collection_path):
        table_name = self._get_table_name(collection_path)
        with self._lock:
            conn = sqlite3.connect(self.db_path, check_same_thread=False)
            conn.row_factory = sqlite3.Row
            try:
                cursor = conn.execute(f"SELECT * FROM {table_name}")
                rows = cursor.fetchall()
                results = {}
                for r in rows:
                    item = dict(r)
                    for k, v in item.items():
                        if isinstance(v, str) and (v.startswith("{") or v.startswith("[")):
                            try:
                                item[k] = json.loads(v)
                            except: pass
                    if "id" in item:
                        results[item["id"]] = item
                return results
            except sqlite3.OperationalError:
                return {} # Table doesn't exist yet
            finally:
                conn.close()

    def get_all(self, collection_path):
        return list(self.get_collection(collection_path).values())

    def get_item(self, collection_path, item_id):
        table_name = self._get_table_name(collection_path)
        with self._lock:
            conn = sqlite3.connect(self.db_path, check_same_thread=False)
            conn.row_factory = sqlite3.Row
            try:
                cursor = conn.execute(f"SELECT * FROM {table_name} WHERE id = ?", (item_id,))
                row = cursor.fetchone()
                if not row: return None
                item = dict(row)
                for k, v in item.items():
                    if isinstance(v, str) and (v.startswith("{") or v.startswith("[")):
                        try:
                            item[k] = json.loads(v)
                        except: pass
                return item
            except sqlite3.OperationalError:
                return None
            finally:
                conn.close()

    def upsert_item(self, collection_path, item_id, payload_dict):
        table_name = self._get_table_name(collection_path)
        if "id" not in payload_dict:
            payload_dict["id"] = item_id
            
        with self._lock:
            conn = sqlite3.connect(self.db_path, check_same_thread=False)
            try:
                # Ensure metadata exists
                conn.execute(
                    "INSERT OR IGNORE INTO collection_metadata (table_name, collection_path) VALUES (?, ?)",
                    (table_name, collection_path)
                )
                
                self._ensure_table(conn, table_name, payload_dict)
                
                columns = list(payload_dict.keys())
                placeholders = ", ".join(["?"] * len(columns))
                cols_str = ", ".join([f'"{c}"' for c in columns])
                
                values = []
                for c in columns:
                    val = payload_dict[c]
                    if isinstance(val, (dict, list)):
                        val = json.dumps(val)
                    elif isinstance(val, bool):
                        val = 1 if val else 0
                    values.append(val)
                
                conn.execute(f"INSERT OR REPLACE INTO {table_name} ({cols_str}) VALUES ({placeholders})", values)
                conn.commit()
            finally:
                conn.close()

    def delete_item(self, collection_path, item_id):
        table_name = self._get_table_name(collection_path)
        with self._lock:
            conn = sqlite3.connect(self.db_path, check_same_thread=False)
            try:
                # Fetch first
                conn.row_factory = sqlite3.Row
                cursor = conn.execute(f"SELECT * FROM {table_name} WHERE id = ?", (item_id,))
                row = cursor.fetchone()
                if row:
                    conn.execute(f"DELETE FROM {table_name} WHERE id = ?", (item_id,))
                    conn.commit()
                    return dict(row)
                return None
            except sqlite3.OperationalError:
                return None
            finally:
                conn.close()
                
    def get_static(self, key, default=None):
        if default is None:
            default = {}
        with self._lock:
            conn = sqlite3.connect(self.db_path, check_same_thread=False)
            try:
                cursor = conn.execute("SELECT value FROM static_store WHERE key = ?", (key,))
                row = cursor.fetchone()
                if row:
                    return json.loads(row[0])
                return default
            except sqlite3.OperationalError:
                return default
            finally:
                conn.close()

db_path = os.path.join(os.path.dirname(__file__), os.path.basename(os.path.dirname(__file__)).replace("mock_server(", "").replace(")", "").lower() + "_db.sqlite")
db = Database(db_path)
'''

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Replace imports
    content = re.sub(
        r'(import sys\s+sys\.path\.insert.*?from db_store import MOCK_DB(\n\s*mock_file.*?get_db_store.*?\n)?)',
        'from database import db',
        content,
        flags=re.DOTALL
    )
    content = re.sub(r'from db_store import get_db_store.*?MOCK_DB = get_db_store.*?\n', 'from database import db\n', content, flags=re.DOTALL)
    content = re.sub(r'from db_store import MOCK_DB\n', 'from database import db\n', content)

    # 2. Pattern: Getting list of items
    # dynamic_items = list(MOCK_DB.get("dynamic_store", {}).get(collection_path, {}).values())
    content = re.sub(
        r'list\(\s*MOCK_DB\.get\(\s*"dynamic_store"\s*,\s*\{\}\s*\)\.get\(\s*collection_path\s*,\s*\{\}\s*\)\.values\(\s*\)\s*\)',
        'db.get_all(collection_path)',
        content
    )
    
    # 3. Pattern: Getting single item direct return
    content = re.sub(
        r'if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB\["dynamic_store"\] and item_id in MOCK_DB\["dynamic_store"\]\[collection_path\]:\s+return MOCK_DB\["dynamic_store"\]\[collection_path\]\[item_id\]',
        'item = db.get_item(collection_path, item_id)\n    if item:\n        return item',
        content
    )
    
    # 4. Pattern: Getting store dictionary
    content = re.sub(
        r'store = MOCK_DB\.get\(\s*"dynamic_store"\s*,\s*\{\}\s*\)\.get\(\s*collection_path\s*,\s*\{\}\s*\)',
        'store = db.get_collection(collection_path)',
        content
    )
    
    # 5. Pattern: Creation init block
    init_block_pattern = r'''\s*if "dynamic_store" not in MOCK_DB:
\s*MOCK_DB\["dynamic_store"\] = \{\}
\s*if collection_path not in MOCK_DB\["dynamic_store"\]:
\s*MOCK_DB\["dynamic_store"\]\[collection_path\] = \{\}'''
    content = re.sub(init_block_pattern, '', content)

    # 6. Pattern: Saving item
    content = re.sub(
        r'MOCK_DB\["dynamic_store"\]\[collection_path\]\[(item_id|id)\] = (payload_dict|existing|device)',
        r'db.upsert_item(collection_path, \1, \2)',
        content
    )
    
    # 7. Pattern: Deleting item
    content = re.sub(
        r'deleted = MOCK_DB\["dynamic_store"\]\[collection_path\]\.pop\((item_id|id)\)',
        r'deleted = db.delete_item(collection_path, \1)',
        content
    )
    
    # 8. Pattern: Static data GET
    content = re.sub(
        r'MOCK_DB\.get\(\s*"([^"]+)"\s*,\s*dict\(\)\s*\)',
        r'db.get_static("\1", dict())',
        content
    )
    
    # Edge case: static item check in oneview main.py
    content = re.sub(
        r'static_list = MOCK_DB\.get\("([^"]+)",\s*\{\}\)\.get\("members",\s*\[\]\)',
        r'static_list = db.get_static("\1").get("members", [])',
        content
    )
    content = re.sub(
        r'MOCK_DB\.get\("([^"]+)",\s*\{\}\)\.get\("id"\)',
        r'db.get_static("\1").get("id")',
        content
    )
    content = re.sub(
        r'static_item = MOCK_DB\.get\("([^"]+)"\)',
        r'static_item = db.get_static("\1")',
        content
    )
    content = re.sub(
        r'MOCK_DB\._save_item\("dynamic_store", collection_path, id, dict\(static_item\)\)',
        r'db.upsert_item(collection_path, id, dict(static_item))',
        content
    )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)


if __name__ == "__main__":
    base_dir = r"d:\HPE CPP\MCP_Integrated"
    mock_servers = ["mock_server(cloud)", "mock_server(Comops)", "mock_server(network)", "mock_server(oneview)", "mock_server(storage)"]
    
    for srv in mock_servers:
        srv_path = os.path.join(base_dir, srv)
        main_py = os.path.join(srv_path, "main.py")
        db_py = os.path.join(srv_path, "database.py")
        
        if os.path.exists(main_py):
            # Write database.py
            with open(db_py, "w", encoding="utf-8") as f:
                f.write(DATABASE_PY_TEMPLATE)
            
            # Process main.py
            process_file(main_py)
            print(f"Migrated {srv}")
