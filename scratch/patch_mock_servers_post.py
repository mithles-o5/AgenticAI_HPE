import sys
for path, endpoint in [('d:/HPE CPP/MCP_Integrated/mock_server(network)/main.py', '/network/v1/devices/{id}'), ('d:/HPE CPP/MCP_Integrated/mock_server(cloud)/main.py', '/api/v1/devices/{id}')]:
    with open(path, 'r') as f:
        content = f.read()
    if f'@app.post("{endpoint}")' not in content:
        content = content.replace(f'@app.put("{endpoint}")', f'@app.put("{endpoint}")\n@app.post("{endpoint}")')
        with open(path, 'w') as f:
            f.write(content)
        print('Patched', path)
