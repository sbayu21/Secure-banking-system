from flask import Flask, render_template, request, redirect, session, url_for
import os
import sys
import requests

# Add utils to path for crypto imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "utils")))

# Import cryptographic helpers
from crypto_utils import (
    load_key, load_public_key, load_dsa_key,
    encrypt_message, sign_message, sign_dsa
)

# Flask app setup
app = Flask(__name__)
app.secret_key = "super-secure-session-key"

# Backend bank API and key
BANK_API = "http://127.0.0.1:1200/api"
BANK_PUB_KEY = load_public_key("certs/bank_public.pem")

# ATM Login Route
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        atm_id = request.form.get("atm_id")
        user_id = request.form.get("user_id")
        password = request.form.get("password")
        sig_type = request.form.get("signature")

        session["atm_id"] = atm_id
        session["user_id"] = user_id
        session["signature"] = sig_type

        # Encrypt login message with bank's public key
        msg = f"{atm_id}:{user_id}:{password}".encode()
        encrypted = encrypt_message(msg, BANK_PUB_KEY)

        # Sign with ATM's private key (RSA or DSA)
        if sig_type == "rsa":
            priv_key = load_key(f"certs/{atm_id}_private.pem")
            signature = sign_message(msg, priv_key)
        else:
            priv_key = load_dsa_key(f"certs/{atm_id}_dsa_private.pem", is_private=True)
            signature = sign_dsa(msg, priv_key)

        # Send encrypted login to bank server
        res = requests.post(f"{BANK_API}/login", json={
            "atm_id": atm_id,
            "user_id": user_id,
            "signature_type": sig_type,
            "encrypted": encrypted.hex(),
            "signature": signature.hex()
        })

        data = res.json()
        if data.get("status") != "ok":
            return render_template("login.html", error=data.get("message"))

        return redirect("/dashboard")

    return render_template("login.html")

# ATM Dashboard Route
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    result = None
    if request.method == "POST":
        command = request.form.get("command")
        msg = command.encode()
        encrypted = encrypt_message(msg, BANK_PUB_KEY)

        # Sign the command
        if session["signature"] == "rsa":
            priv_key = load_key(f"certs/{session['atm_id']}_private.pem")
            signature = sign_message(msg, priv_key)
        else:
            priv_key = load_dsa_key(f"certs/{session['atm_id']}_dsa_private.pem", is_private=True)
            signature = sign_dsa(msg, priv_key)

        # Send command to bank
        res = requests.post(f"{BANK_API}/action", json={
            "atm_id": session["atm_id"],
            "user_id": session["user_id"],
            "signature_type": session["signature"],
            "command": command,
            "encrypted": encrypted.hex(),
            "signature": signature.hex()
        })
        result = res.json().get("message")

    return render_template("atm_dashboard.html", user_id=session.get("user_id"), result=result)

# Logout clears session
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        user_id = request.form.get("user_id")
        password = request.form.get("password")

        try:
            response = requests.post(f"{BANK_API}/signup", json={
                "user_id": user_id,
                "password": password
            })
            data = response.json()
            if data.get("status") == "ok":
                return redirect("/")
            return render_template("signup.html", error=data.get("message"))
        except Exception as e:
            return render_template("signup.html", error=f"Connection error: {e}")

    return render_template("signup.html")


# Launch the Flask app
if __name__ == "__main__":
    app.run(port=5000, debug=True)
