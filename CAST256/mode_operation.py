import secrets

from CAST256.cast256 import encrypt_block, decrypt_block
import OFB


def rdm_iv_generator():
    """
    This function must be able to generate a 128bit random number
    :return: a randomly generated 128-bit integer.
    """
    return secrets.randbits(128)

def encrypt_cbc(blocks, key):
    """
    This function applies CAST256 encryption to a list of 128-bit blocks following the CBC mode of operation.
    :param blocks: List of blocks to encrypt.
    :param key: 256-bit encryption key
    :return: the list of encrypted blocks with the initial vector used in the first position.
    """
    # Generating a 128-bit random initialization vector
    iv = rdm_iv_generator()

    # List to store encrypted blocks
    encrypted_blocks = [iv]


    previous_block = iv
    for block in blocks:
        # XOR with the previous block (or the initialization vector for the first block)
        block_to_encrypt = block ^ previous_block
        # Block encryption
        encrypted_block = encrypt_block(block_to_encrypt, key)

        # Storing the encrypted block for later use
        encrypted_blocks.append(encrypted_block)

        # Update previous block for next loop
        previous_block = encrypted_block

    return encrypted_blocks


def decrypt_cbc(blocks, key):
    """
    This function decrypts a list of 128-bit blocks that has been previously encrypted
    with the CAST256 method following the CBC operating mode.
    :param blocks: List of blocks to decrypt.
    :param key: 256-bit encryption key
    Same as that used for encryption.
    :return: the list of decrypted blocks.
    """
    # Initialization of initialization vector
    iv = blocks[0]

    # List to store decrypted blocks
    decrypted_blocks = []

    # Decrypt each block using CBC mode
    for block in blocks[1:]:
        # Decrypting the block
        decrypted_block = decrypt_block(block, key)

        # XOR the decrypted block with the previous encrypted block (or the initialization vector for the first block)
        xor_result = decrypted_block ^ iv

        # Adding the resulting block to the list
        decrypted_blocks.append(xor_result)

       # Updates the initialization vector for the next block
        iv = block
    return decrypted_blocks


def decrypt(blocks, key, iv, operation_mode="OFB"):
    if operation_mode.upper() == "OFB".upper():
        return OFB.ofb_decrypt(blocks, key,iv)
    else:
        raise ValueError("Unsupported operating mode.")


def encrypt(blocks, key, iv, operation_mode="OFB"):

    if operation_mode.upper() == "OFB".upper():
        return OFB.ofb_encrypt(blocks, key, iv)
    else:
        raise ValueError("Unsupported operating mode.")