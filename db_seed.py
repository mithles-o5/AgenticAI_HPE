"""
Database Seeder — Resource Initialization
===========================================
Populates PostgreSQL with:
- 10 OneViews with 1000 servers each (10,000 servers)
- 1 CoM (Center of Management) with 500 servers

Run this script once to initialize the database:
    python db_seed.py
"""

from __future__ import annotations

import logging
import os
import sys
import uuid as _uuid
from typing import Generator

import psycopg2
from psycopg2 import Error as PsycopgError

# ── Add parent dir to path ────────────────────────────────────────────────────
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, THIS_DIR)

# ── logging ───────────────────────────────────────────────────────────────────
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
    """Clear all existing data from the database."""
    logger.info("[Seed] Clearing existing database tables...")
    
    # Tables in order of dependency (respect foreign keys)
    tables_to_clear = [
        "com_server_tags",
        "com_server_aliases",
        "com_server_protocols",
        "com_servers",
        "coms",
        "server_tags",
        "server_aliases",
        "server_protocols",
        "servers",
        "oneviews",
        "protocols",
        "deployment_types",
        "resource_health",
        "vendors",
    ]
    
    try:
        for table in tables_to_clear:
            db_manager.execute_query(
                f"TRUNCATE TABLE {table} CASCADE",
                fetch_all=False
            )
        logger.info("[Seed] ✓ All tables cleared")
    except Exception as e:
        logger.warning(f"[Seed] Could not clear tables (may be first run): {e}")


# ─────────────────────────────────────────────────────────────────────────────
# Seed Functions
# ─────────────────────────────────────────────────────────────────────────────

def seed_base_data() -> dict:
    """Seed base enumeration data."""
    logger.info("[Seed] Inserting base data...")

    vendors = [("HPE",)]
    deployment_types = [("On-Premises",), ("Cloud",)]
    protocols = [("OneView",), ("COMS",)]
    health_statuses = [("OK",), ("Warning",), ("Critical",), ("Unknown",)]

    db_manager.execute_many(
        "INSERT INTO vendors (name) VALUES (%s) ON CONFLICT DO NOTHING",
        vendors,
    )
    db_manager.execute_many(
        "INSERT INTO deployment_types (name) VALUES (%s) ON CONFLICT DO NOTHING",
        deployment_types,
    )
    db_manager.execute_many(
        "INSERT INTO protocols (name) VALUES (%s) ON CONFLICT DO NOTHING",
        protocols,
    )
    db_manager.execute_many(
        "INSERT INTO resource_health (status) VALUES (%s) ON CONFLICT DO NOTHING",
        health_statuses,
    )

    logger.info("[Seed] Base data inserted")

    # Fetch IDs for use in server creation
    base_data = {}
    for row in db_manager.execute_query("SELECT id, name FROM vendors"):
        base_data[f"vendor_{row['name']}"] = row["id"]
    for row in db_manager.execute_query("SELECT id, name FROM deployment_types"):
        base_data[f"deployment_{row['name']}"] = row["id"]
    for row in db_manager.execute_query("SELECT id, name FROM protocols"):
        base_data[f"protocol_{row['name']}"] = row["id"]
    for row in db_manager.execute_query("SELECT id, status FROM resource_health"):
        base_data[f"health_{row['status']}"] = row["id"]

    return base_data


def create_oneview(ov_num: int, base_data: dict) -> int:
    """Create a OneView and return its database ID."""
    ov_uuid = str(_uuid.uuid4())
    ov_name = f"oneview-{ov_num:02d}"
    ov_ip = f"10.100.{ov_num}.1"
    ov_host = f"oneview-{ov_num:02d}.mgmt.local"

    query = """
        INSERT INTO oneviews (name, uuid, ip_address, management_host, owner, location)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id
    """
    result = db_manager.execute_query(
        query,
        (ov_name, ov_uuid, ov_ip, ov_host, "platform-team", f"DC-{ov_num}"),
        fetch_one=True,
    )
    ov_id = result["id"] if result else None
    logger.info(f"[Seed] Created OneView: {ov_name} (ID: {ov_id})")
    return ov_id


