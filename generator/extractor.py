import os
import json

# pyrefly: ignore [missing-import]
from slugify import slugify

async def extract_api_details(crawled_pages):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("[ERROR] GEMINI_API_KEY is required for accurate API extraction.")
        return []
        
    try:
        from google import genai
        from google.genai import types
        client = genai.Client(api_key=api_key)
    except Exception as e:
        print(f"[!] Failed to initialize Gemini: {e}")
        return []

    api_results = []
    print(f"\n[LLM Extractor] Analyzing {len(crawled_pages)} pages in a single batch...")

    all_text = ""
    for page in crawled_pages:
        text = page.get("text", "")
        url = page.get("url", "Unknown")
        if text and len(text) > 50:
            all_text += f"\n--- Source: {url} ---\n{text}"
            
    if not all_text:
        return []

    prompt = f"""
    Extract all API endpoints explicitly mentioned in the following documentation text.
    We want to create a mock server and generate MCP tool definitions for these APIs.
    
    Return ONLY a valid JSON array of objects, where each object has:
    - "method": "GET", "POST", "PUT", "PATCH", or "DELETE"
    - "path": the API path (e.g., "/api/v1/resource")
    - "request_body": a realistic JSON object for the request body (empty {{}} if none). DO NOT use string literal "string", use actual realistic mock values (e.g. "John Doe", "active").
    - "response_body": a realistic JSON object for the response body (empty {{}} if none). MUST be a deep realistic object, not just "string".
    - "tool_name": a snake_case name for the MCP tool
    - "tool_description": a short description of what the API does
    
    If no explicit APIs are found, return []. Do not include markdown blocks like ```json.
    
    Documentation Text:
    {all_text[:400000]}
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(response_mime_type="application/json")
        )
        
        result_str = response.text.strip()
        data = json.loads(result_str)
        
        if isinstance(data, list):
            for item in data:
                if "method" in item and "path" in item:
                    func_name = slugify(f"{item['method']}_{item['path']}").replace("-", "_")
                    item["function_name"] = func_name
                    item["source_url"] = "Batch Extracted"
                    if not item.get("tool_name"):
                        item["tool_name"] = func_name
                    if not item.get("tool_description"):
                        item["tool_description"] = f"Calls {item['method']} {item['path']}"
                    api_results.append(item)
    except Exception as e:
        print(f"      [!] Error during LLM extraction: {e}")

    # Deduplicate by method and path
    unique_apis = []
    seen = set()
    for api in api_results:
        key = (api["method"].upper(), api["path"])
        if key not in seen:
            seen.add(key)
            unique_apis.append(api)

    return unique_apis

async def llm_enhance_apis(extracted_apis, server_name):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or not extracted_apis:
        return extracted_apis

    try:
        from google import genai
        from google.genai import types
        client = genai.Client(api_key=api_key)
    except Exception as e:
        print(f"[!] Failed to initialize Gemini for enhancement: {e}")
        return extracted_apis

    print(f"\n[LLM Enhancer] Enhancing {len(extracted_apis)} APIs with realistic payloads for '{server_name}'...")

    prompt = f"""
    You are an expert API designer. I have a list of extracted API endpoints for a mock server named "{server_name}".
    Some of these APIs might have empty, generic, or invalid request_body or response_body (like just the word "string").
    Your task is to REWRITE the `request_body` and `response_body` with HIGHLY REALISTIC, deeply nested JSON data appropriate for an API related to "{server_name}".
    - DO NOT use generic types like "string" or 0. Use actual mock values (e.g., "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6", "status": "running", "createdAt": "2025-09-10T18:22:24Z").
    - If a response is an array, provide an array with at least 2 realistic objects.
    Leave method, path, function_name, and tool_name intact.
    Return the entire list as a valid JSON array of objects.
    
    Current APIs:
    {json.dumps(extracted_apis, indent=2)}
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(response_mime_type="application/json")
        )
        
        enhanced_apis = json.loads(response.text.strip())
        if isinstance(enhanced_apis, list) and len(enhanced_apis) > 0:
            # Re-ensure some required fields are still there just in case the LLM dropped them
            for api in enhanced_apis:
                if "function_name" not in api and "method" in api and "path" in api:
                    api["function_name"] = slugify(f"{api['method']}_{api['path']}").replace("-", "_")
            print("  [OK] Successfully enhanced API payloads.")
            return enhanced_apis
    except Exception as e:
        print(f"  [!] Error during LLM enhancement: {e}")
        
    return extracted_apis
