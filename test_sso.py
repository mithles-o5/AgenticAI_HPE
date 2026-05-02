import urllib.request
import json
import sys

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

# 1. Login to Auth Server
login_url = "http://127.0.0.1:3000/login"
login_data = json.dumps({"username": "admin", "password": "admin123"}).encode("utf-8")
login_req = urllib.request.Request(login_url, data=login_data, headers={"Content-Type": "application/json"})

print("[Step 1] Sending Login Request to Auth Server...")
try:
    with urllib.request.urlopen(login_req) as response:
        login_resp_data = json.loads(response.read().decode())
        token = login_resp_data.get("token")
        print(" -> Login Successful! Received Token:")
        print(f"    {token}\n")
except Exception as e:
    print(" -> Login Failed:", e)
    exit(1)

# 2. Access MCP Server with Token
# FIX 5 (test): Changed to POST to match updated /execute endpoint
mcp_url = "http://127.0.0.1:4000/execute"
mcp_req = urllib.request.Request(
    mcp_url,
    data=b"{}",                                      # POST requires a body (even if empty)
    headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
)

print("[Step 2] Sending Execution Request to MCP Server with Token...")
try:
    with urllib.request.urlopen(mcp_req) as response:
        mcp_resp_data = json.loads(response.read().decode())
        print(" -> MCP Execution Successful! Response:")
        print("    ", json.dumps(mcp_resp_data, indent=2))
except urllib.error.HTTPError as e:
    print(f" -> MCP Request Failed with HTTP {e.code}: {e.read().decode()}")
except Exception as e:
    print(" -> MCP Request Failed:", e)

# 3. Test Access Denied (user1)
print("\n[Step 3] Testing 'user1' to verify Role-Based Access Denied...")
user_login_data = json.dumps({"username": "user1", "password": "123"}).encode("utf-8")
user_login_req = urllib.request.Request(login_url, data=user_login_data, headers={"Content-Type": "application/json"})

with urllib.request.urlopen(user_login_req) as response:
    user_token = json.loads(response.read().decode()).get("token")

# FIX 5 (test): POST for user denial test too
user_mcp_req = urllib.request.Request(
    mcp_url,
    data=b"{}",
    headers={
        "Authorization": f"Bearer {user_token}",
        "Content-Type": "application/json"
    }
)
try:
    urllib.request.urlopen(user_mcp_req)
except urllib.error.HTTPError as e:
    print(f" -> Access Correctly Denied! Received HTTP {e.code}: {e.read().decode()}")