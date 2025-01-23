import random
import base64
import os
from ec_elgamal import gen_keypair, ec_elgamal_encrypt, ec_elgamal_decrypt, Curve25519 as curve
import CAST256.mode_operation as mode_operation
import rabin

def split_into_blocks(data, block_size):
    blocks = [data[i:i + block_size] for i in range(0, len(data), block_size)]
    if len(blocks[-1]) < block_size:
        remainder = block_size - len(blocks[-1])
        padding = bytes([0] * remainder)  # Zero padding
        blocks[-1] += padding
    return blocks

def integers_to_bytes(int_list, byteorder='big'):
    byte_size = 16
    byte_data = b''.join(i.to_bytes(byte_size, byteorder) for i in int_list)
    return byte_data


# Bob Generates EC ElGamal keys
print("\n>>> Bob generates a pair of EC ElGamal keys <<<")
bob_private_key, bob_public_key = gen_keypair(curve)
print("\n>>> Bob shares his public key with Alice <<<")

# Generate key (256 bit) for CAST256 OFB
print("\n>>> Alice generates private CAST256-OFB key and IV <<<")
alice_private_key = random.getrandbits(256)
iv = random.getrandbits(128)

alice_private_key_in_bytes = alice_private_key.to_bytes(32, byteorder='big')
iv_in_bytes = iv.to_bytes(16, byteorder='big')

message = alice_private_key_in_bytes + iv_in_bytes

# Encrypt the CAST256 key with Bob's public key
print("\n>>> Alice encrypts CAST256-OFB key using EC ElGamal with Bob's public key <<<")
encrypted_key_iv = ec_elgamal_encrypt(bob_public_key, message, curve)

print("\n>>> Alice sends encrypted sound file to Bob with encrypted key and IV <<<")
mp3_file_path = input("Enter the path to the encrypted sound file (make sure without apostrophes): ")
with open(mp3_file_path, 'rb') as mp3_file:
    mp3_data = mp3_file.read()
print("\n>>> Please wait until Alice finishes the Encryption step <<<")

# Encode the image data in Base64
mp3_base64 = base64.b64encode(mp3_data)
mp3_base64_str = base64.b64encode(mp3_data).decode('utf-8')
block_size = 16  # 16 bytes = 128 bits
# Split the Base64 encoded image into blocks
blocks = split_into_blocks(mp3_base64, block_size)
# Convert each block into an integer
blocks_as_integers = [int.from_bytes(block, byteorder="big") for block in blocks]
# Encrypt the image blocks
encrypted_mp3 = mode_operation.encrypt(blocks_as_integers, alice_private_key, iv, "OFB")
encrypted_mp3_data = base64.b64encode(integers_to_bytes(encrypted_mp3))
encrypted_mp3_path = "encrypted_" + os.path.basename(mp3_file_path)
with open(encrypted_mp3_path, 'wb') as encrypted_mp3_file:
    encrypted_mp3_file.write(encrypted_mp3_data)

print(f"\n>>> Encrypted sound saved to {encrypted_mp3_path} <<<")


# Decrypt the CAST256 key and IV with Bob's private key
print("\n>>> Bob decrypts the CAST256 key and IV using EC ElGamal with his private key <<<")
decrypted_key_iv = ec_elgamal_decrypt(bob_private_key, encrypted_key_iv, curve)
decrypted_key = decrypted_key_iv[:32]
decrypted_iv  = decrypted_key_iv[32:32+16]

print("\n>>> Bob decrypts the the sound file <<<")
print("\n>>> Please wait until Bob finishes the Decryption step <<<")
decrypted_mp3 = mode_operation.decrypt(encrypted_mp3, decrypted_key, decrypted_iv, "OFB")
decrypted_mp3_data =  base64.b64decode(integers_to_bytes(decrypted_mp3))
decrypted_mp3_path = "decrypted_" + os.path.basename(mp3_file_path)
with open(decrypted_mp3_path, 'wb') as decrypted_image_file:
    decrypted_image_file.write(decrypted_mp3_data)

print(f"\n>>> Decrypted sound file saved to {decrypted_mp3_path} <<<")

# Generate the Signature for the original sound file (base64-encoded)
signature, padd = rabin.digital_signature(mp3_base64_str)
print(f"\nsigg for the original sound file: {signature}\n")

# Verify the MAC for the base64-encoded decrypted sound file
decrypted_mp3_base64 = base64.b64encode(decrypted_mp3_data).decode('utf-8')
rabin.verification(decrypted_mp3_base64, padd, signature)
