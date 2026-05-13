import os
import re

def generate_mcp_tools(server_name, api_data, output_folder="servers"):
    base_path = os.path.join(output_folder, server_name)
    os.makedirs(base_path, exist_ok=True)
    
    mcp_code = f"""import os
import requests
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("{server_name}")

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

"""

    for api in api_data:
        tool_name = api.get("tool_name", api["function_name"])
        description = api.get("tool_description", f"Executes {api['method']} on {api['path']}").replace('"', "'")
        
        # Path parameters
        path_params = re.findall(r"\{([a-zA-Z0-9_]+)\}", api["path"])
        
        # Query parameters
        query_params = []
        if "parameters" in api:
            query_params = [p["name"] for p in api["parameters"] if p.get("in") == "query"]
            
        # Body parameters
        req_body = api.get("request_body")
        body_params = []
        if req_body and isinstance(req_body, dict):
            body_params = list(req_body.keys())
            
        all_params = []
        for p in path_params:
            all_params.append(f"{p}: str")
        for p in query_params:
            safe_p = p.replace("-", "_").replace(".", "_")
            all_params.append(f"{safe_p}: str = None")
        for p in body_params:
            safe_p = p.replace("-", "_").replace(".", "_")
            all_params.append(f"{safe_p}: str = None")
            
        params_str = ", ".join(all_params)
        
        mcp_code += f"""@mcp.tool(description="{description}")
def {tool_name}({params_str}):
    try:
"""
        mcp_code += f'        url = f"{{API_BASE_URL}}{api["path"]}"\n'
        
        if query_params:
            mcp_code += "        params = {\n"
            for p in query_params:
                safe_p = p.replace("-", "_").replace(".", "_")
                mcp_code += f'            "{p}": {safe_p},\n'
            mcp_code += "        }\n"
            mcp_code += "        params = {k: v for k, v in params.items() if v is not None}\n"
        else:
            mcp_code += "        params = {}\n"
            
        if body_params:
            mcp_code += "        payload = {\n"
            for p in body_params:
                safe_p = p.replace("-", "_").replace(".", "_")
                mcp_code += f'            "{p}": {safe_p},\n'
            mcp_code += "        }\n"
            mcp_code += "        payload = {k: v for k, v in payload.items() if v is not None}\n"
        else:
            mcp_code += "        payload = {}\n"
            
        method = api["method"].lower()
        if method == "get":
            mcp_code += f'        response = requests.get(url, params=params)\n'
        elif method in ["post", "put", "patch"]:
            mcp_code += f'        response = requests.{method}(url, params=params, json=payload)\n'
        elif method == "delete":
            mcp_code += f'        response = requests.delete(url, params=params)\n'
        else:
            mcp_code += f'        response = requests.request("{method.upper()}", url, params=params, json=payload)\n'
            
        mcp_code += f"""        response.raise_for_status()
        return response.json() if response.content else {{"status": "success"}}
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {{"error": "Resource not found"}}
        return {{"error": f"API error: {{response.status_code}} - {{response.text}}"}}
    except Exception as e:
        return {{"error": f"Failed to call API: {{str(e)}}"}}

"""

    mcp_code += """
# To use these tools in another FastMCP server, you can import `mcp` from this file.
# Example: from mcp_integration import mcp
"""
    mcp_file = os.path.join(base_path, "mcp_integration.py")
    with open(mcp_file, "w", encoding="utf-8") as f:
        f.write(mcp_code)
        
    print(f"  [OK] Generated MCP Integration Module: {mcp_file}")
