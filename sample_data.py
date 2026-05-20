"""
Sample Test Data for MCP Tool
==============================
Used when PostgreSQL database is not available.
Provides sample resources for testing protocol discovery.
"""

from records import ResourceRecord, CredentialRef
from registry import ResourceRegistry
from enums import Vendor, Protocol, ResourceHealth, DeploymentType


def create_sample_registry() -> ResourceRegistry:
    """
    Create a sample registry with test resources.
    Used when database is unavailable.
    """
    registry = ResourceRegistry()
    
    # Sample OneView server
    server_ov = ResourceRecord(
        name="oneview-prod-01",
        uuid="550e8400-e29b-41d4-a716-446655440100",
        aliases=["ov-prod-01", "server-ov-01"],
        ip_address="10.10.1.100",
        management_host="oneview.example.com",
        vendor=Vendor.HPE,
        deployment_type=DeploymentType.ON_PREM,
        supported_protocols=[Protocol.ONEVIEW],
        model="ProLiant DL380 Gen10",
        serial="SN123456",
        firmware="2.88",
        location="Datacenter/Rack-04/Bay-02",
        owner="CloudOps",
        power_state="On",
        health=ResourceHealth.OK,
        credential_ref=CredentialRef(
            vault_path="vault://oneview/prod/admin",
            auth_type="basic",
            username="oneview_admin"
        ),
    )
    registry.register(server_ov)
    
    # Sample COMS server
    server_coms = ResourceRecord(
        name="coms-cloud-01",
        uuid="660e8400-e29b-41d4-a716-446655440200",
        aliases=["coms-01", "compute-ops-01"],
        ip_address="10.10.2.100",
        management_host="compute-ops.cloud.com",
        vendor=Vendor.HPE,
        deployment_type=DeploymentType.CLOUD,
        supported_protocols=[Protocol.COMS],
        model="Virtual Machine",
        serial="VM-12345",
        firmware="1.0",
        location="Cloud/Region-us-east-1",
        owner="CloudOps",
        power_state="On",
        health=ResourceHealth.OK,
        credential_ref=CredentialRef(
            vault_path="vault://coms/prod/api_user",
            auth_type="token",
            username="api_user"
        ),
    )
    registry.register(server_coms)
    
    # Sample OneView with ambiguous credentials (for testing fallback)
    server_generic = ResourceRecord(
        name="generic-prod-02",
        uuid="770e8400-e29b-41d4-a716-446655440300",
        aliases=["generic-02"],
        ip_address="10.10.3.100",
        management_host="infra.example.com",
        vendor=Vendor.HPE,
        deployment_type=DeploymentType.ON_PREM,
        supported_protocols=[Protocol.ONEVIEW],
        model="ProLiant DL360 Gen9",
        serial="SN789012",
        firmware="2.60",
        location="Datacenter/Rack-05/Bay-01",
        owner="Infrastructure",
        power_state="Standby",
        health=ResourceHealth.WARNING,
        credential_ref=CredentialRef(
            vault_path="secret/datacenter/prod/generic",
            auth_type="basic",
            username="generic_user"
        ),
    )
    registry.register(server_generic)
    
    return registry
