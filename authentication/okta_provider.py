"""
okta_provider.py
================
SSO Provider for Okta (PKCE Authorization Code Flow).

TO ACTIVATE:
    1. Create an Okta application (type: Single-Page App or Native)
    2. Fill in OKTA_DOMAIN and OKTA_CLIENT_ID below
    3. Add `http://127.0.0.1:8080/callback` as an Allowed Redirect URI in Okta
    4. Set PROVIDER = "okta" in authentication/__init__.py

Reference:
    https://developer.okta.com/docs/guides/implement-grant-type/authcodepkce/main/
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
# Okta Application Configuration  (fill these in)
# ─────────────────────────────────────────────────────────────────────────────

OKTA_DOMAIN    = "trial-2844204.okta.com"        # e.g. dev-12345678.okta.com
OKTA_CLIENT_ID = "0oa12xcy09nnlPBlf698"
REDIRECT_URI   = "http://127.0.0.1:8080/callback"
SCOPES         = "openid profile email"
CALLBACK_PORT  = 8080


# ─────────────────────────────────────────────────────────────────────────────
# Internal: OAuth Callback HTTP Handler
# ─────────────────────────────────────────────────────────────────────────────

class _OktaCallbackHandler(BaseHTTPRequestHandler):
    """One-shot HTTP handler that captures the OAuth authorization code."""

    captured_code = None

    def log_message(self, format, *args):
        pass  # Suppress all HTTP server logs

    def do_GET(self):
        params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)

        if "code" in params:
            _OktaCallbackHandler.captured_code = params["code"][0]
            self._respond(200, "Login Successful!", "Okta authentication complete. You can close this window and return to your AI agent.")
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
# Okta SSO Provider
# ─────────────────────────────────────────────────────────────────────────────

class OktaProvider(SSOProvider):
    """
    SSO Provider for Okta using PKCE Authorization Code Flow.

    Usage:
        provider = OktaProvider()
        token, message = provider.login()
        user = provider.verify_token(token)

    Endpoints used:
        Authorization : https://{OKTA_DOMAIN}/oauth2/default/v1/authorize
        Token         : https://{OKTA_DOMAIN}/oauth2/default/v1/token
        UserInfo      : https://{OKTA_DOMAIN}/oauth2/default/v1/userinfo
    """

    def login(self) -> tuple[str | None, str]:
        """
        Opens the browser for Okta login and returns an access token.
        Blocks until the user completes login (up to 5 minutes).
        """
        if OKTA_DOMAIN == "your-org.okta.com" or OKTA_CLIENT_ID == "YOUR_OKTA_CLIENT_ID":
            return None, (
                "Okta is not configured. "
                "Please set OKTA_DOMAIN and OKTA_CLIENT_ID in authentication/okta_provider.py."
            )

        _OktaCallbackHandler.captured_code = None
        verifier, challenge = _generate_pkce_pair()

        # Build Okta authorization URL
        auth_url = (
            f"https://{OKTA_DOMAIN}/oauth2/default/v1/authorize?"
            + urllib.parse.urlencode({
                "response_type":         "code",
                "client_id":             OKTA_CLIENT_ID,
                "redirect_uri":          REDIRECT_URI,
                "scope":                 SCOPES,
                "code_challenge":        challenge,
                "code_challenge_method": "S256",
                "state":                 secrets.token_hex(16),
            })
        )

        # Start local callback server
        httpd = HTTPServer(("127.0.0.1", CALLBACK_PORT), _OktaCallbackHandler)
        server_thread = threading.Thread(target=httpd.serve_forever)
        server_thread.daemon = True
        server_thread.start()

        # Open browser for user login
        webbrowser.open(auth_url)

        # Wait for the callback (5-minute timeout)
        server_thread.join(timeout=300)

        if not _OktaCallbackHandler.captured_code:
            return None, "Okta login timed out or was cancelled by the user."

        # Exchange authorization code for access token
        return self._exchange_code_for_token(_OktaCallbackHandler.captured_code, verifier)

    def _exchange_code_for_token(self, code: str, verifier: str) -> tuple[str | None, str]:
        """Exchange the OAuth authorization code for an access token via Okta token endpoint."""
        token_url  = f"https://{OKTA_DOMAIN}/oauth2/default/v1/token"
        token_body = urllib.parse.urlencode({
            "grant_type":    "authorization_code",
            "client_id":     OKTA_CLIENT_ID,
            "code_verifier": verifier,
            "code":          code,
            "redirect_uri":  REDIRECT_URI,
        }).encode("utf-8")

        req = urllib.request.Request(
            token_url,
            data=token_body,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        try:
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                # Prefer access_token; fall back to id_token for userinfo calls
                return data.get("access_token") or data.get("id_token"), "Login successful."
        except Exception as e:
            detail = getattr(e, "read", lambda: b"Unknown error")().decode()
            return None, f"Token exchange failed: HTTP {getattr(e, 'code', 'Error')} — {detail}"

    def verify_token(self, token: str) -> dict | None:
        """
        Verify an Okta access token via the /userinfo endpoint.
        Returns the user's profile dict on success, or None if invalid/expired.
        """
        url = f"https://{OKTA_DOMAIN}/oauth2/default/v1/userinfo"
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
        try:
            with urllib.request.urlopen(req, timeout=5) as resp:
                return json.loads(resp.read().decode())
        except Exception:
            return None
