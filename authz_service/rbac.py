from typing import Dict, List
from models import TokenPayload

class RBACEngine:
    """
    Role-Based Access Control
    Evaluates if a user's role allows the requested action based on basic permission mapping.
    """
    def __init__(self):
        # Basic static permission assignments (in real life, this comes from a DB/LDAP)
        self.role_permissions: Dict[str, List[str]] = {
            "admin": ["restart", "view", "shutdown", "create"],
            "senior_admin": ["restart", "view", "shutdown", "create", "delete", "approve"],
            "operator": ["view", "monitor", "start"]
        }

    def evaluate(self, payload: TokenPayload, action: str) -> tuple[bool, str]:
        # First check permissions directly in the token if our system uses token-carried claims
        if action in payload.permissions:
            return True, f"Token carries '{action}' permission directly."

        # Fallback to role-based lookup
        role = payload.role
        allowed_actions = self.role_permissions.get(role, [])
        if action in allowed_actions:
            return True, f"Role '{role}' is allowed to perform '{action}'."
        
        return False, f"Role '{role}' does not have permission for '{action}'."
