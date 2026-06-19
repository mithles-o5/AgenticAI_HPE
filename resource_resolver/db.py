"""
PostgreSQL Database Module
===========================
Manages connections to the resource resolver database.
Provides connection pooling and helper functions.

IMPORTANT: The singleton ``db_manager`` at the bottom of this module will
NEVER raise on import — even if PostgreSQL is unavailable.  Callers that
need the DB will receive ``None`` / empty lists gracefully so that the MCP
server can start and operate in SQLite-only mode.
"""

from __future__ import annotations

import logging
import os
from typing import Optional

try:
    from dotenv import load_dotenv
    # Load .env from the same directory as this file
    _env_path = os.path.join(os.path.dirname(__file__), ".env")
    load_dotenv(dotenv_path=_env_path)
except ImportError:
    pass

logger = logging.getLogger(__name__)

# ── Optional psycopg2 import ──────────────────────────────────────────────────
try:
    import psycopg2
    from psycopg2 import pool, extras
    from psycopg2.extensions import connection as Connection
    _PSYCOPG2_AVAILABLE = True
except ImportError:
    _PSYCOPG2_AVAILABLE = False
    logger.warning("[DB] psycopg2 not installed — PostgreSQL unavailable; running in SQLite-only mode")


class DatabaseManager:
    """
    Manages PostgreSQL connections with connection pooling.

    If the PostgreSQL server is unreachable or authentication fails the pool
    is set to ``None`` and every public method returns a safe empty value
    instead of raising, so the MCP server can still start.
    """

    _instance: Optional[DatabaseManager] = None
    _connection_pool = None
    _pg_available: bool = False

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
        """Initialize the database manager with connection pooling.

        Does NOT raise if the connection fails — logs a warning instead.
        """
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.min_connections = min_connections
        self.max_connections = max_connections

        if not _PSYCOPG2_AVAILABLE:
            return  # stay in SQLite-only mode

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
                    connect_timeout=5,
                )
                DatabaseManager._pg_available = True
                logger.info(
                    f"[DB] Connection pool created: {min_connections}-{max_connections} "
                    f"connections to {user}@{host}:{port}/{database}"
                )
            except Exception as e:
                # Log but DO NOT raise — run in degraded/SQLite-only mode
                logger.warning(
                    f"[DB] PostgreSQL unavailable ({e}). "
                    "Running in SQLite-only mode — device lookups will use the CMDB SQLite cache."
                )
                self._connection_pool = None
                DatabaseManager._pg_available = False

    # ── Internal helpers ──────────────────────────────────────────────────────

    @property
    def pool(self):
        return self._connection_pool

    def get_connection(self):
        """Get a connection from the pool. Returns None if PG is unavailable."""
        if not self._pg_available or self._connection_pool is None:
            return None
        try:
            conn = self._connection_pool.getconn()
            conn.autocommit = False
            return conn
        except Exception as e:
            logger.error(f"[DB] No available connections: {e}")
            return None

    def return_connection(self, conn) -> None:
        """Return a connection to the pool."""
        if conn and self._connection_pool:
            try:
                self._connection_pool.putconn(conn)
            except Exception as e:
                logger.error(f"[DB] Error returning connection: {e}")

    def close_all(self) -> None:
        """Close all connections in the pool."""
        if self._connection_pool:
            self._connection_pool.closeall()
            self._connection_pool = None
            DatabaseManager._pg_available = False
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

        Returns None/[] gracefully if PostgreSQL is unavailable.
        """
        if not self._pg_available or self._connection_pool is None:
            logger.debug("[DB] PostgreSQL unavailable — returning empty result for query")
            return None if fetch_one else []

        conn = None
        cur = None
        try:
            conn = self.get_connection()
            if conn is None:
                return None if fetch_one else []

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

        except Exception as e:
            if conn:
                try:
                    conn.rollback()
                except Exception:
                    pass
            logger.error(f"[DB] Query error: {e}")
            return None if fetch_one else []
        finally:
            if cur:
                cur.close()
            if conn:
                self.return_connection(conn)

    def execute_many(self, query: str, params_list: list[tuple]) -> None:
        """
        Execute multiple queries in a transaction.
        No-op if PostgreSQL is unavailable.
        """
        if not self._pg_available or self._connection_pool is None:
            logger.debug("[DB] PostgreSQL unavailable — skipping batch execute")
            return

        conn = None
        cur = None
        try:
            conn = self.get_connection()
            if conn is None:
                return
            cur = conn.cursor()
            for params in params_list:
                cur.execute(query, params)
            conn.commit()
            logger.debug(f"[DB] Executed {len(params_list)} statements")
        except Exception as e:
            if conn:
                try:
                    conn.rollback()
                except Exception:
                    pass
            logger.error(f"[DB] Batch execute error: {e}")
        finally:
            if cur:
                cur.close()
            if conn:
                self.return_connection(conn)

    def test_connection(self) -> bool:
        """Test database connectivity."""
        if not self._pg_available or self._connection_pool is None:
            return False
        conn = None
        cur = None
        try:
            conn = self.get_connection()
            if conn is None:
                return False
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


# ── Singleton instance — NEVER raises on import ───────────────────────────────
db_manager = DatabaseManager()
