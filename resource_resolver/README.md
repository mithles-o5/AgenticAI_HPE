# HPE Resource Resolver Subsystem

This document provides architectural, setup, and runtime execution specifications for the **Resource Resolver** subsystem of the HPE Agentic AI platform. It is written to serve as the definitive guide for engineering onboarding.

---

# Resource Resolver Overview

### Why This Module Exists
In large-scale enterprise environments, IT assets (servers, switches, routers, firewalls, and storage arrays) are managed across fragmented deployment topologies by different infrastructure management controllers—specifically **HPE OneView** (typically on-premise hardware managers) and **HPE Compute Ops Management** (abbreviated as **COMS**, a cloud-managed SaaS portal). 

Downstream workflows need to query device states or invoke power/provisioning operations without hardcoding where a specific device resides, what software manager controls it, or what specific REST URL structure that manager expects.

The **Resource Resolver** solves this problem by acting as a high-performance, vendor-agnostic routing registry. It dynamically translates generic user commands and arbitrary device identifiers into an authoritative execution target and synthesis of the exact API URL required by the target controller.

### Inputs & Outputs
* **Inputs**:
  * A query string (natural language or direct command, e.g., `"power off agg-sw02-601"`).
  * An optional `identifier_type` string (explicit hint: `ip`, `sn`, or `fqdn`).
  * An optional `requested_by` string (audit log label, defaults to `"mcp-orchestrator"`).
* **Outputs**:
  * A serialized `RouteResolution` JSON payload containing:
    * `identifier`: Normalized query token used for lookup.
    * `identifier_type`: Resolved category (`ip`, `sn`, or `fqdn`).
    * `management_source`: Inferred vendor host type (`oneview` or `coms`).
    * `source_host`: FQDN or IP of the managing orchestrator.
    * `mcp_tool`: Target MCP tool name downstream (e.g., `oneview` or `compute_ops`).
    * `credential_ref`: Safe reference to vault-stored credentials.
    * `cache_status`: Hit/Miss resolution performance marker.
    * `resolution_ms`: Duration of the routing lookup.
    * `api_endpoint`: Synthesized destination URL for the action.
    * `resource`: Struct containing resource properties (`name`, `vendor`).
    * `action`: Struct detailing the operation category and canonical action.
    * `device`: Direct dictionary serialization of the resolved `DeviceRecord`.

#### Example Execution
* **Input Query**: 
  `"power off agg-sw02-601"`
* **Output Resolution**:
  ```json
  {
    "identifier": "agg-sw02-601",
    "identifier_type": "sn",
    "management_source": "coms",
    "source_host": "coms-01.cloud.local",
    "mcp_tool": "compute_ops",
    "credential_ref": null,
    "cache_status": "miss",
    "resolution_ms": 14,
    "api_endpoint": "https://coms-01.cloud.local/compute-ops/v1/switches/coms-uuid-aggsw05/power-off",
    "resource": {
      "name": "agg-sw05.cloud.local",
      "vendor": "HPE"
    },
    "action": {
      "category": "Operational",
      "action": "OFF"
    },
    "device": {
      "id": "2e71d3df-8349-4b6b-84a1-db9b0a1d46b7",
      "serial_number": "agg-sw05",
      "ip_address": "10.200.1.21",
      "fqdn": "agg-sw05.cloud.local",
      "management_source": "coms",
      "source_host": "coms-01.cloud.local",
      "source_device_id": "coms-uuid-aggsw05",
      "device_type": "switch",
      "last_seen": "2026-06-12T19:18:28+05:30",
      "created_at": "2026-06-12T19:18:28+05:30",
      "updated_at": "2026-06-12T19:18:28+05:30"
    }
  }
  ```

---

# Core Responsibility

The Resource Resolver is designed with strict separation of concerns:

### What it is Responsible For:
1. **Natural Language Intent Parsing**: Classifying human-written phrases to determine actions (e.g., `ON`, `OFF`, `STATUS`) and stripping noise tokens.
2. **Identifier Extraction and Normalization**: Extracting clean tokens (IPs, serials, hostnames) and stripping boundary punctuation.
3. **Identifier Type Inference**: Automatically identifying whether a token is an IP address, FQDN, or serial number.
4. **Hot Cache Lookup**: Providing sub-millisecond lookups via Redis/Memurai using key-value serialization.
5. **Database Registry Lookup**: Performing fallback queries on Cache Misses against PostgreSQL database indexes.
6. **Cache Re-Warming**: Executing pipelined updates to Redis when missing keys are queried and resolved from PostgreSQL.
7. **Dynamic Route Synthesis**: Querying the database-driven `endpoint_registry` to construct execution URLs by mapping `(vendor, device_type, action)` to parameterized API paths.
8. **Routing Audit Logging**: Writing resolution metadata (time, requestor, cache status) into database audit tables.
9. **Daemon Background Polling**: Maintaining a separate execution thread to periodically sync remote controller inventories into PostgreSQL.

