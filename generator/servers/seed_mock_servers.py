#!/usr/bin/env python3
"""
Seed Mock Servers Script (Separate Databases, 100% Deterministic)
==================================================================
Generates mock devices and seeds them directly into each mock server's
individual SQLite database. Also removes custom-servers details.
"""

from __future__ import annotations

import json
import logging
import os
import sys
import uuid as _uuid

# Set up paths and logger
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, THIS_DIR)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(name)s: %(message)s",
)
logger = logging.getLogger("seed_mock_servers")

from db_store import get_db_store


def generate_mock_devices_data(count_per_source: int = 200) -> list[dict]:
    """Generate mock provider devices data deterministically."""
    server_types = ["server", "blade_server", "rack_server", "compute_node", "hypervisor"]
    server_prefixes = ["dl360-prod", "dl380-prod", "synergy-comp", "apollo-node", "esx-host"]

    storage_types = ["storage_system", "storage_pool", "volume", "volume_set", "filesystem", "host", "host_group", "snapshot", "replication_group"]
    storage_prefixes = ["alletra-array", "nimble-prod", "primera-san", "3par-array", "storeonce-backup", "nas-prod", "san-host"]

    network_types = ["switch", "router", "firewall", "gateway", "wireless_controller", "access_point", "vlan", "port_channel"]
    network_prefixes = ["aruba-cx", "core-sw", "edge-router", "wireless-ctrl", "net-gateway", "ap-floor", "vlan-cfg", "port-channel-cfg"]

    cloud_types = ["virtual_machine", "kubernetes_cluster", "database_service", "storage_service", "virtual_network", "subnet", "load_balancer", "namespace"]
    cloud_prefixes = ["gl-vm", "gl-k8s", "gl-db", "gl-storage", "gl-vnet", "gl-subnet", "gl-lb", "gl-ns"]

    devices = []
    
    # Constant timestamp for 100% identical data
    fixed_time = "2026-06-18 09:00:00+05:30"

    # Helper function to generate deterministic namespace UUIDs
    def make_uuid(seed_name: str) -> str:
        return str(_uuid.uuid5(_uuid.NAMESPACE_DNS, seed_name))

    # 1. mock_server
    for i in range(count_per_source):
        dev_type = server_types[i % len(server_types)]
        prefix = server_prefixes[i % len(server_prefixes)]
        serial = f"{prefix}-{i+1:03d}"
        ip = f"10.11.{(i // 250) + 1}.{(i % 250) + 1}"
        fqdn = f"{serial}.server.local"
        host = "mock-server-manager.local"
        devices.append({
            "id": make_uuid(f"pk-{serial}"),
            "serial_number": serial,
            "ip_address": ip,
            "fqdn": fqdn,
            "management_source": "mock_server",
            "source_host": host,
            "source_device_id": make_uuid(f"source-{serial}"),
            "device_type": dev_type,
            "last_seen": fixed_time,
            "created_at": fixed_time,
            "updated_at": fixed_time
        })

    # 2. mock_storage
    for i in range(count_per_source):
        dev_type = storage_types[i % len(storage_types)]
        prefix = storage_prefixes[i % len(storage_prefixes)]
        serial = f"{prefix}-{i+1:03d}"
        ip = f"10.12.{(i // 250) + 1}.{(i % 250) + 1}"
        fqdn = f"{serial}.storage.local"
        host = "mock-storage-manager.local"
        devices.append({
            "id": make_uuid(f"pk-{serial}"),
            "serial_number": serial,
            "ip_address": ip,
            "fqdn": fqdn,
            "management_source": "mock_storage",
            "source_host": host,
            "source_device_id": make_uuid(f"source-{serial}"),
            "device_type": dev_type,
            "last_seen": fixed_time,
            "created_at": fixed_time,
            "updated_at": fixed_time
        })

    # 3. mock_network
    for i in range(count_per_source):
        dev_type = network_types[i % len(network_types)]
        prefix = network_prefixes[i % len(network_prefixes)]
        serial = f"{prefix}-{i+1:03d}"
        ip = f"10.13.{(i // 250) + 1}.{(i % 250) + 1}"
        fqdn = f"{serial}.network.local"
        host = "mock-network-manager.local"
        devices.append({
            "id": make_uuid(f"pk-{serial}"),
            "serial_number": serial,
            "ip_address": ip,
            "fqdn": fqdn,
            "management_source": "mock_network",
            "source_host": host,
            "source_device_id": make_uuid(f"source-{serial}"),
            "device_type": dev_type,
            "last_seen": fixed_time,
            "created_at": fixed_time,
            "updated_at": fixed_time
        })

    # 4. mock_cloud
    for i in range(count_per_source):
        dev_type = cloud_types[i % len(cloud_types)]
        prefix = cloud_prefixes[i % len(cloud_prefixes)]
        serial = f"{prefix}-{i+1:03d}"
        ip = f"10.14.{(i // 250) + 1}.{(i % 250) + 1}"
        fqdn = f"{serial}.cloud.local"
        host = "mock-cloud-manager.local"
        devices.append({
            "id": make_uuid(f"pk-{serial}"),
            "serial_number": serial,
            "ip_address": ip,
            "fqdn": fqdn,
            "management_source": "mock_cloud",
            "source_host": host,
            "source_device_id": make_uuid(f"source-{serial}"),
            "device_type": dev_type,
            "last_seen": fixed_time,
            "created_at": fixed_time,
            "updated_at": fixed_time
        })

    return devices


