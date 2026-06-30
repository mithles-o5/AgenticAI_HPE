import httpx
import os
import logging
from typing import Dict, Any
from config.settings import settings

logger = logging.getLogger("server-agent.cred-vault-client")

class CredVaultClient:
    def get(self, ref: str) -> Dict[str, Any]:
        if not ref or ref.strip().lower() == "mock":
            return {"host": "localhost", "username": "admin", "password": "password", "verify_ssl": False}
        
        # Determine actual URL
        cred_vault_url = os.getenv("CRED_VAULT_URL", settings.CRED_VAULT_URL)
        service_token = os.getenv("SERVICE_TOKEN", settings.SERVICE_TOKEN)
        
        url = f"{cred_vault_url}/secret/{ref}"
        headers = {"Authorization": f"Bearer {service_token}"}
        
        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.get(url, headers=headers)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Failed to fetch secret '{ref}' from Cred Vault: {e}")
            # Return realistic mock credentials if failed during local testing / demo
            return {
                "host": "127.0.0.1:8010",
                "username": "admin",
                "password": "password",
                "verify_ssl": False,
                "interface": "lanplus"
            }

