"""Storage Agent cred vault client."""

from __future__ import annotations
import httpx
from typing import Any, Dict
from config.settings import settings


class CredVaultClient:
    def get(self, ref: str) -> Dict[str, Any]:
        if not ref:
            return {}
        url = f"{settings.CRED_VAULT_URL}/secret/{ref}"
        headers = {"Authorization": f"Bearer {settings.SERVICE_TOKEN}"}
        with httpx.Client(timeout=10.0) as client:
            resp = client.get(url, headers=headers)
            resp.raise_for_status()
            return resp.json()
