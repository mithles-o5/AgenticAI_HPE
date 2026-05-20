"""
Database Registry Loader
=========================
Loads ResourceRecords from PostgreSQL instead of hard-coded sample data.
"""

from __future__ import annotations

import logging
import os
import sys
from typing import Optional

# ── path: ensure flat files are importable ────────────────────────────────────
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, THIS_DIR)

from records import (
    Vendor, Protocol, ResourceHealth, ResourceRecord,
    CredentialRef, DeploymentType,
)
from registry import ResourceRegistry
from db import db_manager

logger = logging.getLogger(__name__)


def get_protocols_for_resource(ip_address: str, vault_path: str, auth_type: str) -> list[Protocol]:
    """
    Fetch supported protocols for a resource using IP and credentials.
    
    Parameters
    ----------
    ip_address  : IP address of the server
    vault_path  : Vault path for credentials
    auth_type   : Authentication type
    
    Returns
    -------
    List of Protocol enums
    """
    protocol_names = db_manager.fetch_protocols_by_credentials(ip_address, vault_path, auth_type)
    
    if not protocol_names:
        logger.warning(
            f"[DB Loader] No protocols found for {ip_address}, "
            f"vault_path={vault_path}, auth_type={auth_type}"
        )
        return []
    
    protocols = []
    for name in protocol_names:
        try:
            protocols.append(Protocol(name))
        except ValueError:
            logger.warning(f"[DB Loader] Unknown protocol: {name}")
    
    return protocols


def _parse_deployment_type(db_value: str) -> DeploymentType:
    """
    Convert database deployment type string to enum.
    Handles variations like 'ON_PREMISES', 'on-prem', 'CLOUD', etc.
    """
    if not db_value:
        return DeploymentType.ON_PREM
    
    normalized = db_value.upper().replace("-", "_").replace("_ES", "")
    
    # Map common variations
    if normalized in ("ON_PREM", "ON_PREMISES"):
        return DeploymentType.ON_PREM
    elif normalized in ("CLOUD", "CLOUD_HOSTED"):
        return DeploymentType.CLOUD
    else:
        logger.warning(f"[DB Loader] Unknown deployment type '{db_value}', defaulting to ON_PREM")
        return DeploymentType.ON_PREM


def load_server_from_db(ip_address: str, vault_path: str, auth_type: str) -> Optional[ResourceRecord]:
    """
    Load a single server record from the database using IP and credentials.
    
    Parameters
    ----------
    ip_address  : IP address of the server
    vault_path  : Vault path for credentials
    auth_type   : Authentication type
    
    Returns
    -------
    ResourceRecord if found, None otherwise
    """
    row = db_manager.fetch_server_by_ip_and_credentials(ip_address, vault_path, auth_type)
    
    if not row:
        logger.debug(f"[DB Loader] No server found: {ip_address}")
        return None
    
    try:
        # Determine if it's OneView or CoM based on protocols
        protocols = [Protocol(p) for p in (row.get("protocols") or []) if p]
        
        record = ResourceRecord(
            name=row["name"],
            uuid=row["uuid"],
            aliases=[a for a in (row.get("aliases") or []) if a],
            ip_address=row["ip_address"] or "",
            management_host=row["management_host"] or "",
            vendor=Vendor[row.get("vendor_name", "HPE").upper()],
            deployment_type=_parse_deployment_type(row.get("deployment_type", "ON_PREM")),
            supported_protocols=protocols,
            model=row["model"] or "",
            serial=row["serial"] or "",
            firmware=row["firmware"] or "",
            enclosure=row["enclosure"] or "",
            bay=row["bay"],
            location=row["location"],
            asset_tag=row["asset_tag"],
            owner=row["owner"],
            tags=[t for t in (row.get("tags") or []) if t],
            power_state=row["power_state"] or "Unknown",
            health=ResourceHealth[row.get("health_status", "UNKNOWN").upper().replace(" ", "_")],
            etag=row["etag"],
            credential_ref=CredentialRef(
                vault_path=row["vault_path"] or "secret/default",
                auth_type=row["auth_type"] or "basic",
                username=row["vault_username"],
            ) if row["vault_path"] else None,
        )
        
        logger.info(
            f"[DB Loader] Loaded server: {record.name} "
            f"[{record.uuid[:8]}…] from {ip_address}"
        )
        return record
        
    except Exception as e:
        logger.error(
            f"[DB Loader] Error converting row to ResourceRecord: {e}"
        )
        return None


def load_registry_from_db() -> ResourceRegistry:
    """
    Load all servers from PostgreSQL into a ResourceRegistry.
    Combines OneView servers and CoM servers.
    """
    registry = ResourceRegistry()

    # Test connection
    if not db_manager.test_connection():
        logger.error("[DB Loader] Database connection failed, falling back to empty registry")
        return registry

    try:
        # Load OneView servers
        logger.info("[DB Loader] Loading OneView servers...")
        _load_oneview_servers(registry)

        # Load CoM servers
        logger.info("[DB Loader] Loading CoM servers...")
        _load_com_servers(registry)

        logger.info(f"[DB Loader] ✓ Loaded {len(registry)} records from database")
        return registry

    except Exception as e:
        logger.error(f"[DB Loader] Error loading from database: {e}")
        logger.warning("[DB Loader] Returning empty registry")
        return registry


