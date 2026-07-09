import sys
import os
import glob
import importlib.util

# Add resource_resolver to path to import db
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from db import db_manager
from psycopg2 import extras
from seed_endpoint_registry import _infer_device_type, _infer_resource_type

def extract_routes(workspace_dir=r"c:\AgenticAI_HPE"):
    mock_dirs = glob.glob(os.path.join(workspace_dir, "mock_server(*)")) + glob.glob(os.path.join(workspace_dir, "mock_*")) + glob.glob(os.path.join(workspace_dir, "oneview")) + glob.glob(os.path.join(workspace_dir, "coms"))
    
    # ensure uniqueness of directories
    mock_dirs = list(set(d for d in mock_dirs if os.path.isdir(d)))
    
    all_endpoints = []
    
    for d in mock_dirs:
        vendor_name = os.path.basename(d)
        if vendor_name.startswith("mock_server("):
            vendor_name = vendor_name.replace("mock_server(", "").replace(")", "")
        elif vendor_name.startswith("mock_"):
            vendor_name = vendor_name.replace("mock_", "")
            
        main_py = os.path.join(d, "main.py")
        if not os.path.exists(main_py):
            continue
        
        # Clear modules that might conflict
        to_delete = [m for m, mod in sys.modules.items() if getattr(mod, '__file__', None) and ('mock_' in mod.__file__ or 'mock_server' in mod.__file__)]
        for m in to_delete:
            del sys.modules[m]
            
        sys.path.insert(0, d)
        spec = importlib.util.spec_from_file_location("main", main_py)
        main_mod = importlib.util.module_from_spec(spec)
        
        try:
            spec.loader.exec_module(main_mod)
            if hasattr(main_mod, 'app') and hasattr(main_mod.app, 'routes'):
                for r in main_mod.app.routes:
                    if hasattr(r, "methods") and hasattr(r, "path"):
                        for method in r.methods:
                            if method == "HEAD": continue
                            # Infer device_type and action_key based on simple rules or keep them generic for now,
                            # the prompt says "Extract: HTTP Method, Endpoint Path, Provider / Management Source, Resource Category, Source File"
                            # We'll map Resource Category as device_type, Management Source as vendor
                            
                            device_types = _infer_device_type(r.path, vendor_name.lower())
                            resource_type = _infer_resource_type(r.path)
                            
                            action_key = method.upper()
                            if method == "GET" and not r.path.endswith("}"): action_key = "LIST"
                            if method == "GET" and r.path.endswith("}"): action_key = "STATUS"
                            
                            all_endpoints.append({
                                "vendor": vendor_name.lower(),
                                "device_types": device_types,
                                "resource_type": resource_type,
                                "action_key": action_key,
                                "http_method": method.upper(),
                                "api_path": r.path,
                                "source_file": main_py
                            })
        except Exception as e:
            print(f"Error loading {d}: {e}")
        finally:
            if sys.path[0] == d:
                sys.path.pop(0)
                
    return all_endpoints

