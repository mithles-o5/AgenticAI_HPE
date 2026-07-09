import sys, os, asyncio, json
os.environ['PYTHONIOENCODING'] = 'utf-8'
sys.path.append('c:\\AgenticAI_HPE')

import mcp_server.mcp_server as ms
ms._require_auth = lambda: ("admin@hpe.com", "admin")
ms._authorize = lambda a, b, c, d, e: (True, "Authorized", "admin@hpe.com")

from mcp_server.mcp_server import manage_infrastructure_resource

test_cases = [
    "poweron apollo-node-029",
    "power off apollo-node-029",
    "reboot node-abc",
    "create new storage array named alletra-999",
    "allocate 500GB volume for db-cluster",
    "deprovision vm-test-123",
    "delete virtual machine named web-app-1",
    "status of my-db-server",
    "check health of all routers",
    "rescan network for new devices",
    "show temperature for alletra-array-999",
    "set firmware version of switch-01 to 1.2.3",
    "change status of gl-ns-008 to offline",
    "modify firmware of apollo-node-029 to 2.1.0",
    "update health status to OK",
    "configure new device apollo-node-097",
    "nuke vm-test",
    "show firmware version of apollo-node-999",
    "get event logs for dl360-prod-01",
    "show metrics for vm-123",
    "create storage array named apollo-node-999",
    "show firmware-version of apollo-node-999",
    "show event-logs for apollo-node-999",
    "show power-state of apollo-node-999",
    "show user_accounts on apollo-node-999",
    "show firmware-node-999",
    "show event-router-01",
    "show power-array-01"
]

async def run_query(query):
    try:
        res = await manage_infrastructure_resource(query)
        if "Authorization error" in res or "Access Denied" in res or "ERROR" in res:
            return query, {"status": "FAILED", "output": res}
        return query, {"status": "SUCCESS", "output": res}
    except Exception as e:
        return query, {"status": "EXCEPTION", "output": str(e)}

async def main():
    results = {}
    passed = 0
    failed = 0
    
    tasks = [run_query(q) for q in test_cases]
    outputs = await asyncio.gather(*tasks)
    
    for query, result in outputs:
        results[query] = result
        if result["status"] == "SUCCESS":
            passed += 1
        else:
            failed += 1

    results["SUMMARY"] = {"passed": passed, "failed": failed}
    
    with open("c:\\AgenticAI_HPE\\scratch\\run_all_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)
        
    print(f"Done! Passed: {passed}, Failed: {failed}")

if __name__ == "__main__":
    asyncio.run(main())
