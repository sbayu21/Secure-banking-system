from flask import Flask, request, jsonify
from utils.crypto_utils import (
    load_private_key, load_public_key,
    rsa_decrypt, rsa_verify, dsa_verify
)
import os, json
from base64 import b64decode

app = Flask(__name__)
DATA_PATH = "user_db.json"

# Load keys
BANK_PRIV_KEY = load_private_key("certs/bank_private.pem")

# Load user database
def load_users():
    if not os.path.exists(DATA_PATH):
        return {}
    with open(DATA_PATH, "r") as f:
        return json.load(f)

def save_users(users):
    with open(DATA_PATH, "w") as f:
        json.dump(users, f, indent=4)

# ---------------------- SIGNUP --------------------------
@app.route("/api/signup", methods=["POST"])
def signup():
    data = request.json
    user_id = data.get("user_id")
    password = data.get("password")
    users = load_users()

    if user_id in users:
        return jsonify({"status": "fail", "message": "User ID already exists"})

    users[user_id] = {
        "password": password,
        "balance": 0,
        "activity": []
    }
    save_users(users)
    return jsonify({"status": "ok", "message": "User created"})

# ---------------------- LOGIN ---------------------------
@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    atm_id = data["atm_id"]
    encrypted = bytes.fromhex(data["encrypted"])
    signature = bytes.fromhex(data["signature"])
    sig_type = data["signature_type"]

    try:
        decrypted = rsa_decrypt(encrypted, BANK_PRIV_KEY).decode()
        atm_check, user_id, password = decrypted.split(":")
        print(f"[DEBUG] Decrypted: ATM={atm_check}, user_id={user_id}, pass={password}")
    except Exception as e:
        print("[ERROR] Decryption failed:", e)
        return jsonify({"status": "fail", "message": "Decryption error"})

    pubkey_path = f"certs/{atm_id}_{sig_type}_public.pem"
    if not os.path.exists(pubkey_path):
        print("[ERROR] Missing ATM public key file:", pubkey_path)
        return jsonify({"status": "fail", "message": "ATM not registered"})

    atm_pub = load_public_key(pubkey_path)

    # Signature check
    if sig_type == "rsa":
        verified = rsa_verify(decrypted.encode(), signature, atm_pub)
    else:
        verified = dsa_verify(decrypted.encode(), signature, atm_pub)

    if not verified:
        print("[ERROR] Signature verification failed")
        return jsonify({"status": "fail", "message": "Signature verification failed"})

    # Validate user
    users = load_users()
    print(f"[DEBUG] Checking user DB for {user_id}")
    if user_id not in users:
        print("[ERROR] User not found")
        return jsonify({"status": "fail", "message": "Invalid credentials"})
    if users[user_id]["password"] != password:
        print("[ERROR] Password mismatch")
        return jsonify({"status": "fail", "message": "Invalid credentials"})

    return jsonify({"status": "ok", "message": "Login successful"})


# --------------------- ACTION ---------------------------
@app.route("/api/action", methods=["POST"])
def action():
    data = request.json
    atm_id = data["atm_id"]
    user_id = data["user_id"]
    sig_type = data["signature_type"]
    command = data["command"]
    encrypted = bytes.fromhex(data["encrypted"])
    signature = bytes.fromhex(data["signature"])

    try:
        decrypted = rsa_decrypt(encrypted, BANK_PRIV_KEY).decode()
    except Exception:
        return jsonify({"status": "fail", "message": "Decryption failed"})

    # Verify the command matches decrypted text
    if decrypted != command:
        return jsonify({"status": "fail", "message": "Tampered command"})

    atm_pub = load_public_key(f"certs/{atm_id}_{sig_type}_public.pem")

    if sig_type == "rsa":
        verified = rsa_verify(decrypted.encode(), signature, atm_pub)
    else:
        verified = dsa_verify(decrypted.encode(), signature, atm_pub)

    if not verified:
        return jsonify({"status": "fail", "message": "Signature invalid"})

    users = load_users()
    if user_id not in users:
        return jsonify({"status": "fail", "message": "User not found"})

    # --- Perform command ---
    user = users[user_id]
    response = ""
    if command == "balance":
        response = f"Balance: ${user['balance']}"
    elif command == "deposit":
        user["balance"] += 100  # Fixed deposit
        user["activity"].append({"action": "deposit", "amount": 100})
        response = "Deposited $100"
    elif command == "withdraw":
        if user["balance"] >= 50:
            user["balance"] -= 50
            user["activity"].append({"action": "withdraw", "amount": 50})
            response = "Withdrew $50"
        else:
            response = "Insufficient balance"
    elif command == "activity":
        activity = user.get("activity", [])
        if not activity:
            response = "No recent activity"
        else:
            response = "\n".join([f"{a['action']}: ${a['amount']}" for a in activity])
    elif command == "quit":
        response = "Session ended"
    else:
        response = "Unknown command"

    save_users(users)
    return jsonify({"status": "ok", "message": response})

# ------------------- MAIN ----------------------------
if __name__ == "__main__":
    app.run(port=1200, debug=True)
