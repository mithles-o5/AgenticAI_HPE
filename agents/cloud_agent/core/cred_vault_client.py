"""CredVaultClient — fetches runtime credentials from the Credential Vault service.

Agents NEVER store credentials. Every call fetches the secret fresh from
the vault using the reference string passed in the TaskRequest.
"""

from __future__ import annotations
import os
import httpx
from typing import Any, Dict

from config.settings import settings


class CredVaultClient:
    """Thin HTTP client for the Credential Vault service."""

    def get(self, ref: str) -> Dict[str, Any]:
        """
        Retrieve the secret identified by *ref* from the Credential Vault.

        Returns a dict of credential key-value pairs.
        Raises httpx.HTTPStatusError on auth/not-found errors.
        """
        if not ref:
            return {}           # No ref → unauthenticated / mock path

        url = f"{settings.CRED_VAULT_URL}/secret/{ref}"
        headers = {"Authorization": f"Bearer {settings.SERVICE_TOKEN}"}

        with httpx.Client(timeout=10.0) as client:
            response = client.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
