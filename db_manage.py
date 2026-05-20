#!/usr/bin/env python3
"""
Database Management CLI
=======================
Production-grade command-line tool for managing the Resource Resolver database.

Usage:
    python db_manage.py --help
    python db_manage.py init              # Initialize database schema
    python db_manage.py seed              # Seed database with sample data
    python db_manage.py clear             # Clear all data
    python db_manage.py status            # Show database status
    python db_manage.py list-servers      # List all servers
    python db_manage.py add-server        # Add a new server
    python db_manage.py update-server     # Update existing server
    python db_manage.py delete-server     # Delete a server
    python db_manage.py export-data       # Export database to JSON
    python db_manage.py import-data       # Import database from JSON
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from pathlib import Path
from typing import Optional

import psycopg2

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, THIS_DIR)

from db import db_manager
from db_seed import (
    clear_database,
    seed_base_data,
    create_oneview,
    create_com,
    insert_oneview_servers,
    insert_com_servers,
    add_server_protocols,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)-8s] %(message)s",
)
logger = logging.getLogger(__name__)


class DatabaseManager:
    """High-level database management interface."""

    @staticmethod
    def init_schema():
        """Initialize database schema from db_schema.sql."""
        logger.info("[DB Manager] Initializing database schema...")
        
        schema_file = os.path.join(THIS_DIR, "db_schema.sql")
        
        if not os.path.exists(schema_file):
            logger.error(f"Schema file not found: {schema_file}")
            return False
        
        try:
            with open(schema_file, 'r') as f:
                schema_sql = f.read()
            
            # Execute schema (note: psycopg2 doesn't support multiple statements directly)
            # So we need to split and execute
            statements = schema_sql.split(';')
            
            for statement in statements:
                statement = statement.strip()
                if statement:
                    try:
                        db_manager.execute_query(statement, fetch_all=False)
                    except psycopg2.ProgrammingError as e:
                        if "already exists" not in str(e):
                            logger.warning(f"Skipping statement (may already exist): {statement[:50]}")
            
            logger.info("[DB Manager] ✓ Schema initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"[DB Manager] Error initializing schema: {e}")
            return False

    @staticmethod
    def seed_database():
        """Seed database with sample data."""
        logger.info("[DB Manager] Seeding database...")
        
        try:
            # Clear existing data
            clear_database()
            
            # Seed base data
            base_data = seed_base_data()
            
            # Create OneViews
            logger.info("[DB Manager] Creating OneViews...")
            for ov_num in range(1, 11):  # 10 OneViews
                ov_id = create_oneview(ov_num, base_data)
                insert_oneview_servers(ov_id, base_data, count=1000)
            
            # Create CoM
            logger.info("[DB Manager] Creating CoM...")
            com_id = create_com(base_data)
            insert_com_servers(com_id, base_data, count=500)
            
            # Add protocols
            add_server_protocols(base_data)
            
            logger.info("[DB Manager] ✓ Database seeded successfully")
            return True
            
        except Exception as e:
            logger.error(f"[DB Manager] Error seeding database: {e}")
            return False

    @staticmethod
    def get_status():
        """Get database status and statistics."""
        logger.info("[DB Manager] Fetching database status...")
        
        try:
            stats = {}
            
            # Count records
            queries = {
                "Vendors": "SELECT COUNT(*) as count FROM vendors",
                "Protocols": "SELECT COUNT(*) as count FROM protocols",
                "OneViews": "SELECT COUNT(*) as count FROM oneviews",
                "OneView Servers": "SELECT COUNT(*) as count FROM servers",
                "CoMs": "SELECT COUNT(*) as count FROM coms",
                "CoM Servers": "SELECT COUNT(*) as count FROM com_servers",
            }
            
            for label, query in queries.items():
                result = db_manager.execute_query(query, fetch_one=True)
                stats[label] = result["count"] if result else 0
            
            return stats
            
        except Exception as e:
            logger.error(f"[DB Manager] Error getting status: {e}")
            return None

    @staticmethod
    def list_servers(limit: int = 100, offset: int = 0):
        """List all servers with pagination."""
        logger.info(f"[DB Manager] Listing servers (limit={limit}, offset={offset})...")
        
        try:
            query = """
                SELECT 
                    s.id, s.uuid, s.name, s.ip_address, 
                    v.name as vendor, s.model, s.location,
                    string_agg(DISTINCT p.name, ', ') as protocols
                FROM servers s
                LEFT JOIN vendors v ON s.vendor_id = v.id
                LEFT JOIN server_protocols sp ON s.id = sp.server_id
                LEFT JOIN protocols p ON sp.protocol_id = p.id
                GROUP BY s.id, v.name
                ORDER BY s.name
                LIMIT %s OFFSET %s
            """
            
            rows = db_manager.execute_query(query, (limit, offset), fetch_all=True)
            
            logger.info(f"[DB Manager] Found {len(rows) if rows else 0} servers")
            
            return rows
            
        except Exception as e:
            logger.error(f"[DB Manager] Error listing servers: {e}")
            return None

    @staticmethod
    def get_server_by_uuid(uuid: str):
        """Get server details by UUID."""
        logger.info(f"[DB Manager] Fetching server: {uuid}")
        
        try:
            query = """
                SELECT 
                    s.*, v.name as vendor_name,
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
            
            result = db_manager.execute_query(query, (uuid,), fetch_one=True)
            
            if result:
                logger.info(f"[DB Manager] ✓ Found server: {result['name']}")
                return dict(result)
            else:
                logger.warning(f"[DB Manager] Server not found: {uuid}")
                return None
                
        except Exception as e:
            logger.error(f"[DB Manager] Error fetching server: {e}")
            return None

    @staticmethod
    def export_to_json(output_file: str = "db_export.json"):
        """Export database to JSON file."""
        logger.info(f"[DB Manager] Exporting database to {output_file}...")
        
        try:
            export_data = {
                "exported_at": str(__import__('datetime').datetime.now()),
                "status": db_manager.execute_query(
                    "SELECT COUNT(*) as count FROM servers",
                    fetch_one=True
                ),
                "servers": [],
                "metadata": {}
            }
            
            # Export servers
            query = """
                SELECT 
                    s.*, v.name as vendor_name,
                    string_agg(DISTINCT p.name, ', ') as protocols,
                    string_agg(DISTINCT sa.alias, ', ') as aliases,
                    string_agg(DISTINCT st.tag, ', ') as tags
                FROM servers s
                LEFT JOIN vendors v ON s.vendor_id = v.id
                LEFT JOIN server_protocols sp ON s.id = sp.server_id
                LEFT JOIN protocols p ON sp.protocol_id = p.id
                LEFT JOIN server_aliases sa ON s.id = sa.server_id
                LEFT JOIN server_tags st ON s.id = st.server_id
                GROUP BY s.id, v.name
                ORDER BY s.name
            """
            
            rows = db_manager.execute_query(query, fetch_all=True)
            
            for row in rows:
                export_data["servers"].append(dict(row))
            
            # Write to file
            with open(output_file, 'w') as f:
                json.dump(export_data, f, indent=2, default=str)
            
            logger.info(f"[DB Manager] ✓ Exported {len(export_data['servers'])} servers to {output_file}")
            return True
            
        except Exception as e:
            logger.error(f"[DB Manager] Error exporting data: {e}")
            return False


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Resource Resolver Database Management Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python db_manage.py init              # Initialize schema
  python db_manage.py seed              # Seed sample data
  python db_manage.py status            # Show statistics
  python db_manage.py list-servers      # List all servers
  python db_manage.py export-data       # Export to JSON
        """
    )
    
    parser.add_argument(
        "command",
        nargs="?",
        default="status",
        choices=[
            "init",
            "seed",
            "status",
            "list-servers",
            "get-server",
            "export-data",
            "import-data",
            "clear",
        ],
        help="Command to execute"
    )
    
    parser.add_argument("--uuid", help="Server UUID (for get-server)")
    parser.add_argument("--output", default="db_export.json", help="Output file for exports")
    parser.add_argument("--limit", type=int, default=100, help="Limit for list commands")
    parser.add_argument("--offset", type=int, default=0, help="Offset for list commands")
    
    args = parser.parse_args()
    
    # Test connection first
    if not db_manager.test_connection():
        logger.error("Cannot connect to database. Check your configuration.")
        sys.exit(1)
    
    # Execute command
    if args.command == "init":
        success = DatabaseManager.init_schema()
        sys.exit(0 if success else 1)
    
    elif args.command == "seed":
        success = DatabaseManager.seed_database()
        sys.exit(0 if success else 1)
    
    elif args.command == "status":
        stats = DatabaseManager.get_status()
        if stats:
            print("\n" + "="*60)
            print("DATABASE STATUS")
            print("="*60)
            for label, count in stats.items():
                print(f"  {label:.<40} {count:>10,}")
            print("="*60 + "\n")
        sys.exit(0)
    
    elif args.command == "list-servers":
        servers = DatabaseManager.list_servers(limit=args.limit, offset=args.offset)
        if servers:
            print("\n" + "="*120)
            print(f"{'ID':<5} {'UUID':<37} {'Name':<30} {'IP Address':<20} {'Protocols':<20}")
            print("="*120)
            for server in servers:
                print(
                    f"{server['id']:<5} "
                    f"{server['uuid']:<37} "
                    f"{server['name']:<30} "
                    f"{str(server['ip_address']):<20} "
                    f"{server['protocols'] or 'N/A':<20}"
                )
            print("="*120 + "\n")
        sys.exit(0)
    
    elif args.command == "get-server":
        if not args.uuid:
            logger.error("--uuid required for get-server command")
            sys.exit(1)
        server = DatabaseManager.get_server_by_uuid(args.uuid)
        if server:
            print("\n" + "="*60)
            print("SERVER DETAILS")
            print("="*60)
            for key, value in server.items():
                print(f"  {key:.<40} {value}")
            print("="*60 + "\n")
        sys.exit(0)
    
    elif args.command == "export-data":
        success = DatabaseManager.export_to_json(args.output)
        sys.exit(0 if success else 1)
    
    elif args.command == "clear":
        logger.warning("Clearing all database data...")
        confirm = input("Type 'yes' to confirm: ")
        if confirm.lower() == "yes":
            clear_database()
            logger.info("✓ Database cleared")
        else:
            logger.info("Cancelled")
        sys.exit(0)
    
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
