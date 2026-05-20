-- Resource Resolver Database Schema
-- ====================================
-- Stores 10 OneViews with 1000 servers each + CoM with 500 servers

CREATE TABLE IF NOT EXISTS vendors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS deployment_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS protocols (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS resource_health (
    id SERIAL PRIMARY KEY,
    status VARCHAR(50) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS oneviews (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    uuid VARCHAR(36) UNIQUE NOT NULL,
    ip_address INET NOT NULL,
    management_host VARCHAR(255),
    owner VARCHAR(255),
    location VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS servers (
    id SERIAL PRIMARY KEY,
    uuid VARCHAR(36) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    ip_address INET NOT NULL,
    management_host VARCHAR(255),
    
    -- Relationships
    vendor_id INTEGER REFERENCES vendors(id),
    deployment_type_id INTEGER REFERENCES deployment_types(id),
    health_id INTEGER REFERENCES resource_health(id),
    oneview_id INTEGER REFERENCES oneviews(id),
    
    -- Hardware metadata
    model VARCHAR(255),
    serial VARCHAR(255),
    firmware VARCHAR(255),
    enclosure VARCHAR(255),
    bay INTEGER,
    location VARCHAR(255),
    asset_tag VARCHAR(255),
    owner VARCHAR(255),
    
    -- Live state
    power_state VARCHAR(50) DEFAULT 'Unknown',
    
    -- Vault credentials
    vault_path VARCHAR(500),
    auth_type VARCHAR(50) DEFAULT 'basic',
    vault_username VARCHAR(255),
    
    -- Metadata
    etag VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS server_protocols (
    id SERIAL PRIMARY KEY,
    server_id INTEGER NOT NULL REFERENCES servers(id) ON DELETE CASCADE,
    protocol_id INTEGER NOT NULL REFERENCES protocols(id) ON DELETE CASCADE,
    UNIQUE(server_id, protocol_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS server_aliases (
    id SERIAL PRIMARY KEY,
    server_id INTEGER NOT NULL REFERENCES servers(id) ON DELETE CASCADE,
    alias VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS server_tags (
    id SERIAL PRIMARY KEY,
    server_id INTEGER NOT NULL REFERENCES servers(id) ON DELETE CASCADE,
    tag VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS coms (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    uuid VARCHAR(36) UNIQUE NOT NULL,
    ip_address INET NOT NULL,
    management_host VARCHAR(255),
    owner VARCHAR(255),
    location VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS com_servers (
    id SERIAL PRIMARY KEY,
    uuid VARCHAR(36) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    ip_address INET NOT NULL,
    management_host VARCHAR(255),
    
    -- Relationships
    vendor_id INTEGER REFERENCES vendors(id),
    deployment_type_id INTEGER REFERENCES deployment_types(id),
    health_id INTEGER REFERENCES resource_health(id),
    com_id INTEGER REFERENCES coms(id),
    
    -- Hardware metadata
    model VARCHAR(255),
    serial VARCHAR(255),
    firmware VARCHAR(255),
    enclosure VARCHAR(255),
    bay INTEGER,
    location VARCHAR(255),
    asset_tag VARCHAR(255),
    owner VARCHAR(255),
    
    -- Live state
    power_state VARCHAR(50) DEFAULT 'Unknown',
    
    -- Vault credentials
    vault_path VARCHAR(500),
    auth_type VARCHAR(50) DEFAULT 'basic',
    vault_username VARCHAR(255),
    
    -- Metadata
    etag VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS com_server_protocols (
    id SERIAL PRIMARY KEY,
    com_server_id INTEGER NOT NULL REFERENCES com_servers(id) ON DELETE CASCADE,
    protocol_id INTEGER NOT NULL REFERENCES protocols(id) ON DELETE CASCADE,
    UNIQUE(com_server_id, protocol_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS com_server_aliases (
    id SERIAL PRIMARY KEY,
    com_server_id INTEGER NOT NULL REFERENCES com_servers(id) ON DELETE CASCADE,
    alias VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS com_server_tags (
    id SERIAL PRIMARY KEY,
    com_server_id INTEGER NOT NULL REFERENCES com_servers(id) ON DELETE CASCADE,
    tag VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_servers_uuid ON servers(uuid);
CREATE INDEX IF NOT EXISTS idx_servers_name ON servers(name);
CREATE INDEX IF NOT EXISTS idx_servers_ip ON servers(ip_address);
CREATE INDEX IF NOT EXISTS idx_servers_oneview_id ON servers(oneview_id);
CREATE INDEX IF NOT EXISTS idx_server_aliases_alias ON server_aliases(alias);
CREATE INDEX IF NOT EXISTS idx_server_tags_tag ON server_tags(tag);

CREATE INDEX IF NOT EXISTS idx_com_servers_uuid ON com_servers(uuid);
CREATE INDEX IF NOT EXISTS idx_com_servers_name ON com_servers(name);
CREATE INDEX IF NOT EXISTS idx_com_servers_ip ON com_servers(ip_address);
CREATE INDEX IF NOT EXISTS idx_com_servers_com_id ON com_servers(com_id);
CREATE INDEX IF NOT EXISTS idx_com_server_aliases_alias ON com_server_aliases(alias);
CREATE INDEX IF NOT EXISTS idx_com_server_tags_tag ON com_server_tags(tag);

CREATE INDEX IF NOT EXISTS idx_oneviews_uuid ON oneviews(uuid);
CREATE INDEX IF NOT EXISTS idx_coms_uuid ON coms(uuid);
