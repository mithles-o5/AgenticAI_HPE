"""
PostgreSQL Database Module
===========================
Manages connections to the resource resolver database.
Provides connection pooling and helper functions.
"""

from __future__ import annotations

import logging
import os
from typing import Optional, Generator

import psycopg2
from psycopg2 import pool, extras
from psycopg2.extensions import connection as Connection

logger = logging.getLogger(__name__)


class DatabaseManager:
    """
    Manages PostgreSQL connections with connection pooling.
    """

    _instance: Optional[DatabaseManager] = None
    _connection_pool: Optional[pool.SimpleConnectionPool] = None

    def __new__(cls) -> DatabaseManager:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(
        self,
        host: str = os.getenv("DB_HOST", "localhost"),
        port: int = int(os.getenv("DB_PORT", "5432")),
        database: str = os.getenv("DB_NAME", "hpe_agentic_ai"),
        user: str = os.getenv("DB_USER", "postgres"),
        password: str = os.getenv("DB_PASSWORD", "Mithles"),
        min_connections: int = 2,
        max_connections: int = 10,
    ) -> None:
        """Initialize the database manager with connection pooling."""
        
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.min_connections = min_connections
        self.max_connections = max_connections

        if self._connection_pool is None:
            try:
                self._connection_pool = pool.SimpleConnectionPool(
                    min_connections,
                    max_connections,
                    host=host,
                    port=port,
                    database=database,
                    user=user,
                    password=password,
                    connect_timeout=5,  # 5 second timeout
                )
                logger.info(
                    f"[DB] Connection pool created: {min_connections}-{max_connections} "
                    f"connections to {user}@{host}:{port}/{database}"
                )
            except psycopg2.Error as e:
                logger.error(f"[DB] Failed to create connection pool: {e}")
                raise

    @property
    def pool(self) -> pool.SimpleConnectionPool:
        """Get the connection pool."""
        if self._connection_pool is None:
            raise RuntimeError("Database manager not initialized")
        return self._connection_pool

    def get_connection(self) -> Connection:
        """Get a connection from the pool."""
        try:
            conn = self.pool.getconn()
            conn.autocommit = False
            logger.debug("[DB] Connection retrieved from pool")
            return conn
        except pool.PoolError as e:
            logger.error(f"[DB] No available connections: {e}")
            raise

    def return_connection(self, conn: Connection) -> None:
        """Return a connection to the pool."""
        if conn:
            try:
                self.pool.putconn(conn)
                logger.debug("[DB] Connection returned to pool")
            except pool.PoolError as e:
                logger.error(f"[DB] Error returning connection: {e}")

    def close_all(self) -> None:
        """Close all connections in the pool."""
        if self._connection_pool:
            self._connection_pool.closeall()
            self._connection_pool = None
            logger.info("[DB] Connection pool closed")

    def execute_query(
        self,
        query: str,
        params: tuple = (),
        fetch_one: bool = False,
        fetch_all: bool = True,
    ) -> Optional[list | tuple]:
        """
        Execute a query and optionally fetch results.
        
        Parameters
        ----------
        query      : SQL query string
        params     : Query parameters
        fetch_one  : Return single row
        fetch_all  : Return all rows
        
        Returns
        -------
        Query results or None
        """
        conn = None
        try:
            conn = self.get_connection()
            cur = conn.cursor(cursor_factory=extras.RealDictCursor)
            cur.execute(query, params)
            
            if fetch_one:
                result = cur.fetchone()
                conn.commit()
                return result
            elif fetch_all:
                result = cur.fetchall()
                conn.commit()
                return result
            else:
                conn.commit()
                return None
                
        except psycopg2.Error as e:
            if conn:
                conn.rollback()
            logger.error(f"[DB] Query error: {e}")
            raise
        finally:
            cur.close() if 'cur' in locals() else None
            if conn:
                self.return_connection(conn)

    def execute_many(self, query: str, params_list: list[tuple]) -> None:
        """
        Execute multiple queries in a transaction.
        
        Parameters
        ----------
        query       : SQL query string with %s placeholders
        params_list : List of parameter tuples
        """
        conn = None
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            for params in params_list:
                cur.execute(query, params)
            conn.commit()
            logger.debug(f"[DB] Executed {len(params_list)} statements")
        except psycopg2.Error as e:
            if conn:
                conn.rollback()
            logger.error(f"[DB] Batch execute error: {e}")
            raise
        finally:
            cur.close() if 'cur' in locals() else None
            if conn:
                self.return_connection(conn)

    def test_connection(self) -> bool:
        """Test database connectivity."""
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            cur.execute("SELECT 1")
            cur.close()
            self.return_connection(conn)
            logger.info("[DB] Connection test successful")
            return True
        except Exception as e:
            logger.error(f"[DB] Connection test failed: {e}")
            return False

    def fetch_protocols_by_credentials(
        self, 
        ip_address: str, 
        vault_path: str, 
        auth_type: str
    ) -> list[str]:
        """
        Fetch supported protocols from the database using IP address and credentials.
        
        Parameters
        ----------
        ip_address  : IP address of the server (e.g. "10.10.1.104")
        vault_path  : Vault path for credentials (e.g. "secret/datacenter/rack-04/ilo")
        auth_type   : Authentication type (e.g. "basic", "token", "certificate")
        
        Returns
        -------
        List of protocol names (e.g. ["ONEVIEW", "COMS"])
        """
        try:
            # Query OneView servers first
            query_oneview = """
                SELECT DISTINCT p.name as protocol_name
                FROM servers s
                LEFT JOIN server_protocols sp ON s.id = sp.server_id
                LEFT JOIN protocols p ON sp.protocol_id = p.id
                WHERE s.ip_address = %s 
                  AND s.vault_path = %s
                  AND s.auth_type = %s
                  AND p.name IS NOT NULL
                ORDER BY p.name
            """
            
            rows = self.execute_query(
                query_oneview,
                params=(ip_address, vault_path, auth_type),
                fetch_all=True
            )
            
            if rows:
                protocols = [row["protocol_name"] for row in rows]
                logger.debug(
                    f"[DB] Fetched {len(protocols)} protocols for {ip_address} "
                    f"(vault: {vault_path[:30]}..., auth: {auth_type}): {protocols}"
                )
                return protocols
            
            # Query CoM servers if not found in OneView
            query_com = """
                SELECT DISTINCT p.name as protocol_name
                FROM com_servers cs
                LEFT JOIN com_server_protocols csp ON cs.id = csp.com_server_id
                LEFT JOIN protocols p ON csp.protocol_id = p.id
                WHERE cs.ip_address = %s 
                  AND cs.vault_path = %s
                  AND cs.auth_type = %s
                  AND p.name IS NOT NULL
                ORDER BY p.name
            """
            
            rows = self.execute_query(
                query_com,
                params=(ip_address, vault_path, auth_type),
                fetch_all=True
            )
            
            if rows:
                protocols = [row["protocol_name"] for row in rows]
                logger.debug(
                    f"[DB] Fetched {len(protocols)} protocols for CoM {ip_address} "
                    f"(vault: {vault_path[:30]}..., auth: {auth_type}): {protocols}"
                )
                return protocols
            
            logger.warning(
                f"[DB] No protocols found for {ip_address} "
                f"with vault_path={vault_path}, auth_type={auth_type}"
            )
            return []
            
        except psycopg2.Error as e:
            logger.error(
                f"[DB] Error fetching protocols for {ip_address}: {e}"
            )
            return []

    def fetch_server_by_ip_and_credentials(
        self,
        ip_address: str,
        vault_path: str,
        auth_type: str
    ) -> Optional[dict]:
        """
        Fetch a complete server record by IP address and credentials.
        
        Parameters
        ----------
        ip_address  : IP address of the server
        vault_path  : Vault path for credentials
        auth_type   : Authentication type
        
        Returns
        -------
        Server record as dictionary or None if not found
        """
        try:
            # Try OneView servers first
            query_oneview = """
                SELECT
                    s.uuid, s.name, s.ip_address, s.management_host,
                    s.model, s.serial, s.firmware, s.enclosure, s.bay,
                    s.location, s.asset_tag, s.owner, s.power_state, s.etag,
                    s.vault_path, s.auth_type, s.vault_username,
                    v.name as vendor_name,
                    dt.name as deployment_type,
                    rh.status as health_status,
                    array_agg(DISTINCT p.name) FILTER (WHERE p.name IS NOT NULL) as protocols,
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
                WHERE s.ip_address = %s 
                  AND s.vault_path = %s
                  AND s.auth_type = %s
                GROUP BY s.id, v.name, dt.name, rh.status
                LIMIT 1
            """
            
            record = self.execute_query(
                query_oneview,
                params=(ip_address, vault_path, auth_type),
                fetch_one=True
            )
            
            if record:
                logger.debug(f"[DB] Found OneView server: {record['name']}")
                return dict(record)
            
            # Try CoM servers
            query_com = """
                SELECT
                    cs.uuid, cs.name, cs.ip_address, cs.management_host,
                    cs.model, cs.serial, cs.firmware, cs.enclosure, cs.bay,
                    cs.location, cs.asset_tag, cs.owner, cs.power_state, cs.etag,
                    cs.vault_path, cs.auth_type, cs.vault_username,
                    v.name as vendor_name,
                    dt.name as deployment_type,
                    rh.status as health_status,
                    array_agg(DISTINCT p.name) FILTER (WHERE p.name IS NOT NULL) as protocols,
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
                WHERE cs.ip_address = %s 
                  AND cs.vault_path = %s
                  AND cs.auth_type = %s
                GROUP BY cs.id, v.name, dt.name, rh.status
                LIMIT 1
            """
            
            record = self.execute_query(
                query_com,
                params=(ip_address, vault_path, auth_type),
                fetch_one=True
            )
            
            if record:
                logger.debug(f"[DB] Found CoM server: {record['name']}")
                return dict(record)
            
            logger.warning(
                f"[DB] No server found for {ip_address} "
                f"with vault_path={vault_path}, auth_type={auth_type}"
            )
            return None
            
        except psycopg2.Error as e:
            logger.error(
                f"[DB] Error fetching server for {ip_address}: {e}"
            )
            return None


# Singleton instance
db_manager = DatabaseManager()
