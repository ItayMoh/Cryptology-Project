from CAST256.cast256 import encrypt_block  # Importing encrypt_block for encryption


def ofb_encrypt(int_blocks, key, iv):
    """
    Encrypts using OFB mode with integer blocks.

    Args:
        int_blocks (list of int): A list of integer blocks to encrypt.
        key (bytes): The encryption key.
        iv (bytes): The initialization vector.

    Returns:
        list of int: The encrypted integer blocks.
    """
    prev_output = iv
    encrypted_blocks = []

    for block in int_blocks:  # Expecting `block` to be an integer
        encrypted_block = encrypt_block(prev_output, key)  # Encrypt the previous output
        xor_result = block ^ encrypted_block  # XOR the integer block with the encrypted block
        encrypted_blocks.append(xor_result)  # Store the encrypted integer block
        prev_output = encrypted_block  # Update the previous output

    return encrypted_blocks



def ofb_decrypt(encrypted_blocks, key, iv):
    """
    Decrypts using OFB mode with integer blocks.

    Args:
        encrypted_blocks (list of int): A list of encrypted integer blocks.
        key (bytes): The encryption key.
        iv (bytes): The initialization vector.

    Returns:
        list of int: The decrypted integer blocks (plaintext blocks).
    """
    prev_output = iv
    decrypted_blocks = []

    for block in encrypted_blocks:  # Expecting `block` to be an integer
        encrypted_block = encrypt_block(prev_output, key)  # Encrypt the previous output
        xor_result = block ^ encrypted_block  # XOR the encrypted block with the key stream
        decrypted_blocks.append(xor_result)  # Store the decrypted integer block
        prev_output = encrypted_block  # Update the previous output

    return decrypted_blocks





def split_plaintext_to_hex_blocks(plaintext):
    blocks_list = []
    for i in range(0, len(plaintext), 16):
        block = plaintext[i:i + 16].ljust(16, "\0")
        hex_value = hex(int.from_bytes(block.encode('utf-8'), 'big'))[2:]
        blocks_list.append(hex_value.zfill(32))
    return blocks_list
