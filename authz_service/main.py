from fastapi import FastAPI, HTTPException
from models import AuthRequest, AuthResponse, Resource, Context
from policy_engine import PolicyEngine
from hardware_mock import router as hardware_router

app = FastAPI(
    title="Identity-Centric Authorization & Hardware Service",
    description="Enterprise-grade Authorization Service with Server-Side Role Mapping",
    version="2.0.0"
)

app.include_router(hardware_router)

policy_engine = PolicyEngine()

@app.post("/authorize", response_model=AuthResponse)
def authorize_action(request: AuthRequest):
    """
    Evaluate identity-based authorization.
    Role is resolved server-side from roles.json using the user_email.
    """
    # Orchestrate the authorization flow using the authoritative identity manager
    response = policy_engine.authorize(
        token=request.token,
        action=request.action,
        resource=request.resource,
        context=request.context
    )
    
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
