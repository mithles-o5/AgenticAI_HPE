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
        return "coms"
    parts = [x for x in p.split("/") if x]
    return parts[0] if parts else "unknown"


def _infer_device_type(api_path: str, vendor: str) -> str:
    if vendor == "oneview":
        m = _ONEVIEW_RESOURCE_RE.match(api_path)
    else:
        m = _COMS_RESOURCE_RE.match(api_path)
    seg = m.group(1).lower() if m else None
    if seg is None:
        return "generic"
    return RESOURCE_TO_DEVICE_TYPE.get(seg, "generic")


# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------

def parse_prompt_file(filepath: str) -> list[dict]:
    """
    Parse one prompt reference file.
    Generic paths ({resource_category}) are SKIPPED.
    Returns a list of exact-path entries:
        [{"action_key": ..., "http_method": ..., "api_path": ...}, ...]
    """
    with open(filepath, encoding="utf-8") as fh:
        text = fh.read()

    blocks  = _BLOCK_SEP.split(text)
    entries: list[dict] = []
    seen:    set[tuple] = set()
    skipped = 0

    for block in blocks:
        lines      = [ln.strip() for ln in block.splitlines() if ln.strip()]
        action_key = http_method = api_path = None

        for line in lines:
            if m := _ACTION_LINE.match(line):
                action_key = m.group(1).strip()
            elif m := _METHOD_LINE.match(line):
                http_method = m.group(1).strip().upper()
            elif m := _PATH_LINE.match(line):
                api_path = m.group(1).strip()

        if not (action_key and http_method and api_path):
            continue

        # ── Skip generic templates entirely ───────────────────────────────
        if "{resource_category}" in api_path:
            skipped += 1
            continue

        key = (action_key, http_method, api_path)
        if key not in seen:
            seen.add(key)
            entries.append(
                {
                    "action_key":  action_key,
                    "http_method": http_method,
                    "api_path":    api_path,
                }
            )

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
    elif path_lower.endswith("/reboot") or path_lower.endswith("/restart") or path_lower.endswith("/reset"):
        if http_method in ("PUT", "POST", "PATCH"):
            return ["RESET"]
    elif path_lower.endswith("/cold-boot") or path_lower.endswith("/coldboot"):
        if http_method in ("PUT", "POST", "PATCH"):
            return ["COLD_BOOT"]

    # 2. Single resource lookups / deletions (STATUS, DELETE, DEALLOCATE)
    is_single_resource = False
    
    if vendor == "oneview":
        parts = [p for p in api_path.split("/") if p]
        if len(parts) == 3 and parts[0] == "rest" and parts[2].startswith("{") and parts[2].endswith("}"):
            is_single_resource = True
    else: # COMS
        parts = [p for p in api_path.split("/") if p]
        if len(parts) == 4 and parts[0].startswith("compute-ops") and parts[3].startswith("{") and parts[3].endswith("}"):
            is_single_resource = True

    if is_single_resource:
        if http_method == "GET":
            return ["STATUS"]
        elif http_method == "DELETE":
            return ["DELETE", "DEALLOCATE"]

    # 3. Collection POSTs (CREATE, ALLOCATE) and GETs (LIST)
    is_collection = False
    if vendor == "oneview":
        parts = [p for p in api_path.split("/") if p]
        if len(parts) == 2 and parts[0] == "rest" and not ("{" in parts[1] or "}" in parts[1]):
            is_collection = True
    else: # COMS
        parts = [p for p in api_path.split("/") if p]
        if len(parts) == 3 and parts[0].startswith("compute-ops") and not ("{" in parts[2] or "}" in parts[2]):
            is_collection = True

    if is_collection:
        if http_method == "POST":
            return ["CREATE", "ALLOCATE"]
        elif http_method == "GET":
            return ["LIST"]

    return [raw_action_key]


