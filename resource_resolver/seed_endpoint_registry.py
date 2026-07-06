"""
seed_endpoint_registry.py
=========================
Parse oneview_api_prompts.txt and comops_api_prompts.txt, then bulk-insert
ONLY the exact endpoints (as written in the files) into endpoint_registry.

Rules
-----
* Generic paths containing ``{resource_category}`` are SKIPPED entirely.
* Only verbatim exact paths from the txt files are stored.
* device_type is inferred deterministically from the resource segment in
  each api_path (e.g. /rest/server-hardware/... → "server").
* Idempotent — uses ON CONFLICT DO NOTHING, safe to re-run.

Usage
-----
    .venv\\Scripts\\python.exe seed_endpoint_registry.py
"""
from __future__ import annotations

import logging
import os
import re
import sys

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, THIS_DIR)

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(name)s: %(message)s",
)
logger = logging.getLogger("seed_endpoint_registry")

# ---------------------------------------------------------------------------
# Resource segment → device_type mapping
# Keyed by the exact resource path segment; used for device_type inference.
# ---------------------------------------------------------------------------
RESOURCE_TO_DEVICE_TYPE: dict[str, str] = {
    # OneView
    "server-hardware":            "server",
    "rack-managers":              "rack_manager",
    "storage-volumes":            "storage",
    "storage-systems":            "storage",
    "ethernet-networks":          "network",
    "interconnects":              "switch",
    "updates":                    "update",
    "certificates":               "certificate",
    "login-sessions":             "session",
    # COMS v1
    "servers":                    "server",
    "storage":                    "storage",
    "switches":                   "switch",
    "networks":                   "network",
    "groups":                     "group",
    "jobs":                       "job",
    "firmware-bundles":           "firmware",
    "appliance-firmware-bundles": "firmware",
    "settings":                   "settings",
    "metrics-configurations":     "metrics",
    "user-preferences":           "user_pref",
    "async-operations":           "async_op",
    # COMS v1beta1
    "activation-keys":            "auth",
    "activation-tokens":          "auth",
    "ahs-files":                  "log",
    "external-services":          "service",
    "filters":                    "filter",
    "oneview-appliances":         "appliance",
    "oneview-server-templates":   "template",
    "oneview-settings":           "settings",
    "server-locations":           "location",
    "webhooks":                   "webhook",
    "energy-by-entity":           "energy",
    "energy-over-time":           "energy",
    "utilization-by-entity":      "utilization",
    "utilization-over-time":      "utilization",
    # COMS v1beta2
    "activities":                 "activity",
    "appliances":                 "appliance",
    "approval-policies":          "policy",
    "approval-requests":          "request",
    "job-templates":              "job",
    "reports":                    "report",
    "schedules":                  "schedule",
    "server-warranty":            "warranty",
    # compute-ops (legacy)
    "server-settings":            "settings",
}

# ---------------------------------------------------------------------------
# Path parsing regexes
# ---------------------------------------------------------------------------
_BLOCK_SEP   = re.compile(r"={10,}")
_ACTION_LINE = re.compile(r"^Action Key\s*:\s*(.+)$", re.IGNORECASE)
_METHOD_LINE = re.compile(r"^Method\s*:\s*(.+)$",     re.IGNORECASE)
_PATH_LINE   = re.compile(r"^API Path\s*:\s*(.+)$",   re.IGNORECASE)

_ONEVIEW_RESOURCE_RE = re.compile(r"^/rest/([^/{]+)")
_COMS_RESOURCE_RE    = re.compile(r"^/compute-ops(?:-mgmt)?/[^/]+/([^/{]+)")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _infer_vendor(api_path: str) -> str:
    p = api_path.strip().lower()
    if p.startswith("/rest/"):
        return "oneview"
    if p.startswith("/compute-ops"):
        return "comops"
    parts = [x for x in p.split("/") if x]
    return parts[0] if parts else "unknown"


