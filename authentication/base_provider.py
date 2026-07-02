"""
base_provider.py
================
Abstract base class for all SSO providers.
Every new SSO provider (Auth0, Okta, etc.) must inherit
from SSOProvider and implement the two abstract methods below.
"""

from abc import ABC, abstractmethod


class SSOProvider(ABC):
    """
    Base interface for all SSO providers.

    To add a new provider:
        1. Create a new file e.g. `okta_provider.py`
        2. Subclass SSOProvider
        3. Implement `login()` and `verify_token()`
        4. Register it in `__init__.py`
    """

    @abstractmethod
    def login(self) -> tuple[str | None, str]:
        """
        Trigger the login flow for this provider.

        Returns:
            (token, message)
            - token  : Access token string on success, None on failure
            - message: Human-readable status message
        """
        ...

    @abstractmethod
    def verify_token(self, token: str) -> dict | None:
        """
        Verify a token issued by this provider.

        Returns:
            dict of user claims (email, sub, name, etc.) on success,
            or None if the token is invalid/expired.
        """
        ...
