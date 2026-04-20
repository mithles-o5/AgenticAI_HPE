import re
import os
import json
from slugify import slugify

HTTP_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE"]

async def llm_assisted_extraction(text_chunk):
    """
    Improvement 2: LLM-Assisted Extraction
    Uses google-genai to parse malformed text blocks if regex fails.
    Requires GEMINI_API_KEY environment variable.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None
        
    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        
        prompt = f"""
        Extract the API details from the following documentation text.
        Return ONLY valid JSON in the exact following format, without markdown formatting or code blocks:
        {{
            "method": "GET/POST/PUT/etc",
            "path": "/api/v1/resource",
            "request_body": {{"key": "value"}},
            "response_body": {{"key": "value"}}
        }}
        If multiple APIs are present, extract the first one. If no clear API is found, return empty JSON {{}}.
        
        Documentation Text:
        {text_chunk}
        """
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        result = response.text.strip()
        if result.startswith("```json"):
            result = result[7:-3].strip()
        elif result.startswith("```"):
            result = result[3:-3].strip()
            
        return json.loads(result)
    except Exception as e:
        return None

async def extract_api_details(crawled_pages):
    api_results = []
    
    endpoint_pattern = re.compile(
        r"\b(GET|POST|PUT|PATCH|DELETE)\b\s*(/[a-zA-Z0-9_\-\.\/\{\}]+)",
        re.IGNORECASE
    )

    json_pattern = re.compile(r"\{.*?\}", re.DOTALL)

    for page in crawled_pages:
        text = page["text"]
        endpoints = endpoint_pattern.findall(text)

        for method, path in endpoints:
            start_idx = max(0, text.find(path) - 500)
            end_idx = text.find(path) + 1500
            nearby_text = text[start_idx:end_idx]
            
            possible_json = json_pattern.findall(nearby_text)
            
            request_body = {}
            response_body = {}

            if len(possible_json) >= 1:
                try:
                    request_body = json.loads(possible_json[0])
                except Exception:
                    request_body = possible_json[0]

            if len(possible_json) >= 2:
                try:
                    response_body = json.loads(possible_json[1])
                except Exception:
                    response_body = possible_json[1]

            # LLM Fallback for bad regex results
            if not request_body and not response_body and os.getenv("GEMINI_API_KEY"):
                llm_data = await llm_assisted_extraction(nearby_text)
                if llm_data and "path" in llm_data:
                    method = llm_data.get("method", method)
                    path = llm_data.get("path", path)
                    request_body = llm_data.get("request_body", {})
                    response_body = llm_data.get("response_body", {})

            # Ensure we serialize properly if string
            if isinstance(request_body, str):
                try:
                    request_body = json.loads(request_body)
                except Exception:
                    request_body = {}

            if isinstance(response_body, str):
                try:
                    response_body = json.loads(response_body)
                except Exception:
                    response_body = {}

            # avoid duplicates
            if not any(a["method"].upper() == method.upper() and a["path"] == path for a in api_results):
                api_results.append({
                    "method": method.upper(),
                    "path": path,
                    "function_name": slugify(f"{method}_{path}").replace("-", "_"),
                    "request_body": request_body,
                    "response_body": response_body,
                    "source_url": page["url"]
                })

    return api_results

async def llm_enhance_apis(api_results, server_name):
    """
    Enhancement: Post-processing step to use Gemini to hallucinate payloads.
    Updated to use BATCH PROCESSING to avoid 429 Rate Limits!
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return api_results

    try:
        from google import genai
        from google.genai import types
        client = genai.Client(api_key=api_key)
    except Exception as e:
        print("Failed to initialize Gemini:", e)
        return api_results

    apis_to_enhance = [api for api in api_results if not api["response_body"]]
    if not apis_to_enhance:
        return api_results
        
    print(f"\n[LLM Enhancer] Generating realistic mock data for {len(apis_to_enhance)} endpoints in bulk. This avoids rate limits...")
    
    # We will ask the LLM to return a dictionary mapping `METHOD /path` to payloads
    endpoints_list_str = "\n".join([f"- {a['method']} {a['path']}" for a in apis_to_enhance])
    
    prompt = f"""
    You are an expert API developer system working on an API specification for "{server_name}".
    I have a list of API endpoints that need realistic JSON mock payloads.
    
    For each endpoint, generate a professional, realistic full JSON payload for the response body. If the method is POST, PUT, or PATCH, also generate a realistic request body.
    
    Endpoints:
    {endpoints_list_str}
    
    Return ONLY a valid, parseable JSON object mapping each endpoint string literal (e.g. "GET /api/v1/users") to its generated payloads.
    Format your response exactly like this, with no markdown codeblocks:
    {{
      "GET /data-services/v1beta1/async-operations": {{
          "request_body": {{}},
          "response_body": {{"id": "123", "status": "COMPLETED"}}
      }}
    }}
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(response_mime_type="application/json")
        )
        
        result_str = response.text.strip()
        data_map = json.loads(result_str)
        
        # Apply the generated data back to our api_results
        for api in api_results:
            key = f"{api['method']} {api['path']}"
            if key in data_map:
                enhanced = data_map[key]
                if not api["request_body"] and "request_body" in enhanced:
                    api["request_body"] = enhanced["request_body"]
                if not api["response_body"] and "response_body" in enhanced:
                    api["response_body"] = enhanced["response_body"]
                    
        print(f"      ✅ Successfully enhanced payloads in bulk!")
    except Exception as e:
        print(f"      [!] Error during bulk LLM enhancement: {e}")
                
    # New Fallback Layer imported from mock_data_fallback.py
    try:
        from mock_data_fallback import apply_template_fallbacks
        api_results = apply_template_fallbacks(api_results)
    except ImportError:
        pass
        
    return api_results