### What it is NOT Responsible For:
1. **Executing Actions / API Dispatch**: It does *not* fire HTTP requests to the target manager systems in production. It only resolves and returns the execution context to the orchestrator.
2. **Authentication / Token Exchange**: It does *not* communicate with identity providers or retrieve secrets. It only exposes credential vaults configuration paths (`credential_ref`).
3. **Authorization / RBAC**: It does *not* enforce access policies.
4. **Hardware control / Session state**: It does *not* maintain connections to hardware consoles or monitor transient power changes.

---

# Module Architecture

The following diagram illustrates the relationship between components during a query resolution cycle:

```
                  ┌──────────────────────────┐
                  │       Client Query       │
                  └─────────────┬────────────┘
                                │
                                ▼
                  ┌──────────────────────────┐
                  │        QueryAgent        │
                  │   (Intent/Token Parser)  │
                  └─────────────┬────────────┘
                                │
                                ▼
                  ┌──────────────────────────┐
                  │     ResourceResolver     │
                  │  (Type Inference Engine) │
                  └──────┬────────────┬──────┘
                         │            │
             (Hot-Path)  ▼            ▼  (Cold-Path)
            ┌───────────────┐      ┌─────────────────────────┐
            │ ResourceCache │      │    ResourceRegistry     │
            │  (Redis/Key)  │      │ (PostgreSQL DBLoader)   │
            └───────────────┘      └──────────┬──────────────┘
                                              │
                                              ▼
                                   ┌────────────────────┐
                                   │ DeviceQueries      │
                                   │ EndpointQueries    │
                                   └──────────┬─────────┘
                                              │
                                              ▼
                                   ┌────────────────────┐
                                   │  Route Resolution  │
                                   │    Context built   │
                                   └────────────────────┘
```

### Component Breakdown
* **`QueryAgent`**: Lightweight NLP component. Runs regular expression filters sequentially against input text to match known actions, strips them out, and isolates clean boundary-trimmed identifiers.
* **`ResourceResolver`**: Main routing orchestrator. Determines the query mode (IP/Serial/FQDN), coordinates caching layers, loads records, calls route discoverers, and delegates URL building.
* **`ResourceCache`**: Redis-backed wrapper. Writes and reads serialized JSON payloads with pipelines and manages keyspace expiration.
* **`ResourceRegistry`**: Authoritative data layer. Abstracts PostgreSQL lookups, device registration, and log execution.
* **Endpoint Registry**: DB-driven catalog mapping API endpoint templates to specific hardware and operations.

---

# File Guide

Here is the functional map of files associated with the **Resource Resolver** subsystem:

## [db.py](db.py)
* **Purpose**: Manages connection pooling to PostgreSQL.
* **Used By**: `db_loader.py`, `db_manage.py`, `db_seed.py`, `db_queries.py`, `seed_endpoint_registry.py`.
* **Dependencies**: `psycopg2`, `psycopg2.pool`, `psycopg2.extras`.
* **Key Classes**:
  * `DatabaseManager`: A thread-safe singleton connection manager implementing `.get_connection()`, `.return_connection()`, `.execute_query()`, and `.execute_many()`.
* **Runtime Role**: Provides DB connection resources. If deleted, all Postgres communications halt immediately, preventing cold-path lookups, polling logs, and route mappings.

## [db_schema.sql](db_schema.sql)
* **Purpose**: Establishes database architecture.
* **Used By**: Executed by `db_manage.py` to provision schema.
* **Key Entities**: Table definitions for `devices`, `routing_audit`, `poll_history`, and `endpoint_registry`.
* **Runtime Role**: Contains the structure of the tables. If removed or altered outside of migration, DB initialization fails, causing runtime query execution errors.

## [db_queries.py](db_queries.py)
* **Purpose**: Isolates raw SQL statements from business logic.
* **Used By**: `registry.py`, `cache.py`, `power_ops.py`, `polling_engine.py`, `mcp_tool.py`.
* **Dependencies**: `db.py`, `enums.py`, `errors.py`, `protocol_discovery.py`.
* **Key Classes**:
  * `DeviceQueries`: Selects/upserts/syncs records.
  * `RoutingAuditQueries`: Commits telemetry logs.
  * `PollHistoryQueries`: Registers background sync states.
  * `EndpointRegistryQueries`: Lookups dynamic REST templates with a fallback mechanism.
* **Runtime Role**: Orchestrates queries. Without this file, the resolver cannot retrieve device records, write logs, or find endpoint paths.

## [db_manage.py](db_manage.py)
* **Purpose**: Commands CLI admin interface.
* **Used By**: System Administrator / Engineer setup.
* **Dependencies**: `db.py`, `db_seed.py`.
* **Key Classes**:
  * `DatabaseManager`: Implements CLI triggers (`init_schema`, `seed_database`, `clear_database`).
