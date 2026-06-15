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

import mock_db_cache
mock_db_cache.setup()

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
    manage_oneview_resource(query)   — OneView physical servers
    manage_comops_resource(query)    — Compute Ops cloud nodes

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

@mcp.tool()
async def manage_oneview_resource(query: str, resource_category: str = "server-hardware", env: str = "dev") -> str:
    """
    Manage ANY OneView on-premises resource (servers, storage, networks, enclosures, profiles).
    Set resource_category to the REST API path (e.g., 'server-hardware', 'storage-volumes', 'ethernet-networks', 'enclosures').
    """
    return await _execute_hardware_command(query, env, expected_protocol=Protocol.ONEVIEW, backend_url="http://127.0.0.1:8000", resource_category=resource_category)

@mcp.tool()
async def manage_comops_resource(query: str, resource_category: str = "servers", env: str = "dev") -> str:
    """
    Manage ANY Compute Ops Management cloud resource (servers, policies, firmware).
    Set resource_category to the REST API path (e.g., 'servers', 'policies', 'jobs').
    """
    return await _execute_hardware_command(query, env, expected_protocol=Protocol.COMS, backend_url="http://127.0.0.1:8001", resource_category=resource_category)

async def _execute_hardware_command(query: str, env: str, expected_protocol: Protocol, backend_url: str, resource_category: str = "server-hardware") -> str:
    # ── Step 1: Authentication ────────────────────────────────────────────────
    try:
        token, claims = _get_token_and_claims()
        email, role   = _resolve_role(claims)
    except ValueError:
        return (
            "You are not logged in. Please choose an SSO provider:\n\n"
            "• [auth0](https://auth0.com) — Auth0 SSO Login\n"
            "• [okta](https://okta.com) — Okta SSO Login\n"
            "• [azure](https://azure.microsoft.com) — Azure AD SSO Login\n\n"
            "Reply with your choice: auth0, okta, or azure."
        )

    # ── Step 2: Resource Resolution ───────────────────────────────────────────
    if any(w in query.lower() for w in ["list", "all servers", "show servers"]):
        ov_records = _registry.list_devices_by_management_source("oneview")
        com_records = _registry.list_devices_by_management_source("coms")
        
        # Grab top 5 for sample individual data
        sample_data = []
        for r in (ov_records[:3] + com_records[:2]):
            sample_data.append({
                "uuid": r.id,
                "name": r.serial_number,
                "protocol": "OneView" if r.management_source == "oneview" else "Compute Ops",
                "powerState": "Unknown",
                "ip_address": r.ip_address
            })
            
        return (
            f"✅ Authenticated as {email} (Role: {role})\n"
            f"📋 Infrastructure Summary (Total: {len(ov_records) + len(com_records)}):\n"
            f"  • OneView Physical Nodes : {len(ov_records)}\n"
            f"  • Compute Ops Cloud Nodes: {len(com_records)}\n\n"
            f"🔍 Sample Individual Data (First 5 records):\n"
            f"{json.dumps(sample_data, indent=2)}\n\n"
            f"💡 Note: Displaying 5 of 1500 to prevent chat overflow. "
            f"To check a specific resource, ask for its status directly."
        )

    tasks = TaskPlanner.decompose_instruction(query)
    if not tasks:
        return f"❌ Query parsed to an empty task list: '{query}'"

    resolved_tasks = []
    results = []
    
    # ── Step 3: Resource Resolution ───────────────────────────────────────────
    for task in tasks:
        try:
            parsed_payload = {
                "identifier": task.identifier,
                "action": task.action,
                "category": task.category
            }
            ctx = _resolver.resolve(
                parsed_payload=parsed_payload,
                requested_by=email,
            )
            resolved_tasks.append((task, ctx))
        except ResolverError as e:
            results.append(f"❌ Task resolution failed for '{task.identifier}': {e}")

    # ── Step 4: Vendor Synthesis (Group and Optimize by Vendor/Host) ─────────
    from synthesizer import VendorSynthesizer
    batches = VendorSynthesizer.synthesize_batches(resolved_tasks)
    
    # Iterate through synthesized batches and execute
    for key, batch in batches.items():
        for task in batch.tasks:
            # Find the corresponding resolved context for this task
            ctx = next(r for t, r in resolved_tasks if t.task_id == task.task_id)

            if expected_protocol != ctx.management_source:
                results.append(f"❌ Wrong tool used! Server {ctx.device.serial_number} uses protocol {ctx.management_source}, but you used the tool for {expected_protocol}.")
                continue

            # ── Step 5: Authorization (RBAC + ABAC) ───────────────────────────────────
            action_verb_map = {
                "ON": "execute", "OFF": "execute", "RESET": "execute", "COLD_BOOT": "execute",
                "STATUS": "read", "CREATE": "create", "ALLOCATE": "create",
                "DEALLOCATE": "delete", "DELETE": "delete",
            }
            action_val = task.action
            rbac_action = action_verb_map.get(action_val, "execute")
            
            try:
                allowed, reason, identity = _authorize(
                    rbac_action, ctx.device.id, "server-hardware", env, "HPE"
                )
            except (RuntimeError, ValueError) as e:
                results.append(f"❌ Authorization error for '{task.identifier}': {e}")
                continue

            if not allowed:
                results.append(f"❌ Access Denied for {email} (Role: {role}) on '{task.identifier}'\nReason: {reason}")
                continue

            # ── Step 6: Dispatch via OASF Agent (Resolved from Capability Registry) ──
            import asyncio
            loop = asyncio.get_event_loop()
            
            # Map action_val to OASF Skill parameters if required
            parameters = {}
            if action_val in ("ON", "OFF", "RESET", "COLD_BOOT"):
                parameters = {"action_type": "power", "state": "On" if action_val == "ON" else "Off" if action_val == "OFF" else "Reset"}
            elif action_val == "STATUS":
                # Onprem health check skill is mapped via health_check action
                pass

            try:
                # If query is status of server, map action_val to health_check or fetch_metrics
                query_action = "health_check" if action_val == "STATUS" else "execute_action"
                
                response_data = await loop.run_in_executor(
                    None,
                    lambda: _dispatcher.dispatch(
                        agent_type="onprem",
                        query_action=query_action,
                        resource_type=ctx.device.device_type or "server_hardware",
                        resource_id=ctx.device.serial_number,
                        provider_or_protocol=ctx.management_source,
                        parameters=parameters,
                    ),
                )

                # Extract key fields for clear visibility
                norm_data = response_data.get("normalized_data", {}) or response_data.get("raw", {})
                if not norm_data and "raw" in response_data.get("normalized_data", {}):
                    norm_data = response_data["normalized_data"]["raw"]
                
                power_state = (
                    norm_data.get("power_state") 
                    or norm_data.get("powerState") 
                    or (response_data.get("metrics", {})).get("power_state") 
                    or response_data.get("power_state") 
                    or "N/A"
                )
                health_status = (
                    response_data.get("status_level") 
                    or norm_data.get("health_status") 
                    or norm_data.get("health") 
                    or norm_data.get("status") 
                    or "N/A"
                )
                
                insights_list = response_data.get("insights", [])
                insights_summary = ""
                if insights_list:
                    insights_summary = "\nInsights:\n" + "\n".join(f"  • [{i.get('severity', 'info').upper()}] {i.get('message')}" for i in insights_list)

                results.append(
                    f"✅ Executed Successfully via OASF Route\n"
                    f"User         : {email} (Role: {role})\n"
                    f"Resource     : {ctx.device.serial_number}\n"
                    f"Power State  : {power_state.upper()}\n"
                    f"Health Status: {health_status.upper()}\n"
                    f"Action       : {action_val}\n"
                    f"─────────────────────────────────"
                    f"{insights_summary}\n\n"
                    f"Raw Agent Response:\n"
                    + json.dumps(response_data, indent=2)
                )
            except Exception as e:
                results.append(f"⚠️ Agent call failed for '{task.identifier}': {e}")

    return "\n\n=========================================\n\n".join(results)


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
    Manage a cloud resource (VM, container, function) via the Cloud Agent.
    provider: 'aws' | 'azure' | 'gcp' | 'mock'
    resource_type: 'vm' | 'container' | 'function'
    Examples:
      manage_cloud_resource(query="status of my-vm-001", provider="aws")
      manage_cloud_resource(query="create vm prod-worker", provider="gcp")
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
    Manage a network device (switch, router, interface) via the Network Agent.
    protocol: 'snmp' | 'netconf' | 'rest' | 'mock'
    resource_type: 'switch' | 'router' | 'interface'
    Examples:
      manage_network_resource(query="status of core-sw-01", protocol="snmp")
      manage_network_resource(query="discover topology of dc-router-01")
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
    Manage a storage resource (volume, array, pool, bucket) via the Storage Agent.
    provider: 'dscc' | 'nas' | 's3' | 'mock'
    resource_type: 'volume' | 'array' | 'pool' | 'bucket'
    Examples:
      manage_storage_resource(query="capacity of prod-vol-001", provider="dscc")
      manage_storage_resource(query="discover all arrays", provider="nas")
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
    Manage a bare-metal server (server, bmc, sensor, firmware, event_log) via the Server Agent.
    provider: 'redfish' | 'ipmi' | 'ilo' | 'mock'
    resource_type: 'server' | 'bmc' | 'sensor' | 'firmware' | 'event_log'
    Examples:
      manage_server_resource(query="status of OV1-RackServer-001", provider="redfish")
      manage_server_resource(query="power off MS-123", provider="ipmi")
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
            "You are not logged in. Please choose an SSO provider:\n\n"
            "• [auth0](https://auth0.com) — Auth0 SSO Login\n"
            "• [okta](https://okta.com) — Okta SSO Login\n"
            "• [azure](https://azure.microsoft.com) — Azure AD SSO Login\n\n"
            "Reply with your choice: auth0, okta, or azure."
        )

    # ── Step 2: Parse query with QueryAgent ───────────────────────────────────
    parsed   = QueryAgent.parse_query(query)
    action   = parsed.get("action", "STATUS")
    identifier = parsed.get("identifier") or query.strip()
    if identifier.lower().startswith("of "):
        identifier = identifier[3:].strip()

    # ── Step 2.5: Verify CMDB Resource Existence ─────────────────────────────
    allowed_mock_resources = {"demo-vm-001", "core-switch-01", "core-sw-01", "prod-vol-001", "prod-worker", "MS-123", "OV1-RackServer-001", "CoM-CloudNode-001"}
    device = None
    try:
        from resolver import ResourceResolver
        ident_type = ResourceResolver._infer_identifier_type(identifier)
        device = _registry.lookup(identifier, ident_type)
    except Exception:
        pass

    if not device and identifier not in allowed_mock_resources:
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

    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────────────
