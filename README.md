# SecureBank System

**CS-352 Final Project – Spring 2025**  
**Professor: Mikhail Gofman**

## Team Members
- **Simegnew Bayu** – Backend Developer  
- **Sagarkumar Patel** – Front-end Developer

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
   
2. Create and activate a virtual environment:
   
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   
3. Install dependencies:

   ```bash
   pip install -r requirements.txt

4. Start the Bank Server:

   ```bash
   python bank_api.py

5. Start the ATM Client:
   ```bash
   python app.py
   
