import urllib.request
import json
import sys

url = 'http://127.0.0.1:8009/server-agent/execute-task'
data = json.dumps({
    'task_id': '123',
    'task_type': 'server_action',
    'agent_type': 'server',
    'resource_type': 'server',
    'resource_id': '1fd2c8a6-f77c-4d1e-827f-c2240198b9a0',
    'action': 'OFF',
    'provider': 'mock_server'
}).encode('utf-8')
headers = {'Content-Type': 'application/json'}
req = urllib.request.Request(url, data=data, headers=headers)

try:
    response = urllib.request.urlopen(req)
    print(response.read().decode('utf-8'))
except urllib.error.HTTPError as e:
    print(f"HTTP {e.code}: {e.reason}")
    print(e.read().decode('utf-8'))
