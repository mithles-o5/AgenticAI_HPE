routes = [
    "ethernet-networks",
    "fc-networks",
    "fcoe-networks",
    "logical-interconnect-groups",
    "uplink-sets",
]

template = '''
@app.get("/rest/{route}")
def get_rest_{var}():
    \"\"\"
    Dynamic CRUD Route: GET /rest/{route}
    \"\"\"
    collection_path = "/rest/{route}"
    return db.get_all(collection_path)

@app.get("/rest/{route}/{{id}}")
def get_rest_{var}_id(id: str):
    \"\"\"
    Dynamic CRUD Route: GET /rest/{route}/{{id}}
    \"\"\"
    collection_path = f"/rest/{route}"
    item = db.get_item(collection_path, id)
    if item:
        return item
    raise HTTPException(status_code=404, detail="{route} not found")

@app.post("/rest/{route}")
def post_rest_{var}(payload: dict, request: Request):
    \"\"\"
    Dynamic CRUD Route: POST /rest/{route}
    Returns 202 Accepted.
    \"\"\"
    collection_path = "/rest/{route}"
    item_id = payload.get("id") or payload.get("uri", "").split("/")[-1] or str(uuid.uuid4())
    payload["id"] = item_id
    if "uri" not in payload:
        payload["uri"] = f"/rest/{route}/{{item_id}}"
    payload["status"] = "Adding"

    # Save immediately with Adding state
    db.upsert_item(collection_path, item_id, payload)

    # Async delay to simulate backend provisioning (status: OK after 3 seconds)
    t = threading.Thread(
        target=_apply_async_crud,
        args=(collection_path, item_id, {{"status": "OK"}}, 3, "POST"),
        daemon=True
    )
    t.start()
    return JSONResponse(status_code=202, content={{"message": "Creation accepted", "id": item_id, "item": payload}})

@app.put("/rest/{route}/{{id}}")
def put_rest_{var}_id(id: str, payload: dict):
    \"\"\"
    Dynamic CRUD Route: PUT /rest/{route}/{{id}}
    Returns 202 Accepted.
    \"\"\"
    collection_path = "/rest/{route}"
    existing = db.get_item(collection_path, id)
    if not existing:
        raise HTTPException(status_code=404, detail="{route} not found")
    
    payload["id"] = id
    payload["status"] = "Updating"
    
    # Save immediately with Updating state
    db.upsert_item(collection_path, id, payload)
    
    t = threading.Thread(
        target=_apply_async_crud,
        args=(collection_path, id, {{"status": "OK"}}, 3, "PUT"),
        daemon=True
    )
    t.start()
    return JSONResponse(status_code=202, content={{"message": "Update accepted", "id": id, "item": payload}})

@app.delete("/rest/{route}/{{id}}")
def delete_rest_{var}_id(id: str):
    \"\"\"
    Dynamic CRUD Route: DELETE /rest/{route}/{{id}}
    Returns 202 Accepted.
    \"\"\"
    collection_path = "/rest/{route}"
    item = db.get_item(collection_path, id)
    if item:
        item = dict(item)
        item["status"] = "Removing"
        db.upsert_item(collection_path, id, item)
        
        t = threading.Thread(
            target=_apply_async_crud,
            args=(collection_path, id, {{}}, 5, "DELETE"),
            daemon=True
        )
        t.start()
        return JSONResponse(status_code=202, content={{"message": "Deletion accepted", "id": id, "item": item}})
    raise HTTPException(status_code=404, detail="{route} not found")
'''

li_template = '''
@app.get("/rest/logical-interconnects")
def get_rest_logical_interconnects():
    \"\"\"
    Dynamic CRUD Route: GET /rest/logical-interconnects
    \"\"\"
    collection_path = "/rest/logical-interconnects"
    return db.get_all(collection_path)

@app.get("/rest/logical-interconnects/{id}")
def get_rest_logical_interconnects_id(id: str):
    \"\"\"
    Dynamic CRUD Route: GET /rest/logical-interconnects/{id}
    \"\"\"
    collection_path = "/rest/logical-interconnects"
    item = db.get_item(collection_path, id)
    if item:
        return item
    raise HTTPException(status_code=404, detail="logical-interconnects not found")

@app.put("/rest/logical-interconnects/{id}")
def put_rest_logical_interconnects_id(id: str, payload: dict):
    \"\"\"
    Dynamic CRUD Route: PUT /rest/logical-interconnects/{id}
    Returns 202 Accepted.
    \"\"\"
    collection_path = "/rest/logical-interconnects"
    existing = db.get_item(collection_path, id)
    if not existing:
        raise HTTPException(status_code=404, detail="logical-interconnects not found")
    
    payload["id"] = id
    payload["status"] = "Updating"
    
    db.upsert_item(collection_path, id, payload)
    
    t = threading.Thread(
        target=_apply_async_crud,
        args=(collection_path, id, {"status": "OK"}, 5, "PUT"),
        daemon=True
    )
    t.start()
    return JSONResponse(status_code=202, content={"message": "Update accepted", "id": id, "item": payload})
'''

out = ""
for r in routes:
    out += template.format(route=r, var=r.replace("-", "_"))

out += li_template

with open("d:/HPE CPP/MCP_Integrated/mock_server(oneview)/routes_networking.py", "w") as f:
    f.write(out)

print("Generated routes_networking.py")
