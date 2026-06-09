import asyncio
import os
import json
from crawler import crawl_documentation
from extractor import extract_api_details, llm_enhance_apis
from fastapi_builder import generate_fastapi_server
from mcp_builder import generate_mcp_tools
from utils import save_json, load_json
from dotenv import load_dotenv

# Load env variables for LLM keys if present
script_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(script_dir, ".env"))

def generate_mock_from_schema(schema, schemas_dict, visited=None):
    if visited is None:
        visited = set()
    if not isinstance(schema, dict):
        return None

    # Resolve $ref
    if "$ref" in schema:
        ref_path = schema["$ref"]
        ref_name = ref_path.split("/")[-1]
        if ref_name in visited:
            return None
        visited.add(ref_name)
        resolved = schemas_dict.get(ref_name)
        if resolved:
            val = generate_mock_from_schema(resolved, schemas_dict, visited)
            visited.remove(ref_name)
            return val
        visited.remove(ref_name)
        return None

    if "allOf" in schema:
        merged = {}
        for subschema in schema["allOf"]:
            sub_val = generate_mock_from_schema(subschema, schemas_dict, visited)
            if isinstance(sub_val, dict):
                merged.update(sub_val)
        return merged

    if "anyOf" in schema or "oneOf" in schema:
        subschemas = schema.get("anyOf") or schema.get("oneOf")
        if subschemas:
            for sub in subschemas:
                val = generate_mock_from_schema(sub, schemas_dict, visited)
                if val is not None:
                    return val
        return None

    type_ = schema.get("type")
    if isinstance(type_, list):
        non_null_types = [t for t in type_ if t != "null"]
        type_ = non_null_types[0] if non_null_types else None

    # Check for example or default
    if "example" in schema:
        return schema["example"]
    if "default" in schema:
        return schema["default"]

    if type_ == "object" or "properties" in schema:
        obj = {}
        properties = schema.get("properties", {})
        for prop_name, prop_schema in properties.items():
            obj[prop_name] = generate_mock_from_schema(prop_schema, schemas_dict, visited)
        return obj
    elif type_ == "array":
        items = schema.get("items", {})
        item_val = generate_mock_from_schema(items, schemas_dict, visited)
        return [item_val] if item_val is not None else []
    elif type_ == "string":
        if "format" in schema:
            fmt = schema["format"]
            if fmt == "date-time":
                return "2026-06-09T22:59:46Z"
            elif fmt == "date":
                return "2026-06-09"
            elif fmt == "uuid":
                return "123e4567-e89b-12d3-a456-426614174000"
            elif fmt == "uri" or fmt == "url":
                return "https://example.com"
        if "enum" in schema and schema["enum"]:
            return schema["enum"][0]
        return "string"
    elif type_ == "integer":
        return 0
    elif type_ == "number":
        return 0.0
    elif type_ == "boolean":
        return True

    return None

