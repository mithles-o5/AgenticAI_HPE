import ast
import json
import os

generator_dir = os.path.dirname(os.path.abspath(__file__))

def parse_main_py(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read())
    
    routes = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            for decorator in node.decorator_list:
                if isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Attribute):
                    if isinstance(decorator.func.value, ast.Name) and decorator.func.value.id == "app":
                        method = decorator.func.attr.upper()
                        if decorator.args:
                            path_node = decorator.args[0]
                            if isinstance(path_node, ast.Constant):
                                path = path_node.value
                                routes.append({
                                    "method": method,
                                    "path": path,
                                    "function_name": node.name
                                })
    return routes

def rebuild_routes_for_server(server_name):
    server_dir = os.path.join(generator_dir, "servers", server_name)
    main_py_path = os.path.join(server_dir, "main.py")
    routes_json_path = os.path.join(server_dir, "routes.json")
    
    if not os.path.exists(main_py_path):
        print(f"Error: {main_py_path} not found.")
        return
        
    routes = parse_main_py(main_py_path)
    
    routes_data = {
        "protocol": server_name,
        "base_url": "http://localhost:8000",
        "endpoints": {}
    }
    for r in routes:
        routes_data["endpoints"][r["function_name"]] = {
            "method": r["method"],
            "path_template": r["path"],
            "triggers": [
                r["function_name"],
                r["path"]
            ]
        }
        
    with open(routes_json_path, "w", encoding="utf-8") as f:
        json.dump(routes_data, f, indent=4)
    print(f"Successfully generated routes.json for {server_name} with {len(routes)} endpoints.")

if __name__ == "__main__":
    rebuild_routes_for_server("oneview")
    rebuild_routes_for_server("compute_ops")
