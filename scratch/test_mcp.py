import json
import subprocess

payload = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
        "name": "manage_infrastructure_resource",
        "arguments": {
            "query": "List all servers"
        }
    }
}

p = subprocess.Popen(["python", "mcp_server/mcp_server.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
stdout, stderr = p.communicate(json.dumps(payload) + "\n")

print("STDOUT:")
print(stdout)
print("STDERR:")
print(stderr)
