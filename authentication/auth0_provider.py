"""
auth0_provider.py
=================
SSO Provider implementation for Auth0 (PKCE OAuth 2.0 flow).

Configuration:
    Update AUTH0_DOMAIN, AUTH0_CLIENT_ID, and REDIRECT_URI
    with your Auth0 application credentials.

Flow:
    1. Generates a PKCE verifier/challenge pair
    2. Opens the user's browser to Auth0 login page
    3. Starts a local callback server on port 8080
    4. Captures the authorization code from the redirect
    5. Exchanges the code for an Access Token
    6. Verifies tokens via the Auth0 /userinfo endpoint
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
# Auth0 Application Configuration
# ─────────────────────────────────────────────────────────────────────────────

AUTH0_DOMAIN    = "dev-m8h0kmfpfmbtdhoq.us.auth0.com"
AUTH0_CLIENT_ID = "De3dgvX4Szp5rPY2qwwRUlXHe1kEK4cy"
REDIRECT_URI    = "http://127.0.0.1:8080/callback"
SCOPES          = "openid profile email"
CALLBACK_PORT   = 8080

# ─────────────────────────────────────────────────────────────────────────────
# Internal: OAuth Callback HTTP Handler
# ─────────────────────────────────────────────────────────────────────────────

class _CallbackHandler(BaseHTTPRequestHandler):
    """One-shot HTTP handler that captures the OAuth authorization code."""

    captured_code = None  # Shared state written by the callback

    def log_message(self, format, *args):
        pass  # Suppress all HTTP server logs

    def do_GET(self):
        params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)

        if "code" in params:
            _CallbackHandler.captured_code = params["code"][0]
            self._respond(200, "Login Successful!", "Authentication complete. You can close this window and return to your AI agent.")
        else:
            self._respond(400, "Login Failed.", "No authorization code found in the redirect URL.")

        # Shutdown the callback server after responding to avoid blocking
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
# Auth0 SSO Provider
# ─────────────────────────────────────────────────────────────────────────────

class Auth0Provider(SSOProvider):
    """
    SSO Provider for Auth0 using PKCE Authorization Code Flow.

    Usage:
        provider = Auth0Provider()
        token, message = provider.login()
        user = provider.verify_token(token)
    """

    def login(self) -> tuple[str | None, str]:
        """
        Opens the browser for Auth0 login and returns an access token.
        Blocks until the user completes login (up to 5 minutes).
        """
        _CallbackHandler.captured_code = None
        verifier, challenge = _generate_pkce_pair()

        # Build Auth0 authorization URL
        auth_url = (
            f"https://{AUTH0_DOMAIN}/authorize?"
            + urllib.parse.urlencode({
                "response_type":         "code",
                "client_id":             AUTH0_CLIENT_ID,
                "redirect_uri":          REDIRECT_URI,
                "scope":                 SCOPES,
                "code_challenge":        challenge,
                "code_challenge_method": "S256",
            })
        )

        # Start local callback server (fail fast if port is already in use)
        try:
            httpd = HTTPServer(("127.0.0.1", CALLBACK_PORT), _CallbackHandler)
        except OSError as e:
            return None, (
                f"Cannot start Auth0 callback server on port {CALLBACK_PORT}: {e}\n"
                f"Another process is using that port. "
                f"Stop it or change CALLBACK_PORT in auth0_provider.py."
            )
        server_thread = threading.Thread(target=httpd.serve_forever)
        server_thread.daemon = True
        server_thread.start()

        # Open browser for user login
        webbrowser.open(auth_url)

        # Wait for the callback (2-minute timeout — reduced from 5 min)
        server_thread.join(timeout=120)

        if not _CallbackHandler.captured_code:
            return None, "Login timed out or was cancelled by the user."

        # Exchange authorization code for access token
        return self._exchange_code_for_token(_CallbackHandler.captured_code, verifier)

    def _exchange_code_for_token(self, code: str, verifier: str) -> tuple[str | None, str]:
        """Exchange the OAuth authorization code for an access token."""
        token_url  = f"https://{AUTH0_DOMAIN}/oauth/token"
        token_body = json.dumps({
            "grant_type":    "authorization_code",
            "client_id":     AUTH0_CLIENT_ID,
            "code_verifier": verifier,
            "code":          code,
            "redirect_uri":  REDIRECT_URI,
        }).encode("utf-8")

        req = urllib.request.Request(
            token_url,
            data=token_body,
            headers={"Content-Type": "application/json"}
        )
        try:
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data.get("access_token"), "Login successful."
        except Exception as e:
            detail = getattr(e, "read", lambda: b"Unknown error")().decode()
            return None, f"Token exchange failed: HTTP {getattr(e, 'code', 'Error')} — {detail}"

    def verify_token(self, token: str) -> dict | None:
        """
        Verify a token by calling the Auth0 /userinfo endpoint.
        Returns the user's profile dict on success, or None if invalid.
        """
        url = f"https://{AUTH0_DOMAIN}/userinfo"
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
        try:
            with urllib.request.urlopen(req) as resp:
                return json.loads(resp.read().decode())
        except Exception:
            return None
