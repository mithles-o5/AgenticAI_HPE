import logging
from typing import Dict, Any, List, Optional, Tuple

logger = logging.getLogger("server-agent.models")

REQUIRED_FIELDS = [
    "management_source",
    "source_host",
    "api_endpoint",
    "http_method",
    "action"
]

class ValidationError(Exception):
    """Exception raised when payload validation fails."""
    def __init__(self, message: str, missing_fields: List[str], action: str = "unknown"):
        super().__init__(message)
        self.message = message
        self.missing_fields = missing_fields
        self.action = action

    def to_dict(self) -> Dict[str, Any]:
        """Convert validation error to structured error dictionary."""
        return {
            "success": False,
            "action": self.action,
            "status": "failed",
            "message": self.message,
            "error": {
                "validation_errors": {
                    "missing_fields": self.missing_fields
                }
            }
        }


def validate_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validates the input execution payload against required fields and formats.
    Returns the cleaned/validated payload dictionary.
    Raises ValidationError if validation fails.
    """
    if not isinstance(payload, dict):
        raise ValidationError(
            message="Payload must be a JSON object (dictionary)",
            missing_fields=REQUIRED_FIELDS,
            action="unknown"
        )

    # 1. Check for required fields
    missing_fields = [field for field in REQUIRED_FIELDS if field not in payload or payload.get(field) is None]
    
    # Extract action safely for error reporting
    action = payload.get("action")
    if not isinstance(action, str) or not action.strip():
        action_val = "unknown"
    else:
        action_val = action.strip()

    if missing_fields:
        field_names = ", ".join(missing_fields)
        raise ValidationError(
            message=f"Validation failed: missing required fields: {field_names}",
            missing_fields=missing_fields,
            action=action_val
        )

    # 2. Validate specific field values and formats
    management_source = str(payload["management_source"]).upper().strip()
    if management_source not in ["ONEVIEW", "COM"]:
        raise ValidationError(
            message=f"Validation failed: Unsupported management_source '{management_source}'. Must be ONEVIEW or COM.",
            missing_fields=[],
            action=action_val
        )

    http_method = str(payload["http_method"]).upper().strip()
    if http_method not in ["GET", "POST", "PUT", "DELETE", "PATCH"]:
        raise ValidationError(
            message=f"Validation failed: Unsupported HTTP method '{http_method}'.",
            missing_fields=[],
            action=action_val
        )

    # Return normalized clean dictionary
    validated = {
        "management_source": management_source,
        "source_host": str(payload["source_host"]).strip(),
        "api_endpoint": str(payload["api_endpoint"]).strip(),
        "http_method": http_method,
        "action": action_val,
        "category": payload.get("category"),
        "serial_number": payload.get("serial_number"),
        "credential_ref": payload.get("credential_ref"),
        "device_type": payload.get("device_type")
    }
    
    return validated
