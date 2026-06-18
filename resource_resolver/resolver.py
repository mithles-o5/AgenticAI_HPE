"""Resource resolver API: identifier to MCP routing context."""

from __future__ import annotations

import ipaddress
import logging
import time
from typing import Optional

from cache import ResourceCache
from enums import CacheStatus, IdentifierType
from errors import InvalidIdentifierError, ResourceNotFoundError, UnsupportedManagementSourceError, InvalidCMDBRecordError
from records import RouteResolution
from registry import ResourceRegistry
from protocol_discovery import discover_route

logger = logging.getLogger(__name__)


class ResourceResolver:
    """Resolve IP, serial number, or FQDN to the owning management source."""

    def __init__(self, registry: ResourceRegistry, cache: ResourceCache) -> None:
        self.registry = registry
        self.cache = cache

    def resolve(
        self,
        parsed_payload: dict,
        identifier_type: str | IdentifierType | None = None,
        requested_by: Optional[str] = None,
    ) -> RouteResolution:
        start = time.perf_counter()
        identifier = parsed_payload.get("identifier", "").strip()
        action = parsed_payload.get("action", "STATUS")
        category = parsed_payload.get("category", "Operational")

        normalized_identifier = self._normalize_identifier(identifier)
        normalized_type = self._normalize_identifier_type(
            identifier_type,
            normalized_identifier,
        )

        device, cache_status = self.cache.get_by_identifier(
            normalized_identifier,
            normalized_type,
        )
        cache_hit = cache_status == CacheStatus.HIT

        if device is None:
            device = self.registry.lookup(normalized_identifier, normalized_type)
            if device is not None:
                logger.info(
                    "[Resolver] Warming Memurai cache | sn=%s",
                    device.serial_number,
                )
                self.cache.put_device(device)
                logger.info(
                    "[Resolver] Memurai cache warm complete | sn=%s",
                    device.serial_number,
                )

        resolution_ms = int((time.perf_counter() - start) * 1000)

        if device is None:
            self.registry.log_routing_audit(
                identifier=normalized_identifier,
                identifier_type=normalized_type,
                resolved_source=None,
                resolved_host=None,
                cache_hit=cache_hit,
                resolution_ms=resolution_ms,
                requested_by=requested_by,
            )
            raise ResourceNotFoundError(
                f"No device found for {normalized_type.value} '{normalized_identifier}'"
            )

        # 1. CMDB Record Validation
        if not device.serial_number or not device.management_source or not device.device_type:
            logger.error(
                "[Resolver] CMDB Record Validation failed: missing required fields for device (serial_number=%r, management_source=%r, device_type=%r)",
                device.serial_number, device.management_source, device.device_type
            )
            raise InvalidCMDBRecordError(
                f"CMDB record invalid: missing serial_number, management_source, or device_type"
            )

        # 2. Management Source Validation
        supported_sources = {"oneview", "coms", "mock_server", "mock_storage", "mock_network", "mock_cloud"}
        source_normalized = (device.management_source or "").strip().lower()
        if source_normalized not in supported_sources:
            logger.error(
                "[Resolver] Unsupported management source: %r for device serial_number=%s",
                device.management_source, device.serial_number
            )
            raise UnsupportedManagementSourceError(
                management_source=device.management_source or ""
            )

        mcp_tool, credential_ref = discover_route(device.management_source, device.source_host)

        # Build execution/routing context using ExecutionOrchestrator
        from power_ops import ExecutionOrchestrator
        executor = ExecutionOrchestrator()
        
        # Build temp resolution for context builder
        temp_resolution = RouteResolution(
            identifier=normalized_identifier,
            identifier_type=normalized_type,
            device=device,
            mcp_tool=mcp_tool,
            credential_ref=credential_ref,
            cache_status=cache_status,
            resolution_ms=resolution_ms,
            api_endpoint="",
            management_source=device.management_source,
            resource={},
            action={}
        )
        exec_ctx = executor.build_execution_context(temp_resolution, action, category)

        result = RouteResolution(
            identifier=normalized_identifier,
            identifier_type=normalized_type,
            device=device,
            mcp_tool=mcp_tool,
            credential_ref=credential_ref,
            cache_status=cache_status,
            resolution_ms=resolution_ms,
            api_endpoint=exec_ctx["api_endpoint"],
            management_source=device.management_source,
            resource={
                "name": device.fqdn or device.serial_number,
                "vendor": "HPE"
            },
            action={
                "category": exec_ctx["category"],
                "action": exec_ctx["action"]
            }
        )

        self.registry.log_routing_audit(
            identifier=normalized_identifier,
            identifier_type=normalized_type,
            resolved_source=device.management_source,
            resolved_host=device.source_host,
            cache_hit=cache_hit,
            resolution_ms=resolution_ms,
            requested_by=requested_by,
        )
        logger.info(
            "[Resolver] %s:%s -> %s/%s cache=%s %sms",
            normalized_type.value,
            normalized_identifier,
            device.management_source,
            device.source_host,
            cache_status.value,
            resolution_ms,
        )
        return result


    @staticmethod
    def _normalize_identifier(identifier: str) -> str:
        value = (identifier or "").strip()
        if not value:
            raise InvalidIdentifierError("identifier is required")
        return value

    @classmethod
    def _normalize_identifier_type(
        cls,
        identifier_type: str | IdentifierType | None,
        identifier: str,
    ) -> IdentifierType:
        if isinstance(identifier_type, IdentifierType):
            return identifier_type
        if identifier_type:
            value = identifier_type.strip().lower()
            aliases = {
                "ip": IdentifierType.IP,
                "ip_address": IdentifierType.IP,
                "serial": IdentifierType.SERIAL_NUMBER,
                "serial_number": IdentifierType.SERIAL_NUMBER,
                "sn": IdentifierType.SERIAL_NUMBER,
                "fqdn": IdentifierType.FQDN,
                "hostname": IdentifierType.FQDN,
            }
            if value in aliases:
                resolved = aliases[value]
                # Cross-validate: FQDN requires at least one dot in the identifier.
                # If the caller (e.g. an LLM) passes identifier_type="fqdn" for a
                # dotless token like "sge-vm-1000" or "rack41-compute-1-10140",
                # that hint is wrong — fall back to inference so the lookup
                # runs as serial-number instead of failing silently as FQDN.
                if resolved is IdentifierType.FQDN and "." not in identifier:
                    logger.debug(
                        "[Resolver] identifier_type='fqdn' overridden → inferred type "
                        "because identifier %r has no dot",
                        identifier,
                    )
                    return cls._infer_identifier_type(identifier)
                return resolved
            raise InvalidIdentifierError(f"unsupported identifier_type '{identifier_type}'")
        return cls._infer_identifier_type(identifier)

    @staticmethod
    def _infer_identifier_type(identifier: str) -> IdentifierType:
        try:
            ipaddress.ip_address(identifier)
            return IdentifierType.IP
        except ValueError:
            pass
        if "." in identifier:
            return IdentifierType.FQDN
        return IdentifierType.SERIAL_NUMBER
