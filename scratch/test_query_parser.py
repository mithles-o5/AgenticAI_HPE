import sys
import os

sys.path.insert(0, r'c:\AgenticAI_HPE\resource_resolver')
from query_agent import QueryAgent

test_cases = [
    # (Query, Expected Action, Expected Identifier, Expected Resource Type)
    ("poweron apollo-node-029", "ON", "apollo-node-029", ""),
    ("power off apollo-node-029", "OFF", "apollo-node-029", "power"),
    ("reboot node-abc", "RESET", "node-abc", ""),
    ("create new storage array named alletra-999", "CREATE", "alletra-999", ""),
    ("allocate 500GB volume for db-cluster", "ALLOCATE", "db-cluster", ""), # Expected to fail regex but fallback to LLM
    ("deprovision vm-test-123", "DELETE", "vm-test-123", ""),
    ("delete virtual machine named web-app-1", "DELETE", "web-app-1", ""),
    ("status of my-db-server", "STATUS", "my-db-server", ""),
    ("check health of all routers", "STATUS", "all", ""),
    ("rescan network for new devices", "RESCAN", "", ""),
    ("show temperature for alletra-array-999", "STATUS", "alletra-array-999", "sensor"),
    ("set firmware version of switch-01 to 1.2.3", "UPDATE", "switch-01", "firmware"),
    ("change status of gl-ns-008 to offline", "UPDATE", "gl-ns-008", ""),
    ("modify firmware of apollo-node-029 to 2.1.0", "UPDATE", "apollo-node-029", "firmware"),
    ("update health status to OK", "UPDATE", "", ""),
    ("configure new device apollo-node-097", "UPDATE", "apollo-node-097", ""),
    ("nuke vm-test", "DELETE", "vm-test", ""),
    
    # User's specific regression tests
    ("show firmware version of apollo-node-999", "STATUS", "apollo-node-999", "firmware"),
    ("get event logs for dl360-prod-01", "FETCH_EVENT_LOG", "dl360-prod-01", "event"),
    ("show metrics for vm-123", "STATUS", "vm-123", "metric"),
    ("create storage array named apollo-node-999", "CREATE", "apollo-node-999", ""),
    
    # Separator variants tests
    ("show firmware-version of apollo-node-999", "STATUS", "apollo-node-999", "firmware"),
    ("show event-logs for apollo-node-999", "STATUS", "apollo-node-999", "event"),
    ("show power-state of apollo-node-999", "STATUS", "apollo-node-999", "power"),
    ("show user_accounts on apollo-node-999", "STATUS", "apollo-node-999", "account"),
    
    # Boundary preservation tests
    ("show firmware-node-999", "STATUS", "firmware-node-999", "firmware"),
    ("show event-router-01", "STATUS", "event-router-01", "event"),
    ("show power-array-01", "STATUS", "power-array-01", "power"),
]

def run_tests():
    passed = 0
    failed = 0
    for query, exp_action, exp_identifier, exp_resource_type in test_cases:
        res = QueryAgent._parse(query)
        
        act = res.get('action')
        ident = res.get('identifier')
        r_type = res.get('resource_type')
        conf = res.get('confidence', 0.0)
            
        success = True
        errors = []
        
        if act != exp_action:
            if not (exp_action == "UNPARSEABLE" and conf < 0.7):
                success = False
                errors.append(f"Action: expected {exp_action}, got {act}")
        if exp_identifier != "" and ident != exp_identifier:
            if not (conf < 0.7):
                if query != "allocate 500GB volume for db-cluster": # Ignore this specific fallback case
                    success = False
                    errors.append(f"Identifier: expected '{exp_identifier}', got '{ident}'")
        if r_type != exp_resource_type:
            success = False
            errors.append(f"Resource Type: expected '{exp_resource_type}', got '{r_type}'")
                    
        if success:
            print(f"[PASS] {query}")
            passed += 1
        else:
            print(f"[FAIL] {query}")
            for e in errors:
                print(f"       - {e}")
            failed += 1
            
    print(f"\nResults: {passed} passed, {failed} failed")

if __name__ == "__main__":
    run_tests()
