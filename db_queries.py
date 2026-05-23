"""
Database Query Utilities
========================
Production-grade query utilities for common database operations.

Usage:
    from db_queries import get_server_by_ip, get_servers_by_location, etc.
"""

from __future__ import annotations

import logging
from typing import Optional

from db import db_manager

logger = logging.getLogger(__name__)


class ServerQueries:
    """High-level queries for server management."""

    @staticmethod
    def get_by_uuid(uuid: str) -> Optional[dict]:
        """Get server by UUID."""
        query = """
            SELECT 
                s.id, s.uuid, s.name, s.ip_address, s.management_host,
                s.model, s.serial, s.firmware, s.location, s.owner,
                s.power_state, s.health_id, s.vault_path, s.auth_type,
                v.name as vendor_name,
                string_agg(DISTINCT p.name, ', ') as protocols,
                string_agg(DISTINCT sa.alias, ', ') as aliases,
                string_agg(DISTINCT st.tag, ', ') as tags
            FROM servers s
            LEFT JOIN vendors v ON s.vendor_id = v.id
            LEFT JOIN server_protocols sp ON s.id = sp.server_id
            LEFT JOIN protocols p ON sp.protocol_id = p.id
            LEFT JOIN server_aliases sa ON s.id = sa.server_id
            LEFT JOIN server_tags st ON s.id = st.server_id
            WHERE s.uuid = %s
            GROUP BY s.id, v.name
        """
        return db_manager.execute_query(query, (uuid,), fetch_one=True)

    @staticmethod
    def get_by_ip(ip_address: str) -> Optional[dict]:
        """Get server by IP address."""
        query = """
            SELECT 
                s.id, s.uuid, s.name, s.ip_address, s.management_host,
                s.model, s.serial, s.firmware, s.location, s.owner,
                s.power_state, s.vault_path, s.auth_type,
                v.name as vendor_name,
                string_agg(DISTINCT p.name, ', ') as protocols
            FROM servers s
            LEFT JOIN vendors v ON s.vendor_id = v.id
            LEFT JOIN server_protocols sp ON s.id = sp.server_id
            LEFT JOIN protocols p ON sp.protocol_id = p.id
            WHERE s.ip_address = %s
            GROUP BY s.id, v.name
            LIMIT 1
        """
        return db_manager.execute_query(query, (ip_address,), fetch_one=True)

    @staticmethod
    def get_by_name(name: str) -> Optional[dict]:
        """Get server by name (partial match)."""
        query = """
            SELECT 
                s.id, s.uuid, s.name, s.ip_address, s.management_host,
                s.model, s.location, s.power_state,
                v.name as vendor_name
            FROM servers s
            LEFT JOIN vendors v ON s.vendor_id = v.id
            WHERE s.name ILIKE %s
            ORDER BY s.name
            LIMIT 10
        """
        return db_manager.execute_query(query, (f"%{name}%",), fetch_all=True)

    @staticmethod
    def get_by_alias(alias: str) -> Optional[dict]:
        """Get server by alias with all details."""
        query = """
            SELECT 
                s.id, s.uuid, s.name, s.ip_address, s.management_host,
                s.model, s.serial, s.firmware, s.location, s.owner,
                s.power_state, s.health_id, s.vault_path, s.auth_type,
                v.name as vendor_name,
                string_agg(DISTINCT p.name, ', ') as protocols,
                string_agg(DISTINCT sa.alias, ', ') as aliases,
                string_agg(DISTINCT st.tag, ', ') as tags
            FROM servers s
            LEFT JOIN vendors v ON s.vendor_id = v.id
            LEFT JOIN server_protocols sp ON s.id = sp.server_id
            LEFT JOIN protocols p ON sp.protocol_id = p.id
            LEFT JOIN server_aliases sa ON s.id = sa.server_id
            LEFT JOIN server_tags st ON s.id = st.server_id
            WHERE sa.alias ILIKE %s
            GROUP BY s.id, v.name
            LIMIT 1
        """
        return db_manager.execute_query(query, (alias,), fetch_one=True)

    @staticmethod
    def get_by_vault_path_and_auth(vault_path: str, auth_type: str) -> list[dict]:
        """Get servers by vault path and auth type."""
        query = """
            SELECT 
                s.id, s.uuid, s.name, s.ip_address,
                s.vault_path, s.auth_type, s.vault_username,
                v.name as vendor_name,
                string_agg(DISTINCT p.name, ', ') as protocols
            FROM servers s
            LEFT JOIN vendors v ON s.vendor_id = v.id
            LEFT JOIN server_protocols sp ON s.id = sp.server_id
            LEFT JOIN protocols p ON sp.protocol_id = p.id
            WHERE s.vault_path = %s AND s.auth_type = %s
            GROUP BY s.id, v.name
            ORDER BY s.name
        """
        return db_manager.execute_query(query, (vault_path, auth_type), fetch_all=True) or []

    @staticmethod
    def get_by_location(location: str) -> list[dict]:
        """Get servers by location (partial match)."""
        query = """
            SELECT 
                s.id, s.name, s.ip_address, s.location,
                s.power_state, s.model,
                v.name as vendor_name
            FROM servers s
            LEFT JOIN vendors v ON s.vendor_id = v.id
            WHERE s.location ILIKE %s
            ORDER BY s.name
        """
        return db_manager.execute_query(query, (f"%{location}%",), fetch_all=True) or []

    @staticmethod
    def get_by_tag(tag: str) -> list[dict]:
        """Get servers by tag."""
        query = """
            SELECT DISTINCT 
                s.id, s.uuid, s.name, s.ip_address, s.location,
                s.power_state, s.model,
                v.name as vendor_name
            FROM servers s
            LEFT JOIN vendors v ON s.vendor_id = v.id
            JOIN server_tags st ON s.id = st.server_id
            WHERE st.tag ILIKE %s
            ORDER BY s.name
        """
        return db_manager.execute_query(query, (tag,), fetch_all=True) or []

    @staticmethod
    def get_by_owner(owner: str) -> list[dict]:
        """Get servers by owner."""
        query = """
            SELECT 
                s.id, s.name, s.ip_address, s.location,
                s.power_state, s.model, s.owner,
                COUNT(DISTINCT s.id) as count
            FROM servers s
            WHERE s.owner ILIKE %s
            GROUP BY s.id
            ORDER BY s.name
        """
        return db_manager.execute_query(query, (owner,), fetch_all=True) or []

    @staticmethod
    def get_by_model(model: str) -> list[dict]:
        """Get servers by model."""
        query = """
            SELECT 
                s.id, s.name, s.ip_address, s.model, s.location,
                v.name as vendor_name,
                COUNT(*) OVER(PARTITION BY s.model) as model_count
            FROM servers s
            LEFT JOIN vendors v ON s.vendor_id = v.id
            WHERE s.model ILIKE %s
            ORDER BY s.location, s.name
        """
        return db_manager.execute_query(query, (f"%{model}%",), fetch_all=True) or []

    @staticmethod
    def get_by_power_state(power_state: str) -> list[dict]:
        """Get servers by power state."""
        query = """
            SELECT 
                s.id, s.name, s.ip_address, s.power_state,
                s.location, s.owner,
                v.name as vendor_name
            FROM servers s
            LEFT JOIN vendors v ON s.vendor_id = v.id
            WHERE s.power_state = %s
            ORDER BY s.location, s.name
        """
        return db_manager.execute_query(query, (power_state,), fetch_all=True) or []

    @staticmethod
    def get_by_protocol(protocol_name: str) -> list[dict]:
        """Get servers supporting a specific protocol."""
        query = """
            SELECT DISTINCT 
                s.id, s.uuid, s.name, s.ip_address, s.location,
                v.name as vendor_name,
                string_agg(DISTINCT p.name, ', ') as protocols
            FROM servers s
            LEFT JOIN vendors v ON s.vendor_id = v.id
            JOIN server_protocols sp ON s.id = sp.server_id
            JOIN protocols p ON sp.protocol_id = p.id
            WHERE p.name ILIKE %s
            GROUP BY s.id, v.name
            ORDER BY s.name
        """
        return db_manager.execute_query(query, (protocol_name,), fetch_all=True) or []

    @staticmethod
    def list_all(limit: int = 1000, offset: int = 0) -> list[dict]:
        """List all servers with pagination."""
        query = """
            SELECT 
                s.id, s.uuid, s.name, s.ip_address, s.model,
                s.location, s.power_state, s.owner,
                v.name as vendor_name,
                string_agg(DISTINCT p.name, ', ') as protocols
            FROM servers s
            LEFT JOIN vendors v ON s.vendor_id = v.id
            LEFT JOIN server_protocols sp ON s.id = sp.server_id
            LEFT JOIN protocols p ON sp.protocol_id = p.id
            GROUP BY s.id, v.name
            ORDER BY s.name
            LIMIT %s OFFSET %s
        """
        return db_manager.execute_query(query, (limit, offset), fetch_all=True) or []

    @staticmethod
    def count_total() -> int:
        """Count total servers."""
        result = db_manager.execute_query(
            "SELECT COUNT(*) as count FROM servers",
            fetch_one=True
        )
        return result["count"] if result else 0

    @staticmethod
    def fuzzy_search(query: str, limit: int = 10) -> list[dict]:
        """
        Fuzzy search across name, model, serial, location, owner, tags.
        Returns servers ranked by relevance.
        """
        search_term = f"%{query}%"
        
        query_sql = """
            SELECT 
                s.id, s.uuid, s.name, s.ip_address, s.management_host,
                s.model, s.serial, s.firmware, s.location, s.owner,
                s.power_state, s.health_id, s.vault_path, s.auth_type,
                v.name as vendor_name,
                string_agg(DISTINCT p.name, ', ') as protocols,
                string_agg(DISTINCT sa.alias, ', ') as aliases,
                string_agg(DISTINCT st.tag, ', ') as tags,
                -- Relevance scoring
                CASE 
                    WHEN s.name ILIKE %s THEN 3
                    WHEN s.serial ILIKE %s THEN 2
                    WHEN s.model ILIKE %s OR s.location ILIKE %s THEN 1
                    WHEN string_agg(DISTINCT st.tag, ', ') ILIKE %s THEN 0.5
                    ELSE 0
                END as relevance_score
            FROM servers s
            LEFT JOIN vendors v ON s.vendor_id = v.id
            LEFT JOIN server_protocols sp ON s.id = sp.server_id
            LEFT JOIN protocols p ON sp.protocol_id = p.id
            LEFT JOIN server_aliases sa ON s.id = sa.server_id
            LEFT JOIN server_tags st ON s.id = st.server_id
            WHERE s.name ILIKE %s 
                OR s.serial ILIKE %s 
                OR s.model ILIKE %s 
                OR s.location ILIKE %s 
                OR s.owner ILIKE %s
                OR string_agg(DISTINCT sa.alias, ', ') ILIKE %s
                OR string_agg(DISTINCT st.tag, ', ') ILIKE %s
            GROUP BY s.id, v.name
            ORDER BY relevance_score DESC, s.name ASC
            LIMIT %s
        """
        
        params = (
            search_term, search_term, search_term, search_term, search_term,  # relevance scores
            search_term, search_term, search_term, search_term, search_term,   # WHERE clause
            search_term, search_term, limit
        )
        
        return db_manager.execute_query(query_sql, params, fetch_all=True) or []


