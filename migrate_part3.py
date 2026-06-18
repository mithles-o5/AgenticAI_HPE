import os

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Just do straightforward string replacement
    s1 = """    if "dynamic_store" not in MOCK_DB:
        MOCK_DB["dynamic_store"] = {}
    if collection_path not in MOCK_DB["dynamic_store"]:
        MOCK_DB["dynamic_store"][collection_path] = {}"""
    content = content.replace(s1, "")
    
    s2 = """        if "dynamic_store" not in MOCK_DB:
            MOCK_DB["dynamic_store"] = {}
        if collection_path not in MOCK_DB["dynamic_store"]:
            MOCK_DB["dynamic_store"][collection_path] = {}"""
    content = content.replace(s2, "")
    
    s3 = """    if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB["dynamic_store"] and item_id in MOCK_DB["dynamic_store"][collection_path]:"""
    s3_replace = """    item = db.get_item(collection_path, item_id)
    if item:"""
    content = content.replace(s3, s3_replace)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    base_dir = r"d:\HPE CPP\MCP_Integrated"
    mock_servers = ["mock_server(cloud)", "mock_server(Comops)", "mock_server(network)", "mock_server(oneview)", "mock_server(storage)"]
    
    for srv in mock_servers:
        srv_path = os.path.join(base_dir, srv)
        main_py = os.path.join(srv_path, "main.py")
        if os.path.exists(main_py):
            process_file(main_py)
            print(f"Migrated part3 MOCK_DB in {srv}")
