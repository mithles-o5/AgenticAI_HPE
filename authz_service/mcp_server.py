import asyncio
import httpx
import os
import json
from mcp.server.fastmcp import FastMCP
from models import Resource, Context, AuthRequest
from policy_engine import PolicyEngine

# Initialize the MCP Server (Identity-Based Upgrade)
mcp = FastMCP(
    "Identity-Managed-Authz",
    instructions="""
    Hardware management tools with zero-trust cryptographic authorization.
    All actions are strongly bound to the cryptographic identity which is ALREADY securely configured in the background. 
    DO NOT ask the user for any tokens, emails, or credentials. Just execute the tools directly when requested. The system will automatically resolve their identity.
    """
)

# Backend configuration
BASE_URL = "http://127.0.0.1:8001"

def get_authz_token() -> str:
    """Get the JWT token from the environment configuration or fallback local file."""
    token = os.environ.get("AUTHZ_ID_TOKEN")
    
    if not token:
        # Fallback for when Claude Desktop env config parsing fails on Windows
        try:
            token_path = os.path.join(os.path.dirname(__file__), ".auth_token")
            with open(token_path, "r") as f:
                token = f.read().strip()
        except Exception:
            pass

    if not token:
        raise ValueError("Security Error: AUTHZ_ID_TOKEN not found in environment and .auth_token file is missing. Hardware management tools are locked down.")
    return token

# ----------------- Hardware Management Tools (Authorized) ----------------- #

async def _call_backend_authorized(action, resource_id, env, vendor):
    """Internal helper to communicate with the Authz Engine backend using the active identity."""
    try:
        token = get_authz_token()
    except Exception as e:
        return False, str(e)
    
    # Context for the evaluation
    resource = Resource(id=resource_id, env=env, vendor=vendor)
    context = Context(time="12:00", location="mcp-client") # Simulated context
    
    auth_req = AuthRequest(
        token=token,
        action=action,
        resource=resource,
        context=context
    )

    async with httpx.AsyncClient() as client:
        try:
            # 1. Ask for Authorization
            auth_res = await client.post(f"{BASE_URL}/authorize", json=auth_req.model_dump())
            auth_data = auth_res.json()
            
            if auth_data["decision"] == "DENY":
                return False, f"ACCESS DENIED: {auth_data['reason']}"

            return True, "Authorized"
        except Exception as e:
            return False, f"Authorization Connection Error: {str(e)}"

@mcp.tool()
async def list_servers(env: str = "dev", vendor: str = "HPE") -> str:
    """List all physical servers. Identity automatically resolved."""
    allowed, message = await _call_backend_authorized("view", "all-servers", env, vendor)
    if not allowed: return message

    async with httpx.AsyncClient() as client:
        res = await client.get(f"{BASE_URL}/rest/server-hardware")
        return str(res.json())

@mcp.tool()
async def power_on(server_id: str, env: str = "dev", vendor: str = "HPE") -> str:
    """Power on a specific server. Identity automatically resolved."""
    allowed, message = await _call_backend_authorized("restart", server_id, env, vendor)
    if not allowed: return message

    async with httpx.AsyncClient() as client:
        res = await client.put(f"{BASE_URL}/rest/server-hardware/{server_id}/powerState", params={"state": "On"})
        return str(res.json())

@mcp.tool()
async def reboot_server(server_id: str, env: str = "dev", vendor: str = "HPE") -> str:
    """Reboot a specific server. Identity automatically resolved."""
    allowed, message = await _call_backend_authorized("restart", server_id, env, vendor)
    if not allowed: return message

    async with httpx.AsyncClient() as client:
        res = await client.post(f"{BASE_URL}/rest/server-hardware/{server_id}/actions/reset")
        return str(res.json())

if __name__ == "__main__":
    mcp.run()
