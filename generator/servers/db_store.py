import os
import json
import psycopg2
from contextlib import contextmanager

PG_HOST = os.getenv("PGHOST", "localhost")
PG_PORT = int(os.getenv("PGPORT", "5432"))
PG_USER = os.getenv("PGUSER", "postgres")
PG_PASSWORD = os.getenv("PGPASSWORD", "password")
PG_DATABASE = os.getenv("PGDATABASE", "postgres")

def _get_connection():
    return psycopg2.connect(
        host=PG_HOST,
        port=PG_PORT,
        user=PG_USER,
        password=PG_PASSWORD,
        database=PG_DATABASE
    )

@contextmanager
def db_cursor():
    conn = None
    try:
        conn = _get_connection()
        cursor = conn.cursor()
        yield cursor
        conn.commit()
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()

def init_table():
    with db_cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mock_db_store (
                server_name VARCHAR(50),
                key_name VARCHAR(255),
                subkey_name VARCHAR(255) DEFAULT '',
                subsubkey_name VARCHAR(255) DEFAULT '',
                data JSONB,
                PRIMARY KEY (server_name, key_name, subkey_name, subsubkey_name)
            )
        """)

def seed_if_empty(server_name, mock_file_path):
    with db_cursor() as cursor:
        cursor.execute(
            "SELECT COUNT(*) FROM mock_db_store WHERE server_name = %s",
            (server_name,)
        )
        count = cursor.fetchone()[0]
        if count > 0:
            return

    if not mock_file_path or not os.path.exists(mock_file_path):
        return

    print(f"[db_store] Seeding PostgreSQL mock_db_store for '{server_name}' from {mock_file_path}...")
    try:
        with open(mock_file_path, "r", encoding="utf-8") as f:
            db_data = json.load(f)
    except Exception as e:
        print(f"[db_store] Error loading mock file {mock_file_path}: {e}")
        return

    with db_cursor() as cursor:
        for key, val in db_data.items():
            if key in ["server_hardware", "servers"] and isinstance(val, dict):
                for subkey, item in val.items():
                    cursor.execute(
                        """INSERT INTO mock_db_store (server_name, key_name, subkey_name, subsubkey_name, data)
                           VALUES (%s, %s, %s, '', %s)
                           ON CONFLICT (server_name, key_name, subkey_name, subsubkey_name)
                           DO UPDATE SET data = EXCLUDED.data""",
                        (server_name, key, subkey, json.dumps(item))
                    )
            elif key == "dynamic_store" and isinstance(val, dict):
                for subkey, col_items in val.items():
                    if isinstance(col_items, dict):
                        for subsubkey, item in col_items.items():
                            cursor.execute(
                                """INSERT INTO mock_db_store (server_name, key_name, subkey_name, subsubkey_name, data)
                                   VALUES (%s, %s, %s, %s, %s)
                                   ON CONFLICT (server_name, key_name, subkey_name, subsubkey_name)
                                   DO UPDATE SET data = EXCLUDED.data""",
                                (server_name, key, subkey, subsubkey, json.dumps(item))
                            )
            else:
                cursor.execute(
                    """INSERT INTO mock_db_store (server_name, key_name, subkey_name, subsubkey_name, data)
                       VALUES (%s, %s, '', '', %s)
                       ON CONFLICT (server_name, key_name, subkey_name, subsubkey_name)
                       DO UPDATE SET data = EXCLUDED.data""",
                    (server_name, key, json.dumps(val))
                )
    print(f"[db_store] Seeding for '{server_name}' complete.")

def fetch_item(server_name, key_name, subkey_name='', subsubkey_name=''):
    with db_cursor() as cursor:
        cursor.execute(
            """SELECT data FROM mock_db_store 
               WHERE server_name = %s AND key_name = %s AND subkey_name = %s AND subsubkey_name = %s""",
            (server_name, key_name, subkey_name, subsubkey_name)
        )
        row = cursor.fetchone()
        return row[0] if row else None

def save_item(server_name, key_name, subkey_name, subsubkey_name, data):
    with db_cursor() as cursor:
        cursor.execute(
            """INSERT INTO mock_db_store (server_name, key_name, subkey_name, subsubkey_name, data)
               VALUES (%s, %s, %s, %s, %s)
               ON CONFLICT (server_name, key_name, subkey_name, subsubkey_name)
               DO UPDATE SET data = EXCLUDED.data""",
            (server_name, key_name, subkey_name, subsubkey_name, json.dumps(data))
        )

def delete_item(server_name, key_name, subkey_name, subsubkey_name):
    with db_cursor() as cursor:
        cursor.execute(
            """DELETE FROM mock_db_store 
               WHERE server_name = %s AND key_name = %s AND subkey_name = %s AND subsubkey_name = %s
               RETURNING data""",
            (server_name, key_name, subkey_name, subsubkey_name)
        )
        row = cursor.fetchone()
        return row[0] if row else None

def fetch_all_items(server_name, key_name, subkey_name=''):
    with db_cursor() as cursor:
        if subkey_name:
            cursor.execute(
                """SELECT subsubkey_name, data FROM mock_db_store 
                   WHERE server_name = %s AND key_name = %s AND subkey_name = %s""",
                (server_name, key_name, subkey_name)
            )
        else:
            cursor.execute(
                """SELECT subkey_name, data FROM mock_db_store 
                   WHERE server_name = %s AND key_name = %s AND subsubkey_name = ''""",
                (server_name, key_name)
            )
        rows = cursor.fetchall()
        return {row[0]: row[1] for row in rows}

def fetch_subkeys(server_name, key_name):
    with db_cursor() as cursor:
        cursor.execute(
            """SELECT DISTINCT subkey_name FROM mock_db_store 
               WHERE server_name = %s AND key_name = %s""",
            (server_name, key_name)
        )
        rows = cursor.fetchall()
        return [row[0] for row in rows]

def has_top_level_key(server_name, key_name):
    with db_cursor() as cursor:
        cursor.execute(
            """SELECT 1 FROM mock_db_store 
               WHERE server_name = %s AND key_name = %s LIMIT 1""",
            (server_name, key_name)
        )
        return cursor.fetchone() is not None

class PGItemProxy(dict):
    def __init__(self, server_name, key_name, subkey_name, subsubkey_name, data):
        self.server_name = server_name
        self.key_name = key_name
        self.subkey_name = subkey_name
        self.subsubkey_name = subsubkey_name
        super().__init__(data)

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        save_item(self.server_name, self.key_name, self.subkey_name, self.subsubkey_name, dict(self))

    def update(self, other):
        super().update(other)
        save_item(self.server_name, self.key_name, self.subkey_name, self.subsubkey_name, dict(self))

class PGCollectionProxy(dict):
    def __init__(self, server_name, key_name, subkey_name=''):
        self.server_name = server_name
        self.key_name = key_name
        self.subkey_name = subkey_name
        items = fetch_all_items(server_name, key_name, subkey_name)
        super().__init__(items)

    def _get_item_keys(self, item_id):
        if not self.subkey_name:
            return item_id, ''
        else:
            return self.subkey_name, item_id

    def __getitem__(self, item_id):
        sk, ssk = self._get_item_keys(item_id)
        val = fetch_item(self.server_name, self.key_name, sk, ssk)
        if val is None:
            raise KeyError(item_id)
        return PGItemProxy(self.server_name, self.key_name, sk, ssk, val)

    def __setitem__(self, item_id, value):
        sk, ssk = self._get_item_keys(item_id)
        save_item(self.server_name, self.key_name, sk, ssk, value)
        super().__setitem__(item_id, value)

    def get(self, item_id, default=None):
        sk, ssk = self._get_item_keys(item_id)
        val = fetch_item(self.server_name, self.key_name, sk, ssk)
        if val is None:
            return default
        return PGItemProxy(self.server_name, self.key_name, sk, ssk, val)

    def pop(self, item_id, default=None):
        sk, ssk = self._get_item_keys(item_id)
        val = delete_item(self.server_name, self.key_name, sk, ssk)
        super().pop(item_id, None)
        if val is None:
            return default
        return val

    def values(self):
        items = fetch_all_items(self.server_name, self.key_name, self.subkey_name)
        result = []
        for item_id, val in items.items():
            sk, ssk = self._get_item_keys(item_id)
            result.append(PGItemProxy(self.server_name, self.key_name, sk, ssk, val))
        return result

class PGDynamicStoreProxy(dict):
    def __init__(self, server_name):
        self.server_name = server_name
        subkeys = fetch_subkeys(self.server_name, "dynamic_store")
        super().__init__({sk: None for sk in subkeys})

    def __getitem__(self, collection_path):
        return PGCollectionProxy(self.server_name, "dynamic_store", collection_path)

    def __setitem__(self, collection_path, value):
        pass

    def get(self, collection_path, default=None):
        return PGCollectionProxy(self.server_name, "dynamic_store", collection_path)

class PGMockDB(dict):
    def __init__(self, server_name, mock_file_path):
        self.server_name = server_name
        init_table()
        seed_if_empty(server_name, mock_file_path)
        keys = fetch_subkeys(server_name, "dynamic_store")
        super().__init__({k: None for k in keys})

    def __getitem__(self, key):
        if key in ["server_hardware", "servers"]:
            return PGCollectionProxy(self.server_name, key)
        elif key == "dynamic_store":
            return PGDynamicStoreProxy(self.server_name)
        else:
            val = fetch_item(self.server_name, key, '', '')
            if val is None:
                raise KeyError(key)
            return val

    def get(self, key, default=None):
        if key in ["server_hardware", "servers"]:
            return PGCollectionProxy(self.server_name, key)
        elif key == "dynamic_store":
            return PGDynamicStoreProxy(self.server_name)
        val = fetch_item(self.server_name, key, '', '')
        if val is None:
            return default
        return val

    def __contains__(self, key):
        if key in {"dynamic_store", "server_hardware", "servers"}:
            return True
        return has_top_level_key(self.server_name, key)

_db_store_cache = {}

def get_db_store(server_name, mock_file_path):
    if server_name not in _db_store_cache:
        _db_store_cache[server_name] = PGMockDB(server_name, mock_file_path)
    return _db_store_cache[server_name]
