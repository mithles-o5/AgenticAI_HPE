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
    """A thin wrapper around a single SQLite database that stores a JSON blob per server.
    The class mimics a dict for compatibility with the existing proxy classes.
    """

    def __init__(self, server_name: str, db_path: str):
        self.server_name = server_name
        self.db_path = db_path
        self._conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._lock = threading.RLock()
        with self._lock:
            self._conn.execute(
                "CREATE TABLE IF NOT EXISTS store (server TEXT PRIMARY KEY, data TEXT)"
            )
            self._conn.commit()
        cur = self._conn.execute(
            "SELECT data FROM store WHERE server = ?", (self.server_name,)
        ).fetchone()
        if cur is None:
            self._data = {"dynamic_store": {}}
            # Insert empty record
            with self._lock:
                self._conn.execute(
                    "INSERT INTO store (server, data) VALUES (?, ?)",
                    (self.server_name, json.dumps(self._data)),
                )
                self._conn.commit()
        else:
            try:
                self._data = json.loads(cur[0])
            except Exception:
                self._data = {"dynamic_store": {}}
        # Ensure dynamic_store exists
        self._data.setdefault("dynamic_store", {})
        super().__init__(self._data)

    # Persistence helper – write full JSON blob back to SQLite
    def persist(self):
        json_blob = json.dumps(self._data)
        with self._lock:
            self._conn.execute(
                "INSERT OR REPLACE INTO store (server, data) VALUES (?, ?)",
                (self.server_name, json_blob),
            )
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
        self.persist()

    def __delitem__(self, key):
        super().__delitem__(key)
        self._data.pop(key, None)
        self.persist()

    def update(self, other):
        super().update(other)
        self._data.update(other)
        self.persist()

    def pop(self, key, default=None):
        val = super().pop(key, default)
        if key in self._data:
            self._data.pop(key)
            self.persist()
        return val

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
        with self._lock:
            if subkey_name:
                self._data.setdefault(key_name, {})
                self._data[key_name].setdefault(subkey_name, {})
                self._data[key_name][subkey_name][subsubkey_name] = data
            else:
                self._data[key_name] = data
            # Reflect changes in dict view
            self[key_name] = self._data[key_name]
            self.persist()

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
            else:
                val = self._data.pop(key_name, None)
            self.pop(key_name, None)
            self.persist()
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
        # direct assignment not needed; dynamic store updates go through proxies
        pass

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
# Shared SQLite DB path located at generator/servers/mock_db.sqlite
shared_db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "mock_db.sqlite"))
_db_store_cache = {}

def get_db_store(server_name, db_path):
    # Use a single shared SQLiteMockDB instance for all servers to ensure consistent data and thread safety
    shared_key = "shared"
    if shared_key not in _db_store_cache:
        _db_store_cache[shared_key] = SQLiteMockDB(shared_key, shared_db_path)
    return _db_store_cache[shared_key]

MOCK_DB = get_db_store("shared", shared_db_path)

# Persistence helper – run this script to write back all in‑memory changes to the SQLite DB
# and also export the current store to each server's mock_data.json (append/merge)
if __name__ == "__main__":
    # 1️⃣ Persist SQLite DB first
    for db in _db_store_cache.values():
        db.persist()
    print("[db_store] All changes persisted to SQLite DB.")

    # 2️⃣ Export data to each server's mock_data.json (merge with existing content)
    import os, json

    # Server folder names under ./servers
    server_folders = ["Cloud", "compute_ops", "Storage", "oneview"]

    # The shared in‑memory data (the whole JSON blob stored in SQLite)
    shared_data = _db_store_cache["shared"]._data

    # Helper to check if a collection path belongs to a server
    def path_belongs_to_server(path, srv):
        if srv == "compute_ops":
            return path.startswith("/compute-ops") or path.startswith("/compute-ops-mgmt")
        elif srv == "oneview":
            return path.startswith("/rest")
        elif srv == "Storage":
            return path.startswith("/data-services")
        elif srv == "Cloud":
            return path.startswith("/api")
        return False

    # Load existing JSON files to map static keys
    existing_data_map = {}
    for srv in server_folders:
        json_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), srv, "mock_data.json")
        )
        if os.path.exists(json_path):
            try:
                with open(json_path, "r", encoding="utf-8") as f:
                    existing_data_map[srv] = json.load(f)
            except Exception:
                existing_data_map[srv] = {}
        else:
            existing_data_map[srv] = {}

    for srv in server_folders:
        json_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), srv, "mock_data.json")
        )
        existing = existing_data_map[srv]

        # Filter shared_data for this server
        srv_shared = {}
        
        # 1. Filter static keys (keys other than "dynamic_store")
        for k, v in shared_data.items():
            if k == "dynamic_store":
                continue
            
            # Check if this key was originally in this server's mock_data.json
            in_this_server = k in existing
            
            # Check if it's in other servers' mock_data.json to avoid duplicate routing
            in_other_servers = any(k in existing_data_map[other] for other in server_folders if other != srv)
            
            if in_this_server:
                srv_shared[k] = v
            elif not in_other_servers:
                # Fallback based on name/prefix
                kl = k.lower()
                if srv == "compute_ops" and "compute_ops" in kl:
                    srv_shared[k] = v
                elif srv == "oneview" and "rest" in kl:
                    srv_shared[k] = v
                elif srv == "Storage" and "data_services" in kl:
                    srv_shared[k] = v
                elif srv == "Cloud" and ("api" in kl or not any(x in kl for x in ["compute_ops", "rest", "data_services"])):
                    srv_shared[k] = v

        # 2. Filter dynamic_store paths for this server
        dynamic_store = shared_data.get("dynamic_store", {})
        srv_dynamic_store = {
            path: items for path, items in dynamic_store.items()
            if path_belongs_to_server(path, srv)
        }
        
        # Only add "dynamic_store" if there are filtered paths or if it was originally there
        if srv_dynamic_store or "dynamic_store" in existing:
            srv_shared["dynamic_store"] = srv_dynamic_store

        # Shallow-merge with the existing content
        merged = {**existing, **srv_shared}

        # Write back the merged content
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(merged, f, indent=2)
        print(f"[db_store] Exported filtered data for {srv} to {json_path}")

