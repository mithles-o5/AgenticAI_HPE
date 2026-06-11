from abc import ABC, abstractmethod

class BaseAdapter(ABC):
    @abstractmethod
    async def health_check(self, resource_type: str, resource_id: str, credentials: dict, parameters: dict) -> dict:
        """Perform health check on the specified resource."""
        pass

    @abstractmethod
    async def fetch_metrics(self, resource_type: str, resource_id: str, credentials: dict, parameters: dict) -> dict:
        """Fetch real-time or historical metrics for the specified resource."""
        pass

    @abstractmethod
    async def fetch_alerts(self, resource_type: str, resource_id: str, credentials: dict, parameters: dict) -> list:
        """Fetch alert logs for the specified resource."""
        pass

    @abstractmethod
    async def execute_action(self, resource_type: str, resource_id: str, credentials: dict, parameters: dict) -> dict:
        """Execute lifecycle actions (power actions, firmware updates, profile assignment)."""
        pass

    @abstractmethod
    async def discover_inventory(self, resource_type: str, credentials: dict, parameters: dict) -> list:
        """Discover and list all on-premises resources of the specified type."""
        pass

    @abstractmethod
    async def sync_cmdb(self, credentials: dict, parameters: dict) -> dict:
        """Fetch inventory metadata suitable for syncing to CMDB."""
        pass
