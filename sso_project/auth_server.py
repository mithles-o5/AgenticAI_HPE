from flask import Flask, request, jsonify
import jwt
import datetime

app = Flask(__name__)

SECRET_KEY = "my_secret_key"

# Mock users
USERS = {
    "user1": "123",
    "admin": "admin123"
}

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    # Validate user
    if username in USERS and USERS[username] == password:
        token = jwt.encode({
            "user": username,                          # KEY: "user" (must be consistent across all servers)
            "role": "admin" if username == "admin" else "user",
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }, SECRET_KEY, algorithm="HS256")

        return jsonify({"token": token})

    return jsonify({"message": "Invalid credentials"}), 401


if __name__ == '__main__':
    app.run(port=3000, debug=True)