class StatisticsQueries:
    """High-level queries for statistics and reporting."""

    @staticmethod
    def servers_by_location():
        """Get server count by location."""
        query = """
            SELECT 
                SUBSTRING(location, 1, POSITION('/' IN location) - 1) as datacenter,
                COUNT(*) as server_count,
                STRING_AGG(DISTINCT owner, ', ') as owners
            FROM servers
            GROUP BY SUBSTRING(location, 1, POSITION('/' IN location) - 1)
            ORDER BY server_count DESC
        """
        return db_manager.execute_query(query, fetch_all=True)

    @staticmethod
    def servers_by_health():
        """Get server count by health status."""
        query = """
            SELECT 
                rh.status as health_status,
                COUNT(s.id) as server_count,
                STRING_AGG(DISTINCT s.name, ', ') FILTER(LIMIT 5) as example_servers
            FROM servers s
            JOIN resource_health rh ON s.health_id = rh.id
            GROUP BY rh.status
            ORDER BY server_count DESC
        """
        return db_manager.execute_query(query, fetch_all=True)

    @staticmethod
    def servers_by_power_state():
        """Get server count by power state."""
        query = """
            SELECT 
                power_state,
                COUNT(*) as count
            FROM servers
            GROUP BY power_state
            ORDER BY count DESC
        """
        return db_manager.execute_query(query, fetch_all=True)

    @staticmethod
    def servers_per_oneview():
        """Get server count per OneView."""
        query = """
            SELECT 
                ov.name,
                COUNT(s.id) as server_count,
                ov.ip_address,
                ov.owner,
                ov.location
            FROM oneviews ov
            LEFT JOIN servers s ON ov.id = s.oneview_id
            GROUP BY ov.id
            ORDER BY server_count DESC
        """
        return db_manager.execute_query(query, fetch_all=True)

    @staticmethod
    def protocols_distribution():
        """Get protocol usage statistics."""
        query = """
            SELECT 
                p.name as protocol,
                COUNT(DISTINCT sp.server_id) as server_count,
                ROUND(100.0 * COUNT(DISTINCT sp.server_id) / 
                    (SELECT COUNT(*) FROM servers), 2) as percentage
            FROM protocols p
            LEFT JOIN server_protocols sp ON p.id = sp.protocol_id
            GROUP BY p.name
            ORDER BY server_count DESC
        """
        return db_manager.execute_query(query, fetch_all=True)

    @staticmethod
    def servers_by_owner():
        """Get server count by owner/team."""
        query = """
            SELECT 
                owner,
                COUNT(*) as server_count,
                STRING_AGG(DISTINCT location, ', ') as locations,
                STRING_AGG(DISTINCT model, ', ') FILTER(LIMIT 3) as models
            FROM servers
            WHERE owner IS NOT NULL
            GROUP BY owner
            ORDER BY server_count DESC
        """
        return db_manager.execute_query(query, fetch_all=True)


