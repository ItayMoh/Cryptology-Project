import random
import base64
import os
import time
import pickle
import common
from cleanup import cleanup_bob
from ec_elgamal import gen_keypair, ec_elgamal_decrypt, Curve25519 as curve
import CAST256.mode_operation as mode_operation
import rabin

current_dir = os.path.abspath(os.getcwd())

#cleaning up previous run
cleanup_bob()

# Bob Generates EC ElGamal keys
print("\n>>> Bob generates a pair of EC ElGamal keys <<<")
bob_private_key, bob_public_key = gen_keypair(curve)
print("\n>>> Bob shares his public key with Alice <<<")

with open(f"{current_dir}/bob_public_key.pkl", "wb") as f:
    pickle.dump(bob_public_key, f)
    f.close()

mp3_file_path = input("Enter the path to the encrypted sound file (make sure without apostrophes): ")

while not os.path.isfile(f"{current_dir}/encrypted_{os.path.basename(mp3_file_path)}"):
    print("Waiting for Alice sound to be encrypted")
    time.sleep(10)


with open(f"{current_dir}/alice_encrypted_private.pkl", "rb") as f:
    encrypted_key_iv = pickle.load(f)
    f.close()

with open(f"{current_dir}/encrypted_{os.path.basename(mp3_file_path)}", 'rb') as mp3_file:
    encrypted_mp3_encoded = mp3_file.read()

# Decode the Base64-encoded data
encrypted_mp3_data = base64.b64decode(encrypted_mp3_encoded)

#Split it back to encrypted blocks
block_size = 16  # Block size in bytes (used during encryption)
encrypted_blocks = common.bytes_to_integers(encrypted_mp3_data, block_size)

# Decrypt the CAST256 key and IV with Bob's private key
print("\n>>> Bob decrypts the CAST256 key and IV using EC ElGamal with his private key <<<")
decrypted_key_iv = ec_elgamal_decrypt(bob_private_key, encrypted_key_iv, curve)

#Extract the decrypted key and iv in bytes
decrypted_key = decrypted_key_iv[:32]
decrypted_iv  = decrypted_key_iv[32:32+16]

print("\n>>> Bob decrypts the the sound file <<<")
print("\n>>> Please wait until Bob finishes the Decryption step <<<")
decrypted_mp3 = mode_operation.decrypt(encrypted_blocks, decrypted_key, decrypted_iv, "OFB")
decrypted_data_bytes = common.integers_to_bytes(decrypted_mp3)
original_mp3_data = base64.b64decode(decrypted_data_bytes)


decrypted_mp3_path = "decrypted_" + os.path.basename(mp3_file_path)
with open(decrypted_mp3_path, 'wb') as decrypted_sound_file:
    decrypted_sound_file.write(original_mp3_data)

print(f"\n>>> Decrypted sound file saved to {decrypted_mp3_path} <<<")


#Checking file signature
with open(f"{current_dir}/signature.pkl", "rb") as f:
    signature = pickle.load(f)
    f.close()

with open(f"{current_dir}/padd.pkl", "rb") as f:
    padd = pickle.load(f)
    f.close()

with open(decrypted_mp3_path, 'rb') as mp3_file:
    mp3_data = mp3_file.read()

# Verify the MAC for the base64-encoded decrypted sound file
decrypted_mp3_base64 = base64.b64encode(original_mp3_data).decode('utf-8')
rabin.verification(decrypted_mp3_base64, padd, signature)

