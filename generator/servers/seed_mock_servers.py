#!/usr/bin/env python3
"""
Seed Mock Servers Script (Separate Databases, 100% Deterministic)
==================================================================
Generates mock devices and seeds them directly into each mock server's
individual SQLite database.
"""

from __future__ import annotations

import json
import logging
import os
import sys
import uuid as _uuid
import random

# Set up paths and logger
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, THIS_DIR)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(name)s: %(message)s",
)
logger = logging.getLogger("seed_mock_servers")

import db_store
from db_store import get_db_store


# ─────────────────────────────────────────────────────────────────────────────
# Feature Generation Helper
# ─────────────────────────────────────────────────────────────────────────────

def generate_device_features(management_source: str, device_type: str) -> dict:
    """Generate realistic default/simulated features based on source and type."""
    # Default fallback values (Ensuring NO 0 values where possible)
    temp = round(random.uniform(20.0, 28.0), 1)
    storage = random.choice([250, 500, 1000])
    free_storage = int(storage * random.uniform(0.5, 0.9))
    mem = random.choice([8, 16, 32])
    cores = random.choice([4, 8, 16])
    health = "OK"
    power = "ON"
    
    # Non-zero default VM/Compute metrics for all devices (simulating virtualization/mgmt capacity)
    active_vms = random.randint(2, 5)
    allocated_vcpu = active_vms * random.choice([2, 4])
    allocated_ram_gb = active_vms * random.choice([4, 8])
    
    # 1. Server/Compute Ops specific features (High-tier servers)
    if management_source in ["mock_server", "coms"]:
        temp = round(random.uniform(20.0, 45.0), 1)
        storage = random.choice([1000, 2000, 4000, 8000])
        free_storage = int(storage * random.uniform(0.15, 0.85))
        mem = random.choice([128, 256, 512, 1024])
        cores = random.choice([32, 64, 128])
        health = random.choices(["OK", "WARNING", "CRITICAL"], weights=[0.90, 0.07, 0.03])[0]
        power = random.choices(["ON", "OFF"], weights=[0.95, 0.05])[0]
        active_vms = random.randint(5, 15)
        allocated_vcpu = active_vms * random.choice([2, 4])
        allocated_ram_gb = active_vms * random.choice([8, 16])
        
    # 2. OneView specific features
    elif management_source == "oneview":
        if device_type == "server":
            temp = round(random.uniform(22.0, 42.0), 1)
            storage = random.choice([1000, 2000, 4000])
            free_storage = int(storage * random.uniform(0.2, 0.8))
            mem = random.choice([64, 128, 256, 512])
            cores = random.choice([16, 32, 64])
            health = random.choices(["OK", "WARNING", "CRITICAL"], weights=[0.88, 0.09, 0.03])[0]
            power = random.choices(["ON", "OFF"], weights=[0.94, 0.06])[0]
            active_vms = random.randint(4, 10)
            allocated_vcpu = active_vms * random.choice([2, 4])
            allocated_ram_gb = active_vms * random.choice([8, 16])
        elif device_type == "storage":
            storage = random.choice([10000, 20000, 50000])
            free_storage = int(storage * random.uniform(0.2, 0.8))
            health = random.choices(["OK", "WARNING", "CRITICAL"], weights=[0.90, 0.08, 0.02])[0]
        elif device_type in ["switch", "router", "firewall"]:
            temp = round(random.uniform(25.0, 50.0), 1)
            health = random.choices(["OK", "WARNING", "CRITICAL"], weights=[0.91, 0.07, 0.02])[0]
            power = "ON"
            
    # 3. Storage specific features
    elif management_source == "mock_storage":
        if device_type == "storage_system":
            temp = round(random.uniform(25.0, 38.0), 1)
            power = random.choices(["ON", "OFF"], weights=[0.95, 0.05])[0]
            
        if device_type in ["storage_system", "storage_pool", "volume", "volume_set", "filesystem"]:
            storage = random.choice([5000, 10000, 50000, 100000])
            free_storage = int(storage * random.uniform(0.2, 0.8))
            
        health = random.choices(["OK", "WARNING", "CRITICAL"], weights=[0.92, 0.06, 0.02])[0]
        
    # 4. Network specific features
    elif management_source == "mock_network":
        physical_net = ["switch", "router", "firewall", "gateway", "wireless_controller", "access_point"]
        if device_type in physical_net:
            temp = round(random.uniform(28.0, 52.0), 1)
            power = random.choices(["ON", "OFF"], weights=[0.96, 0.04])[0]
            
        health = random.choices(["OK", "WARNING", "CRITICAL"], weights=[0.93, 0.05, 0.02])[0]
        
    # 5. Cloud specific features
    elif management_source == "mock_cloud":
        cloud_compute = ["virtual_machine", "kubernetes_cluster", "database_service", "storage_service"]
        if device_type in cloud_compute:
            cores = random.choice([4, 8, 16, 32])
            mem = random.choice([8, 16, 32, 64, 128])
            storage = random.choice([250, 500, 1000, 2000])
            free_storage = int(storage * random.uniform(0.2, 0.8))
            
        if device_type in ["virtual_machine", "kubernetes_cluster"]:
            active_vms = random.randint(3, 8)
            allocated_vcpu = active_vms * random.choice([2, 4])
            allocated_ram_gb = active_vms * random.choice([4, 8])
            
        health = random.choices(["OK", "WARNING", "CRITICAL"], weights=[0.94, 0.04, 0.02])[0]
        
    # Generate ports config
    ports = {}
    if device_type in ["switch", "router", "firewall", "gateway"]:
        port_count = 24 if device_type == "switch" else 8
        for p_idx in range(1, port_count + 1):
            status = "UP" if p_idx % 3 != 0 else "DOWN"
            ports[f"GigabitEthernet1/0/{p_idx}"] = status
    else:
        ports = {"eth0": "UP", "eth1": "DOWN"}
        
    # Generate VLANs config
    configured_vlans = [
        {"vlan_id": 1, "name": "Management"},
        {"vlan_id": 10, "name": "Data-VLAN"},
        {"vlan_id": 100, "name": "Vlan100"}
    ]
        
    return {
        "temperature_celsius": temp,
        "storage_capacity_gb": storage,
        "free_storage_gb": free_storage,
        "memory_gb": mem,
        "cpu_cores": cores,
        "health_status": health,
        "power_state": power,
        "active_vms": active_vms,
        "allocated_vcpu": allocated_vcpu,
        "allocated_ram_gb": allocated_ram_gb,
        "ports": ports,
        "configured_vlans": configured_vlans
    }


