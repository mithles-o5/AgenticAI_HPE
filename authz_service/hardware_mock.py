from fastapi import APIRouter, HTTPException
import random
import threading
import time

router = APIRouter(prefix="/rest/server-hardware")

# Mock database
servers = {
    "server01": {
        "name": "Server 01",
        "powerState": "On",
        "processorUtilization": 30,
        "memoryUtilization": 50
    },
    "server02": {
        "name": "Server 02",
        "powerState": "On",
        "processorUtilization": 20,
        "memoryUtilization": 40
    }
}

@router.get("")
def get_all_servers():
    result = []
    for sid, data in servers.items():
        if data["powerState"] in ["Off", "Rebooting"]:
            data["processorUtilization"] = 0
            data["memoryUtilization"] = 0
        else:
            data["processorUtilization"] = random.randint(10, 90)
            data["memoryUtilization"] = random.randint(10, 90)

        result.append({
            "uri": f"/rest/server-hardware/{sid}",
            "name": data["name"],
            "powerState": data["powerState"],
            "processorUtilization": data["processorUtilization"],
            "memoryUtilization": data["memoryUtilization"]
        })
    return {"members": result, "count": len(result)}

@router.get("/{server_id}")
def get_server(server_id: str):
    if server_id not in servers:
        raise HTTPException(status_code=404, detail="Server not found")

    data = servers[server_id]
    if data["powerState"] in ["Off", "Rebooting"]:
        data["processorUtilization"] = 0
        data["memoryUtilization"] = 0
    else:
        data["processorUtilization"] = random.randint(10, 90)
        data["memoryUtilization"] = random.randint(10, 90)

    return {
        "uri": f"/rest/server-hardware/{server_id}",
        "name": data["name"],
        "powerState": data["powerState"],
        "processorUtilization": data["processorUtilization"],
        "memoryUtilization": data["memoryUtilization"]
    }

@router.put("/{server_id}/powerState")
def change_power(server_id: str, state: str):
    if server_id not in servers:
        raise HTTPException(status_code=404, detail="Server not found")

    state = state.capitalize()
    if state not in ["On", "Off"]:
        raise HTTPException(status_code=400, detail="Invalid state")

    servers[server_id]["powerState"] = state
    return {"message": f"{server_id} power set to {state}"}

def reboot_process(server_id):
    data = servers[server_id]
    data["powerState"] = "Rebooting"
    data["processorUtilization"] = 0
    data["memoryUtilization"] = 0
    time.sleep(5)  # simulate reboot delay
    servers[server_id]["powerState"] = "On"

@router.post("/{server_id}/actions/reset")
def reboot_server(server_id: str):
    if server_id not in servers:
        raise HTTPException(status_code=404, detail="Server not found")

    thread = threading.Thread(target=reboot_process, args=(server_id,))
    thread.start()
    return {"message": f"{server_id} is rebooting"}
