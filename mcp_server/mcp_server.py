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
from mcp.server.fastmcp import FastMCP

# ─────────────────────────────────────────────────────────────────────────────
# Path Setup — add authentication/, authorization/, resource_resolver/
# ─────────────────────────────────────────────────────────────────────────────

BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
AUTH_DIR     = os.path.normpath(os.path.join(BASE_DIR, "..", "authentication"))
AUTHZ_DIR    = os.path.normpath(os.path.join(BASE_DIR, "..", "authorization"))
RESOLVER_DIR = os.path.normpath(os.path.join(BASE_DIR, "..", "resource_resolver"))

sys.path.insert(0, AUTH_DIR)
sys.path.insert(0, AUTHZ_DIR)
sys.path.insert(0, RESOLVER_DIR)

# Authentication imports
from __init__    import get_provider, PROVIDER       # noqa: E402
from token_store import save_token, load_token, load_provider, clear_token  # noqa: E402

# Authorization engine imports (runs in-process, no separate server needed)
from rbac   import RBACEngine   # noqa: E402
from abac   import ABACEngine   # noqa: E402
from models import TokenPayload, Resource, Context  # noqa: E402

# Resource Resolver imports
from resolver    import ResourceResolver   # noqa: E402
from registry    import ResourceRegistry  # noqa: E402
from cache       import ResourceCache     # noqa: E402
from sample_data import load_sample_registry  # noqa: E402
from errors      import ResolverError     # noqa: E402
from records     import Protocol          # noqa: E402

# Path to roles.json (the role mapping file you can freely edit)
ROLES_FILE = os.path.join(AUTHZ_DIR, "roles.json")

# ── In-memory token claims cache (avoids repeated /userinfo network calls) ────
# Structure: {token_hash: {"claims": {...}, "expires_at": float}}
_CLAIMS_CACHE: dict = {}
_CLAIMS_CACHE_TTL = 300  # seconds — re-verify every 5 minutes max

# Mock server — mirrors the real HPE OneView REST API
HARDWARE_BACKEND_URL = "http://127.0.0.1:8000"

# ── Resolver singletons (built once at startup) ───────────────────────────────
_registry = load_sample_registry()
_cache    = ResourceCache(ttl=300)
_resolver = ResourceResolver(registry=_registry, cache=_cache)

# ─────────────────────────────────────────────────────────────────────────────
# MCP Server
# ─────────────────────────────────────────────────────────────────────────────

# Available SSO providers — ALL use browser-based PKCE (no credentials in chat).
AVAILABLE_PROVIDERS = {
    "local" : "Local Dev  ✅ Ready         (automated demo)",
    "auth0" : "Auth0      ✅ Ready         (browser login via Auth0)",
    "okta"  : "Okta       🔲 Needs config  (fill in OKTA_DOMAIN + OKTA_CLIENT_ID in okta_provider.py)",
    "azure" : "Azure AD   🔲 Needs config  (fill in AZURE_TENANT_ID + AZURE_CLIENT_ID in azure_provider.py)",
}

PROVIDER_LIST = "\n".join(
    f"  • {k} — {v}" for k, v in AVAILABLE_PROVIDERS.items()
)

