"""
mock_db_cache.py
================
In-memory mock database and cache provider.
Injects mock psycopg2 (SQLite3 back-end) and mock redis modules into sys.modules.
Automatically initializes schema and seeds 1500+ devices and all prompt endpoints.
"""

from __future__ import annotations

import logging
import os
import sys
import types
import sqlite3
import uuid
import time
import fnmatch
import re
import threading

logger = logging.getLogger("mock_db_cache")

# ─────────────────────────────────────────────────────────────────────────────
# In-Memory Shared SQLite Connection & Lock
# ─────────────────────────────────────────────────────────────────────────────
_db_lock = threading.Lock()
_shared_conn = sqlite3.connect(":memory:", check_same_thread=False)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

_shared_conn.row_factory = dict_factory

# ─────────────────────────────────────────────────────────────────────────────
# Mock Psycopg2 Exceptions & Wrapper Classes
# ─────────────────────────────────────────────────────────────────────────────
class Error(Exception):
    pass

class ProgrammingError(Error):
    pass

class OperationalError(Error):
    pass

class MockCursor:
    def __init__(self, sqlite_conn):
        self.sqlite_conn = sqlite_conn
        self.sqlite_cur = sqlite_conn.cursor()
        self.description = None
        self.rowcount = -1

    def execute(self, query, params=None):
        if params is None:
            params = ()

        # Preprocess PostgreSQL query to be SQLite compatible
        query_processed = query
        query_processed = query_processed.replace("NOW()", "CURRENT_TIMESTAMP")
        query_processed = query_processed.replace("DEFAULT NOW()", "DEFAULT CURRENT_TIMESTAMP")
        query_processed = query_processed.replace("::text", "")
        query_processed = query_processed.replace("::uuid", "")
        query_processed = query_processed.replace("::inet", "")
        query_processed = query_processed.replace("RESTART IDENTITY CASCADE", "")

        # SQLite does not support TRUNCATE; replace with DELETE
        if query_processed.strip().upper().startswith("TRUNCATE TABLE"):
            parts = query_processed.strip().split()
            table_name = parts[2].rstrip(";")
            query_processed = f"DELETE FROM {table_name};"

        # Correct whitespace in ON CONFLICT blocks
        query_processed = query_processed.replace("ON CONFLICT (serial_number)", "ON CONFLICT(serial_number)")
        query_processed = query_processed.replace(
            "ON CONFLICT (vendor, device_type, action_key, api_path, http_method)",
            "ON CONFLICT(vendor, device_type, action_key, api_path, http_method)"
        )

        # Convert PostgreSQL parameter placeholders (%s) to SQLite (?)
        # But skip escaped % (%%)
        parts = query_processed.split("%s")
        query_final = ""
        new_params = []
        
        if params is not None and (len(params) if isinstance(params, (list, tuple)) else 1) == len(parts) - 1:
            if not isinstance(params, (list, tuple)):
                params = [params]
            param_idx = 0
            for i, part in enumerate(parts[:-1]):
                if part.endswith("ANY("):
                    list_val = params[param_idx]
                    if not isinstance(list_val, (list, tuple, set)):
                        list_val = [list_val]
                    placeholders = ", ".join(["?"] * len(list_val))
                    part = part[:-4].rstrip()
                    if part.endswith("="):
                        part = part[:-1].rstrip()
                    part = part + " IN ("
                    query_final += part + placeholders
                    new_params.extend(list_val)
                else:
                    query_final += part + "?"
                    new_params.append(params[param_idx])
                param_idx += 1
            query_final += parts[-1]
            params = tuple(new_params)
        else:
            for part in parts[:-1]:
                query_final += part + "?"
            query_final += parts[-1]
            
        query_final = query_final.replace("%%", "%")

        # Auto-inject UUID for INSERT statements if ID is missing from columns
        if "INSERT INTO" in query_final.upper() and "ID," not in query_final.upper() and "(ID" not in query_final.upper():
            match = re.search(r"INSERT\s+INTO\s+(\w+)\s*\(([^)]+)\)\s*VALUES\s*\(([^)]+)\)", query_final, re.IGNORECASE)
            if match:
                table_name = match.group(1)
                columns = match.group(2)
                values = match.group(3)
                new_columns = "id, " + columns
                new_values = "?, " + values
                new_insert = f"INSERT INTO {table_name} ({new_columns}) VALUES ({new_values})"
                query_final = query_final.replace(match.group(0), new_insert)
                
                # Prepend a fresh UUID to params
                if isinstance(params, tuple):
                    params = (str(uuid.uuid4()),) + params
                elif isinstance(params, list):
                    params = [str(uuid.uuid4())] + list(params)

        with _db_lock:
            try:
                self.sqlite_cur.execute(query_final, params)
                self.description = self.sqlite_cur.description
                self.rowcount = self.sqlite_cur.rowcount
            except Exception as e:
                logger.error(f"[MockDB Error] SQL: {query_final} | Params: {params} | Error: {e}")
                raise

    def fetchone(self):
        with _db_lock:
            return self.sqlite_cur.fetchone()

    def fetchall(self):
        with _db_lock:
            return self.sqlite_cur.fetchall()

    def close(self):
        self.sqlite_cur.close()


