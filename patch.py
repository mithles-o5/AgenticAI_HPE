import re

path = 'd:/HPE CPP/MCP_Integrated/mcp_server/mcp_server.py'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('\"category\": task.category\n        })', '\"category\": task.category,\n            \"management_source_hint\": management_source_hint\n        })')

text = text.replace('\"category\": task.category\n                  })', '\"category\": task.category,\n                      \"management_source_hint\": management_source_hint\n                  })')


text = text.replace('\"category\": \"Operational\"\n              })', '\"category\": \"Operational\",\n                  \"management_source_hint\": management_source_hint\n              })')

text = text.replace('\"category\": \"Operational\"\n                  })', '\"category\": \"Operational\",\n                      \"management_source_hint\": management_source_hint\n                  })')


with open(path, 'w', encoding='utf-8') as f:
    f.write(text)

print('Success')
