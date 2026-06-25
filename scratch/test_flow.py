"""
Simulate a full flow trace.
"""
import sys, os, logging
from unittest.mock import patch

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.normpath(os.path.join(BASE_DIR, ".."))
sys.path.insert(0, ROOT_DIR)
for p in ["authentication", "authorization", "resource_resolver", "task_planner", "execution_engine"]:
    sys.path.insert(0, os.path.join(ROOT_DIR, p))

logging.basicConfig(level=logging.DEBUG)

# Mock auth
import mcp_server.mcp_server as ms
ms._get_token_and_claims = lambda: ("mock_token", {"email": "admin@hpe.com"})
ms._resolve_role = lambda claims: ("devasksr@gmail.com", "Infrastructure administrator")

import asyncio
async def test_flow():
    print("\n\n=== EXECUTING FLOW TEST ===")
    res = await ms._execute_agent_command(
        query="power off ap-floor-006",
        env="dev",
        agent_type="unknown",
        provider_or_protocol="unknown",
        resource_type="access_point"
    )
    with open("scratch/result.txt", "w", encoding="utf-8") as f:
        f.write(res)
    print("Wrote output to scratch/result.txt")

asyncio.run(test_flow())
