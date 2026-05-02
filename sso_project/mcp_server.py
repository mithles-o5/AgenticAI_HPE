import sys
import os
import logging
import json
import jwt
import datetime
import asyncio
import urllib.request
import urllib.parse
import webbrowser
import base64
import hashlib
import secrets
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# Suppress logs so Claude receives clean JSON-RPC on stdout
logging.disable(logging.CRITICAL)

from mcp.server.stdio import stdio_server
import mcp.types as types
from mcp.server import Server

SECRET_KEY = "my_secret_key"
server = Server("sso-mcp-server")

# ==========================================
# AUTH0 CONFIGURATION 
# Please update these with your Auth0 details!
# ==========================================
AUTH0_DOMAIN = "dev-m8h0kmfpfmbtdhoq.us.auth0.com"      # e.g. dev-abc123yz.us.auth0.com
AUTH0_CLIENT_ID = "De3dgvX4Szp5rPY2qwwRUlXHe1kEK4cy"                # e.g. a1b2c3d4e5...
REDIRECT_URI = "http://127.0.0.1:8080/callback"   # Provide this exact URL in Auth0 Allowed Callback URLs

# We will store the temporary code captured from the callback here
captured_code = None

def generate_token(username, role):
    return jwt.encode({
        "user": username,
        "role": role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }, SECRET_KEY, algorithm="HS256")

def login_via_sso(username, password):
    USERS = {"user1": ("123", "user"), "admin": ("admin123", "admin")}
    if username in USERS and USERS[username][0] == password:
        role = USERS[username][1]
        return {"success": True, "token": generate_token(username, role), "role": role, "user": username}
    return {"success": False, "error": "Invalid credentials"}


class CallbackHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass # Suppress HTTP logs

    def do_GET(self):
        global captured_code
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)
        
        if 'code' in params:
            captured_code = params['code'][0]
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<html><body><h1 style='font-family: sans-serif'>Login Successful!</h1><p style='font-family: sans-serif'>Authentication complete. You can close this window and return to your AI agent.</p></body></html>")
        else:
            self.send_response(400)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<html><body><h1 style='font-family: sans-serif'>Login Failed.</h1><p style='font-family: sans-serif'>No authorization code parameter found in the URL.</p></body></html>")
        
        # Stop the server after responding
        threading.Thread(target=self.server.shutdown).start()

def generate_pkce_pair():
    # Generate random verifier string
    verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode('utf-8').rstrip('=')
    # Hash it for the challenge
    digest = hashlib.sha256(verifier.encode('utf-8')).digest()
    challenge = base64.urlsafe_b64encode(digest).decode('utf-8').rstrip('=')
    return verifier, challenge

def trigger_auth0_login():
    """Starts local server, opens browser, returns the Auth0 Access Token, or None."""
    global captured_code
    captured_code = None
    
    verifier, challenge = generate_pkce_pair()
    
    # 1. Build the Auth0 login URL
    auth_params = {
        "response_type": "code",
        "client_id": AUTH0_CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": "openid profile email",
        "code_challenge": challenge,
        "code_challenge_method": "S256"
    }
    url = f"https://{AUTH0_DOMAIN}/authorize?" + urllib.parse.urlencode(auth_params)
    
    # 2. Start local callback server on port 8080
    httpd = HTTPServer(('127.0.0.1', 8080), CallbackHandler)
    
    # Run the server in a thread so we can open the browser
    server_thread = threading.Thread(target=httpd.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    
    # 3. Pop Open Browser!
    webbrowser.open(url)
    
    # 4. Wait for the user to log in (server.shutdown() will release this)
    server_thread.join(timeout=300) # Give user 5 mins to login
    
    if not captured_code:
        return None, "Login timed out or failed."
        
    # 5. Exchange Code for Token
    token_url = f"https://{AUTH0_DOMAIN}/oauth/token"
    token_data = {
        "grant_type": "authorization_code",
        "client_id": AUTH0_CLIENT_ID,
        "code_verifier": verifier,
        "code": captured_code,
        "redirect_uri": REDIRECT_URI
    }
    encoded_data = json.dumps(token_data).encode('utf-8')
    req = urllib.request.Request(token_url, data=encoded_data, headers={"Content-Type": "application/json"})
    
    try:
        with urllib.request.urlopen(req) as response:
            token_resp = json.loads(response.read().decode('utf-8'))
            # token_resp normally contains 'access_token', 'id_token', etc.
            return token_resp.get("access_token"), "Success"
    except Exception as e:
        error_info = getattr(e, 'read', lambda: b"Unknown Error")().decode()
        return None, f"Failed to exchange token: HTTP {getattr(e, 'code', 'Error')} - {error_info}"

def verify_token(token):
    # Try Auth0 first
    url = f"https://{AUTH0_DOMAIN}/userinfo"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except Exception:
        # Fall back to local secret key validation for testing
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except Exception:
            return None


@server.list_tools()
async def list_tools():
    return [
        types.Tool(
            name="sso_login",
            description="Login securely via browser-based Auth0 SSO. Pops up a browser window for you to log in. No credentials needed in the input.",
            inputSchema={
                "type": "object",
                "properties": {},
            }
        ),
        types.Tool(
            name="execute_action",
            description="Execute a privileged action. Requires Auth0 Access Token. Used to test valid authentication.",
            inputSchema={
                "type": "object",
                "properties": {
                    "token": {"type": "string"},
                    "action": {"type": "string"}
                },
                "required": ["token", "action"]
            }
        ),
        types.Tool(
            name="check_access",
            description="Check what resources a user can access using their Auth0 token.",
            inputSchema={
                "type": "object",
                "properties": {
                    "token": {"type": "string"},
                    "resource": {"type": "string"}
                },
                "required": ["token"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name, arguments):
    if name == "sso_login":
        if AUTH0_DOMAIN == "YOUR_AUTH0_DOMAIN.auth0.com":
            return [types.TextContent(type="text", text="ERROR: Auth0 placeholders are not configured. Please edit mcp_server.py to add your Domain and Client ID.")]
        
        token, message = trigger_auth0_login()
        if token:
            return [types.TextContent(type="text",
                text=f"Login Successful via Browser!\nAuth0 Access Token: {token}\n(Pass this token to other tools to prove identity).")]
        else:
            return [types.TextContent(type="text", text=f"Login Failed: {message}")]

    elif name == "execute_action":
        user_data = verify_token(arguments.get("token"))
        if not user_data:
            return [types.TextContent(type="text", text="Invalid or expired token. Please run sso_login again.")]
            
        identity = user_data.get("email") or user_data.get("nickname") or user_data.get("sub") or user_data.get("user")
        role = user_data.get("role")
        
        if role and role != "admin" and not identity:
             return [types.TextContent(type="text", text=f"Access Denied. Role '{role}' cannot execute actions.")]
             
        return [types.TextContent(type="text",
            text=f"Action Executed!\nUser (from Auth0): {identity}\nAction: {arguments.get('action')}\nStatus: Completed")]

    elif name == "check_access":
        user_data = verify_token(arguments.get("token"))
        if not user_data:
            return [types.TextContent(type="text", text="Invalid or expired token. Please run sso_login again.")]
            
        identity = user_data.get("email") or user_data.get("nickname") or user_data.get("sub") or user_data.get("user")
        return [types.TextContent(type="text",
            text=f"Access Control Check:\nIdentity '{identity}' is recognized via Auth0. Access Granted to '{arguments.get('resource')}'.")]

    return [types.TextContent(type="text", text=f"Unknown tool: {name}")]


if __name__ == "__main__":
    async def main():
        async with stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                server.create_initialization_options()
            )
    asyncio.run(main())