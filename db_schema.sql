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
