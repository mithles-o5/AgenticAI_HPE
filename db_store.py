# SQLite-backed mock store for all servers

import os
import json
import sqlite3
import threading
import fastapi
from fastapi import HTTPException

# Global caches for collection and item keys used by the FastAPI route mapper
_collection_keys = {}
_item_keys = {}

# Helper to extract a stable ID from items
def get_item_id(item):
    if not isinstance(item, dict):
        return None
    for field in [
        "id", "uuid", "uid", "name", "uri", "resourceUri",
        "serverHardwareUri", "entityId", "volumeName", "volumeWWN", "wwn",
        "timestamp", "applicationSetType", "hostGroupName", "deviceType"
    ]:
        val = item.get(field)
        if val is not None and not isinstance(val, (dict, list)):
            sval = str(val).strip()
            if sval != "":
                return sval[:255]
    return None

class SQLiteMockDB(dict):
    """A schema-aware SQLite-backed database store that stores mock data in dedicated tables."""

    def __init__(self, server_name: str, db_path: str, json_path: str):
        self.server_name = server_name
        self.db_path = db_path
        self.json_path = json_path
        self._conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._lock = threading.RLock()
        
        # Initialize basic tables
        with self._lock:
            self._conn.execute(
                "CREATE TABLE IF NOT EXISTS static_store (key TEXT PRIMARY KEY, value TEXT)"
            )
            self._conn.execute(
                "CREATE TABLE IF NOT EXISTS collection_metadata (table_name TEXT PRIMARY KEY, collection_path TEXT)"
            )
            self._conn.commit()

        # Seed from mock_data.json on first initialization if empty
        self._seed_if_empty()

        # Load data from the SQLite DB into memory cache
        self._data = {"dynamic_store": {}}
        self._load_from_db()
        super().__init__(self._data)

    def _seed_if_empty(self):
        with self._lock:
            count_static = self._conn.execute("SELECT COUNT(*) FROM static_store").fetchone()[0]
            count_metadata = self._conn.execute("SELECT COUNT(*) FROM collection_metadata").fetchone()[0]
            if count_static == 0 and count_metadata == 0 and os.path.exists(self.json_path):
                try:
                    with open(self.json_path, "r", encoding="utf-8") as f:
                        js_data = json.load(f)
                    
                    # Store static keys
                    for k, v in js_data.items():
                        if k == "dynamic_store":
                            continue
                        self._conn.execute(
                            "INSERT OR REPLACE INTO static_store (key, value) VALUES (?, ?)",
                            (k, json.dumps(v))
                        )
                    
                    # Store dynamic_store
                    dynamic_store = js_data.get("dynamic_store", {})
                    for col_path, items in dynamic_store.items():
                        for item_id, item in items.items():
                            table_name = self._get_table_for_collection(col_path, item)
                            self._ensure_columns(table_name, item)
                            
                            columns = list(item.keys())
                            placeholders = ", ".join(["?"] * len(columns))
                            cols_str = ", ".join([f'"{c}"' for c in columns])
                            
                            values = []
                            for c in columns:
                                val = item[c]
                                if isinstance(val, (dict, list)):
                                    val = json.dumps(val)
                                elif isinstance(val, bool):
                                    val = 1 if val else 0
                                values.append(val)
                                
                            self._conn.execute(
                                f'INSERT OR REPLACE INTO {table_name} ({cols_str}) VALUES ({placeholders})',
                                values
                            )
                    self._conn.commit()
                except Exception as e:
                    print(f"Error importing initial mock_data.json for {self.server_name}: {e}")

    def _load_from_db(self):
        # 1. Load static keys
        cur = self._conn.execute("SELECT key, value FROM static_store").fetchall()
        for row in cur:
            self._data[row[0]] = json.loads(row[1])
            
        # 2. Load dynamic collections
        metadata = self._conn.execute("SELECT table_name, collection_path FROM collection_metadata").fetchall()
        for t_name, col_path in metadata:
            self._data["dynamic_store"][col_path] = {}
            try:
                cursor = self._conn.execute(f"SELECT * FROM {t_name}")
                col_names = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
                for r in rows:
                    item = {}
                    for i, col in enumerate(col_names):
                        val = r[i]
                        # Convert/deserialize types as needed
                        if isinstance(val, str) and (val.startswith("[") or val.startswith("{")):
                            try:
                                val = json.loads(val)
                            except Exception:
                                pass
                        item[col] = val
                    
                    item_id = get_item_id(item) or item.get("id")
                    if item_id:
                        self._data["dynamic_store"][col_path][item_id] = item
            except Exception as e:
                print(f"Error loading table {t_name}: {e}")

    def _get_table_for_collection(self, col_path, sample_item=None):
        parts = [p for p in col_path.split('/') if p]
        table_name = "dynamic_" + "_".join(parts).replace("-", "_")
        
        row = self._conn.execute("SELECT table_name FROM collection_metadata WHERE table_name = ?", (table_name,)).fetchone()
        if not row:
            with self._lock:
                self._conn.execute(
                    "INSERT OR REPLACE INTO collection_metadata (table_name, collection_path) VALUES (?, ?)",
                    (table_name, col_path)
                )
                self._conn.commit()
            
            schema_model = self._find_schema_model(col_path)
            self._create_table_for_collection(table_name, schema_model, sample_item)
            
        return table_name

    def _find_schema_model(self, col_path):
        import importlib
        from pydantic import BaseModel
        parts = [p for p in col_path.split('/') if p]
        if not parts:
            return None
        last_seg = parts[-1]
        singular = last_seg.rstrip('s').replace("-", "").lower()
        
        try:
            mod = importlib.import_module(f"generator.servers.{self.server_name}.models")
            for name in dir(mod):
                if name.endswith("Request") or name.endswith("Response"):
                    continue
                obj = getattr(mod, name)
                if isinstance(obj, type) and issubclass(obj, BaseModel) and obj is not BaseModel:
                    if singular in name.lower():
                        return obj
        except Exception:
            pass
        return None

    def _create_table_for_collection(self, table_name, schema_model, sample_item):
        columns = []
        field_types = {}
        
        if schema_model:
            if hasattr(schema_model, "model_fields"):
                fields = schema_model.model_fields
                for field_name, field_info in fields.items():
                    annotation = field_info.annotation
                    field_types[field_name] = annotation
            else:
                fields = schema_model.__fields__
                for field_name, model_field in fields.items():
                    field_types[field_name] = model_field.type_
        
        keys = list(field_types.keys()) if field_types else (list(sample_item.keys()) if sample_item else ["id"])
        
        if "id" not in keys and sample_item and "id" in sample_item:
            keys.append("id")
            
        for k in keys:
            val_type = field_types.get(k)
            if val_type is None and sample_item:
                val_type = type(sample_item.get(k))
                
            sql_type = "TEXT"
            if val_type in (int, "int", "Integer"):
                sql_type = "INTEGER"
            elif val_type in (float, "float", "Float"):
                sql_type = "REAL"
            elif val_type in (bool, "bool", "Boolean"):
                sql_type = "INTEGER"
                
            primary_key_clause = " PRIMARY KEY" if k == "id" else ""
            columns.append(f'"{k}" {sql_type}{primary_key_clause}')
            
        cols_str = ", ".join(columns)
        with self._lock:
            self._conn.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({cols_str})")
            self._conn.commit()

    def _ensure_columns(self, table_name, data):
        if not data:
            return
        # Retrieve existing columns
        cursor = self._conn.execute(f"PRAGMA table_info({table_name})")
        existing_cols = {row[1] for row in cursor.fetchall()}
        
        # Add any missing columns
        with self._lock:
            for k, val in data.items():
                if k not in existing_cols:
                    sql_type = "TEXT"
                    if isinstance(val, int) and not isinstance(val, bool):
                        sql_type = "INTEGER"
                    elif isinstance(val, float):
                        sql_type = "REAL"
                    elif isinstance(val, bool):
                        sql_type = "INTEGER"
                    self._conn.execute(f'ALTER TABLE {table_name} ADD COLUMN "{k}" {sql_type}')
            self._conn.commit()

    def persist(self):
        # We write transactions instantly, but commit any pending changes
        with self._lock:
            self._conn.commit()

    def __getitem__(self, key):
        if key in ["server_hardware", "servers"]:
            return PGCollectionProxy(self.server_name, key)
        elif key == "dynamic_store":
            return PGDynamicStoreProxy(self.server_name)
        else:
            if key not in self._data:
                raise KeyError(key)
            return self._data[key]

    def get(self, key, default=None):
        if key in ["server_hardware", "servers"]:
            return PGCollectionProxy(self.server_name, key)
        elif key == "dynamic_store":
            return PGDynamicStoreProxy(self.server_name)
        return self._data.get(key, default)

    def __contains__(self, key):
        if key in {"dynamic_store", "server_hardware", "servers"}:
            return True
        return key in self._data

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self._data[key] = value
        if key != "dynamic_store":
            self.save_static_key(key, value)

    def __delitem__(self, key):
        super().__delitem__(key)
        self._data.pop(key, None)
        if key != "dynamic_store":
            self.delete_static_key(key)

    def update(self, other):
        super().update(other)
        self._data.update(other)
        for k, v in other.items():
            if k != "dynamic_store":
                self.save_static_key(k, v)

    def pop(self, key, default=None):
        val = super().pop(key, default)
        if key in self._data:
            self._data.pop(key)
            if key != "dynamic_store":
                self.delete_static_key(key)
        return val

    def save_static_key(self, key, value):
        with self._lock:
            self._conn.execute(
                "INSERT OR REPLACE INTO static_store (key, value) VALUES (?, ?)",
                (key, json.dumps(value))
            )
            self._conn.commit()

    def delete_static_key(self, key):
        with self._lock:
            self._conn.execute("DELETE FROM static_store WHERE key = ?", (key,))
            self._conn.commit()

    def _clear_collection(self, col_path):
        table_name = self._get_table_for_collection(col_path, None)
        with self._lock:
            self._conn.execute(f"DELETE FROM {table_name}")
            self._conn.commit()
        if col_path in self._data.get("dynamic_store", {}):
            self._data["dynamic_store"][col_path].clear()

    # Helper methods used by proxy classes
    def _fetch_item(self, key_name, subkey_name="", subsubkey_name=""):
        cur = self._data.get(key_name)
        if cur is None:
            return None
        if subkey_name:
            cur = cur.get(subkey_name, {})
            if subsubkey_name:
                cur = cur.get(subsubkey_name)
        return cur

    def _save_item(self, key_name, subkey_name, subsubkey_name, data):
        # key_name="dynamic_store", subkey_name=collection_path, subsubkey_name=item_id, data=item
        with self._lock:
            if subkey_name:
                if isinstance(data, dict):
                    if "id" not in data and subsubkey_name:
                        data = dict(data)
                        data["id"] = subsubkey_name
                self._data.setdefault(key_name, {})
                self._data[key_name].setdefault(subkey_name, {})
                self._data[key_name][subkey_name][subsubkey_name] = data
                
                # Write to sqlite table
                table_name = self._get_table_for_collection(subkey_name, data)
                self._ensure_columns(table_name, data)
                
                columns = list(data.keys())
                placeholders = ", ".join(["?"] * len(columns))
                cols_str = ", ".join([f'"{c}"' for c in columns])
                
                values = []
                for c in columns:
                    val = data[c]
                    if isinstance(val, (dict, list)):
                        val = json.dumps(val)
                    elif isinstance(val, bool):
                        val = 1 if val else 0
                    values.append(val)
                    
                self._conn.execute(
                    f'INSERT OR REPLACE INTO {table_name} ({cols_str}) VALUES ({placeholders})',
                    values
                )
                self._conn.commit()
            else:
                self._data[key_name] = data
                self.save_static_key(key_name, data)

    def _delete_item(self, key_name, subkey_name, subsubkey_name):
        with self._lock:
            cur = self._data.get(key_name)
            if cur is None:
                return None
            if subkey_name:
                sub = cur.get(subkey_name, {})
                val = sub.pop(subsubkey_name, None)
                if not sub:
                    cur.pop(subkey_name, None)
                    
                # Delete from sqlite table
                table_name = self._get_table_for_collection(subkey_name, None)
                self._conn.execute(f"DELETE FROM {table_name} WHERE id = ?", (subsubkey_name,))
                self._conn.commit()
            else:
                val = self._data.pop(key_name, None)
                self.delete_static_key(key_name)
            return val

    def _fetch_all_items(self, key_name, subkey_name=""):
        cur = self._data.get(key_name, {})
        if subkey_name:
            cur = cur.get(subkey_name, {})
        return cur

    def _fetch_subkeys(self, key_name):
        return list(self._data.get(key_name, {}).keys())

    def _has_top_level_key(self, key_name):
        return key_name in self._data

