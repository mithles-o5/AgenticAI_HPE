import asyncio
import os
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import mcp_server.mcp_server as mcp_server_module

# Monkey patch auth
def _mock_get_token_and_claims():
    return "mock_token", {"email": "devasksr@gmail.com", "roles": ["Infrastructure administrator"]}

def _mock_resolve_role(claims):
    return "devasksr@gmail.com", "Infrastructure administrator"

mcp_server_module._get_token_and_claims = _mock_get_token_and_claims
mcp_server_module._resolve_role = _mock_resolve_role

# Monkey patch QueryAgent
class MockQueryAgent:
    @staticmethod
    def parse_query(q):
        if "status" in q:
            return {"action": "STATUS", "identifier": "demo-vm-001", "resource_type": "server"}
        return {"action": "OFF", "identifier": "demo-vm-001", "resource_type": "server"}

mcp_server_module.QueryAgent = MockQueryAgent

async def run_test():
    try:
        print("Starting E2E Flow Test...")
        print("Query: stop demo-vm-001")
        result = await mcp_server_module._execute_agent_command(
            query="stop demo-vm-001",
            env="dev",
            agent_type="cloud",
            provider_or_protocol="mock",
            resource_type="server"
        )
        print("\n=== Result ===")
        print(result)

        print("\nQuery: status\n")
        result2 = await mcp_server_module._execute_agent_command(
            query="status",
            env="dev",
            agent_type="cloud",
            provider_or_protocol="mock",
            resource_type="server"
        )
        print("=== Result 2 ===")
        print(result2)

    except Exception as e:
        print(f"Error during test: {e}")

if __name__ == "__main__":
    asyncio.run(run_test())
