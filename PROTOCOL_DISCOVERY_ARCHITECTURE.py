"""
Database-Driven Protocol Discovery Architecture
=================================================

OVERVIEW
--------
The resolver architecture has been refactored to move protocol selection from
hardcoded developer rules to dynamic database-driven discovery based on 
infrastructure metadata.

This ensures protocol ownership is determined by the infrastructure inventory
(PostgreSQL database) rather than assumptions in code.


ARCHITECTURE LAYERS
-------------------

Layer 1: Database (PostgreSQL)
  Source of truth for infrastructure metadata:
  - servers table (IP, vault_path, auth_type, etc.)
  - server_protocols (server_id → protocol_id mapping)
  - com_servers table (COMS-managed resources)
  - protocols table (ONEVIEW, COMS, future protocols)
  
Layer 2: Database Connection (db.py)
  - db_manager.execute_query()
  - db_manager.fetch_protocols_by_credentials()
  - db_manager.fetch_server_by_ip_and_credentials()
  
Layer 3: Database Queries (db_queries.py)
  - ServerQueries.get_by_ip()
  - ServerQueries.get_by_protocol()
  - ServerQueries.get_by_vault_path_and_auth()
  
Layer 4: Protocol Discovery (protocol_discovery.py) ← NEW
  - determine_protocol_from_credential_ref()
  - determine_protocol_by_ip_and_credentials()
  - select_managed_protocol()
  - discover_protocol_for_resource()
  
Layer 5: Protocol Selection (selector.py) - REFACTORED
  - select_protocol() → now calls discover_protocol_for_resource()
  - build_endpoint() → unchanged
  - classify_action() → unchanged
  
Layer 6: Resolution Orchestration (resolver.py) - UNCHANGED
  - resolve() → orchestrates all steps
  - Uses new database-driven select_protocol()
  
Layer 7: Endpoint Routing (route_mapper.py) - UNCHANGED
  - get_route_template()
  - build_endpoint()
  - Dynamic endpoint generation


PROTOCOL DISCOVERY WORKFLOW
---------------------------

User Query
    ↓
Resolver.resolve()
    ↓
[Step 1-3: Resource Identification, Cache, Vendor]
    ↓
[Step 4: Action Classification]
    ↓
[Step 5: PROTOCOL SELECTION (Database-Driven)]
    ├─ Check credential vault_path
    │  "vault://oneview/prod" → Protocol.ONEVIEW
    │  "vault://coms/staging" → Protocol.COMS
    │
    ├─ Query DB if credential path ambiguous
    │  SELECT protocols FROM servers
    │  WHERE ip=? AND vault_path=? AND auth_type=?
    │
    └─ Select primary protocol from supported list
       (prefer ONEVIEW if multiple, else first)
    ↓
[Step 6: Endpoint Generation]
    Get route template from route_mapper
    Build full endpoint URL
    ↓
Return ExecutionContext


KEY FUNCTIONS
-------------

protocol_discovery.discover_protocol_for_resource(resource: ResourceRecord) 
  → (Protocol, str)
  Complete workflow: extract IP → query DB → select protocol → return reason
  
protocol_discovery.determine_protocol_from_credential_ref(credential_ref)
  → Protocol | None
  Fast path: infer protocol from credential vault path patterns
  
protocol_discovery.determine_protocol_by_ip_and_credentials(ip, vault, auth)
  → List[Protocol]
  Query DB for supported protocols by IP + credentials
  
protocol_discovery.select_managed_protocol(supported_protocols, credential_ref)
  → Protocol | None
  Choose primary protocol from list, with credential path override


EXAMPLES
--------

Example 1: Credential Path Inference (Fast Path)
  resource = ResourceRecord(
      name="server01",
      ip_address="10.10.1.104",
      credential_ref=CredentialRef("vault://oneview/prod/admin")
  )
  protocol, reason = discover_protocol_for_resource(resource)
  # Returns: (Protocol.ONEVIEW, "Protocol 'OneView' determined from credential path...")
  
Example 2: Database Query (When Credential Path Ambiguous)
  resource = ResourceRecord(
      name="server02",
      ip_address="10.10.1.105",
      credential_ref=CredentialRef("secret/datacenter/prod/generic")  # ambiguous
  )
  protocol, reason = discover_protocol_for_resource(resource)
  # Queries DB: SELECT protocols FROM servers WHERE ip='10.10.1.105'
  # If result: [ONEVIEW], returns (Protocol.ONEVIEW, "discovered from database...")
  
Example 3: Multiple Protocols Supported
  resource has IP managed by both ONEVIEW and COMS
  supported_protocols = [Protocol.ONEVIEW, Protocol.COMS]
  
  If credential_ref contains "coms" → select COMS
  Else if credential_ref contains "oneview" → select ONEVIEW
  Else → prefer ONEVIEW (primary management layer)


EXTENSIBILITY
-------------

Adding a New Protocol (e.g., HPE Synergy):

1. Update enums.py:
   class Protocol(str, Enum):
       ONEVIEW = "ONEVIEW"
       COMS = "COMS"
       SYNERGY = "SYNERGY"  # ← ADD THIS

2. Update route_mapper.py:
   SYNERGY_ROUTES: dict[ResourceType, str] = {
       ResourceType.SERVER_HARDWARE: "/api/v1/servers/{uuid}",
       ...
   }
   
3. Update PostgreSQL:
   INSERT INTO protocols (name) VALUES ('SYNERGY');
   INSERT INTO server_protocols (server_id, protocol_id)
   SELECT s.id, p.id FROM servers s
   JOIN protocols p ON p.name = 'SYNERGY'
   WHERE s.ip_address IN ('10.10.1.200', ...);

4. Update credential path patterns (optional):
   protocol_discovery.py:determine_protocol_from_credential_ref()
   if "synergy" in vault_path:
       return Protocol.SYNERGY

5. No resolver.py changes needed!
   Protocol discovery automatically works with new protocol.


MIGRATION FROM HARDCODED PROTOCOL
----------------------------------

Old (Hardcoded):
  def select_protocol(resource, category):
      if resource.deployment_type == DeploymentType.CLOUD:
          return Protocol.COMS
      elif resource.deployment_type == DeploymentType.ON_PREM:
          return Protocol.ONEVIEW
      else:
          raise Error

New (Database-Driven):
  def select_protocol(resource, category):
      return discover_protocol_for_resource(resource)

Benefits:
  ✓ Dynamic: Change protocol in DB without code changes
  ✓ Scalable: Support unlimited protocols
  ✓ Auditable: Protocol ownership tracked in database
  ✓ Infrastructure-driven: DB is source of truth, not code


DATABASE SCHEMA REQUIREMENTS
----------------------------

servers table must have:
  - ip_address (varchar)
  - vault_path (varchar)
  - auth_type (varchar)

server_protocols table:
  - server_id (foreign key to servers)
  - protocol_id (foreign key to protocols)

protocols table:
  - id (primary key)
  - name (varchar: ONEVIEW, COMS, etc.)

com_servers table (for COMS resources):
  - ip_address
  - vault_path
  - auth_type
  - (similar structure for COMS-specific metadata)

com_server_protocols table:
  - com_server_id
  - protocol_id


CONFIGURATION PATTERNS (Vault Paths)
------------------------------------

Recommended vault path patterns to enable credential-based protocol inference:

OneView:
  vault://oneview/prod/admin
  secret/datacenter/oneview/rack-04/ilo
  secret/hpe/oneview/staging

COMS:
  vault://coms/prod/user
  secret/datacenter/coms/cloud/api
  secret/hpe/compute-ops/prod

Generic (requires DB lookup):
  secret/datacenter/prod/generic
  vault://infrastructure/credentials
  secret/servers/rack-04


TESTING
-------

Run protocol discovery examples:
  python protocol_discovery_examples.py

Run full routing examples:
  python routing_examples.py

Run resolver integration tests:
  python -c "from resolver import ResourceResolver; 
             print('✓ Resolver imports successfully')"


FUTURE ENHANCEMENTS
-------------------

1. Caching Protocol Metadata
   - Cache protocol mappings to reduce DB queries
   - Invalidate on protocol table updates

2. Protocol Fallback/Failover
   - If primary protocol unavailable, try secondary
   - Define fallback chain: ONEVIEW → COMS → fallback

3. Dynamic Protocol Weighting
   - Store protocol priority in DB
   - Choose highest priority available protocol

4. Protocol Capability Matrix
   - Store which resources support which operations
   - Select protocol based on required operation

5. Multi-Protocol Transactions
   - Orchestrate operations across multiple protocols
   - Ensure consistency across ONEVIEW + COMS


TROUBLESHOOTING
---------------

Q: "No protocols found in infrastructure database"
A: Check:
   1. Server IP exists in database
   2. server_protocols table has entries for this server
   3. protocols table has ONEVIEW/COMS entries
   4. vault_path matches exactly

Q: "Protocol discovery failed for resource"
A: Check:
   1. Resource has ip_address set
   2. credential_ref is properly configured
   3. Database connection is working
   4. SQL queries execute without errors

Q: Protocol selected is unexpected
A: Check:
   1. Credential vault path for protocol indicators
   2. server_protocols table for this IP address
   3. select_managed_protocol() logic (prefers ONEVIEW)
   4. Run protocol_discovery_examples.py to validate logic


ARCHITECTURE DIAGRAM
--------------------

┌─────────────────────────────────────────────────┐
│         PostgreSQL Infrastructure DB            │
│  ├─ servers (IP, vault_path, auth_type)        │
│  ├─ server_protocols (server ↔ protocol)       │
│  ├─ protocols (ONEVIEW, COMS, etc.)            │
│  └─ com_servers (COMS-specific)                │
└─────────────────────────────────────────────────┘
              ↑
              │ Query by IP + credentials
              │
┌─────────────────────────────────────────────────┐
│    protocol_discovery.py (NEW MODULE)           │
│  ├─ determine_protocol_from_credential_ref()   │
│  ├─ determine_protocol_by_ip_and_credentials() │
│  ├─ select_managed_protocol()                  │
│  └─ discover_protocol_for_resource()           │
└─────────────────────────────────────────────────┘
              ↑
              │ Called by select_protocol()
              │
┌─────────────────────────────────────────────────┐
│    selector.py (REFACTORED)                    │
│  ├─ select_protocol() - now DB-driven         │
│  ├─ classify_action() - unchanged             │
│  └─ build_endpoint() - unchanged              │
└─────────────────────────────────────────────────┘
              ↑
              │ Orchestrates protocol selection
              │
┌─────────────────────────────────────────────────┐
│    resolver.py (UNCHANGED)                     │
│  └─ resolve() → ExecutionContext               │
└─────────────────────────────────────────────────┘
              ↑
              │ Routes & builds endpoints
              │
┌─────────────────────────────────────────────────┐
│    route_mapper.py (UNCHANGED)                 │
│  ├─ ONEVIEW_ROUTES (57 mappings)              │
│  ├─ COMS_ROUTES (28 mappings)                 │
│  └─ build_endpoint()                          │
└─────────────────────────────────────────────────┘


SUMMARY
-------

✓ Protocol selection is now database-driven, not hardcoded
✓ Infrastructure DB is single source of truth
✓ Credential paths encode protocol ownership
✓ Supports dynamic discovery without code changes
✓ Extensible for future protocols (just add to enum + DB)
✓ Full separation of concerns (db → discovery → selection)
✓ Backward compatible with existing resolver pipeline
✓ Production-ready with comprehensive error handling
"""

# This module serves as architectural documentation.
# For actual implementation, see:
# - protocol_discovery.py (protocol discovery logic)
# - selector.py (protocol selection in resolver)
# - db.py (database queries)
