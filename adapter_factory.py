from typing import Dict
from adapters.base_adapter import BaseAdapter
from adapters.oneview_adapter import OneViewAdapter
from adapters.com_adapter import COMAdapter

class AdapterFactory:
    """
    Factory for resolving and instantiating the correct management platform adapter.
    """

    @classmethod
    def get(cls, management_source: str, poll_interval: float = 1.0, poll_timeout: float = 30.0) -> BaseAdapter:
        """
        Returns an instance of BaseAdapter for the specified management source.
        Supports configuring task polling parameters.
        Raises ValueError if the management source is unsupported.
        """
        source_key = str(management_source).upper().strip()
        
        if source_key == "ONEVIEW":
            return OneViewAdapter(poll_interval=poll_interval, poll_timeout=poll_timeout)
        elif source_key == "COM":
            return COMAdapter(poll_interval=poll_interval, poll_timeout=poll_timeout)
        else:
            raise ValueError(f"Unsupported management source: '{management_source}'")
