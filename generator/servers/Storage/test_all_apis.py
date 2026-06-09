import sys
import os
import json
import time
import subprocess
import urllib.request
import urllib.error
import re

def main():
    print("Starting FastAPI Mock Server...")
    # Find python executable in current env
    python_exe = sys.executable
    
    server_dir = os.path.dirname(os.path.abspath(__file__))
    main_py = os.path.join(server_dir, "main.py")
    routes_json = os.path.join(server_dir, "routes.json")
    uvicorn_log_path = os.path.join(server_dir, "uvicorn.log")
    
    if not os.path.exists(main_py) or not os.path.exists(routes_json):
        print("Error: main.py or routes.json not found in this folder.")
        sys.exit(1)
        
    # Open uvicorn.log for writing logs safely (no pipe buffer issues)
    with open(uvicorn_log_path, "w", encoding="utf-8") as log_file:
        proc = subprocess.Popen(
            [python_exe, "-m", "uvicorn", "main:app", "--port", "8039"],
            cwd=server_dir,
            stdout=log_file,
            stderr=log_file
        )
        
        # Wait for startup
        time.sleep(4)
        if proc.poll() is not None:
            print(f"Failed to start server. (Exit code: {proc.poll()})")
            # Dump uvicorn log to console for debugging
            try:
                with open(uvicorn_log_path, "r", encoding="utf-8") as f:
                    print("--- Uvicorn Logs ---")
                    print(f.read())
                    print("--------------------")
            except Exception:
                pass
            sys.exit(1)
            
        try:
            with open(routes_json, "r", encoding="utf-8") as f:
                routes_data = json.load(f)
                
            endpoints = routes_data.get("endpoints", {})
            total_endpoints = len(endpoints)
            print(f"Loaded {total_endpoints} endpoints from routes.json. Starting testing...")
            
            success_count = 0
            failure_count = 0
            errors_details = []
            
            # Test a representative sample of 40 endpoints across different resource ranges
            all_items = list(endpoints.items())
            step = max(1, len(all_items) // 40)
            tested_endpoints = all_items[::step][:40]
            
            for name, info in tested_endpoints:
                method = info["method"].upper()
                path_template = info["path_template"]
                body = info.get("body_template", {})
                
                # Format path parameters (replace {param} with "test_val")
                path = re.sub(r"\{[^}]+\}", "test_id", path_template)
                url = f"http://127.0.0.1:8039{path}"
                
                print(f"Testing {method} {path_template} -> ", end="", flush=True)
                
                req_data = None
                headers = {}
                if method in ["POST", "PUT", "PATCH"] and body:
                    req_data = json.dumps(body).encode("utf-8")
                    headers = {"Content-Type": "application/json"}
                    
                req = urllib.request.Request(url, data=req_data, headers=headers, method=method)
                
                try:
                    with urllib.request.urlopen(req, timeout=5) as resp:
                        code = resp.getcode()
                        if code in [200, 201, 202, 204]:
                            print(f"OK ({code})")
                            success_count += 1
                        else:
                            print(f"UNEXPECTED STATUS ({code})")
                            failure_count += 1
                            errors_details.append((method, path_template, f"Status: {code}"))
                except urllib.error.HTTPError as e:
                    code = e.code
                    if code in [422]:
                        detail = e.read().decode('utf-8')
                        print(f"VALIDATION FAILED ({code}): {detail[:200]}")
                        failure_count += 1
                        errors_details.append((method, path_template, f"Validation Error (422): {detail}"))
                    elif code == 500:
                        print(f"SERVER ERROR (500)")
                        failure_count += 1
                        errors_details.append((method, path_template, "Server Error (500)"))
                    else:
                        print(f"OK/IGNORED ({code})")
                        success_count += 1
                except Exception as e:
                    print(f"CONNECTION ERROR: {e}")
                    failure_count += 1
                    errors_details.append((method, path_template, f"Connection Error: {e}"))
                    
            print("\n=================== TESTING SUMMARY ===================")
            print(f"Total endpoints in spec: {total_endpoints}")
            print(f"Sample endpoints tested: {len(tested_endpoints)}")
            print(f"Passed/OK: {success_count}")
            print(f"Failed/Errors: {failure_count}")
            if errors_details:
                print("\nError Details:")
                for m, p, err in errors_details[:10]:
                    print(f" - {m} {p}: {err[:150]}")
                if len(errors_details) > 10:
                    print(f" ... and {len(errors_details)-10} more.")
            print("=======================================================")
            
        finally:
            print("Stopping FastAPI Mock Server...")
            proc.terminate()
            proc.wait()

if __name__ == "__main__":
    main()
