"""
Database Registry Loader
=========================
Initializes a database-backed ResourceRegistry with zero in-memory loading.

All server data stays in PostgreSQL.  The registry queries on-demand.
"""

from __future__ import annotations

import logging
import os
import sys

# ── path: ensure flat files are importable ────────────────────────────────────
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, THIS_DIR)

from registry import ResourceRegistry
from db import db_manager

logger = logging.getLogger(__name__)


def load_registry_from_db() -> ResourceRegistry:
    """
    Initialize a database-backed registry.
    
    NOTE: This registry queries PostgreSQL directly on each lookup.
    All servers stay in the database - zero in-memory loading.
    
    Returns
    -------
    Empty ResourceRegistry instance (backed by database queries)
    """
    registry = ResourceRegistry()

    # Test connection
    if not db_manager.test_connection():
        logger.error("[DB Loader] Database connection failed!")
        raise RuntimeError("Cannot connect to database")

    logger.info("[DB Loader] ✓ Database connection verified")
    logger.info("[DB Loader] ✓ Registry will query database on-demand (zero memory overhead)")
    
    return registry

