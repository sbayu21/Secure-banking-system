from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, dsa, padding
from cryptography.hazmat.primitives.asymmetric import utils as dsa_utils
from cryptography.exceptions import InvalidSignature

# Load a private key (RSA or DSA) from a PEM file
def load_key(path):
    with open(path, "rb") as f:
        return serialization.load_pem_private_key(f.read(), password=None)

# Alias for compatibility with older import in bank_api.py
load_private_key = load_key

# Load a public key (RSA or DSA) from a PEM file
def load_public_key(path):
    with open(path, "rb") as f:
        return serialization.load_pem_public_key(f.read())

# Load DSA private or public key
def load_dsa_key(path, is_private=True):
    with open(path, "rb") as f:
        return serialization.load_pem_private_key(f.read(), password=None) if is_private else serialization.load_pem_public_key(f.read())

# Encrypt message with RSA public key
def encrypt_message(message, public_key):
    return public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

# Decrypt message with RSA private key
def rsa_decrypt(ciphertext, private_key):
    return private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

# Sign a message with RSA private key
def sign_message(message, private_key):
    return private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

# Verify an RSA signature using public key
def rsa_verify(message, signature, public_key):
    try:
        public_key.verify(
            signature,
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except InvalidSignature:
        return False

# Sign a message using DSA private key
def sign_dsa(message, private_key):
    return private_key.sign(message, hashes.SHA256())

# Verify a DSA signature using public key
def dsa_verify(message, signature, public_key):
    try:
        public_key.verify(signature, message, hashes.SHA256())
        return True
    except InvalidSignature:
        return False
