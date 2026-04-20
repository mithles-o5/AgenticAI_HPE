import httpx
import json
import yaml
import asyncio
from urllib.parse import urljoin
from slugify import slugify
from playwright.async_api import async_playwright

async def detect_and_parse_openapi(base_url):
    """
    Improvement 1: OpenAPI / Swagger Detection
    Checks common paths for structured specs, and also sniffs the network
    load of the page for dynamically loaded Swagger/OpenAPI configs.
    """
    common_paths = [
        "",
        "/swagger.json",
        "/openapi.json",
        "/v3/api-docs",
        "/api-docs",
        "/openapi.yaml",
        "/swagger.yaml"
    ]
    
    if not base_url.startswith("http"):
        # Local file
        try:
            with open(base_url, "r", encoding="utf-8") as f:
                if base_url.endswith((".yaml", ".yml")):
                    spec = yaml.safe_load(f)
                else:
                    spec = json.load(f)
            return parse_openapi_spec(spec, base_url)
        except Exception:
            return None

    # URL - Check standard paths
    async with httpx.AsyncClient(verify=False, timeout=10) as client:
        for path in common_paths:
            test_url = urljoin(base_url, path) if path else base_url
            try:
                response = await client.get(test_url, follow_redirects=True)
                if response.status_code == 200:
                    try:
                        spec = response.json()
                        if isinstance(spec, dict) and ("openapi" in spec or "swagger" in spec):
                            print(f"  -> Found OpenAPI JSON spec at {test_url}")
                            return parse_openapi_spec(spec, test_url)
                    except json.JSONDecodeError:
                        try:
                            spec = yaml.safe_load(response.text)
                            if isinstance(spec, dict) and ("openapi" in spec or "swagger" in spec):
                                print(f"  -> Found OpenAPI YAML spec at {test_url}")
                                return parse_openapi_spec(spec, test_url)
                        except Exception:
                            pass
            except Exception:
                continue

    # Advanced detection: Sniff network for JS-loaded openAPI JSONs
    print("  -> Checking for dynamically-loaded JSON specifications...")
    sniffed_spec = None
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()

            def find_openapi_spec(d):
                if isinstance(d, dict):
                    if "paths" in d and ("openapi" in d or "swagger" in d):
                        return d
                    for k, v in d.items():
                        found = find_openapi_spec(v)
                        if found: return found
                elif isinstance(d, list):
                    for item in d:
                        found = find_openapi_spec(item)
                        if found: return found
                return None

            async def check_response(response):
                nonlocal sniffed_spec
                try:
                    if response.status == 200:
                        content_type = response.headers.get("content-type", "")
                        if "json" in content_type:
                            data = await response.json()
                            spec = find_openapi_spec(data)
                            if spec:
                                print(f"  -> Intercepted nested OpenAPI payload from network: {response.url}")
                                sniffed_spec = spec
                except Exception:
                    pass

            page.on("response", check_response)
            await page.goto(base_url, wait_until="networkidle", timeout=15000)
            await asyncio.sleep(2) # Give extra time for async JSON fetch
            await context.close()
            await browser.close()
    except Exception as e:
        pass

    if sniffed_spec:
        return parse_openapi_spec(sniffed_spec, base_url)

    return None

def generate_dummy_from_schema(schema, spec, depth=0):
    if depth > 5 or not isinstance(schema, dict):
        return None
        
    if "$ref" in schema:
        ref_path = schema["$ref"].split("/")
        curr = spec
        for p in ref_path[1:]:
            curr = curr.get(p, {})
        return generate_dummy_from_schema(curr, spec, depth+1)
        
    if "allOf" in schema:
        obj = {}
        for sub in schema["allOf"]:
            sub_dummy = generate_dummy_from_schema(sub, spec, depth+1)
            if isinstance(sub_dummy, dict):
                obj.update(sub_dummy)
        return obj

    if "properties" in schema or schema.get("type") == "object":
        obj = {}
        for k, v in schema.get("properties", {}).items():
            obj[k] = generate_dummy_from_schema(v, spec, depth+1)
        return obj
        
    sys_type = schema.get("type")
    if sys_type == "array":
        item = generate_dummy_from_schema(schema.get("items", {}), spec, depth+1)
        return [item] if item is not None else []
    elif sys_type == "string":
        return schema.get("example", "string")
    elif sys_type == "integer" or sys_type == "number":
        return schema.get("example", 0)
    elif sys_type == "boolean":
        return schema.get("example", True)
        
    return schema.get("example", "dummy")

def parse_openapi_spec(spec, source_url):
    api_results = []
    paths = spec.get("paths", {})
    
    for path, path_item in paths.items():
        if not isinstance(path_item, dict):
            continue
        for method, operation in path_item.items():
            if method.lower() not in ["get", "post", "put", "patch", "delete"]:
                continue
                
            function_name = operation.get("operationId", slugify(f"{method}_{path}").replace("-", "_"))
            
            # Request body extraction
            request_body = {}
            if "requestBody" in operation:
                try:
                    content = operation["requestBody"].get("content", {})
                    if content:
                        req_content_type = next(iter(content))
                        schema = content[req_content_type].get("schema", {})
                        if "example" in schema:
                            request_body = schema["example"]
                        elif "example" in content[req_content_type]:
                            request_body = content[req_content_type]["example"]
                        else:
                            request_body = generate_dummy_from_schema(schema, spec)
                except Exception:
                    pass

            # Response body extraction
            response_body = {}
            if "responses" in operation:
                success_code = next((str(code) for code in operation["responses"] if str(code).startswith(("2", "3"))), None)
                if success_code:
                    try:
                        resp_content = operation["responses"][success_code].get("content", {})
                        if resp_content:
                            resp_content_type = next(iter(resp_content))
                            schema = resp_content[resp_content_type].get("schema", {})
                            if "example" in schema:
                                response_body = schema["example"]
                            elif "examples" in schema:
                                response_body = next(iter(schema["examples"].values()))
                            elif "example" in resp_content[resp_content_type]:
                                response_body = resp_content[resp_content_type]["example"]
                            else:
                                response_body = generate_dummy_from_schema(schema, spec)
                    except Exception:
                        pass

            # Parameters extraction
            parameters = []
            if "parameters" in operation:
                for param in operation["parameters"]:
                    if isinstance(param, dict) and "name" in param:
                        parameters.append({
                            "name": param["name"],
                            "in": param.get("in", "query"),
                            "required": param.get("required", False)
                        })

            api_results.append({
                "method": method.upper(),
                "path": path,
                "function_name": function_name,
                "parameters": parameters,
                "request_body": request_body if request_body else {},
                "response_body": response_body if response_body else {},
                "source_url": source_url
            })
            
    return api_results
