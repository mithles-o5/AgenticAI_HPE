import hashlib

_ADJECTIVES = [
    "Primary", "Secondary", "Backup", "Staging", "Production",
    "Dev", "Test", "QA", "Demo", "Legacy", "New", "Temp",
    "Regional", "Global", "Local", "Internal"
]

_STATUSES = ["active", "inactive", "provisioning", "error", "maintenance",
             "ready", "warning", "degraded", "disabled", "pending"]

def _generate_sample_items(path, count=3):
    parts = [p for p in path.split('/') if p and '{' not in p]
    resource_type = parts[-1] if parts else "item"
    resource_type = resource_type.lower().replace("-", "_")
    items = []
    
    for i in range(max(1, count)):
        seed = f"{resource_type}:{i}:{path}"
        uid = hashlib.md5(seed.encode()).hexdigest()
        uuid_str = f"{uid[:8]}-{uid[8:12]}-{uid[12:16]}-{uid[16:20]}-{uid[20:32]}"
        
        adj = _ADJECTIVES[i % len(_ADJECTIVES)]
        status = _STATUSES[i % len(_STATUSES)]
        
        items.append({
            "id": uuid_str,
            "type": resource_type,
            "uri": f"{path.split('{')[0]}{uuid_str}" if '{' in path else f"{path}/{uuid_str}",
            "name": f"{adj} {resource_type.title()} {i + 1}",
            "status": status,
            "created": f"2025-06-15T10:30:00.000Z",
            "modified": f"2025-06-15T10:30:00.000Z",
        })
    return items

def get_fallback_payload(method, path):
    parts = [p for p in path.split('/') if p and '{' not in p]
    resource_type = parts[-1] if parts else "item"
    
    request_body = {}
    response_body = {}
    
    if method == "GET":
        if "{" not in path:
            # Collection
            items = _generate_sample_items(path, 3)
            response_body = {
                "type": f"{resource_type}_list",
                "count": len(items),
                "total": len(items),
                "items": items
            }
        else:
            # Single
            items = _generate_sample_items(path, 1)
            response_body = items[0]
    elif method in ("POST", "PUT", "PATCH"):
        items = _generate_sample_items(path, 1)
        # For a task or resource creation
        request_body = {
            "name": items[0]["name"],
            "description": "Auto-generated dummy payload"
        }
        response_body = {
            "type": "task",
            "state": "completed",
            "status": "success",
            "resourceUri": items[0]["uri"]
        }
    elif method == "DELETE":
        pass  # Empty

    return request_body, response_body

def apply_template_fallbacks(api_results):
    assigned = 0
    for api in api_results:
        req, res = get_fallback_payload(api["method"], api["path"])
        
        # Check if we have a weak response (e.g. "dummy" string, entirely empty, or missing items)
        resp = api.get("response_body")
        is_weak = False
        
        if not resp or resp == "dummy" or resp == "string" or resp == {}:
            is_weak = True

        if is_weak:
            if not api.get("request_body"):
                api["request_body"] = req
            api["response_body"] = res
            assigned += 1
        elif isinstance(resp, dict):
            # If it's a GET list collection, force populate items if missing or empty
            if api["method"] == "GET" and "{" not in api["path"]:
                if "items" not in resp or not resp["items"] or (isinstance(resp["items"], list) and len(resp["items"]) > 0 and not resp["items"][0]):
                    resp["items"] = res.get("items", [])
                    assigned += 1
            elif api["method"] == "GET" and "{" in api["path"]:
                 # If it's a single item, verify it's not mostly blank
                 keys = [k for k in resp.keys() if k not in ["type", "id", "name", "status", "count", "offset", "total"]]
                 # Inject some UUID properties to make it richer if it lacks standard fields
                 if "id" not in resp: resp["id"] = res.get("id")
                 if "name" not in resp: resp["name"] = res.get("name")
                 if "status" not in resp: resp["status"] = res.get("status")
                 if "createdAt" not in resp: resp["createdAt"] = res.get("created")
            
    if assigned > 0:
        print(f"      🟡 Applied offline template generation & UUID patching to {assigned} endpoints.")
    return api_results