# Proxy classes unchanged – they operate on SQLiteMockDB via the helper methods above
class PGItemProxy(dict):
    def __init__(self, server_name, key_name, subkey_name, subsubkey_name, data):
        self.server_name = server_name
        self.key_name = key_name
        self.subkey_name = subkey_name
        self.subsubkey_name = subsubkey_name
        super().__init__(data)

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        db = _db_store_cache[self.server_name]
        db._save_item(self.key_name, self.subkey_name, self.subsubkey_name, dict(self))

    def update(self, other):
        super().update(other)
        db = _db_store_cache[self.server_name]
        db._save_item(self.key_name, self.subkey_name, self.subsubkey_name, dict(self))

class PGCollectionProxy(dict):
    def __init__(self, server_name, key_name, subkey_name=''):
        self.server_name = server_name
        self.key_name = key_name
        self.subkey_name = subkey_name
        db = _db_store_cache[server_name]
        items = db._fetch_all_items(key_name, subkey_name)
        super().__init__(items)

    def _get_item_keys(self, item_id):
        if not self.subkey_name:
            return item_id, ''
        else:
            return self.subkey_name, item_id

    def __getitem__(self, item_id):
        sk, ssk = self._get_item_keys(item_id)
        db = _db_store_cache[self.server_name]
        val = db._fetch_item(self.key_name, sk, ssk)
        if val is None:
            raise KeyError(item_id)
        return PGItemProxy(self.server_name, self.key_name, sk, ssk, val)

    def __setitem__(self, item_id, value):
        sk, ssk = self._get_item_keys(item_id)
        db = _db_store_cache[self.server_name]
        db._save_item(self.key_name, sk, ssk, value)
        super().__setitem__(item_id, value)

    def get(self, item_id, default=None):
        sk, ssk = self._get_item_keys(item_id)
        db = _db_store_cache[self.server_name]
        val = db._fetch_item(self.key_name, sk, ssk)
        if val is None:
            return default
        return PGItemProxy(self.server_name, self.key_name, sk, ssk, val)

    def pop(self, item_id, default=None):
        sk, ssk = self._get_item_keys(item_id)
        db = _db_store_cache[self.server_name]
        val = db._delete_item(self.key_name, sk, ssk)
        super().pop(item_id, None)
        return val if val is not None else default

    def values(self):
        db = _db_store_cache[self.server_name]
        items = db._fetch_all_items(self.key_name, self.subkey_name)
        result = []
        for item_id, val in items.items():
            sk, ssk = self._get_item_keys(item_id)
            result.append(PGItemProxy(self.server_name, self.key_name, sk, ssk, val))
        return result

