import os
import json

def generate_pydantic_model(body_dict, model_name):
    """
    Improvement 3: Schema-to-Pydantic Model Generator
    Auto-generates Pydantic BaseModel instances based on request JSON structure.
    """
    if not isinstance(body_dict, dict) or not body_dict:
        return ""
        
    lines = [f"class {model_name}(BaseModel):"]
    for key, value in body_dict.items():
        type_str = "Any"
        if isinstance(value, str): type_str = "str"
        elif isinstance(value, bool): type_str = "bool"
        elif isinstance(value, int): type_str = "int"
        elif isinstance(value, float): type_str = "float"
        elif isinstance(value, list): type_str = "list"
        elif isinstance(value, dict): type_str = "dict"
        
        # Pydantic v2 compliant
        lines.append(f"    {key}: {type_str} = None")
        
    if len(lines) == 1:
        lines.append("    pass")
    return "\n".join(lines) + "\n"

def generate_fastapi_server(server_name, api_data, output_folder="servers"):
    base_path = os.path.join(output_folder, server_name)
    os.makedirs(base_path, exist_ok=True)
    
    mock_db = {}
    main_file_path = os.path.join(base_path, "main.py")
    models_file_path = os.path.join(base_path, "models.py")

    models_code = "from pydantic import BaseModel\nfrom typing import Any\n\n"
    
    main_code = """from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import json
import os
from models import *

mock_file = os.path.join(os.path.dirname(__file__), "mock_data.json")
try:
    with open(mock_file, "r", encoding="utf-8") as f:
        MOCK_DB = json.load(f)
except Exception:
    MOCK_DB = {}

app = FastAPI(title='Generated Mock Server', description='Generated automatically from API docs.')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
"""

    for index, api in enumerate(api_data):
        # Ensure entry is a dict
        if not isinstance(api, dict):
            print(f"[WARN] Skipping non-dict API entry at index {index}: {api}")
            continue
        # Ensure we have a function_name; fall back to generated name if missing
        if "function_name" not in api:
            # Generate a deterministic name based on method and path
            from slugify import slugify
            generated_name = slugify(f"{api.get('method','GET')}_{api.get('path','')}").replace("-", "_")
            api["function_name"] = generated_name
        clean_name = "".join(x.capitalize() or "_" for x in api["function_name"].split("_"))
        model_name = f"{clean_name}Request"
        has_model = False
        
        # Build Request Body Model
        if api.get("request_body"):
            model_str = generate_pydantic_model(api["request_body"], model_name)
            if "class" in model_str:
                models_code += model_str + "\n"
                has_model = True

        # Append mock JSON response payload to database
        mock_db[api["function_name"]] = api.get("response_body", {})

        main_code += f'''
@{api["method"].lower() if api["method"].lower() in ["get", "post", "put", "patch", "delete"] else "api.route"}("{api["path"]}")
def {api["function_name"]}('''
        
        # Extract path parameters using regex
        import re
        path_params = re.findall(r"\{([a-zA-Z0-9_]+)\}", api["path"])
        
        sig_args = []
        for param in path_params:
            sig_args.append(f"{param}: str")
            
        # Add query parameters if present
        query_params = [p for p in api.get("parameters", []) if p.get("in") == "query"]
        for p in query_params:
            name = p["name"]
            is_required = p.get("required", False)
            if "-" in name or "." in name:
                safe_name = name.replace("-", "_").replace(".", "_")
                if is_required:
                    sig_args.append(f"{safe_name}: str = Query(..., alias='{name}')")
                else:
                    sig_args.append(f"{safe_name}: str = Query(None, alias='{name}')")
            else:
                if is_required:
                    sig_args.append(f"{name}: str")
                else:
                    sig_args.append(f"{name}: str = None")
            
        # Add Request body payload parameter
        if has_model and api["method"].upper() in ["POST", "PUT", "PATCH"]:
            sig_args.append(f"payload: {model_name}")
            
        main_code += ", ".join(sig_args)
            
        main_code += f'''):
    """
    Auto-generated Route
    Original Doc: {api.get("source_url", "Unknown")}
    """
    return MOCK_DB.get("{api["function_name"]}", dict())
'''

    with open(os.path.join(base_path, "mock_data.json"), "w", encoding="utf-8") as f:
        json.dump(mock_db, f, indent=4)

    # Unify writing to just `main.py` and `models.py`
    with open(models_file_path, "w", encoding="utf-8") as f:
        f.write(models_code)
        
    # main code fixes specifically using `@app.` instead of `@get(`
    main_code = main_code.replace("\n@get(", "\n@app.get(")
    main_code = main_code.replace("\n@post(", "\n@app.post(")
    main_code = main_code.replace("\n@put(", "\n@app.put(")
    main_code = main_code.replace("\n@patch(", "\n@app.patch(")
    main_code = main_code.replace("\n@delete(", "\n@app.delete(")

    with open(main_file_path, "w", encoding="utf-8") as f:
        f.write(main_code)

    requirements_path = os.path.join(base_path, "requirements.txt")
    with open(requirements_path, "w") as f:
        f.write("fastapi\nuvicorn\npydantic\nmcp\nrequests\n")

    # Generate routes.json mapping path templates to action/function names
    routes_data = {
        "protocol": server_name,
        "base_url": "http://localhost:8000",
        "endpoints": {}
    }
    for api in api_data:
        routes_data["endpoints"][api["function_name"]] = {
            "method": api["method"].upper(),
            "path_template": api["path"],
            "triggers": [
                api["function_name"],
                api["path"]
            ],
            "body_template": api.get("request_body")
        }
    routes_path = os.path.join(base_path, "routes.json")
    with open(routes_path, "w", encoding="utf-8") as f:
        json.dump(routes_data, f, indent=4)
        
    print(f"  [OK] Generated Routes Config: {routes_path}")

    # Generate human prompts reference guide
    def get_prompt_text(method, path):
        parts = [p for p in path.split("/") if p and not p.startswith("{") and p not in ("rest", "compute-ops-mgmt")]
        resource_desc = " ".join(parts).replace("-", " ").replace("_", " ") if parts else "resource"
        import re
        path_vars = re.findall(r'\{([^}]+)\}', path)
        vars_str = " ".join(f"with {v} '<value>'" for v in path_vars)
        if method == "GET":
            if not path_vars: return f"List all {resource_desc}."
            elif path.endswith("thermal"): return f"Get thermal information of server {vars_str.replace('id', 'server_id')}."
            elif path.endswith("processors"): return f"Get processor details of server {vars_str.replace('id', 'server_id')}."
            elif path.endswith("networkAdapters"): return f"Get network adapters of server {vars_str.replace('id', 'server_id')}."
            elif path.endswith("powerSupplies"): return f"Get power supplies of server {vars_str.replace('id', 'server_id')}."
            elif path.endswith("firmwareInventory"): return f"Get firmware inventory of server {vars_str.replace('id', 'server_id')}."
            elif path.endswith("softwareInventory"): return f"Get software inventory of server {vars_str.replace('id', 'server_id')}."
            elif path.endswith("chassis"): return f"Get chassis details of {resource_desc} {vars_str}."
            elif path.endswith("alerts"): return f"Get alerts details for {resource_desc} {vars_str}."
            else: return f"Get details of {resource_desc} {vars_str}."
        elif method == "POST":
            if "power-on" in path or "power_on" in path or path.endswith("power-on") or path.endswith("power_on"):
                return f"Power on server {vars_str.replace('id', 'server_id')}."
            elif "power-off" in path or "power_off" in path or path.endswith("power-off") or path.endswith("power_off"):
                return f"Power off server {vars_str.replace('id', 'server_id')}."
            elif "approve" in path: return f"Approve request {vars_str} with remarks 'approved'."
            elif "test" in path: return f"Run test on {resource_desc} {vars_str}."
            else: return f"Create a new {resource_desc} {vars_str}."
        elif method == "DELETE": return f"Delete {resource_desc} {vars_str}."
        elif method in ["PUT", "PATCH"]:
            if "powerState" in path: return f"Set power state of server {vars_str.replace('id', 'server_id')} to 'On' (or 'Off' / 'Reset')."
            else: return f"Update {resource_desc} {vars_str}."
        return f"Execute {method} on {path}."

    human_prompt_lines = [
        "=" * 80,
        f"  HUMAN PROMPTS REFERENCE GUIDE FOR {server_name.upper()} APIS",
        "=" * 80,
        "Copy and paste any of the prompts below directly into your chat with Claude.",
        "Replace '<value>' with the actual UUID, ID, or payload values you want to target.",
        "=" * 80 + "\n\n"
    ]
    for api in sorted(api_data, key=lambda x: x["function_name"]):
        method = api["method"].upper()
        path = api["path"]
        func_name = api["function_name"]
        
        parts = [p for p in path.split("/") if p and not p.startswith("{") and p not in ("rest", "compute-ops-mgmt")]
        resource_desc = " ".join(parts).replace("-", " ").replace("_", " ") if parts else "resource"
        human_prompt = get_prompt_text(method, path)
        
        human_prompt_lines.append("=" * 80)
        human_prompt_lines.append(f"API Goal: {resource_desc.upper()} ({method})")
        human_prompt_lines.append(f"Prompt  : {human_prompt}")
        human_prompt_lines.append(f"Action  : action:{func_name}")
        human_prompt_lines.append("=" * 80 + "\n")
        
    human_prompts_path = os.path.join(base_path, "human_prompts.txt")
    with open(human_prompts_path, "w", encoding="utf-8") as f:
        f.write("\n".join(human_prompt_lines))
    print(f"  [OK] Generated Human Prompts Guide: {human_prompts_path}")
