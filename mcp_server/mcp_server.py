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

import httpx
import time
import psycopg2
import uuid
from mcp.server.fastmcp import FastMCP

# ─────────────────────────────────────────────────────────────────────────────
# Path Setup — add authentication/, authorization/, resource_resolver/
# ─────────────────────────────────────────────────────────────────────────────

BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
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



# New Redis Memory Store
try:
    from mem_store.store import SESSION_ID, remember, recall, list_sessions
except ImportError as e:
    print(f"⚠️ Failed to import mem_store: {e}", file=sys.stderr)

# Authentication imports
from authentication import get_provider, PROVIDER       # noqa: E402
from token_store import save_token, load_token, load_provider, clear_token  # noqa: E402

# Authorization engine imports (runs in-process, no separate server needed)
from rbac   import RBACEngine   # noqa: E402
from abac   import ABACEngine   # noqa: E402
from models import TokenPayload, Resource, Context  # noqa: E402

# Resource Resolver imports
from resolver    import ResourceResolver   # noqa: E402
from cache       import ResourceCache     # noqa: E402
from db_loader   import load_registry_from_db  # noqa: E402
from query_agent import QueryAgent        # noqa: E402
from planner     import TaskPlanner       # noqa: E402
from errors      import ResolverError     # noqa: E402
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

    ── SERVER TOOLS (on-premises) ────────────────────────────────────────────
    manage_server_resource(query, provider, resource_type, env)
      Manage a bare-metal server (server, bmc, sensor, firmware, event_log) via the Server Agent.
      provider: 'redfish' | 'ipmi' | 'ilo' | 'mock'
      resource_type: 'server' | 'bmc' | 'sensor' | 'firmware' | 'event_log'

    ── OASF AGENT TOOLS ─────────────────────────────────────────────────────
    manage_cloud_resource(query, provider, resource_type)
      Manage cloud VMs/containers. provider: aws | azure | gcp | mock
      resource_type: vm | container | function

    manage_network_resource(query, protocol, resource_type)
      Manage network devices. protocol: snmp | netconf | rest | mock
      resource_type: switch | router | interface

    manage_storage_resource(query, provider, resource_type)
      Manage storage. provider: dscc | nas | s3 | mock
      resource_type: volume | array | pool | bucket

    ── FULL PIPELINE (all tools) ─────────────────────────────────────────────
      1. Authenticates the user
      2. Parses the natural language command
      3. Checks RBAC + ABAC permissions
      4. Dispatches to the correct backend / agent
      5. Returns the result

    ── AUTHENTICATION (BROWSER ONLY — no credentials in chat) ──────────────────
    All login flows open a secure browser window. Credentials NEVER pass through chat.

    CRITICAL LOGIN RULES (Follow strictly):
    1. If the user is not logged in, reply with EXACTLY:
       "You are not logged in. Please choose an SSO provider:
       • [auth0](https://auth0.com) — Auth0 SSO Login
       • [okta](https://okta.com) — Okta SSO Login
       • [azure](https://azure.microsoft.com) — Azure AD SSO Login

       Reply with your choice: auth0, okta, or azure."

    2. STOP. Wait for the user to reply with their choice.
    3. Once the user replies, call `sso_login(provider="<their choice>")`.
    4. NEVER ask for a username or password in the chat.
    5. NEVER auto-select a provider.

    CRITICAL LOGOUT RULES:
    If the user asks to logout or end the session, you MUST execute the `logout()` tool.

    ── CRITICAL BEHAVIOURAL RULES (STRICT) ─────────────────────────────────────
    1. ZERO HALLUCINATION: You MUST ONLY reply using the data returned by the tools.
       If a tool returns an error, "Not found", or "Task resolution failed", you must report that failure verbatim.
       NEVER make up or assume any status, configuration, metrics, or details for any resource.
    2. FORCE SSO: If the tool returns "Not authenticated" or "Not logged in", you MUST NOT perform any actions or show any resource information. Force the user to log in first.
    3. NO ACCESS BYPASS: If a resource is not found in the CMDB database (resolution fails), you must tell the user that the resource is not registered in the system. Do not guess its state.
    4. NEVER REFUSE: When asked for the status or details of a resource (e.g. WAN-R08-10367, servers, etc.), you MUST use the appropriate manage_* tool (e.g., manage_network_resource). DO NOT say "I don't have access to internal systems". You DO have access through these tools!
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
    try:
        token, claims = _get_token_and_claims()
    except ValueError:
        raise ValueError(
            "You are not logged in. "
            "Please choose a provider to login with before performing any server operations."
        )

    email, role   = _resolve_role(claims)

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
        token, claims = _get_token_and_claims()
        email, role   = _resolve_role(claims)
        active_provider = load_provider() or PROVIDER
    except (RuntimeError, ValueError) as e:
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
    clear_token()
    _CLAIMS_CACHE.clear()   # ← also evict in-memory claims cache on logout
    return f"✅ Logged out. Session cleared."


# ─────────────────────────────────────────────────────────────────────────────
# Tools 5-7 — OASF Agent Microservices
# ─────────────────────────────────────────────────────────────────────────────

@mcp.tool()
async def manage_cloud_resource(
    query: str,
    provider: str = "mock",
    resource_type: str = "vm",
    env: str = "dev",
) -> str:
    """
    USE THIS TOOL to manage or check the status of any cloud resource (VM, container, function).
    If the user asks for the status of a cloud device, you MUST use this tool.
    provider: 'aws' | 'azure' | 'gcp' | 'mock'
    resource_type: 'vm' | 'container' | 'function'
    """
    return await _execute_agent_command(
        query=query,
        env=env,
        agent_type="cloud",
        provider_or_protocol=provider,
        resource_type=resource_type,
    )


@mcp.tool()
async def manage_network_resource(
    query: str,
    protocol: str = "mock",
    resource_type: str = "switch",
    env: str = "dev",
) -> str:
    """
    USE THIS TOOL to manage or check the status of any network device (switch, router, interface, WAN devices).
    If the user asks for the status of a router or network equipment (e.g., wan-r08-10367), you MUST use this tool.
    protocol: 'snmp' | 'netconf' | 'rest' | 'mock'
    resource_type: 'switch' | 'router' | 'interface'
    """
    return await _execute_agent_command(
        query=query,
        env=env,
        agent_type="network",
        provider_or_protocol=protocol,
        resource_type=resource_type,
    )


@mcp.tool()
async def manage_storage_resource(
    query: str,
    provider: str = "mock",
    resource_type: str = "volume",
    env: str = "dev",
) -> str:
    """
    USE THIS TOOL to manage or check the status of any storage resource (volume, array, pool, bucket).
    If the user asks for the status of a storage device, you MUST use this tool.
    provider: 'dscc' | 'nas' | 's3' | 'mock'
    resource_type: 'volume' | 'array' | 'pool' | 'bucket'
    """
    return await _execute_agent_command(
        query=query,
        env=env,
        agent_type="storage",
        provider_or_protocol=provider,
        resource_type=resource_type,
    )


@mcp.tool()
async def manage_server_resource(
    query: str,
    provider: str = "mock",
    resource_type: str = "server",
    env: str = "dev",
) -> str:
    """
    USE THIS TOOL to manage or check the status of any bare-metal server (server, bmc, sensor, firmware).
    If the user asks for the status of a server or physical hardware, you MUST use this tool.
    provider: 'redfish' | 'ipmi' | 'ilo' | 'mock'
    resource_type: 'server' | 'bmc' | 'sensor' | 'firmware' | 'event_log'
    """
    return await _execute_agent_command(
        query=query,
        env=env,
        agent_type="server",
        provider_or_protocol=provider,
        resource_type=resource_type,
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
        token, claims = _get_token_and_claims()
        email, role   = _resolve_role(claims)
    except ValueError:
        return (
            "ERROR: UNAUTHENTICATED\n\n"
            "CRITICAL INSTRUCTION FOR THE AGENT:\n"
            "DO NOT call the `sso_login` tool yet! You MUST stop and ask the user which provider they want to use.\n"
            "Relay this exact message to the user:\n\n"
            "\"You are not logged in. Please choose an SSO provider:\n"
            "• [auth0](https://auth0.com) — Auth0 SSO Login\n"
            "• [okta](https://okta.com) — Okta SSO Login\n"
            "• [azure](https://azure.microsoft.com) — Azure AD SSO Login\n\n"
            "Reply with your choice: auth0, okta, or azure.\"\n\n"
            "Wait for the user's reply before calling sso_login."
        )

    # ── Step 2: Parse query with QueryAgent ───────────────────────────────────
    parsed   = QueryAgent.parse_query(query)
    action   = parsed.get("action", "STATUS")
    identifier = parsed.get("identifier") or query.strip()
    if identifier.lower().startswith("of "):
        identifier = identifier[3:].strip()

    # ── Step 2.5: Verify CMDB Resource Existence ─────────────────────────────
    device = None
    api_path = ""
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

    # Conversational memory fallback
    if not device:
        try:
            last_target = recall(SESSION_ID, "last_target_id")
            if last_target:
                resolution = _resolver.resolve({
                    "identifier": last_target,
                    "action": action,
                    "category": "Operational"
                })
                device = resolution.device
                api_path = resolution.api_endpoint
                if device:
                    identifier = last_target
        except Exception:
            pass

    if not device:
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

    # ── Step 4: Dispatch to OASF Agent microservice ───────────────────────────
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        None,
        lambda: _dispatcher.dispatch(
            agent_type=agent_type,
            query_action=action,
            resource_type=resource_type,
            resource_id=identifier,
            provider_or_protocol=provider_or_protocol,
            parameters={"api_path": api_path} if api_path else None,
        ),
    )

    # ── Step 5: Format response ───────────────────────────────────────────────
    status       = result.get("status", "unknown")
    status_level = result.get("status_level", "")
    errors       = result.get("errors", [])
    insights     = result.get("insights", [])
    metrics      = result.get("metrics", {})
    actions_taken = result.get("actions_taken", [])

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
        sessions = list_sessions()
        return f"📋 Active Redis sessions:\n" + json.dumps(sessions, indent=2)
    except Exception as e:
        return f"❌ Failed to list sessions: {e}"

# ─────────────────────────────────────────────────────────────────────────────
# Entry Point
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    mcp.run()
