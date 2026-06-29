import re

path = 'd:/HPE CPP/MCP_Integrated/mcp_server/mcp_server.py'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('elif provider_or_protocol in {\"mock_server\", \"oneview\"}:\n                  agent_type = \"server\"', 'elif provider_or_protocol == \"mock_server\":\n                  agent_type = \"server\"\n              elif provider_or_protocol in {\"oneview\", \"coms\"}:\n                  agent_type = \"onprem\"')

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)

print('Patched agent_type mapping')
