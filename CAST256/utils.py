"""
This file includes a series of useful functions that perform basic arithmetic and binary operations
"""


def sum_mod_232(a, b):
    """
    This function performs a sum in a space modulo 2 to the power of 32
    :param a: first term
    :param b: second term
    :return: the sum modulo 2 to the power of 32
    """
    return (a + b) % (2 ** 32)


def diff_mod_232(a, b):
    """
    This function performs a difference in a space modulo 2 to the power of 32
    :param a: first term
    :param b: second term
    :return: the difference between the first and second terms modulo 2 to the power of 32
    """
    return (a - b) % (2 ** 32)


def build_128_bit_bloc_from_32_bit_blocs(a, b, c, d):
    """
    This function assembles 32-bit blocks into a single 128-bit block. The blocks in parameters are ordered
    from highest to lowest, that is, in the order of final appearance from left to right
    :param a: 1st 32-bit block
    :param b: 2nd 32-bit block
    :param c: 3rd 32-bit block
    :param d: 4th 32-bit block
    :return: a 128-bit block corresponding to the order 'abcd'
    """
    # Use shift and mask operations to construct the 128-bit block
    return (a << 96) | (b << 64) | (c << 32) | d


def extract_32bit_bloc_from_128(abcd):
    """
    This function breaks a 128-bit block into 4 32-bit blocks. The output blocks are ordered
    from strongest to weakest, that is, in order of appearance starting from left to right
    :param abcd: 128-bit block
    :return: 4 blocks of 32 bits a, b, c, d such that abcd is the starting block
    """
    
    # Convert bytes to int if needed
    if isinstance(abcd, bytes):
        abcd = int.from_bytes(abcd, byteorder='big')
        
    # Mask to extract the lowest 32 bits
    mask = ((1 << 32) - 1)

    # Extracting 32-bit blocks using masking operations
    d = abcd & mask
    c = (abcd >> 32) & mask
    b = (abcd >> 64) & mask
    a = (abcd >> 96) & mask

    return a, b, c, d


def extract_32bit_bloc_from_256(abcdefgh):
    """
    This function decomposes a 256-bit block into 8 blocks of 32 bits. The output blocks are ordered
    from highest to lowest, that is, in the order of appearance from left to right
    :param abcdefgh: 128-bit block
    :return: 4 blocks of 32 bits a, b, c, d, e, f, g, h such that abcdefgh is the starting block
    """
    # Convert bytes to int if needed
    if isinstance(abcdefgh, bytes):
        abcdefgh = int.from_bytes(abcdefgh, byteorder='big')
    # Mask to extract the lowest 32 bits
    mask = ((1 << 32) - 1)

    h = abcdefgh & mask
    g = (abcdefgh >> 32) & mask
    f = (abcdefgh >> 64) & mask
    e = (abcdefgh >> 96) & mask
    d = (abcdefgh >> 128) & mask
    c = (abcdefgh >> 160) & mask
    b = (abcdefgh >> 192) & mask
    a = (abcdefgh >> 224) & mask

    return a, b, c, d, e, f, g, h


def build_256_bit_bloc_from_32_bit_blocs(a, b, c, d, e, f, g, h):
    """
    This function assembles 32-bit blocks into a single 256-bit block. The blocks in parameters are ordered
    from highest to lowest, that is, in the order of final appearance from left to right
    :param a: 1st 32-bit block
    :param b: 2nd 32-bit block
    :param c: 3rd 32-bit block
    :param d: 4th 32-bit block
    :param e: 5th 32-bit block
    :param f: 6th 32-bit block
    :param g: 7th 32-bit block
    :param h: 8th 32-bit block
    :return: a 128-bit block corresponding to the order 'abcdefgh'
    """
    return (a << 224) | (b << 192) | (c << 160) | (d << 128) | (e << 96) | (f << 64) | (g << 32) | h


def extract_8bit_blocs_from_32(abcd):
    """
    This function decomposes a 32-bit block into 4 blocks of 8 bits. The output blocks are ordered
    from highest to lowest, that is, in the order of appearance from left to right
    :param abcd: 32-bit block
    :return: 4 blocks of 8 bits a, b, c, d such that abcd is the starting block
    """
    # Mask to extract the lowest 8 bits
    mask = ((1 << 8) - 1)

    # Extracting 8-bit blocks using masking operations
    d = abcd & mask
    c = (abcd >> 8) & mask
    b = (abcd >> 16) & mask
    a = (abcd >> 24) & mask

    return a, b, c, d


def shift_left(data, input_size, n_bit):
    """
    This function must be able to barrel-shift left by n_bit elements
    the argument data of size input_size
    :param data: The integer to shift.
    :param input_size: The size in bits of data.
    :param n_bit: number of bits to shift
    :return: The integer data shifted n-bit to the left
    """
# Use the modulo operator to ensure that n_bit does not exceed the range
    n_bit = n_bit % input_size

    # Shift data to the left by n_bits positions
    data_shift_left = data << n_bit

    # Shift data to the right by (input_size - n_bit) positions
    # To ensure that bits that come out on the right side
    # to the left are reinserted on the left side
    data_shift_right = data >> (input_size - n_bit)

    # Combine the results of the shifts to take the resulting bits of the left shift
    # and the resulting bits of the right shift to form the final result of the circular shift
    shifted_data = data_shift_left | data_shift_right

    # Use a mask to keep only the low-order input_size bits
    shift_left_result = shifted_data & ((1 << input_size) - 1)

    return shift_left_result
