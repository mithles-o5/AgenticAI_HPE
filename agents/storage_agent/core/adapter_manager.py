"""Storage AdapterManager."""

from __future__ import annotations
from typing import Dict, Type
from adapters.base import BaseStorageAdapter
from adapters.plugins.mock_adapter import MockStorageAdapter
from adapters.plugins.dscc_adapter import DSCCStorageAdapter
from adapters.plugins.nas_adapter import NASStorageAdapter
from adapters.plugins.s3_adapter import S3StorageAdapter

REGISTRY: Dict[str, Type[BaseStorageAdapter]] = {
    "mock": MockStorageAdapter,
    "mock_storage": MockStorageAdapter,
    "dscc": DSCCStorageAdapter,
    "coms": DSCCStorageAdapter,
    "nas":  NASStorageAdapter,
    "s3":   S3StorageAdapter,
}


class StorageAdapterManager:
    @staticmethod
    def get(provider: str) -> BaseStorageAdapter:
        key = provider.strip().lower()
        cls = REGISTRY.get(key)
        if cls is None:
            raise ValueError(f"No storage adapter for provider '{provider}'. Known: {sorted(REGISTRY)}")
        return cls()

    @staticmethod
    def registered_providers() -> list[str]:
        return sorted(REGISTRY.keys())
