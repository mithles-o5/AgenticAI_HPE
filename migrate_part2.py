import os
import re

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Init block variations
    content = re.sub(
        r'(\s*if "dynamic_store" not in MOCK_DB:\s*MOCK_DB\["dynamic_store"\] = \{\}\s*if collection_path not in MOCK_DB\["dynamic_store"\]:\s*MOCK_DB\["dynamic_store"\]\[collection_path\] = \{\})',
        '',
        content
    )
    
    # 2. Saving variations
    content = re.sub(
        r'MOCK_DB\["dynamic_store"\]\[collection_path\]\[([^\]]+)\] = ([^\n]+)',
        r'db.upsert_item(collection_path, \1, \2)',
        content
    )
    
    # 3. Store reference
    content = re.sub(
        r'store = MOCK_DB\["dynamic_store"\]\[collection_path\]',
        r'store = db.get_collection(collection_path)',
        content
    )
    
    # 4. Get by ID variations
    content = re.sub(
        r'if "dynamic_store" in MOCK_DB and collection_path in MOCK_DB\["dynamic_store"\] and ([^ ]+) in MOCK_DB\["dynamic_store"\]\[collection_path\]:\s*deleted = MOCK_DB\["dynamic_store"\]\[collection_path\]\.pop\(\1\)',
        r'deleted = db.delete_item(collection_path, \1)',
        content
    )
    
    content = re.sub(
        r'existing = MOCK_DB\["dynamic_store"\]\[collection_path\]\.get\(([^,]+), \{\}\)',
        r'existing = db.get_item(collection_path, \1) or {}',
        content
    )

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
            print(f"Migrated remaining MOCK_DB in {srv}")