class MockConnection:
    def __init__(self, sqlite_conn):
        self.sqlite_conn = sqlite_conn
        self.autocommit = False

    def cursor(self, cursor_factory=None):
        return MockCursor(self.sqlite_conn)

    def commit(self):
        with _db_lock:
            self.sqlite_conn.commit()

    def rollback(self):
        with _db_lock:
            self.sqlite_conn.rollback()

    def close(self):
        pass


class MockSimpleConnectionPool:
    def __init__(self, minconn, maxconn, **kwargs):
        pass

    def getconn(self):
        return MockConnection(_shared_conn)

    def putconn(self, conn):
        pass

    def closeall(self):
        pass


def execute_values(cur, sql, args, page_size=100):
    """Implement psycopg2.extras.execute_values for SQLite inserts."""
    for arg in args:
        # replace %s in INSERT ... VALUES %s with (?, ?, ?, ...)
        placeholders = "(" + ",".join(["?"] * len(arg)) + ")"
        query = sql.replace("%s", placeholders)
        cur.execute(query, arg)


# ─────────────────────────────────────────────────────────────────────────────
# Mock Redis Client & Pipeline
# ─────────────────────────────────────────────────────────────────────────────
class MockRedisPipeline:
    def __init__(self, client):
        self.client = client
        self.commands = []

    def setex(self, key, ttl, value):
        self.commands.append(('setex', key, ttl, value))
        return self

    def sadd(self, key, member):
        self.commands.append(('sadd', key, member))
        return self

    def expire(self, key, ttl):
        self.commands.append(('expire', key, ttl))
        return self

    def hset(self, key, mapping):
        self.commands.append(('hset', key, mapping))
        return self

    def execute(self):
        for cmd in self.commands:
            op = cmd[0]
            if op == 'setex':
                self.client.setex(cmd[1], cmd[2], cmd[3])
            elif op == 'sadd':
                self.client.sadd(cmd[1], cmd[2])
            elif op == 'expire':
                self.client.expire(cmd[1], cmd[2])
            elif op == 'hset':
                self.client.hset(cmd[1], cmd[2])
        self.commands = []


