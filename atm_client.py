import requests
import os, sys

# Add 'utils/' directory to path for module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "utils")))

from utils.crypto_utils import (
    load_public_key, load_dsa_key, load_key,
    encrypt_message, sign_message, sign_dsa
)

# Bank server API URL and its RSA public key
BANK_URL = "http://127.0.0.1:1200/api"
BANK_PUB_KEY = load_public_key("certs/bank_public.pem")

def atm_login(atm_id, user_id, password, sig_type):
    """
    Send encrypted and signed login request to the bank.
    """
    message = f"{atm_id}:{user_id}:{password}".encode()
    encrypted = encrypt_message(message, BANK_PUB_KEY)

    # Choose signature method: RSA or DSA
    if sig_type == "rsa":
        priv_key = load_key(f"certs/{atm_id}_private.pem")
        signature = sign_message(message, priv_key)
    else:
        priv_key = load_dsa_key(f"certs/{atm_id}_dsa_private.pem", is_private=True)
        signature = sign_dsa(message, priv_key)

    response = requests.post(f"{BANK_URL}/login", json={
        "atm_id": atm_id,
        "signature_type": sig_type,
        "encrypted": encrypted.hex(),
        "signature": signature.hex()
    })

    return response.json()

def send_command(atm_id, user_id, command, sig_type):
    """
    Send encrypted and signed banking action command to the bank.
    """
    message = command.encode()
    encrypted = encrypt_message(message, BANK_PUB_KEY)

    # Sign command using the selected method
    if sig_type == "rsa":
        priv_key = load_key(f"certs/{atm_id}_private.pem")
        signature = sign_message(message, priv_key)
    else:
        priv_key = load_dsa_key(f"certs/{atm_id}_dsa_private.pem", is_private=True)
        signature = sign_dsa(message, priv_key)

    response = requests.post(f"{BANK_URL}/action", json={
        "atm_id": atm_id,
        "user_id": user_id,
        "signature_type": sig_type,
        "command": command,
        "encrypted": encrypted.hex(),
        "signature": signature.hex()
    })

    return response.json()

def start_atm(atm_id):
    """
    Start ATM interface and handle secure login and command flow.
    """
    print(f"\n--- {atm_id.upper()} ATM SESSION ---")

    user_id = input("Customer ID (6-digit): ").strip()
    password = input("Password: ").strip()
    sig_type = input("Signature method (rsa or dsa): ").strip().lower()

    login_result = atm_login(atm_id, user_id, password, sig_type)
    if login_result.get("status") != "ok":
        print("Login failed:", login_result.get("message"))
        return

    print("Login successful.")

    while True:
        print("\nChoose an action:")
        print("1. balance")
        print("2. deposit")
        print("3. withdraw")
        print("4. activity")
        print("5. quit")

        choice = input("Choice (1–5): ").strip()
        command = {
            "1": "balance",
            "2": "deposit",
            "3": "withdraw",
            "4": "activity",
            "5": "quit"
        }.get(choice)

        if not command:
            print("Invalid selection.")
            continue

        result = send_command(atm_id, user_id, command, sig_type)
        print("Response:", result.get("message"))

        if command == "quit":
            break

# If this script is run directly, ask which ATM to start
if __name__ == "__main__":
    atm_id = input("Run as ATM1 or ATM2? (enter 'atm1' or 'atm2'): ").strip().lower()
    if atm_id in ["atm1", "atm2"]:
        start_atm(atm_id)
    else:
        print("Invalid ATM ID. Please use 'atm1' or 'atm2'.")
