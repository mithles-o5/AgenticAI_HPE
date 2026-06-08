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

async def main():
    print("========================================")
    print(" FastAPI Mock Server Generator from Docs")
    print("========================================\n")
    source = input("Enter docs URL, local file path, or a text description: ").strip()
    server_name = input("Enter output server name: ").strip()

    os.makedirs("intermediate_results", exist_ok=True)

    extracted_apis = []

    if not source.startswith("http") and not os.path.exists(source):
        # Treat as a text description
        print("\n[1/4] Input recognized as a text description. Bypassing crawler...")
        crawled_pages = [{"url": "User Description", "text": source}]
    else:
        # 1. Crawler (HTTPX + Playwright)
        print("\n[1/4] Crawling documentation...")
        crawled_pages = await crawl_documentation(source)
        save_json(crawled_pages, "intermediate_results/crawled_pages.json")
        print(f"[OK] Crawled {len(crawled_pages)} pages.")

    # 2. Extraction (LLM)
    print("\n[2/4] Extracting API details (LLM)...")
    extracted_apis = await extract_api_details(crawled_pages)
    
    # 3. LLM Enhancer for Data Payloads
    print("\n[3/4] Enhancing API payloads...")
    extracted_apis = await llm_enhance_apis(extracted_apis, server_name)

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
