#!/usr/bin/env python3
"""
Minimal Database Management CLI
Keeps only `init`, `seed`, and `clear` commands per user request.
"""

from __future__ import annotations

import argparse
import logging
import os
import sys

import psycopg2

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, THIS_DIR)

from db import db_manager
from db_seed import clear_database, seed_current_schema

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)-8s] %(message)s")
logger = logging.getLogger(__name__)


class DatabaseManager:
    """Minimal DB management for init/seed/clear."""

    @staticmethod
    def init_schema() -> bool:
        """Initialize database schema from db_schema.sql."""
        logger.info("[DB Manager] Initializing database schema...")

        schema_file = os.path.join(THIS_DIR, "db_schema.sql")

        if not os.path.exists(schema_file):
            logger.error(f"Schema file not found: {schema_file}")
            return False

        try:
            with open(schema_file, "r", encoding="utf-8") as f:
                schema_sql = f.read()

            # Split statements; execute non-empty ones
            statements = [s.strip() for s in schema_sql.split(";") if s.strip()]
            for stmt in statements:
                try:
                    db_manager.execute_query(stmt, fetch_all=False)
                except psycopg2.ProgrammingError as e:
                    if "already exists" not in str(e):
                        logger.warning("Skipping statement (may already exist)")

            logger.info("[DB Manager] ✓ Schema initialized successfully")
            return True

        except Exception as e:
            logger.error(f"[DB Manager] Error initializing schema: {e}")
            return False

    @staticmethod
    def seed_database() -> bool:
        """Seed database with sample data using the project's seeder."""
        logger.info("[DB Manager] Seeding database...")
        try:
            seed_current_schema()
            logger.info("[DB Manager] ✓ Database seeded successfully")
            return True
        except Exception as e:
            logger.error(f"[DB Manager] Error seeding database: {e}")
            return False


def main() -> None:
    parser = argparse.ArgumentParser(description="Minimal DB management: init, seed, clear")
    parser.add_argument("command", choices=["init", "seed", "clear"], help="Command to run")

    args = parser.parse_args()

    # Ensure DB is reachable
    if not db_manager.test_connection():
        logger.error("Cannot connect to database. Check your configuration.")
        sys.exit(1)

    if args.command == "init":
        success = DatabaseManager.init_schema()
        sys.exit(0 if success else 1)

    elif args.command == "seed":
        success = DatabaseManager.seed_database()
        sys.exit(0 if success else 1)

    elif args.command == "clear":
        logger.warning("Clearing all database data...")
        confirm = input("Type 'yes' to confirm: ")
        if confirm.lower() == "yes":
            clear_database()
            logger.info("✓ Database cleared")
            sys.exit(0)
        else:
            logger.info("Cancelled")
            sys.exit(1)


if __name__ == "__main__":
    main()