def _infer_device_type(api_path: str, management_source: str) -> list[str]:
    """
    Heuristically extract the resource type from the API path,
    and then map it to the corresponding CMDB device_type.
    Returns a list of device types. If the endpoint is specific, the list
    contains only that specific device type. If it is generic, it returns
    all valid device types for that management source.
    """
    management_source = management_source.lower()
    words = api_path.lower().replace('/', ' ').replace('-', ' ').replace('_', ' ').split()

    # --- MAP TO CMDB DEVICE TYPE ---
    if management_source == 'oneview':
        if any(k in words for k in ['switch', 'switches', 'interconnect', 'interconnects', 'uplink', 'uplinks']): return ['switch']
        if any(k in words for k in ['storage', 'volume', 'volumes', 'san', 'jbod']): return ['storage']
        if any(k in words for k in ['network', 'networks', 'router', 'routers']): return ['router']
        if any(k in words for k in ['firewall', 'firewalls']): return ['firewall']
        if any(k in words for k in ['server', 'servers', 'hardware', 'chassis', 'manager', 'managers']): return ['server']
        return ['server', 'storage', 'switch', 'router', 'firewall']

    elif management_source in ['comops']:
        if any(k in words for k in ['switch', 'switches']): return ['switch']
        if any(k in words for k in ['router', 'routers']): return ['router']
        if any(k in words for k in ['firewall', 'firewalls']): return ['firewall']
        if any(k in words for k in ['storage']): return ['storage']
        if any(k in words for k in ['server', 'servers', 'appliance', 'appliances']): return ['server']
        return ['server', 'storage', 'switch', 'router', 'firewall']

    elif management_source in ['ilo', 'mock_server']:
        if any(k in words for k in ['chassis']): return ['blade_server']
        if any(k in words for k in ['processor', 'processors', 'compute']): return ['compute_node']
        if any(k in words for k in ['manager', 'managers']): return ['rack_server']
        if any(k in words for k in ['switch', 'switches']): return ['switch']
        if any(k in words for k in ['router', 'routers']): return ['router']
        if any(k in words for k in ['firewall', 'firewalls']): return ['firewall']
        if any(k in words for k in ['server', 'servers', 'system', 'systems']): return ['server']
        return ['server', 'blade_server', 'compute_node', 'rack_server']

    elif management_source in ['storage', 'mock_storage']:
        if any(k in words for k in ['volume', 'volumes']): return ['volume']
        if any(k in words for k in ['pool', 'pools']): return ['storage_pool']
        if any(k in words for k in ['host', 'hosts']): return ['host']
        if any(k in words for k in ['snapshot', 'snapshots']): return ['snapshot']
        if any(k in words for k in ['filesystem', 'filesystems']): return ['filesystem']
        if any(k in words for k in ['system', 'systems']): return ['storage_system']
        return ['storage_system', 'volume', 'host', 'storage_pool', 'snapshot', 'filesystem', 'host_group', 'volume_set']

    elif management_source in ['network', 'mock_network']:
        if any(k in words for k in ['ap', 'aps', 'access']): return ['access_point']
        if any(k in words for k in ['switch', 'switches', 'vsx']): return ['switch']
        if any(k in words for k in ['gateway', 'gateways']): return ['gateway']
        if any(k in words for k in ['vlan', 'vlans']): return ['vlan']
        if any(k in words for k in ['router', 'routers']): return ['router']
        if any(k in words for k in ['firewall', 'firewalls']): return ['firewall']
        if any(k in words for k in ['controller', 'controllers']): return ['wireless_controller']
        return ['switch', 'access_point', 'gateway', 'vlan', 'router', 'firewall', 'wireless_controller']

    elif management_source in ['cloud', 'mock_cloud']:
        if any(k in words for k in ['virtual', 'vm', 'vms']): return ['virtual_machine']
        if any(k in words for k in ['kubernetes', 'cluster', 'clusters']): return ['kubernetes_cluster']
        if any(k in words for k in ['load', 'lb']): return ['load_balancer']
        if any(k in words for k in ['subnet', 'subnets', 'network', 'networks']): return ['subnet']
        if any(k in words for k in ['namespace', 'namespaces']): return ['namespace']
        if any(k in words for k in ['database', 'databases', 'db']): return ['database_service']
        return ['virtual_machine', 'kubernetes_cluster', 'load_balancer', 'subnet', 'namespace', 'database_service']

    return ['generic']

