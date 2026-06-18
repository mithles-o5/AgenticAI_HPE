import httpx
import asyncio

async def test():
    async with httpx.AsyncClient() as client:
        r = await client.post("http://localhost:8008/tasks", json={
            "task_id": "1234",
            "task_type": "control",
            "agent_type": "onprem",
            "resource_type": "server_hardware",
            "resource_id": "ov-uuid-c22",
            "provider": "oneview",
            "action": "execute_action",
            "parameters": {"action_verb": "power-off"}
        })
        print(r.status_code)
        print(r.json())

asyncio.run(test())
