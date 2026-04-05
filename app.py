from flask import Flask, request, jsonify, abort
import json
from pathlib import Path

app = Flask(__name__)
DATA_FILE = Path("users.json")

# Ensure JSON file exists
if not DATA_FILE.exists():
    DATA_FILE.write_text("[]")

# Helper functions
def read_users():
    with DATA_FILE.open("r") as f:
        return json.load(f)

def write_users(users):
    with DATA_FILE.open("w") as f:
        json.dump(users, f, indent=4)

def get_next_id(users):
    if not users:
        return 1
    return max(user["id"] for user in users) + 1

# CREATE
@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data.get("name") or not data.get("email"):
        return jsonify({"error": "Name and email are required"}), 400

    users = read_users()
    new_user = {
        "id": get_next_id(users),
        "name": data["name"],
        "email": data["email"]
    }
    users.append(new_user)
    write_users(users)
    return jsonify(new_user), 201

# READ ALL
@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(read_users())

# READ ONE
@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    users = read_users()
    for user in users:
        if user["id"] == user_id:
            return jsonify(user)
    abort(404, description="User not found")

# UPDATE
@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()
    users = read_users()
    for user in users:
        if user["id"] == user_id:
            if "name" in data:
                user["name"] = data["name"]
            if "email" in data:
                user["email"] = data["email"]
            write_users(users)
            return jsonify(user)
    abort(404, description="User not found")

# DELETE
@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    users = read_users()
    new_users = [user for user in users if user["id"] != user_id]
    if len(new_users) == len(users):
        abort(404, description="User not found")
    write_users(new_users)
    return jsonify({"message": "User deleted successfully"})

# Run the server
if __name__ == "__main__":
    app.run(debug=True)