class PGDynamicStoreProxy(dict):
    def __init__(self, server_name):
        self.server_name = server_name
        db = _db_store_cache[server_name]
        subkeys = db._fetch_subkeys("dynamic_store")
        super().__init__({sk: None for sk in subkeys})

    def __getitem__(self, collection_path):
        return PGCollectionProxy(self.server_name, "dynamic_store", collection_path)

    def __setitem__(self, collection_path, value):
        if not value:
            db = _db_store_cache[self.server_name]
            db._clear_collection(collection_path)

    def get(self, collection_path, default=None):
        return PGCollectionProxy(self.server_name, "dynamic_store", collection_path)

# FastAPI integration – unchanged, but now works with SQLiteMockDB
_original_fastapi_init = fastapi.FastAPI.__init__

def _new_fastapi_init(self, *args, **kwargs):
    _original_fastapi_init(self, *args, **kwargs)

    @self.on_event("startup")
    def sync_and_map_routes():
        for server_name, db in _db_store_cache.items():
            coll_keys = {}
            item_keys = set()
            for route in self.routes:
                if not hasattr(route, "path") or not hasattr(route, "name") or not hasattr(route, "methods"):
                    continue
                methods = route.methods
                if not methods or not (methods & {"GET", "PATCH", "PUT", "DELETE"}):
                    continue
                path = route.path
                func_name = route.name
                if path.endswith("}"):
                    parts = path.rstrip("/").split("/")
                    if parts and parts[-1].startswith("{") and parts[-1].endswith("}"):
                        item_keys.add(func_name)
                else:
                    if "GET" in methods:
                        coll_keys[func_name] = path
            _collection_keys[server_name] = coll_keys
            _item_keys[server_name] = item_keys
        # No seeding logic

