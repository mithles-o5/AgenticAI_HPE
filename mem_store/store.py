import os
import json
import uuid
import sys
from datetime import datetime
import psycopg2

# Session ID file persistence path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Put the session_id.txt in the mcp_server directory to maintain compatibility
SESSION_ID_FILE = os.path.join(os.path.dirname(BASE_DIR), "mcp_server", "session_id.txt")

# Load database connection parameters
PG_HOST = os.getenv("PGHOST", "localhost")
PG_PORT = int(os.getenv("PGPORT", "5432"))
PG_USER = os.getenv("PGUSER", "postgres")
PG_PASSWORD = os.getenv("PGPASSWORD", "password")
PG_DATABASE = os.getenv("PGDATABASE", "postgres")

def _get_connection():
    """Opens a connection to the database."""
    return psycopg2.connect(
        host=PG_HOST,
        port=PG_PORT,
        user=PG_USER,
        password=PG_PASSWORD,
        database=PG_DATABASE
    )

def init_db():
    """Initializes the database table for memory store if it doesn't exist."""
    conn = None
    try:
        conn = _get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memory (
                session_id TEXT,
                key TEXT,
                value TEXT,
                updated_at TEXT,
                PRIMARY KEY (session_id, key)
            )
        """)
        conn.commit()
        print("✅ memory store database initialized successfully.", file=sys.stderr)
    except Exception as e:
        print(f"❌ Error initializing memory database: {e}", file=sys.stderr)
        raise
    finally:
        if conn:
            conn.close()

def remember(session_id: str, key: str, value):
    """Upsert a key-value pair for a session."""
    conn = None
    try:
        conn = _get_connection()
        cursor = conn.cursor()
        val_json = json.dumps(value)
        updated_at = datetime.utcnow().isoformat() + "Z"
        cursor.execute("""
            INSERT INTO memory (session_id, key, value, updated_at)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (session_id, key) DO UPDATE SET
                value = EXCLUDED.value,
                updated_at = EXCLUDED.updated_at
        """, (session_id, key, val_json, updated_at))
        conn.commit()
    except Exception as e:
        print(f"❌ Error saving to database (remember): {e}", file=sys.stderr)
        raise
    finally:
        if conn:
            conn.close()

def recall(session_id: str, key: str):
    """Fetch a single value, return None if missing."""
    conn = None
    try:
        conn = _get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM memory WHERE session_id = %s AND key = %s", (session_id, key))
        row = cursor.fetchone()
        if row:
            return json.loads(row[0])
        return None
    except Exception as e:
        print(f"❌ Error fetching from database (recall): {e}", file=sys.stderr)
        return None
    finally:
        if conn:
            conn.close()

def recall_session(session_id: str) -> dict:
    """Return all key-value pairs for a session as a dictionary."""
    conn = None
    try:
        conn = _get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT key, value FROM memory WHERE session_id = %s", (session_id,))
        rows = cursor.fetchall()
        return {row[0]: json.loads(row[1]) for row in rows}
    except Exception as e:
        print(f"❌ Error fetching session data (recall_session): {e}", file=sys.stderr)
        return {}
    finally:
        if conn:
            conn.close()

def forget_key(session_id: str, key: str):
    """Delete one key from the session."""
    conn = None
    try:
        conn = _get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM memory WHERE session_id = %s AND key = %s", (session_id, key))
        conn.commit()
    except Exception as e:
        print(f"❌ Error deleting key (forget_key): {e}", file=sys.stderr)
        raise
    finally:
        if conn:
            conn.close()

def forget_session(session_id: str):
    """Delete an entire session."""
    conn = None
    try:
        conn = _get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM memory WHERE session_id = %s", (session_id,))
        conn.commit()
    except Exception as e:
        print(f"❌ Error deleting session (forget_session): {e}", file=sys.stderr)
        raise
    finally:
        if conn:
            conn.close()

def list_sessions() -> list:
    """Return all active session IDs in the database."""
    conn = None
    try:
        conn = _get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT session_id FROM memory")
        rows = cursor.fetchall()
        return [row[0] for row in rows]
    except Exception as e:
        print(f"❌ Error listing sessions: {e}", file=sys.stderr)
        return []
    finally:
        if conn:
            conn.close()

def _get_or_create_session_id() -> str:
    """Retrieves the persisted session ID from file or creates a new one."""
    try:
        if os.path.exists(SESSION_ID_FILE):
            with open(SESSION_ID_FILE, "r") as f:
                sid = f.read().strip()
                if sid:
                    return sid
    except Exception as e:
        print(f"⚠️ Error reading session ID file: {e}", file=sys.stderr)
        
    sid = str(uuid.uuid4())
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(SESSION_ID_FILE), exist_ok=True)
        with open(SESSION_ID_FILE, "w") as f:
            f.write(sid)
    except Exception as e:
        print(f"⚠️ Error writing session ID file: {e}", file=sys.stderr)
    return sid

# Initialise persistent session ID
SESSION_ID = _get_or_create_session_id()
