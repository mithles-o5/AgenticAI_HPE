"""
azure_provider.py
=================
SSO Provider for Microsoft Azure Active Directory (PKCE OAuth 2.0).

TO ACTIVATE:
    1. Register an app in Azure Portal → Azure Active Directory → App Registrations
    2. Set Supported account types to your preference
    3. Add `http://127.0.0.1:8080/callback` as a Redirect URI (Platform: Mobile and desktop applications)
    4. Fill in AZURE_TENANT_ID and AZURE_CLIENT_ID below
    5. Under API Permissions, add: openid, profile, email, User.Read
    6. Set PROVIDER = "azure" in authentication/__init__.py

Reference:
    https://learn.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-auth-code-flow
"""

import json
import base64
import hashlib
import secrets
import threading
import urllib.request
import urllib.parse
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler

from base_provider import SSOProvider


# ─────────────────────────────────────────────────────────────────────────────
# Azure AD Application Configuration  (fill these in)
# ─────────────────────────────────────────────────────────────────────────────

AZURE_TENANT_ID = "YOUR_TENANT_ID"         # e.g. xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
                                            # Use "common" for multi-tenant apps
AZURE_CLIENT_ID = "YOUR_AZURE_CLIENT_ID"   # Application (client) ID from Azure Portal
REDIRECT_URI    = "http://127.0.0.1:8080/callback"
SCOPES          = "openid profile email User.Read"
CALLBACK_PORT   = 8080


# ─────────────────────────────────────────────────────────────────────────────
# Internal: OAuth Callback HTTP Handler
# ─────────────────────────────────────────────────────────────────────────────

class _AzureCallbackHandler(BaseHTTPRequestHandler):
    """One-shot HTTP handler that captures the OAuth authorization code."""

    captured_code = None

    def log_message(self, format, *args):
        pass  # Suppress all HTTP server logs

    def do_GET(self):
        params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)

        if "code" in params:
            _AzureCallbackHandler.captured_code = params["code"][0]
            self._respond(200, "Login Successful!", "Azure AD authentication complete. You can close this window and return to your AI agent.")
        else:
            error = params.get("error_description", ["No authorization code found."])[0]
            self._respond(400, "Login Failed.", error)

        threading.Thread(target=self.server.shutdown).start()

    def _respond(self, status: int, heading: str, body: str):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        html = (
            f"<html><body style='font-family:sans-serif;padding:40px'>"
            f"<h1>{heading}</h1><p>{body}</p>"
            f"</body></html>"
        ).encode("utf-8")
        self.wfile.write(html)


# ─────────────────────────────────────────────────────────────────────────────
# Internal: PKCE Utilities
# ─────────────────────────────────────────────────────────────────────────────

def _generate_pkce_pair() -> tuple[str, str]:
    """Generate a PKCE (Proof Key for Code Exchange) verifier and challenge."""
    verifier  = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode("utf-8").rstrip("=")
    digest    = hashlib.sha256(verifier.encode("utf-8")).digest()
    challenge = base64.urlsafe_b64encode(digest).decode("utf-8").rstrip("=")
    return verifier, challenge


# ─────────────────────────────────────────────────────────────────────────────
# Azure AD SSO Provider
# ─────────────────────────────────────────────────────────────────────────────

class AzureADProvider(SSOProvider):
    """
    SSO Provider for Microsoft Azure Active Directory using PKCE Authorization Code Flow.

    Usage:
        provider = AzureADProvider()
        token, message = provider.login()
        user = provider.verify_token(token)

    Endpoints used:
        Authorization : https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/authorize
        Token         : https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token
        UserInfo      : https://graph.microsoft.com/oidc/userinfo
    """

    def login(self) -> tuple[str | None, str]:
        """
        Opens the browser for Azure AD login and returns an access token.
        Blocks until the user completes login (up to 5 minutes).
        """
        if AZURE_TENANT_ID == "YOUR_TENANT_ID" or AZURE_CLIENT_ID == "YOUR_AZURE_CLIENT_ID":
            return None, (
                "Azure AD is not configured. "
                "Please set AZURE_TENANT_ID and AZURE_CLIENT_ID in authentication/azure_provider.py."
            )

        _AzureCallbackHandler.captured_code = None
        verifier, challenge = _generate_pkce_pair()

        # Build Azure AD authorization URL
        auth_url = (
            f"https://login.microsoftonline.com/{AZURE_TENANT_ID}/oauth2/v2.0/authorize?"
            + urllib.parse.urlencode({
                "response_type":         "code",
                "client_id":             AZURE_CLIENT_ID,
                "redirect_uri":          REDIRECT_URI,
                "scope":                 SCOPES,
                "code_challenge":        challenge,
                "code_challenge_method": "S256",
                "state":                 secrets.token_hex(16),
                "response_mode":         "query",
            })
        )

        # Start local callback server
        httpd = HTTPServer(("127.0.0.1", CALLBACK_PORT), _AzureCallbackHandler)
        server_thread = threading.Thread(target=httpd.serve_forever)
        server_thread.daemon = True
        server_thread.start()

        # Open browser for user login
        webbrowser.open(auth_url)

        # Wait for the callback (5-minute timeout)
        server_thread.join(timeout=300)

        if not _AzureCallbackHandler.captured_code:
            return None, "Azure AD login timed out or was cancelled by the user."

        # Exchange authorization code for access token
        return self._exchange_code_for_token(_AzureCallbackHandler.captured_code, verifier)

    def _exchange_code_for_token(self, code: str, verifier: str) -> tuple[str | None, str]:
        """Exchange the OAuth authorization code for an access token via Azure AD token endpoint."""
        token_url  = f"https://login.microsoftonline.com/{AZURE_TENANT_ID}/oauth2/v2.0/token"
        token_body = urllib.parse.urlencode({
            "grant_type":    "authorization_code",
            "client_id":     AZURE_CLIENT_ID,
            "code_verifier": verifier,
            "code":          code,
            "redirect_uri":  REDIRECT_URI,
            "scope":         SCOPES,
        }).encode("utf-8")

        req = urllib.request.Request(
            token_url,
            data=token_body,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        try:
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                # access_token is for Graph API; id_token contains user claims
                return data.get("access_token"), "Login successful."
        except Exception as e:
            detail = getattr(e, "read", lambda: b"Unknown error")().decode()
            return None, f"Token exchange failed: HTTP {getattr(e, 'code', 'Error')} — {detail}"

    def verify_token(self, token: str) -> dict | None:
        """
        Verify an Azure AD access token via the Microsoft Graph /userinfo endpoint.
        Returns the user's profile dict on success, or None if invalid/expired.
        """
        url = "https://graph.microsoft.com/oidc/userinfo"
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
        try:
            with urllib.request.urlopen(req) as resp:
                return json.loads(resp.read().decode())
        except Exception:
            return None
