"""
Database Seeder — Current Schema
=================================
Populates PostgreSQL with the current device registry schema:
- devices
- routing_audit
- poll_history
"""

from __future__ import annotations

import logging
import os
import sys
import uuid as _uuid
from typing import Generator

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, THIS_DIR)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

from db import db_manager


# ─────────────────────────────────────────────────────────────────────────────
# Clear Existing Data
# ─────────────────────────────────────────────────────────────────────────────

def clear_database():
    """Clear all existing data from the current schema."""
    logger.info("[Seed] Clearing existing database tables...")

    tables_to_clear = [
        "poll_history",
        "routing_audit",
        "devices",
    ]

    try:
        for table in tables_to_clear:
            db_manager.execute_query(
                f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE",
                fetch_all=False,
            )
        logger.info("[Seed] ✓ All tables cleared")
    except Exception as e:
        logger.warning(f"[Seed] Could not clear tables (may be first run): {e}")


# ─────────────────────────────────────────────────────────────────────────────
# Source-system seed helpers
# ─────────────────────────────────────────────────────────────────────────────

def create_oneview(ov_num: int) -> int:
    """Return a configured OneView source number for sample inventory."""
    ov_host = f"oneview-{ov_num:02d}.mgmt.local"
    logger.info(f"[Seed] Configured OneView source: {ov_host}")
    return ov_num


def create_coms_source() -> int:
    """Return a configured COMS source marker for sample inventory."""
    coms_host = "coms-01.cloud.local"
    logger.info(f"[Seed] Configured COMS source: {coms_host}")
    return 1


def get_enterprise_name(device_type: str, index: int, parent_type: str) -> tuple[str, str]:
    """Generate a unique, realistic enterprise infrastructure name."""
    domain = "datacenter.local" if parent_type == "oneview" else "cloud.local"
    t = (device_type or "server").lower()
    
    if t == "server":
        rack = (index % 50) + 1
        node = (index % 10) + 1
        name = f"rack{rack}-compute-{node}-{index}"
    elif t == "switch":
        sw_type = "leaf" if index % 2 == 0 else "agg"
        num = (index % 20) + 1
        name = f"{sw_type}-sw{num:02d}-{index}"
    elif t == "router":
        r_type = "edge" if index % 2 == 0 else "wan"
        num = (index % 10) + 1
        name = f"{r_type}-r{num:02d}-{index}"
    elif t == "firewall":
        fw_type = "west" if index % 2 == 0 else "east"
        num = (index % 5) + 1
        name = f"fw-{fw_type}-{num:02d}-{index}"
    elif t == "storage":
        stg_type = "array" if index % 2 == 0 else "nas"
        name = f"stg-{stg_type}-{index}"
    else:
        name = f"infra-node-{index}"
        
    return name, f"{name}.{domain}"


def generate_device_batch(
    start_idx: int,
    count: int,
    parent_id: int,
    parent_type: str,
) -> Generator[tuple, None, None]:
    """Generate device data for batch insertion."""
    types = ["server", "switch", "router", "firewall", "storage"]
    for i in range(count):
        device_num = start_idx + i
        device_uuid = str(_uuid.uuid4())
        device_type = types[device_num % len(types)]
        
        serial_number, fqdn = get_enterprise_name(device_type, device_num, parent_type)

        if parent_type == "oneview":
            management_source = "oneview"
            source_host = f"oneview-{parent_id:02d}.mgmt.local"
            ip_addr = f"10.100.{parent_id}.{(device_num % 254) + 1}"
        else:
            management_source = "coms"
            source_host = "coms-01.cloud.local"
            ip_addr = f"10.200.1.{(device_num % 254) + 1}"

        yield (
            serial_number,
            ip_addr,
            fqdn,
            management_source,
            source_host,
            device_uuid,
            device_type,
        )


def insert_oneview_devices(oneview_id: int, count: int = 1000, start_idx: int = 0):
    """Insert OneView-managed devices."""
    query = """
        INSERT INTO devices (
            serial_number, ip_address, fqdn,
            management_source, source_host, source_device_id,
            device_type, last_seen, created_at, updated_at
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, NOW(), NOW(), NOW())
    """

    batch_params = list(
        generate_device_batch(
            start_idx=start_idx,
            count=count,
            parent_id=oneview_id,
            parent_type="oneview",
        )
    )

    db_manager.execute_many(query, batch_params)
    logger.info(
        f"[Seed] Inserted {count} OneView-managed devices for source ID {oneview_id}"
    )


def insert_coms_devices(coms_id: int, count: int = 500):
    """Insert COMS-managed devices."""
    query = """
        INSERT INTO devices (
            serial_number, ip_address, fqdn,
            management_source, source_host, source_device_id,
            device_type, last_seen, created_at, updated_at
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, NOW(), NOW(), NOW())
    """

    batch_params = list(
        generate_device_batch(
            start_idx=10000,
            count=count,
            parent_id=coms_id,
            parent_type="coms",
        )
    )

    db_manager.execute_many(query, batch_params)
    logger.info(f"[Seed] Inserted {count} COMS-managed devices for source ID {coms_id}")


