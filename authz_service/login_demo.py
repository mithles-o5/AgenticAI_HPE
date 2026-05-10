import sys
from utils import generate_id_token

DEMO_USERS = {
    "Mahasriya": {
        "name": "Mahasriya Somalinga",
        "email": "mahasriya@company.com",
        "role": "operator"
    },
    "Kishore": {
        "name": "Kishore Raj",
        "email": "kishore@company.com",
        "role": "admin"
    },
    "Arun": {
        "name": "Arun Kumar",
        "email": "arun@company.com",
        "role": "senior_admin"
    }
}

def main():
    if len(sys.argv) < 2:
        print("Usage: python login_demo.py [Mahasriya|Kishore|Arun]")
        return

    user_key = sys.argv[1]
    if user_key not in DEMO_USERS:
        print(f"Error: Unknown user '{user_key}'")
        return

    user = DEMO_USERS[user_key]
    token = generate_id_token(user['name'], user['email'], user['role'])

    print("\n--- LOGIN SIMULATION SUCCESS ---")
    print(f"User:  {user['name']}")
    print(f"Role:  {user['role']}")
    print("-" * 32)
    print("Add this to your Claude Desktop config 'env' section:")
    print("-" * 32)
    print(f' "AUTHZ_ID_TOKEN": "{token}"')
    print("-" * 32)

if __name__ == "__main__":
    main()
