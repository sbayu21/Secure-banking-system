from Crypto.PublicKey import RSA
import os

CERTS_DIR = os.path.join(os.path.dirname(__file__), "..", "certs")

def generate_keys(name, bits=2048):
    key = RSA.generate(bits)
    private_key = key.export_key()
    public_key = key.publickey().export_key()

    with open(os.path.join(CERTS_DIR, f"{name}_private.pem"), "wb") as priv_file:
        priv_file.write(private_key)

    with open(os.path.join(CERTS_DIR, f"{name}_public.pem"), "wb") as pub_file:
        pub_file.write(public_key)

if __name__ == "__main__":
    os.makedirs(CERTS_DIR, exist_ok=True)
    for identity in ["bank", "atm1", "atm2"]:
        generate_keys(identity)

    print("✔ All RSA key pairs have been generated in the 'certs/' folder.")
