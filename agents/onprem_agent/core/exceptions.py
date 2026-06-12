class AgentError(Exception):
    """Base exception class for On-Prem Agent."""
    pass

class AdapterError(AgentError):
    """Raised when an operation on a vendor adapter fails."""
    pass

class CredentialError(AgentError):
    """Raised when fetching or parsing credentials from Vault fails."""
    pass

class NormalizationError(AgentError):
    """Raised when normalising response payload fails."""
    pass

class SkillError(AgentError):
    """Raised when skill validation or execution fails."""
    pass