fastapi.FastAPI.__init__ = _new_fastapi_init

# Global cache for SQLiteMockDB instances
import os
import sys
_db_store_cache = {}

def get_current_server_name():
    # 1. Stack frame inspection to detect importing module's folder name
    import inspect
    for frame_info in inspect.stack():
        filename = frame_info.filename.replace("\\", "/").lower()
        for srv in ["cloud", "storage", "oneview", "compute_ops", "network"]:
            if f"servers/{srv}/" in filename or f"/{srv}/" in filename:
                canonical_map = {
                    "cloud": "Cloud",
                    "storage": "Storage",
                    "oneview": "oneview",
                    "compute_ops": "compute_ops",
                    "network": "network"
                }
                return canonical_map[srv]

    # 2. Command-line arguments check (joined sys.argv)
    args_str = " ".join(sys.argv).replace("\\", "/").lower()
    for srv in ["cloud", "storage", "oneview", "compute_ops", "network"]:
        if srv in args_str:
            canonical_map = {
                "cloud": "Cloud",
                "storage": "Storage",
                "oneview": "oneview",
                "compute_ops": "compute_ops",
                "network": "network"
            }
            return canonical_map[srv]

    # 3. Default fallback
    return "shared"

def get_db_store(server_name, db_path):
    canonical_map = {
        "cloud": "Cloud",
        "storage": "Storage",
        "oneview": "oneview",
        "compute_ops": "compute_ops",
        "network": "network",
        "shared": "shared"
    }
    canonical_name = canonical_map.get(server_name.lower(), server_name)
    
    if canonical_name not in _db_store_cache:
        if db_path.endswith(".json"):
            mock_file = os.path.abspath(db_path)
            server_dir = os.path.dirname(mock_file)
            sqlite_path = os.path.join(server_dir, f"{canonical_name.lower()}_db.sqlite")
        else:
            sqlite_path = os.path.abspath(db_path)
            server_dir = os.path.dirname(sqlite_path)
            mock_file = os.path.join(server_dir, "mock_data.json")
            
        _db_store_cache[canonical_name] = SQLiteMockDB(canonical_name, sqlite_path, mock_file)
    return _db_store_cache[canonical_name]

