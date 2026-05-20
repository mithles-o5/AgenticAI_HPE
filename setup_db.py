#!/usr/bin/env python3
"""
Quick Start Setup Script
========================
Automates initial PostgreSQL setup for Resource Resolver.

This script:
1. Prompts for database configuration
2. Creates the database schema
3. Seeds with mocked infrastructure
4. Verifies the setup
"""

import os
import sys
import subprocess
from pathlib import Path

def print_banner(text: str):
    """Print a formatted banner."""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def check_postgres():
    """Check if PostgreSQL is installed and accessible."""
    try:
        result = subprocess.run(
            ["psql", "--version"],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            print(f"✓ PostgreSQL found: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        print("✗ PostgreSQL not found in PATH")
        return False

def get_db_config():
    """Prompt user for database configuration."""
    print_banner("PostgreSQL Configuration")
    
    config = {}
    config["host"] = input("Database host [localhost]: ").strip() or "localhost"
    config["port"] = input("Database port [5432]: ").strip() or "5432"
    config["user"] = input("Database user [postgres]: ").strip() or "postgres"
    config["password"] = input("Database password [postgres]: ").strip() or "postgres"
    config["dbname"] = input("Database name [resource_resolver]: ").strip() or "resource_resolver"
    
    return config

def create_env_file(config: dict):
    """Create .env file with database configuration."""
    env_path = Path(".env")
    env_content = f"""# PostgreSQL Database Configuration (Auto-generated)
DB_HOST={config['host']}
DB_PORT={config['port']}
DB_NAME={config['dbname']}
DB_USER={config['user']}
DB_PASSWORD={config['password']}
"""
    
    env_path.write_text(env_content)
    print(f"✓ Created .env file")

def test_connection(config: dict):
    """Test database connection."""
    print("\nTesting database connection...")
    
    conn_string = f"postgresql://{config['user']}@{config['host']}:{config['port']}/{config['dbname']}"
    
    try:
        result = subprocess.run(
            [
                "psql",
                "-h", config["host"],
                "-p", config["port"],
                "-U", config["user"],
                "-d", "postgres",  # Connect to default postgres DB first
                "-c", "SELECT 1",
            ],
            capture_output=True,
            text=True,
            timeout=5,
        )
        
        if result.returncode == 0:
            print("✓ Connection successful")
            return True
        else:
            print(f"✗ Connection failed: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("✗ Connection timeout")
        return False
    except Exception as e:
        print(f"✗ Connection error: {e}")
        return False

def create_database(config: dict):
    """Create the database if it doesn't exist."""
    print(f"\nCreating database '{config['dbname']}'...")
    
    try:
        result = subprocess.run(
            [
                "psql",
                "-h", config["host"],
                "-p", config["port"],
                "-U", config["user"],
                "-d", "postgres",
                "-c", f"CREATE DATABASE {config['dbname']};",
            ],
            capture_output=True,
            text=True,
        )
        
        if result.returncode == 0 or "already exists" in result.stderr:
            print(f"✓ Database ready: {config['dbname']}")
            return True
        else:
            print(f"✗ Failed to create database: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def load_schema(config: dict):
    """Load database schema from SQL file."""
    schema_file = Path("db_schema.sql")
    
    if not schema_file.exists():
        print(f"✗ Schema file not found: {schema_file}")
        return False
    
    print(f"\nLoading schema from {schema_file}...")
    
    try:
        with open(schema_file, "r") as f:
            schema_sql = f.read()
        
        result = subprocess.run(
            [
                "psql",
                "-h", config["host"],
                "-p", config["port"],
                "-U", config["user"],
                "-d", config["dbname"],
            ],
            input=schema_sql,
            capture_output=True,
            text=True,
        )
        
        if result.returncode == 0:
            print("✓ Schema loaded successfully")
            return True
        else:
            print(f"✗ Schema load error:\n{result.stderr}")
            return False
            
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def seed_database():
    """Run database seeder."""
    print("\nSeeding database with mocked infrastructure...")
    print("(This may take a minute for 10,500 servers...)\n")
    
    try:
        result = subprocess.run(
            [sys.executable, "db_seed.py"],
            capture_output=True,
            text=True,
            timeout=300,
        )
        
        if result.returncode == 0:
            print("✓ Database seeded successfully")
            if result.stdout:
                print(result.stdout)
            return True
        else:
            print(f"✗ Seed error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("✗ Seeding timed out")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def verify_setup(config: dict):
    """Verify the setup is complete."""
    print_banner("Verifying Setup")
    
    queries = [
        ("Vendors", "SELECT COUNT(*) as count FROM vendors;"),
        ("OneViews", "SELECT COUNT(*) as count FROM oneviews;"),
        ("OneView Servers", "SELECT COUNT(*) as count FROM servers;"),
        ("CoM Servers", "SELECT COUNT(*) as count FROM com_servers;"),
        ("Total Servers", "SELECT (SELECT COUNT(*) FROM servers) + (SELECT COUNT(*) FROM com_servers) as count;"),
    ]
    
    try:
        for name, query in queries:
            result = subprocess.run(
                [
                    "psql",
                    "-h", config["host"],
                    "-p", config["port"],
                    "-U", config["user"],
                    "-d", config["dbname"],
                    "-t", "-c", query,
                ],
                capture_output=True,
                text=True,
                timeout=10,
            )
            
            if result.returncode == 0:
                count = result.stdout.strip().split("\n")[0].strip()
                print(f"  {name}: {count}")
            else:
                print(f"  {name}: [error]")
                
    except Exception as e:
        print(f"✗ Verification error: {e}")

def main():
    print_banner("Resource Resolver Database Setup")
    
    # Check dependencies
    if not check_postgres():
        print("\n⚠ PostgreSQL is required. Please install it first.")
        sys.exit(1)
    
    # Get configuration
    config = get_db_config()
    
    # Create .env file
    create_env_file(config)
    
    # Test connection
    if not test_connection(config):
        print("\n⚠ Could not connect to PostgreSQL. Check your credentials.")
        sys.exit(1)
    
    # Create database
    if not create_database(config):
        print("\n⚠ Failed to create database.")
        sys.exit(1)
    
    # Load schema
    if not load_schema(config):
        print("\n⚠ Failed to load schema.")
        sys.exit(1)
    
    # Seed database
    if not seed_database():
        print("\n⚠ Failed to seed database.")
        sys.exit(1)
    
    # Verify setup
    verify_setup(config)
    
    print_banner("Setup Complete!")
    print("""
Next steps:
  1. Install Python dependencies:
     pip install -r requirements.txt
     
  2. Start the MCP server:
     python mcp_tool.py
     
  3. Use with Claude:
     - resolve_resource("turn on server-00001")
     - list_servers()
     - power_on_server("power on cloud-server-00001", action="On")

For more details, see SETUP_DATABASE.md
""")

if __name__ == "__main__":
    main()
