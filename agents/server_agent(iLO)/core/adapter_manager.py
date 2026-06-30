import structlog
from typing import Dict, Any, Type
from adapters.base import ServerAdapter
from adapters.plugins.redfish_adapter import RedfishAdapter
from adapters.plugins.ilo_adapter import ILOAdapter
from adapters.plugins.mock_adapter import MockAdapter
from core.cred_vault_client import CredVaultClient

logger = structlog.get_logger()

REGISTRY: Dict[str, Type[ServerAdapter]] = {
    "redfish": RedfishAdapter,
    "ilo": ILOAdapter,
    "mock_server": MockAdapter,
    "default": MockAdapter,
}

def get_adapter(provider: str, credentials_ref: str) -> ServerAdapter:
    """
    Select adapter by provider string.
    Pull credentials from Cred Vault using credentials_ref.
    Instantiate and return the adapter with credentials injected.
    Fall back to MockAdapter if provider not in registry.
    """
    prov_clean = provider.strip().lower()
    
    # Fetch credentials
    vault_client = CredVaultClient()
    credentials = vault_client.get(credentials_ref)
    
    adapter_class = REGISTRY.get(prov_clean)
    if not adapter_class:
        logger.warning(
            "Unknown provider, falling back to MockAdapter",
            provider=provider,
            credentials_ref=credentials_ref
        )
        adapter_class = MockAdapter
        
    logger.info(
        "Selected server adapter",
        provider=provider,
        adapter_class=adapter_class.__name__
    )
    
    # If credentials_ref is mock or provider is mock/default, return MockAdapter
    if credentials_ref == "mock" or prov_clean in ("mock", "default") or not adapter_class:
        return MockAdapter()
        
    return adapter_class(credentials)
