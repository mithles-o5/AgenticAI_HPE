import sqlite3
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
        existing_cols = {row[1].lower() for row in cursor.fetchall()}
        for k in data.keys():
            if k.lower() not in existing_cols:
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

    def _intercept_devices(self, collection_path):
        """Intercept Aruba Central endpoints to read from main devices collection"""
        path_lower = collection_path.lower()
        parts = [p for p in path_lower.split('/') if p]
        
        # Only intercept the base endpoints or specific device lookup endpoints (len 3 or 4)
        if len(parts) > 4:
            return None
            
        if "/network/v1/devices" in path_lower:
            return None
            
        if "network-monitoring/v1/aps" in path_lower or "network-monitoring/v1/swarms" in path_lower or "network-monitoring/v1/top-aps" in path_lower:
            devices = list(self.get_collection("/network/v1/devices").values())
            return [d for d in devices if d.get("device_type", "").lower() in ["ap", "iap", "access point", "access_point"]]
            
        if "network-monitoring/v1/switches" in path_lower:
            devices = list(self.get_collection("/network/v1/devices").values())
            return [d for d in devices if d.get("device_type", "").lower() in ["switch", "aos-s", "aos-cx", "cx"]]
            
        if "network-monitoring/v1/gateways" in path_lower:
            devices = list(self.get_collection("/network/v1/devices").values())
            return [d for d in devices if d.get("device_type", "").lower() in ["gateway", "mc", "mobility controller", "router", "firewall", "wireless_controller"]]
            
        return None

    def get_all(self, collection_path):
        intercepted = self._intercept_devices(collection_path)
        if intercepted is not None:
            return intercepted
        return list(self.get_collection(collection_path).values())

    def get_item(self, collection_path, item_id):
        intercepted = self._intercept_devices(collection_path)
        if intercepted is not None:
            for d in intercepted:
                if d.get("id") == item_id or d.get("serial_number") == item_id or d.get("name") == item_id:
                    return d
            return None
            
        table_name = self._get_table_name(collection_path)
        with self._lock:
            conn = sqlite3.connect(self.db_path, check_same_thread=False)
            conn.row_factory = sqlite3.Row
            try:
                # Get available columns to search by multiple identifiers
                cursor = conn.execute(f"PRAGMA table_info({table_name})")
                cols = {row[1] for row in cursor.fetchall()}
                
                where_clause = ["id = ?"]
                params = [item_id]
                
                if "name" in cols:
                    where_clause.append("name = ?")
                    params.append(item_id)
                if "source_device_id" in cols:
                    where_clause.append("source_device_id = ?")
                    params.append(item_id)
                if "uuid" in cols:
                    where_clause.append("uuid = ?")
                    params.append(item_id)
                    
                query = f"SELECT * FROM {table_name} WHERE " + " OR ".join(where_clause)
                cursor = conn.execute(query, tuple(params))
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
        existing_item = self.get_item(collection_path, item_id)
        if existing_item and "id" in existing_item:
            payload_dict["id"] = existing_item["id"]
        elif "id" not in payload_dict:
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
        existing_item = self.get_item(collection_path, item_id)
        if not existing_item or "id" not in existing_item:
            return None
        true_id = existing_item["id"]
        with self._lock:
            conn = sqlite3.connect(self.db_path, check_same_thread=False)
            try:
                # Fetch first
                conn.row_factory = sqlite3.Row
                cursor = conn.execute(f"SELECT * FROM {table_name} WHERE id = ?", (true_id,))
                row = cursor.fetchone()
                if row:
                    conn.execute(f"DELETE FROM {table_name} WHERE id = ?", (true_id,))
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