# ─────────────────────────────────────────────────────────────────────────────
# Additional current-schema seed helpers
# ─────────────────────────────────────────────────────────────────────────────

def seed_current_schema(seed_oneview_count: int = 1000, seed_com_count: int = 500) -> None:
    """Populate the current schema with sample device rows."""
    clear_database()
    oneview_id = create_oneview(1)
    insert_oneview_devices(oneview_id, count=seed_oneview_count, start_idx=0)
    coms_id = create_coms_source()
    insert_coms_devices(coms_id, count=seed_com_count)

    # Insert explicit testing devices matching exact enterprise naming guidelines
    testing_devices = [
        # OneView devices (management_source='oneview', source_host='oneview-01.mgmt.local')
        ("dc1-a7", "10.100.1.10", "dc1-a7.datacenter.local", "oneview", "oneview-01.mgmt.local", "ov-uuid-dc1a7", "server"),
        ("compute-22", "10.100.1.11", "compute-22.datacenter.local", "oneview", "oneview-01.mgmt.local", "ov-uuid-c22", "server"),
        ("rack42-n3", "10.100.1.20", "rack42-n3.datacenter.local", "oneview", "oneview-01.mgmt.local", "ov-uuid-rack42n3", "server"),
        ("edge-r1", "10.100.1.12", "edge-r1.datacenter.local", "oneview", "oneview-01.mgmt.local", "ov-uuid-edger1", "router"),
        ("wan-r2", "10.100.1.21", "wan-r2.datacenter.local", "oneview", "oneview-01.mgmt.local", "ov-uuid-wanr2", "router"),
        ("core-sw01", "10.100.1.13", "core-sw01.datacenter.local", "oneview", "oneview-01.mgmt.local", "ov-uuid-coresw01", "switch"),
        ("leaf-sw12", "10.100.1.22", "leaf-sw12.datacenter.local", "oneview", "oneview-01.mgmt.local", "ov-uuid-leafsw12", "switch"),
        ("fw-core-01", "10.100.1.14", "fw-core-01.datacenter.local", "oneview", "oneview-01.mgmt.local", "ov-uuid-fc01", "firewall"),
        ("fw-edge-02", "10.100.1.23", "fw-edge-02.datacenter.local", "oneview", "oneview-01.mgmt.local", "ov-uuid-fwedge02", "firewall"),

        # COMS devices (management_source='coms', source_host='coms-01.cloud.local')
        ("prod-x1", "10.200.1.13", "prod-x1.cloud.local", "coms", "coms-01.cloud.local", "coms-uuid-prodx1", "server"),
        ("core-r3", "10.200.1.20", "core-r3.cloud.local", "coms", "coms-01.cloud.local", "coms-uuid-corer3", "router"),
        ("agg-sw05", "10.200.1.21", "agg-sw05.cloud.local", "coms", "coms-01.cloud.local", "coms-uuid-aggsw05", "switch"),
        ("fw-west-01", "10.200.1.12", "fw-west-01.cloud.local", "coms", "coms-01.cloud.local", "coms-uuid-fwwest01", "firewall"),
        ("stg-array-02", "10.200.1.11", "stg-array-02.cloud.local", "coms", "coms-01.cloud.local", "coms-uuid-stgarray02", "storage"),
        ("nas-prod-01", "10.200.1.10", "nas-prod-01.cloud.local", "coms", "coms-01.cloud.local", "coms-uuid-np01", "storage"),
        ("backup-san-01", "10.200.1.22", "backup-san-01.cloud.local", "coms", "coms-01.cloud.local", "coms-uuid-backupsan01", "storage"),
    ]

    db_manager.execute_many(
        """
        INSERT INTO devices (
            serial_number, ip_address, fqdn,
            management_source, source_host, source_device_id,
            device_type, last_seen, created_at, updated_at
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, NOW(), NOW(), NOW())
        ON CONFLICT (serial_number) DO NOTHING
        """,
        testing_devices,
    )




# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def main():
    """Main seeding function."""
    logger.info("[Seed] Starting database population for the current schema...")

    try:
        if not db_manager.test_connection():
            logger.error("[Seed] Database connection failed")
            sys.exit(1)

        seed_current_schema()

        logger.info("[Seed] ✓ Database population complete!")
        logger.info("[Seed] Summary:")
        logger.info("[Seed]   - Devices: 1,516 sample rows")
        logger.info("[Seed]   - routing_audit: populated by runtime resolver only")
        logger.info("[Seed]   - poll_history:  populated by runtime polling engine only")

    except Exception as e:
        logger.error(f"[Seed] Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
