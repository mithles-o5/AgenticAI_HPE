"""
PostgreSQL Database Module
===========================
Manages connections to the resource resolver database.
Provides connection pooling and helper functions.
"""

from __future__ import annotations

import logging
import os
from typing import Optional

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
        cur = None
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
            if cur:
                cur.close()
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
        cur = None
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
            if cur:
                cur.close()
            if conn:
                self.return_connection(conn)

    def test_connection(self) -> bool:
        """Test database connectivity."""
        conn = None
        cur = None
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            cur.execute("SELECT 1")
            cur.close()
            cur = None
            self.return_connection(conn)
            conn = None
            logger.info("[DB] Connection test successful")
            return True
        except Exception as e:
            logger.error(f"[DB] Connection test failed: {e}")
            return False
        finally:
            if cur:
                cur.close()
            if conn:
                self.return_connection(conn)




# Singleton instance
db_manager = DatabaseManager()
