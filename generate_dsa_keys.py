from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import dsa
import os

def generate_dsa_keypair(name):
    private_key = dsa.generate_private_key(key_size=2048)
    public_key = private_key.public_key()

    with open(f"certs/{name}_dsa_private.pem", "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

    with open(f"certs/{name}_dsa_public.pem", "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

if __name__ == "__main__":
    os.makedirs("certs", exist_ok=True)
    generate_dsa_keypair("atm1")
    generate_dsa_keypair("atm2")
    generate_dsa_keypair("bank")
    print("✅ DSA keypairs generated for atm1, atm2, and bank.")
