"""
Database-Driven Protocol Discovery
===================================
Determines which management protocol (OneView, COMS, etc.) should be used
for a resource based on infrastructure metadata from PostgreSQL.

This module removes hardcoded protocol assumptions and instead queries the
database to dynamically discover protocol ownership.

Key Functions:
  • determine_protocol_from_credential_ref()
    - Uses vault path patterns to infer protocol
    - Examples: "vault://oneview/prod" → ONEVIEW, "vault://coms/prod" → COMS
  
  • determine_protocol_by_ip_and_credentials()
    - Queries server_protocols table to find supported protocols
    - Uses IP + credentials as lookup key
    - Returns list of supported protocols from DB
  
  • select_managed_protocol()
    - Chooses primary protocol from list of supported protocols
    - Considers management ownership metadata
    - Fallback to first supported protocol if no primary indicator
  
  • get_protocol_metadata()
    - Retrieves full protocol configuration from DB
    - Returns base URL, API version, headers, etc.

Architecture:
  Infrastructure DB → Protocol Metadata → Resource Record → Protocol Selection
"""

from __future__ import annotations

import logging
from typing import Optional, List

from enums import Protocol
from records import ResourceRecord, CredentialRef
from db import db_manager
from errors import ActionClassificationError

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# Credential-Based Protocol Discovery
# ─────────────────────────────────────────────────────────────────────────────

def determine_protocol_from_credential_ref(
    credential_ref: Optional[CredentialRef],
) -> Optional[Protocol]:
    """
    Infer protocol from credential vault path pattern.
    
    Credential paths encode protocol ownership:
    - vault://oneview/... → ONEVIEW
    - vault://coms/... → COMS
    - secret/datacenter/oneview/... → ONEVIEW
    - secret/datacenter/coms/... → COMS
    
    Parameters
    ----------
    credential_ref : CredentialRef or None
        Credential reference with vault path
    
    Returns
    -------
    Protocol if path contains protocol indicator, None otherwise
    
    Examples
    --------
    >>> ref = CredentialRef("vault://oneview/prod/admin")
    >>> determine_protocol_from_credential_ref(ref)
    <Protocol.ONEVIEW: 'ONEVIEW'>
    
    >>> ref = CredentialRef("vault://coms/staging/user")
    >>> determine_protocol_from_credential_ref(ref)
    <Protocol.COMS: 'COMS'>
    """
    if not credential_ref or not credential_ref.vault_path:
        return None
    
    vault_path = credential_ref.vault_path.lower()
    
    # Check for COMS indicators (check before ONEVIEW since COMS is more specific)
    if "coms" in vault_path or "compute-ops" in vault_path or "co_" in vault_path:
        logger.debug(
            f"[Protocol Discovery] COMS protocol inferred from vault path: "
            f"{credential_ref.vault_path[:40]}…"
        )
        return Protocol.COMS
    
    # Check for OneView indicators
    if "oneview" in vault_path or "one_view" in vault_path or "ov_" in vault_path:
        logger.debug(
            f"[Protocol Discovery] OneView protocol inferred from vault path: "
            f"{credential_ref.vault_path[:40]}…"
        )
        return Protocol.ONEVIEW
    
    return None


# ─────────────────────────────────────────────────────────────────────────────
# IP + Credentials Based Protocol Discovery
# ─────────────────────────────────────────────────────────────────────────────

def determine_protocol_by_ip_and_credentials(
    ip_address: str,
    vault_path: str,
    auth_type: str,
) -> List[Protocol]:
    """
    Query database to find which protocols manage this resource.
    
    Uses the server_protocols and com_server_protocols tables to determine
    which management platforms (OneView, COMS) own this IP address.
    
    Parameters
    ----------
    ip_address : str
        Server IP address (e.g., "10.10.1.104")
    vault_path : str
        Vault path for credentials
    auth_type : str
        Authentication type (basic, token, certificate)
    
    Returns
    -------
    List of Protocol enums supported by this resource
    
    Examples
    --------
    >>> protocols = determine_protocol_by_ip_and_credentials(
    ...     "10.10.1.104",
    ...     "secret/datacenter/prod/ilo",
    ...     "basic"
    ... )
    >>> protocols
    [<Protocol.ONEVIEW: 'ONEVIEW'>]
    """
    try:
        protocol_names = db_manager.fetch_protocols_by_credentials(
            ip_address,
            vault_path,
            auth_type
        )
        
        if not protocol_names:
            logger.warning(
                f"[Protocol Discovery] No protocols found for {ip_address} "
                f"(vault: {vault_path[:30]}…, auth: {auth_type})"
            )
            return []
        
        protocols = []
        for name in protocol_names:
            try:
                protocol = Protocol(name)
                protocols.append(protocol)
            except ValueError:
                logger.warning(
                    f"[Protocol Discovery] Unknown protocol in DB: {name}"
                )
        
        logger.info(
            f"[Protocol Discovery] Found {len(protocols)} protocols for {ip_address}: "
            f"{[p.value for p in protocols]}"
        )
        return protocols
        
    except Exception as e:
        logger.error(
            f"[Protocol Discovery] Error querying protocols for {ip_address}: {e}"
        )
        return []


# ─────────────────────────────────────────────────────────────────────────────
# Primary Protocol Selection
# ─────────────────────────────────────────────────────────────────────────────

