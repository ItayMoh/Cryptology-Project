from CAST256.key_generator import key_generator
from CAST256.functions_cast256 import forward_quad_round, reverse_quad_round

def encrypt_block(message, key):
    """
    This function performs the encryption of a 128-bit block by executing successive rounds of the cast-256
    :param message: the block to be encrypted (128bits)
    :param key: the encryption key (256bits)
    :return: the cryptogram (128bits)
    """
    # Generation of encryption subkeys
    kr, km = key_generator(key)

    # Executing the first 6 rounds (forward_quad_round)
    for i in range(6):
        message = forward_quad_round(message, kr[i], km[i])

    # Run the last 6 rounds in reverse (reverse_quad_round)
    for i in range(6, 12):
        message = reverse_quad_round(message, kr[i], km[i])
    return message


def decrypt_block(cipher, key):
    """
    This function performs the decryption of a 128-bit block by executing successive rounds of the cast-256
    :param cipher: the block to decrypt (128bits)
    :param key: the encryption key (256bits)
    :return: the message (128bits)
    """
    # Generation of encryption subkeys
    kr, km = key_generator(key)

    # Perform the first 6 rounds in reverse (forward_quad_round)
    for i in range(11, 5, -1):
        cipher = forward_quad_round(cipher, kr[i], km[i])

    # Executing the last 6 rounds (reverse_quad_round)
    for i in range(5, -1, -1):
        cipher = reverse_quad_round(cipher, kr[i], km[i])
    return cipher