import httpx
import asyncio

async def test_mock():
    server_id = "agg-sw02-1"
    async with httpx.AsyncClient(base_url="http://127.0.0.1:8000") as client:
        # Test 1: Turn off
        print("\n--- Testing Power OFF ---")
        await client.put(f"/rest/server-hardware/{server_id}/powerState", json={"powerState": "Off"})
        
        # Check utilization and thermal
        util_resp = await client.get(f"/rest/server-hardware/{server_id}/utilization")
        print(f"Utilization (Off): {util_resp.json()}")
        therm_resp = await client.get(f"/rest/server-hardware/{server_id}/thermal")
        print(f"Thermal (Off): {therm_resp.json()}")

if __name__ == "__main__":
    asyncio.run(test_mock())