class ProtocolQueries:
    """Queries related to protocols and capabilities."""

    @staticmethod
    def get_server_protocols(server_uuid: str) -> list[str]:
        """Get protocols supported by a server."""
        query = """
            SELECT DISTINCT p.name
            FROM servers s
            JOIN server_protocols sp ON s.id = sp.server_id
            JOIN protocols p ON sp.protocol_id = p.id
            WHERE s.uuid = %s
            ORDER BY p.name
        """
        rows = db_manager.execute_query(query, (server_uuid,), fetch_all=True)
        return [row["name"] for row in (rows or [])]

    @staticmethod
    def get_all_protocols() -> list[str]:
        """Get all available protocols."""
        query = "SELECT DISTINCT name FROM protocols ORDER BY name"
        rows = db_manager.execute_query(query, fetch_all=True)
        return [row["name"] for row in (rows or [])]


# Convenience aliases
def get_server_by_uuid(uuid: str) -> Optional[dict]:
    """Get server by UUID."""
    return ServerQueries.get_by_uuid(uuid)


def get_server_by_ip(ip: str) -> Optional[dict]:
    """Get server by IP address."""
    return ServerQueries.get_by_ip(ip)


def get_server_by_name(name: str) -> list[dict]:
    """Get servers by name (partial match)."""
    return ServerQueries.get_by_name(name)


def get_server_by_alias(alias: str) -> Optional[dict]:
    """Get server by alias."""
    return ServerQueries.get_by_alias(alias)


def get_servers_by_location(location: str) -> list[dict]:
    """Get servers by location."""
    return ServerQueries.get_by_location(location)


def get_servers_by_tag(tag: str) -> list[dict]:
    """Get servers by tag."""
    return ServerQueries.get_by_tag(tag)


def get_servers_by_protocol(protocol: str) -> list[dict]:
    """Get servers by protocol."""
    return ServerQueries.get_by_protocol(protocol)


def get_statistics() -> dict:
    """Get all statistics."""
    return {
        "servers_by_location": StatisticsQueries.servers_by_location(),
        "servers_by_health": StatisticsQueries.servers_by_health(),
        "servers_by_power": StatisticsQueries.servers_by_power_state(),
        "servers_per_oneview": StatisticsQueries.servers_per_oneview(),
        "protocols": StatisticsQueries.protocols_distribution(),
        "by_owner": StatisticsQueries.servers_by_owner(),
    }
