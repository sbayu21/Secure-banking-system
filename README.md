# SecureBank System

**CS-352 Final Project – Spring 2025**  
**Professor: Mikhail Gofman**

## Team Members
- **Simegnew Bayu**
- **Sagarkumar Patel** 

---

## 📘 Overview

The **SecureBank System** is a secure, distributed banking application that simulates real-world ATM interactions with a central bank server. It ensures strong authentication and encrypted communication using RSA and DSA digital signatures, maintaining the confidentiality, integrity, and authenticity of all transactions.

The system includes:
- One **Bank Server**
- Two **ATM Clients** (CLI and web-based)

---

## 🔐 Features

- Secure login using RSA or DSA digital signatures
- Encrypted communication between ATM and Bank Server (RSA)
- Real-time banking operations: Balance check, Deposit, Withdraw, and Transaction history
- Signature method selection at login (RSA or DSA)
- CLI and web interfaces (with dark mode UI)
- Timestamped transaction logging
- Concurrent handling of multiple ATM sessions
- Robust threat mitigation protocols

---

## 🏗️ System Architecture

### Components

- **Bank Server**: Flask-based REST API handling cryptographic verification and transaction execution.
- **ATM Clients**: 
  - Accept user input and send encrypted/signed messages
  - Support both CLI and browser-based interfaces
- **Database**:
  - `user_db.json`: Stores user credentials (hashed) and balances
  - `transactns.log`: Maintains a log of all operations with timestamps

### Interactions

1. ATM signs and encrypts messages using DSA or RSA.
2. Bank verifies ATM authenticity and decrypts the message.
3. Actions are processed and securely logged.

---

## 🔧 Technologies Used

- **Programming Language**: Python 3.12
- **Framework**: Flask (API & Web UI)
- **Cryptography**: RSA & DSA via `cryptography` library
- **Storage**: JSON files
- **Front-End**: HTML, CSS (with Flask templates)

---

## 🚀 Installation & Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/SecureBank.git
   cd SecureBank
   ```
   
2. Create and activate a virtual environment:
   
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
   
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the Bank Server:

   ```bash
   python bank_api.py
   ```

5. Start the ATM Client:
   ```bash
   python app.py
   ```

   ---

## 🧪 How to Use

- **Login**: Use a 6-digit user ID and password
- **Operations**: Choose from:
  - Balance Inquiry
  - Deposit
  - Withdraw
  - View Activity Log
- **Security**: All requests are digitally signed and encrypted

---

## ⚠️ Notes & Warnings

- **For Educational Use Only**:  
  This project is intended solely for academic purposes in CS-352. It is not production-ready or suitable for real banking environments.

- **No Real Financial Transactions**:  
  The system simulates transactions for learning purposes. It does **not** interface with any actual financial services or networks.

- **Key & Credential Management**:  
  In a real-world system, cryptographic keys and credentials should be stored securely using key vaults or hardware modules. This project uses JSON and local files for simplicity and demonstration only.

- **Security Assumptions**:  
  While strong cryptographic primitives are used (RSA/DSA), aspects like TLS certificates, key expiration, nonce/timestamp verification, and 2FA are **not fully implemented**. These would be necessary in a real deployment.

- **Run Locally in a Safe Environment**:  
  Do not expose the app to the public internet or run it in production-like environments. Localhost testing is strongly recommended.

---

## 📈 Future Enhancements

- Add timestamp/nonce to prevent replay attacks
- Upgrade to SQLite/PostgreSQL backend
- Implement mutual TLS authentication
- Integrate 2FA (OTP or biometric)
- Key rotation and expiration handling
- Role-based access control for bank admin

---

## 🏁 Conclusion

The SecureBank System demonstrates a comprehensive, secure, and user-friendly banking infrastructure. It employs real-world cryptographic techniques to protect sensitive data and enforce strong authentication, making it a practical model for secure financial software.
   
