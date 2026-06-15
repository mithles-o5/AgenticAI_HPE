"""Helper function, if my db connection fails it throws an error ."""

from __future__ import annotations

import logging

from db import db_manager
from registry import ResourceRegistry

logger = logging.getLogger(__name__)


def load_registry_from_db() -> ResourceRegistry:
    """Initialize a PostgreSQL-backed registry."""
    if not db_manager.test_connection():
        logger.error("[DB Loader] Database connection failed")
        raise RuntimeError("Cannot connect to database")
    logger.info("[DB Loader] PostgreSQL registry verified")
    return ResourceRegistry()
