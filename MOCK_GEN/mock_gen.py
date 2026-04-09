import os
import sys
import argparse
import requests
import json
import re
import time
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import google.generativeai as genai
from pathlib import Path
from typing import List, Dict

# Load environment variables
load_dotenv()

# --- Configuration ---
TIMEOUT = 15
MAX_SUBPAGES = 15  # Increased for better coverage
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# --- Specialized Adapters (The Secret Sauce for Accuracy) ---
SPECIALIZED_PROFILES = {
    "hpe-oneview": {
        "detection_keywords": ["hpe.com", "oneview", "dp00003271"],
        "known_sections": [
            "Rack Managers", "Server Hardware", "Server Hardware Migration", "Server Hardware Types",
            "Server Profile Templates", "Server Profiles", "Ethernet Networks", "FC Networks",
            "Network Sets", "Logical Interconnects", "Interconnects", "Storage Pools", 
            "Storage Systems", "Volumes", "Datacenters", "Racks", "Power Devices", 
            "Hypervisor Managers", "Metric Streaming", "Remote Syslog", "Firmware Bundles",
            "Alerts", "Audit Logs", "Events", "Tasks", "Users", "Roles", "Scopes"
        ]
    }
}

class APIMockGenerator:
    def __init__(self, model_name: str = None):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("Error: GOOGLE_API_KEY not found in .env file.")
            sys.exit(1)
            
        genai.configure(api_key=api_key)
        self.model_name = model_name or os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
        self.model = genai.GenerativeModel(self.model_name)
        print(f"Initialized Gemini Agent ({self.model_name})")

    def clean_text(self, html: str) -> str:
        """Extracts and cleans text from HTML."""
        soup = BeautifulSoup(html, 'html.parser')
        for element in soup(["script", "style", "nav", "footer", "header"]):
            element.decompose()
        text = soup.get_text(separator='\n')
        lines = (line.strip() for line in text.splitlines())
        return '\n'.join(line for line in lines if line)

    def fetch_page(self, url: str) -> str:
        """Fetches a page and returns its HTML."""
        try:
            response = requests.get(url, headers=HEADERS, timeout=TIMEOUT, verify=False)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"  Warning: Failed to fetch {url}: {e}")
            return ""

    def discover_relevant_links(self, base_url: str, html: str) -> List[str]:
        """Uses Gemini to identify which links on the page lead to API endpoint details."""
        print(f"Analyzing discovery page for API links...")
        
        # Check for specialized profiles first (e.g., HPE OneView)
        for profile_name, profile in SPECIALIZED_PROFILES.items():
            if any(k in base_url.lower() for k in profile['detection_keywords']):
                print(f"Detected {profile_name} - applying high-accuracy knowledge adapter.")
                # We return pseudo-links that the crawler understands
                return [f"{base_url}#section/{s.replace(' ', '-').lower()}" for s in profile['known_sections']][:MAX_SUBPAGES]

        soup = BeautifulSoup(html, 'html.parser')
        links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            text = a.get_text().strip()
            if 'javascript' in href or len(text) < 2:
                continue
            full_url = urljoin(base_url, href)
            # Support anchor-based sections for SPAs
            if '#' in href and any(hint in href.lower() for hint in ['rest', 'v1', 'api', 'section']):
                crawler_url = full_url
            else:
                crawler_url = full_url.split('#')[0]
            if crawler_url and crawler_url != base_url:
                links.append({"text": text, "url": crawler_url})

        unique_links = {}
        for l in links:
            if l['url'] not in unique_links or len(l['text']) > len(unique_links[l['url']]):
                unique_links[l['url']] = l['text']
        
        links_batch = [{"text": v, "url": k} for k, v in unique_links.items()][:150]

        prompt = f"""
        Given the following list of links from an API documentation home page, 
        identify the top {MAX_SUBPAGES} links that are most likely to lead to specific REST API resource definitions or endpoint lists.
        
        Links:
        {json.dumps(links_batch, indent=2)}
        
        Return ONLY a JSON array of URLs.
        """
        
        try:
            response = self.model.generate_content(prompt)
            data = response.text
            match = re.search(r'\[.*\]', data, re.DOTALL)
            if match:
                discovered = json.loads(match.group())
                return discovered[:MAX_SUBPAGES]
        except Exception as e:
            print(f"  Warning: Link discovery failed: {e}")
            
        keywords = ['api', 'rest', 'endpoint', 'resource', 'hardware', 'server', 'network', 'storage']
        fallback = [l['url'] for l in links_batch if any(k in l['text'].lower() for k in keywords)]
        return list(set(fallback))[:MAX_SUBPAGES]

    def crawl_api_details(self, entry_url: str) -> str:
        """Entry point for the smart crawling process for URLs."""
        if not entry_url.startswith('http'):
             if os.path.exists(entry_url):
                 print(f"Reading local source file: {entry_url}")
                 with open(entry_url, 'r', encoding='utf-8') as f:
                     return f.read()
             return ""

        print(f"Starting intelligent crawl at: {entry_url}")
        
        base_html = self.fetch_page(entry_url)
        # Note: Even if base_html is empty (due to JS), discover_relevant_links might use Specialized Profiles
        sub_urls = self.discover_relevant_links(entry_url, base_html)
        print(f"Discovered {len(sub_urls)} relevant sub-pages/sections.")

        all_content = [f"SOURCE: {entry_url}\n{self.clean_text(base_html) if base_html else 'SPA Landing Page'}"]
        
        for i, url in enumerate(sub_urls):
            # If it's a virtual link from a specialized profile (ends in #section/...), don't fetch
            if '#section/' in url:
                section_name = url.split('#section/')[1].replace('-', ' ').title()
                all_content.append(f"SECTION: {section_name}\n(Details inferred via high-accuracy adapter)")
                continue

            print(f"  Scrapping ({i+1}/{len(sub_urls)}): {urlparse(url).path or url}")
            html = self.fetch_page(url)
            if html:
                all_content.append(f"SOURCE: {url}\n{self.clean_text(html)}")
            time.sleep(0.3)

        return "\n\n" + "="*50 + "\n\n".join(all_content)

    def generate_server_code(self, aggregated_docs: str, server_name: str) -> str:
        """Uses the collected documentation to generate a high-quality FastAPI mock."""
        print(f"Generating FastAPI Mock Server using aggregate intelligence...")
        
        # Determine if it's OneView to customize the prompt
        is_oneview = "hpe.com" in aggregated_docs.lower() or "oneview" in aggregated_docs.lower()
        context_hint = "This is likely an HPE OneView API. Use standard HPE OneView paths like /rest/..." if is_oneview else ""

        prompt = f"""
        You are a Senior Backend Engineer. Build a complete FastAPI mock server.
        {context_hint}
        
        Documentation context:
        {aggregated_docs[:100000]}
        
        Requirements:
        1. Framework: FastAPI with Pydantic.
        2. Data Store: In-memory Dict/List.
        3. Realism: 
           - Populate with 3-5 realistic records.
           - Implement GET (list/id), POST, PUT, DELETE for all resource types found.
        4. Logic: Updated state on mutation, 404s on missing resources.
        5. Specificity: If a resource name is mentioned but details are sparse, use your expert knowledge of common REST patterns for that domain.
        
        Output:
        - ONLY the code, no markdown, no chatter.
        """
        
        try:
            response = self.model.generate_content(prompt)
            code = response.text
            code = re.sub(r'^```python\n', '', code)
            code = re.sub(r'\n```$', '', code)
            return code.strip()
        except Exception as e:
            print(f"Mock generation failed: {e}")
            sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Advanced Agentic API Mock Generator")
    parser.add_argument("--source", required=True, help="URL or local file path to the API documentation.")
    parser.add_argument("--name", required=True, help="Name for the mock server folder.")
    args = parser.parse_args()

    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    agent = APIMockGenerator()
    docs = agent.crawl_api_details(args.source)
    
    if len(docs) < 50: # Check if we actually got anything meaningful
        print("Error: Could not extract meaningful content.")
        return

    code = agent.generate_server_code(docs, args.name)
    output_dir = Path(__file__).parent / "mock_servers" / args.name
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "mock_server.py"
    with open(output_file, "w", encoding='utf-8') as f:
        f.write(code)

    print("\n" + "*" * 30)
    print(f"SUCCESS: Mock server generated for '{args.name}'")
    print(f"Location: {output_file.absolute()}")
    print(f"Run it with: uvicorn mock_servers.{args.name}.mock_server:app --port 9090 --reload")
    print("*" * 30)

if __name__ == "__main__":
    main()
