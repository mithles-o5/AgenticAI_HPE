
@app.get("/rest/storage-systems")
def get_rest_storage_systems():
    """
    Dynamic CRUD Route: GET /rest/storage-systems
    """
    collection_path = "/rest/storage-systems"
    return db.get_all(collection_path)

@app.get("/rest/storage-systems/{id}")
def get_rest_storage_systems_id(id: str):
    """
    Dynamic CRUD Route: GET /rest/storage-systems/{id}
    """
    collection_path = f"/rest/storage-systems"
    item = db.get_item(collection_path, id)
    if item:
        return item
    raise HTTPException(status_code=404, detail="storage-systems not found")

@app.post("/rest/storage-systems")
def post_rest_storage_systems(payload: dict, request: Request):
    """
    Dynamic CRUD Route: POST /rest/storage-systems
    Returns 202 Accepted.
    """
    collection_path = "/rest/storage-systems"
    item_id = payload.get("id") or payload.get("uri", "").split("/")[-1] or str(uuid.uuid4())
    payload["id"] = item_id
    if "uri" not in payload:
        payload["uri"] = f"/rest/storage-systems/{item_id}"
    payload["status"] = "Adding"

    db.upsert_item(collection_path, item_id, payload)

    t = threading.Thread(
        target=_apply_async_crud,
        args=(collection_path, item_id, {"status": "OK"}, 5, "POST"),
        daemon=True
    )
    t.start()
    return JSONResponse(status_code=202, content={"message": "Creation accepted", "id": item_id, "item": payload})

@app.put("/rest/storage-systems/{id}")
def put_rest_storage_systems_id_batch2(id: str, payload: dict):
    """
    Dynamic CRUD Route: PUT /rest/storage-systems/{id}
    Returns 202 Accepted.
    """
    collection_path = "/rest/storage-systems"
    existing = db.get_item(collection_path, id)
    if not existing:
        raise HTTPException(status_code=404, detail="storage-systems not found")
    
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

@app.delete("/rest/storage-systems/{id}")
def delete_rest_storage_systems_id(id: str):
    """
    Dynamic CRUD Route: DELETE /rest/storage-systems/{id}
    Returns 202 Accepted.
    """
    collection_path = "/rest/storage-systems"
    item = db.get_item(collection_path, id)
    if item:
        item = dict(item)
        item["status"] = "Removing"
        db.upsert_item(collection_path, id, item)
        
        t = threading.Thread(
            target=_apply_async_crud,
            args=(collection_path, id, {}, 6, "DELETE"),
            daemon=True
        )
        t.start()
        return JSONResponse(status_code=202, content={"message": "Deletion accepted", "id": id, "item": item})
    raise HTTPException(status_code=404, detail="storage-systems not found")

@app.get("/rest/storage-pools")
def get_rest_storage_pools():
    """
    Dynamic CRUD Route: GET /rest/storage-pools
    """
    collection_path = "/rest/storage-pools"
    return db.get_all(collection_path)

@app.get("/rest/storage-pools/{id}")
def get_rest_storage_pools_id(id: str):
    """
    Dynamic CRUD Route: GET /rest/storage-pools/{id}
    """
    collection_path = f"/rest/storage-pools"
    item = db.get_item(collection_path, id)
    if item:
        return item
    raise HTTPException(status_code=404, detail="storage-pools not found")

@app.post("/rest/storage-pools")
def post_rest_storage_pools(payload: dict, request: Request):
    """
    Dynamic CRUD Route: POST /rest/storage-pools
    Returns 202 Accepted.
    """
    collection_path = "/rest/storage-pools"
    item_id = payload.get("id") or payload.get("uri", "").split("/")[-1] or str(uuid.uuid4())
    payload["id"] = item_id
    if "uri" not in payload:
        payload["uri"] = f"/rest/storage-pools/{item_id}"
    payload["status"] = "Adding"

    db.upsert_item(collection_path, item_id, payload)

    t = threading.Thread(
        target=_apply_async_crud,
        args=(collection_path, item_id, {"status": "OK"}, 5, "POST"),
        daemon=True
    )
    t.start()
    return JSONResponse(status_code=202, content={"message": "Creation accepted", "id": item_id, "item": payload})

@app.put("/rest/storage-pools/{id}")
def put_rest_storage_pools_id_batch2(id: str, payload: dict):
    """
    Dynamic CRUD Route: PUT /rest/storage-pools/{id}
    Returns 202 Accepted.
    """
    collection_path = "/rest/storage-pools"
    existing = db.get_item(collection_path, id)
    if not existing:
        raise HTTPException(status_code=404, detail="storage-pools not found")
    
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

