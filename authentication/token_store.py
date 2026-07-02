"""
token_store.py
==============
Secure, interoperable, zero-dependency token storage for SSO tokens.

This module is completely cross-platform (Windows, Mac, Linux) and does
NOT depend on any external OS-specific credential managers.

Storage layers:
  1. IN-MEMORY : Fastest, exists only in RAM for the life of the process.
  2. LOCAL FILE: Saves to `.mcp_session` (JSON) with strict file permissions.
  3. ENV VAR   : AUTHZ_ID_TOKEN from Claude Desktop config (for headless deployments).

Session file format (JSON):
  {
    "token"    : "<access token string>",
    "provider" : "okta"   ← which SSO provider issued this token
  }

WHY WE STORE THE PROVIDER:
  Each SSO provider has its own /userinfo endpoint for token verification.
  An Okta token cannot be verified by calling Auth0's /userinfo — they are
  completely different services.  Storing the provider alongside the token
  ensures that verify_token() always calls the correct endpoint, regardless
  of which provider is set as the default in __init__.py.
"""

import os
import json
import stat

# The .mcp_session file lives next to the MCP server
_SESSION_FILE = os.path.join(
    os.path.dirname(__file__),   # authentication/
    "..",                        # MCP_Integrated/
    "mcp_server",
    ".mcp_session"
)
SESSION_FILE = os.path.normpath(_SESSION_FILE)

# ─────────────────────────────────────────────────────────────────────────────
# Layer 1: In-Memory Store
# ─────────────────────────────────────────────────────────────────────────────

_MEMORY_STORE: dict = {"token": None, "provider": None}


# ─────────────────────────────────────────────────────────────────────────────
# Layer 2: Secure File Storage (JSON)
# ─────────────────────────────────────────────────────────────────────────────

def _save_to_file(token: str, provider: str) -> None:
    """Saves the token + provider to a JSON session file and locks permissions."""
    from datetime import date
    payload = json.dumps({
        "token": token,
        "provider": provider,
        "date": date.today().isoformat()
    })
    with open(SESSION_FILE, "w") as f:
        f.write(payload)

    # Restrict file permissions to Owner Read/Write only (0o600)
    try:
        os.chmod(SESSION_FILE, stat.S_IRUSR | stat.S_IWUSR)
    except Exception:
        pass  # Failsafe on some restrictive Windows environments


def _load_from_file() -> tuple[str | None, str | None]:
    """Loads token + provider from the secure session file.
    Returns (token, provider) or (None, None) if missing/corrupt or expired today.
    """
    if not os.path.exists(SESSION_FILE):
        return None, None
    try:
        from datetime import date
        with open(SESSION_FILE, "r") as f:
            data = json.loads(f.read().strip())
        
        # Verify if session was created on a different day
        session_date_str = data.get("date")
        if session_date_str and session_date_str != date.today().isoformat():
            # Invalidate session file automatically on date change
            _clear_file()
            return None, None

        token    = data.get("token", "").strip() or None
        provider = data.get("provider", "").strip() or None
        return token, provider
    except Exception:
        return None, None


def _clear_file() -> None:
    """Deletes the session file."""
    if os.path.exists(SESSION_FILE):
        try:
            os.remove(SESSION_FILE)
        except Exception:
            pass


# ─────────────────────────────────────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────────────────────────────────────

def save_token(token: str, provider: str) -> None:
    """
    Save the token and the provider name after a successful SSO login.
    Saves to both RAM and the secure local session file.

    Args:
        token    : The access token string returned by the SSO provider.
        provider : The provider key used for login (e.g. 'okta', 'auth0').
    """
    token    = token.strip()
    provider = provider.strip().lower()
    _MEMORY_STORE["token"]    = token
    _MEMORY_STORE["provider"] = provider
    _save_to_file(token, provider)


def load_token() -> str:
    """
    Load the active SSO token.

    Priority:
      1. In-memory store (RAM)
      2. Secure local file (.mcp_session)
      3. AUTHZ_ID_TOKEN environment variable (no provider context — treated as 'auth0')

    Raises:
      ValueError: If no active session is found.
    """
    # 1. Memory
    token = _MEMORY_STORE.get("token")
    if token:
        return token

    # 2. Secure File
    token, provider = _load_from_file()
    if token:
        _MEMORY_STORE["token"]    = token
        _MEMORY_STORE["provider"] = provider
        return token

    # 3. Environment Variable (legacy / headless deployments)
    token = os.environ.get("AUTHZ_ID_TOKEN", "").strip()
    if token:
        _MEMORY_STORE["token"]    = token
        _MEMORY_STORE["provider"] = os.environ.get("AUTHZ_PROVIDER", "auth0").strip()
        return token

    raise ValueError(
        "No active session found. Login required.\n"
        "Please choose a provider: auth0, okta, or local."
    )


def load_provider() -> str | None:
    """
    Return the SSO provider that issued the current active token.

    Returns the provider key (e.g. 'okta', 'auth0') or None
    if no session exists yet.

    This is used by mcp_server.py to verify a token with the SAME provider
    that originally issued it — so an Okta token is verified via Okta's
    /userinfo, not Auth0's.
    """
    # 1. Memory (fastest path)
    provider = _MEMORY_STORE.get("provider")
    if provider:
        return provider

    # 2. File (e.g. server was restarted between calls)
    _, provider = _load_from_file()
    if provider:
        _MEMORY_STORE["provider"] = provider
        return provider

    # 3. Environment variable fallback
    return os.environ.get("AUTHZ_PROVIDER", None)


def clear_token() -> None:
    """
    Clear the token and provider from all storage layers (logout).
    """
    _MEMORY_STORE["token"]    = None
    _MEMORY_STORE["provider"] = None
    _clear_file()


def has_token() -> bool:
    """
    Quick check: is there an active token without raising an error?
    """
    try:
        load_token()
        return True
    except ValueError:
        return False
