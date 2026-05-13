"""
Data models used across the entire resolver pipeline.
"""

from __future__ import annotations

import uuid as _uuid
from dataclasses import dataclass, field
from typing import Optional, Union

from enums import (
    Vendor, Protocol, ActionCategory,
    PowerAction, ProvisionAction,
    ResourceHealth, CacheStatus, DeploymentType,
)


# ─────────────────────────────────────────────────────────────────────────────
# Credentials  (vault reference — never store plain text in production)
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class CredentialRef:
    """
    Reference to credentials stored in a secure vault (e.g. HashiCorp Vault,
    AWS Secrets Manager).  The resolver returns the *reference*, not the secret.
    The execution agent resolves the actual secret at call time.
    """
    vault_path:   str                    # e.g. "secret/datacenter/rack-04/ilo"
    auth_type:    str = "basic"          # basic | token | certificate
    username:     Optional[str] = None   # pre-resolved username (non-secret)
    certificate:  Optional[str] = None   # PEM path for cert auth

    def to_dict(self) -> dict:
        return {
            "vault_path":  self.vault_path,
            "auth_type":   self.auth_type,
            "username":    self.username,
            "certificate": self.certificate,
            "password":    "***VAULT_REF***",   # never serialised
        }


# ─────────────────────────────────────────────────────────────────────────────
# Resource Record  (what the registry stores and the cache caches)
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class ResourceRecord:
    """Full descriptor for a managed server resource."""
    # identity
    name:              str
    uuid:              str
    aliases:           list[str]         = field(default_factory=list)

    # network
    ip_address:        str               = ""
    management_host:   str               = ""    # HPE iLO / OneView / Compute Ops host

    # vendor & protocol capabilities
    vendor:            Vendor            = Vendor.HPE
    deployment_type:   DeploymentType    = DeploymentType.ON_PREM
    supported_protocols: list[Protocol] = field(default_factory=list)

    # hardware metadata
    model:             str               = ""
    serial:            str               = ""
    firmware:          str               = ""
    enclosure:         str               = ""
    bay:               Optional[int]     = None
    location:          Optional[str]     = None
    asset_tag:         Optional[str]     = None
    owner:             Optional[str]     = None
    tags:              list[str]         = field(default_factory=list)

    # live state
    power_state:       str               = "Unknown"
    health:            ResourceHealth    = ResourceHealth.UNKNOWN
    etag:              Optional[str]     = None

    # credentials
    credential_ref:    Optional[CredentialRef] = None

    def to_dict(self) -> dict:
        return {
            "name":               self.name,
            "uuid":               self.uuid,
            "aliases":            self.aliases,
            "ip_address":         self.ip_address,
            "management_host":    self.management_host,
            "vendor":             self.vendor.value,
            "supported_protocols":[p.value for p in self.supported_protocols],
            "model":              self.model,
            "serial":             self.serial,
            "firmware":           self.firmware,
            "enclosure":          self.enclosure,
            "bay":                self.bay,
            "location":           self.location,
            "asset_tag":          self.asset_tag,
            "owner":              self.owner,
            "tags":               self.tags,
            "power_state":        self.power_state,
            "health":             self.health.value,
            "etag":               self.etag,
            "credential_ref":     self.credential_ref.to_dict()
                                  if self.credential_ref else None,
        }


# ─────────────────────────────────────────────────────────────────────────────
# Execution Context  — output of the resolver, input to the execution agent
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class ExecutionContext:
    """
    Structured payload returned by the resolver to the Execution Agent.
    Contains everything the agent needs to invoke the correct handler.
    """
    request_id:       str = field(default_factory=lambda: str(_uuid.uuid4()))

    # resolved resource
    resource_uuid:    str               = ""
    resource_name:    str               = ""
    vendor:           Vendor            = Vendor.HPE

    # action classification
    action_category:  ActionCategory    = ActionCategory.OPERATIONAL
    action:           Union[PowerAction, ProvisionAction, str] = PowerAction.STATUS

    # protocol decision
    selected_protocol:Protocol          = Protocol.ONEVIEW
    protocol_reason:  str               = ""      # why this protocol was chosen

    # endpoint
    endpoint:         str               = ""      # full URL or IP for the handler

    # credential reference (not the secret itself)
    credential_ref:   Optional[CredentialRef] = None

    # resolver diagnostics
    resolved_by:      str               = ""      # uuid | alias | fuzzy | cmdb
    cache_status:     CacheStatus       = CacheStatus.MISS
    query:            str               = ""

    def to_dict(self) -> dict:
        action_val = self.action.value if hasattr(self.action, "value") else str(self.action)
        return {
            "request_id":        self.request_id,
            "resource_uuid":     self.resource_uuid,
            "resource_name":     self.resource_name,
            "vendor":            self.vendor.value,
            "action_category":   self.action_category.value,
            "action":            action_val,
            "selected_protocol": self.selected_protocol.value,
            "protocol_reason":   self.protocol_reason,
            "endpoint":          self.endpoint,
            "credential_ref":    self.credential_ref.to_dict()
                                 if self.credential_ref else None,
            "resolved_by":       self.resolved_by,
            "cache_status":      self.cache_status.value,
            "query":             self.query,
        }


# ─────────────────────────────────────────────────────────────────────────────
# Action Result  — returned from the execution agent back to the MCP tool
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class ActionResult:
    success:        bool
    request_id:     str
    resource_name:  str
    action:         str
    final_state:    str
    task_uri:       Optional[str] = None
    error:          Optional[str] = None
    duration_ms:    int           = 0

    def to_dict(self) -> dict:
        return {
            "success":       self.success,
            "request_id":    self.request_id,
            "resource_name": self.resource_name,
            "action":        self.action,
            "final_state":   self.final_state,
            "task_uri":      self.task_uri,
            "error":         self.error,
            "duration_ms":   self.duration_ms,
        }
