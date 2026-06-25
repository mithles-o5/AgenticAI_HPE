"""
Helper function: load the registry from the database.

If PostgreSQL is unavailable the registry still works in SQLite-only mode —
device lookups will return None / [] rather than crashing.
"""

from __future__ import annotations

import logging

from db import db_manager
from registry import ResourceRegistry

logger = logging.getLogger(__name__)


def load_registry_from_db() -> ResourceRegistry:
    """
    Initialize a ResourceRegistry.

    If PostgreSQL is available it will be used for device lookups.
    If not, the registry still starts successfully — all query methods
    return None/[] gracefully (SQLite CMDB cache is used by the resolver
    as the fallback source of truth).
    """
    if db_manager._pg_available and db_manager.test_connection():
        logger.info("[DB Loader] PostgreSQL registry verified and connected")
    else:
        logger.warning(
            "[DB Loader] PostgreSQL unavailable — registry starting in "
            "SQLite-only mode. Device lookups will use the CMDB SQLite cache."
        )
    # ResourceRegistry() is always safe to construct — its methods handle
    # the unavailable-PG case internally via db_manager._pg_available guards.
    return ResourceRegistry()
