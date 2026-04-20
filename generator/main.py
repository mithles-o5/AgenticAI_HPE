import asyncio
import os
import json
from crawler import crawl_documentation
from extractor import extract_api_details, llm_enhance_apis
from fastapi_builder import generate_fastapi_server
from openapi_parser import detect_and_parse_openapi
from utils import save_json, load_json
from dotenv import load_dotenv

# Load env variables for LLM keys if present
script_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(script_dir, ".env"))

async def main():
    print("========================================")
    print(" FastAPI Mock Server Generator from Docs")
    print("========================================\n")
    source = input("Enter documentation URL or local file path: ").strip()
    server_name = input("Enter output server name: ").strip()

    os.makedirs("intermediate_results", exist_ok=True)

    extracted_apis = []

    # 1. Try OpenAPI / Swagger first
    print("\n[1/4] Detecting OpenAPI/Swagger specifications...")
    extracted_apis = await detect_and_parse_openapi(source)
    
    if extracted_apis:
        print(f"✅ Detected structured OpenAPI/Swagger specification. Found {len(extracted_apis)} endpoints.")
    else:
        print("❌ OpenAPI not detected. Falling back to HTML/JS crawler.")
        
        # 2 & 3. Crawler (HTTPX + Playwright fallback)
        print("\n[2/4] Crawling documentation...")
        crawled_pages = await crawl_documentation(source)
        save_json(crawled_pages, "intermediate_results/crawled_pages.json")
        print(f"✅ Crawled {len(crawled_pages)} pages.")

        # 4. Extraction (Regex + LLM fallback)
        print("\n[3/4] Extracting API details (Regex + LLM fallback)...")
        extracted_apis = await extract_api_details(crawled_pages)
    
    # 4.5 LLM Enhancer for Data Payloads
    extracted_apis = await llm_enhance_apis(extracted_apis, server_name)

    # Save Intermediate Results (Improvement #6)
    save_json(extracted_apis, "intermediate_results/extracted_apis.json")
    print(f"✅ Extracted {len(extracted_apis)} APIs in total.")

    if not extracted_apis:
        print("\n❌ No APIs found. Exiting.")
        return

    # 5. Generate Server + Pydantic Models + Routes
    print("\n[4/4] Generating FastAPI server and Mock data...")
    generate_fastapi_server(
        server_name=server_name,
        api_data=extracted_apis,
        output_folder="servers"
    )

    print(f"\n🎉 Server generated successfully in servers/{server_name}")
    print("\nTo run the generated server:")
    print(f"  cd servers/{server_name}")
    print("  pip install -r requirements.txt")
    print("  uvicorn main:app --reload")


if __name__ == "__main__":
    asyncio.run(main())
