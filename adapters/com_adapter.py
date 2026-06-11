from typing import Dict, Any
from .base_adapter import BaseAdapter

class COMAdapter(BaseAdapter):
    """
    Adapter for HPE Compute Ops Management (COM).
    Handles COM-specific headers, URL construction, and response parsing.
    """
    
    def get_headers(self, payload: Dict[str, Any]) -> Dict[str, str]:
        """
        Builds headers for HPE COM.
        Uses standard 'Authorization: Bearer <token>' header for authentication.
        """
        headers = {
            "Accept": "application/json",
        }
        
        credential_ref = payload.get("credential_ref")
        if credential_ref:
            # COM/GreenLake APIs typically use Bearer tokens for authorization
            headers["Authorization"] = f"Bearer {credential_ref}"
            
        return headers

    def normalize_success(self, payload: Dict[str, Any], raw_response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Overrides normalize_success to add COM-specific messages.
        """
        result = super().normalize_success(payload, raw_response)
        action = payload.get("action", "unknown")
        
        # COM responses might use different status keys
        if isinstance(raw_response, dict):
            if "message" in raw_response and isinstance(raw_response["message"], str):
                result["message"] = raw_response["message"]
            elif "taskStatus" in raw_response:
                result["message"] = f"Compute Ops Management operation '{action}' completed. Status: {raw_response['taskStatus']}"
            elif "state" in raw_response and isinstance(raw_response["state"], str):
                result["message"] = f"Compute Ops Management operation '{action}' completed. Current state: {raw_response['state']}"
                
        return result