* **Runtime Role**: Performs setup operations. Removing it has no runtime impact on active queries, but blocks the ability to initialize or wipe the PostgreSQL database via standard CLI commands.

## [db_seed.py](db_seed.py)
* **Purpose**: Automates mock inventory generation.
* **Used By**: `db_manage.py`.
* **Dependencies**: `db.py`.
* **Key Functions**:
  * `seed_current_schema()`: Drops tables and creates mock batches of OneView and COMS devices.
  * `clear_database()`: Performs cascading truncate calls.
* **Runtime Role**: Used for testing. Removal disables mock data seeding during sandbox setup.

## [seed_endpoint_registry.py](seed_endpoint_registry.py)
* **Purpose**: Seed the REST routing templates.
* **Used By**: Engineer configuration flow.
* **Dependencies**: `db.py`.
* **Key Functions**:
  * `parse_prompt_file()`: Parses text templates, skips templates matching `{resource_category}`, and builds entries.
  * `seed()`: Performs transaction-wrapped bulk updates.
* **Runtime Role**: Used for provisioning. If missing, endpoint routing mappings cannot be loaded from prompt files into PostgreSQL.

## [cache.py](cache.py)
* **Purpose**: Manages Redis/Memurai caching.
* **Used By**: `resolver.py`, `polling_engine.py`, `mcp_tool.py`.
* **Dependencies**: `redis`, `enums.py`, `records.py`, `protocol_discovery.py`.
* **Key Classes**:
  * `ResourceCache`: Manages keyspaces, pipelined updates, warming functions, key eviction, and non-blocking SCAN statistics.
* **Runtime Role**: Handles caching. If removed, the resolver loses its cache layer, causing all lookups to query the PostgreSQL database directly, reducing throughput.

## [query_agent.py](query_agent.py)
* **Purpose**: Extracts search tokens and intents using NLP preprocessing.
* **Used By**: `mcp_tool.py`.
* **Dependencies**: `re`, `typing.NamedTuple`.
* **Key Classes**:
  * `QueryAgent`: Preprocesses query queries deterministically via regex.
* **Runtime Role**: Normalizes inputs. If removed, natural language lookups fail, and clients must supply pre-parsed identifiers and explicit parameters.

## [resolver.py](resolver.py)
* **Purpose**: Main routing coordinator.
* **Used By**: `mcp_tool.py`.
* **Dependencies**: `cache.py`, `enums.py`, `errors.py`, `records.py`, `registry.py`, `protocol_discovery.py`, `power_ops.py`.
* **Key Classes**:
  * `ResourceResolver`: Coordinates lookups, type inferences, caching, and database resolution.
* **Runtime Role**: Orchestrates lookups. If removed, the Resource Resolver subsystem cannot function.

## [power_ops.py](power_ops.py)
* **Purpose**: Coordinates target URL formatting.
* **Used By**: `resolver.py`.
* **Dependencies**: `records.py`, `protocol_discovery.py`, `errors.py`, `db_queries.py`.
* **Key Classes**:
  * `ExecutionOrchestrator`: Resolves paths from the endpoint registry and maps managers to handlers.
* **Runtime Role**: Builds URL routes. If removed, route synthesis fails, preventing the resolution of target API URLs.

## [protocol_discovery.py](protocol_discovery.py)
* **Purpose**: Maps managers to MCP tools and credentials.
* **Used By**: `resolver.py`, `power_ops.py`, `cache.py`.
* **Dependencies**: `os`.
* **Key Functions**:
  * `discover_route()`: Returns target tools and credential paths.
  * `normalize_management_source()`: Normalizes manager names (e.g. `com` -> `coms`).
* **Runtime Role**: Resolves targets. If removed, target tool and credential configuration lookups fail.

## [records.py](records.py)
* **Purpose**: Defines data schemas.
* **Used By**: All files in the subsystem.
* **Dependencies**: `enums.py`.
* **Key Classes**:
  * `DeviceRecord`: Representation of a physical device.
  * `RouteResolution`: Context payload returned by the resolver.
* **Runtime Role**: Serializes and deserializes payloads. Removing it halts all data routing and storage operations.

## [enums.py](enums.py)
* **Purpose**: Defines system constants.
* **Used By**: Nearly all files in the subsystem.
* **Key Classes**:
  * `IdentifierType`: `ip`, `sn`, `fqdn`.
  * `CacheStatus`: `hit`, `miss`.
  * `ManagementSource`: `oneview`, `coms`.
* **Runtime Role**: Provides type safety. Removing it causes validation and syntax errors throughout the project.

