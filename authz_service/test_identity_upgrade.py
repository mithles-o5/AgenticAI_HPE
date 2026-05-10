import httpx
import time
import subprocess
import os
import json
from utils import generate_id_token

def test_identity_flow():
    print("--- [IDENTITY UPGRADE TEST] ---")
    
    # Start the Unified Backend
    server_process = subprocess.Popen(
        ["python", "main.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    time.sleep(3) # Boot delay

    BASE_URL = "http://127.0.0.1:8001"

    def check_auth(token, action, env, label):
        payload = {
            "token": token,
            "action": action,
            "resource": {"id": "server01", "env": env, "vendor": "HPE"},
            "context": {"time": "12:00", "location": "test-script"}
        }
        res = httpx.post(f"{BASE_URL}/authorize", json=payload)
        if res.status_code != 200:
            print(f"ERROR {res.status_code}: {res.text}")
        data = res.json()
        print(f"User: {label:25} | Action: {action:8} | Env: {env:10} | Decision: {data.get('decision', 'NO_DECISION')}:6 | Reason: {data.get('reason')}")
        return data.get('decision')

    try:
        # Generate Tokens for scenarios based on roles.json
        op_token = generate_id_token("Mahasriya Somalinga", "mahasriya@company.com", "operator")
        admin_token = generate_id_token("Kishore Raj", "kishore@company.com", "admin")
        snr_token = generate_id_token("Arun Kumar", "arun@company.com", "senior_admin")
        hacker_token = generate_id_token("Hacker", "stranger@hacker.com", "admin")

        # Scenario 1: Operator (View Only)
        check_auth(op_token, "view", "dev", "Mahasriya")
        check_auth(op_token, "restart", "dev", "Mahasriya") # Deny

        # Scenario 2: Admin (Full Dev, Restricted Prod)
        check_auth(admin_token, "restart", "dev", "Kishore")
        check_auth(admin_token, "restart", "production", "Kishore") # Deny

        # Scenario 3: Senior Admin (Full Prod Access)
        check_auth(snr_token, "restart", "production", "Arun")

        # Scenario 4: Unknown User (Reject even if token is valid signed)
        check_auth(hacker_token, "view", "dev", "Hacker")

    finally:
        print("\nStopping Backend...")
        server_process.terminate()

if __name__ == "__main__":
    test_identity_flow()
