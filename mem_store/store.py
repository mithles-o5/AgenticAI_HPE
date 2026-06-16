import os
import json
import uuid
import sys
import redis

# Redis connection details from environment (matching resource_resolver/cache.py)
REDIS_HOST = os.getenv("MEMURAI_HOST", os.getenv("REDIS_HOST", "localhost"))
REDIS_PORT = int(os.getenv("MEMURAI_PORT", os.getenv("REDIS_PORT", "6379")))
REDIS_DB = int(os.getenv("MEMURAI_DB", os.getenv("REDIS_DB", "0")))
REDIS_PASSWORD = os.getenv("MEMURAI_PASSWORD", os.getenv("REDIS_PASSWORD"))

# Persistence path for Session ID
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Put the session_id.txt in the mcp_server directory to maintain compatibility
SESSION_ID_FILE = os.path.join(os.path.dirname(BASE_DIR), "mcp_server", "session_id.txt")

# Create a shared Redis client
_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    password=REDIS_PASSWORD,
    decode_responses=True
)

def init_db():
    """Initializes/pings the Redis database."""
    try:
        _client.ping()
        print("✅ Redis memory store connection verified successfully.", file=sys.stderr)
    except Exception as e:
        print(f"❌ Error connecting to Redis memory store: {e}", file=sys.stderr)
        raise

def remember(session_id: str, key: str, value):
    """Upsert a key-value pair for a session in Redis."""
    redis_key = f"session:{session_id}:{key}"
    val_json = json.dumps(value)
    # Store key value
    _client.set(redis_key, val_json)
    # Keep track of the keys in this session via a Redis Set
    _client.sadd(f"session:{session_id}:_keys", key)

def recall(session_id: str, key: str):
    """Fetch a single value from Redis, return None if missing."""
    redis_key = f"session:{session_id}:{key}"
    val_json = _client.get(redis_key)
    if val_json:
        return json.loads(val_json)
    return None

def recall_session(session_id: str) -> dict:
    """Return all key-value pairs for a session as a dictionary."""
    keys_set = _client.smembers(f"session:{session_id}:_keys")
    if not keys_set:
        return {}
    session_data = {}
    for key in keys_set:
        val = recall(session_id, key)
        if val is not None:
            session_data[key] = val
    return session_data

def forget_key(session_id: str, key: str):
    """Delete one key from the session."""
    redis_key = f"session:{session_id}:{key}"
    _client.delete(redis_key)
    _client.srem(f"session:{session_id}:_keys", key)

def forget_session(session_id: str):
    """Delete an entire session."""
    keys_set = _client.smembers(f"session:{session_id}:_keys")
    if keys_set:
        for key in keys_set:
            _client.delete(f"session:{session_id}:{key}")
    _client.delete(f"session:{session_id}:_keys")

def list_sessions() -> list:
    """Return all active session IDs in the Redis store."""
    sessions = set()
    for k in _client.scan_iter(match="session:*:_keys"):
        parts = k.split(":")
        if len(parts) >= 3:
            sessions.add(parts[1])
    return list(sessions)

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
