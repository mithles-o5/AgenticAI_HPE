import os
import re

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # The missing blocks
    pattern = r'[ \t]*if "dynamic_store" not in MOCK_DB:\s*MOCK_DB\["dynamic_store"\] = \{\}\s*if collection_path not in MOCK_DB\["dynamic_store"\]:\s*MOCK_DB\["dynamic_store"\]\[collection_path\] = \{\}\s*'
    content = re.sub(pattern, '', content)

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
