class ResolverError(Exception):
    """Base error for the resource resolver pipeline."""

class ResourceNotFoundError(ResolverError):
    """No resource matched the query in cache, registry, or CMDB."""

class InvalidIdentifierError(ResolverError):
    """The supplied identifier or identifier type is invalid."""

class EndpointNotFoundError(ResolverError):
    """No endpoint_registry row matches the requested (vendor, action_key) pair."""

class UnsupportedManagementSourceError(ResolverError):
    """The management source is unsupported or invalid."""
    def __init__(self, management_source: str, message: str = ""):
        self.management_source = management_source
        super().__init__(message or f"Unsupported management source: {management_source}")

class InvalidCMDBRecordError(ResolverError):
    """The CMDB record has missing or invalid fields."""

