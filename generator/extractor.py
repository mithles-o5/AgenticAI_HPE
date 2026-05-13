import os
import json
import asyncio
import time

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
    seen_lengths = set()
    for page in crawled_pages:
        text = page.get("text", "")
        url = page.get("url", "Unknown")
        
        # Aggressive Deduplication: SPAs often change tiny parts of the DOM (like 'active' classes),
        # causing exact text matches to fail and duplicating massive pages.
        # If the text length is within 2% of a page we've already seen, discard it as a duplicate.
        is_dup = False
        for slen in seen_lengths:
            if abs(len(text) - slen) / max(slen, 1) < 0.02:
                is_dup = True
                break
                
        if text and len(text) > 50 and not is_dup:
            seen_lengths.add(len(text))
            all_text += f"\n--- Source: {url} ---\n{text}"
            
    if not all_text:
        return []

    # Chunk the text to prevent the LLM from hitting its output token limit on massive docs
    chunk_size = 300000
    text_chunks = [all_text[i:i+chunk_size] for i in range(0, len(all_text), chunk_size)]
    
    print(f"  -> Split text into {len(text_chunks)} chunks to prevent extraction limits.")

    def process_chunk_sync(idx, chunk):
        print(f"  -> Sending chunk {idx + 1}/{len(text_chunks)} to LLM...")
        local_results = []
        prompt = f"""
        Extract EVERY SINGLE API endpoint explicitly mentioned in the following documentation text.
        Make absolutely sure to be exhaustive and do not skip, summarize, or omit any endpoints.
        We want to create a mock server and generate MCP tool definitions for all of these APIs.
        
        Return ONLY a valid JSON array of objects, where each object has:
        - "method": "GET", "POST", "PUT", "PATCH", or "DELETE"
        - "path": the API path (e.g., "/api/v1/resource")
        - "request_body": a realistic JSON object for the request body (empty {{}} if none). DO NOT use string literal "string", use actual realistic mock values (e.g. "John Doe", "active").
        - "response_body": a realistic JSON object for the response body (empty {{}} if none). MUST be a deep realistic object, not just "string".
        - "tool_name": a snake_case name for the MCP tool
        - "tool_description": a short description of what the API does
        
        If no explicit APIs are found, return []. Do not include markdown blocks like ```json.
        
        Documentation Text:
        {chunk}
        """
        
        max_retries = 5
        for attempt in range(max_retries):
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
                            local_results.append(item)
                # Success, break out of retry loop
                break
            except Exception as e:
                error_str = str(e)
                if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                    print(f"      [!] Rate limit hit on chunk {idx + 1}. Waiting 65s before retry (attempt {attempt+1}/{max_retries})...")
                    time.sleep(65)
                else:
                    print(f"      [!] Error during LLM extraction on chunk {idx + 1}: {e}")
                    break
            
        return local_results

    # Run chunks sequentially to strictly avoid hitting the 5 RPM limit on free tiers
    sem = asyncio.Semaphore(1)
    async def bound_process(idx, chunk):
        async with sem:
            # Small delay to stagger requests
            await asyncio.sleep(2)
            return await asyncio.to_thread(process_chunk_sync, idx, chunk)

    tasks = [bound_process(idx, chunk) for idx, chunk in enumerate(text_chunks)]
    results = await asyncio.gather(*tasks)
    
    for res in results:
        api_results.extend(res)

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