class MockRedis:
    def __init__(self, **kwargs):
        self._cache = {}  # key -> (value, expires_at)
        self._sets = {}   # key -> set
        self._hashes = {} # key -> dict

    def ping(self):
        return True

    def pipeline(self):
        return MockRedisPipeline(self)

    def setex(self, key, ttl, value):
        self._cache[key] = (value, time.time() + ttl)

    def set(self, key, value):
        self._cache[key] = (value, float('inf'))

    def get(self, key):
        if key in self._cache:
            val, expires_at = self._cache[key]
            if time.time() < expires_at:
                return val
            else:
                del self._cache[key]
        return None

    def delete(self, *keys):
        for k in keys:
            self._cache.pop(k, None)
            self._sets.pop(k, None)
            self._hashes.pop(k, None)

    def sadd(self, key, member):
        if key not in self._sets:
            self._sets[key] = set()
        self._sets[key].add(member)

    def smembers(self, key):
        return self._sets.get(key, set())

    def srem(self, key, member):
        if key in self._sets:
            self._sets[key].discard(member)

    def expire(self, key, ttl):
        pass


    def hset(self, key, mapping):
        self._hashes[key] = mapping

    def scan_iter(self, match=None, count=None):
        all_keys = list(self._cache.keys()) + list(self._sets.keys()) + list(self._hashes.keys())
        if match:
            all_keys = [k for k in all_keys if fnmatch.fnmatch(k.lower(), match.lower())]
        return iter(all_keys)


# ─────────────────────────────────────────────────────────────────────────────
# Schema Initialization
# ─────────────────────────────────────────────────────────────────────────────
def _init_sqlite_schema():
    """Load db_schema.sql and transform it into SQLite syntax."""
    schema_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resource_resolver", "db_schema.sql")
    if not os.path.exists(schema_path):
        logger.error(f"db_schema.sql not found at {schema_path}")
        return

    with open(schema_path, "r", encoding="utf-8") as f:
        sql = f.read()

    lines = []
    for line in sql.splitlines():
        if "CREATE EXTENSION" in line:
            continue
        # Use regex to handle variable whitespace
        line = re.sub(r"UUID\s+PRIMARY\s+KEY\s+DEFAULT\s+gen_random_uuid\(\)", "TEXT PRIMARY KEY", line, flags=re.IGNORECASE)
        line = re.sub(r"UUID\s+PRIMARY\s+KEY", "TEXT PRIMARY KEY", line, flags=re.IGNORECASE)
        line = re.sub(r"\bUUID\b", "TEXT", line, flags=re.IGNORECASE)
        line = re.sub(r"TIMESTAMPTZ\s+DEFAULT\s+NOW\(\)", "TEXT DEFAULT CURRENT_TIMESTAMP", line, flags=re.IGNORECASE)
        line = re.sub(r"\bTIMESTAMPTZ\b", "TEXT", line, flags=re.IGNORECASE)
        line = re.sub(r"\bINET\b", "TEXT", line, flags=re.IGNORECASE)
        line = re.sub(r"DEFAULT\s+NOW\(\)", "DEFAULT CURRENT_TIMESTAMP", line, flags=re.IGNORECASE)
        line = line.replace("lower(vendor), lower(device_type), lower(action_key)", "vendor, device_type, action_key")
        # Standard VARCHAR replacements
        for width in [16, 32, 64, 128, 255]:
            line = line.replace(f"VARCHAR({width})", "TEXT")
        lines.append(line)

    sql_clean = "\n".join(lines)
    cur = _shared_conn.cursor()
    for stmt in sql_clean.split(";"):
        stmt = stmt.strip()
        if stmt:
            try:
                cur.execute(stmt)
            except Exception as e:
                logger.error(f"[MockDB] Schema error on statement: {stmt} | Error: {e}")
                raise
    _shared_conn.commit()
    cur.close()
    logger.info("[MockDB] In-memory SQLite schema initialized.")