def get_enterprise_name(device_type: str, index: int, parent_type: str) -> tuple[str, str]:
    """Generate a unique, realistic enterprise infrastructure name."""
    domain = "datacenter.local" if parent_type == "oneview" else "cloud.local"
    t = (device_type or "server").lower()
    
    if t == "server":
        rack = (index % 50) + 1
        node = (index % 10) + 1
        name = f"rack{rack}-compute-{node}-{index}"
    elif t == "switch":
        sw_type = "leaf" if index % 2 == 0 else "agg"
        num = (index % 20) + 1
        name = f"{sw_type}-sw{num:02d}-{index}"
    elif t == "router":
        r_type = "edge" if index % 2 == 0 else "wan"
        num = (index % 10) + 1
        name = f"{r_type}-r{num:02d}-{index}"
    elif t == "firewall":
        fw_type = "west" if index % 2 == 0 else "east"
        num = (index % 5) + 1
        name = f"fw-{fw_type}-{num:02d}-{index}"
    elif t == "storage":
        stg_type = "array" if index % 2 == 0 else "nas"
        name = f"stg-{stg_type}-{index}"
    else:
        name = f"infra-node-{index}"
        
    return name, f"{name}.{domain}"


def generate_all_devices() -> list[dict]:
    """Generate all devices for seeding."""
    devices = []
    fixed_time = "2026-06-18 09:00:00+05:30"
    
    def make_uuid(seed_name: str) -> str:
        return str(_uuid.uuid5(_uuid.NAMESPACE_DNS, seed_name))
        
    # Set seed for reproducibility
    random.seed(42)

    # 1. 200 Storage devices
    storage_types = ["storage_system", "storage_pool", "volume", "volume_set", "filesystem", "host", "host_group", "snapshot", "replication_group"]
    storage_prefixes = ["alletra-array", "nimble-prod", "primera-san", "3par-array", "storeonce-backup", "nas-prod", "san-host"]
    for i in range(200):
        dev_type = storage_types[i % len(storage_types)]
        prefix = storage_prefixes[i % len(storage_prefixes)]
        serial = f"{prefix}-{i+1:03d}"
        ip = f"10.12.{(i // 250) + 1}.{(i % 250) + 1}"
        fqdn = f"{serial}.storage.local"
        host = "mock-storage-manager.local"
        dev_uuid = make_uuid(f"pk-{serial}")
        features = generate_device_features("mock_storage", dev_type)
        
        dev = {
            "id": dev_uuid,
            "serial_number": serial,
            "ip_address": ip,
            "fqdn": fqdn,
            "management_source": "mock_storage",
            "source_host": host,
            "source_device_id": make_uuid(f"source-{serial}"),
            "device_type": dev_type,
            "last_seen": fixed_time,
            "created_at": fixed_time,
            "updated_at": fixed_time,
            "name": serial,
            "firmware_version": "1.0.0",
            "total_capacity_gb": features["storage_capacity_gb"],
            "free_capacity_gb": features["free_storage_gb"]
        }
        dev.update(features)
        devices.append(dev)

    # 2. 200 Network devices
    network_types = ["switch", "router", "firewall", "gateway", "wireless_controller", "access_point", "vlan", "port_channel"]
    network_prefixes = ["aruba-cx", "core-sw", "edge-router", "wireless-ctrl", "net-gateway", "ap-floor", "vlan-cfg", "port-channel-cfg"]
    for i in range(200):
        dev_type = network_types[i % len(network_types)]
        prefix = network_prefixes[i % len(network_prefixes)]
        serial = f"{prefix}-{i+1:03d}"
        ip = f"10.13.{(i // 250) + 1}.{(i % 250) + 1}"
        fqdn = f"{serial}.network.local"
        host = "mock-network-manager.local"
        dev_uuid = make_uuid(f"pk-{serial}")
        features = generate_device_features("mock_network", dev_type)
        
        dev = {
            "id": dev_uuid,
            "serial_number": serial,
            "ip_address": ip,
            "fqdn": fqdn,
            "management_source": "mock_network",
            "source_host": host,
            "source_device_id": make_uuid(f"source-{serial}"),
            "device_type": dev_type,
            "last_seen": fixed_time,
            "created_at": fixed_time,
            "updated_at": fixed_time,
            "name": serial,
            "firmware_version": "1.0.0",
            "total_capacity_gb": features["storage_capacity_gb"],
            "free_capacity_gb": features["free_storage_gb"]
        }
        dev.update(features)
        devices.append(dev)

    # 3. 200 Cloud devices
    cloud_types = ["virtual_machine", "kubernetes_cluster", "database_service", "storage_service", "virtual_network", "subnet", "load_balancer", "namespace"]
    cloud_prefixes = ["gl-vm", "gl-k8s", "gl-db", "gl-storage", "gl-vnet", "gl-subnet", "gl-lb", "gl-ns"]
    for i in range(200):
        dev_type = cloud_types[i % len(cloud_types)]
        prefix = cloud_prefixes[i % len(cloud_prefixes)]
        serial = f"{prefix}-{i+1:03d}"
        ip = f"10.14.{(i // 250) + 1}.{(i % 250) + 1}"
        fqdn = f"{serial}.cloud.local"
        host = "mock-cloud-manager.local"
        dev_uuid = make_uuid(f"pk-{serial}")
        features = generate_device_features("mock_cloud", dev_type)
        
        dev = {
            "id": dev_uuid,
            "serial_number": serial,
            "ip_address": ip,
            "fqdn": fqdn,
            "management_source": "mock_cloud",
            "source_host": host,
            "source_device_id": make_uuid(f"source-{serial}"),
            "device_type": dev_type,
            "last_seen": fixed_time,
            "created_at": fixed_time,
            "updated_at": fixed_time,
            "name": serial,
            "firmware_version": "1.0.0",
            "total_capacity_gb": features["storage_capacity_gb"],
            "free_capacity_gb": features["free_storage_gb"]
        }
        dev.update(features)
        devices.append(dev)

    # 4. 1000 Compute Ops (coms) devices
    types_coms = ["server", "switch", "router", "firewall", "storage"]
    for i in range(1000):
        device_num = 10000 + i
        device_type = types_coms[device_num % len(types_coms)]
        serial, fqdn = get_enterprise_name(device_type, device_num, "coms")
        ip = f"10.200.1.{(device_num % 254) + 1}"
        host = "coms-01.cloud.local"
        dev_uuid = make_uuid(f"pk-{serial}")
        features = generate_device_features("coms", device_type)
        
        dev = {
            "id": dev_uuid,
            "serial_number": serial,
            "ip_address": ip,
            "fqdn": fqdn,
            "management_source": "coms",
            "source_host": host,
            "source_device_id": make_uuid(f"source-{serial}"),
            "device_type": device_type,
            "last_seen": fixed_time,
            "created_at": fixed_time,
            "updated_at": fixed_time,
            "name": serial,
            "firmware_version": "1.0.0",
            "total_capacity_gb": features["storage_capacity_gb"],
            "free_capacity_gb": features["free_storage_gb"]
        }
        dev.update(features)
        devices.append(dev)

    # 5. 7 Compute Ops testing devices
    coms_testing = [
        ("prod-x1", "10.200.1.13", "prod-x1.cloud.local", "coms", "coms-01.cloud.local", "coms-uuid-prodx1", "server"),
        ("core-r3", "10.200.1.20", "core-r3.cloud.local", "coms", "coms-01.cloud.local", "coms-uuid-corer3", "router"),
        ("agg-sw05", "10.200.1.21", "agg-sw05.cloud.local", "coms", "coms-01.cloud.local", "coms-uuid-aggsw05", "switch"),
        ("fw-west-01", "10.200.1.12", "fw-west-01.cloud.local", "coms", "coms-01.cloud.local", "coms-uuid-fwwest01", "firewall"),
        ("stg-array-02", "10.200.1.11", "stg-array-02.cloud.local", "coms", "coms-01.cloud.local", "coms-uuid-stgarray02", "storage"),
        ("nas-prod-01", "10.200.1.10", "nas-prod-01.cloud.local", "coms", "coms-01.cloud.local", "coms-uuid-np01", "storage"),
        ("backup-san-01", "10.200.1.22", "backup-san-01.cloud.local", "coms", "coms-01.cloud.local", "coms-uuid-backupsan01", "storage"),
    ]
    for serial, ip, fqdn, management_source, source_host, source_device_id, device_type in coms_testing:
        features = generate_device_features("coms", device_type)
        dev = {
            "id": source_device_id,
            "serial_number": serial,
            "ip_address": ip,
            "fqdn": fqdn,
            "management_source": management_source,
            "source_host": source_host,
            "source_device_id": source_device_id,
            "device_type": device_type,
            "last_seen": fixed_time,
            "created_at": fixed_time,
            "updated_at": fixed_time,
            "name": serial,
            "firmware_version": "1.0.0",
            "total_capacity_gb": features["storage_capacity_gb"],
            "free_capacity_gb": features["free_storage_gb"]
        }
        dev.update(features)
        devices.append(dev)

    # 6. 500 OneView devices
    for i in range(500):
        device_num = i
        device_type = types_coms[device_num % len(types_coms)]
        serial, fqdn = get_enterprise_name(device_type, device_num, "oneview")
        ip = f"10.100.1.{(device_num % 254) + 1}"
        host = "oneview-01.mgmt.local"
        dev_uuid = make_uuid(f"pk-ov-{serial}")
        features = generate_device_features("oneview", device_type)
        
        dev = {
            "id": dev_uuid,
            "serial_number": serial,
            "ip_address": ip,
            "fqdn": fqdn,
            "management_source": "oneview",
            "source_host": host,
            "source_device_id": make_uuid(f"source-ov-{serial}"),
            "device_type": device_type,
            "last_seen": fixed_time,
            "created_at": fixed_time,
            "updated_at": fixed_time,
            "name": serial,
            "firmware_version": "1.0.0",
            "total_capacity_gb": features["storage_capacity_gb"],
            "free_capacity_gb": features["free_storage_gb"]
        }
        dev.update(features)
        devices.append(dev)

    # 7. 9 OneView testing devices
    oneview_testing = [
        ("dc1-a7", "10.100.1.10", "dc1-a7.datacenter.local", "oneview", "oneview-01.mgmt.local", "ov-uuid-dc1a7", "server"),
        ("compute-22", "10.100.1.11", "compute-22.datacenter.local", "oneview", "oneview-01.mgmt.local", "ov-uuid-c22", "server"),
        ("rack42-n3", "10.100.1.20", "rack42-n3.datacenter.local", "oneview", "oneview-01.mgmt.local", "ov-uuid-rack42n3", "server"),
        ("edge-r1", "10.100.1.12", "edge-r1.datacenter.local", "oneview", "oneview-01.mgmt.local", "ov-uuid-edger1", "router"),
        ("wan-r2", "10.100.1.21", "wan-r2.datacenter.local", "oneview", "oneview-01.mgmt.local", "ov-uuid-wanr2", "router"),
        ("core-sw01", "10.100.1.13", "core-sw01.datacenter.local", "oneview", "oneview-01.mgmt.local", "ov-uuid-coresw01", "switch"),
        ("leaf-sw12", "10.100.1.22", "leaf-sw12.datacenter.local", "oneview", "oneview-01.mgmt.local", "ov-uuid-leafsw12", "switch"),
        ("fw-core-01", "10.100.1.14", "fw-core-01.datacenter.local", "oneview", "oneview-01.mgmt.local", "ov-uuid-fc01", "firewall"),
        ("fw-edge-02", "10.100.1.23", "fw-edge-02.datacenter.local", "oneview", "oneview-01.mgmt.local", "ov-uuid-fwedge02", "firewall"),
    ]
    for serial, ip, fqdn, management_source, source_host, source_device_id, device_type in oneview_testing:
        features = generate_device_features("oneview", device_type)
        dev = {
            "id": source_device_id,
            "serial_number": serial,
            "ip_address": ip,
            "fqdn": fqdn,
            "management_source": management_source,
            "source_host": source_host,
            "source_device_id": source_device_id,
            "device_type": device_type,
            "last_seen": fixed_time,
            "created_at": fixed_time,
            "updated_at": fixed_time,
            "name": serial,
            "firmware_version": "1.0.0",
            "total_capacity_gb": features["storage_capacity_gb"],
            "free_capacity_gb": features["free_storage_gb"]
        }
        dev.update(features)
        devices.append(dev)

    return devices


