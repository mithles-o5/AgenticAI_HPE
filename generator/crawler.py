import httpx
import asyncio
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque
from playwright.async_api import async_playwright

visited = set()

def is_relevant_url(base_url, target_url):
    base_parsed = urlparse(base_url)
    target_parsed = urlparse(target_url)
    if base_parsed.netloc != target_parsed.netloc:
        return False
        
    # If it's an SPA (has fragment), only crawl links on the exact same path
    if base_parsed.fragment:
        return base_parsed.path == target_parsed.path
        
    base_path = base_parsed.path
    if not base_path.endswith('/'):
        if '/' in base_path:
            base_path = base_path.rsplit('/', 1)[0] + '/'
        else:
            base_path = '/'
    return target_parsed.path.startswith(base_path)

async def fetch_page_httpx(client, url):
    """ Improve 4: Async Crawling """
    try:
        response = await client.get(url, follow_redirects=True)
        if response.status_code == 200:
            return response.text
    except Exception as e:
        pass
    return None

async def fetch_page_playwright(url, browser):
    """ Improve 5: Playwright Support for dynamic JS rendering """
    try:
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(url, wait_until="domcontentloaded", timeout=20000)
        await asyncio.sleep(1.5) # Give extra time for JS frameworks to place content
        content = await page.content()
        await context.close()
        return content
    except Exception as e:
        print(f"    Playwright Error crawling {url}: {e}")
    return None

async def crawl_documentation(start_url, max_pages=50):
    if not start_url.startswith("http"):
        # Local HTML/Markdown doc file
        try:
            with open(start_url, "r", encoding="utf-8") as f:
                content = f.read()
                soup = BeautifulSoup(content, "lxml")
                return [{
                    "url": start_url,
                    "html": content,
                    "text": soup.get_text(separator="\n")
                }]
        except Exception as e:
            print(f"Error reading local file: {e}")
            return []

    queue = deque([start_url])
    pages = []
    
    # Keep one browser open for the entire crawl to be faster
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        async with httpx.AsyncClient(verify=False, timeout=15) as client:
            while queue and len(visited) < max_pages:
                current_url = queue.popleft()
                if current_url in visited:
                    continue
                
                visited.add(current_url)

                is_js_rendered = False
                
                # Single Page Applications use '#' for routing
                # if there is a hash route, the server returns the same HTML
                # every time. We MUST use Playwright to actually execute the router.
                if "#" in current_url and current_url.split("#")[-1] != "":
                    is_js_rendered = True

                html_content = None
                if not is_js_rendered:
                    html_content = await fetch_page_httpx(client, current_url)
                    
                    if html_content:
                        soup = BeautifulSoup(html_content, "lxml")
                        body = soup.find("body")
                        if body and len(body.get_text(strip=True)) < 300: 
                            is_js_rendered = True
                    else:
                        is_js_rendered = True

                if is_js_rendered:
                    html_content = await fetch_page_playwright(current_url, browser)
                    if not html_content:
                        continue
                        
                soup = BeautifulSoup(html_content, "lxml")
                
                text_content = soup.get_text(separator="\n")
                pages.append({
                    "url": current_url,
                    "html": html_content,
                    "text": text_content
                })

                # Extract internal links
                for link in soup.find_all("a", href=True):
                    href = link["href"]
                    full_url = urljoin(current_url, href)

                    if is_relevant_url(start_url, full_url) and full_url not in visited:
                        queue.append(full_url)
                        
                await asyncio.sleep(0.05)
                
                if len(pages) % 5 == 0:
                    print(f"  ...Crawled {len(pages)} pages")

        await browser.close()
        
    return pages
