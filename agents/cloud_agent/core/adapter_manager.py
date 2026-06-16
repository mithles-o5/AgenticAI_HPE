"""AdapterManager — dynamically selects and instantiates the correct cloud adapter.

Adding a new provider requires only:
  1. Subclass BaseCloudAdapter in adapters/plugins/<name>_adapter.py
  2. Register it in the REGISTRY dict below.
"""

from __future__ import annotations
from typing import Dict, Type

from adapters.base import BaseCloudAdapter
from adapters.plugins.mock_adapter import MockCloudAdapter
from adapters.plugins.aws_adapter import AWSCloudAdapter
from adapters.plugins.azure_adapter import AzureCloudAdapter
from adapters.plugins.gcp_adapter import GCPCloudAdapter

# ── Provider Registry ─────────────────────────────────────────────────────────
# Key: provider label as sent in TaskRequest.provider (lower-case)
# Value: adapter class (instantiated lazily)
REGISTRY: Dict[str, Type[BaseCloudAdapter]] = {
    "mock":       MockCloudAdapter,
    "aws":        AWSCloudAdapter,
    "azure":      AzureCloudAdapter,
    "gcp":        GCPCloudAdapter,
    # Add on-prem adapters here — e.g. "openstack": OpenStackAdapter
}


class AdapterManager:
    """Selects and returns an adapter instance for a given provider string."""

    @staticmethod
    def get(provider: str) -> BaseCloudAdapter:
        key = provider.strip().lower()
        cls = REGISTRY.get(key)
        if cls is None:
            known = sorted(REGISTRY.keys())
            raise ValueError(
                f"No adapter registered for provider '{provider}'. "
                f"Registered providers: {known}"
            )
        return cls()

    @staticmethod
    def registered_providers() -> list[str]:
        return sorted(REGISTRY.keys())