mcp = FastMCP(
    "HPE-Integrated-MCP",
    instructions=f"""
    You are managing HPE physical servers via MCP.

    ── PRIMARY TOOLS ────────────────────────────────────────────────────────────
    For hardware commands on OneView servers, use: manage_oneview_server(query="<user request>")
    For hardware commands on Compute Ops (CoM) servers, use: manage_comops_server(query="<user request>")
    
    Both tools handle the full pipeline automatically:
      1. Authenticates the user
      2. Resolves the natural language command to the correct server + API
      3. Checks role-based permissions (RBAC + ABAC)
      4. Executes on the respective mock server (OneView or CoM)
      5. Returns the result

    Examples:
      manage_oneview_server(query="turn on OV1-RackServer-001")
      manage_comops_server(query="power on CoM-CloudNode-005")
      manage_oneview_server(query="list all servers")

    ── AUTHENTICATION (BROWSER ONLY — no credentials in chat) ──────────────────
    All login flows open a secure browser window. Credentials NEVER pass through chat.

    CRITICAL LOGIN RULES (Follow strictly):
    1. If the user is not logged in, reply with EXACTLY:
       "You are not logged in. Please choose an SSO provider:

{PROVIDER_LIST}

       Reply with: auth0, okta, or azure."

    2. STOP. Wait for the user to reply with their choice.
    3. Once the user replies, call `sso_login(provider="<their choice>")`.
    4. NEVER ask for a username or password in the chat.
    5. NEVER auto-select a provider.

    CRITICAL LOGOUT RULES:
    If the user asks to logout or end the session, you MUST execute the `logout()` tool. Do not just say you logged out without executing the tool.

    ── OTHER TOOLS ─────────────────────────────────────────────────────────────
    • sso_login(provider)      — Login via browser SSO
    • logout()                 — End the current session
    • check_access()           — Show identity, role, and permissions
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
# Tool 4 — Resolve & Execute  (THE MAIN FLOW TOOL)
# ─────────────────────────────────────────────────────────────────────────────

# ─────────────────────────────────────────────────────────────────────────────
# Tool 4 — Resolve & Execute  (THE MAIN FLOW TOOL)
# ─────────────────────────────────────────────────────────────────────────────

@mcp.tool()
async def manage_oneview_resource(query: str, resource_category: str = "server-hardware", env: str = "dev", request_body: dict = None, parameters: dict = None) -> str:
    """
    Manage ANY OneView on-premises resource (servers, storage, networks, enclosures, profiles).
    Set resource_category to the REST API path (e.g., 'server-hardware', 'storage-volumes', 'ethernet-networks', 'enclosures').
    """
    return await _execute_hardware_command(query, env, expected_protocol=Protocol.ONEVIEW, resource_category=resource_category, request_body=request_body, parameters=parameters)

@mcp.tool()
async def manage_comops_resource(query: str, resource_category: str = "servers", env: str = "dev", request_body: dict = None, parameters: dict = None) -> str:
    """
    Manage ANY Compute Ops Management cloud resource (servers, policies, firmware).
    Set resource_category to the REST API path (e.g., 'servers', 'policies', 'jobs').
    """
    return await _execute_hardware_command(query, env, expected_protocol=Protocol.COMS, resource_category=resource_category, request_body=request_body, parameters=parameters)

def _extract_category_from_query(query: str, current_category: str, protocol: Protocol) -> str:
    q = query.lower()
    
    # Mapping of keywords in query -> category name
    mappings = {
        "firmware-bundles": "firmware-bundles",
        "firmware-bundle": "firmware-bundles",
        "firmware bundles": "firmware-bundles",
        "firmware bundle": "firmware-bundles",
        "firmware": "firmware-bundles" if protocol == Protocol.COMS else "server-hardware/*/firmware",
        "storage-volumes": "storage-volumes",
        "storage-volume": "storage-volumes",
        "storage volumes": "storage-volumes",
        "storage volume": "storage-volumes",
        "storage": "storage-volumes",
        "volumes": "storage-volumes",
        "volume": "storage-volumes",
        "ethernet-networks": "ethernet-networks",
        "ethernet-network": "ethernet-networks",
        "ethernet networks": "ethernet-networks",
        "ethernet network": "ethernet-networks",
        "networks": "ethernet-networks",
        "network": "ethernet-networks",
        "enclosures": "enclosures",
        "enclosure": "enclosures",
        "servers": "servers" if protocol == Protocol.COMS else "server-hardware",
        "server": "servers" if protocol == Protocol.COMS else "server-hardware",
    }
    
    for keyword, mapped in mappings.items():
        if keyword in q:
            return mapped
            
    return current_category

async def _execute_hardware_command(query: str, env: str, expected_protocol: Protocol, resource_category: str = "server-hardware", request_body: dict = None, parameters: dict = None) -> str:
    # Auto-extract correct resource category from query to avoid default collisions
    default_categories = ["server-hardware", "servers"]
    if resource_category in default_categories:
        resource_category = _extract_category_from_query(query, resource_category, expected_protocol)

    # ── Step 1: Authentication ────────────────────────────────────────────────
    try:
        token, claims = _get_token_and_claims()
        email, role   = _resolve_role(claims)
    except ValueError as e:
        return (
            f"❌ Not authenticated.\n{e}\n\n"
            f"Please login first using sso_login(provider='auth0' | 'okta' | 'azure')."
        )

    # ── Step 2: Resource Resolution ───────────────────────────────────────────
    is_list_query = any(w in query.lower() for w in ["list", "show all", "all servers", "show servers"])
    is_servers_category = resource_category in ["server-hardware", "servers"]
    if is_list_query and is_servers_category:
        ov_records = [r for r in _registry.all_records() if Protocol.ONEVIEW in r.supported_protocols]
        com_records = [r for r in _registry.all_records() if Protocol.COMS in r.supported_protocols]
        
        ov_on = sum(1 for r in ov_records if r.power_state == "On")
        com_on = sum(1 for r in com_records if r.power_state == "On")
        
        # Grab top 5 for sample individual data
        sample_data = []
        for r in (ov_records[:3] + com_records[:2]):
            sample_data.append({
                "uuid": r.uuid,
                "name": r.name,
                "protocol": "OneView" if Protocol.ONEVIEW in r.supported_protocols else "Compute Ops",
                "powerState": r.power_state,
                "ip_address": r.ip_address
            })
            
        return (
            f"✅ Authenticated as {email} (Role: {role})\n"
            f"📋 Infrastructure Summary (Total: {len(ov_records) + len(com_records)}):\n"
            f"  • OneView Physical Nodes : {len(ov_records)} ({ov_on} Powered On)\n"
            f"  • Compute Ops Cloud Nodes: {len(com_records)} ({com_on} Powered On)\n\n"
            f"🔍 Sample Individual Data (First 5 records):\n"
            f"{json.dumps(sample_data, indent=2)}\n\n"
            f"💡 Note: Displaying 5 of 1500 to prevent chat overflow. "
            f"To check a specific resource, ask for its status directly."
        )

    try:
        ctx = _resolver.resolve(query, resource_category=resource_category, expected_protocol=expected_protocol, parameters=parameters)
    except ResolverError as e:
        return f"❌ Resource not found or query unclear.\nReason: {e}"

    if expected_protocol != ctx.selected_protocol:
        return f"❌ Wrong tool used! Server {ctx.resource_name} uses protocol {ctx.selected_protocol.value}, but you used the tool for {expected_protocol.value}."

    # ── Step 3: Authorization (RBAC + ABAC) ───────────────────────────────────
    action_verb_map = {
        "On": "execute", "Off": "execute", "Reset": "execute", "ColdBoot": "execute",
        "Status": "read", "Create": "create", "Allocate": "create",
        "Deallocate": "delete", "Delete": "delete",
    }
    action_val = ctx.action.value if hasattr(ctx.action, "value") else str(ctx.action)
    rbac_action = action_verb_map.get(action_val, "execute")
    
    try:
        allowed, reason, identity = _authorize(
            rbac_action, ctx.resource_uuid, "server-hardware", env, ctx.vendor.value
        )
    except (RuntimeError, ValueError) as e:
        return f"❌ Authorization error: {e}"

    if not allowed:
        return f"❌ Access Denied for {email} (Role: {role})\nReason: {reason}"

    # ── Step 4: Execute on Mock Server ────────────────────────────────────────
    http_method = ctx.http_method
    url = ctx.endpoint
    body = request_body if request_body is not None else ctx.request_body

    async with httpx.AsyncClient(timeout=3.0) as client:
        try:
            if http_method == "GET": resp = await client.get(url)
            elif http_method == "POST": resp = await client.post(url, json=body or {})
            elif http_method == "PUT": resp = await client.put(url, json=body or {})
            elif http_method == "DELETE": resp = await client.delete(url)
            
            response_data = resp.json() if resp.content else {"status": resp.status_code}

            return (
                f"✅ Executed Successfully via {expected_protocol.value}\n"
                f"User      : {email} (Role: {role})\n"
                f"Resource  : {ctx.resource_name}\n"
                f"Action    : {action_val}\n"
                f"Endpoint  : {url} ({http_method} → {resp.status_code})\n"
                f"─────────────────────────────────\n"
                + json.dumps(response_data, indent=2)
            )
        except Exception as e:
            return f"⚠️ Mock server call failed: {e}\nEnsure backend {expected_protocol.value} is running."


# ─────────────────────────────────────────────────────────────────────────────
# Entry Point
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    mcp.run()
