from typing import Dict, List
from models import TokenPayload

class RBACEngine:
    """
    Role-Based Access Control (Matrix Model)
    Evaluates permissions based on the official HPE OneView role matrix.
    Role -> Resource Category -> Allowed Actions
    """
    def __init__(self):
        self.matrix = {
            "Infrastructure administrator": {
                "*": ["read", "create", "update", "delete", "execute"]
            },
            "Read only": {
                "*": ["read"]
            },
            "Backup administrator": {
                "backups": ["create", "read", "execute"],
                "settings": ["read"],
                "activities": ["read"]
            },
            "Network administrator": {
                "ethernet-networks": ["read", "create", "update", "delete"],
                "fc-networks": ["read", "create", "update", "delete"],
                "network-sets": ["read", "create", "update", "delete"],
                "interconnects": ["read", "create", "update", "delete"],
                "uplink-sets": ["read", "create", "update", "delete"],
                "firmware-bundles": ["read", "create", "update", "delete"],
                "activities": ["read"],
                "logs": ["read"],
                "notifications": ["read"]
            },
            "Server administrator": {
                "server-profiles": ["read", "create", "update", "delete"],
                "server-profile-templates": ["read", "create", "update", "delete"],
                "network-sets": ["read", "create", "update", "delete"],
                "enclosures": ["read", "create", "update", "delete"],
                "firmware-bundles": ["read", "create", "update", "delete"],
                "server-hardware": ["read", "execute"],
                "hypervisor-managers": ["read", "execute"],
                "connections": ["read"],
                "ethernet-networks": ["read"],
                "racks": ["read"],
                "power-devices": ["read"],
                "storage-volumes": ["create", "read"] # Can add volumes, but no pools
            },
            "Server firmware operator": {
                "*": ["read"],
                "server-hardware": ["read", "update", "execute"]
            },
            "Storage administrator": {
                "storage-systems": ["read", "create", "update", "delete"],
                "storage-pools": ["read", "update"],
                "storage-volumes": ["read", "create", "update", "delete"],
                "storage-volume-templates": ["read", "create", "update", "delete"],
                "fc-sans": ["read", "create", "update"]
            }
        }

    def evaluate(self, payload: TokenPayload, action: str, resource_category: str) -> tuple[bool, str]:
        role = payload.role
        
        if role not in self.matrix:
            return False, f"Role '{role}' is not recognized."

        role_rules = self.matrix[role]

        # 1. Check if they have global God-mode (Infrastructure admin)
        if "*" in role_rules:
            if "*" in role_rules["*"] or action in role_rules["*"]:
                return True, f"Allowed by global '{action}' permission."

        # 2. Check if they have access to this specific resource
        if resource_category in role_rules:
            if action in role_rules[resource_category] or "*" in role_rules[resource_category]:
                return True, f"Role '{role}' has '{action}' permission on '{resource_category}'."
        
        # 3. Check if they have global read-only access (e.g. Read only role, Server firmware operator)
        if action == "read" and "*" in role_rules and "read" in role_rules["*"]:
            return True, "Allowed by global 'read' permission."

        return False, f"Role '{role}' is DENIED '{action}' on '{resource_category}'."
