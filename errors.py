class ResolverError(Exception):
    """Base error for the resource resolver pipeline."""

class ResourceNotFoundError(ResolverError):
    """No resource matched the query in cache, registry, or CMDB."""

class InvalidIdentifierError(ResolverError):
    """The supplied identifier or identifier type is invalid."""

class EndpointNotFoundError(ResolverError):
    """No endpoint_registry row matches the requested (vendor, action_key) pair."""
