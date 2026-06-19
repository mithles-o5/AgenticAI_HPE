-- Resource Resolver Database Schema
-- ====================================
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS devices (
	id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
	serial_number VARCHAR(64) UNIQUE NOT NULL,
	ip_address INET,
	fqdn VARCHAR(255),
	management_source VARCHAR(32) NOT NULL,
	source_host VARCHAR(255),
	source_device_id VARCHAR(128),
	device_type VARCHAR(64),
	last_seen TIMESTAMPTZ DEFAULT NOW(),
	created_at TIMESTAMPTZ DEFAULT NOW(),
	updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_devices_ip ON devices(ip_address);
CREATE INDEX IF NOT EXISTS idx_devices_fqdn ON devices(fqdn);
CREATE INDEX IF NOT EXISTS idx_devices_source ON devices(management_source, source_host);

CREATE TABLE IF NOT EXISTS routing_audit (
	id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
	identifier VARCHAR(255) NOT NULL,
	identifier_type VARCHAR(16) NOT NULL,
	resolved_source VARCHAR(32),
	resolved_host VARCHAR(255),
	cache_hit BOOLEAN NOT NULL,
	resolution_ms INTEGER,
	requested_by VARCHAR(128),
	timestamp TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS poll_history (
	id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
	source_type VARCHAR(32) NOT NULL,
	source_host VARCHAR(255) NOT NULL,
	devices_found INTEGER,
	devices_added INTEGER,
	devices_removed INTEGER,
	duration_ms INTEGER,
	status VARCHAR(16),
	error_message TEXT,
	timestamp TIMESTAMPTZ DEFAULT NOW()
);

-- Used for faster retrieval of recently used devices and logs
CREATE INDEX IF NOT EXISTS idx_poll_history_timestamp on poll_history(timestamp);

-- ---------------------------------------------------------------------------
-- Poll Snapshots — persistent baseline for reconciliation diffs
-- ---------------------------------------------------------------------------
-- Stores the last successfully polled set of serial numbers per
-- (source_type, source_host). Used as the comparison baseline for computing
-- devices_added / devices_removed across restarts, deployments, and crashes.
--
-- serial_numbers : JSON array of serial number strings from the last poll
-- snapshot_at    : wall-clock timestamp of when this snapshot was captured
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS poll_snapshots (
    id            UUID         PRIMARY KEY DEFAULT gen_random_uuid(),
    source_type   VARCHAR(32)  NOT NULL,
    source_host   VARCHAR(255) NOT NULL,
    serial_numbers JSONB       NOT NULL DEFAULT '[]',
    snapshot_at   TIMESTAMPTZ  DEFAULT NOW(),
    UNIQUE (source_type, source_host)
);

CREATE INDEX IF NOT EXISTS idx_poll_snapshots_source
    ON poll_snapshots (lower(source_type), lower(source_host));

-- ---------------------------------------------------------------------------
-- Endpoint Registry — vendor-agnostic, DB-driven API endpoint catalogue
-- ---------------------------------------------------------------------------
-- Seeded from oneview_api_prompts.txt and comops_api_prompts.txt via
-- seed_endpoint_registry.py. Replaces hardcoded if/elif endpoint trees.
--
-- device_type  : inferred from api_path resource segment ("server", "storage"…)
-- action_key   : short semantic key ("On", "Status") or verbose API key
-- api_path     : EXACT vendor API path — no generic {resource_category} allowed
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS endpoint_registry (
    id          UUID         PRIMARY KEY DEFAULT gen_random_uuid(),
    vendor      VARCHAR(64)  NOT NULL,
    device_type VARCHAR(64)  NOT NULL DEFAULT 'generic',
    action_key  VARCHAR(128) NOT NULL,
    http_method VARCHAR(16)  NOT NULL,
    api_path    TEXT         NOT NULL,
    created_at  TIMESTAMPTZ  DEFAULT NOW(),
    UNIQUE (vendor, device_type, action_key, api_path, http_method)
);

-- Covers the primary lookup pattern: vendor + device_type + action_key
CREATE INDEX IF NOT EXISTS idx_endpoint_registry_lookup
    ON endpoint_registry (lower(vendor), lower(device_type), lower(action_key));

