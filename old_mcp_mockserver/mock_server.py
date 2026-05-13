from fastapi import FastAPI, HTTPException, Query, Body, Response
import requests
import uuid
from datetime import datetime, timezone
import re

app = FastAPI()

servers = {
    "1": {"status": "running"},
    "2": {"status": "stopped"},
    "3": {"status": "running"}
}

users_db = {
    "3fa85f64-5717-4562-b3fc-2c963f66afa6": {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "type": "user",
        "generation": 1,
        "createdAt": "2025-09-10T18:22:24.530Z",
        "updatedAt": "2025-09-11T10:20:19.530Z",
        "username": "user@example.com",
        "firstName": "First",
        "lastName": "Last",
        "userStatus": "UNVERIFIED",
        "lastLogin": "2025-09-10T18:22:24.530Z",
        "resourceUri": "/identity/v1/users/3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "language": "en",
        "idleTimeout": 1800
    }
}

@app.get("/servers")
def list_servers():
    return servers

@app.get("/servers/{server_id}")
def get_server_status(server_id: str):
    server = servers.get(server_id)
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")
    return {"server_id": server_id, "status": server["status"]}

@app.post("/servers/{server_id}/restart")
def restart_server(server_id: str):
    server = servers.get(server_id)
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")

    server["status"] = "running"
    return {
        "message": f"Server {server_id} restarted successfully",
        "status": "running"
    }


HPE_API_URL = "https://us-west.api.greenlake.hpe.com/compute-ops-mgmt/v1/servers"
JWT_TOKEN = "YOUR_JWT_HERE"

@app.get("/hpe/servers")
def get_hpe_servers():
    try:
        headers = {
            "Authorization": f"Bearer {JWT_TOKEN}"
        }

        response = requests.get(HPE_API_URL, headers=headers)

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.text
            )

        return response.json()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/identity/v1/users")
def get_users(
    filter: str = Query("", description="Filter data using a subset of OData 4.0"),
    limit: int = Query(300, ge=1, le=600),
    offset: int = Query(0, ge=0)
):
    result = list(users_db.values())
    if filter:
        match = re.search(r"(\w+)\s+(eq|ne|gt|ge|lt)\s+'(.*)'", filter)
        if match:
            field, op, val = match.groups()
            filtered_result = []
            for u in result:
                u_val = str(u.get(field, ""))
                if op == "eq" and u_val == val:
                    filtered_result.append(u)
                elif op == "ne" and u_val != val:
                    filtered_result.append(u)
                elif op == "gt" and u_val > val:
                    filtered_result.append(u)
                elif op == "ge" and u_val >= val:
                    filtered_result.append(u)
                elif op == "lt" and u_val < val:
                    filtered_result.append(u)
            result = filtered_result

    total = len(result)
    paginated_result = result[offset:offset+limit]

    return {
        "offset": offset,
        "count": len(paginated_result),
        "total": total,
        "items": paginated_result
    }

@app.post("/identity/v1/users", status_code=201)
def invite_user(email: str = Body(..., embed=True), sendWelcomeEmail: bool = Body(True, embed=True)):
    new_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
    user = {
        "id": new_id,
        "type": "user",
        "generation": 1,
        "createdAt": now,
        "updatedAt": now,
        "username": email,
        "firstName": "",
        "lastName": "",
        "userStatus": "UNVERIFIED",
        "lastLogin": "",
        "resourceUri": f"/identity/v1/users/{new_id}",
        "language": "en",
        "idleTimeout": 1800
    }
    users_db[new_id] = user
    return {"message": f"Invited user {email}"}

@app.get("/identity/v1/users/{id}")
def get_user(id: str):
    user = users_db.get(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/identity/v1/users/{id}")
def update_user(id: str, language: str = Body("en", embed=True), idleTimeout: int = Body(1800, embed=True)):
    user = users_db.get(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user["language"] = language
    user["idleTimeout"] = idleTimeout
    user["updatedAt"] = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
    user["generation"] += 1
    return {"message": "User preferences updated successfully"}

@app.delete("/identity/v1/users/{id}", status_code=204)
def delete_user(id: str):
    if id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    del users_db[id]
    return Response(status_code=204)