def _load_oneview_servers(registry: ResourceRegistry) -> None:
    """Load all OneView servers from database."""
    query = """
        SELECT
            s.uuid, s.name, s.ip_address, s.management_host,
            s.model, s.serial, s.firmware, s.enclosure, s.bay,
            s.location, s.asset_tag, s.owner, s.power_state, s.etag,
            s.vault_path, s.auth_type, s.vault_username,
            v.name as vendor_name,
            dt.name as deployment_type,
            rh.status as health_status,
            array_agg(DISTINCT p.name) as protocols,
            array_agg(DISTINCT sa.alias) FILTER (WHERE sa.alias IS NOT NULL) as aliases,
            array_agg(DISTINCT st.tag) FILTER (WHERE st.tag IS NOT NULL) as tags
        FROM servers s
        LEFT JOIN vendors v ON s.vendor_id = v.id
        LEFT JOIN deployment_types dt ON s.deployment_type_id = dt.id
        LEFT JOIN resource_health rh ON s.health_id = rh.id
        LEFT JOIN server_protocols sp ON s.id = sp.server_id
        LEFT JOIN protocols p ON sp.protocol_id = p.id
        LEFT JOIN server_aliases sa ON s.id = sa.server_id
        LEFT JOIN server_tags st ON s.id = st.server_id
        GROUP BY s.id, v.name, dt.name, rh.status
        ORDER BY s.name
        LIMIT 10000
    """

    rows = db_manager.execute_query(query, fetch_all=True)
    if not rows:
        logger.warning("[DB Loader] No OneView servers found")
        return

    for row in rows:
        protocols = [Protocol(p) for p in (row.get("protocols") or []) if p]
        if not protocols:
            protocols = [Protocol.ONEVIEW]

        record = ResourceRecord(
            name=row["name"],
            uuid=row["uuid"],
            aliases=[a for a in (row.get("aliases") or []) if a],
            ip_address=row["ip_address"] or "",
            management_host=row["management_host"] or "",
            vendor=Vendor[row.get("vendor_name", "HPE").upper()],
            deployment_type=_parse_deployment_type(row.get("deployment_type", "ON_PREM")),
            supported_protocols=protocols,
            model=row["model"] or "",
            serial=row["serial"] or "",
            firmware=row["firmware"] or "",
            enclosure=row["enclosure"] or "",
            bay=row["bay"],
            location=row["location"],
            asset_tag=row["asset_tag"],
            owner=row["owner"],
            tags=[t for t in (row.get("tags") or []) if t],
            power_state=row["power_state"] or "Unknown",
            health=ResourceHealth[row.get("health_status", "UNKNOWN").upper().replace(" ", "_")],
            etag=row["etag"],
            credential_ref=CredentialRef(
                vault_path=row["vault_path"] or "secret/default",
                auth_type=row["auth_type"] or "basic",
                username=row["vault_username"],
            ) if row["vault_path"] else None,
        )
        registry.register(record)

    logger.info(f"[DB Loader] Loaded {len(rows)} OneView servers")


def _load_com_servers(registry: ResourceRegistry) -> None:
    """Load all CoM servers from database."""
    query = """
        SELECT
            cs.uuid, cs.name, cs.ip_address, cs.management_host,
            cs.model, cs.serial, cs.firmware, cs.enclosure, cs.bay,
            cs.location, cs.asset_tag, cs.owner, cs.power_state, cs.etag,
            cs.vault_path, cs.auth_type, cs.vault_username,
            v.name as vendor_name,
            dt.name as deployment_type,
            rh.status as health_status,
            array_agg(DISTINCT p.name) as protocols,
            array_agg(DISTINCT csa.alias) FILTER (WHERE csa.alias IS NOT NULL) as aliases,
            array_agg(DISTINCT cst.tag) FILTER (WHERE cst.tag IS NOT NULL) as tags
        FROM com_servers cs
        LEFT JOIN vendors v ON cs.vendor_id = v.id
        LEFT JOIN deployment_types dt ON cs.deployment_type_id = dt.id
        LEFT JOIN resource_health rh ON cs.health_id = rh.id
        LEFT JOIN com_server_protocols csp ON cs.id = csp.com_server_id
        LEFT JOIN protocols p ON csp.protocol_id = p.id
        LEFT JOIN com_server_aliases csa ON cs.id = csa.com_server_id
        LEFT JOIN com_server_tags cst ON cs.id = cst.com_server_id
        GROUP BY cs.id, v.name, dt.name, rh.status
        ORDER BY cs.name
        LIMIT 500
    """

    rows = db_manager.execute_query(query, fetch_all=True)
    if not rows:
        logger.warning("[DB Loader] No CoM servers found")
        return

    for row in rows:
        protocols = [Protocol(p) for p in (row.get("protocols") or []) if p]
        if not protocols:
            protocols = [Protocol.COMS]

        record = ResourceRecord(
            name=row["name"],
            uuid=row["uuid"],
            aliases=[a for a in (row.get("aliases") or []) if a],
            ip_address=row["ip_address"] or "",
            management_host=row["management_host"] or "",
            vendor=Vendor[row.get("vendor_name", "HPE").upper()],
            deployment_type=_parse_deployment_type(row.get("deployment_type", "CLOUD")),
            supported_protocols=protocols,
            model=row["model"] or "",
            serial=row["serial"] or "",
            firmware=row["firmware"] or "",
            enclosure=row["enclosure"] or "",
            bay=row["bay"],
            location=row["location"],
            asset_tag=row["asset_tag"],
            owner=row["owner"],
            tags=[t for t in (row.get("tags") or []) if t],
            power_state=row["power_state"] or "Unknown",
            health=ResourceHealth[row.get("health_status", "UNKNOWN").upper().replace(" ", "_")],
            etag=row["etag"],
            credential_ref=CredentialRef(
                vault_path=row["vault_path"] or "secret/default",
                auth_type=row["auth_type"] or "basic",
                username=row["vault_username"],
            ) if row["vault_path"] else None,
        )
        registry.register(record)

    logger.info(f"[DB Loader] Loaded {len(rows)} CoM servers")