def create_com(base_data: dict) -> int:
    """Create a CoM (Center of Management) and return its database ID."""
    com_uuid = str(_uuid.uuid4())
    com_name = "center-of-management-01"
    com_ip = "10.200.1.1"
    com_host = "com-01.cloud.local"

    query = """
        INSERT INTO coms (name, uuid, ip_address, management_host, owner, location)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id
    """
    result = db_manager.execute_query(
        query,
        (com_name, com_uuid, com_ip, com_host, "cloud-team", "Cloud-Region-1"),
        fetch_one=True,
    )
    com_id = result["id"] if result else None
    logger.info(f"[Seed] Created CoM: {com_name} (ID: {com_id})")
    return com_id


def generate_server_batch(
    start_idx: int,
    count: int,
    base_data: dict,
    parent_id: int,
    parent_type: str,  # "oneview" or "com"
) -> Generator[tuple, None, None]:
    """Generate server data for batch insertion."""
    vendor_id = base_data.get("vendor_HPE")
    deployment_id = (
        base_data.get("deployment_On-Premises")
        if parent_type == "oneview"
        else base_data.get("deployment_Cloud")
    )
    health_id = base_data.get("health_OK")

    for i in range(count):
        server_num = start_idx + i
        server_uuid = str(_uuid.uuid4())
        
        if parent_type == "oneview":
            server_name = f"server-{server_num:05d}"
            ip_addr = f"10.100.{parent_id}.{(server_num % 254) + 1}"
            # Management through OneView appliance, NOT direct iLO
            mgmt_host = f"oneview-{parent_id:02d}.mgmt.local"
            model = "ProLiant DL380 Gen10" if server_num % 2 == 0 else "ProLiant DL360 Gen10"
            location = f"DC-{parent_id}/Row-{(server_num % 10)}/Rack-{(server_num % 42)}"
            enclosure = f"RACK-{(server_num % 10):02d}"
            # Vault path aligned with OneView protocol discovery
            vault_path = f"secret/oneview/datacenter/rack-{server_num:05d}"
            bay = None
        else:  # com
            server_name = f"cloud-server-{server_num:05d}"
            ip_addr = f"10.200.1.{(server_num % 254) + 1}"
            # Management through COMS appliance
            mgmt_host = f"com-01.cloud.local"
            model = "Synergy 480 Gen10"
            location = f"Cloud-Region-1/Zone-{(server_num % 5)}"
            enclosure = f"FRAME-{(server_num % 20):02d}"
            # Vault path aligned with COMS protocol discovery
            vault_path = f"secret/coms/cloud/server-{server_num:05d}"
            bay = (server_num % 20) + 1

        yield (
            server_uuid,
            server_name,
            ip_addr,
            mgmt_host,
            vendor_id,
            deployment_id,
            health_id,
            parent_id,
            model,
            f"SERIAL-{server_num:06d}",
            "OneView 7.4" if parent_type == "oneview" else "COMS API v1.0",
            enclosure,
            bay,
            location,
            f"ASSET-{server_num:06d}",
            "platform-team" if parent_type == "oneview" else "cloud-team",
            "Off",
            vault_path,
            "basic",
            "administrator" if parent_type == "oneview" else "api-user",
            f'W/"{server_num:x}"',
        )