## [errors.py](errors.py)
* **Purpose**: Centralizes custom exceptions.
* **Used By**: `resolver.py`, `power_ops.py`, `mcp_tool.py`, `db_queries.py`.
* **Key Classes**:
  * `ResolverError`: Subsystem base exception.
  * `ResourceNotFoundError`: Raised when a device lookup fails.
  * `EndpointNotFoundError`: Raised when an action mapping is missing.
* **Runtime Role**: Handles error classification. If removed, the application cannot catch or raise domain-specific exceptions.

## [polling_engine.py](polling_engine.py)
* **Purpose**: Periodically pulls inventories to sync PostgreSQL and Redis.
* **Used By**: `mcp_tool.py`.
* **Dependencies**: `concurrent.futures.ThreadPoolExecutor`, `threading`, `cache.py`, `db_queries.py`, `records.py`.
* **Key Classes**:
  * `PollingEngine`: Executes multi-threaded inventory queries, merges data with PostgreSQL, and updates Redis cache entries.
* **Runtime Role**: Syncs inventory. If removed, the database and cache will drift from active controller inventories over time.

## [db_loader.py](db_loader.py)
* **Purpose**: Bootstraps the PostgreSQL database registry during startup.
* **Used By**: `mcp_tool.py`.
* **Dependencies**: `db.py`, `registry.py`.
* **Key Functions**:
  * `load_registry_from_db()`: Verifies database connectivity and returns a registry instance.
* **Runtime Role**: Validates startup connections. If removed, the MCP server cannot instantiate or verify its registry on boot.

## [mcp_tool.py](mcp_tool.py)
* **Purpose**: Main entrypoint for the MCP Server.
* **Used By**: External orchestrators (FastMCP execution environment).
* **Dependencies**: `mcp.server.fastmcp`, `resolver.py`, `polling_engine.py`, `db_loader.py`, `cache.py`.
* **Key Functions**:
  * `resolve_resource()`: Exposes query resolution as an MCP tool.
  * `list_devices()`: Exposes device listings with pagination.
  * `manual_register_device()`: Manually adds devices to the database and cache.
  * `cache_stats()` and `resolver_statistics()`: Exposes system health monitoring.
* **Runtime Role**: Exposes MCP tools. If removed, external clients cannot call resolver tools.

---

# Database Design

The PostgreSQL registry consists of four tables designed for inventory management, route mapping, and auditing.

```
          ┌───────────────────────┐
          │   endpoint_registry   │
          │                       │
          └───────────────────────┘
          
          ┌───────────────────────┐
          │        devices        │
          │                       │
          └───────────┬───────────┘
                      │
            ┌─────────┴─────────┐
            ▼                   ▼
    ┌───────────────┐   ┌──────────────┐
    │ routing_audit │   │ poll_history │
    │               │   │              │
    └───────────────┘   └──────────────┘
```

## Tables

### 1. `devices`
* **Purpose**: Authoritative record of active devices and their respective management controllers.
* **Columns**:
  * `id` (`UUID`, PK, Default `gen_random_uuid()`): Unique system primary key.
  * `serial_number` (`VARCHAR(64)`, UNIQUE, NOT NULL): Device hardware serial number.
  * `ip_address` (`INET`): Assigned management IP.
  * `fqdn` (`VARCHAR(255)`): Fully qualified domain name.
  * `management_source` (`VARCHAR(32)`, NOT NULL): Controller type (`oneview` or `coms`).
  * `source_host` (`VARCHAR(255)`): FQDN or IP of the managing controller.
  * `source_device_id` (`VARCHAR(128)`): Identifier on the remote manager.
  * `device_type` (`VARCHAR(64)`): Device classification (e.g. `server`, `switch`, `storage`).
  * `last_seen` (`TIMESTAMPTZ`): Timestamp of the last successful poll update.
  * `created_at` (`TIMESTAMPTZ`): Record creation timestamp.
  * `updated_at` (`TIMESTAMPTZ`): Record modification timestamp.
* **Indexes**:
  * `idx_devices_ip` ON `devices(ip_address)` (Accelerates IP-based lookups).
  * `idx_devices_fqdn` ON `devices(fqdn)` (Accelerates hostname lookups).
  * `idx_devices_source` ON `devices(management_source, source_host)` (Optimizes source checks).
* **Relationships**: Log targets in `routing_audit` and `poll_history` reference these fields.
* **Reads**: `resolver.py`, `polling_engine.py`, `mcp_tool.py`.
* **Writes**: `db_seed.py`, `polling_engine.py`, `mcp_tool.py`.

