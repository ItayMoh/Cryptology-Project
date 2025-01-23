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