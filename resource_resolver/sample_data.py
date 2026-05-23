"""
Sample Registry Loader
=======================
Populates the registry with representative resources.
Replace with a CMDB / database fetch in production.
"""

from __future__ import annotations
import os
import uuid

from records import (
    Vendor, Protocol, ResourceHealth,
    ResourceRecord, CredentialRef, DeploymentType,
)
from registry import ResourceRegistry

def load_sample_registry() -> ResourceRegistry:
    registry = ResourceRegistry()

    # Generate 1000 OneView servers across 10 simulated OneViews
    for ov_idx in range(1, 11):
        for srv_idx in range(1, 101):
            name = f"OV{ov_idx}-RackServer-{srv_idx:03d}"
            # Ensure stable but unique UUIDs
            server_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, name))
            registry.register(ResourceRecord(
                name              = name,
                uuid              = server_uuid,
                aliases           = [f"server-{ov_idx}-{srv_idx}", f"ilo-{name}"],
                ip_address        = f"10.10.{ov_idx}.{srv_idx}",
                management_host   = f"ilo-{name}.mgmt.local",
                vendor            = Vendor.HPE,
                supported_protocols = [Protocol.ONEVIEW],
                model             = "ProLiant DL380 Gen10",
                serial            = f"USE749{ov_idx:02d}{srv_idx:03d}",
                firmware          = "iLO5 2.65",
                enclosure         = f"RACK-{ov_idx:02d}",
                location          = f"DC-East / Row-{chr(64+ov_idx)} / Rack-{ov_idx:02d} / U{srv_idx%40+1}",
                asset_tag         = f"ASSET-OV{ov_idx}-{srv_idx:03d}",
                owner             = "platform-team",
                tags              = ["production", "rack", f"ov-{ov_idx}"],
                power_state       = "Off" if srv_idx % 2 == 0 else "On",
                health            = ResourceHealth.OK,
                credential_ref    = CredentialRef(
                    vault_path = f"secret/datacenter/rack-{ov_idx:02d}/{srv_idx}/ilo",
                    auth_type  = "basic",
                    username   = os.getenv("HPE_OV_USER", "administrator"),
                ),
            ))

    # Generate 500 Compute Ops (CoM) servers
    for com_idx in range(1, 501):
        name = f"CoM-CloudNode-{com_idx:03d}"
        server_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, name))
        registry.register(ResourceRecord(
            name              = name,
            uuid              = server_uuid,
            aliases           = [f"cloud-node-{com_idx}"],
            ip_address        = f"192.168.100.{com_idx % 250 + 1}",
            management_host   = "compute-ops.us-west.hpe-cloud.net",
            vendor            = Vendor.HPE,
            deployment_type   = DeploymentType.CLOUD,
            supported_protocols = [Protocol.COMS],
            model             = "HPE Compute Ops Instance",
            serial            = f"CLOUD-{com_idx:03d}-SERIAL",
            firmware          = "Compute Ops v1.2",
            enclosure         = "CLOUD",
            location          = f"HPE GreenLake Data Center / US-West / Zone-{(com_idx%3)+1}",
            asset_tag         = f"ASSET-CLOUD-{com_idx:03d}",
            owner             = "cloud-team",
            tags              = ["cloud", "prod", "compute-ops"],
            power_state       = "On" if com_idx % 2 == 0 else "Off",
            health            = ResourceHealth.OK,
            credential_ref    = CredentialRef(
                vault_path = f"secret/cloud/us-west/{name}/api",
                auth_type  = "token",
                username   = os.getenv("COMPUTE_OPS_USER", "api-user"),
            ),
        ))

    return registry