### 2. `endpoint_registry`
* **Purpose**: Stores API routing endpoints to map management operations dynamically.
* **Columns**:
  * `id` (`UUID`, PK): Primary identifier.
  * `vendor` (`VARCHAR(64)`, NOT NULL): Controller type (`oneview` or `coms`).
  * `device_type` (`VARCHAR(64)`, NOT NULL, default `'generic'`): Hardware category.
  * `action_key` (`VARCHAR(128)`, NOT NULL): Command token (e.g. `ON`, `OFF`, `STATUS`).
  * `http_method` (`VARCHAR(16)`, NOT NULL): API verb (`GET`, `POST`, `PUT`, `DELETE`).
  * `api_path` (`TEXT`, NOT NULL): Verbatim template path (e.g. `/rest/server-hardware/{id}/powerState`).
  * `created_at` (`TIMESTAMPTZ`): Creation timestamp.
* **Constraints**: `UNIQUE (vendor, device_type, action_key, api_path, http_method)`.
* **Indexes**:
  * `idx_endpoint_registry_lookup` ON `endpoint_registry (lower(vendor), lower(device_type), lower(action_key))` (Speeds routing lookups).
* **Reads**: `power_ops.py`, `db_queries.py`.
* **Writes**: `seed_endpoint_registry.py`.

### 3. `routing_audit`
* **Purpose**: Telemetry database recording execution statistics.
* **Columns**:
  * `id` (`UUID`, PK): Log entry identifier.
  * `identifier` (`VARCHAR(255)`, NOT NULL): Target token queried.
  * `identifier_type` (`VARCHAR(16)`, NOT NULL): Inferred type (`ip`, `sn`, `fqdn`).
  * `resolved_source` (`VARCHAR(32)`): Resulting controller type.
  * `resolved_host` (`VARCHAR(255)`): Resulting manager IP/host.
  * `cache_hit` (`BOOLEAN`, NOT NULL): Cache hit indicator.
  * `resolution_ms` (`INTEGER`): Duration of lookup.
  * `requested_by` (`VARCHAR(128)`): Calling client identifier.
  * `timestamp` (`TIMESTAMPTZ`): Timestamp of the request.
* **Reads**: `mcp_tool.py`, `cache.py`.
* **Writes**: `resolver.py`, `db_queries.py`.

### 4. `poll_history`
* **Purpose**: Tracks inventory polling runs.
* **Columns**:
  * `id` (`UUID`, PK): Log entry identifier.
  * `source_type` (`VARCHAR(32)`, NOT NULL): Controller type.
  * `source_host` (`VARCHAR(255)`, NOT NULL): Controller hostname.
  * `devices_found` (`INTEGER`): Total devices retrieved.
  * `devices_added` (`INTEGER`): New devices inserted.
  * `devices_removed` (`INTEGER`): Stale devices removed.
  * `duration_ms` (`INTEGER`): Sync duration.
  * `status` (`VARCHAR(16)`): `'success'` or `'failed'`.
  * `error_message` (`TEXT`): Error logs if sync failed.
  * `timestamp` (`TIMESTAMPTZ`): Run timestamp.
* **Indexes**:
  * `idx_poll_history_timestamp` ON `poll_history(timestamp)`.
* **Reads**: `mcp_tool.py`.
* **Writes**: `polling_engine.py`, `db_queries.py`.

---

# Cache Design

The Resource Cache uses **Redis/Memurai** to serve device routing details, bypassing PostgreSQL for repeat lookups.

### Cache Key Architecture
The cache stores key-value associations and source tracking lists:
* **Lookup Keys**: Maps a typed identifier to a serialized `DeviceRecord` JSON payload.
  * Key Format: `resolver:{identifier_type}:{identifier_token}` (tokens are stored in lowercase).
  * *Example*: `resolver:sn:dc1-a7` -> JSON string representation of `DeviceRecord`.
  * *Example*: `resolver:ip:10.100.1.10` -> JSON string representation of `DeviceRecord`.
* **Source Tracking Sets**: Track device membership on specific management controllers using Redis `SADD`.
  * COMS Source Key: `resolver:source:coms:{source_device_id}`
  * OneView Source Key: `resolver:source:{source_host}`
  * *Example*: `resolver:source:oneview-01.mgmt.local` -> Set of member serial numbers.
* **Poll Run Keys**: Tracks background metadata per source.
  * Key Format: `resolver:poll:{source_type}:{identifier}`

### Cache Hit Flow
1. Resolver receives query for serial number `"dc1-a7"`.
2. Computes lookup key: `resolver:sn:dc1-a7`.
3. Calls Redis `GET "resolver:sn:dc1-a7"`.
4. Redis returns JSON payload.
5. Resolver deserializes the JSON string into a `DeviceRecord` object and returns `cache_status="hit"`.

### Cache Miss Flow
1. Resolver calls Redis `GET "resolver:sn:dc1-a7"`, which returns `nil`.
2. Resolver queries PostgreSQL:
   ```sql
   SELECT * FROM devices WHERE lower(serial_number) = 'dc1-a7' LIMIT 1;
   ```