def main():
    logger.info("Generating deterministic mock device records...")
    devices = generate_mock_devices_data(count_per_source=200)

    # Server mappings and collection paths
    server_folders = ["Cloud", "compute_ops", "Storage", "oneview", "network"]
    collections = {
        "mock_server": ("/compute-ops-mgmt/v1/devices", "compute_ops"),
        "mock_storage": ("/data-services/v1beta1/devices", "Storage"),
        "mock_network": ("/network/v1/devices", "network"),
        "mock_cloud": ("/api/v1/devices", "Cloud")
    }

    # Initialize / clean dynamic stores for all 5 servers
    dbs = {}
    for srv in server_folders:
        srv_dir = os.path.join(THIS_DIR, srv)
        mock_file = os.path.join(srv_dir, "mock_data.json")
        db = get_db_store(srv, mock_file)
        
        # Ensure dynamic_store structure is set
        db.setdefault("dynamic_store", {})
        
        # Clear device collection paths if they belong to this server
        for src, (col_path, target_srv) in collections.items():
            if target_srv == srv:
                db["dynamic_store"][col_path] = {}
                logger.info(f"Cleared collection path {col_path} in {srv} database.")
        
        # Explicitly remove custom-servers from databases
        deleted_custom = False
        for old_col in ["/compute-ops-mgmt/v1/custom-servers", "/rest/custom-servers"]:
            if old_col in db["dynamic_store"]:
                db["dynamic_store"].pop(old_col, None)
                logger.info(f"Removed custom-servers collection {old_col} from {srv} database.")
                deleted_custom = True
                
        dbs[srv] = db

    # Seed the devices into their respective databases
    for dev in devices:
        src = dev["management_source"]
        col_path, srv = collections[src]
        db = dbs[srv]
        
        item_id = dev["id"]
        db["dynamic_store"][col_path][item_id] = dev

    # Save and export database changes to SQLite files and mock_data.json files
    logger.info("Persisting databases and exporting to local mock_data.json files...")
    for srv in server_folders:
        db = dbs[srv]
        db.persist()
        
        # Write merged SQLite state back to mock_data.json
        srv_dir = os.path.join(THIS_DIR, srv)
        mock_file = os.path.join(srv_dir, "mock_data.json")
        
        # Make sure custom-servers is also popped from the static json files
        with open(mock_file, "r", encoding="utf-8") as f:
            try:
                js_data = json.load(f)
            except Exception:
                js_data = {}
        
        # Remove custom-servers from the root of mock_data.json as well if present
        for key in ["get_compute_ops_mgmt_v1_custom_servers", "get_compute_ops_mgmt_v1_custom_servers_id", "get_rest_custom_servers", "get_rest_custom_servers_id"]:
            js_data.pop(key, None)
            
        if "dynamic_store" in js_data:
            js_data["dynamic_store"].pop("/compute-ops-mgmt/v1/custom-servers", None)
            js_data["dynamic_store"].pop("/rest/custom-servers", None)
            
        # Merge DB state
        merged = {**js_data, **db._data}
        
        with open(mock_file, "w", encoding="utf-8") as f:
            json.dump(merged, f, indent=2)
            
        logger.info(f"✓ Seeded and exported data for {srv} mock server.")

    logger.info("Mock servers seeding and export successfully completed!")


if __name__ == "__main__":
    main()
