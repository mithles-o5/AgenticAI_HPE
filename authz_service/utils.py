import jwt
from datetime import datetime, timedelta

# Production-grade secret handling (simulated)
SECRET_KEY = "demo_secret_key"
ALGORITHM = "HS256"

def generate_id_token(name: str, email: str, role: str) -> str:
    """Generates a signed JWT identity token."""
    payload = {
        "name": name,
        "email": email,
        "role": role,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_id_token(token: str) -> dict:
    """Verifies the JWT token and returns the payload if valid."""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except Exception as e:
        raise ValueError(f"Token Verification Failed: {str(e)}")