async def main():
    print("========================================")
    print(" FastAPI Mock Server Generator from Docs")
    print("========================================\n")
    # Prompt user for source (URL, file path, or description) and server name
    raw_source = input("Enter docs URL, local file path, or a text description: ").strip()
    # Remove surrounding quotes if the user supplied a quoted path
    source = raw_source.strip('"\'')
    server_name = input("Enter output server name: ").strip()

    os.makedirs("intermediate_results", exist_ok=True)

    extracted_apis = []
    json_loaded = False

    # If the source is a local JSON file containing API definitions, load it directly
    if source.lower().endswith('.json') and os.path.isfile(source):
        print("\n[1/4] Detected JSON file. Loading APIs from file...")
        # Load the OpenAPI spec and convert to our internal API format
        spec = load_json(source) or {}
        extracted_apis = []
        if isinstance(spec, dict) and "paths" in spec:
            schemas_dict = spec.get("components", {}).get("schemas", {})
            for path, methods in spec["paths"].items():
                if not isinstance(methods, dict):
                    continue
                for method, details in methods.items():
                    if method.lower() not in ["get", "post", "put", "delete", "options", "head", "patch", "trace"]:
                        continue
                    if not isinstance(details, dict):
                        continue
                    api_entry = {
                        "method": method.upper(),
                        "path": path,
                        "function_name": details.get("operationId") or f"{method}_{path}".replace('/', '_').replace('{', '').replace('}', ''),
                        "request_body": {},
                        "response_body": {},
                        "tool_name": details.get("operationId"),
                        "tool_description": details.get("description", f"Calls {method.upper()} {path}"),
                    }
                    # Extract example request/response if available
                    if "requestBody" in details and isinstance(details["requestBody"], dict):
                        content = details["requestBody"].get("content", {})
                        for schema in content.values():
                            if isinstance(schema, dict) and "schema" in schema:
                                mock_val = generate_mock_from_schema(schema["schema"], schemas_dict)
                                if mock_val is not None:
                                    api_entry["request_body"] = mock_val
                                    break
                    if "responses" in details and isinstance(details["responses"], dict):
                        resp = details["responses"].get("200") or details["responses"].get("default")
                        if isinstance(resp, dict):
                            content = resp.get("content", {})
                            for schema in content.values():
                                if isinstance(schema, dict) and "schema" in schema:
                                    mock_val = generate_mock_from_schema(schema["schema"], schemas_dict)
                                    if mock_val is not None:
                                        api_entry["response_body"] = mock_val
                                        break
                    extracted_apis.append(api_entry)
        else:
            # Fallback: assume file already contains list of APIs
            extracted_apis = spec
        json_loaded = True
        print(f"[OK] Loaded {len(extracted_apis)} APIs from JSON file.")
    elif not source.startswith("http") and not os.path.exists(source):
        # Treat as a text description
        print("\n[1/4] Input recognized as a text description. Bypassing crawler...")
        crawled_pages = [{"url": "User Description", "text": source}]
    else:
        # 1. Crawler (HTTPX + Playwright)
        print("\n[1/4] Crawling documentation...")
        crawled_pages = await crawl_documentation(source)
        save_json(crawled_pages, "intermediate_results/crawled_pages.json")
        print(f"[OK] Crawled {len(crawled_pages)} pages.")

    # 2. Extraction (LLM) – only if not loading from JSON
    if not json_loaded:
        print("\n[2/4] Extracting API details (LLM)...")
        extracted_apis = await extract_api_details(crawled_pages)
    else:
        print("\n[2/4] Skipping LLM extraction (JSON input).")
    
    # 3. LLM Enhancer for Data Payloads – only if not loading from JSON
    if not json_loaded:
        print("\n[3/4] Enhancing API payloads...")
        extracted_apis = await llm_enhance_apis(extracted_apis, server_name)
    else:
        print("\n[3/4] Skipping LLM enhancement (JSON input).")

    # Save Intermediate Results (Improvement #6)
    save_json(extracted_apis, "intermediate_results/extracted_apis.json")
    print(f"[OK] Extracted {len(extracted_apis)} APIs in total.")

    if not extracted_apis:
        print("\n[ERROR] No APIs found. Exiting.")
        return

    servers_dir = os.path.join(script_dir, "servers")
    # 4. Generate Server + Pydantic Models + Routes + MCP Tools
    print("\n[4/4] Generating FastAPI server and MCP Tools...")
    generate_fastapi_server(
        server_name=server_name,
        api_data=extracted_apis,
        output_folder=servers_dir
    )
    generate_mcp_tools(
        server_name=server_name,
        api_data=extracted_apis,
        output_folder=servers_dir
    )

    print(f"\n[DONE] Server generated successfully in servers/{server_name}")
    print("\nTo run the generated servers:")
    print(f"  cd servers/{server_name}")
    print("  pip install -r requirements.txt")
    print("  Terminal 1: uvicorn main:app --reload --port 8000")
    print("  Terminal 2: python mcp_server.py")


if __name__ == "__main__":
    asyncio.run(main())
