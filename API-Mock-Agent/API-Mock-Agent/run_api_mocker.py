"""
run_api_mocker.py
Entry point for the API Mocker — crawl any API docs URL and start a mock server.

Usage
─────
  # Crawl any API documentation and start mock server on port 8080
  python run_api_mocker.py \\
      --url https://petstore.swagger.io/

  # Only crawl (don't start server)
  python run_api_mocker.py --url <url> --crawl-only

  # Only serve (use previously crawled data)
  python run_api_mocker.py --serve-only --port 8080
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
import sys
from pathlib import Path

import uvicorn
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("api-mocker")


# ── CLI ──────────────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="API Mocker — crawl API docs and generate a mock server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument(
        "--url",
        default=None,
        help="URL of the API documentation page to crawl and mock",
    )
    p.add_argument(
        "--output-dir",
        default="output",
        help="Directory to save crawl results (default: output/)",
    )
    p.add_argument(
        "--port",
        type=int,
        default=int(os.getenv("MOCK_SERVER_PORT", "8080")),
        help="Port for the mock server (default: 8080)",
    )
    p.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host for the mock server (default: 0.0.0.0)",
    )
    p.add_argument(
        "--instances",
        type=int,
        default=3,
        metavar="N",
        help="Number of sample items per collection in mock responses (default: 3).\n"
             "  Use 1 for minimal data, 10-50 for realistic load testing.",
    )
    p.add_argument(
        "--batch-size",
        type=int,
        default=5,
        help="Number of API sections to process per LLM call (default: 5)",
    )
    p.add_argument(
        "--provider",
        default=os.getenv("LLM_PROVIDER", None),
        choices=["groq", "gemini", "ollama", "huggingface", "anthropic"],
        help="LLM provider (default: auto-detect). FREE options: groq, gemini, ollama, huggingface",
    )
    p.add_argument(
        "--model",
        default=None,
        help="Override the default model for the chosen provider",
    )
    p.add_argument(
        "--list-providers",
        action="store_true",
        help="Show all supported LLM providers and exit",
    )
    p.add_argument(
        "--crawl-only",
        action="store_true",
        help="Only crawl — don't start the mock server",
    )
    p.add_argument(
        "--serve-only",
        action="store_true",
        help="Only serve — use previously crawled data",
    )
    return p.parse_args()


# ── Helpers ──────────────────────────────────────────────────────────────────

def _extract_api_title(url: str) -> str:
    """Derive a human-readable API title from the documentation URL."""
    from urllib.parse import urlparse
    parsed = urlparse(url)
    host = parsed.hostname or "API"
    # Remove common prefixes
    for prefix in ("www.", "docs.", "api.", "developer.", "support."):
        if host.startswith(prefix):
            host = host[len(prefix):]
    # Take the domain name and capitalize
    domain = host.split(".")[0].title()
    return f"{domain} API"


# ── Crawl pipeline ───────────────────────────────────────────────────────────

async def run_crawler(
    url: str,
    output_dir: str,
    batch_size: int,
    instance_count: int = 3,
    provider: str | None = None,
    model: str | None = None,
) -> dict:
    """Run the LangGraph API crawler and save results."""
    from api_mocker.graph import build_api_crawler_graph

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Progress callback prints to console
    async def on_progress(msg: str) -> None:
        print(f"  {msg}")

    graph = build_api_crawler_graph(
        progress_callback=on_progress,
        provider=provider,
        model=model,
    )

    # Initial state
    initial_state = {
        "messages": [],
        "source_url": url,
        "sections_discovered": [],
        "current_batch_idx": 0,
        "batch_size": batch_size,
        "instance_count": instance_count,
        "discovered_endpoints": [],
        "mock_data": {},
        "status": "discovering",
        "errors": [],
        "progress_log": [],
    }

    print("\n  ╔══════════════════════════════════════════════════════╗")
    print("  ║           API Mocker — LangGraph Crawler            ║")
    print("  ╠══════════════════════════════════════════════════════╣")
    print(f"  ║  Source     →  {url[:39]:<39}║")
    print(f"  ║  Output     →  {str(output_path):<39}║")
    print(f"  ║  Batch      →  {batch_size} sections per LLM call{' ' * 17}║")
    print(f"  ║  Instances  →  {instance_count} sample items per collection{' ' * (10 - len(str(instance_count)))}║")
    print("  ╚══════════════════════════════════════════════════════╝\n")

    # Run the graph
    result = await graph.ainvoke(initial_state)

    # Save results
    endpoints = result.get("discovered_endpoints", [])
    mock_data = result.get("mock_data", {})
    errors = result.get("errors", [])

    api_spec = {
        "title": _extract_api_title(url),
        "version": "1.0.0",
        "source_url": url,
        "total_endpoints": len(endpoints),
        "total_sections": len(result.get("sections_discovered", [])),
        "endpoints": endpoints,
        "sections": result.get("sections_discovered", []),
    }

    spec_path = output_path / "api_spec.json"
    data_path = output_path / "mock_data.json"
    errors_path = output_path / "errors.json"

    with open(spec_path, "w", encoding="utf-8") as f:
        json.dump(api_spec, f, indent=2, default=str)

    with open(data_path, "w", encoding="utf-8") as f:
        json.dump(mock_data, f, indent=2, default=str)

    if errors:
        with open(errors_path, "w", encoding="utf-8") as f:
            json.dump(errors, f, indent=2)

    # Print summary
    categories = sorted({ep.get("category", "") for ep in endpoints if ep.get("category")})
    methods = {}
    for ep in endpoints:
        m = ep.get("method", "?")
        methods[m] = methods.get(m, 0) + 1

    print("\n  ┌──────────────────────────────────────────────────────┐")
    print("  │                   Crawl Complete                     │")
    print("  ├──────────────────────────────────────────────────────┤")
    print(f"  │  Sections discovered : {len(result.get('sections_discovered', [])):<28}│")
    print(f"  │  Endpoints extracted : {len(endpoints):<28}│")
    print(f"  │  Methods             : {json.dumps(methods):<28}│")
    print(f"  │  Categories          : {len(categories):<28}│")
    print(f"  │  Errors              : {len(errors):<28}│")
    print("  ├──────────────────────────────────────────────────────┤")
    print(f"  │  API Spec  → {str(spec_path):<38}│")
    print(f"  │  Mock Data → {str(data_path):<38}│")
    print("  └──────────────────────────────────────────────────────┘\n")

    return result


# ── Mock server ──────────────────────────────────────────────────────────────

def start_mock_server(
    host: str, port: int, output_dir: str
) -> None:
    """Start the FastAPI mock server."""
    from api_mocker.mock_server import create_mock_app

    spec_path = os.path.join(output_dir, "api_spec.json")
    data_path = os.path.join(output_dir, "mock_data.json")

    if not os.path.exists(spec_path) or not os.path.exists(data_path):
        print(
            "\n  ❌  No crawl data found. Run the crawler first:\n"
            f"     python run_api_mocker.py --url <docs-url>\n"
        )
        sys.exit(1)

    app = create_mock_app(api_spec_path=spec_path, mock_data_path=data_path)

    # Count endpoints for the banner
    with open(spec_path, "r", encoding="utf-8") as f:
        spec = json.load(f)
    ep_count = spec.get("total_endpoints", 0)

    print("\n  ╔══════════════════════════════════════════════════════╗")
    print("  ║           Mock API Server                         ║")
    print("  ╠══════════════════════════════════════════════════════╣")
    print(f"  ║  Server    →  http://{host}:{port:<24}║")
    print(f"  ║  Swagger   →  http://{host}:{port}/docs{' ' * (19 - len(str(port)))}║")
    print(f"  ║  Endpoints →  {ep_count} mocked{' ' * (37 - len(str(ep_count)))}║")
    print("  ║                                                      ║")
    print("  ║  Press Ctrl+C to stop                                ║")
    print("  ╚══════════════════════════════════════════════════════╝\n")

    uvicorn.run(app, host=host, port=port, log_level="info")


# ── Main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    args = parse_args()

    # Show providers and exit
    if args.list_providers:
        from api_mocker.llm_provider import list_providers
        print(list_providers())
        print(
            "\n  💡 Recommended FREE setup:\n"
            "     1. Get a free Groq key at https://console.groq.com\n"
            "     2. export GROQ_API_KEY=gsk_...\n"
            "     3. python run_api_mocker.py --provider groq\n"
        )
        return

    if args.serve_only:
        start_mock_server(args.host, args.port, args.output_dir)
        return

    # Require URL for crawling
    if not args.url:
        print(
            "\n  ❌  --url is required when crawling.  Example:\n"
            "     python run_api_mocker.py --url https://petstore.swagger.io/\n"
            "     python run_api_mocker.py --url https://support.hpe.com/docs/display/public/dp00003271en_us/index.html\n"
        )
        sys.exit(1)

    # Validate: if a specific provider is given, check its key;
    # otherwise auto-detect will handle it (ollama needs no key)
    provider = args.provider
    if provider is None:
        # Check if ANY key is available; if not, suggest free options
        has_any = any(
            os.getenv(k)
            for k in ["GROQ_API_KEY", "GOOGLE_API_KEY", "HUGGINGFACEHUB_API_TOKEN", "ANTHROPIC_API_KEY"]
        )
        if not has_any:
            print(
                "\n  ⚠️  No API keys found — will try Ollama (local, free).\n"
                "  Make sure Ollama is running: https://ollama.com\n"
                "\n  Or set one of these FREE API keys:\n"
                "    export GROQ_API_KEY=gsk_...        # https://console.groq.com\n"
                "    export GOOGLE_API_KEY=AI...         # https://aistudio.google.com/apikey\n"
                "\n  Run  python run_api_mocker.py --list-providers  to see all options.\n"
            )

    # Run the crawler
    asyncio.run(
        run_crawler(args.url, args.output_dir, args.batch_size, args.instances, provider, args.model)
    )

    if args.crawl_only:
        print("  ✅ Crawl-only mode — mock server not started.")
        return

    # Start the mock server
    start_mock_server(args.host, args.port, args.output_dir)


if __name__ == "__main__":
    main()
