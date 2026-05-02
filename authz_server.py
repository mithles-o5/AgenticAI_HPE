from flask import Flask, request, jsonify
import jwt

app = Flask(__name__)

SECRET_KEY = "my_secret_key"

ACCESS_CONTROL = {
    "user1": ["cloud"],
    "user2": ["oneview"],
    "user3": ["cloud", "oneview"]
}

def verify_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except Exception:
        return None

@app.route('/authorize', methods=['POST'])
def authorize():
    auth_header = request.headers.get("Authorization")
    data = request.json
    resource = data.get("resource")

    # FIX 4: Strip "Bearer " prefix before decoding
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"message": "Token missing or malformed"}), 401

    token = auth_header.split(" ")[1]
    user = verify_token(token)

    if not user:
        return jsonify({"message": "Invalid token"}), 403

    # FIX 1: Use "user" key (matches what auth_server.py encodes)
    username = user["user"]

    if resource in ACCESS_CONTROL.get(username, []): 
        return jsonify({"message": f"Access granted to {resource}"})
    else:
        return jsonify({"message": f"Access denied to {resource}"}), 403


# FIX 2: Added __name__ guard
# FIX 3: Changed port to 5000 (avoids clash with mcp_server on 4000)
if __name__ == '__main__':
    app.run(port=5000, debug=True)