import sys
import os
import json

sys.path.insert(0, os.path.abspath('mcp_server'))
sys.path.insert(0, os.path.abspath('resource_resolver'))
from sample_data import load_sample_registry
from records import Protocol

def main():
    registry = load_sample_registry()
    records = registry.all_records()
    
    ov_servers = {}
    com_servers = {}
    
    for r in records:
        if Protocol.ONEVIEW in r.supported_protocols:
            ov_servers[r.uuid] = {
                "uuid": r.uuid,
                "name": r.name,
                "model": r.model,
                "ip_address": r.ip_address,
                "powerState": r.power_state,
                "health": r.health.value,
                "location": r.location
            }
        if Protocol.COMS in r.supported_protocols:
            com_servers[r.uuid] = {
                "uuid": r.uuid,
                "name": r.name,
                "model": r.model,
                "ip_address": r.ip_address,
                "powerState": r.power_state,
                "health": r.health.value,
                "location": r.location
            }

    # Update OneView mock db
    ov_db_path = os.path.join("mock_server(oneview)", "mock_data.json")
    with open(ov_db_path, "r", encoding="utf-8") as f:
        ov_db = json.load(f)
    ov_db["server_hardware"] = ov_servers
    with open(ov_db_path, "w", encoding="utf-8") as f:
        json.dump(ov_db, f, indent=4)
        
    # Update ComOps mock db
    com_db_path = os.path.join("mock_server(Comops)", "mock_data.json")
    with open(com_db_path, "r", encoding="utf-8") as f:
        com_db = json.load(f)
    com_db["servers"] = com_servers
    with open(com_db_path, "w", encoding="utf-8") as f:
        json.dump(com_db, f, indent=4)

    print(f"✅ Successfully injected {len(ov_servers)} OneView servers and {len(com_servers)} ComOps servers into mock_data.json files.")

if __name__ == "__main__":
    main()
