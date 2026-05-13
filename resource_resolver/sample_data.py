"""
Sample Registry Loader
=======================
Populates the registry with representative resources.
Replace with a CMDB / database fetch in production.

Credentials use vault_path references — resolve actual secrets
from HashiCorp Vault / AWS Secrets Manager at execution time.
"""

from __future__ import annotations
import os

from records import (
    Vendor, Protocol, ResourceHealth,
    ResourceRecord, CredentialRef, DeploymentType,
)
from registry import ResourceRegistry

def load_sample_registry() -> ResourceRegistry:
    registry = ResourceRegistry()

    # ── HPE ProLiant DL380 Gen10 (OneView managed) ───────────────────────────
    registry.register(ResourceRecord(
        name              = "rack-server-04",
        uuid              = "b2c3d4e5-0002-4f6a-9012-bcdef0123402",
        aliases           = ["dl380-rack04", "server04", "ilo-rack-04"],
        ip_address        = "10.10.1.104",
        management_host   = "ilo-rack-04.mgmt.local",
        vendor            = Vendor.HPE,
        supported_protocols = [Protocol.ONEVIEW],
        model             = "ProLiant DL380 Gen10",
        serial            = "USE7491QRA",
        firmware          = "iLO5 2.65",
        enclosure         = "RACK-04",
        location          = "DC-East / Row-B / Rack-04 / U12",
        asset_tag         = "ASSET-00412",
        owner             = "platform-team",
        tags              = ["production", "rack", "tier-2", "web-tier"],
        power_state       = "Off",
        health            = ResourceHealth.OK,
        etag              = 'W/"1c4a7"',
        credential_ref    = CredentialRef(
            vault_path = "secret/datacenter/rack-04/ilo",
            auth_type  = "basic",
            username   = os.getenv("HPE_OV_USER", "administrator"),
        ),
    ))

    # ── HPE BL460c Gen10 Blade (OneView managed) ─────────────────────────────
    registry.register(ResourceRecord(
        name              = "blade-enclosure-01",
        uuid              = "a1b2c3d4-0001-4e5f-8901-abcdef012301",
        aliases           = ["bl460c-01", "blade01"],
        ip_address        = "10.10.1.101",
        management_host   = "ilo-blade-01.mgmt.local",
        vendor            = Vendor.HPE,
        supported_protocols = [Protocol.ONEVIEW],
        model             = "ProLiant BL460c Gen10",
        serial            = "USE7480BMP",
        firmware          = "iLO5 2.65",
        enclosure         = "ENC-01",
        bay               = 3,
        location          = "DC-East / Row-A / Enc-01 / Bay-3",
        asset_tag         = "ASSET-00301",
        owner             = "platform-team",
        tags              = ["production", "blade", "tier-1", "db-tier"],
        power_state       = "Off",
        health            = ResourceHealth.OK,
        etag              = 'W/"3a9f2"',
        credential_ref    = CredentialRef(
            vault_path = "secret/datacenter/enc-01/bay3/ilo",
            auth_type  = "basic",
            username   = os.getenv("HPE_OV_USER", "administrator"),
        ),
    ))

    # ── HPE Synergy 480 Gen10 (OneView + COMS provisioning) — Compute 01 ─────
    registry.register(ResourceRecord(
        name              = "synergy-compute-01",
        uuid              = "c3d4e5f6-0001-5a7b-a123-cdef01234501",
        aliases           = ["sy480-01", "synergy01", "gpu-node-01"],
        ip_address        = "10.10.1.201",
        management_host   = "ilo-sy-01.mgmt.local",
        vendor            = Vendor.HPE,
        supported_protocols = [Protocol.COMS, Protocol.ONEVIEW],
        model             = "Synergy 480 Gen10",
        serial            = "CZ3725BLKV",
        firmware          = "iLO5 2.71",
        enclosure         = "SY-FRAME-01",
        bay               = 1,
        location          = "DC-West / Synergy-Frame-01 / Bay-1",
        asset_tag         = "ASSET-00501",
        owner             = "ml-team",
        tags              = ["prod", "synergy", "gpu", "composable"],
        power_state       = "On",
        health            = ResourceHealth.OK,
        etag              = 'W/"7e2a1"',
        credential_ref    = CredentialRef(
            vault_path = "secret/datacenter/synergy-frame-01/bay1/ilo",
            auth_type  = "basic",
            username   = os.getenv("HPE_OV_USER", "administrator"),
        ),
    ))

    # ── HPE Synergy 480 Gen10 (OneView + COMS provisioning) — Compute 02 ─────
    registry.register(ResourceRecord(
        name              = "synergy-compute-02",
        uuid              = "c3d4e5f6-0002-5a7b-a123-cdef01234502",
        aliases           = ["sy480-02", "synergy02", "gpu-node-02"],
        ip_address        = "10.10.1.202",
        management_host   = "ilo-sy-02.mgmt.local",
        vendor            = Vendor.HPE,
        supported_protocols = [Protocol.COMS, Protocol.ONEVIEW],
        model             = "Synergy 480 Gen10",
        serial            = "CZ3725BLKW",
        firmware          = "iLO5 2.71",
        enclosure         = "SY-FRAME-01",
        bay               = 3,
        location          = "DC-West / Synergy-Frame-01 / Bay-3",
        asset_tag         = "ASSET-00502",
        owner             = "ml-team",
        tags              = ["dev", "synergy", "gpu", "composable"],
        power_state       = "Off",
        health            = ResourceHealth.OK,
        etag              = 'W/"6d3b2"',
        credential_ref    = CredentialRef(
            vault_path = "secret/datacenter/synergy-frame-01/bay3/ilo",
            auth_type  = "basic",
            username   = os.getenv("HPE_OV_USER", "administrator"),
        ),
    ))

    # ── HPE Synergy 480 Gen10 (OneView + COMS provisioning) — Compute 03 ─────
    registry.register(ResourceRecord(
        name              = "synergy-compute-03",
        uuid              = "c3d4e5f6-0003-5a7b-a123-cdef01234503",
        aliases           = ["sy480-03", "synergy03", "gpu-node-03"],
        ip_address        = "10.10.1.203",
        management_host   = "ilo-sy-03.mgmt.local",
        vendor            = Vendor.HPE,
        supported_protocols = [Protocol.COMS, Protocol.ONEVIEW],
        model             = "Synergy 480 Gen10",
        serial            = "CZ3725BLKX",
        firmware          = "iLO5 2.71",
        enclosure         = "SY-FRAME-01",
        bay               = 5,
        location          = "DC-West / Synergy-Frame-01 / Bay-5",
        asset_tag         = "ASSET-00503",
        owner             = "ml-team",
        tags              = ["dev", "synergy", "gpu", "composable"],
        power_state       = "Off",
        health            = ResourceHealth.WARNING,
        etag              = 'W/"8f1b3"',
        credential_ref    = CredentialRef(
            vault_path = "secret/datacenter/synergy-frame-01/bay5/ilo",
            auth_type  = "basic",
            username   = os.getenv("HPE_OV_USER", "administrator"),
        ),
    ))

    # ── HPE Compute Ops Cloud Server (Cloud-hosted Compute instance) ────────
    registry.register(ResourceRecord(
        name              = "cloud-compute-web-01",
        uuid              = "d5e6f7a8-0006-6c8d-d456-f01234567806",
        aliases           = ["web-server-01", "cloud-web-01"],
        ip_address        = "192.168.100.50",
        management_host   = "compute-ops.us-west.hpe-cloud.net",
        vendor            = Vendor.HPE,
        deployment_type   = DeploymentType.CLOUD,
        supported_protocols = [Protocol.COMS],
        model             = "HPE Compute Ops Instance",
        serial            = "CLOUD-001-SERIAL",
        firmware          = "Compute Ops v1.2",
        enclosure         = "CLOUD",
        location          = "HPE GreenLake Data Center / US-West / Zone-A",
        asset_tag         = "ASSET-CLOUD-001",
        owner             = "cloud-team",
        tags              = ["cloud", "prod", "web", "compute-ops"],
        power_state       = "On",
        health            = ResourceHealth.OK,
        etag              = 'W/"cloud1"',
        credential_ref    = CredentialRef(
            vault_path = "secret/cloud/us-west/compute-web-01/api",
            auth_type  = "token",
            username   = os.getenv("COMPUTE_OPS_USER", "api-user"),
        ),
    ))

    return registry
