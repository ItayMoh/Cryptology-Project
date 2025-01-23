import random
import base64
import os
import time
import pickle
import common
from ec_elgamal import gen_keypair, ec_elgamal_encrypt, ec_elgamal_decrypt, Curve25519 as curve
import CAST256.mode_operation as mode_operation
import rabin

current_dir = os.path.abspath(os.getcwd())

# Bob Generates EC ElGamal keys
print("\n>>> Bob generates a pair of EC ElGamal keys <<<")
bob_private_key, bob_public_key = gen_keypair(curve)
print("\n>>> Bob shares his public key with Alice <<<")

#Saving bob's public key object on file bob_public_key.txt
with open(f"{current_dir}/bob_public_key.txt", "wb") as f:
    pickle.dump(bob_public_key, f)
    f.close()

mp3_file_path = input("Enter the path to the encrypted sound file (make sure without apostrophes): ")

#Checking if alice already encrypted the desired file
while not os.path.isfile(f"{current_dir}/encrypted_{os.path.basename(mp3_file_path)}"):
    print("Waiting for Alice sound to be encrypted")
    time.sleep(1)

print("Found alice's sound file")

#Takes alice encrypted public key from file alice_encrypted_private.txt
with open(f"{current_dir}/alice_encrypted_private.txt", "rb") as f:
    encrypted_key_iv = pickle.load(f)
    f.close()

#Reading encrypted mp3 file
with open(f"{current_dir}/encrypted_{os.path.basename(mp3_file_path)}", 'rb') as mp3_file:
    encrypted_mp3 = mp3_file.read()

# Decrypt the CAST256 key and IV with Bob's private key
print("\n>>> Bob decrypts the CAST256 key and IV using EC ElGamal with his private key <<<")
decrypted_key_iv = ec_elgamal_decrypt(bob_private_key, encrypted_key_iv, curve)
decrypted_key = decrypted_key_iv[:32]
decrypted_iv  = decrypted_key_iv[32:32+16]
print(decrypted_iv, decrypted_key)

print("\n>>> Bob decrypts the the sound file <<<")
print("\n>>> Please wait until Bob finishes the Decryption step <<<")
decrypted_mp3 = mode_operation.decrypt(encrypted_mp3, decrypted_key, decrypted_iv, "OFB")
decrypted_mp3_data =  base64.b64decode(common.integers_to_bytes(decrypted_mp3))
decrypted_mp3_path = "decrypted_" + os.path.basename(mp3_file_path)
with open(decrypted_mp3_path, 'wb') as decrypted_image_file:
    decrypted_image_file.write(decrypted_mp3_data)

print(f"\n>>> Decrypted sound file saved to {decrypted_mp3_path} <<<")

#Cleaning up environment
print(f"\n>>> Removing  encrypted_{os.path.basename(mp3_file_path)}<<<")
os.remove(f"{current_dir}/encrypted_{os.path.basename(mp3_file_path)}")

print(f"\n>>> Removing Alice encrypted private key {current_dir}/alice_encrypted_private.txt<<<")
os.remove(f"{current_dir}/alice_encrypted_private.txt")

print(f"\n>>> Removing Bob public key {current_dir}/alice_encrypted_private.txt<<<")
os.remove(f"{current_dir}/encrypted_{os.path.basename(mp3_file_path)}")