# POSTGRESQL MEMORY STORE MODULE
# ─────────────────────────────────────────────────────────────────────────────

# Load PostgreSQL connection parameters from environment with default values
PG_HOST = os.getenv("PGHOST", "localhost")
PG_PORT = int(os.getenv("PGPORT", "5432"))
PG_USER = os.getenv("PGUSER", "postgres")
PG_PASSWORD = os.getenv("PGPASSWORD", "password")
PG_DATABASE = os.getenv("PGDATABASE", "postgres")

# Session ID file persistence path
SESSION_ID_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "session_id.txt")

def _get_connection():
    """Opens a connection to the PostgreSQL database."""
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
        print("✅ PostgreSQL memory store database initialized successfully.", file=sys.stderr)
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
        with open(SESSION_ID_FILE, "w") as f:
            f.write(sid)
    except Exception as e:
        print(f"⚠️ Error writing session ID file: {e}", file=sys.stderr)
    return sid

# Initialise persistent session ID
SESSION_ID = _get_or_create_session_id()

# Initialize memory store table at module loading time (since we already have a lifespan context)
try:
    init_db()
except Exception as e:
    print(f"⚠️ Failed to auto-initialize PostgreSQL memory database: {e}", file=sys.stderr)

# ─────────────────────────────────────────────────────────────────────────────
# Memory Store MCP Tools
# ─────────────────────────────────────────────────────────────────────────────