def main():
    print("Extracting endpoints from mock providers...")
    discovered = extract_routes()
    print(f"Total discovered raw routes: {len(discovered)}")
    
    # Connect to DB
    conn = db_manager.get_connection()
    if not conn:
        print("Could not connect to database.")
        return

    try:
        with conn.cursor() as cur:
            existing_set = set()
            cur.execute("""
                SELECT e.management_source, d.name, e.action_key, e.http_method, e.api_path 
                FROM endpoint_registry e
                JOIN endpoint_device_mapping m ON e.id = m.endpoint_id
                JOIN device_type d ON m.device_type_id = d.id
            """)
            for row in cur.fetchall():
                existing_set.add((row[0], row[1], row[2], row[3], row[4]))
            
            # Gap analysis
            to_insert = []
            seen = set()
            duplicates = 0
            
            vendor_counts = {}
            for ep in discovered:
                vendor = ep['vendor']
                vendor_counts.setdefault(vendor, {"discovered": 0, "registered": 0, "missing": 0, "duplicates": 0, "final": 0})
                vendor_counts[vendor]["discovered"] += 1
                
                for dt in ep['device_types']:
                    key = (vendor, dt, ep['action_key'], ep['http_method'], ep['api_path'])
                    if key in seen:
                        vendor_counts[vendor]["duplicates"] += 1
                        duplicates += 1
                        continue
                    seen.add(key)
                    
                    if key in existing_set:
                        vendor_counts[vendor]["registered"] += 1
                    else:
                        vendor_counts[vendor]["missing"] += 1
                        # We track the endpoint as a whole if any of its mappings are missing
                        if ep not in to_insert:
                            to_insert.append(ep)
                    
            print("\n--- GAP ANALYSIS ---")
            for v, c in vendor_counts.items():
                c["final"] = c["registered"] + c["missing"]
                print(f"Vendor: {v}")
                print(f"  Discovered: {c['discovered']}")
                print(f"  Already Registered: {c['registered']}")
                print(f"  Missing (to add): {c['missing']}")
                print(f"  Duplicates detected: {c['duplicates']}")
                print(f"  Final count: {c['final']}\n")
                
            if to_insert:
                print(f"Inserting {len(to_insert)} missing endpoints...")
                
                # First ensure all device_types exist in device_type
                unique_types = set()
                unique_res_types = set()
                for r in to_insert:
                    unique_types.update(r["device_types"])
                    if r["resource_type"]:
                        unique_res_types.add(r["resource_type"])
                
                cur.execute("SELECT name, id FROM device_type")
                type_map = {row[0]: row[1] for row in cur.fetchall()}
                
                for t in unique_types:
                    if t not in type_map:
                        cur.execute(
                            "INSERT INTO device_type (name) VALUES (%s) RETURNING id",
                            (t,)
                        )
                        type_map[t] = cur.fetchone()[0]
                        
                cur.execute("SELECT res_type, id FROM resource_type")
                res_type_map = {row[0]: row[1] for row in cur.fetchall()}
                
                for rt in unique_res_types:
                    if rt not in res_type_map:
                        cur.execute(
                            "INSERT INTO resource_type (res_type) VALUES (%s) RETURNING id",
                            (rt,)
                        )
                        res_type_map[rt] = cur.fetchone()[0]

                args = [
                    (
                        r["vendor"], 
                        r["action_key"], 
                        r["http_method"], 
                        r["api_path"], 
                        res_type_map.get(r["resource_type"]) if r["resource_type"] else None
                    )
                    for r in to_insert
                ]
                
                insert_query = """
                    INSERT INTO endpoint_registry
                        (management_source, action_key, http_method, api_path, resource_type_id)
                    VALUES %s
                    ON CONFLICT (management_source, action_key, api_path, http_method)
                    DO NOTHING
                """
                extras.execute_values(cur, insert_query, args, page_size=250)
                
                # We fetch IDs to perform the mapping insertion
                cur.execute("SELECT id, management_source, action_key, http_method, api_path FROM endpoint_registry")
                endpoint_map = {(row[1], row[2], row[3], row[4]): row[0] for row in cur.fetchall()}
                
                mapping_args = []
                for r in to_insert:
                    ep_key = (r["vendor"], r["action_key"], r["http_method"], r["api_path"])
                    ep_id = endpoint_map.get(ep_key)
                    if ep_id:
                        for dt in r["device_types"]:
                            mapping_args.append((ep_id, type_map[dt]))
                        
                if mapping_args:
                    extras.execute_values(
                        cur,
                        "INSERT INTO endpoint_device_mapping (endpoint_id, device_type_id) VALUES %s ON CONFLICT DO NOTHING",
                        mapping_args,
                        page_size=250
                    )
                conn.commit()
                print("Insertion complete.")
            else:
                print("No missing endpoints to insert.")
                
    except Exception as e:
        print(f"Database error: {e}")
        conn.rollback()
    finally:
        db_manager.return_connection(conn)

if __name__ == "__main__":
    main()
