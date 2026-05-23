class ResolverError(Exception):
    """Base error for the resource resolver pipeline."""

class ResourceNotFoundError(ResolverError):
    """No resource matched the query in cache, registry, or CMDB."""

class ProtocolError(ResolverError):
    """Protocol handler encountered an unrecoverable error."""

class TaskTimeoutError(ResolverError):
    """Async task (e.g. HPE OneView) did not complete within the timeout."""

class CredentialError(ResolverError):
    """Credential reference missing or vault lookup failed."""

class ActionClassificationError(ResolverError):
    """Unable to classify the requested action as Operational."""
