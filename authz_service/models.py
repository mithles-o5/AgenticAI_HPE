from pydantic import BaseModel
from typing import Dict, Any, List, Optional

class Resource(BaseModel):
    id: str
    env: str
    vendor: Optional[str] = "unknown"

class Context(BaseModel):
    time: str
    location: Optional[str] = "unknown"

class AuthRequest(BaseModel):
    token: str
    action: str
    resource: Resource
    context: Context

class TokenPayload(BaseModel):
    user_id: str
    user_email: str
    role: str
    permissions: List[str]

class DecisionTrace(BaseModel):
    rbac: str
    abac: str
    policy: str

class AuthResponse(BaseModel):
    decision: str
    reason: str
    trace: DecisionTrace