@app.delete("/rest/storage-pools/{id}")
def delete_rest_storage_pools_id(id: str):
    """
    Dynamic CRUD Route: DELETE /rest/storage-pools/{id}
    Returns 202 Accepted.
    """
    collection_path = "/rest/storage-pools"
    item = db.get_item(collection_path, id)
    if item:
        item = dict(item)
        item["status"] = "Removing"
        db.upsert_item(collection_path, id, item)
        
        t = threading.Thread(
            target=_apply_async_crud,
            args=(collection_path, id, {}, 6, "DELETE"),
            daemon=True
        )
        t.start()
        return JSONResponse(status_code=202, content={"message": "Deletion accepted", "id": id, "item": item})
    raise HTTPException(status_code=404, detail="storage-pools not found")

@app.get("/rest/storage-volumes")
def get_rest_storage_volumes():
    """
    Dynamic CRUD Route: GET /rest/storage-volumes
    """
    collection_path = "/rest/storage-volumes"
    return db.get_all(collection_path)

@app.get("/rest/storage-volumes/{id}")
def get_rest_storage_volumes_id(id: str):
    """
    Dynamic CRUD Route: GET /rest/storage-volumes/{id}
    """
    collection_path = f"/rest/storage-volumes"
    item = db.get_item(collection_path, id)
    if item:
        return item
    raise HTTPException(status_code=404, detail="storage-volumes not found")

@app.post("/rest/storage-volumes")
def post_rest_storage_volumes(payload: dict, request: Request):
    """
    Dynamic CRUD Route: POST /rest/storage-volumes
    Returns 202 Accepted.
    """
    collection_path = "/rest/storage-volumes"
    item_id = payload.get("id") or payload.get("uri", "").split("/")[-1] or str(uuid.uuid4())
    payload["id"] = item_id
    if "uri" not in payload:
        payload["uri"] = f"/rest/storage-volumes/{item_id}"
    payload["status"] = "Adding"

    db.upsert_item(collection_path, item_id, payload)

    t = threading.Thread(
        target=_apply_async_crud,
        args=(collection_path, item_id, {"status": "OK"}, 5, "POST"),
        daemon=True
    )
    t.start()
    return JSONResponse(status_code=202, content={"message": "Creation accepted", "id": item_id, "item": payload})

@app.put("/rest/storage-volumes/{id}")
def put_rest_storage_volumes_id_batch2(id: str, payload: dict):
    """
    Dynamic CRUD Route: PUT /rest/storage-volumes/{id}
    Returns 202 Accepted.
    """
    collection_path = "/rest/storage-volumes"
    existing = db.get_item(collection_path, id)
    if not existing:
        raise HTTPException(status_code=404, detail="storage-volumes not found")
    
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

@app.delete("/rest/storage-volumes/{id}")
def delete_rest_storage_volumes_id(id: str):
    """
    Dynamic CRUD Route: DELETE /rest/storage-volumes/{id}
    Returns 202 Accepted.
    """
    collection_path = "/rest/storage-volumes"
    item = db.get_item(collection_path, id)
    if item:
        item = dict(item)
        item["status"] = "Removing"
        db.upsert_item(collection_path, id, item)
        
        t = threading.Thread(
            target=_apply_async_crud,
            args=(collection_path, id, {}, 6, "DELETE"),
            daemon=True
        )
        t.start()
        return JSONResponse(status_code=202, content={"message": "Deletion accepted", "id": id, "item": item})
    raise HTTPException(status_code=404, detail="storage-volumes not found")

@app.get("/rest/storage-volume-templates")
def get_rest_storage_volume_templates():
    """
    Dynamic CRUD Route: GET /rest/storage-volume-templates
    """
    collection_path = "/rest/storage-volume-templates"
    return db.get_all(collection_path)

@app.get("/rest/storage-volume-templates/{id}")
def get_rest_storage_volume_templates_id(id: str):
    """
    Dynamic CRUD Route: GET /rest/storage-volume-templates/{id}
    """
    collection_path = f"/rest/storage-volume-templates"
    item = db.get_item(collection_path, id)
    if item:
        return item
    raise HTTPException(status_code=404, detail="storage-volume-templates not found")

