import logging
from adapters.plugins.oneview_adapter import OneViewAdapter
from adapters.plugins.com_adapter import ComOpsAdapter
from adapters.plugins.mock_adapter import MockAdapter
from core.exceptions import AdapterError

logger = logging.getLogger("onprem_agent.adapter_manager")

class AdapterManager:
    def __init__(self):
        self._oneview = OneViewAdapter()
        self._com = ComOpsAdapter()
        self._mock = MockAdapter()

    def get_adapter(self, provider: str):
        """
        Returns the appropriate adapter plugin.
        Strictly raises a ValueError if provider is 'default' or not provided.
        """
        if not provider or provider == "default":
            raise ValueError("Provider must be supplied (e.g. 'oneview', 'com' or 'mock')")

        prov = provider.lower().strip()
        if prov == "oneview":
            return self._oneview
        elif prov in ("com", "composable", "coms"):
            return self._com
        elif prov == "mock_onprem":
            return self._mock
        else:
            raise AdapterError(f"Unsupported provider '{provider}'")
