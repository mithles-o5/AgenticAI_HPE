"""
HPE OneView MCP Server — Fully Embedded (No Separate Server Needed)
====================================================================

FLOW:
  1. Any hardware tool is called by Claude
  2. If no token is found → SSO login is triggered automatically (browser opens)
  3. After login → token is saved → user claims are fetched from the SSO provider
  4. Claims (email) are looked up in roles.json to get the user's role
  5. RBAC + ABAC checks run IN-PROCESS (no separate server needed)
  6. If authorized → hardware action is performed on the mock backend
  7. Result returned to Claude

WHY NO SEPARATE SERVER:
  The authorization policy engine (RBAC, ABAC) is pure Python logic.
  It does NOT need to be a web server. Importing it directly is:
    - Simpler  (one process, not two)
    - Faster   (no HTTP round-trips)
    - Reliable (no risk of the backend not being running)
  The hardware_mock.py IS kept as a FastAPI server because it simulates
  a real HPE OneView REST API that would exist in production.

TO SWITCH SSO PROVIDER:
  Edit authentication/__init__.py and change PROVIDER = "auth0"
"""

import sys
import os
import json
from datetime import datetime
import logging

import httpx
import time
import uuid
from mcp.server.fastmcp import FastMCP

# ─────────────────────────────────────────────────────────────────────────────
# Path Setup — add authentication/, authorization/, resource_resolver/
# ─────────────────────────────────────────────────────────────────────────────

BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
LOG_FILE     = os.path.join(BASE_DIR, "mcp.log")

# Configure logging to write to mcp.log
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
    ]
)

# Mirror sys.stderr to mcp.log so traceback and warnings are captured
class StderrLogger:
    def __init__(self, original_stderr, log_filepath):
        self.stderr = original_stderr
        self.log_file = open(log_filepath, "a", encoding="utf-8")

    def write(self, message):
        self.stderr.write(message)
        self.log_file.write(message)
        self.log_file.flush()

    def flush(self):
        self.stderr.flush()
        self.log_file.flush()

sys.stderr = StderrLogger(sys.stderr, LOG_FILE)
ROOT_DIR     = os.path.normpath(os.path.join(BASE_DIR, ".."))
AUTH_DIR     = os.path.normpath(os.path.join(BASE_DIR, "..", "authentication"))
AUTHZ_DIR    = os.path.normpath(os.path.join(BASE_DIR, "..", "authorization"))
RESOLVER_DIR = os.path.normpath(os.path.join(BASE_DIR, "..", "resource_resolver"))
PLANNER_DIR  = os.path.normpath(os.path.join(BASE_DIR, "..", "task_planner"))
ENGINE_DIR   = os.path.normpath(os.path.join(BASE_DIR, "..", "execution_engine"))

sys.path.insert(0, ROOT_DIR)
sys.path.insert(0, AUTH_DIR)
sys.path.insert(0, AUTHZ_DIR)
sys.path.insert(0, RESOLVER_DIR)
sys.path.insert(0, PLANNER_DIR)
sys.path.insert(0, ENGINE_DIR)

# Mock database disabled by user request

import psycopg2



# New Redis Memory Store
try:
    from mem_store.store import SESSION_ID, remember, recall, list_sessions
except ImportError as e:
    print(f"⚠️ Failed to import mem_store: {e}", file=sys.stderr)

# Authentication imports
from authentication import get_provider, PROVIDER       # noqa: E402
from authentication.token_store import save_token, load_token, load_provider, clear_token  # noqa: E402

# Authorization engine imports (runs in-process, no separate server needed)
from authorization.rbac   import RBACEngine   # noqa: E402
from authorization.abac   import ABACEngine   # noqa: E402
from authorization.models import TokenPayload, Resource, Context  # noqa: E402

# Resource Resolver imports
from resource_resolver.resolver    import ResourceResolver   # noqa: E402
from resource_resolver.cache       import ResourceCache     # noqa: E402
from resource_resolver.db_loader   import load_registry_from_db  # noqa: E402
from resource_resolver.query_agent import QueryAgent        # noqa: E402
from task_planner.planner     import TaskPlanner, Task  # noqa: E402
from resource_resolver.errors      import ResolverError     # noqa: E402
from enum        import Enum              # noqa: E402

# Execution engine / Agent dispatcher
from execution_engine import AgentDispatcher  # noqa: E402
_dispatcher = AgentDispatcher()

class Protocol(str, Enum):
    ONEVIEW = "oneview"
    COMS = "coms"

# Path to roles.json (the role mapping file you can freely edit)
ROLES_FILE = os.path.join(AUTHZ_DIR, "roles.json")

# ── In-memory token claims cache (avoids repeated /userinfo network calls) ────
# Structure: {token_hash: {"claims": {...}, "expires_at": float}}
_CLAIMS_CACHE: dict = {}
_CLAIMS_CACHE_TTL = 300  # seconds — re-verify every 5 minutes max

# Mock server — mirrors the real HPE OneView REST API
HARDWARE_BACKEND_URL = "http://127.0.0.1:8000"

# ── Resolver singletons (built once at startup) ───────────────────────────────
_registry = load_registry_from_db()
_cache    = ResourceCache()
_resolver = ResourceResolver(registry=_registry, cache=_cache)

# Start background polling thread
try:
    from resource_resolver.polling_engine import start_background_polling
    poll_interval = int(os.getenv("POLL_INTERVAL_SECONDS", "600"))
    start_background_polling(_cache, poll_interval)
except Exception as e:
    print(f"⚠️ Failed to start background polling: {e}", file=sys.stderr)

# ─────────────────────────────────────────────────────────────────────────────
# MCP Server
# ─────────────────────────────────────────────────────────────────────────────

