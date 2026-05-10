from typing import Optional
from utils import verify_id_token
import json

import os

class IdentityManager:
    """
    Secure Service to handle user identity verification via JWT.
    Zero Trust: Identity is extracted from a cryptographically verified token.
    """
    def __init__(self, roles_file: str = "roles.json"):
        # Ensure we always look up roles.json relative to this python file
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.roles_file = os.path.join(base_dir, roles_file)
        self.roles_mapping = {}
        self.load_roles()

    def load_roles(self):
        try:
            with open(self.roles_file, 'r') as f:
                self.roles_mapping = json.load(f)
        except Exception:
            self.roles_mapping = {}

    def verify_and_resolve(self, token: str) -> dict:
        """
        Verifies the JWT token and resolves the user's role.
        Role can be extracted from token or looked up in roles.json for extra security.
        """
        self.load_roles() # dev-mode reload
        
        # 1. Verify the Cryptographic Signature
        payload = verify_id_token(token)
        email = payload.get("email")
        
        # 2. Authorization Handshake (Internal Mapping)
        # We look up the role from our master registry to ensure it hasn't been revoked
        profile = self.roles_mapping.get(email)
        if not profile:
            raise ValueError(f"Identity '{email}' verified but not found in authorization registry.")
            
        return {
            "name": profile.get("name"),
            "email": email,
            "role": profile.get("role")
        }

identity_manager = IdentityManager()