def _infer_resource_type(api_path: str) -> str | None:
    path_lower = api_path.lower()
    import re
    words = set(re.findall(r'[a-z0-9]+', path_lower))
    
    # Core resources
    if any(k in words for k in ['firmware', 'firmwareinventory', 'updates', 'updateservice', 'update']): return 'firmware'
    if any(k in words for k in ['certificate', 'certificates', 'certificateservice', 'ca']): return 'certificate'
    if any(k in words for k in ['metric', 'metrics', 'metricreport', 'telemetry', 'telemetryservice']): return 'metric'
    if any(k in words for k in ['account', 'accounts', 'user', 'users', 'accountservice']): return 'account'
    if any(k in words for k in ['session', 'sessions', 'sessionservice', 'login']): return 'session'
    if any(k in words for k in ['event', 'events', 'eventservice', 'log', 'logs', 'logservice']): return 'event'
    if any(k in words for k in ['license', 'licenses', 'licensing']): return 'license'
    if any(k in words for k in ['profile', 'profiles', 'server_profile', 'serverprofile']): return 'profile'
    if any(k in words for k in ['power', 'powerstate', 'computersystem', 'reset']): return 'power'
    if any(k in words for k in ['issue', 'issues', 'alert', 'alerts']): return 'issue'
    if any(k in words for k in ['port', 'ports', 'interface', 'interfaces']): return 'port'
    if any(k in words for k in ['route', 'routes']): return 'route'
    
    # Fallback: extract last meaningful segment
    path_clean = re.sub(r'/\{[^}]+\}', '', api_path.rstrip('/'))
    segments = path_clean.split('/')
    if segments:
        return segments[-1].lower()
    
    return 'generic'

# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------

def generate_raw_action_key(http_method: str, api_path: str) -> str:
    import re
    clean_path = re.sub(r'[{}]', '', api_path).replace('-', '_')
    parts = [http_method.lower()] + [p for p in clean_path.split('/') if p]
    return "_".join(parts)


def parse_routes_dump(filepath: str) -> list[dict]:
    """
    Parse the routes_dump.txt file instead of missing prompt files.
    """
    entries: list[dict] = []
    seen: set[tuple] = set()
    skipped = 0

    with open(filepath, encoding="utf-8") as fh:
        vendor = None
        for line in fh:
            line = line.strip()
            if not line: continue
            
            if line.startswith('--- Vendor:'):
                # e.g., --- Vendor: cloud ---
                parts = line.split(':')
                if len(parts) >= 2:
                    vendor = parts[1].strip().split()[0].lower()
                continue
                
            if not vendor: continue
                
            parts = line.split(' ', 1)
            if len(parts) != 2: continue
            
            http_method, api_path = parts[0].strip().upper(), parts[1].strip()
            
            # Skip generics
            if "{resource_category}" in api_path:
                skipped += 1
                continue
                
            action_key = generate_raw_action_key(http_method, api_path)
            
            # Note: the dump includes 'cloud' and 'storage', etc. The vendor
            # normalization in build_rows will handle inferring if needed.
            # But the DB expects 'management_source' to be 'comops' instead of 'cloud' if it's coms.
            # Let's map it cleanly if needed:
            ms = vendor.lower()
            if ms == "ilo": ms = "mock_server"
            elif ms == "cloud": ms = "mock_cloud"
            elif ms == "storage": ms = "storage"
            elif ms == "network": ms = "network"
                
            key = (ms, action_key, http_method, api_path)
            if key not in seen:
                seen.add(key)
                entries.append({
                    "action_key": action_key,
                    "http_method": http_method,
                    "api_path": api_path,
                    "management_source": ms # Pass explicit vendor to build_rows
                })

    logger.info(
        "%-40s  %3d exact entries  (%d generic skipped)",
        os.path.basename(filepath), len(entries), skipped,
    )
    return entries


# ---------------------------------------------------------------------------
# Normalize and Build rows
# ---------------------------------------------------------------------------