3. PostgreSQL returns the row.
4. Resolver deserializes it into a `DeviceRecord`.
5. **Cache Warming Step**: The resolver calls `ResourceCache.put_device`. This writes key-value pairs to Redis using a pipeline:
   * `SETEX resolver:sn:dc1-a7 900 <JSON_PAYLOAD>`
   * `SETEX resolver:ip:10.100.1.10 900 <JSON_PAYLOAD>`
   * `SETEX resolver:fqdn:dc1-a7.datacenter.local 900 <JSON_PAYLOAD>`
   * `SADD resolver:source:oneview-01.mgmt.local dc1-a7`
   * `EXPIRE resolver:source:oneview-01.mgmt.local 900`
6. Returns `cache_status="miss"`.

### Cache Warming Strategies
* **On-Demand Warming**: Triggers during resolve calls on cache misses.
* **Background Sync Warming**: The `PollingEngine` writes synced inventory batches directly to Redis during its polling cycles using pipelined writes.
* **Incremental Seeding**: `ResourceCache` implements warming functions:
  * `warm_recent_devices(limit)`: Loads the most active devices from `routing_audit` logs and updates Redis.
  * `warm_updated_devices(limit)`: Selects devices sorted by `updated_at` from PostgreSQL to warm Redis.

### Cache Invalidation Strategy
* **Time To Live (TTL)**: Cache entries default to an expiration time of 900 seconds (15 minutes), configured via `CACHE_TTL`.
* **Explicit Eviction**: Triggered on manual changes. Calling `ResourceCache.invalidate_device` deletes the associated keys:
  ```python
  keys = ["resolver:ip:10.100.1.10", "resolver:sn:dc1-a7", "resolver:fqdn:dc1-a7.datacenter.local"]
  client.delete(*keys)
  ```

---

# Registry Loading

On server boot, the Resource Resolver loads and validates its database configuration.

```
       ┌────────────────────────┐
       │   mcp_tool.py Starts   │
       └───────────┬────────────┘
                   │
                   ▼
       ┌────────────────────────┐
       │ load_registry_from_db  │
       └───────────┬────────────┘
                   │
         [Connection Test]
                   │
         ┌─────────┴─────────┐
         ▼                   ▼
     (Succeeds)          (Fails)
   ┌───────────┐     ┌─────────────┐
   │ Instantiate │     │ Log Error / │
   │ Registry  │     │ Raise Excep │
   └───────────┘     └─────────────┘
```

1. **Loader Script**: `db_loader.py` exports `load_registry_from_db()`.
2. **Boot Sequence**: During startup, `mcp_tool.py` calls `load_registry_from_db()`.
3. **Connectivity Check**: The loader calls `db_manager.test_connection()` to run:
   ```sql
   SELECT 1;
   ```
4. **Outcome**:
   * **Success**: Returns a `ResourceRegistry` instance to bind to the resolver.
   * **Failure**: Logs `"[DB Loader] Database connection failed"` and raises a `RuntimeError("Cannot connect to database")`, halting the server initialization.

---

# Polling Engine

The Polling Engine runs background sync cycles to match the local registry with upstream inventory systems.

```
                  ┌───────────────────────────┐
                  │ Background Thread Wakes   │
                  └─────────────┬─────────────┘
                                │
                                ▼
                  ┌───────────────────────────┐
                  │ Discover active OneView / │
                  │ COMS management endpoints │
                  └─────────────┬─────────────┘
                                │
                                ▼
                  ┌───────────────────────────┐
                  │   ThreadPoolExecutor      │
                  │   Concurrent Collection   │
                  └─────────────┬─────────────┘
                                │
                                ▼
                  ┌───────────────────────────┐
                  │ Authoritative DB Sync     │
                  │ (Insert, Update, Delete)  │
                  └─────────────┬─────────────┘
                                │
                                ▼
                  ┌───────────────────────────┐
                  │ Pipelined Cache Warming   │
                  └─────────────┬─────────────┘
                                │
                                ▼
                  ┌───────────────────────────┐
                  │ Write Poll History Log    │
                  └─────────────┬─────────────┘
                                │
                                ▼
                  ┌───────────────────────────┐
                  │ Sleep for Interval (600s) │
                  └───────────────────────────┘
```

### How Polling Works
* **Daemon Thread**: Spun up by `start_background_polling()` on server start.
* **Interval**: Set by `POLL_INTERVAL_SECONDS` (defaults to 600 seconds / 10 minutes).
* **Inventory Collection**:
  * Discover target controllers using discovery clients.
  * Spawns worker threads inside a `ThreadPoolExecutor` to pull inventory lists.
  * Normalizes the retrieved device data.
* **Database Updates**:
  Calls `DeviceQueries.sync_source_devices` within a database transaction:
  * Computes the difference between current records and the polled inventory.
  * **Inserts** new records.
  * **Updates** modified fields (e.g. IPs, FQDNs).
  * **Deletes** stale devices no longer returned by the manager.