def insert_oneview_servers(oneview_id: int, base_data: dict, count: int = 1000):
    """Insert servers for a specific OneView."""
    query = """
        INSERT INTO servers (
            uuid, name, ip_address, management_host,
            vendor_id, deployment_type_id, health_id, oneview_id,
            model, serial, firmware, enclosure, bay, location,
            asset_tag, owner, power_state, vault_path, auth_type,
            vault_username, etag
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    batch_params = list(
        generate_server_batch(
            start_idx=0, count=count, base_data=base_data, parent_id=oneview_id, parent_type="oneview"
        )
    )

    db_manager.execute_many(query, batch_params)
    logger.info(f"[Seed] Inserted {count} servers for OneView ID {oneview_id}")


def insert_com_servers(com_id: int, base_data: dict, count: int = 500):
    """Insert servers for CoM."""
    query = """
        INSERT INTO com_servers (
            uuid, name, ip_address, management_host,
            vendor_id, deployment_type_id, health_id, com_id,
            model, serial, firmware, enclosure, bay, location,
            asset_tag, owner, power_state, vault_path, auth_type,
            vault_username, etag
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    batch_params = list(
        generate_server_batch(
            start_idx=10000, count=count, base_data=base_data, parent_id=com_id, parent_type="com"
        )
    )

    db_manager.execute_many(query, batch_params)
    logger.info(f"[Seed] Inserted {count} servers for CoM ID {com_id}")


def add_server_protocols(base_data: dict):
    """Associate protocols with servers."""
    oneview_protocol_id = base_data.get("protocol_OneView")
    coms_protocol_id = base_data.get("protocol_COMS")

    # All OneView servers support OneView protocol
    db_manager.execute_query(
        f"""
        INSERT INTO server_protocols (server_id, protocol_id)
        SELECT id, {oneview_protocol_id} FROM servers
        ON CONFLICT DO NOTHING
        """,
        fetch_all=False
    )

    # All CoM servers support COMS protocol
    db_manager.execute_query(
        f"""
        INSERT INTO com_server_protocols (com_server_id, protocol_id)
        SELECT id, {coms_protocol_id} FROM com_servers
        ON CONFLICT DO NOTHING
        """,
        fetch_all=False
    )
    logger.info("[Seed] Associated protocols with servers")


def add_server_aliases(base_data: dict):
    """Add aliases for servers."""
    # Get all servers and add aliases
    servers = db_manager.execute_query("SELECT id, name FROM servers")
    if servers:
        alias_params = [(s["id"], f"{s['name']}-alias") for s in servers]
        db_manager.execute_many(
            "INSERT INTO server_aliases (server_id, alias) VALUES (%s, %s)",
            alias_params[:1000],  # Limit for performance
        )

    com_servers = db_manager.execute_query("SELECT id, name FROM com_servers")
    if com_servers:
        com_alias_params = [(s["id"], f"{s['name']}-alias") for s in com_servers]
        db_manager.execute_many(
            "INSERT INTO com_server_aliases (com_server_id, alias) VALUES (%s, %s)",
            com_alias_params[:500],  # Limit for performance
        )

    logger.info("[Seed] Added aliases for servers")


def add_server_tags(base_data: dict):
    """Add tags for servers."""
    tag_params = [
        ("production",),
        ("tier-1",),
        ("tier-2",),
        ("web-tier",),
        ("db-tier",),
        ("gpu",),
    ]

    servers = db_manager.execute_query("SELECT id FROM servers")
    if servers:
        server_tag_params = []
        for i, s in enumerate(servers[:1000]):  # Tag subset for performance
            tag = tag_params[i % len(tag_params)][0]
            server_tag_params.append((s["id"], tag))
        db_manager.execute_many(
            "INSERT INTO server_tags (server_id, tag) VALUES (%s, %s)",
            server_tag_params,
        )

    com_servers = db_manager.execute_query("SELECT id FROM com_servers")
    if com_servers:
        com_server_tag_params = []
        for i, s in enumerate(com_servers[:500]):
            tag = tag_params[i % len(tag_params)][0]
            com_server_tag_params.append((s["id"], tag))
        db_manager.execute_many(
            "INSERT INTO com_server_tags (com_server_id, tag) VALUES (%s, %s)",
            com_server_tag_params,
        )

    logger.info("[Seed] Added tags for servers")


def main():
    """Main seeding function."""
    logger.info("[Seed] Starting database population...")

    try:
        # Test connection
        if not db_manager.test_connection():
            logger.error("[Seed] Database connection failed")
            sys.exit(1)

        # Clear existing data
        clear_database()

        # Seed base data
        base_data = seed_base_data()

        # Create 10 OneViews with 1000 servers each
        logger.info("[Seed] Creating OneViews...")
        for ov_num in range(1, 11):
            ov_id = create_oneview(ov_num, base_data)
            insert_oneview_servers(ov_id, base_data, count=1000)

        # Create CoM with 500 servers
        logger.info("[Seed] Creating Center of Management...")
        com_id = create_com(base_data)
        insert_com_servers(com_id, base_data, count=500)

        # Add protocols, aliases, and tags
        add_server_protocols(base_data)
        add_server_aliases(base_data)
        add_server_tags(base_data)

        logger.info("[Seed] ✓ Database population complete!")
        logger.info("[Seed] Summary:")
        logger.info("[Seed]   - 10 OneViews")
        logger.info("[Seed]   - 10,000 OneView servers")
        logger.info("[Seed]   - 1 Center of Management")
        logger.info("[Seed]   - 500 CoM servers")

    except PsycopgError as e:
        logger.error(f"[Seed] Database error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"[Seed] Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
