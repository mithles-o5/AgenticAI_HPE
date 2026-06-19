import re

with open(r'd:\HPE CPP\MCP_Integrated\mock_server(oneview)\main.py', 'r') as f:
    content = f.read()

# Replace:
#         if not static_item and db.get_static("get_rest_server_hardware_id").get("id") == id:
#             static_item = db.get_static("get_rest_server_hardware_id")
# With:
#         if not static_item:
#             static_item = dict(db.get_static("get_rest_server_hardware_id", {}))
#             if static_item:
#                 static_item["id"] = id
#                 static_item["uuid"] = id

replacement = '''        if not static_item:
            static_item = dict(db.get_static("get_rest_server_hardware_id", {}))
            if static_item:
                static_item["id"] = id
                static_item["uuid"] = id'''

pattern = r'        if not static_item and db\.get_static\("get_rest_server_hardware_id"\)\.get\("id"\) == id:\s+static_item = db\.get_static\("get_rest_server_hardware_id"\)'

new_content = re.sub(pattern, replacement, content)

with open(r'd:\HPE CPP\MCP_Integrated\mock_server(oneview)\main.py', 'w') as f:
    f.write(new_content)

print(f"Replaced {content.count('if not static_item and db.get_static(\"get_rest_server_hardware_id\").get(\"id\") == id:')} occurrences")
