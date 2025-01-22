from struct import pack, unpack
import os

# Constants for CAST-256
BLOCK_SIZE = 16  # 128 bits
KEY_SIZES = [16, 20, 24, 32]  # Valid key sizes
NUM_ROUNDS = 48  # Number of rounds in CAST-256

# Simplified S-boxes (placeholders for full implementation)
S_BOXES = [[i for i in range(256)] for _ in range(4)]

def rotate_left(value, shift, size=32):
    return ((value << shift) & (2**size - 1)) | (value >> (size - shift))

def rotate_right(value, shift, size=32):
    return (value >> shift) | ((value << (size - shift)) & (2**size - 1))

# Simplified CAST-256 key schedule (placeholder for full implementation)
def key_schedule(key):
    return [unpack('<I', key[i:i+4])[0] for i in range(0, len(key), 4)]

# Simplified CAST-256 encryption function (single block)
def cast256_encrypt_block(block, subkeys):
    A, B, C, D = unpack('<4I', block)
    for i in range(NUM_ROUNDS):
        if i % 2 == 0:
            A = (A + subkeys[i % len(subkeys)]) & 0xFFFFFFFF
            A = rotate_left(A, 3)
        else:
            B = (B ^ subkeys[i % len(subkeys)]) & 0xFFFFFFFF
            B = rotate_right(B, 5)
        A, B, C, D = D, A, B, C
    return pack('<4I', A, B, C, D)

def cast256_decrypt_block(block, subkeys):
    A, B, C, D = unpack('<4I', block)
    for i in reversed(range(NUM_ROUNDS)):
        A, B, C, D = B, C, D, A
        if i % 2 == 0:
            A = rotate_right(A, 3)
            A = (A - subkeys[i % len(subkeys)]) & 0xFFFFFFFF
        else:
            B = rotate_left(B, 5)
            B = (B ^ subkeys[i % len(subkeys)]) & 0xFFFFFFFF
    return pack('<4I', A, B, C, D)

# OFB mode implementation
def ofb_mode(input_bytes, key, iv, encrypt=True):
    subkeys = key_schedule(key)
    output = bytearray()
    feedback = iv
    for i in range(0, len(input_bytes), BLOCK_SIZE):
        keystream = cast256_encrypt_block(feedback, subkeys)
        chunk = input_bytes[i:i + BLOCK_SIZE]
        output_chunk = bytes(a ^ b for a, b in zip(chunk, keystream))
        output.extend(output_chunk)
        feedback = keystream
    return bytes(output)

# File encryption and decryption
def encrypt_file(input_file, output_file, key):
    if len(key) not in KEY_SIZES:
        raise ValueError("Key size must be 16, 20, 24, or 32 bytes.")

    iv = os.urandom(BLOCK_SIZE)
    with open(input_file, 'rb') as f_input, open(output_file, 'wb') as f_output:
        f_output.write(iv)
        plaintext = f_input.read()
        ciphertext = ofb_mode(plaintext, key, iv, encrypt=True)
        f_output.write(ciphertext)

def decrypt_file(input_file, output_file, key):
    if len(key) not in KEY_SIZES:
        raise ValueError("Key size must be 16, 20, 24, or 32 bytes.")

    with open(input_file, 'rb') as f_input:
        iv = f_input.read(BLOCK_SIZE)
        ciphertext = f_input.read()
        plaintext = ofb_mode(ciphertext, key, iv, encrypt=False)
        with open(output_file, 'wb') as f_output:
            f_output.write(plaintext)

# Example usage
if __name__ == "__main__":
    input_mp3 = "example.mp3"
    encrypted_mp3 = "example_encrypted.mp3"
    decrypted_mp3 = "example_decrypted.mp3"

    key = os.urandom(32)

    print("Encrypting...")
    encrypt_file(input_mp3, encrypted_mp3, key)
    print(f"File encrypted and saved to {encrypted_mp3}")

    print("Decrypting...")
    decrypt_file(encrypted_mp3, decrypted_mp3, key)
    print(f"File decrypted and saved to {decrypted_mp3}")
