import os

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped == 'if "dynamic_store" not in MOCK_DB:':
            continue
        if stripped == 'MOCK_DB["dynamic_store"] = {}':
            continue
        if stripped == 'if collection_path not in MOCK_DB["dynamic_store"]:':
            continue
        if stripped == 'MOCK_DB["dynamic_store"][collection_path] = {}':
            continue
        new_lines.append(line)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

if __name__ == "__main__":
    base_dir = r"d:\HPE CPP\MCP_Integrated"
    mock_servers = ["mock_server(cloud)", "mock_server(Comops)", "mock_server(network)", "mock_server(oneview)", "mock_server(storage)"]
    
    for srv in mock_servers:
        srv_path = os.path.join(base_dir, srv)
        main_py = os.path.join(srv_path, "main.py")
        if os.path.exists(main_py):
            process_file(main_py)