# Auto-detect which server database to use for imports
current_server = get_current_server_name()
if current_server == "shared":
    shared_db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "mock_db.sqlite"))
    MOCK_DB = get_db_store("shared", shared_db_path)
else:
    srv_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), current_server))
    mock_file = os.path.join(srv_dir, "mock_data.json")
    MOCK_DB = get_db_store(current_server, mock_file)

# Persistence helper – run this script to write back all in‑memory changes to the SQLite DB
# and also export the current store to each server's mock_data.json (append/merge)
if __name__ == "__main__":
    import os, json
    server_folders = ["Cloud", "compute_ops", "Storage", "oneview", "network"]
    
    for srv in server_folders:
        srv_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), srv))
        mock_file = os.path.join(srv_dir, "mock_data.json")
        db = get_db_store(srv, mock_file)
        db.persist()
        
        existing = {}
        if os.path.exists(mock_file):
            try:
                with open(mock_file, "r", encoding="utf-8") as f:
                    existing = json.load(f)
            except Exception:
                existing = {}
                
        for key in ["get_compute_ops_mgmt_v1_custom_servers", "get_compute_ops_mgmt_v1_custom_servers_id", "get_rest_custom_servers", "get_rest_custom_servers_id"]:
            existing.pop(key, None)
            
        if "dynamic_store" in existing:
            existing["dynamic_store"].pop("/compute-ops-mgmt/v1/custom-servers", None)
            existing["dynamic_store"].pop("/rest/custom-servers", None)
            
        merged = {**existing, **db._data}
        
        with open(mock_file, "w", encoding="utf-8") as f:
            json.dump(merged, f, indent=2)
            
        print(f"[db_store] Exported and synced {srv} SQLite data to {mock_file}")