* **Cache Warming**: Loops through the synced device records and writes them to Redis using pipelines to minimize round-trip latency.
* **Telemetry logging**: Commits sync statistics (duration, changes, status) to the `poll_history` table.

---

# Startup Flow

The startup sequence of the Resource Resolver service when launching `mcp_tool.py`:

```
1. Load configurations from .env
   ├── Read DB details
   └── Read CACHE_TTL and POLL_INTERVAL_SECONDS
2. Initialize DatabaseManager
   └── Open psycopg2 connection pool (min: 2, max: 10)
3. Initialize ResourceCache
   └── Ping Redis/Memurai to confirm connectivity
4. Verify Registry Configuration
   └── Call load_registry_from_db() and test DB connection
5. Instantiate ResourceResolver
   └── Bind ResourceRegistry and ResourceCache instances
6. Initialize FastMCP Server
   └── Register "resource-resolver" server target
7. Spin up Background Polling Loop
   └── Run OASF-Background-Polling daemon thread
8. Register MCP Tools
   └── resolve_resource, list_devices, manual_register_device, cache_stats
9. Start TCP/STDIO listener
   └── Ready to receive client request payloads
```

---

# Database Initialization

Running database schema initialization:
```bash
python db_manage.py init
```

* **Execution Sequence**:
  1. Verifies database connectivity.
  2. Reads the `db_schema.sql` file.
  3. Splits SQL statements at semicolon boundaries and runs them sequentially.
  4. Skips errors containing `"already exists"` to allow safe re-runs.
* **Entities Created**:
  * Extensions: `pgcrypto` (For UUID generation).
  * Tables: `devices`, `routing_audit`, `poll_history`, and `endpoint_registry`.
  * Indexes: `idx_devices_ip`, `idx_devices_fqdn`, `idx_devices_source`, `idx_poll_history_timestamp`, `idx_endpoint_registry_lookup`.

---

# Database Seeding

Running database inventory seeding:
```bash
python db_manage.py seed
```

* **Mock Payload Stats**:
  * **OneView Devices**: 1,000 devices generated with IP prefixes `10.100.x.x` and serials matching standard enterprise formats.
  * **COMS Devices**: 500 devices generated with IP prefixes `10.200.x.x`.
  * **Testing Targets**: 16 dedicated static records seeded for regression testing (including `dc1-a7`, `compute-22`, `prod-x1`, `stg-array-02`).
* **Generation logic**: Device types are rotated across `server`, `switch`, `router`, `firewall`, and `storage` using index operations in `generate_device_batch()`.
* **Adding Seed Data**: Modify the `testing_devices` array within `seed_current_schema()` in `db_seed.py`. Add your custom device tuple:
  ```python
  ("custom-serial-99", "10.100.1.99", "custom-node.datacenter.local", "oneview", "oneview-01.mgmt.local", "ov-uuid-custom99", "server")
  ```

---

# Endpoint Registry Seeding

Running endpoint route seeding:
```bash
python seed_endpoint_registry.py
```

* **Workflow**:
  1. Reads `oneview_api_prompts.txt` and `comops_api_prompts.txt` from the project root.
  2. Parses block segments, filtering out generic template paths containing `{resource_category}`.
  3. Infers the `device_type` from the path (e.g. `/rest/server-hardware` maps to `server`, `/rest/storage-systems` maps to `storage`).
  4. Normalizes action mappings (e.g., PUT /powerState maps to actions `ON`, `OFF`, `RESET`, `COLD_BOOT`).
  5. Runs a bulk-insert transaction to populate the `endpoint_registry` table.
* **Usage**:
  The `ExecutionOrchestrator` queries these endpoint configurations at runtime to translate actions like `OFF` into the target manager's API path (e.g., `/compute-ops-mgmt/v1/switches/{id}/power-off`).

---

# Local Setup

This setup guide assumes a clean machine environment.

### 1. Install System Prerequisites
* Install Python 3.9+ (Ensure it is added to your system path).
* Install **PostgreSQL** Database Server.
* Install **Redis** (or Memurai for native Windows development).

### 2. Configure Local Databases
* Create a database named `hpe_agentic_ai` in your PostgreSQL instance.
* Start Redis/Memurai:
  ```bash
  # Windows (Memurai CLI)
  memurai-server.exe
  
  # Linux
  sudo systemctl start redis-server
  ```

