import jwt
import json
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def generate_token(role: str) -> str:
    """Creates a fake JWT without a signature for testing."""
    payload = {
        "user_id": "demo_user",
        "role": role,
        "permissions": ["restart", "view"]
    }
    # Create an unverified JWT token
    return jwt.encode(payload, "secret", algorithm="HS256")

def run_scenario(name: str, token: str, action: str, env: str, vendor: str = "HPE", time: str = "14:00"):
    print(f"\\n{'='*50}")
    print(f"Scenario: {name}")
    print(f"Token Role: {jwt.decode(token, options={'verify_signature': False})['role']}")
    print(f"Action: {action} | Env: {env} | Time: {time} | Vendor: {vendor}")
    
    payload = {
      "token": token,
      "action": action,
      "resource": {
        "id": "server-1",
        "env": env,
        "vendor": vendor
      },
      "context": {
        "time": time,
        "location": "datacenter-1"
      }
    }
    
    response = client.post("/authorize", json=payload)
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def run_all_scenarios():
    # Setup roles
    admin_token = generate_token("admin")
    senior_admin_token = generate_token("senior_admin")
    operator_token = generate_token("operator")

    # Scenario 1: Admin restarting dev server -> ALLOW
    # Note: Our PBAC specifies admin restarting non-prod is ALLOWED.
    run_scenario("Admin restarting dev server", admin_token, "restart", "dev")

    # Scenario 2: Operator restarting any server -> DENY
    run_scenario("Operator restarting any server", operator_token, "restart", "dev")

    # Scenario 3: Admin restarting production server -> DENY
    # Policy says: if action==restart, admin and NOT production. 
    # Plus ABAC restricts prod modification to senior_admin.
    run_scenario("Admin restarting production server", admin_token, "restart", "production")

    # Scenario 4: Senior admin restarting production server -> ALLOW
    # Note: According to PBAC, if action=='restart', condition is `admin and not production`. 
    # But wait, PBAC says `admin and not production`. If user is senior_admin doing it in production, that PBAC rule isn't going to fail if we wrote the rule to apply only to 'admin'.
    # Actually, the PBAC condition I wrote: lambda p, r: p.role == 'admin' and r.env != 'production'
    # Wait, if we apply this to *any* restart, senior_admin will fail the PBAC rule! Let's examine this carefully.
    run_scenario("Senior admin restarting production server", senior_admin_token, "restart", "production")

if __name__ == "__main__":
    run_all_scenarios()