@mcp.tool()
async def list_servers_in_rack(rack_id: str, session_id: str = None) -> str:
    """
    List all servers in a given rack on the OneView mock server.
    Stores the result in memory under last_targets and last_rack, and returns the server list.
    
    Args:
        rack_id: The ID of the rack to query (e.g. 'Rack-01', 'Rack-02').
        session_id: Optional session ID override.
    """
    sid = session_id or SESSION_ID
    url = f"{HARDWARE_BACKEND_URL}/rest/server-hardware"
    
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(url, params={"rack": rack_id})
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            return f"❌ Failed to fetch servers from OneView mock server: {e}"
            
    # Handle if returned structure is list or dict
    members = []
    if isinstance(data, dict):
        if "members" in data:
            members = data["members"]
        elif "server_hardware" in data:
            members = list(data["server_hardware"].values())
    elif isinstance(data, list):
        members = data
        
    if not members:
        return f"⚠️ No servers found in rack '{rack_id}'."
        
    # Format and save targets to memory database
    targets = []
    for s in members:
        targets.append({
            "uuid": s.get("uuid") or s.get("id"),
            "name": s.get("name"),
            "location": s.get("location"),
            "powerState": s.get("powerState") or s.get("power_state")
        })
        
    try:
        remember(sid, "last_rack", rack_id)
        remember(sid, "last_targets", targets)
    except Exception as e:
        return f"⚠️ Retrieved {len(targets)} servers, but failed to persist to memory database: {e}\n\nServers:\n" + json.dumps(targets, indent=2)
        
    return f"✅ Found {len(targets)} servers in rack '{rack_id}' (stored in memory database under session '{sid}'):\n" + json.dumps(targets, indent=2)

