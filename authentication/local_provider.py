"""
local_provider.py
=================
Local JWT SSO Provider for development and testing purposes.

This provider does NOT contact any external identity service.
It validates a username/password against a local dictionary and
issues a signed HS256 JWT token — useful for offline testing
or as a fallback when real SSO providers are unavailable.

WARNING: Do not use in production. Replace with a real provider.
"""

import jwt
import datetime

from base_provider import SSOProvider


# ─────────────────────────────────────────────────────────────────────────────
# Local Configuration
# ─────────────────────────────────────────────────────────────────────────────

LOCAL_SECRET_KEY  = "my_secret_key"     # Must match authorization/utils.py → SECRET_KEY
TOKEN_EXPIRY_MINS = 30

# Local user database: { username: (password, role, email) }
# ─────────────────────────────────────────────────────────────────────────────
# IMPORTANT: Add users here AND in authorization/roles.json.
#   The email MUST match the key in roles.json for role lookup to work.
#   Format: "username": ("password", "HPE role name", "email@domain")
# ─────────────────────────────────────────────────────────────────────────────
LOCAL_USERS = {
    # ── Matches roles.json entries ──
    "dsksr19":   ("password123",  "Storage administrator",        "dsksr19@gmail.com"),
    "devasksr":  ("password123",  "Infrastructure administrator", "devasksr@gmail.com"),
    "mithles2k05": ("password123", "Storage administrator", "mithles2k05@gmail.com"),
    "mithles":   ("password123", "Infrastructure administrator", "mithles@student.tce.edu"),

    # ── Additional dev/test accounts (add to roles.json if needed) ──
    "infra_admin":  ("admin123",  "Infrastructure administrator", "infra_admin@local.dev"),
    "net_admin":    ("admin123",  "Network administrator",        "net_admin@local.dev"),
    "server_admin": ("admin123",  "Server administrator",         "server_admin@local.dev"),
    "storage_admin":("admin123",  "Storage administrator",        "storage_admin@local.dev"),
    "backup_admin": ("admin123",  "Backup administrator",         "backup_admin@local.dev"),
    "fw_operator":  ("admin123",  "Server firmware operator",     "fw_operator@local.dev"),
    "readonly":     ("readonly1", "Read only",                    "readonly@local.dev"),
}


# ─────────────────────────────────────────────────────────────────────────────
# Local SSO Provider
# ─────────────────────────────────────────────────────────────────────────────

class LocalProvider(SSOProvider):
    """
    SSO Provider using a local username/password store.
    Issues signed JWT tokens for offline/testing use only.

    Usage:
        provider = LocalProvider(username="admin", password="admin123")
        token, message = provider.login()
        user = provider.verify_token(token)
    """

    def __init__(self, username: str = "", password: str = ""):
        self.username = username
        self.password = password

    def login(self) -> tuple[str | None, str]:
        """
        Validate credentials against LOCAL_USERS and return a signed JWT.
        The JWT's 'email' claim is set to the user's registered email so that
        it matches the key in authorization/roles.json.
        """
        user = LOCAL_USERS.get(self.username)
        if not user or user[0] != self.password:
            return None, f"Invalid username or password for local provider."

        _, role, email = user
        token = jwt.encode(
            {
                "user":  self.username,
                "email": email,
                "role":  role,
                "exp":   datetime.datetime.utcnow() + datetime.timedelta(minutes=TOKEN_EXPIRY_MINS),
            },
            LOCAL_SECRET_KEY,
            algorithm="HS256"
        )
        return token, f"Local login successful. Role: {role}"

    def verify_token(self, token: str) -> dict | None:
        """
        Verify a locally issued JWT token.
        Returns the payload dict on success, or None if invalid/expired.
        """
        try:
            return jwt.decode(token, LOCAL_SECRET_KEY, algorithms=["HS256"])
        except Exception:
            return None