# Available SSO providers — ALL use browser-based PKCE (no credentials in chat).
AVAILABLE_PROVIDERS = {
    "auth0" : "Auth0      ✅ Ready         (browser login via Auth0)",
    "okta"  : "Okta       ✅ Ready         (browser login via okta)",
    "azure" : "Azure AD   🔲 Needs config  (fill in AZURE_TENANT_ID + AZURE_CLIENT_ID in azure_provider.py)",
    "local" : "Local Mock ✅ Ready         (username/password credentials)",
}

PROVIDER_LIST = "\n".join(
    f"  • {k} — {v}" for k, v in AVAILABLE_PROVIDERS.items()
)

mcp = FastMCP(
    "HPE-Integrated-MCP",
    instructions=f"""
    You are managing HPE infrastructure via MCP.

    ── INFRASTRUCTURE MANAGEMENT TOOL ─────────────────────────────────────────
    manage_infrastructure_resource(query)
      USE THIS TOOL for ALL resource operations — status, power, create, delete, AND attribute updates.
      Pass the user's query EXACTLY as written. The backend handles routing automatically.

      SUPPORTED OPERATIONS (ALL must call this tool — NEVER refuse):
        • Status / Query  : "status of nimble-prod-009", "show alletra-array-008"
        • Power           : "turn off primera-san-010", "power on 3par-array-011"
        • Create          : "create storage device new-array-01"
        • Delete          : "delete nimble-prod-009"
        • Update / Patch  : "change the temperature of nimble-prod-009 to 78.5"
                            "set health_status of alletra-array-008 to DEGRADED"
                            "update free_capacity_gb of primera-san-010 to 50"
                            "modify firmware version of 3par-array-011 to 2.1.0"
        • List            : "list all storage systems", "list storage volumes"

    ── FULL PIPELINE (all tools) ─────────────────────────────────────────────
      1. Authenticates the user
      2. Parses the natural language command
      3. Checks RBAC + ABAC permissions
      4. Dispatches to the correct backend / agent
      5. Returns the result

    ── AUTHENTICATION (BROWSER ONLY — no credentials in chat) ──────────────────
    All login flows open a secure browser window. Credentials NEVER pass through chat.

    CRITICAL LOGIN RULES (Follow strictly):
    1. If a tool returns an unauthenticated error, you must use the `sso_login` tool to authenticate the mock session.
    2. Because this is a mock environment, you can use any of the mock providers (e.g. 'auth0', 'okta', 'azure') without needing real credentials.
    3. You can either ask the user which mock provider to use, or if they have already given permission, just call `sso_login` directly.

    CRITICAL LOGOUT RULES:
    If the user asks to logout or end the session, you MUST execute the `logout()` tool.

    ── CRITICAL BEHAVIOURAL RULES (STRICT) ─────────────────────────────────────
    1. ZERO HALLUCINATION: You MUST ONLY reply using the data returned by the tools.
       If a tool returns an error, "Not found", or "Task resolution failed", you must report that failure verbatim.
       NEVER make up or assume any status, configuration, metrics, or details for any resource.
    2. FORCE SSO: If the tool returns "Not authenticated" or "Not logged in", you MUST NOT perform any actions or show any resource information. Force the user to log in first.
    3. NO ACCESS BYPASS: If a resource is not found in the CMDB database (resolution fails), you must tell the user that the resource is not registered in the system. Do not guess its state.
    4. NEVER REFUSE: When asked for the status, update, or any operation on a resource, you MUST call manage_infrastructure_resource with the user's query. DO NOT say "not supported", "I don't have access", or generate your own error. The tool handles ALL operations including attribute updates (PATCH). ALWAYS call the tool first.
    5. NO SELF-GENERATED ERRORS: NEVER produce an "Update Not Supported" or similar message from your own knowledge. ALWAYS call manage_infrastructure_resource and return what the tool says.
    """
)

# ─────────────────────────────────────────────────────────────────────────────
# Core Helpers
# ─────────────────────────────────────────────────────────────────────────────

def _trigger_login(provider_name: str, **kwargs) -> tuple[str, dict]:
    """
    Trigger SSO login for the specified provider.
    kwargs are passed to the provider constructor (e.g. username/password for local).
    Returns (token, user_claims) on success.
    Raises RuntimeError on failure.
    """
    if provider_name not in AVAILABLE_PROVIDERS:
        names = ", ".join(AVAILABLE_PROVIDERS.keys())
        raise RuntimeError(f"Unknown provider '{provider_name}'. Choose from: {names}")

    try:
        provider = get_provider(provider_name, **kwargs)
    except Exception as e:
        raise RuntimeError(f"Could not initialise provider '{provider_name}': {e}")

    token, message = provider.login()
    if not token:
        raise RuntimeError(f"Login failed: {message}")
    save_token(token, provider_name)   # ← saves both token AND which provider issued it

    # Local provider issues HS256 JWTs — verify_token decodes them locally.
    # Browser providers verify via the provider's /userinfo endpoint.
    claims = provider.verify_token(token)
    if not claims:
        raise RuntimeError("Token was issued but could not be verified.")
    return token, claims


def _get_token_and_claims() -> tuple[str, dict]:
    """
    Load the existing token and verify it using the provider that originally
    issued it (saved in the session file alongside the token).

    Uses an in-memory cache to avoid repeated /userinfo network calls.
    The cache TTL is 5 minutes; after that, the token is re-verified once.

    Returns (token, claims) or raises ValueError if no active session.
    """
    token         = load_token()          # raises ValueError if missing
    provider_name = load_provider()       # which SSO provider issued this token

    if not provider_name:
        raise ValueError(
            "Session is missing provider information.\n"
            "Please log out and log in again."
        )

    # ── Fast path: serve from in-memory cache ────────────────────────────────
    cache_key = hash(token)
    cached    = _CLAIMS_CACHE.get(cache_key)
    if cached and time.time() < cached["expires_at"]:
        return token, cached["claims"]

    # ── Slow path: verify via SSO provider /userinfo (network call) ──────────
    provider = get_provider(provider_name)
    claims   = provider.verify_token(token)
    if not claims:
        _CLAIMS_CACHE.pop(cache_key, None)   # evict stale entry if present
        raise ValueError("Token expired or invalid. Please log in again.")

    # Store result in cache
    _CLAIMS_CACHE[cache_key] = {
        "claims":     claims,
        "expires_at": time.time() + _CLAIMS_CACHE_TTL,
    }
    return token, claims


