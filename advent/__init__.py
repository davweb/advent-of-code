import operator
import functools
from math import prod
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

    # autopep8: off
    return ''.join(f'{byte:02x}' for byte in list_of_bytes)  # nopep8
    # autopep8: on


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


class Span():
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

    def __contains__(self, item):
        """
        >>> span = Span(3, 5)
        >>> 1 in span
        False
        >>> 3 in span
        True
        >>> 5 in span
        True
        >>> 6 in span
        False
        """
        return self.lower <= item <= self.upper

    def __len__(self):
        return self.upper - self.lower + 1

    def overlaps(self, other):
        return other.lower in self or other.upper in self

    def merge(self, other):
        self.lower = min(self.lower, other.lower)
        self.upper = max(self.upper, other.upper)

    def __lt__(self, other):
        if self.lower == other.lower:
            return self.upper < other.upper

        return self.lower < other.lower

    def __hash__(self):
        return hash((self.lower, self.upper))

    def __iter__(self):
        return iter(range(self.lower, self.upper + 1))

    def __repr__(self):
        return f'Span({self.lower}, {self.upper})'


# This isn't used anywhere but saved here in case it come in handy
class Cube:
    def __init__(self, near_corner, far_corner):
        """
        >>> Cube((1, 2, 3), (4, 5, 6))
        Cube((1, 2, 3), (4, 5, 6))
        >>> Cube((4, 5, 6), (1, 2, 3))
        Traceback (most recent call last):
        ...
        ValueError: Near corner must be less than far corner: 4 > 1
        """

        for n, f in zip(near_corner, far_corner):
            if n > f:
                raise ValueError(f'Near corner must be less than far corner: {n} > {f}')

        self.near_corner = near_corner
        self.far_corner = far_corner

    def __repr__(self):
        return f'Cube({self.near_corner}, {self.far_corner})'

    def __contains__(self, point):
        """
        >>> (0, 0, 0) in Cube((1, 2, 3), (4, 5, 6))
        False
        >>> (1, 2, 3) in Cube((1, 2, 3), (4, 5, 6))
        True
        >>> (2, 3, 4) in Cube((1, 2, 3), (4, 5, 6))
        True
        >>> (4, 5, 6) in Cube((1, 2, 3), (4, 5, 6))
        False
        >>> (5, 6, 7) in Cube((1, 2, 3), (4, 5, 6))
        False
        """

        return all(n <= p < f for n, p, f in zip(self.near_corner, point, self.far_corner))

    def overlap(self, other):
        """
        >>> Cube((0, 0, 0), (2, 3, 4)).overlap(Cube((1, 2, 3), (4, 5, 6)))
        Cube((1, 2, 3), (2, 3, 4))
        >>> Cube((1, 2, 3), (4, 5, 6)).overlap(Cube((0, 0, 0), (2, 3, 4)))
        Cube((1, 2, 3), (2, 3, 4))
        >>> Cube((1, 2, 3), (4, 5, 6)).overlap(Cube((7, 8, 9), (11, 12, 13)))
        >>> Cube((1, 2, 3), (11, 12, 13)).overlap(Cube((4, 5, 6), (7, 8, 9)))
        Cube((4, 5, 6), (7, 8, 9))
        >>> Cube((12, 8, 8), (20, 16, 16)).overlap(Cube((8, 8, 8), (20, 20, 20)))
        Cube((12, 8, 8), (20, 16, 16))
        """

        near = (
            self.near_corner[0] if self.near_corner[0] > other.near_corner[0] else other.near_corner[0],
            self.near_corner[1] if self.near_corner[1] > other.near_corner[1] else other.near_corner[1],
            self.near_corner[2] if self.near_corner[2] > other.near_corner[2] else other.near_corner[2]
        )

        far = (
            self.far_corner[0] if self.far_corner[0] < other.far_corner[0] else other.far_corner[0],
            self.far_corner[1] if self.far_corner[1] < other.far_corner[1] else other.far_corner[1],
            self.far_corner[2] if self.far_corner[2] < other.far_corner[2] else other.far_corner[2]
        )

        if near[0] >= far[0] or near[1] >= far[1] or near[2] >= far[2]:
            return None

        return Cube(near, far)

    def __eq__(self, other):
        return self.near_corner == other.near_corner and self.far_corner == other.far_corner

    def slice_cube(self, other):
        """
        Split to cube into 27 smaller cubes based on overlap with another cube

        >>> nine = Cube((0, 0, 0), (3, 3, 3))
        >>> one = Cube((1, 1, 1), (2, 2, 2))
        >>> len(list(nine.slice_cube(one)))
        27
        >>> whole = Cube((2, 2, 3), (20, 40, 60))
        >>> overlap = Cube((10, 12, 14), (20, 40, 60))
        >>> result = whole.slice_cube(overlap)
        >>> whole.volume() == sum(cube.volume() for cube in result)
        True
        """

        overlap = self.overlap(other)

        x_options, y_options, z_options = zip(
            self.near_corner, overlap.near_corner, overlap.far_corner, self.far_corner)

        previous_x = x_options[0]

        for x in x_options[1:]:
            if x == previous_x:
                continue

            previous_y = y_options[0]

            for y in y_options[1:]:
                if y == previous_y:
                    continue

                previous_z = z_options[0]

                for z in z_options[1:]:
                    if z == previous_z:
                        continue

                    yield Cube((previous_x, previous_y, previous_z), (x, y, z))
                    previous_z = z

                previous_y = y

            previous_x = x

    def is_adjacent(self, other):
        """
        Check if two cubes are next to each other with matching faces

        >>> Cube((0, 0, 0), (1, 1, 1)).is_adjacent(Cube((0, 0, 1), (1, 1, 10)))
        True
        >>> Cube((0, 0, 0), (1, 1, 1)).is_adjacent(Cube((7, 0, 1), (12, 1, 10)))
        False
        >>> Cube((0, 0, 0), (3, 3, 3)).is_adjacent(Cube((3, 0, 0), (10, 3, 3)))
        True
        >>> Cube((0, 0, 0), (3, 3, 3)).is_adjacent(Cube((0, 3, 0), (3, 10, 3)))
        True
        >>> Cube((0, 0, 0), (3, 3, 3)).is_adjacent(Cube((0, 3, 0), (4, 10, 3)))
        False
        """

        if self.far_corner[0] == other.near_corner[0] and \
                self.near_corner[1] == other.near_corner[1] and \
                self.near_corner[2] == other.near_corner[2] and \
                self.far_corner[1] == other.far_corner[1] and \
                self.far_corner[2] == other.far_corner[2]:
            return True

        if self.far_corner[1] == other.near_corner[1] and \
                self.near_corner[0] == other.near_corner[0] and \
                self.near_corner[2] == other.near_corner[2] and \
                self.far_corner[0] == other.far_corner[0] and \
                self.far_corner[2] == other.far_corner[2]:
            return True

        if self.far_corner[2] == other.near_corner[2] and \
                self.near_corner[0] == other.near_corner[0] and \
                self.near_corner[1] == other.near_corner[1] and \
                self.far_corner[0] == other.far_corner[0] and \
                self.far_corner[1] == other.far_corner[1]:
            return True

        return False

    def volume(self):
        """
        >>> Cube((0, 0, 0), (1, 1, 1)).volume()
        1
        >>> Cube((0, 0, 0), (3, 3, 3)).volume()
        27
        >>> Cube((1, 2, 3), (4, 5, 7)).volume()
        36
        """

        return prod(j - i for i, j in zip(self.near_corner, self.far_corner))

    def __sub__(self, other):
        """
        >>> Cube((0, 0, 0), (1, 2, 3)) - Cube((0, 0, 0), (1, 2, 3))
        []
        >>> Cube((0, 0, 0), (1, 2, 3)) - Cube((4, 5, 6), (7, 8, 9))
        [Cube((0, 0, 0), (1, 2, 3))]
        >>> a = Cube((0, 0, 0), (334, 324, 379))
        >>> b = Cube((98, 78, 11), (421, 432, 432))
        >>> overlap = a.overlap(b)
        >>> result = a - b
        >>> a.volume() - overlap.volume() == sum(cube.volume() for cube in result)
        True
        >>> overlap = b.overlap(a)
        >>> result = b - a
        >>> b.volume() - overlap.volume() == sum(cube.volume() for cube in result)
        True
        """

        overlap = self.overlap(other)

        #  If there's no overlap then this cube is unchanged
        if overlap is None:
            return [self]

        # If the overlap is the same as this cube then there's none of this cube left
        if overlap == self:
            return []

        result = []

        for sub_cube in self.slice_cube(overlap):
            if sub_cube.overlap(overlap) is None:
                result.append(sub_cube)

        response = []

        while result:
            sub_cube = result.pop()

            for other_sub_cube in result:
                if sub_cube.is_adjacent(other_sub_cube):
                    other_sub_cube.near_corner = sub_cube.near_corner
                    sub_cube = None
                    break

                if other_sub_cube.is_adjacent(sub_cube):
                    other_sub_cube.far_corner = sub_cube.far_corner
                    sub_cube = None
                    break

            if sub_cube is not None:
                response.append(sub_cube)

        return response

    def __hash__(self):
        return hash((self.near_corner, self.far_corner))
