from flask import Flask, render_template, request, jsonify
import json
import os
import random
import string

app = Flask(__name__)
VAULT_FILE = "vault.json"

def load_vault():
    if not os.path.exists(VAULT_FILE):
        return {"vault": []}
    try:
        with open(VAULT_FILE, "r") as f:
            data = json.load(f)
            if "vault" not in data:
                data = {"vault": []}
            return data
    except (json.JSONDecodeError, IOError):
        return {"vault": []}

def save_vault(data):
    with open(VAULT_FILE, "w") as f:
        json.dump(data, f, indent=2)

def check_strength(password):
    has_upper   = any(c.isupper()  for c in password)
    has_lower   = any(c.islower()  for c in password)
    has_digit   = any(c.isdigit()  for c in password)
    has_special = any(c in string.punctuation for c in password)
    score = sum([has_upper, has_lower, has_digit, has_special])
    if len(password) < 6 or score <= 1:
        return "Weak"
    if len(password) < 10 or score <= 2:
        return "Medium"
    return "Strong"

def generate_password(length=12):
    chars = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"
    while True:
        pwd = "".join(random.choices(chars, k=length))
        if (any(c.isupper() for c in pwd) and
                any(c.islower() for c in pwd) and
                any(c.isdigit() for c in pwd) and
                any(c in string.punctuation for c in pwd)):
            return pwd

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/credentials", methods=["GET"])
def get_credentials():
    data = load_vault()
    return jsonify(data["vault"])

@app.route("/api/credentials", methods=["POST"])
def add_credential():
    body     = request.get_json()
    site     = body.get("site", "").strip()
    username = body.get("username", "").strip()
    password = body.get("password", "").strip()
    if not site or not username or not password:
        return jsonify({"error": "All fields are required"}), 400
    data   = load_vault()
    new_id = max((e["id"] for e in data["vault"]), default=0) + 1
    entry  = {"id": new_id, "site": site, "username": username,
              "password": password, "strength": check_strength(password)}
    data["vault"].append(entry)
    save_vault(data)
    return jsonify(entry), 201

@app.route("/api/credentials/<int:entry_id>", methods=["PUT"])
def edit_credential(entry_id):
    body     = request.get_json()
    site     = body.get("site", "").strip()
    username = body.get("username", "").strip()
    password = body.get("password", "").strip()
    if not site or not username or not password:
        return jsonify({"error": "All fields are required"}), 400
    data = load_vault()
    for entry in data["vault"]:
        if entry["id"] == entry_id:
            entry["site"]     = site
            entry["username"] = username
            entry["password"] = password
            entry["strength"] = check_strength(password)
            save_vault(data)
            return jsonify(entry)
    return jsonify({"error": "Entry not found"}), 404

@app.route("/api/credentials/<int:entry_id>", methods=["DELETE"])
def delete_credential(entry_id):
    data = load_vault()
    original_len = len(data["vault"])
    data["vault"] = [e for e in data["vault"] if e["id"] != entry_id]
    if len(data["vault"]) == original_len:
        return jsonify({"error": "Entry not found"}), 404
    save_vault(data)
    return jsonify({"message": "Deleted successfully"})

@app.route("/api/generate-password", methods=["GET"])
def api_generate_password():
    pwd = generate_password(12)
    return jsonify({"password": pwd, "strength": check_strength(pwd)})

@app.route("/api/check-strength", methods=["POST"])
def api_check_strength():
    body = request.get_json()
    pwd  = body.get("password", "")
    return jsonify({"strength": check_strength(pwd)})

if __name__ == "__main__":
    if not os.path.exists(VAULT_FILE):
        save_vault({"vault": []})
        print(f"✅ Created empty {VAULT_FILE}")
    app.run(debug=True)