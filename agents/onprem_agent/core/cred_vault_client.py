import os
import httpx
import logging
from core.exceptions import CredentialError

logger = logging.getLogger("onprem_agent.cred_vault")

class CredVaultClient:
    def get(self, ref: str) -> dict:
        url = os.getenv("CRED_VAULT_URL")
        token = os.getenv("SERVICE_TOKEN")
        if not url or url.startswith("mock") or "localhost:8002" in url:
            logger.warning("CRED_VAULT_URL missing or matches dev URL, using local testing credentials")
            # Returns standard dictionary format matching expected vault responses
            return {
                "username": "administrator",
                "password": "password123",
                "host": "localhost",
                "verify_ssl": False,
                "token": "test-session-token-123"
            }
        
        try:
            response = httpx.get(
                f"{url}/secret/{ref}",
                headers={"Authorization": f"Bearer {token}"},
                timeout=10.0
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error fetching secret from CredVault for ref '{ref}': {e}")
            raise CredentialError(f"Failed to fetch credentials from Vault: {e}") from e
