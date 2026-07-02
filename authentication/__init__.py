"""
authentication/__init__.py
==========================
Provider Registry — controls which SSO provider is active.

ALL providers use browser-based PKCE OAuth 2.0 (no credentials in chat).

TO SWITCH PROVIDERS:
    Change the PROVIDER variable to one of:
        "auth0"  → Auth0 PKCE       (ready to use)
        "okta"   → Okta PKCE        (fill in OKTA_DOMAIN + OKTA_CLIENT_ID in okta_provider.py)

TO ADD A NEW PROVIDER:
    1. Create `my_provider.py` in this folder
    2. Subclass SSOProvider and implement login() + verify_token()
    3. Import it below and add an entry to PROVIDER_REGISTRY
    4. Set PROVIDER = "my_provider"
"""

from authentication.auth0_provider import Auth0Provider
from authentication.okta_provider  import OktaProvider
from authentication.local_provider import LocalProvider

# ─────────────────────────────────────────────────────────────────────────────
# Active Provider Selection
# Change this to switch between SSO providers
# ─────────────────────────────────────────────────────────────────────────────

PROVIDER = "local"

# ─────────────────────────────────────────────────────────────────────────────
# Provider Registry
# ─────────────────────────────────────────────────────────────────────────────

PROVIDER_REGISTRY = {
    "auth0": Auth0Provider,
    "okta" : OktaProvider,
    "local": LocalProvider
}

def get_provider(name: str = PROVIDER, **kwargs):
    """
    Factory function — returns an instance of the requested SSO provider.

    Args:
        name   : Provider key (default = PROVIDER)
        kwargs : Extra args passed to the provider constructor
                 (e.g. username/password for LocalProvider)

    Returns:
        An instance of the selected SSOProvider subclass.

    Raises:
        ValueError: If the provider name is not registered.
    """
    cls = PROVIDER_REGISTRY.get(name)
    if not cls:
        available = ", ".join(PROVIDER_REGISTRY.keys())
        raise ValueError(
            f"Unknown SSO provider '{name}'. Available: {available}"
        )
    return cls(**kwargs)
