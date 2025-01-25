import OFB


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