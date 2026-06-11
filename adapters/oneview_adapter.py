from typing import Dict, Any
from .base_adapter import BaseAdapter

class OneViewAdapter(BaseAdapter):
    """
    Adapter for HPE OneView.
    Handles OneView-specific headers, URL construction, and response parsing.
    """
    
    def get_headers(self, payload: Dict[str, Any]) -> Dict[str, str]:
        """
        Builds headers for HPE OneView.
        Uses the 'Auth' header for authentication token if credential_ref is provided.
        Includes typical OneView headers like X-API-Version.
        """
        headers = {
            "Accept": "application/json",
        }
        
        credential_ref = payload.get("credential_ref")
        if credential_ref:
            # HPE OneView uses 'Auth' header for session token authentication
            headers["Auth"] = str(credential_ref)
            # Default X-API-Version, standard in OneView api
            headers["X-API-Version"] = "3200"
            
        return headers

    def normalize_success(self, payload: Dict[str, Any], raw_response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Overrides normalize_success to add OneView-specific messages
        or parse OneView-specific fields.
        """
        result = super().normalize_success(payload, raw_response)
        action = payload.get("action", "unknown")
        
        # In OneView, if we do a power operation, raw_response may contain detailed message
        if isinstance(raw_response, dict):
            # OneView often returns resource names or task logs
            if "statusText" in raw_response:
                result["message"] = f"OneView operation '{action}' reports: {raw_response['statusText']}"
            elif "description" in raw_response:
                result["message"] = f"OneView operation '{action}' reports: {raw_response['description']}"

        return result
