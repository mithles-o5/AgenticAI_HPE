import sys
import os
import asyncio

# Ensure stdout uses UTF-8 to prevent character encoding issues on Windows
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

# Add root directory to sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.normpath(os.path.join(BASE_DIR, ".."))
sys.path.insert(0, ROOT_DIR)
sys.path.insert(0, os.path.join(ROOT_DIR, "mcp_server"))

# Mock authentication to run as "mithles@student.tce.edu" (Infrastructure administrator)
import mcp_server
mcp_server._get_token_and_claims = lambda: (
    "mock-token",
    {"email": "mithles@student.tce.edu", "role": "Infrastructure administrator"}
)

async def main():
    print("======================================================================")
    print("E2E MANUAL POWER OFF TEST FOR CLOUD DEVICE: gl-db-011")
    print("======================================================================")

    # 1. Check Status
    print("\n[+] 1. Fetching current status of gl-db-011...")
    status_result = await mcp_server._execute_agent_command(
        query="status of gl-db-011",
        env="dev",
        agent_type="cloud",
        provider_or_protocol="mock_cloud",
        resource_type="database_service"
    )
    print("Result:")
    print(status_result)

    # 2. Test Power OFF
    print("\n[+] 2. Executing power OFF for gl-db-011...")
    power_off_result = await mcp_server._execute_agent_command(
        query="turn OFF gl-db-011",
        env="dev",
        agent_type="cloud",
        provider_or_protocol="mock_cloud",
        resource_type="database_service"
    )
    print("Result:")
    print(power_off_result)

    # 3. Check Status again to confirm power state is OFF
    print("\n[+] 3. Fetching status of gl-db-011 again...")
    status_result_after = await mcp_server._execute_agent_command(
        query="status of gl-db-011",
        env="dev",
        agent_type="cloud",
        provider_or_protocol="mock_cloud",
        resource_type="database_service"
    )
    print("Result:")
    print(status_result_after)

if __name__ == "__main__":
    asyncio.run(main())
