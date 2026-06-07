class ResolverError(Exception):
    """Base error for the resource resolver pipeline."""

class ResourceNotFoundError(ResolverError):
    """No resource matched the query in cache, registry, or CMDB."""

class InvalidIdentifierError(ResolverError):
    """The supplied identifier or identifier type is invalid."""