# ─────────────────────────────────────────────────────────────────────────────
# Device & Endpoint Registry Seeding
# ─────────────────────────────────────────────────────────────────────────────
def _seed_devices():
    """Seed the devices table with 1500+ realistic devices."""
    # Generate 1000 OneView-managed devices
    ov_devices = []
    types = ["server", "switch", "router", "firewall", "storage"]
    for i in range(1000):
        dev_type = types[i % len(types)]
        rack = (i % 50) + 1
        node = (i % 10) + 1
        sn = f"rack{rack}-compute-{node}-{i}"
        fqdn = f"{sn}.datacenter.local"
        ov_devices.append((
            str(uuid.uuid4()), sn, f"10.100.1.{(i % 254) + 1}", fqdn,
            "oneview", "oneview-01.mgmt.local", f"ov-uuid-{i}", dev_type
        ))

    # Generate 500 COMS-managed devices
    coms_devices = []
    for i in range(500):
        idx = 10000 + i
        dev_type = types[idx % len(types)]
        rack = (idx % 50) + 1
        node = (idx % 10) + 1
        sn = f"rack{rack}-compute-{node}-{idx}"
        fqdn = f"{sn}.cloud.local"
        coms_devices.append((
            str(uuid.uuid4()), sn, f"10.200.1.{(i % 254) + 1}", fqdn,
            "coms", "coms-01.cloud.local", f"coms-uuid-{idx}", dev_type
        ))

    # Explicit testing devices matching tests
    testing_devices = [
        # OneView devices
        ("0dcee874-7f57-5049-b1fd-c52e5587ff5c", "OV1-RackServer-001", "10.10.1.1", "OV1-RackServer-001.datacenter.local", "oneview", "oneview-01.mgmt.local", "ov-uuid-001", "server"),
        (str(uuid.uuid4()), "OV1-RackServer-045", "10.10.1.45", "OV1-RackServer-045.datacenter.local", "oneview", "oneview-01.mgmt.local", "c15759d2-cf85-5792-8c65-61402b2b2b50", "server"),
        (str(uuid.uuid4()), "dc1-a7", "10.100.1.10", "dc1-a7.datacenter.local", "oneview", "oneview-01.mgmt.local", "ov-uuid-dc1a7", "server"),
        (str(uuid.uuid4()), "compute-22", "10.100.1.11", "compute-22.datacenter.local", "oneview", "oneview-01.mgmt.local", "ov-uuid-c22", "server"),
        (str(uuid.uuid4()), "rack42-n3", "10.100.1.20", "rack42-n3.datacenter.local", "oneview", "oneview-01.mgmt.local", "ov-uuid-rack42n3", "server"),
        (str(uuid.uuid4()), "edge-r1", "10.100.1.12", "edge-r1.datacenter.local", "oneview", "oneview-01.mgmt.local", "ov-uuid-edger1", "router"),
        (str(uuid.uuid4()), "wan-r2", "10.100.1.21", "wan-r2.datacenter.local", "oneview", "oneview-01.mgmt.local", "ov-uuid-wanr2", "router"),
        (str(uuid.uuid4()), "core-sw01", "10.100.1.13", "core-sw01.datacenter.local", "oneview", "oneview-01.mgmt.local", "ov-uuid-coresw01", "switch"),
        (str(uuid.uuid4()), "core-sw-01", "10.100.1.13", "core-sw-01.datacenter.local", "oneview", "oneview-01.mgmt.local", "ov-uuid-coresw01-hyphen", "switch"),
        (str(uuid.uuid4()), "leaf-sw12", "10.100.1.22", "leaf-sw12.datacenter.local", "oneview", "oneview-01.mgmt.local", "ov-uuid-leafsw12", "switch"),
        (str(uuid.uuid4()), "fw-core-01", "10.100.1.14", "fw-core-01.datacenter.local", "oneview", "oneview-01.mgmt.local", "ov-uuid-fc01", "firewall"),
        (str(uuid.uuid4()), "fw-edge-02", "10.100.1.23", "fw-edge-02.datacenter.local", "oneview", "oneview-01.mgmt.local", "ov-uuid-fwedge02", "firewall"),
        (str(uuid.uuid4()), "prod-vol-001", "10.100.1.15", "prod-vol-001.datacenter.local", "oneview", "oneview-01.mgmt.local", "ov-uuid-prodvol001", "storage"),
        (str(uuid.uuid4()), "dsk-007", "10.100.1.16", "dsk-007.datacenter.local", "oneview", "oneview-01.mgmt.local", "ov-uuid-dsk007", "storage"),

        # COMS devices
        ("97f236a5-548d-5223-b096-6d38059d1d27", "CoM-CloudNode-001", "192.168.100.2", "CoM-CloudNode-001.cloud.local", "coms", "coms-01.cloud.local", "coms-uuid-001", "server"),
        (str(uuid.uuid4()), "MS-123", "192.168.100.123", "MS-123.local", "coms", "coms-01.cloud.local", "coms-uuid-123", "server"),
        (str(uuid.uuid4()), "demo-vm-001", "192.168.100.124", "demo-vm-001.local", "coms", "coms-01.cloud.local", "coms-uuid-demovm001", "server"),
        (str(uuid.uuid4()), "MS-2112", "192.168.100.212", "MS-2112.local", "coms", "coms-01.cloud.local", "coms-uuid-2112", "server"),
        (str(uuid.uuid4()), "CoM-CloudNode-128", "192.168.100.129", "CoM-CloudNode-128.cloud.local", "coms", "coms-01.cloud.local", "3097b130-3c1b-5656-88ef-49c70576410a", "server"),
        (str(uuid.uuid4()), "prod-x1", "10.200.1.13", "prod-x1.cloud.local", "coms", "coms-01.cloud.local", "coms-uuid-prodx1", "server"),
        (str(uuid.uuid4()), "core-r3", "10.200.1.20", "core-r3.cloud.local", "coms", "coms-01.cloud.local", "coms-uuid-corer3", "router"),
        (str(uuid.uuid4()), "agg-sw05", "10.200.1.21", "agg-sw05.cloud.local", "coms", "coms-01.cloud.local", "coms-uuid-aggsw05", "switch"),
        (str(uuid.uuid4()), "fw-west-01", "10.200.1.12", "fw-west-01.cloud.local", "coms", "coms-01.cloud.local", "coms-uuid-fwwest01", "firewall"),
        (str(uuid.uuid4()), "stg-array-02", "10.200.1.11", "stg-array-02.cloud.local", "coms", "coms-01.cloud.local", "coms-uuid-stgarray02", "storage"),
        (str(uuid.uuid4()), "nas-prod-01", "10.200.1.10", "nas-prod-01.cloud.local", "coms", "coms-01.cloud.local", "coms-uuid-np01", "storage"),
        (str(uuid.uuid4()), "backup-san-01", "10.200.1.22", "backup-san-01.cloud.local", "coms", "coms-01.cloud.local", "coms-uuid-backupsan01", "storage"),
    ]

    cur = _shared_conn.cursor()
    insert_sql = """
        INSERT INTO devices (
            id, serial_number, ip_address, fqdn,
            management_source, source_host, source_device_id,
            device_type, last_seen, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
    """
    cur.executemany(insert_sql, ov_devices)
    cur.executemany(insert_sql, coms_devices)
    cur.executemany(insert_sql, testing_devices)
    _shared_conn.commit()
    cur.close()
    logger.info(f"[MockDB] Seeded {len(ov_devices) + len(coms_devices) + len(testing_devices)} devices.")


