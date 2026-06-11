import sys
import os
import asyncio
import subprocess
import time
import json
import psycopg2

sys.path.insert(0, os.path.abspath('.'))

# Import from mcp_server
from mcp_server.mcp_server import (
    init_db,
    remember,
    recall,
    recall_session,
    forget_key,
    forget_session,
    list_sessions,
    list_servers_in_rack,
    power_off_last_targets,
    SESSION_ID
)

async def test_db_functions():
    print("\n=== Testing Memory Store CRUD functions ===")
    
    # 1. Initialize DB
    print("[+] Initializing DB...")
    init_db()
    
    # Test session ID
    test_sid = "test-session-xyz"
    
    # Clean up any leftover test session
    forget_session(test_sid)
    
    # 2. Test remember and recall
    print("[+] Testing remember & recall...")
    test_key = "last_rack"
    test_val = "Rack-05"
    remember(test_sid, test_key, test_val)
    
    recalled = recall(test_sid, test_key)
    print(f"    Recalled: {recalled} (Expected: {test_val})")
    assert recalled == test_val, f"Recall failed. Expected {test_val}, got {recalled}"
    
    # 3. Test list_sessions
    sessions = list_sessions()
    print(f"    Sessions list: {sessions}")
    assert test_sid in sessions, f"Session ID '{test_sid}' not found in listed sessions"
    
    # 4. Test recall_session
    remember(test_sid, "another_key", {"some": "data"})
    sess_dict = recall_session(test_sid)
    print(f"    Recalled Session Dict: {sess_dict}")
    assert "another_key" in sess_dict
    assert sess_dict["another_key"] == {"some": "data"}
    
    # 5. Test forget_key
    print("[+] Testing forget_key...")
    forget_key(test_sid, "another_key")
    recalled_forgotten = recall(test_sid, "another_key")
    print(f"    Recalled forgotten key: {recalled_forgotten} (Expected: None)")
    assert recalled_forgotten is None
    
    # 6. Test forget_session
    print("[+] Testing forget_session...")
    forget_session(test_sid)
    sess_dict_empty = recall_session(test_sid)
    print(f"    Recalled empty session: {sess_dict_empty} (Expected: {{}})")
    assert len(sess_dict_empty) == 0
    
    print("✅ Memory Store CRUD functions tested successfully!")