def _normalize_action_key(vendor: str, raw_action_key: str, http_method: str, api_path: str) -> list[str]:
    """
    Map an exact endpoint path and HTTP method to normalized semantic actions:
    ON, OFF, RESET, COLD_BOOT, STATUS, CREATE, DELETE, ALLOCATE, DEALLOCATE, LIST.
    
    If the endpoint does not map to any semantic action, returns [raw_action_key].
    """
    vendor = vendor.lower()
    http_method = http_method.upper()
    path_lower = api_path.lower()
    
    # 1. Power operations
    if path_lower.endswith("/powerstate") or "/powerstate/" in path_lower:
        if http_method in ("PUT", "POST", "PATCH"):
            return ["ON", "OFF", "RESET", "COLD_BOOT"]
    elif path_lower.endswith("/power-on"):
        if http_method in ("PUT", "POST", "PATCH"):
            return ["ON"]
    elif path_lower.endswith("/power-off"):
        if http_method in ("PUT", "POST", "PATCH"):
            return ["OFF"]
    elif path_lower.endswith("/reboot") or path_lower.endswith("/restart") or path_lower.endswith("/reset") or path_lower.endswith("computersystem.reset"):
        if http_method in ("PUT", "POST", "PATCH"):
            return ["ON", "OFF", "RESET", "COLD_BOOT"]
    elif path_lower.endswith("/cold-boot") or path_lower.endswith("/coldboot"):
        if http_method in ("PUT", "POST", "PATCH"):
            return ["COLD_BOOT"]
            
    # 1.5 Operational / Sensor / Log / Media operations
    if "/logservices/" in path_lower and path_lower.endswith("/entries"):
        if http_method == "GET":
            return ["FETCH_EVENT_LOG"]
    elif path_lower.endswith("clearlog"):
        if http_method in ("PUT", "POST", "PATCH"):
            return ["CLEAR_EVENT_LOG"]
    elif "virtualmedia" in path_lower and path_lower.endswith("insertmedia"):
        if http_method in ("PUT", "POST", "PATCH"):
            return ["MOUNT_VIRTUAL_MEDIA"]
    elif "/sensors" in path_lower or "/thermal" in path_lower:
        if http_method == "GET":
            return ["FETCH_SENSORS"]
    elif "/firmwareinventory" in path_lower or "/inventory" in path_lower:
        if http_method == "GET":
            return ["DISCOVER_INVENTORY"]
    elif path_lower.endswith("/failover"):
        if http_method in ("PUT", "POST", "PATCH"):
            return ["FAILOVER"]

    # 2. Single resource lookups / deletions (STATUS, DELETE, DEALLOCATE)
    is_single_resource = False
    
    if vendor == "oneview":
        parts = [p for p in api_path.split("/") if p]
        if len(parts) == 3 and parts[0] == "rest" and parts[2].startswith("{") and parts[2].endswith("}"):
            is_single_resource = True
    elif "mock_server" in vendor or "ilo" in vendor:
        parts = [p for p in api_path.split("/") if p]
        if len(parts) == 4 and parts[0] == "redfish" and parts[3].startswith("{") and parts[3].endswith("}"):
            is_single_resource = True
    else: # COMS or cloud mocks
        parts = [p for p in api_path.split("/") if p]
        if len(parts) >= 4 and parts[-1].startswith("{") and parts[-1].endswith("}") and not path_lower.endswith("power"):
            is_single_resource = True

    if is_single_resource:
        if http_method == "GET":
            return ["STATUS"]
        elif http_method == "DELETE":
            return ["DELETE", "DEALLOCATE"]
        elif http_method in ("PUT", "PATCH"):
            return ["UPDATE"]

    # 3. Collection POSTs (CREATE, ALLOCATE) and GETs (LIST)
    is_collection = False
    if vendor == "oneview":
        parts = [p for p in api_path.split("/") if p]
        if len(parts) == 2 and parts[0] == "rest" and not ("{" in parts[1] or "}" in parts[1]):
            is_collection = True
    elif "mock_server" in vendor or "ilo" in vendor:
        parts = [p for p in api_path.split("/") if p]
        if len(parts) == 3 and parts[0] == "redfish" and not ("{" in parts[2] or "}" in parts[2]):
            is_collection = True
    else: # COMS or cloud
        parts = [p for p in api_path.split("/") if p]
        if len(parts) >= 3 and not ("{" in parts[-1] or "}" in parts[-1]):
            is_collection = True

    if is_collection:
        if http_method == "POST":
            return ["CREATE", "ALLOCATE"]
        elif http_method == "GET":
            return ["LIST"]
        elif http_method in ("PUT", "PATCH"):
            return ["UPDATE"]
        elif http_method == "DELETE":
            return ["CLEAR", "DELETE"]

    return [raw_action_key]


