import random
import base64
import os
import pickle
import common
from ec_elgamal import ec_elgamal_encrypt, Curve25519 as curve
import CAST256.mode_operation as mode_operation
from cleanup import cleanup_alice
import rabin
import time

current_dir = os.path.abspath(os.getcwd())

#cleanup_alice()

# Generate key (256 bit) for CAST256 OFB
print("\n>>> Alice generates private CAST256-OFB key and IV <<<")
alice_private_key = random.getrandbits(256)
iv = random.getrandbits(128)

alice_private_key_in_bytes = alice_private_key.to_bytes(32, byteorder='big')
iv_in_bytes = iv.to_bytes(16, byteorder='big')

message = alice_private_key_in_bytes + iv_in_bytes

while not os.path.isfile(f"{current_dir}/bob_public_key.pkl"):
    print("Waiting for bob's public key to be generated...")
    time.sleep(1)

with open(f"{current_dir}/bob_public_key.pkl", "rb") as f:
    bob_public_key = pickle.load(f)
    f.close()

print("Bob has shared his Elgamal public key with alice at bob_public_key.txt")
print("\n\n\n\n")

# Encrypt the CAST256 key with Bob's public key
print("\n>>> Alice encrypts CAST256-OFB key using EC ElGamal with Bob's public key <<<")
encrypted_key_iv = ec_elgamal_encrypt(bob_public_key, message, curve)

#Writing Alice's encrypted private key
with open(f"{current_dir}/alice_encrypted_private.pkl", "wb") as f:
    pickle.dump(encrypted_key_iv, f)
    f.close()

print("\n>>> Alice sends encrypted sound file to Bob with encrypted key and IV <<<")
mp3_file_path = input("Enter the path to the encrypted sound file (make sure without apostrophes): ")
with open(mp3_file_path, 'rb') as mp3_file:
    mp3_data = mp3_file.read()
print("\n>>> Please wait until Alice finishes the Encryption step <<<")

# Encode the sound data in Base64
mp3_base64 = base64.b64encode(mp3_data)
mp3_base64_str = base64.b64encode(mp3_data).decode('utf-8')
block_size = 16  # 16 bytes = 128 bits
# Split the Base64 encoded sound into blocks
blocks = common.split_into_blocks(mp3_base64, block_size)
# Convert each block into an integer
blocks_as_integers = [int.from_bytes(block, byteorder="big") for block in blocks]

# Encrypt the sound blocks
encrypted_mp3 = mode_operation.encrypt(blocks_as_integers, alice_private_key, iv, "OFB")
encrypted_mp3_data = base64.b64encode(common.integers_to_bytes(encrypted_mp3))

mp3_base64_str_for_signature = base64.b64encode(mp3_data).decode('utf-8')

encrypted_mp3_path = "encrypted_" + os.path.basename(mp3_file_path)
with open(encrypted_mp3_path, 'wb') as encrypted_mp3_file:
    encrypted_mp3_file.write(encrypted_mp3_data)

print(f"\n>>> Encrypted sound saved to {encrypted_mp3_path} <<<")

# Generate the Signature for the original sound file (base64-encoded)
signature, padd = rabin.digital_signature(mp3_base64_str)
print(f"\nsigg for the original sound file: {signature}\n")

#Writing padd and signature
with open(f"{current_dir}/signature.pkl", "wb") as f:
    pickle.dump(signature, f)
    f.close()

with open(f"{current_dir}/padd.pkl", "wb") as f:
    pickle.dump(padd, f)
    f.close()