async def test_mcp_tools():
    print("\n=== Testing MCP Tools Integration ===")
    
    # Start OneView mock server
    print("[+] Starting OneView Mock Server on port 8000...")
    ov_server = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--port", "8000"],
        cwd="mock_server(oneview)",
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    # Start ComOps mock server
    print("[+] Starting Compute Ops Mock Server on port 8001...")
    comops_server = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--port", "8001"],
        cwd="mock_server(Comops)",
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    time.sleep(3) # Wait for servers to start
    
    try:
        # 1. Call list_servers_in_rack (OneView)
        rack_id = "Rack-01"
        print(f"[+] Calling list_servers_in_rack(rack_id='{rack_id}') ...")
        res_list = await list_servers_in_rack(rack_id=rack_id)
        print("Response from list_servers_in_rack:")
        print(res_list[:500] + "...") # Limit output
        
        # Verify it was stored in memory
        stored_targets = recall(SESSION_ID, "last_targets")
        stored_rack = recall(SESSION_ID, "last_rack")
        print(f"[+] Verifying saved memory context for session '{SESSION_ID}':")
        print(f"    Saved Rack: {stored_rack}")
        print(f"    Saved Targets count: {len(stored_targets)}")
        
        assert stored_rack == rack_id
        assert len(stored_targets) > 0
        
        # 2. Call power_off_last_targets (OneView)
        print("\n[+] Calling power_off_last_targets() ...")
        res_power_off = await power_off_last_targets()
        print("Response from power_off_last_targets:")
        print(res_power_off)
        
        # Verify last_operation stored
        stored_op = recall(SESSION_ID, "last_operation")
        print(f"[+] Verifying saved last_operation:")
        print(json.dumps(stored_op, indent=2))
        assert stored_op["operation"] == "power_off"
        assert len(stored_op["affected_servers"]) == len(stored_targets)
        
        # Verify on mock server that power states are updated
        print("\n[+] Checking server state on mock server after power off...")
        import httpx
        first_target_uuid = stored_targets[0]["uuid"]
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"http://127.0.0.1:8000/rest/server-hardware/{first_target_uuid}")
            server_data = resp.json()
            print(f"    Server {server_data.get('name')} Power State: {server_data.get('powerState')}")
            assert server_data.get("powerState") == "Off"
            
        # 3. Verify Compute Ops Rack Filtering
        print("\n[+] Verifying Compute Ops Mock Server Rack Filtering on Port 8001...")
        async with httpx.AsyncClient() as client:
            # Query without filter: should return all 500 servers
            resp_all = await client.get("http://127.0.0.1:8001/compute-ops-mgmt/v1/servers")
            data_all = resp_all.json()
            all_count = len(data_all.get("items", []))
            print(f"    Total servers without filter: {all_count}")
            assert all_count == 500
            
            # Query with rack/location filter "Zone-2"
            resp_filt = await client.get("http://127.0.0.1:8001/compute-ops-mgmt/v1/servers", params={"rack": "Zone-2"})
            data_filt = resp_filt.json()
            filt_servers = data_filt.get("items", [])
            print(f"    Filtered servers with 'Zone-2': {len(filt_servers)}")
            assert len(filt_servers) > 0 and len(filt_servers) < 500
            for s in filt_servers:
                assert "zone-2" in s.get("location", "").lower()
                
            # Verify v1beta2 route behaves the same
            resp_filt_beta = await client.get("http://127.0.0.1:8001/compute-ops-mgmt/v1beta2/servers", params={"rack": "Zone-2"})
            data_filt_beta = resp_filt_beta.json()
            filt_servers_beta = data_filt_beta.get("items", [])
            print(f"    Filtered servers (v1beta2) with 'Zone-2': {len(filt_servers_beta)}")
            assert len(filt_servers_beta) > 0 and len(filt_servers_beta) < 500
            
            # 4. Verify Dynamic CRUD Middleware on OneView mock server (Port 8000)
            print("\n[+] Verifying Dynamic CRUD Middleware on OneView Mock Server (Port 8000)...")
            # POST to create a rack-manager
            post_payload = {"name": "DynamicRackManager", "model": "RMv1"}
            resp_post = await client.post("http://127.0.0.1:8000/rest/rack-managers", json=post_payload)
            data_post = resp_post.json()
            print(f"    POST Response: {data_post}")
            assert resp_post.status_code in [200, 201]
            assert data_post.get("id") == "DynamicRackManager"
            assert data_post.get("model") == "RMv1"
            
            # GET list to verify it's included
            resp_get_list = await client.get("http://127.0.0.1:8000/rest/rack-managers")
            data_get_list = resp_get_list.json()
            # The static data has members, let's verify
            members = data_get_list.get("members", [])
            print(f"    GET List Count: {len(members)}")
            found = False
            for m in members:
                if m.get("id") == "DynamicRackManager":
                    found = True
                    break
            assert found, "Created rack manager not found in list GET response"
            
            # GET specific item
            resp_get_item = await client.get("http://127.0.0.1:8000/rest/rack-managers/DynamicRackManager")
            data_get_item = resp_get_item.json()
            print(f"    GET Item Response: {data_get_item}")
            assert resp_get_item.status_code == 200
            assert data_get_item.get("model") == "RMv1"
            
            # DELETE to remove it
            resp_del = await client.delete("http://127.0.0.1:8000/rest/rack-managers/DynamicRackManager")
            data_del = resp_del.json()
            print(f"    DELETE Response: {data_del}")
            assert resp_del.status_code == 200
            
            # GET list again to verify it was removed
            resp_get_list_2 = await client.get("http://127.0.0.1:8000/rest/rack-managers")
            data_get_list_2 = resp_get_list_2.json()
            members_2 = data_get_list_2.get("members", [])
            found_2 = False
            for m in members_2:
                if m.get("id") == "DynamicRackManager":
                    found_2 = True
                    break
            assert not found_2, "Rack manager still present in list after DELETE"
            print("    Dynamic CRUD Middleware verified successfully!")
            
        print("✅ MCP tools and mock servers integrated and tested successfully!")
        
    finally:
        print("[+] Shutting down mock servers...")
        ov_server.terminate()
        comops_server.terminate()
        ov_server.wait()
        comops_server.wait()

async def main():
    await test_db_functions()
    await test_mcp_tools()
    print("\n🎉 ALL TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    asyncio.run(main())