def build_rows(entries: list[dict]) -> list[dict]:
    """Attach vendor + device_type to each exact entry, normalize action keys, and deduplicate."""
    rows: list[dict] = []
    seen: set[tuple] = set()

    for e in entries:
        api_path    = e["api_path"]
        vendor      = e.get("management_source") or _infer_vendor(api_path)
        device_types = _infer_device_type(api_path, vendor)
        resource_type = _infer_resource_type(api_path)

        action_keys = _normalize_action_key(vendor, e["action_key"], e["http_method"], api_path)
        for ak in action_keys:
            key = (vendor, ak, e["http_method"], api_path)
            if key in seen:
                continue
            seen.add(key)

            rows.append(
                {
                    "management_source": vendor,
                    "device_types":  device_types,
                    "resource_type": resource_type,
                    "action_key":   ak,
                    "http_method":  e["http_method"],
                    "api_path":     api_path,
                }
            )

    logger.info("Built %d unique rows for insertion.", len(rows))
    return rows


# ---------------------------------------------------------------------------
# Seeder
# ---------------------------------------------------------------------------

def seed(rows: list[dict]) -> int:
    """Bulk-insert with ON CONFLICT DO NOTHING after truncating. Returns number of rows inserted."""
    if not rows:
        logger.warning("No rows to seed.")
        return 0

    from db import db_manager
    from psycopg2 import extras

    unique_device_types = set()
    unique_resource_types = set()
    for r in rows:
        unique_device_types.update(r["device_types"])
        if r.get("resource_type"):
            unique_resource_types.add(r["resource_type"])
            
    conn = db_manager.get_connection()
    inserted = 0
    try:
        with conn.cursor() as cur:
            # 1. Populate device_type mapping table
            logger.info("Ensuring %d unique device types exist in device_type...", len(unique_device_types))
            extras.execute_values(
                cur,
                "INSERT INTO device_type (name) VALUES %s ON CONFLICT (name) DO NOTHING",
                [(dt,) for dt in unique_device_types],
                page_size=250,
            )
            
            # 2. Populate resource_type table
            if unique_resource_types:
                logger.info("Ensuring %d unique resource types exist in resource_type...", len(unique_resource_types))
                extras.execute_values(
                    cur,
                    "INSERT INTO resource_type (res_type) VALUES %s ON CONFLICT (res_type) DO NOTHING",
                    [(rt,) for rt in unique_resource_types],
                    page_size=250,
                )
            
            # Fetch the new/existing IDs
            cur.execute("SELECT id, name FROM device_type")
            dt_to_id = {row[1]: row[0] for row in cur.fetchall()}
            
            cur.execute("SELECT id, res_type FROM resource_type")
            rt_to_id = {row[1]: row[0] for row in cur.fetchall()}

            # 3. Seed endpoint_registry
            logger.info("Truncating tables to start fresh...")
            cur.execute("TRUNCATE TABLE endpoint_device_mapping CASCADE;")
            cur.execute("TRUNCATE TABLE endpoint_registry CASCADE;")

            args = [
                (
                    r.get("management_source", r.get("vendor")), 
                    r["action_key"], 
                    r["http_method"], 
                    r["api_path"], 
                    rt_to_id.get(r["resource_type"]) if r.get("resource_type") else None
                )
                for r in rows
            ]
            
            insert_query = """
                INSERT INTO endpoint_registry
                    (management_source, action_key, http_method, api_path, resource_type_id)
                VALUES %s
                ON CONFLICT (management_source, action_key, api_path, http_method)
                DO NOTHING
                RETURNING id, management_source, action_key, http_method, api_path
            """
            
            extras.execute_values(cur, insert_query, args, page_size=250, template="(%s, %s, %s, %s, %s)")
            
            cur.execute("SELECT id, management_source, action_key, http_method, api_path FROM endpoint_registry")
            endpoint_map = {(row[1], row[2], row[3], row[4]): row[0] for row in cur.fetchall()}
            
            # 4. Insert mappings
            mapping_args = []
            for r in rows:
                ep_key = (r.get("management_source", r.get("vendor")), r["action_key"], r["http_method"], r["api_path"])
                ep_id = endpoint_map.get(ep_key)
                if ep_id:
                    for dt in r["device_types"]:
                        if dt in dt_to_id:
                            mapping_args.append((ep_id, dt_to_id[dt]))
            
            if mapping_args:
                extras.execute_values(
                    cur,
                    "INSERT INTO endpoint_device_mapping (endpoint_id, device_type_id) VALUES %s ON CONFLICT DO NOTHING",
                    mapping_args,
                    page_size=250
                )
            
            inserted = len(endpoint_map)
        conn.commit()
        logger.info(
            "Seed complete: %d inserted.",
            inserted,
        )
    except Exception:
        conn.rollback()
        logger.exception("Seed failed — transaction rolled back.")
        raise
    finally:
        db_manager.return_connection(conn)

    return inserted


