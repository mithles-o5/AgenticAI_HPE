"""
run_mock_agent.py
─────────────────
Entry point for the COM/OneView Mock Agent.

Usage
─────
  # Full pipeline: crawl docs → generate → serve
  python run_mock_agent.py --url https://support.hpe.com/...

  # HPE OneView (fast path — no URL needed, uses seeded schemas)
  python run_mock_agent.py --hpe-oneview

  # Crawl only (don't start server)
  python run_mock_agent.py --hpe-oneview --crawl-only

  # Serve from existing SQLite database (skip crawl)
  python run_mock_agent.py --serve-only --port 8080

  # Reset DB and re-seed
  python run_mock_agent.py --hpe-oneview --reset

  # Enable auth middleware (after teammate integrates JWT)
  python run_mock_agent.py --hpe-oneview --enable-auth
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
logger = logging.getLogger("com-mock")

# ── CLI ──────────────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="COM / OneView Mock Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--url",         default=None,  help="API docs URL to crawl")
    p.add_argument("--hpe-oneview", action="store_true",
                   help="Use HPE OneView fast-path (no URL crawl, uses seeded schemas)")
    p.add_argument("--output-dir",  default="output", help="Output directory (default: output/)")
    p.add_argument("--port",        type=int, default=int(os.getenv("MOCK_SERVER_PORT", "8080")))
    p.add_argument("--host",        default="0.0.0.0")
    p.add_argument("--instances",   type=int, default=5, metavar="N",
                   help="Sample items per resource collection (default: 5)")
    p.add_argument("--provider",    default=os.getenv("LLM_PROVIDER"),
                   choices=["groq", "gemini", "ollama", "huggingface", "anthropic"])
    p.add_argument("--model",       default=None)
    p.add_argument("--max-depth",   type=int, default=2, help="Max doc fetch depth (default: 2)")
    p.add_argument("--crawl-only",  action="store_true")
    p.add_argument("--serve-only",  action="store_true")
    p.add_argument("--reset",       action="store_true",
                   help="Wipe the SQLite DB and re-seed from scratch")
    p.add_argument("--enable-auth", action="store_true",
                   help="Enable X-Auth-Token middleware (plug in teammate's JWT validator)")
    p.add_argument("--list-providers", action="store_true")
    p.add_argument("--db-path",     default=None,
                   help="Path to SQLite DB file (default: output/mock.db)")
    return p.parse_args()


# ── Crawler pipeline ─────────────────────────────────────────────────────────

async def run_pipeline(
    url: str,
    output_dir: str,
    instances: int,
    max_depth: int,
    provider: str | None,
    model: str | None,
    reset: bool,
    db_path: str,
) -> None:
    from com_mock.db import DatabaseEngine
    from com_mock.graph import build_com_crawler_graph

    db = DatabaseEngine(db_path)
    await db.init()

    if reset:
        logger.info("🗑️  Resetting database...")
        await db.reset()

    async def on_progress(msg: str) -> None:
        print(f"  {msg}")

    graph = build_com_crawler_graph(
        db=db,
        progress_callback=on_progress,
        provider=provider,
        model=model,
        output_dir=output_dir,
    )

    # Detect HPE OneView URL for fake initial state
    from com_mock.agents.doc_fetcher import _is_hpe_oneview_url
    is_hpe = _is_hpe_oneview_url(url)

    initial_state = {
        "messages":              [],
        "source_url":            url,
        "max_fetch_depth":       max_depth,
        "instances_per_resource": instances,
        "output_dir":            output_dir,
        "fetched_pages":         {},
        "pages_to_fetch":        [],
        "visited_urls":          [],
        "extracted_schemas":     {},
        "schema_batches_total":  0,
        "schema_batches_done":   0,
        "schema_extraction_errors": [],
        "relationship_graph":    {},
        "synthesized_data":      {},
        "retry_resource_types":  [],
        "validation_errors":     {},
        "validation_retries":    {},
        "max_validation_retries": 3,
        "seeded_resource_types": [],
        "seeded_total_records":  0,
        "api_spec":              {},
        "status":                "fetching",
        "is_hpe_oneview":        False,
        "errors":                [],
        "progress_log":          [],
    }

    _print_banner(url, output_dir, instances, provider)

    result = await graph.ainvoke(initial_state)

    _print_summary(result)
    await db.close()


def _print_banner(url: str, output: str, n: int, provider: str | None) -> None:
    print("\n  ╔══════════════════════════════════════════════════════════╗")
    print("  ║        COM / OneView Mock Agent — Beast Edition         ║")
    print("  ╠══════════════════════════════════════════════════════════╣")
    print(f"  ║  Source     → {url[:43]:<43}║")
    print(f"  ║  Output     → {output:<43}║")
    print(f"  ║  Instances  → {str(n):<43}║")
    print(f"  ║  Provider   → {str(provider or 'auto-detect'):<43}║")
    print("  ╚══════════════════════════════════════════════════════════╝\n")


def _print_summary(result: dict) -> None:
    seeded = result.get("seeded_total_records", 0)
    resource_types = result.get("seeded_resource_types", [])
    errors = result.get("errors", [])
    print("\n  ┌──────────────────────────────────────────────────────────┐")
    print("  │                   Pipeline Complete                      │")
    print("  ├──────────────────────────────────────────────────────────┤")
    print(f"  │  Resource types : {len(resource_types):<38}│")
    print(f"  │  Total records  : {seeded:<38}│")
    print(f"  │  Errors         : {len(errors):<38}│")
    if errors:
        for e in errors[:3]:
            print(f"  │    ⚠️  {e[:50]:<52}│")
    print("  └──────────────────────────────────────────────────────────┘\n")


# ── Mock server ──────────────────────────────────────────────────────────────

async def start_mock_server(
    host: str,
    port: int,
    output_dir: str,
    db_path: str,
    enable_auth: bool,
) -> None:
    from com_mock.db import DatabaseEngine
    from com_mock.mock_server import create_mock_app
    import com_mock.oneview_protocol as proto

    if enable_auth:
        proto.AUTH_ENABLED = True
        logger.info("🔒 Auth middleware ENABLED — X-Auth-Token required")
    else:
        logger.info("🔓 Auth middleware DISABLED (pass-through)")

    db = DatabaseEngine(db_path)
    await db.init()

    spec_path = os.path.join(output_dir, "api_spec.json")
    app = create_mock_app(db=db, api_spec_path=spec_path)

    # Count records for the banner
    total = 0
    from com_mock.resource_graph import ONEVIEW_RESOURCE_SCHEMAS
    for slug in ONEVIEW_RESOURCE_SCHEMAS:
        total += await db.count_resources(slug)

    print("\n  ╔══════════════════════════════════════════════════════════╗")
    print("  ║        COM / OneView Mock Server — Beast Edition        ║")
    print("  ╠══════════════════════════════════════════════════════════╣")
    print(f"  ║  Server   → http://{host}:{port:<31}║")
    print(f"  ║  Swagger  → http://{host}:{port}/docs{' ' * (26 - len(str(port)))}║")
    print(f"  ║  Records  → {total} in SQLite{' ' * (37 - len(str(total)))}║")
    print(f"  ║  Auth     → {'ENABLED' if enable_auth else 'DISABLED (pass-through)':<39}║")
    print("  ║                                                          ║")
    print("  ║  Press Ctrl+C to stop                                    ║")
    print("  ╚══════════════════════════════════════════════════════════╝\n")

    config = uvicorn.Config(app, host=host, port=port, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()


# ── Main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    args = parse_args()

    if args.list_providers:
        from com_mock.llm_provider import list_providers
        print(list_providers())
        return

    output_dir = args.output_dir
    db_path = args.db_path or os.path.join(output_dir, "mock.db")

    # --serve-only: skip crawl, just start server
    if args.serve_only:
        asyncio.run(start_mock_server(
            args.host, args.port, output_dir, db_path, args.enable_auth
        ))
        return

    # Determine source URL
    if args.hpe_oneview:
        url = "https://support.hpe.com/hpesc/public/docDisplay?docId=dp00003271en_us"
    elif args.url:
        url = args.url
    else:
        print("\n  ❌  Provide --url <docs-url>  or  --hpe-oneview\n")
        sys.exit(1)

    # Run the pipeline
    asyncio.run(run_pipeline(
        url=url,
        output_dir=output_dir,
        instances=args.instances,
        max_depth=args.max_depth,
        provider=args.provider,
        model=args.model,
        reset=args.reset,
        db_path=db_path,
    ))

    if args.crawl_only:
        print("  ✅  Crawl-only mode — server not started.")
        return

    # Start the server
    asyncio.run(start_mock_server(
        args.host, args.port, output_dir, db_path, args.enable_auth
    ))


if __name__ == "__main__":
    main()