def _require_auth() -> tuple[str, str]:
    """
    Global authentication check to be called by all protected tools.
    Validates token and claims, and returns (email, role).
    Raises ValueError with a clear instruction if unauthenticated.
    """
    try:
        token, claims = _get_token_and_claims()
        email, role = _resolve_role(claims)
        return email, role
    except ValueError:
        raise ValueError(
            "ERROR: UNAUTHENTICATED\n\n"
            "The mock session is unauthenticated. To proceed, please use the `sso_login` tool "
            "with one of the supported providers ('auth0', 'okta', 'local', or 'azure').\n"
            "Note: This is a mock environment, no actual credentials are required."
        )


def _load_roles() -> dict:
    """Load the roles.json mapping."""
    try:
        with open(ROLES_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def _resolve_role(claims: dict) -> tuple[str, str]:
    """
    Resolve the user's role from roles.json using their email.

    For Auth0 tokens  → uses the 'email' claim from /userinfo
    For local tokens  → uses the 'email' claim set by LocalProvider

    Returns (email, role).
    Raises ValueError if user is not in roles.json.
    """
    email = (
        claims.get("email")
        or claims.get("sub")       # Auth0 fallback
        or claims.get("user", "") + "@local.dev"  # local provider fallback
    )

    roles = _load_roles()
    profile = roles.get(email)

    if not profile:
        raise ValueError(
            f"User '{email}' is authenticated but not found in the authorization registry.\n"
            f"Ask your admin to add your email to authorization/roles.json."
        )
    return email, profile["role"]


def _authorize(action: str, resource_id: str, resource_category: str, env: str, vendor: str) -> tuple[bool, str, str]:
    """
    Full authorization check — runs in-process (no external server needed).

    Steps:
      1. Load + verify token — raises ValueError if not logged in
      2. Resolve role from roles.json
      3. RBAC check (role → allowed actions)
      4. ABAC check (environment, time, vendor rules)

    Returns (allowed: bool, reason: str, identity: str)
    Raises ValueError if the user is not authenticated (caller handles asking them to login).
    """
    email, role = _require_auth()

    payload  = TokenPayload(
        user_id=email.split("@")[0],
        user_email=email,
        role=role,
        permissions=[]
    )
    resource = Resource(id=resource_id, env=env, vendor=vendor)
    context  = Context(
        time=datetime.now().strftime("%H:%M"),
        location="mcp-client"
    )

    # RBAC
    rbac = RBACEngine()
    rbac_pass, rbac_reason = rbac.evaluate(payload, action, resource_category)
    if not rbac_pass:
        return False, f"Access Denied (Role check): {rbac_reason}", email

    # ABAC
    abac = ABACEngine()
    abac_pass, abac_reason = abac.evaluate(payload, action, resource, context)
    if not abac_pass:
        return False, f"Access Denied (Policy check): {abac_reason}", email

    return True, "Authorized", email

# ─────────────────────────────────────────────────────────────────────────────
# Tool 1 — SSO Login (manual trigger)
# ─────────────────────────────────────────────────────────────────────────────

@mcp.tool()
def sso_login(provider: str) -> str:
    """
    Login via a browser-based SSO provider chosen by the user.

    Args:
        provider : The SSO provider to use.
                   Must be one of: auth0, okta, azure.
                   Always ask the user which provider they want BEFORE calling this.

    All providers open a browser window — no credentials are ever sent through the chat.
    The user logs in directly on the provider's secure login page.
    """
    provider = provider.strip().lower()

    if provider not in AVAILABLE_PROVIDERS:
        names = ", ".join(AVAILABLE_PROVIDERS.keys())
        return (
            f"❌ Unknown provider '{provider}'.\n"
            f"Available browser-based SSO providers: {names}"
        )

    try:
        token, claims = _trigger_login(provider)
    except RuntimeError as e:
        return f"❌ Login failed: {e}"

    try:
        email, role = _resolve_role(claims)
        role_info = f"\nRole     : {role}"
    except ValueError as e:
        role_info = f"\n⚠️  Warning: {e}"

    identity = (
        claims.get("email")
        or claims.get("nickname")
        or claims.get("sub")
        or claims.get("user", "Unknown")
    )
    return (
        f"✅ Login Successful via {provider.upper()}!\n"
        f"Identity : {identity}"
        f"{role_info}\n\n"
        f"Session saved. You can now use server management tools."
    )

# ─────────────────────────────────────────────────────────────────────────────
# Tool 2 — Check Access
# ─────────────────────────────────────────────────────────────────────────────

@mcp.tool()
def check_access() -> str:
    """
    Show who is currently logged in, their role, and what they are allowed to do.
    Automatically prompts login if no session exists.
    """
    try:
        email, role = _require_auth()
        token, claims = _get_token_and_claims()
        active_provider = load_provider() or PROVIDER
    except ValueError as e:
        return str(e)
    except RuntimeError as e:
        return f"❌ {e}"

    identity = claims.get("email") or claims.get("nickname") or claims.get("sub", "Unknown")

    # Build permissions summary from RBAC matrix
    rbac        = RBACEngine()
    role_rules  = rbac.matrix.get(role, {})
    if "*" in role_rules:
        resource_summary = "ALL resources"
        action_summary   = ", ".join(role_rules["*"])
    else:
        parts = []
        for res, actions in role_rules.items():
            parts.append(f"{res}: [{', '.join(actions)}]")
        resource_summary = "specific resources only"
        action_summary   = "\n             ".join(parts) if parts else "none"

    return (
        f"✅ Active Session\n"
        f"Provider   : {active_provider.upper()}\n"
        f"Identity   : {identity}\n"
        f"Role       : {role}\n"
        f"Scope      : {resource_summary}\n"
        f"Permissions: {action_summary}\n\n"
        f"Note: Additional ABAC policies (environment, time) may further restrict access."
    )

# ─────────────────────────────────────────────────────────────────────────────
# Tool 3 — Logout
# ─────────────────────────────────────────────────────────────────────────────

@mcp.tool()
def logout() -> str:
    """
    End the current session and clear the saved token.
    You will need to login again to use server management tools.
    """
    try:
        _require_auth()
    except ValueError as e:
        return str(e)
    except Exception as e:
        return f"❌ {e}"

    # Simply clear token cache to logout locally
    clear_token()
    _CLAIMS_CACHE.clear()   # ← evict in-memory claims cache on logout
    return "✅ Logged out. Session cleared."


# ─────────────────────────────────────────────────────────────────────────────
# Tools 5-7 — OASF Agent Microservices
# ─────────────────────────────────────────────────────────────────────────────

@mcp.tool()
async def manage_infrastructure_resource(query: str) -> str:
    """
    USE THIS TOOL to manage or check the status of ANY resource (cloud, network, storage, server, onprem).
    You can also use this tool to LIST resources by category (e.g., query='{"action": "LIST", "identifier": "gateways"}').
    The backend CMDB and Capability Registry will automatically route it to the correct agent.
    """
    return await _execute_agent_command(
        query=query,
        env="dev",
        agent_type="unknown",
        provider_or_protocol="unknown",
        resource_type="unknown",
    )


async def _execute_agent_command(
    query: str,
    env: str,
    agent_type: str,
    provider_or_protocol: str,
    resource_type: str,
) -> str:
    """Shared pipeline for the three OASF agent tools."""
    import asyncio

    # ── Step 1: Authentication ────────────────────────────────────────────────
    try:
        email, role = _require_auth()
    except ValueError as e:
        return str(e)

    import json
    
    tasks = None
    try:
        # If the LLM passes a raw JSON string like '{"identifier": "gl-ns-008", ...}'
        parsed = json.loads(query)
        if isinstance(parsed, dict) and "identifier" in parsed:
            tasks = [Task(
                action=parsed.get("action", "STATUS"),
                category=parsed.get("category", "Operational"),
                identifier=parsed.get("identifier")
            )]
    except json.JSONDecodeError:
        pass

    if not tasks:
        tasks = TaskPlanner.decompose_instruction(query)
        if not tasks:
            parsed = QueryAgent.parse_query(query)
            tasks = [Task(
                action=parsed.get("action", "STATUS"),
                category=parsed.get("category", "Operational"),
                identifier=parsed.get("identifier") or query.strip()
            )]

    task = tasks[0]
    action = task.action
    identifier = task.identifier
    if identifier.lower().startswith("of "):
        identifier = identifier[3:].strip()


    # ── Step 2.5: Resource Resolver Validation & CMDB Check ───────────────────

    is_list = action == "LIST"
    if is_list:
        ident_lower = identifier.lower().strip()
        if "pool" in ident_lower:
            normalized_category = "storage-pools"
            resource_type = "storage_pool"
            provider_or_protocol = "mock_storage"
        elif "volume" in ident_lower:
            normalized_category = "storage-volumes"
            resource_type = "volume"
            provider_or_protocol = "mock_storage"
        elif "system" in ident_lower or "array" in ident_lower:
            normalized_category = "storage-systems"
            resource_type = "storage_system"
            provider_or_protocol = "mock_storage"
        elif "server" in ident_lower:
            normalized_category = "server-hardware"
            resource_type = "server"
            provider_or_protocol = "mock_server"
        elif "gateway" in ident_lower or "router" in ident_lower:
            normalized_category = "gateways"
            resource_type = "gateway"
            provider_or_protocol = "mock_network"
        elif "switch" in ident_lower:
            normalized_category = "switches"
            resource_type = "switch"
            provider_or_protocol = "mock_network"
        elif "ap" in ident_lower or "access point" in ident_lower:
            normalized_category = "aps"
            resource_type = "access_point"
            provider_or_protocol = "mock_network"
        else:
            normalized_category = "unknown"
            resource_type = "unknown"
            provider_or_protocol = "unknown"

        # Step 3: Authorization (RBAC + ABAC)
        try:
            allowed, reason, identity = _authorize(
                "read", identifier or "all", normalized_category, env, "HPE"
            )
        except (RuntimeError, ValueError) as e:
            return f"Authorization error for '{identifier}': {e}"

        if not allowed:
            return f"Access Denied for {email} (Role: {role}) on '{identifier}'\nReason: {reason}"

        # If authorized, query Postgres CMDB
        try:
            import psycopg2
            conn = psycopg2.connect(dbname="hpe_agentic_ai", user="postgres", password="Mithles", host="localhost")
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT serial_number, ip_address, device_type, management_source FROM devices WHERE device_type = %s",
                    (resource_type,)
                )
                rows = cur.fetchall()
            conn.close()
            
            if not rows:
                return f"No {normalized_category.replace('-', ' ')} found in the CMDB registry."
                
            lines = [
                f"📋 List of {normalized_category.replace('-', ' ')} in CMDB registry:",
                f"Total: {len(rows)}",
                ""
            ]
            for r in rows:
                lines.append(f"• {r[0]} (IP: {r[1]}, Provider: {r[3]})")
            return "\n".join(lines)
        except Exception as db_err:
            return f"Error querying CMDB registry: {db_err}"

    # ── Step 2.5: Verify CMDB Resource Existence ─────────────────────────────
    device = None
    api_path = ""
    resolution = None
    try:
        resolution = _resolver.resolve({
            "identifier": identifier,
            "action": action,
            "category": task.category
        })
        device = resolution.device
        api_path = resolution.api_endpoint
    except Exception as e:
        print(f"Resolver error for {identifier}: {e}")
        pass

    # Conversational memory fallback
    if not device and identifier.lower() in {"", "it", "this", "that", "the device", "the resource"}:
        try:
            last_target = recall(SESSION_ID, "last_target_id")
            if last_target:
                resolution = _resolver.resolve({
                    "identifier": last_target,
                    "action": action,
                    "category": task.category
                })
                device = resolution.device
                api_path = resolution.api_endpoint
                if device:
                    identifier = last_target
        except Exception:
            pass

    is_creation = action in {"CREATE", "ALLOCATE"}

    if is_creation:
        # Clear cache for this identifier to ensure we don't use stale cache entries
        try:
            _cache._client.delete(f"resolver:sn:{identifier.lower()}")
            _cache._client.delete(f"resolver:ip:{identifier.lower()}")
            _cache._client.delete(f"resolver:fqdn:{identifier.lower()}")
        except Exception as e:
            print(f"Warning: Failed to invalidate cache on creation: {e}")
        # Re-resolve with empty cache so device is loaded properly from DB if it exists
        try:
            resolution = _resolver.resolve({
                "identifier": identifier,
                "action": action,
                "category": "Operational"
            })
            device = resolution.device
            api_path = resolution.api_endpoint
        except Exception:
            device = None
            api_path = ""

    if not device and not is_creation:
        return f"❌ Resource '{identifier}' not found in the CMDB registry. Unable to route task."


    # ── Step 3: Authorization (RBAC + ABAC) ───────────────────────────────────
    action_verb_map = {
        "ON": "execute", "OFF": "execute", "RESET": "execute",
        "COLD_BOOT": "execute", "STATUS": "read",
        "CREATE": "create", "ALLOCATE": "create",
        "DEALLOCATE": "delete", "DELETE": "delete",
        "RESCAN": "read", "RELOAD": "execute",
        "FAILOVER": "execute", "POLICY_SYNC": "execute",
    }
    rbac_action = action_verb_map.get(action, "execute")
    resource_id_for_authz = identifier or "unknown"

    try:
        allowed, reason, identity = _authorize(
            rbac_action, resource_id_for_authz, resource_type, env, "HPE"
        )
    except (RuntimeError, ValueError) as e:
        return f"Authorization error for '{identifier}': {e}"

    if not allowed:
        return f"Access Denied for {email} (Role: {role}) on '{identifier}'\nReason: {reason}"

    # ── Step 3.5: Vendor Synthesizer ──────────────────────────────────────────
    from synthesizer import VendorSynthesizer
    try:
        # Pass the task and resolution to the synthesizer
        batches = VendorSynthesizer.synthesize_batches([(task, resolution)])
        if batches:
            batch = list(batches.values())[0]
            # Verify the batch grouped it correctly
            provider_or_protocol = batch.management_source
    except Exception as e:
        print(f"Vendor Synthesizer warning: {e}")

    # Fallback routing variables for creation
    payload_to_dispatch = {}
    if is_creation:
        if device:
            source_device_id_uuid = device.source_device_id or str(uuid.uuid4())
            provider_or_protocol = device.management_source or provider_or_protocol
            resource_type = device.device_type or resource_type
            
            # Resolve agent_type based on provider_or_protocol
            if provider_or_protocol == "mock_storage":
                agent_type = "storage"
            elif provider_or_protocol in {"mock_server", "oneview"}:
                agent_type = "server"
            elif provider_or_protocol == "mock_network":
                agent_type = "network"
            elif provider_or_protocol == "mock_cloud":
                agent_type = "cloud"
        else:
            source_device_id_uuid = str(uuid.uuid4())
            query_lower = query.lower()
            if "storage" in query_lower or "volume" in query_lower or "pool" in query_lower or "array" in query_lower:
                agent_type = "storage"
                provider_or_protocol = "mock_storage"
                api_path = "/data-services/v1beta1/devices"
                if "volume" in query_lower:
                    resource_type = "volume"
                elif "pool" in query_lower:
                    resource_type = "storage_pool"
                else:
                    resource_type = "storage_system"
            elif "server" in query_lower or "compute" in query_lower or "hardware" in query_lower:
                agent_type = "server"
                provider_or_protocol = "mock_server"
                api_path = "/rest/server-hardware"
                resource_type = "server"
            elif "network" in query_lower or "switch" in query_lower or "vlan" in query_lower or "port" in query_lower:
                agent_type = "network"
                provider_or_protocol = "mock_network"
                api_path = "/network/v1/devices"
                resource_type = "switch"
            elif "cloud" in query_lower or "vm" in query_lower or "cluster" in query_lower:
                agent_type = "cloud"
                provider_or_protocol = "mock_cloud"
                api_path = "/api/v1/devices"
                resource_type = "virtual_machine"
            else:
                agent_type = "server"
                provider_or_protocol = "mock_server"
                api_path = "/rest/server-hardware"
                resource_type = "server"

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S+05:30")
        # Construct creation payload
        creation_payload = {
            "id": identifier,
            "serial_number": identifier,
            "name": identifier,
            "device_type": resource_type,
            "power_state": "ON",
            "health_status": "OK",
            "management_source": provider_or_protocol,
            "source_host": "mock-storage-manager.local" if provider_or_protocol == "mock_storage" else "mock-server-manager.local",
            "source_device_id": source_device_id_uuid,
            "fqdn": f"{identifier}.local",
            "last_seen": now_str,
            "created_at": now_str,
            "updated_at": now_str
        }
        if provider_or_protocol == "mock_storage":
            creation_payload["ip_address"] = "10.12.99.5"
            creation_payload["total_capacity_gb"] = 10000
            creation_payload["free_capacity_gb"] = 10000
        elif provider_or_protocol == "mock_server":
            creation_payload["ip_address"] = "10.11.99.5"
        elif provider_or_protocol == "mock_network":
            creation_payload["ip_address"] = "10.13.99.5"
        elif provider_or_protocol == "mock_cloud":
            creation_payload["ip_address"] = "10.14.99.5"

        payload_to_dispatch = creation_payload

        # Insert into Postgres CMDB
        try:
            import psycopg2
            conn = psycopg2.connect(dbname="hpe_agentic_ai", user="postgres", password="Mithles", host="localhost")
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO devices (
                        serial_number, ip_address, fqdn,
                        management_source, source_host, source_device_id,
                        device_type, last_seen, created_at, updated_at
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, NOW(), NOW(), NOW())
                    ON CONFLICT (serial_number) DO UPDATE SET
                        ip_address = EXCLUDED.ip_address,
                        fqdn = EXCLUDED.fqdn,
                        management_source = EXCLUDED.management_source,
                        source_host = EXCLUDED.source_host,
                        source_device_id = EXCLUDED.source_device_id,
                        device_type = EXCLUDED.device_type,
                        last_seen = NOW(),
                        created_at = COALESCE(devices.created_at, NOW()),
                        updated_at = NOW()
                    """,
                    (
                        identifier,
                        creation_payload.get("ip_address", "10.0.0.1"),
                        f"{identifier}.local",
                        provider_or_protocol,
                        creation_payload["source_host"],
                        source_device_id_uuid,
                        resource_type
                    )
                )
            conn.commit()
            conn.close()
            
            # Now try to resolve again so device object gets loaded
            try:
                resolution = _resolver.resolve({
                    "identifier": identifier,
                    "action": action,
                    "category": "Operational"
                })
                device = resolution.device
                api_path = resolution.api_endpoint
            except Exception:
                pass
        except Exception as db_err:
            print(f"Warning: Failed to insert created device into Postgres CMDB: {db_err}")

    # OVERRIDE the LLM's guessed provider with the actual CMDB source
    if device and device.management_source:
        provider_or_protocol = device.management_source
        
        # Override the LLM's guessed agent type based on the Capability Registry
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    "http://127.0.0.1:8020/agents/lookup",
                    params={
                        "resource_type": device.device_type or resource_type,
                        "provider": provider_or_protocol
                    },
                    timeout=5.0
                )
                if resp.is_success:
                    agent_record = resp.json()
                    agent_name = agent_record.get("name", "")
                    if agent_name.endswith("-agent"):
                        agent_type = agent_name[:-6]  # strip "-agent"
        except Exception as e:
            print(f"Warning: Failed to lookup agent in capability registry: {e}")


    # Use resolver-derived routing metadata, management source, and credentials ref.
    resolved_provider = provider_or_protocol
    resolved_credentials_ref = resolution.credential_ref


    if device:
        resource_type = device.device_type or resource_type

    # Normalize resource_type to match categories in rbac.py
    normalized_category = resource_type
    if device:
        dt = (device.device_type or "").lower().strip()
        src = (device.management_source or "").lower().strip()
        
        # Storage mappings
        if src in {"mock_storage", "storage"}:
            if dt in {"storage_system", "storage-system", "system"}:
                normalized_category = "storage-systems"
            elif dt in {"storage_pool", "storage-pool", "pool"}:
                normalized_category = "storage-pools"
            elif dt in {"volume", "volume_set", "volume-set", "snapshot", "filesystem"}:
                normalized_category = "storage-volumes"
            elif dt in {"storage_volume_template", "storage-volume-template", "storage-volume-templates"}:
                normalized_category = "storage-volume-templates"
            elif dt in {"fc_san", "fc-san", "fc-sans"}:
                normalized_category = "fc-sans"
            else:
                # Fallback: any other mock_storage device type (replication_group, etc.)
                normalized_category = "storage-systems"
        
        # Server mappings
        elif src in {"oneview", "mock_server", "coms", "compute_ops"}:
            if dt in {"server", "blade_server", "rack_server", "compute_node", "hypervisor", "server-hardware"}:
                normalized_category = "server-hardware"
            elif dt in {"server-profile", "server_profile", "server-profiles"}:
                normalized_category = "server-profiles"
            elif dt in {"server-profile-template", "server_profile_template", "server-profile-templates"}:
                normalized_category = "server-profile-templates"
            elif dt in {"enclosure", "enclosures"}:
                normalized_category = "enclosures"
            elif dt in {"rack", "racks"}:
                normalized_category = "racks"
            elif dt in {"power-device", "power-devices", "power_device"}:
                normalized_category = "power-devices"
                
        # Network mappings
        elif src in {"mock_network", "network"}:
            if dt in {"switch", "interconnect", "interconnects"}:
                normalized_category = "interconnects"
            elif dt in {"router", "firewall", "gateway"}:
                normalized_category = "interconnects"
            elif dt in {"ethernet-network", "ethernet-networks", "network"}:
                normalized_category = "ethernet-networks"
                
        # Cloud mappings
        elif src in {"mock_cloud", "cloud"}:
            normalized_category = "server-hardware"
    else:
        # Fallback normalization when device is None (creation flow)
        dt = (resource_type or "").lower().strip()
        src = (provider_or_protocol or "").lower().strip()
        if src == "mock_storage":
            if dt == "storage_system":
                normalized_category = "storage-systems"
            elif dt == "storage_pool":
                normalized_category = "storage-pools"
            elif dt == "volume":
                normalized_category = "storage-volumes"
        elif src == "mock_server":
            normalized_category = "server-hardware"
        elif src == "mock_network":
            normalized_category = "interconnects"
        elif src == "mock_cloud":
            normalized_category = "server-hardware"

    # ── Step 3: Authorization (RBAC + ABAC) ───────────────────────────────────
    action_verb_map = {
        "ON": "execute", "OFF": "execute", "RESET": "execute",
        "COLD_BOOT": "execute", "STATUS": "read",
        "CREATE": "create", "ALLOCATE": "create",
        "DEALLOCATE": "delete", "DELETE": "delete",
        "RESCAN": "read", "RELOAD": "execute",
        "FAILOVER": "execute", "POLICY_SYNC": "execute",
        "UPDATE": "update",
    }
    rbac_action = action_verb_map.get(action, "execute")
    resource_id_for_authz = identifier or "unknown"

    try:
        allowed, reason, identity = _authorize(
            rbac_action, resource_id_for_authz, normalized_category, env, "HPE"
        )
    except (RuntimeError, ValueError) as e:
        return f"Authorization error for '{identifier}': {e}"

    if not allowed:
        return f"Access Denied for {email} (Role: {role}) on '{identifier}'\nReason: {reason}"

    # ── Step 3: Resource Resolver Validation ──────────────────────────────────
    # Task Planner triggers Resource Resolver to query CMDB registry and lookup templates/routes.
    device = None
    api_path_step3 = ""
    resolution = None
    try:
        resolution = _resolver.resolve({
            "identifier": identifier,
            "action": action,
            "category": task.category
        })
        device = resolution.device
        api_path_step3 = resolution.api_endpoint
    except Exception:
        pass

    # Conversational memory fallback
    if not device and not is_creation:
        try:
            last_target = recall(SESSION_ID, "last_target_id")
            if last_target:
                resolution = _resolver.resolve({
                    "identifier": last_target,
                    "action": action,
                    "category": task.category
                })
                device = resolution.device
                api_path_step3 = resolution.api_endpoint
                if device:
                    identifier = last_target
        except Exception:
            pass

    if not device and not is_creation:
        return f"❌ Resource '{identifier}' not found in the CMDB registry. Unable to route task."

    # Use resolver-derived routing metadata, management source, and credentials ref.
    if device:
        resolved_provider = device.management_source
        resolved_credentials_ref = resolution.credential_ref
        if api_path_step3:
            api_path = api_path_step3
    else:
        resolved_provider = provider_or_protocol
        resolved_credentials_ref = None

    if is_creation or resolved_provider in {"mock_storage", "mock_network", "mock_server", "mock_cloud", "oneview"}:
        if resolved_provider == "mock_storage":
            api_path = "/data-services/v1beta1/devices/{id}" if not is_creation else "/data-services/v1beta1/devices"
        elif resolved_provider in {"mock_server", "oneview"}:
            api_path = "/rest/server-hardware/{id}" if not is_creation else "/rest/server-hardware"
        elif resolved_provider == "mock_network":
            api_path = "/network/v1/devices/{id}" if not is_creation else "/network/v1/devices"
        elif resolved_provider == "mock_cloud":
            api_path = "/api/v1/devices/{id}" if not is_creation else "/api/v1/devices"

    # Agent task payload mapping
    agent_task_action = action
    if action == "STATUS":
        if normalized_category in {"storage-systems", "storage-pools", "storage-volumes", "fc-sans"}:
            agent_task_action = "health_check" if (resource_type or "").lower() == "snapshot" else "fetch_capacity_and_performance"
        else:
            agent_task_action = "fetch_metrics"

    # ── UPDATE (PATCH) — handled directly via mock REST API ────────────────
    if action == "UPDATE":
        from query_agent import QueryAgent as _QA  # RESOLVER_DIR already in sys.path
        update_payload = _QA.parse_update_payload(query)
        if not update_payload:
            return (
                f"Could not extract attribute/value from query.\n"
                f"Try: \"change the temperature of <device> to <value>\"\n"
                f"  or: \"set health_status of <device> to DEGRADED\""
            )

        attribute = update_payload["attribute"]
        value     = update_payload["value"]

        # Route to the correct mock server based on device source
        _MOCK_URLS = {
            "mock_storage": os.getenv("MOCK_STORAGE_URL", "http://127.0.0.1:8004"),
            "mock_server":  os.getenv("MOCK_SERVER_URL",  "http://127.0.0.1:8000"),
            "mock_network": os.getenv("MOCK_NETWORK_URL", "http://127.0.0.1:8002"),
            "mock_cloud":   os.getenv("MOCK_CLOUD_URL",   "http://127.0.0.1:8003"),
            "oneview":      os.getenv("HPE_OV_URL",       "http://127.0.0.1:8000"),
        }

        if device and device.management_source in _MOCK_URLS:
            base_url = _MOCK_URLS[device.management_source]
            # Determine per-source PATCH path
            src = device.management_source
            if src == "mock_storage":
                patch_url = f"{base_url}/data-services/v1beta1/devices/{device.source_device_id or identifier}"
            elif src in {"mock_server", "oneview"}:
                patch_url = f"{base_url}/rest/server-hardware/{device.source_device_id or identifier}"
            elif src == "mock_network":
                patch_url = f"{base_url}/network/v1/devices/{device.source_device_id or identifier}"
            elif src == "mock_cloud":
                patch_url = f"{base_url}/api/v1/devices/{device.source_device_id or identifier}"
            else:
                patch_url = ""

            if patch_url:
                try:
                    async with httpx.AsyncClient() as _client:
                        patch_resp = await _client.patch(
                            patch_url,
                            json={attribute: value},
                            timeout=10.0,
                        )
                    if patch_resp.is_success:
                        updated = patch_resp.json()
                        return (
                            f"Update successful\n"
                            f"User       : {email} (Role: {role})\n"
                            f"Device     : {identifier}\n"
                            f"Provider   : {device.management_source}\n"
                            f"Attribute  : {attribute}\n"
                            f"New Value  : {value}\n"
                            f"Confirmed  : {updated.get(attribute, value)}\n"
                        )
                    else:
                        return (
                            f"Update failed (HTTP {patch_resp.status_code})\n"
                            f"Device: {identifier} | Attribute: {attribute}\n"
                            f"Response: {patch_resp.text[:300]}"
                        )
                except Exception as patch_err:
                    return f"Update request failed: {patch_err}"
            else:
                return f"No PATCH URL configured for provider '{device.management_source}'."
        else:
            return (
                f"Device '{identifier}' not found in CMDB or provider not supported for updates.\n"
                f"Supported providers: {list(_MOCK_URLS.keys())}"
            )
    
    dispatch_params = {
        "api_path": api_path,
        "user_email": email
    } if api_path else {"user_email": email}

    if device:
        dispatch_params["serial_number"] = device.serial_number
        dispatch_params["management_source"] = device.management_source

    if resolution and hasattr(resolution, "http_method"):
        dispatch_params["http_method"] = resolution.http_method
    
    is_deletion = action in {"DELETE", "DEALLOCATE"}
    if is_deletion:
        dispatch_params["http_method"] = "DELETE"
        
    if payload_to_dispatch:
        dispatch_params["payload"] = payload_to_dispatch
        dispatch_params["http_method"] = "POST"
        
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        None,
        lambda: _dispatcher.dispatch(
            agent_type=agent_type,
            query_action=agent_task_action,
            resource_type=resource_type,
            resource_id=identifier,
            provider_or_protocol=resolved_provider,
            parameters=dispatch_params,
            credentials_ref=resolved_credentials_ref,
        ),
    )

    # ── Step 5: Format response ───────────────────────────────────────────────
    status       = result.get("status", "unknown")
    status_level = result.get("status_level", "")
    errors       = result.get("errors", [])
    insights     = result.get("insights", [])
    metrics      = result.get("metrics", {})
    actions_taken = result.get("actions_taken", [])

    if status == "success" and not errors and is_deletion:
        # Delete from PostgreSQL CMDB
        try:
            import psycopg2
            conn = psycopg2.connect(dbname="postgres", user="postgres", password="mithles", host="localhost")
            with conn.cursor() as cur:
                cur.execute("DELETE FROM devices WHERE serial_number = %s", (identifier,))
            conn.commit()
            conn.close()
        except Exception as db_err:
            print(f"Warning: Failed to delete device from PostgreSQL: {db_err}")

        # Purge Redis Cache
        try:
            _cache._client.delete(f"resolver:sn:{identifier.lower()}")
            _cache._client.delete(f"resolver:ip:{identifier.lower()}")
            _cache._client.delete(f"resolver:fqdn:{identifier.lower()}")
            if device:
                _cache.invalidate_device(device)
        except Exception as cache_err:
            print(f"Warning: Failed to purge Redis cache: {cache_err}")

    if status == "failed" or errors:
        error_text = "\n  ".join(errors) if errors else "Unknown error"
        return (
            f"Agent command failed\n"
            f"User       : {email} (Role: {role})\n"
            f"Agent      : {agent_type}-agent\n"
            f"Resource   : {resource_type}/{identifier}\n"
            f"Provider   : {provider_or_protocol}\n"
            f"Action     : {action}\n"
            f"Errors:\n  {error_text}\n"
            f"Tip: ensure the {agent_type}-agent is running "
            f"(python agents/{agent_type}_agent/main.py)"
        )

    norm_data = result.get("normalized_data", {})
    # Unpack power state or capacity metrics depending on agent type
    power_state = norm_data.get("power_state") or (result.get("metrics", {})).get("power_state") or "N/A"
    health_status = status_level or norm_data.get("health_status") or "N/A"

    lines = [
        f"Agent command succeeded",
        f"User         : {email} (Role: {role})",
        f"Agent        : {agent_type}-agent",
        f"Resource     : {resource_type}/{identifier}",
        f"Power State  : {power_state.upper()}",
        f"Health Status: {health_status.upper()}",
        f"Provider     : {provider_or_protocol}",
        f"Action       : {action}",
        f"Status       : {status}",
    ]
    if insights:
        lines.append("Insights:")
        lines.extend(f"  • {i}" for i in insights)
    if actions_taken:
        lines.append("Actions taken:")
        lines.extend(f"  • {a}" for a in actions_taken)
    if metrics:
        lines.append(f"Metrics:\n{json.dumps(metrics, indent=2)}")

    try:
        remember(SESSION_ID, "last_action_time", datetime.utcnow().isoformat() + "Z")
        remember(SESSION_ID, "last_target_id", identifier)
        remember(SESSION_ID, "last_action_executed", action)
        remember(SESSION_ID, "last_action_status", "success")
        if insights:
            remember(SESSION_ID, "last_execution_insights", insights)
    except Exception as e:
        print(f"⚠️ Failed to save execution context to memory: {e}", file=sys.stderr)

    return "\n".join(lines)


@mcp.tool()
def mcp_list_sessions() -> str:
    """
    List all active session IDs in the Redis memory database (for debugging).
    """
    try:
        _require_auth()
        sessions = list_sessions()
        return f"📋 Active Redis sessions:\n" + json.dumps(sessions, indent=2)
    except ValueError as e:
        return str(e)
    except Exception as e:
        return f"❌ Failed to list sessions: {e}"

# ─────────────────────────────────────────────────────────────────────────────
# Entry Point
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    mcp.run()
