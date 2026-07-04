import sys
import os
import glob
import importlib.util

# Add resource_resolver to path to import db
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from db import db_manager
from psycopg2 import extras

def extract_routes(workspace_dir=r"c:\AgenticAI_HPE"):
    mock_dirs = glob.glob(os.path.join(workspace_dir, "mock_server(*)")) + glob.glob(os.path.join(workspace_dir, "mock_*")) + glob.glob(os.path.join(workspace_dir, "oneview")) + glob.glob(os.path.join(workspace_dir, "comops"))
    
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
                            
                            device_type = "generic"
                            path_parts = [p for p in r.path.split("/") if p and not p.startswith("{")]
                            if path_parts:
                                device_type = path_parts[-1]
                            
                            action_key = method.upper()
                            if method == "GET" and not r.path.endswith("}"): action_key = "LIST"
                            if method == "GET" and r.path.endswith("}"): action_key = "STATUS"
                            
                            all_endpoints.append({
                                "vendor": vendor_name.lower(),
                                "device_type": device_type,
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
            cur.execute("SELECT vendor, device_type, action_key, http_method, api_path FROM endpoint_registry;")
            existing_rows = cur.fetchall()
            
            existing_set = {
                (r[0], r[1], r[2], r[3], r[4]) for r in existing_rows
            }
            
            # Gap analysis
            to_insert = []
            seen = set()
            duplicates = 0
            missing_added = 0
            
            vendor_counts = {}
            for ep in discovered:
                vendor = ep['vendor']
                vendor_counts.setdefault(vendor, {"discovered": 0, "registered": 0, "missing": 0, "duplicates": 0, "final": 0})
                vendor_counts[vendor]["discovered"] += 1
                
                key = (ep['vendor'], ep['device_type'], ep['action_key'], ep['http_method'], ep['api_path'])
                if key in seen:
                    vendor_counts[vendor]["duplicates"] += 1
                    duplicates += 1
                    continue
                seen.add(key)
                
                if key in existing_set:
                    vendor_counts[vendor]["registered"] += 1
                else:
                    vendor_counts[vendor]["missing"] += 1
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
                args = [
                    (r["vendor"], r["device_type"], r["action_key"], r["http_method"], r["api_path"])
                    for r in to_insert
                ]
                extras.execute_values(
                    cur,
                    """
                    INSERT INTO endpoint_registry
                        (vendor, device_type, action_key, http_method, api_path)
                    VALUES %s
                    ON CONFLICT (vendor, device_type, action_key, api_path, http_method)
                    DO NOTHING
                    """,
                    args,
                    page_size=250,
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
