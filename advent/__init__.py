import operator
import functools
import _md5

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


def knot_hash(value):
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

    input_list = [ord(i) for i in value]
    input_list += [17, 31, 73, 47, 23]
    input_list *= 64

    position = 0
    skip = 0
    hash_value = list(range(KNOT_HASH_SIZE))

    for length in input_list:
        for i in range(length // 2):
            a = (position + i) % KNOT_HASH_SIZE
            b = (position + length - i - 1) % KNOT_HASH_SIZE
            hash_value[a], hash_value[b] = hash_value[b], hash_value[a]

        position = (position + length + skip) % KNOT_HASH_SIZE
        skip += 1

    hash_value = [functools.reduce(operator.xor, hash_value[i:i + KNOT_SLICE_SIZE])
                  for i in range(0, KNOT_HASH_SIZE, KNOT_SLICE_SIZE)]
    return hash_value


def bounds(points):
    """
    >>> bounds([(0, 0)])
    ((0, 0), (0, 0))
    >>> bounds([(7, 1), (-1, 9)])
    ((-1, 1), (7, 9))
    """

    left = min(x for (x, y) in points)
    right = max(x for (x, y) in points)
    top = min(y for (x, y) in points)
    bottom = max(y for (x, y) in points)

    return ((left, top), (right, bottom))


def md5(string):
    """
    >>> md5("test")
    '098f6bcd4621d373cade4e832627b4f6'
    """

    return _md5.md5(string.encode('utf-8')).hexdigest()


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


class Range():
    @classmethod
    def combine(cls, ranges):
        ranges = sorted(ranges)
        lower_range = ranges.pop(0)
        merged = [lower_range]

        while ranges:
            upper_range = ranges.pop(0)

            if lower_range.overlaps(upper_range):
                lower_range.merge(upper_range)
            else:
                lower_range = upper_range
                merged.append(lower_range)

        return merged

    def __init__(self, lower, upper):
        if lower > upper:
            raise ValueError(lower, upper)

        self.lower = lower
        self.upper = upper

    def size(self):
        return self.upper - self.lower + 1

    def overlaps(self, other):
        return self.lower <= other.lower <= self.upper \
            or self.lower <= other.upper <= self.upper

    def merge(self, other):
        self.lower = min(self.lower, other.lower)
        self.upper = max(self.upper, other.upper)

    def __lt__(self, other):
        if self.lower == other.lower:
            return self.upper < other.upper

        return self.lower < other.lower

    def __repr__(self):
        return f'Range({self.lower}, {self.upper})'
