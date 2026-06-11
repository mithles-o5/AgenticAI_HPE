import sys
import os
import re
from fastapi.testclient import TestClient

def import_app(server_dir):
    full_path = os.path.abspath(server_dir)
    sys.path.insert(0, full_path)
    
    # Clean up sys.modules to prevent cache reuse/namespace clashes
    for mod in ['models', 'main']:
        if mod in sys.modules:
            del sys.modules[mod]
            
    import main
    app = main.app
    
    # Restore sys.path
    sys.path.remove(full_path)
    return app

# Load mock servers dynamically in isolation
oneview_app = import_app('generator/servers/oneview')
compute_ops_app = import_app('generator/servers/compute_ops')
storage_app = import_app('generator/servers/Storage')
cloud_app = import_app('generator/servers/Cloud')

servers = {
    "OneView Mock Server": oneview_app,
    "Compute Ops Mock Server": compute_ops_app,
    "Storage Mock Server": storage_app,
    "Cloud Mock Server": cloud_app
}

def test_routes_for_app(app_name, app):
    client = TestClient(app)
    print(f"\n==========================================")
    print(f"Testing {app_name} ({len(app.routes)} routes)")
    print(f"==========================================")
    
    success_count = 0
    fail_count = 0
    
    # Filter out standard FastAPI OpenAPI/docs routes
    test_routes = []
    for r in app.routes:
        if not hasattr(r, "methods") or not hasattr(r, "path"):
            continue
        if r.path in ["/openapi.json", "/docs", "/redoc"]:
            continue
        test_routes.append(r)
        
    for idx, r in enumerate(test_routes):
        methods = r.methods
        path = r.path
        
        # Replace path parameters with dummy test values
        params = re.findall(r'\{([^}]+)\}', path)
        test_path = path
        for p in params:
            test_path = test_path.replace('{' + p + '}', f"test-{p}")
            
        for method in methods:
            if method not in ["GET", "POST", "PUT", "DELETE", "PATCH"]:
                continue
                
            try:
                if method == "GET":
                    resp = client.get(test_path)
                    assert resp.status_code in [200, 201, 204, 404], f"Status: {resp.status_code}"
                elif method == "POST":
                    payload = {"id": "test-resource-id", "name": "TestResource"}
                    resp = client.post(test_path, json=payload)
                    assert resp.status_code in [200, 201, 204, 404], f"Status: {resp.status_code}"
                elif method == "PUT":
                    payload = {"name": "TestResourceUpdated"}
                    resp = client.put(test_path, json=payload)
                    assert resp.status_code in [200, 201, 204, 404], f"Status: {resp.status_code}"
                elif method == "DELETE":
                    resp = client.delete(test_path)
                    assert resp.status_code in [200, 201, 204, 404], f"Status: {resp.status_code}"
                elif method == "PATCH":
                    payload = {"name": "TestResourcePatched"}
                    resp = client.patch(test_path, json=payload)
                    assert resp.status_code in [200, 201, 204, 404], f"Status: {resp.status_code}"
                    
                success_count += 1
            except Exception as e:
                print(f"❌ Failed: {method} {path} (mapped: {test_path}) -> {e}")
                fail_count += 1
                
    print(f"\n{app_name} Summary:")
    print(f"  Passed: {success_count}")
    print(f"  Failed: {fail_count}")
    return success_count, fail_count

def main():
    total_passed = 0
    total_failed = 0
    for name, app in servers.items():
        passed, failed = test_routes_for_app(name, app)
        total_passed += passed
        total_failed += failed
        
    print(f"\n==========================================")
    print(f"OVERALL MOCK SERVERS VERIFICATION SUMMARY:")
    print(f"  Total Passed HTTP Actions: {total_passed}")
    print(f"  Total Failed HTTP Actions: {total_failed}")
    print(f"==========================================")
    
    if total_failed > 0:
        sys.exit(1)
        
if __name__ == "__main__":
    main()
