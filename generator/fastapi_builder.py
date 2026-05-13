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