def build_rows(entries: list[dict]) -> list[dict]:
    """Attach vendor + device_type to each exact entry, normalize action keys, and deduplicate."""
    rows: list[dict] = []
    seen: set[tuple] = set()

    for e in entries:
        api_path    = e["api_path"]
        vendor      = _infer_vendor(api_path)
        device_type = _infer_device_type(api_path, vendor)

        action_keys = _normalize_action_key(vendor, e["action_key"], e["http_method"], api_path)
        for ak in action_keys:
            key = (vendor, device_type, ak, e["http_method"], api_path)
            if key in seen:
                continue
            seen.add(key)

            rows.append(
                {
                    "vendor":       vendor,
                    "device_type":  device_type,
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

    conn = db_manager.get_connection()
    inserted = 0
    try:
        with conn.cursor() as cur:
            logger.info("Truncating endpoint_registry table to start fresh...")
            cur.execute("TRUNCATE TABLE endpoint_registry;")
            
            args = [
                (r["vendor"], r["device_type"], r["action_key"],
                 r["http_method"], r["api_path"])
                for r in rows
            ]
            extras.execute_values(
                cur,
                """
                INSERT INTO endpoint_registry
                    (vendor, device_type, action_key, http_method, api_path)
                VALUES %s
                ON CONFLICT (vendor, device_type, action_key, api_path, http_method)
                DO NOTHING
                """,
                args,
                page_size=250,
            )
            inserted = cur.rowcount
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
        SELECT vendor, device_type, count(*) AS cnt
        FROM   endpoint_registry
        GROUP  BY vendor, device_type
        ORDER  BY vendor, device_type
        """,
        fetch_all=True,
    )
    if not rows:
        logger.warning("endpoint_registry is empty after seeding!")
        return

    logger.info("── endpoint_registry summary ──────────────────────────")
    for r in rows:
        logger.info("  %-12s %-20s %4d rows", r["vendor"], r["device_type"], r["cnt"])

    # Spot-check power ops
    spot = db_manager.execute_query(
        """
        SELECT vendor, device_type, action_key, http_method, api_path
        FROM   endpoint_registry
        WHERE  lower(action_key) = ANY(ARRAY['on','off','status','reset','list','cold_boot'])
           OR  lower(api_path) LIKE '%%power%%'
        ORDER  BY vendor, device_type, action_key
        LIMIT  20
        """,
        fetch_all=True,
    )

    if spot:
        logger.info("── spot-check (power-related endpoints) ──────────────")
        for r in spot:
            logger.info(
                "  %-10s %-12s %-10s %-6s  %s",
                r["vendor"], r["device_type"], r["action_key"],
                r["http_method"], r["api_path"],
            )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    prompt_files = [
        os.path.join(THIS_DIR, "oneview_api_prompts.txt"),
        os.path.join(THIS_DIR, "comops_api_prompts.txt"),
    ]

    all_entries: list[dict] = []
    for fp in prompt_files:
        if not os.path.exists(fp):
            logger.warning("Prompt file not found — skipping: %s", fp)
            continue
        all_entries.extend(parse_prompt_file(fp))

    logger.info("Total exact entries from all files: %d", len(all_entries))

    rows = build_rows(all_entries)

    # Explicitly seed mock_cloud endpoints for all cloud resource types
    cloud_types = [
        "vm", "virtual_machine", "kubernetes_cluster", "database_service",
        "storage_service", "virtual_network", "subnet", "load_balancer", "namespace"
    ]
    for dtype in cloud_types:
        cloud_endpoints = [
            ("STATUS", "GET", "/api/v1/devices/{id}"),
            ("ON", "POST", "/api/v1/devices/{id}/power"),
            ("OFF", "POST", "/api/v1/devices/{id}/power"),
            ("RESET", "POST", "/api/v1/devices/{id}/power"),
            ("COLD_BOOT", "POST", "/api/v1/devices/{id}/power"),
            ("LIST", "GET", "/api/v1/devices"),
            ("RESCAN", "GET", "/api/v1/devices"),
            ("UPDATE", "PATCH", "/api/v1/devices/{id}"),
        ]
        for act, method, path in cloud_endpoints:
            rows.append({
                "vendor": "mock_cloud",
                "device_type": dtype,
                "action_key": act,
                "http_method": method,
                "api_path": path
            })

    # Explicitly seed mock_server endpoints for server types
    server_types = ["server", "server-hardware"]
    for dtype in server_types:
        server_endpoints = [
            ("STATUS", "GET", "/redfish/v1/systems/{id}"),
            ("ON", "POST", "/redfish/v1/systems/{id}/actions/computersystem.reset"),
            ("OFF", "POST", "/redfish/v1/systems/{id}/actions/computersystem.reset"),
            ("RESET", "POST", "/redfish/v1/systems/{id}/actions/computersystem.reset"),
            ("COLD_BOOT", "POST", "/redfish/v1/systems/{id}/actions/computersystem.reset"),
            ("LIST", "GET", "/redfish/v1/systems"),
            ("RESCAN", "GET", "/redfish/v1/systems"),
            ("UPDATE", "PATCH", "/redfish/v1/systems/{id}"),
        ]
        for act, method, path in server_endpoints:
            rows.append({
                "vendor": "mock_server",
                "device_type": dtype,
                "action_key": act,
                "http_method": method,
                "api_path": path
            })

    # Breakdown before insert
    breakdown: dict[str, dict[str, int]] = {}
    for r in rows:
        breakdown.setdefault(r["vendor"], {})
        breakdown[r["vendor"]][r["device_type"]] = (
            breakdown[r["vendor"]].get(r["device_type"], 0) + 1
        )
    for vendor, dtypes in sorted(breakdown.items()):
        for dtype, cnt in sorted(dtypes.items()):
            logger.info("  %-12s %-20s %4d rows", vendor, dtype, cnt)

    seed(rows)
    verify()


if __name__ == "__main__":
    main()