@app.post("/rest/storage-volume-templates")
def post_rest_storage_volume_templates(payload: dict, request: Request):
    """
    Dynamic CRUD Route: POST /rest/storage-volume-templates
    Returns 202 Accepted.
    """
    collection_path = "/rest/storage-volume-templates"
    item_id = payload.get("id") or payload.get("uri", "").split("/")[-1] or str(uuid.uuid4())
    payload["id"] = item_id
    if "uri" not in payload:
        payload["uri"] = f"/rest/storage-volume-templates/{item_id}"
    payload["status"] = "Adding"

    db.upsert_item(collection_path, item_id, payload)

    t = threading.Thread(
        target=_apply_async_crud,
        args=(collection_path, item_id, {"status": "OK"}, 5, "POST"),
        daemon=True
    )
    t.start()
    return JSONResponse(status_code=202, content={"message": "Creation accepted", "id": item_id, "item": payload})

@app.put("/rest/storage-volume-templates/{id}")
def put_rest_storage_volume_templates_id_batch2(id: str, payload: dict):
    """
    Dynamic CRUD Route: PUT /rest/storage-volume-templates/{id}
    Returns 202 Accepted.
    """
    collection_path = "/rest/storage-volume-templates"
    existing = db.get_item(collection_path, id)
    if not existing:
        raise HTTPException(status_code=404, detail="storage-volume-templates not found")
    
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

@app.delete("/rest/storage-volume-templates/{id}")
def delete_rest_storage_volume_templates_id(id: str):
    """
    Dynamic CRUD Route: DELETE /rest/storage-volume-templates/{id}
    Returns 202 Accepted.
    """
    collection_path = "/rest/storage-volume-templates"
    item = db.get_item(collection_path, id)
    if item:
        item = dict(item)
        item["status"] = "Removing"
        db.upsert_item(collection_path, id, item)
        
        t = threading.Thread(
            target=_apply_async_crud,
            args=(collection_path, id, {}, 6, "DELETE"),
            daemon=True
        )
        t.start()
        return JSONResponse(status_code=202, content={"message": "Deletion accepted", "id": id, "item": item})
    raise HTTPException(status_code=404, detail="storage-volume-templates not found")

@app.get("/rest/san-managers")
def get_rest_san_managers():
    """
    Dynamic CRUD Route: GET /rest/san-managers
    """
    collection_path = "/rest/san-managers"
    return db.get_all(collection_path)

@app.get("/rest/san-managers/{id}")
def get_rest_san_managers_id(id: str):
    """
    Dynamic CRUD Route: GET /rest/san-managers/{id}
    """
    collection_path = f"/rest/san-managers"
    item = db.get_item(collection_path, id)
    if item:
        return item
    raise HTTPException(status_code=404, detail="san-managers not found")

@app.post("/rest/san-managers")
def post_rest_san_managers(payload: dict, request: Request):
    """
    Dynamic CRUD Route: POST /rest/san-managers
    Returns 202 Accepted.
    """
    collection_path = "/rest/san-managers"
    item_id = payload.get("id") or payload.get("uri", "").split("/")[-1] or str(uuid.uuid4())
    payload["id"] = item_id
    if "uri" not in payload:
        payload["uri"] = f"/rest/san-managers/{item_id}"
    payload["status"] = "Adding"

    db.upsert_item(collection_path, item_id, payload)

    t = threading.Thread(
        target=_apply_async_crud,
        args=(collection_path, item_id, {"status": "OK"}, 5, "POST"),
        daemon=True
    )
    t.start()
    return JSONResponse(status_code=202, content={"message": "Creation accepted", "id": item_id, "item": payload})

@app.put("/rest/san-managers/{id}")
def put_rest_san_managers_id_batch2(id: str, payload: dict):
    """
    Dynamic CRUD Route: PUT /rest/san-managers/{id}
    Returns 202 Accepted.
    """
    collection_path = "/rest/san-managers"
    existing = db.get_item(collection_path, id)
    if not existing:
        raise HTTPException(status_code=404, detail="san-managers not found")
    
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

@app.delete("/rest/san-managers/{id}")
def delete_rest_san_managers_id(id: str):
    """
    Dynamic CRUD Route: DELETE /rest/san-managers/{id}
    Returns 202 Accepted.
    """
    collection_path = "/rest/san-managers"
    item = db.get_item(collection_path, id)
    if item:
        item = dict(item)
        item["status"] = "Removing"
        db.upsert_item(collection_path, id, item)
        
        t = threading.Thread(
            target=_apply_async_crud,
            args=(collection_path, id, {}, 6, "DELETE"),
            daemon=True
        )
        t.start()
        return JSONResponse(status_code=202, content={"message": "Deletion accepted", "id": id, "item": item})
    raise HTTPException(status_code=404, detail="san-managers not found")
