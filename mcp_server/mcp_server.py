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

# Path to roles.json (the role mapping file you can freely edit)
ROLES_FILE = os.path.join(AUTHZ_DIR, "roles.json")

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
    "auth0" : "Auth0      ✅ Ready         (browser login via Auth0)",
    "okta"  : "Okta       🔲 Needs config  (fill in OKTA_DOMAIN + OKTA_CLIENT_ID in okta_provider.py)",
    "azure" : "Azure AD   🔲 Needs config  (fill in AZURE_TENANT_ID + AZURE_CLIENT_ID in azure_provider.py)",
}

PROVIDER_LIST = "\n".join(
    f"  • {k} — {v}" for k, v in AVAILABLE_PROVIDERS.items()
)

mcp = FastMCP(
    "HPE-OneView-MCP",
    instructions=f"""
    You are managing HPE physical servers via MCP.

    ── PRIMARY TOOL ────────────────────────────────────────────────────────────
    For ALL hardware commands, use: resolve_and_execute(query="<user request>")
    This single tool handles the full pipeline automatically:
      1. Authenticates the user
      2. Resolves the natural language command to the correct server + API
      3. Checks role-based permissions (RBAC + ABAC)
      4. Executes on the HPE OneView mock server
      5. Returns the result

    Examples of what to pass as 'query':
      resolve_and_execute(query="turn on rack-server-04")
      resolve_and_execute(query="reboot blade-enclosure-01")
      resolve_and_execute(query="status synergy-compute-03")
      resolve_and_execute(query="power off synergy-compute-01")
      resolve_and_execute(query="list all servers")

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

    This ensures an Okta token is verified via Okta's /userinfo, an Auth0
    token via Auth0's /userinfo, etc. — never the wrong endpoint.

    Returns (token, claims) or raises ValueError if no active session.
    """
    token         = load_token()          # raises ValueError if missing
    provider_name = load_provider()       # which SSO provider issued this token

    if not provider_name:
        raise ValueError(
            "Session is missing provider information.\n"
            "Please log out and log in again."
        )

    provider = get_provider(provider_name)
    claims   = provider.verify_token(token)
    if not claims:
        raise ValueError("Token expired or invalid. Please log in again.")
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
    return f"✅ Logged out. Session cleared."


# ─────────────────────────────────────────────────────────────────────────────
# Tool 4 — Resolve & Execute  (THE MAIN FLOW TOOL)
# ─────────────────────────────────────────────────────────────────────────────

@mcp.tool()
async def resolve_and_execute(query: str, env: str = "dev") -> str:
    """
    THE PRIMARY TOOL — Full pipeline: Auth → RBAC → Resolve → Execute.

    Takes a natural language command from Claude, resolves it to the correct
    HPE server and API endpoint, checks permissions, then executes against
    the mock OneView server and returns the result.

    Examples:
      "turn on rack-server-04"
      "reboot blade-enclosure-01"
      "status synergy-compute-03"
      "power off synergy-compute-01"
      "list all servers"

    Args:
        query : Natural language command (what to do and on which server).
        env   : Deployment environment for ABAC check. Default: 'dev'.
    """

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
    # Handle 'list servers' shortcut before running the full resolver
    if any(w in query.lower() for w in ["list", "all servers", "show servers"]):
        servers = []
        for r in _registry.all_records():
            servers.append({
                "name":         r.name,
                "uuid":         r.uuid,
                "model":        r.model,
                "location":     r.location,
                "power_state":  r.power_state,
                "health":       r.health.value,
                "protocols":    [p.value for p in r.supported_protocols],
            })
        return (
            f"✅ Authenticated as {email} (Role: {role})\n"
            f"📋 Registered servers ({len(servers)} total):\n"
            + json.dumps(servers, indent=2)
        )

    try:
        ctx = _resolver.resolve(query)
    except ResolverError as e:
        return (
            f"❌ Resource not found.\n"
            f"Query: '{query}'\n"
            f"Reason: {e}\n\n"
            f"Tip: Try 'list all servers' to see what's available."
        )

    # ── Step 3: Authorization (RBAC + ABAC) ───────────────────────────────────
    # Map resolver action → RBAC action verb
    action_verb_map = {
        "On":         "execute",
        "Off":        "execute",
        "Reset":      "execute",
        "ColdBoot":   "execute",
        "Status":     "read",
        "Create":     "create",
        "Allocate":   "create",
        "Deallocate": "delete",
        "Delete":     "delete",
    }
    action_val  = ctx.action.value if hasattr(ctx.action, "value") else str(ctx.action)
    rbac_action = action_verb_map.get(action_val, "execute")
    resource_category = "server-hardware"   # resolver only handles server-hardware

    try:
        allowed, reason, identity = _authorize(
            rbac_action, ctx.resource_uuid, resource_category, env, ctx.vendor.value
        )
    except (RuntimeError, ValueError) as e:
        return f"❌ Authorization error: {e}"

    if not allowed:
        return (
            f"❌ Access Denied for {email} (Role: {role})\n"
            f"Attempted: {rbac_action} on {ctx.resource_name}\n"
            f"Reason: {reason}"
        )

    # ── Step 4: Execute on Mock Server ────────────────────────────────────────
    # Choose the correct mock endpoint based on the resolved action
    action_endpoint_map = {
        "On":         ("PUT",  f"/rest/server-hardware/{ctx.resource_uuid}/powerState",  {"powerState": "On"}),
        "Off":        ("PUT",  f"/rest/server-hardware/{ctx.resource_uuid}/powerState",  {"powerState": "Off"}),
        "Reset":      ("PUT",  f"/rest/server-hardware/{ctx.resource_uuid}/powerState",  {"powerState": "Reset"}),
        "ColdBoot":   ("PUT",  f"/rest/server-hardware/{ctx.resource_uuid}/powerState",  {"powerState": "ColdBoot"}),
        "Status":     ("GET",  f"/rest/server-hardware/{ctx.resource_uuid}",             None),
        "Create":     ("POST", f"/rest/server-hardware",                                 {}),
        "Allocate":   ("POST", f"/rest/server-hardware",                                 {}),
        "Deallocate": ("PUT",  f"/rest/server-hardware/{ctx.resource_uuid}/refreshState", {}),
        "Delete":     ("DELETE",f"/rest/server-hardware/{ctx.resource_uuid}",            None),
    }

    http_method, endpoint, body = action_endpoint_map.get(
        action_val,
        ("GET", f"/rest/server-hardware/{ctx.resource_uuid}", None)  # fallback to status
    )

    async with httpx.AsyncClient() as client:
        try:
            url = f"{HARDWARE_BACKEND_URL}{endpoint}"
            if http_method == "GET":
                resp = await client.get(url)
            elif http_method == "POST":
                resp = await client.post(url, json=body or {})
            elif http_method == "PUT":
                resp = await client.put(url, json=body or {})
            elif http_method == "DELETE":
                resp = await client.delete(url)
            else:
                resp = await client.get(url)

            response_data = resp.json() if resp.content else {}

            return (
                f"✅ Executed Successfully\n"
                f"─────────────────────────────────\n"
                f"User      : {email}\n"
                f"Role      : {role}\n"
                f"Query     : {query}\n"
                f"Resource  : {ctx.resource_name}\n"
                f"Action    : {action_val}\n"
                f"Protocol  : {ctx.selected_protocol.value}\n"
                f"Endpoint  : {endpoint}\n"
                f"HTTP      : {http_method} → {resp.status_code}\n"
                f"─────────────────────────────────\n"
                + json.dumps(response_data, indent=2)
            )

        except Exception as e:
            return (
                f"⚠️ Auth & Resolution passed but mock server call failed.\n"
                f"User      : {email} (Role: {role})\n"
                f"Resource  : {ctx.resource_name}\n"
                f"Endpoint  : {endpoint}\n"
                f"Error     : {e}\n\n"
                f"Ensure the mock server is running: cd mock_server(oneview) && uvicorn main:app --port 8000"
            )


# ─────────────────────────────────────────────────────────────────────────────
# Entry Point
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    mcp.run()
