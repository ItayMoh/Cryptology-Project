import os

current_dir = os.path.abspath(os.getcwd())

#Cleaning up environment

def cleanup_alice():
    if os.path.isfile(f"{current_dir}/alice_encrypted_private.pkl"):
        print(f"\n>>> Removing Alice encrypted private key {current_dir}/alice_encrypted_private.pkl<<<")
        os.remove(f"{current_dir}/alice_encrypted_private.pkl")

    if os.path.isfile(f"{current_dir}/padd.pkl"):
        os.remove(f"{current_dir}/padd.pkl")

    if os.path.isfile(f"{current_dir}/signature.pkl"):
        os.remove(f"{current_dir}/signature.pkl")

def cleanup_bob():
    if os.path.isfile(f"{current_dir}/bob_public_key.pkl"):
        print(f"\n>>> Removing bob's public key {current_dir}/bob_public_key.pkl<<<")
        os.remove(f"{current_dir}/bob_public_key.pkl")