# ---------------------------------------------------------------------------
# Verification
# ---------------------------------------------------------------------------

def verify() -> None:
    """Print a summary of what is now in endpoint_registry."""
    from db import db_manager

    rows = db_manager.execute_query(
        """
        SELECT e.management_source, d.name, count(*) AS cnt
        FROM   endpoint_registry e
        JOIN   endpoint_device_mapping m ON e.id = m.endpoint_id
        JOIN   device_type d ON m.device_type_id = d.id
        GROUP  BY e.management_source, d.name
        ORDER  BY e.management_source, d.name
        """,
        fetch_all=True,
    )
    if not rows:
        logger.warning("endpoint_registry is empty after seeding!")
        return

    logger.info("── endpoint_registry summary ──────────────────────────")
    for r in rows:
        logger.info("  %-12s %-20s %4d rows", r["management_source"], r["name"], r["cnt"])

    # Spot-check power ops
    spot = db_manager.execute_query(
        """
        SELECT e.management_source, d.name, e.action_key, e.http_method, e.api_path
        FROM   endpoint_registry e
        JOIN   endpoint_device_mapping m ON e.id = m.endpoint_id
        JOIN   device_type d ON m.device_type_id = d.id
        WHERE  e.action_key IN ('ON', 'OFF', 'RESET', 'COLD_BOOT')
        ORDER  BY e.management_source, d.name, e.action_key
        """,
        fetch_all=True,
    )
    if spot:
        logger.info("── Power Ops Spot Check ─────────────────────────────")
        for r in spot[:5]:
            logger.info("  %s %s: [%s] %s %s", 
                        r["management_source"], r["name"], r["action_key"],
                        r["http_method"], r["api_path"])


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    dump_file = os.path.join(os.path.dirname(THIS_DIR), "scratch", "routes_dump.txt")

    all_entries: list[dict] = []
    if os.path.exists(dump_file):
        all_entries.extend(parse_routes_dump(dump_file))
    else:
        logger.warning("Routes dump file not found — skipping: %s", dump_file)

    logger.info("Total exact entries from all files: %d", len(all_entries))

    rows = build_rows(all_entries)

    # Breakdown before insert
    breakdown: dict[str, dict[str, int]] = {}
    for r in rows:
        ms = r.get("management_source", r.get("vendor"))
        breakdown.setdefault(ms, {})
        dt_str = ", ".join(sorted(r["device_types"]))
        breakdown[ms][dt_str] = (
            breakdown[ms].get(dt_str, 0) + 1
        )
    for vendor, dtypes in sorted(breakdown.items()):
        for dtype, cnt in sorted(dtypes.items()):
            logger.info("  %-12s %-20s %4d rows", vendor, dtype, cnt)

    seed(rows)
    verify()


if __name__ == "__main__":
    main()
