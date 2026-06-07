import logging
import os
from records import DeviceRecord, RouteResolution
from protocol_discovery import normalize_management_source

logger = logging.getLogger(__name__)


class OneViewHandler:
    """Handler for HPE OneView operations on generalized infrastructure."""

    def execute(self, context: dict) -> dict:
        logger.info(
            "[Execution] OneView Handler invoking endpoint %s for action %s",
            context["api_endpoint"],
            context["action"],
        )
        return {
            "status": "success",
            "handler": "ONEVIEW",
            "action": context["action"],
            "api_endpoint": context["api_endpoint"],
        }


class ComsHandler:
    """Handler for HPE COMS operations on generalized infrastructure."""

    def execute(self, context: dict) -> dict:
        logger.info(
            "[Execution] COMS Handler invoking endpoint %s for action %s",
            context["api_endpoint"],
            context["action"],
        )
        return {
            "status": "success",
            "handler": "COMS",
            "action": context["action"],
            "api_endpoint": context["api_endpoint"],
        }


class ExecutionOrchestrator:
    """
    Modular, extensible execution orchestrator for infrastructure routing.
    Handles operational execution by dispatching to registered handlers.
    """

    def __init__(self) -> None:
        self._handlers = {}
        # Register default OASF management source handlers
        self.register_handler("oneview", OneViewHandler())
        self.register_handler("coms", ComsHandler())

    def register_handler(self, name: str, handler: object) -> None:
        self._handlers[name.lower()] = handler

    def build_execution_context(self, route: RouteResolution, action: str, category: str) -> dict:
        """Construct the execution context payload, resolving endpoints dynamically."""
        device = route.device
        source = normalize_management_source(device.management_source)

        # Build API endpoint base on mock port
        mock_port = os.getenv("MOCK_AGENT_PORT")
        mock_host = os.getenv("MOCK_AGENT_HOST", "localhost")

        if mock_port:
            host = f"{mock_host}:{mock_port}"
            scheme = "http"
        else:
            host = device.source_host or "localhost"
            scheme = "https"

        uuid = device.source_device_id or device.id
        device_type = (device.device_type or "").strip().lower()

        if source == "oneview":
            if device_type == "switch":
                endpoint = f"{scheme}://{host}/rest/v1/switches/{uuid}"
            elif device_type == "router":
                endpoint = f"{scheme}://{host}/rest/v1/routers/{uuid}"
            elif device_type == "firewall":
                endpoint = f"{scheme}://{host}/rest/v1/firewalls/{uuid}"
            elif device_type == "storage":
                endpoint = f"{scheme}://{host}/rest/v1/storage-systems/{uuid}"
            elif device_type == "server":
                endpoint = f"{scheme}://{host}/rest/v1/server-hardware/{uuid}"
            else:
                endpoint = f"{scheme}://{host}/rest/v1/devices/{uuid}"
        elif source == "coms":
            if device_type == "switch":
                endpoint = f"{scheme}://{host}/compute-ops/v1/switches/{uuid}"
            elif device_type == "router":
                endpoint = f"{scheme}://{host}/compute-ops/v1/routers/{uuid}"
            elif device_type == "firewall":
                endpoint = f"{scheme}://{host}/compute-ops/v1/firewalls/{uuid}"
            elif device_type == "storage":
                endpoint = f"{scheme}://{host}/compute-ops/v1/storage-systems/{uuid}"
            elif device_type == "server":
                endpoint = f"{scheme}://{host}/compute-ops/v1/servers/{uuid}"
            else:
                endpoint = f"{scheme}://{host}/compute-ops/v1/devices/{uuid}"
        else:
            endpoint = f"{scheme}://{host}/rest/v1/devices/{uuid}"

        return {
            "management_source": source.upper(),
            "source_host": device.source_host,
            "api_endpoint": endpoint,
            "action": action,
            "category": category,
            "serial_number": device.serial_number,
            "credential_ref": route.credential_ref,
            "device_type": device_type or None,
        }

    def execute_operation(self, context: dict) -> dict:
        """Route the operation to the correct registered management source handler."""
        source = context["management_source"].lower()
        handler = self._handlers.get(source)
        if handler is not None:
            return handler.execute(context)
        else:
            raise ValueError(f"Unsupported management source for execution: {context['management_source']}")



