import sys
import os
import glob
import importlib.util

workspace = r"c:\AgenticAI_HPE"
mock_dirs = glob.glob(os.path.join(workspace, "mock_server(*)"))

all_endpoints = {}

for d in mock_dirs:
    vendor_name = os.path.basename(d).replace("mock_server(", "").replace(")", "")
    main_py = os.path.join(d, "main.py")
    if not os.path.exists(main_py):
        continue
    
    # clear modules that might conflict
    to_delete = []
    for mod_name, mod in sys.modules.items():
        if getattr(mod, '__file__', None) and 'mock_server' in mod.__file__:
            to_delete.append(mod_name)
    for mod_name in to_delete:
        del sys.modules[mod_name]
        
    sys.path.insert(0, d)
    spec = importlib.util.spec_from_file_location("main", main_py)
    main_mod = importlib.util.module_from_spec(spec)
    
    try:
        spec.loader.exec_module(main_mod)
        routes = main_mod.app.routes
        for r in routes:
            if hasattr(r, "methods") and hasattr(r, "path"):
                for method in r.methods:
                    if method == "HEAD": continue
                    if vendor_name not in all_endpoints:
                        all_endpoints[vendor_name] = []
                    all_endpoints[vendor_name].append((method, r.path))
    except Exception as e:
        print(f"Error loading {d}: {e}")
    
    sys.path.pop(0)

with open(r"c:\AgenticAI_HPE\scratch\routes_dump.txt", "w", encoding="utf-8") as f:
    for vendor, eps in all_endpoints.items():
        f.write(f"--- Vendor: {vendor} ---\n")
        for method, path in eps:
            f.write(f"{method} {path}\n")