def _seed_endpoints():
    """Parse prompt files and seed endpoint_registry."""
    resolver_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resource_resolver")
    oneview_prompts = os.path.join(resolver_dir, "oneview_api_prompts.txt")
    comops_prompts = os.path.join(resolver_dir, "comops_api_prompts.txt")

    entries = []
    # Simple regex parsing matching seed_endpoint_registry.py
    for fp in [oneview_prompts, comops_prompts]:
        if not os.path.exists(fp):
            continue
        with open(fp, "r", encoding="utf-8") as fh:
            text = fh.read()
        blocks = re.split(r"={10,}", text)
        for block in blocks:
            lines = [ln.strip() for ln in block.splitlines() if ln.strip()]
            action = method = path = None
            for ln in lines:
                if m := re.match(r"^Action Key\s*:\s*(.+)$", ln, re.IGNORECASE):
                    action = m.group(1).strip()
                elif m := re.match(r"^Method\s*:\s*(.+)$", ln, re.IGNORECASE):
                    method = m.group(1).strip().upper()
                elif m := re.match(r"^API Path\s*:\s*(.+)$", ln, re.IGNORECASE):
                    path = m.group(1).strip()
            
            if action and method and path:
                if "{resource_category}" not in path:
                    entries.append((action, method, path))

    # De-duplicate and normalize semantic actions
    rows_to_insert = []
    seen = set()
    
    if resolver_dir not in sys.path:
        sys.path.insert(0, resolver_dir)
    from seed_endpoint_registry import _infer_vendor, _infer_device_type, _normalize_action_key

    for action, method, path in entries:
        vendor = _infer_vendor(path)
        dtype = _infer_device_type(path, vendor)
        normalized_actions = _normalize_action_key(vendor, action, method, path)
        for act in normalized_actions:
            key = (vendor, dtype, act, method, path)
            if key not in seen:
                seen.add(key)
                rows_to_insert.append((
                    str(uuid.uuid4()), vendor, dtype, act, method, path
                ))

    cur = _shared_conn.cursor()
    cur.executemany(
        """
        INSERT INTO endpoint_registry (id, vendor, device_type, action_key, http_method, api_path)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        rows_to_insert
    )
    _shared_conn.commit()
    cur.close()
    logger.info(f"[MockDB] Seeded {len(rows_to_insert)} API endpoints.")


# ─────────────────────────────────────────────────────────────────────────────
# Setup and Injection Hook
# ─────────────────────────────────────────────────────────────────────────────
def setup():
    """Perform module injection to mock psycopg2 and redis."""
    if "psycopg2" in sys.modules and hasattr(sys.modules["psycopg2"], "_is_mock"):
        # Already set up
        return

    # 1. Create SQLite tables and seed data
    _init_sqlite_schema()
    _seed_devices()
    _seed_endpoints()

    # 2. Build mock modules
    mock_psycopg2_mod = types.ModuleType("psycopg2")
    mock_psycopg2_mod._is_mock = True
    mock_psycopg2_mod.Error = Error
    mock_psycopg2_mod.ProgrammingError = ProgrammingError
    mock_psycopg2_mod.OperationalError = OperationalError
    mock_psycopg2_mod.connect = lambda *a, **kw: MockConnection(_shared_conn)

    mock_psycopg2_pool_mod = types.ModuleType("psycopg2.pool")
    mock_psycopg2_pool_mod.SimpleConnectionPool = MockSimpleConnectionPool

    mock_psycopg2_extras_mod = types.ModuleType("psycopg2.extras")
    mock_psycopg2_extras_mod.RealDictCursor = object
    mock_psycopg2_extras_mod.execute_values = execute_values

    mock_psycopg2_extensions_mod = types.ModuleType("psycopg2.extensions")
    mock_psycopg2_extensions_mod.connection = MockConnection

    mock_redis_mod = types.ModuleType("redis")
    mock_redis_mod.Redis = MockRedis
    mock_redis_mod.exceptions = types.ModuleType("redis.exceptions")
    mock_redis_mod.exceptions.ConnectionError = Exception

    # 3. Inject mock modules into sys.modules
    sys.modules["psycopg2"] = mock_psycopg2_mod
    sys.modules["psycopg2.pool"] = mock_psycopg2_mod.pool = mock_psycopg2_pool_mod
    sys.modules["psycopg2.extras"] = mock_psycopg2_mod.extras = mock_psycopg2_extras_mod
    sys.modules["psycopg2.extensions"] = mock_psycopg2_mod.extensions = mock_psycopg2_extensions_mod
    sys.modules["redis"] = mock_redis_mod
    sys.modules["redis.exceptions"] = mock_redis_mod.exceptions

    logger.info("[MockDB] Mock psycopg2 & redis modules successfully injected.")
