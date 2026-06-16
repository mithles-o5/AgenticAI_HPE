import jwt

# Secret key used to sign and verify JWT identity tokens
SECRET_KEY = "demo_secret_key"
ALGORITHM = "HS256"

def verify_id_token(token: str) -> dict:
    """Verifies the JWT token and returns the payload if valid."""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except Exception as e:
        raise ValueError(f"Token Verification Failed: {str(e)}")