def main():
    logger.info("Closing any open SQLite connections and deleting old database files...")
    # Close existing connections to allow deletion
    for name, db in list(db_store._db_store_cache.items()):
        try:
            db._conn.close()
        except Exception:
            pass
    db_store._db_store_cache.clear()

    # Server mappings and collection paths
    server_folders = ["Cloud", "compute_ops", "Storage", "oneview", "network"]
    collections = {
        "coms": ("/compute-ops-mgmt/v1/devices", "compute_ops"),
        "oneview": ("/rest/server-hardware", "oneview"),
        "mock_storage": ("/data-services/v1beta1/devices", "Storage"),
        "mock_network": ("/network/v1/devices", "network"),
        "mock_cloud": ("/api/v1/devices", "Cloud")
    }

    # Delete existing SQLite files to start fresh
    for srv in server_folders:
        srv_dir = os.path.join(THIS_DIR, srv)
        sqlite_file = os.path.join(srv_dir, f"{srv.lower()}_db.sqlite")
        if os.path.exists(sqlite_file):
            try:
                os.remove(sqlite_file)
                logger.info(f"Deleted old SQLite database: {sqlite_file}")
            except Exception as e:
                logger.warning(f"Could not delete SQLite file {sqlite_file}: {e}")

        # Clear target collections in dynamic_store within mock_data.json
        mock_file = os.path.join(srv_dir, "mock_data.json")
        if os.path.exists(mock_file):
            try:
                with open(mock_file, "r", encoding="utf-8") as f:
                    js_data = json.load(f)
            except Exception:
                js_data = {}
            
            if "dynamic_store" in js_data:
                for src, (col_path, target_srv) in collections.items():
                    if target_srv == srv:
                        js_data["dynamic_store"].pop(col_path, None)
            
            with open(mock_file, "w", encoding="utf-8") as f:
                json.dump(js_data, f, indent=2)
                logger.info(f"Cleaned dynamic_store collection paths in: {mock_file}")

    logger.info("Generating deterministic mock device records...")
    devices = generate_all_devices()

    # Re-initialize dynamic stores for all 5 servers
    dbs = {}
    for srv in server_folders:
        srv_dir = os.path.join(THIS_DIR, srv)
        mock_file = os.path.join(srv_dir, "mock_data.json")
        db = get_db_store(srv, mock_file)
        
        # Ensure dynamic_store structure is set
        db.setdefault("dynamic_store", {})
        
        # Clear device collection paths if they belong to this server (to be absolutely sure)
        for src, (col_path, target_srv) in collections.items():
            if target_srv == srv:
                db["dynamic_store"][col_path] = {}
                logger.info(f"Cleared collection path {col_path} in {srv} database.")
        
        # Explicitly remove custom-servers from databases
        for old_col in ["/compute-ops-mgmt/v1/custom-servers", "/rest/custom-servers"]:
            if old_col in db["dynamic_store"]:
                db["dynamic_store"].pop(old_col, None)
                logger.info(f"Removed custom-servers collection {old_col} from {srv} database.")
                
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