@mcp.tool()
async def power_off_last_targets(session_id: str = None) -> str:
    """
    Recalls last_targets from memory, executes power off on each,
    stores last_operation as power_off, and returns a summary.
    
    Args:
        session_id: Optional session ID override.
    """
    sid = session_id or SESSION_ID
    
    try:
        last_targets = recall(sid, "last_targets")
    except Exception as e:
        return f"❌ Error: Database read failed: {e}"
        
    if not last_targets:
        return (
            "❌ Error: No last targets found in memory for this session.\n"
            "Please run list_servers_in_rack first to populate last_targets."
        )
        
    results = []
    async with httpx.AsyncClient() as client:
        for target in last_targets:
            uuid_val = target.get("uuid")
            name_val = target.get("name")
            if not uuid_val:
                results.append({"name": name_val, "status": "Failed (Missing UUID)"})
                continue
                
            url = f"{HARDWARE_BACKEND_URL}/rest/server-hardware/{uuid_val}/powerState"
            try:
                resp = await client.put(url, json={"powerState": "Off"})
                if resp.status_code == 200:
                    results.append({"name": name_val, "uuid": uuid_val, "status": "Success"})
                else:
                    results.append({"name": name_val, "uuid": uuid_val, "status": f"Failed ({resp.status_code})"})
            except Exception as e:
                results.append({"name": name_val, "uuid": uuid_val, "status": f"Error ({e})"})
                
    # Record the last operation
    last_op = {
        "operation": "power_off",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "affected_servers": [t.get("name") for t in last_targets],
        "results": results
    }
    
    try:
        remember(sid, "last_operation", last_op)
    except Exception as e:
        return (
            f"⚠️ Executed power off on servers, but failed to save operation to memory database: {e}\n\n"
            f"Summary:\n" + json.dumps(results, indent=2)
        )
        
    return f"✅ Power off operation completed for session '{sid}'\n\nSummary:\n" + json.dumps(results, indent=2)

@mcp.tool()
def mcp_list_sessions() -> str:
    """
    List all active session IDs in the memory database (for debugging).
    """
    sessions = list_sessions()
    return f"📋 Active sessions in database:\n" + json.dumps(sessions, indent=2)


# ─────────────────────────────────────────────────────────────────────────────
# Entry Point
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    mcp.run()