### 3. Install Dependencies
Run the install command inside your virtual environment:
```bash
# Initialize venv
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Create Local Configurations
Copy the template file to `.env` and fill in your database credentials:
```bash
cp .env.example .env
```
Example `.env` configuration:
```ini
DB_HOST=localhost
DB_PORT=5432
DB_NAME=hpe_agentic_ai
DB_USER=postgres
DB_PASSWORD=your_secure_password
CACHE_TTL=900
```

### 5. Provision the Database
Run the setup, seeding, and endpoint registration scripts:
```bash
python db_manage.py init
python db_manage.py seed
python seed_endpoint_registry.py
```

### 6. Run the MCP Resolver Server
Start the server:
```bash
python mcp_tool.py
```

---

# Troubleshooting

| Error | Primary Cause | Fix |
| :--- | :--- | :--- |
| `ResourceNotFoundError` | The requested identifier is missing from both the Redis cache and PostgreSQL database. | Verify the serial number or IP matches an active record. Run `python db_manage.py seed` or call the `manual_register_device` tool. |
| `EndpointNotFoundError` | The `endpoint_registry` table does not contain a mapping matching the `(vendor, device_type, action)` query. | Ensure `seed_endpoint_registry.py` has run. If the mapping is custom, add it to `oneview_api_prompts.txt` / `comops_api_prompts.txt` and re-run the script. |
| Connection Pool Timeout | Database connections are exhausted or the database server is unresponsive. | Confirm PostgreSQL is running. Check connection pool configurations in `db.py` and adjust pool sizing. |
| `redis.exceptions.ConnectionError` | The Redis/Memurai server is stopped or running on an alternate port. | Confirm Redis/Memurai is running. Check `.env` port configurations. |
| Overridden FQDN Lookups | An FQDN identifier was resolved as a serial number because it lacked dots. | The resolver requires a dot (`.`) in the query to classify it as an FQDN. Check FQDN formatting. |
| Polling Engine Failure | Discovery clients or managers returned errors during inventory sync. | Check log outputs in `resolver.log` for upstream connection details. |

---

# Extending the Resolver

Follow these steps to extend the Resource Resolver subsystem:

### 1. Add a New Identifier Type
1. Open `enums.py`.
2. Append the type to the `IdentifierType` enum:
   ```python
   class IdentifierType(str, Enum):
       NEW_TYPE = "new_type"
   ```
3. Open `resolver.py`.
4. Update `_normalize_identifier_type` and `_infer_identifier_type` to parse the new identifier format.
5. Update `DeviceQueries.get_by_identifier` in `db_queries.py` to implement the matching SQL lookup.

### 2. Add a New Management Source
1. Open `enums.py`.
2. Add the source system to `ManagementSource`.
3. Open `protocol_discovery.py`.
4. Update `normalize_management_source` to canonicalize the input name, and set default target values in `get_mcp_tool_target`.
5. Open `power_ops.py`.
6. Implement a handler class (e.g. `NewVendorHandler`) with an `.execute()` method, and register it inside `ExecutionOrchestrator.__init__()`.

### 3. Add a New Cache Key Type
1. Open `cache.py`.
2. Add a key-builder function to `ResourceCache`:
   ```python
   @staticmethod
   def custom_key(identifier: str) -> str:
       return f"resolver:custom:{identifier.lower()}"
   ```
3. Update `ResourceCache.put_device` and `ResourceCache.get_by_identifier` to write and retrieve keys using this new format.

### 4. Add a New Database Field
1. Open `db_schema.sql`.
2. Add the column definition to the `devices` table:
   ```sql
   ALTER TABLE devices ADD COLUMN custom_metadata VARCHAR(255);
   ```
3. Open `records.py`.
4. Update `DeviceRecord` properties, `from_row()`, and `to_dict()` to serialize the new field.
5. Update `DeviceQueries.upsert` and related queries in `db_queries.py` to read and write the new column.

### 5. Add a New Route Mapping
1. Add the endpoint definition block to the source prompt files (`oneview_api_prompts.txt` or `comops_api_prompts.txt`).
   * *Example block*:
     ```text
     Action Key : CustomAction
     Method     : POST
     API Path   : /rest/server-hardware/{id}/custom-endpoint
     ==========================================
     ```
2. Re-run `python seed_endpoint_registry.py` to parse and import the new route mapping.

---

# Developer Mental Model

If you only remember five things about the Resource Resolver, remember these:

1. **Pure Routing Subsystem**: The resolver maps identifier queries to target hosts and endpoints. It does not execute actions, handle authentication, or connect to hardware in production.
2. **Double Caching Model**: Sub-millisecond lookups are served via Redis/Memurai (hot-path). If a lookup misses, it queries PostgreSQL (cold-path) and updates the cache.
3. **Database-Driven Endpoint Mappings**: All API endpoints and URL patterns are stored in the `endpoint_registry` database table. The resolver has no hardcoded if/elif conditional routing trees.
4. **Deterministic Token Isolation**: The `QueryAgent` parses query strings deterministically using regex. It does not make database, cache, or network calls.
5. **Periodic background polling**: The `PollingEngine` daemon thread runs concurrent updates to keep PostgreSQL and Redis synced with remote inventories.
