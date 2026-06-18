#!/usr/bin/env python3
"""
Generate Features CSV Script
===========================
Generates deterministic features for the 800 mock devices and writes them to a CSV file.
Ensures that all columns are fully populated for every device with default simulated values.
"""

import os
import sys
import csv
import random

# Path setup to import from current directory
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, THIS_DIR)

from seed_mock_servers import generate_mock_devices_data

CSV_FILE = os.path.join(THIS_DIR, "device_features_seed.csv")

def main():
    # Set seed for 100% deterministic results
    random.seed(42)
    
    print("Generating deterministic features for all 800 mock devices...")
    devices = generate_mock_devices_data(count_per_source=200)
    
    headers = [
        "device_id",
        "serial_number",
        "management_source",
        "device_type",
        "temperature_celsius",
        "storage_capacity_gb",
        "free_storage_gb",
        "memory_gb",
        "cpu_cores",
        "health_status",
        "power_state",
        "active_vms",
        "allocated_vcpu",
        "allocated_ram_gb"
    ]
    
    rows = []
    
    for dev in devices:
        dev_id = dev["id"]
        serial = dev["serial_number"]
        src = dev["management_source"]
        dtype = dev["device_type"]
        
        # Initialize default simulated fallback values (No empty/null columns)
        temp = round(random.uniform(20.0, 28.0), 1)
        storage = random.choice([100, 250, 500, 1000])
        free_storage = int(storage * random.uniform(0.5, 0.9))
        mem = random.choice([4, 8, 16, 32])
        cores = random.choice([2, 4, 8])
        health = "OK"
        power = "ON"
        active_vms = 0
        allocated_vcpu = 0
        allocated_ram_gb = 0
        
        # 1. Server/Compute Ops specific features (High-tier servers)
        if src == "mock_server":
            temp = round(random.uniform(20.0, 45.0), 1)
            storage = random.choice([500, 1000, 2000, 4000, 8000, 16000])
            free_storage = int(storage * random.uniform(0.1, 0.9))
            mem = random.choice([64, 128, 256, 512, 1024])
            cores = random.choice([16, 32, 64, 128])
            health = random.choices(["OK", "WARNING", "CRITICAL"], weights=[0.90, 0.07, 0.03])[0]
            power = random.choices(["ON", "OFF"], weights=[0.95, 0.05])[0]
            
        # 2. Storage specific features
        elif src == "mock_storage":
            if dtype == "storage_system":
                temp = round(random.uniform(25.0, 38.0), 1)
                power = random.choices(["ON", "OFF"], weights=[0.95, 0.05])[0]
                
            if dtype in ["storage_system", "storage_pool", "volume", "volume_set", "filesystem"]:
                storage = random.choice([1000, 2000, 5000, 10000, 50000, 100000])
                free_storage = int(storage * random.uniform(0.1, 0.9))
                
            health = random.choices(["OK", "WARNING", "CRITICAL"], weights=[0.92, 0.06, 0.02])[0]
            
        # 3. Network specific features
        elif src == "mock_network":
            physical_net = ["switch", "router", "firewall", "gateway", "wireless_controller", "access_point"]
            if dtype in physical_net:
                temp = round(random.uniform(28.0, 52.0), 1)
                power = random.choices(["ON", "OFF"], weights=[0.96, 0.04])[0]
                
            health = random.choices(["OK", "WARNING", "CRITICAL"], weights=[0.93, 0.05, 0.02])[0]
            
        # 4. Cloud specific features
        elif src == "mock_cloud":
            cloud_compute = ["virtual_machine", "kubernetes_cluster", "database_service", "storage_service"]
            if dtype in cloud_compute:
                cores = random.choice([2, 4, 8, 16, 32])
                mem = random.choice([4, 8, 16, 32, 64, 128])
                storage = random.choice([50, 100, 250, 500, 1000, 2000])
                free_storage = int(storage * random.uniform(0.1, 0.9))
                
            if dtype in ["virtual_machine", "kubernetes_cluster"]:
                active_vms = random.randint(1, 5)
                allocated_vcpu = active_vms * random.choice([1, 2, 4])
                allocated_ram_gb = active_vms * random.choice([2, 4, 8])
                
            health = random.choices(["OK", "WARNING", "CRITICAL"], weights=[0.94, 0.04, 0.02])[0]
            
        rows.append({
            "device_id": dev_id,
            "serial_number": serial,
            "management_source": src,
            "device_type": dtype,
            "temperature_celsius": temp,
            "storage_capacity_gb": storage,
            "free_storage_gb": free_storage,
            "memory_gb": mem,
            "cpu_cores": cores,
            "health_status": health,
            "power_state": power,
            "active_vms": active_vms,
            "allocated_vcpu": allocated_vcpu,
            "allocated_ram_gb": allocated_ram_gb
        })
        
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)
        
    print(f"Successfully generated features for {len(rows)} devices at: {CSV_FILE}")

if __name__ == "__main__":
    main()
