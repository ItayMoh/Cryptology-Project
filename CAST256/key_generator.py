from CAST256.functions_cast256 import function1, function2, function3
from CAST256.utils import extract_32bit_bloc_from_256, sum_mod_232, build_256_bit_bloc_from_32_bit_blocs


def forward_octave(abcdefgh, tr, tm):
    """
      This function corresponds to the forward_octave of cast-256. It decomposes the 256bit input block into
      32bit blocks. These blocks are transformed by using the functions f1, f2 and f3 of cast-256 using
      the rotation and mask keys. The blocks obtained are recomposed into a 256-bit block.
      !!! ATTENTION TO THE ORDER OF OPERATIONS INDICATED IN THE DOCUMENTATION!!!
      :param abcdefgh: the block to be processed (256bits)
      :param tr: array of 8 rotation keys (8bits)
      :param tm: array of 8 mask keys (32bits)
      :return: the result of the operations (256bits)
      """
    # Decomposition of block 256 into 32-bit block KAPPA <- Wi(KAPPA)
    a, b, c, d, e, f, g, h = extract_32bit_bloc_from_256(abcdefgh)

    G = g ^ function1(h, tr[0], tm[0])
    F = f ^ function2(G, tr[1], tm[1])
    E = e ^ function3(F, tr[2], tm[2])
    D = d ^ function1(E, tr[3], tm[3])
    C = c ^ function2(D, tr[4], tm[4])
    B = b ^ function3(C, tr[5], tm[5])
    A = a ^ function1(B, tr[6], tm[6])
    H = h ^ function2(A, tr[7], tm[7])

    return build_256_bit_bloc_from_32_bit_blocs(A, B, C, D, E, F, G, H)


def initialization():
    """
    This function creates the tr rotation and tm mask keys useful for generating the cast-256 keys.
    :return: two 8x24 two-dimensional arrays (24 rows and 8 columns) containing respectively
    the tr rotation and tm mask keys.
    """
    Cm = 0x5A827999
    Mm = 0x6ED9EBA1
    Cr = 19
    Mr = 17

    # Initialize arrays for rotation and mask keys
    tr = [[0 for _ in range(8)] for _ in range(24)]
    tm = [[0 for _ in range(8)] for _ in range(24)]

    for i in range(24):
        for j in range(8):
            tm[i][j] = Cm
            Cm = sum_mod_232(Cm, Mm)
            tr[i][j] = Cr
            Cr = sum_mod_232(Cr, Mr)

    return tr, tm


def key_generator(key):
    """
    This function generates the kr rotation and km mask keys for cast-256 encryption from the 256bits key
    encryption and tr rotation and tm mask keys.
    :param key: the encryption key (256bits)
    :return: two two-dimensional 12x4 tables (12 rows and 4 columns) containing respectively
    the kr rotation and km mask keys.
    """
    # Calls the initialize function to retrieve the tr and tm lists
    tr, tm = initialization()

    kr = [[0] * 4 for _ in range(12)]
    km = [[0] * 4 for _ in range(12)]
    for i in range(12):
        premier_forward = forward_octave(key, tr[i * 2], tm[i * 2])
        deuxieme_forward = forward_octave(premier_forward, tr[i * 2 + 1], tm[i * 2 + 1])

        key = deuxieme_forward
        a, b, c, d, e, f, g, h = extract_32bit_bloc_from_256(key)

        kr[i][0] = a & 0b11111
        kr[i][1] = c & 0b11111
        kr[i][2] = e & 0b11111
        kr[i][3] = g & 0b11111

        km[i][0] = h
        km[i][1] = f
        km[i][2] = d
        km[i][3] = b
    return kr, km
