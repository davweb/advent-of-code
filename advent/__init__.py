import hashlib
import operator
import functools

KNOT_HASH_SIZE = 256
KNOT_SLICE_SIZE = 16

def bytes_to_hex(list_of_bytes):
    """
    >>> bytes_to_hex([1])
    '01'
    >>> bytes_to_hex([100,120,250])
    '6478fa'
    """

    if any(i < 0 or i > 255 for i in list_of_bytes):
        raise ValueError("Value outside range 0 to 255")

    return "".join("{:02x}".format(i) for i in list_of_bytes)


def knot_hash(input):
    """
    >>> bytes_to_hex(knot_hash(""))
    'a2582a3a0e66e6e86e3812dcb672a272'
    >>> bytes_to_hex(knot_hash("AoC 2017"))
    '33efeb34ea91902bb2f59c9920caa6cd'
    >>> bytes_to_hex(knot_hash("1,2,3"))
    '3efbe78a8d82f29979031a4aa0b16a9d'
    >>> bytes_to_hex(knot_hash("1,2,4"))
    '63960835bcdc130f0b66d7ff4f6a5a8e'
    """

    input_list = [ord(i) for i in input]
    input_list += [17, 31, 73, 47, 23]
    input_list *= 64

    position = 0
    skip = 0
    hash = list(range(KNOT_HASH_SIZE))

    for length in input_list:
        for i in range(length // 2):
            a = (position + i) % KNOT_HASH_SIZE
            b = (position + length - i - 1)  % KNOT_HASH_SIZE
            hash[a], hash[b] = hash[b], hash[a]

        position = (position + length + skip) % KNOT_HASH_SIZE
        skip += 1

    hash = [functools.reduce(operator.xor, hash[i:i + KNOT_SLICE_SIZE]) for i in range(0, KNOT_HASH_SIZE, KNOT_SLICE_SIZE)]
    return hash


def bounds(points):
    """
    >>> bounds([(0, 0)])
    ((0, 0), (0, 0))
    >>> bounds([(7, 1), (-1, 9)])
    ((-1, 1), (7, 9))
    """

    left = min(x for (x,y) in points)
    right = max(x for (x,y) in points)
    top = min(y for (x,y) in points)
    bottom = max(y for (x,y) in points)
    
    return ((left, top), (right, bottom))


def md5(string):
    """
    >>> md5("test")
    '098f6bcd4621d373cade4e832627b4f6'
    """
    
    return hashlib.md5(string.encode('utf-8')).hexdigest()


def taxicab_distance(a, b):
    """Calculate Manhattan distance

    >>> taxicab_distance((0, 0), (0, 0))
    0
    >>> taxicab_distance((0, 0), (1, 1))
    2
    >>> taxicab_distance((-1, -1), (-4, -3))
    5
    """

    return abs(a[0] - b[0]) + abs(a[1] - b[1])