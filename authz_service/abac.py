from models import Resource, Context, TokenPayload

class ABACEngine:
    """
    Attribute-Based Access Control
    Adds contextual checks for the environment, time, and vendor specifics.
    """
    CRITICAL_ACTIONS = ["restart", "shutdown", "delete"]

    def evaluate(self, payload: TokenPayload, action: str, resource: Resource, context: Context) -> tuple[bool, str]:
        role = payload.role

        # 1. Environment check
        if resource.env == "production":
            if role not in ["senior_admin"]:
                return False, f"Production environment modification restricted to 'senior_admin'. Current role: '{role}'."

        # 2. Time-based critical action check
        if action in self.CRITICAL_ACTIONS:
            # Simple string comparison works for HH:MM format like "22:30" vs "22:00"
            if context.time > "22:00" or context.time < "06:00":
                if role != "senior_admin": # Maybe senior_admin can bypass time restrictions
                    return False, f"Critical actions ({action}) are not allowed between 22:00 and 06:00."

        # 3. Vendor awareness rule
        if resource.vendor.upper() == "HPE":
            # Example rule: HPE vendor resources require specific handling or higher privileges for restarts
            if action == "restart" and role == "operator":
                return False, "Operators cannot restart HPE vendor resources."
            
        return True, "All attribute constraints passed."