def select_managed_protocol(
    supported_protocols: List[Protocol],
    credential_ref: Optional[CredentialRef] = None,
) -> Optional[Protocol]:
    """
    Select the primary protocol from list of supported protocols.
    
    Decision hierarchy:
    1. If credential path indicates protocol → use that
    2. If only one protocol supported → use that
    3. If multiple protocols, prefer OneView (primary management layer)
    4. Otherwise return first in list
    
    Parameters
    ----------
    supported_protocols : list[Protocol]
        List of protocols this resource supports
    credential_ref : CredentialRef, optional
        Credential reference with vault path
    
    Returns
    -------
    Primary Protocol for this resource, or None if list is empty
    
    Examples
    --------
    >>> select_managed_protocol([Protocol.ONEVIEW])
    <Protocol.ONEVIEW: 'ONEVIEW'>
    
    >>> select_managed_protocol([Protocol.ONEVIEW, Protocol.COMS], 
    ...     CredentialRef("vault://coms/prod"))
    <Protocol.COMS: 'COMS'>
    """
    if not supported_protocols:
        return None
    
    if len(supported_protocols) == 1:
        logger.debug(
            f"[Protocol Discovery] Single protocol supported: {supported_protocols[0].value}"
        )
        return supported_protocols[0]
    
    # Check credential path for protocol indicator
    inferred_protocol = determine_protocol_from_credential_ref(credential_ref)
    if inferred_protocol and inferred_protocol in supported_protocols:
        logger.info(
            f"[Protocol Discovery] Protocol {inferred_protocol.value} "
            f"selected from credential path"
        )
        return inferred_protocol
    
    # Prefer OneView as primary management layer
    if Protocol.ONEVIEW in supported_protocols:
        logger.debug(
            f"[Protocol Discovery] Multiple protocols available, "
            f"selecting OneView as primary"
        )
        return Protocol.ONEVIEW
    
    # Fallback to first protocol
    selected = supported_protocols[0]
    logger.info(
        f"[Protocol Discovery] Selected first available protocol: {selected.value}"
    )
    return selected


# ─────────────────────────────────────────────────────────────────────────────
# Full Protocol Discovery Workflow
# ─────────────────────────────────────────────────────────────────────────────

def discover_protocol_for_resource(
    resource: ResourceRecord,
) -> tuple[Protocol, str]:
    """
    Complete database-driven protocol discovery workflow.
    
    Steps:
    1. Extract IP, credentials, auth_type from resource
    2. Query DB for supported protocols
    3. Select primary protocol from supported list
    4. Return protocol with discovery reason
    
    Parameters
    ----------
    resource : ResourceRecord
        Resource record with IP, credentials, and metadata
    
    Returns
    -------
    Tuple of (selected_protocol, discovery_reason)
    
    Raises
    ------
    ActionClassificationError
        If no protocols found and unable to determine protocol
    
    Examples
    --------
    >>> resource = ResourceRecord(
    ...     name="server01.dc.hpe.com",
    ...     uuid="abc-123-def",
    ...     ip_address="10.10.1.104",
    ...     credential_ref=CredentialRef("vault://oneview/prod"),
    ...     ...
    ... )
    >>> protocol, reason = discover_protocol_for_resource(resource)
    >>> protocol
    <Protocol.ONEVIEW: 'ONEVIEW'>
    >>> reason
    'Protocol discovered from database: infrastructure owns IP 10.10.1.104 via OneView'
    """
    logger.info(
        f"[Protocol Discovery] Starting discovery for {resource.name} "
        f"(IP: {resource.ip_address}, UUID: {resource.uuid[:8]}…)"
    )
    
    # Step 1: Extract identification info
    ip_address = resource.ip_address
    credential_ref = resource.credential_ref
    
    if not ip_address:
        raise ActionClassificationError(
            f"Cannot discover protocol for '{resource.name}': "
            f"IP address required but not available"
        )
    
    # Step 2: Try credential path first (fastest, no DB query)
    inferred_protocol = determine_protocol_from_credential_ref(credential_ref)
    if inferred_protocol:
        reason = (
            f"Protocol '{inferred_protocol.value}' determined from "
            f"credential path '{credential_ref.vault_path}'"
        )
        logger.info(f"[Protocol Discovery] {reason}")
        return inferred_protocol, reason
    
    # Step 3: Query database for protocols by IP + credentials
    vault_path = credential_ref.vault_path if credential_ref else ""
    auth_type = credential_ref.auth_type if credential_ref else "basic"
    
    supported_protocols = determine_protocol_by_ip_and_credentials(
        ip_address,
        vault_path,
        auth_type,
    )
    
    if not supported_protocols:
        raise ActionClassificationError(
            f"Protocol discovery failed for '{resource.name}' ({ip_address}): "
            f"No protocols found in infrastructure database. "
            f"Check vault_path={vault_path[:30]}… and credentials."
        )
    
    # Step 4: Select primary protocol from supported list
    selected_protocol = select_managed_protocol(supported_protocols, credential_ref)
    
    if not selected_protocol:
        raise ActionClassificationError(
            f"Could not select protocol for '{resource.name}': "
            f"supported_protocols={[p.value for p in supported_protocols]} "
            f"but selection failed"
        )
    
    reason = (
        f"Protocol '{selected_protocol.value}' discovered from infrastructure database "
        f"(IP: {ip_address}, supported: {[p.value for p in supported_protocols]})"
    )
    logger.info(f"[Protocol Discovery] {reason}")
    
    return selected_protocol, reason
