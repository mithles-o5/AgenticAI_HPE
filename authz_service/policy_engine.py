from datetime import datetime
from models import TokenPayload, Resource, Context, AuthResponse, DecisionTrace
from rbac import RBACEngine
from abac import ABACEngine
from identity_manager import identity_manager

class PolicyEngine:
    """
    Orchestrator for Authorization Logic (Identity-Based Upgrade).
    Flow: Email -> Resolve Role (Internal) -> RBAC -> ABAC -> Policy Rules -> Final Decision
    """
    def __init__(self):
        self.rbac_engine = RBACEngine()
        self.abac_engine = ABACEngine()
        
        # Simple PBAC configuration
        self.policies = [
             {
                 "action": "restart",
                 "role_target": "admin",
                 "condition": lambda payload, resource: resource.env != 'production',
                 "name": "Admin cannot restart production"
             }
        ]

    def authorize(self, token: str, action: str, resource: Resource, context: Context) -> AuthResponse:
        trace = DecisionTrace(rbac="SKIPPED", abac="SKIPPED", policy="SKIPPED")
        reason = ""
        decision = "DENY"
        user_email = "UNKNOWN"
        user_name = "UNKNOWN"
        role = "UNKNOWN"

        # 1. Identity Resolution via JWT (Zero Trust)
        try:
            profile = identity_manager.verify_and_resolve(token)
            user_email = profile["email"]
            user_name = profile["name"]
            role = profile["role"]
        except Exception as e:
            reason = f"Identity Error: {str(e)}"
            self._log_audit(user_name, user_email, role, action, resource, decision, reason)
            return AuthResponse(decision="DENY", reason=reason, trace=trace)

        # Create an internal TokenPayload (Zero Trust: constructed only from server data)
        payload = TokenPayload(
            user_id=user_email.split('@')[0],
            user_email=user_email,
            role=role,
            permissions=[] # Default empty, role-based fallback in engine
        )

        try:
            # 2. RBAC Check
            rbac_pass, rbac_reason = self.rbac_engine.evaluate(payload, action)
            if not rbac_pass:
                trace.rbac = "FAIL"
                reason = f"RBAC Check Failed: {rbac_reason}"
                return AuthResponse(decision="DENY", reason=reason, trace=trace)
            trace.rbac = "PASS"

            # 3. ABAC Check
            abac_pass, abac_reason = self.abac_engine.evaluate(payload, action, resource, context)
            if not abac_pass:
                trace.abac = "FAIL"
                reason = f"ABAC Check Failed: {abac_reason}"
                return AuthResponse(decision="DENY", reason=reason, trace=trace)
            trace.abac = "PASS"

            # 4. PBAC Check (Policy Engine Rules)
            policy_pass = True
            for policy in self.policies:
                if policy["action"] == action and policy.get("role_target") == payload.role:
                    if not policy["condition"](payload, resource):
                        policy_pass = False
                        trace.policy = "FAIL"
                        reason = f"Policy Engine Check Failed: {policy.get('name')}"
                        break
            
            if not policy_pass:
                 return AuthResponse(decision="DENY", reason=reason, trace=trace)
            
            trace.policy = "PASS"
            decision = "ALLOW"
            reason = "Authorized successfully via Identity mapping."

            return AuthResponse(decision=decision, reason=reason, trace=trace)

        finally:
            self._log_audit(user_name, user_email, role, action, resource, decision, reason)

    def _log_audit(self, name, email, role, action, resource, decision, reason):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [AUTHZ] name='{name}' user={email} role={role} action={action} env={resource.env} resource={resource.id} decision={decision} reason='{reason}'")
