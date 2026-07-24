with open('d:/HPE CPP/MCP_Integrated/mock_server(storage)/main.py', 'r') as f:
    text = f.read()
import re
routes = re.findall(r'@app\.(?:get|post|patch|delete)\(\"(.*?)\"\)', text)
for r in sorted(set(routes)):
    print(r)
