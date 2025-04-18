import socket
import threading
from utils.crypto_utils import (
    decrypt_message, verify_signature, verify_dsa_signature,
    load_key, load_dsa_key
)
import os
from datetime import datetime

HOST = '127.0.0.1'
PORT = 1200

# In-memory user database
user_db = {
    "124356": {
        "password": "pass123",
        "balance": 1000,
        "history": []
    },
    "654321": {
        "password": "abc321",
        "balance": 2500,
        "history": []
    }
}

# Load bank's private RSA key
bank_private_key = load_key("certs/bank_private.pem")

# Load ATM public keys (RSA and DSA)
atm_keys = {
    "atm1": {
        "rsa": load_key("certs/atm1_public.pem"),
        "dsa": load_dsa_key("certs/atm1_dsa_public.pem", is_private=False)
    },
    "atm2": {
        "rsa": load_key("certs/atm2_public.pem"),
        "dsa": load_dsa_key("certs/atm2_dsa_public.pem", is_private=False)
    }
}

# Create log directory
os.makedirs("logs", exist_ok=True)

def log_transaction(user_id, atm_id, action):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {atm_id} {user_id}: {action}"
    print(entry)

    user_db[user_id]["history"].append(entry)

    with open("logs/transactions.log", "a") as f:
        f.write(entry + "\n")

def handle_client(conn, addr):
    print(f"Connected: {addr}")
    try:
        # Step 1: Receive encrypted login
        enc_credentials = conn.recv(4096)
        decrypted = decrypt_message(enc_credentials, bank_private_key).decode()

        try:
            atm_id, user_id, password = decrypted.split(":")
        except ValueError:
            conn.send(b"Invalid login format")
            return

        # Step 2: Authenticate user
        if user_id not in user_db or user_db[user_id]["password"] != password:
            conn.send(b"Authentication failed")
            return

        conn.send(b"Authenticated")

        while True:
            # Step 3: Receive encrypted command
            enc_command = conn.recv(4096)
            if not enc_command:
                break

            # Step 4: Receive signature
            signature = conn.recv(4096)
            if not signature:
                break

            # Step 5: Decrypt command
            command = decrypt_message(enc_command, bank_private_key).decode()

            # Step 6: Verify ATM signature
            signature_type = "dsa" if "dsa" in conn.recv(1024).decode().lower() else "rsa"
            pub_key = atm_keys[atm_id][signature_type]

            verified = (
                verify_dsa_signature(command.encode(), signature, pub_key)
                if signature_type == "dsa"
                else verify_signature(command.encode(), signature, pub_key)
            )

            if not verified:
                conn.send(b"ATM signature verification failed")
                break

            # Step 7: Process command
            if command == "balance":
                response = f"Balance: ${user_db[user_id]['balance']}"
                log_transaction(user_id, atm_id, "Checked balance")
            elif command.startswith("deposit"):
                try:
                    amount = int(command.split()[1])
                    user_db[user_id]['balance'] += amount
                    response = f"Deposited ${amount}"
                    log_transaction(user_id, atm_id, f"Deposited ${amount}")
                except:
                    response = "Invalid deposit amount"
            elif command.startswith("withdraw"):
                try:
                    amount = int(command.split()[1])
                    if user_db[user_id]['balance'] >= amount:
                        user_db[user_id]['balance'] -= amount
                        response = f"Withdrew ${amount}"
                        log_transaction(user_id, atm_id, f"Withdrew ${amount}")
                    else:
                        response = "Insufficient funds"
                except:
                    response = "Invalid withdraw amount"
            elif command == "history":
                history = "\n".join(user_db[user_id]["history"]) or "No transactions yet"
                response = f"Transaction History:\n{history}"
            elif command == "quit":
                response = "Session ended."
                log_transaction(user_id, atm_id, "Session ended")
                conn.send(response.encode())
                break
            else:
                response = "Unknown command"

            conn.send(response.encode())

    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        conn.close()
        print(f"Disconnected: {addr}")

# Start the concurrent server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((HOST, PORT))
    server.listen()
    print(f"[BANK SERVER] Listening on {HOST}:{PORT}...")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()
