# pylint: disable=too-many-arguments,too-many-locals
# -*- coding: utf-8 -*-

import re
from itertools import product

PATTERN = re.compile(r'(on|off) x=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),z=(-?\d+)\.\.(-?\d+)')


def read_input():
    output = []

    with open('input/2021/day22-input.txt', encoding='utf8') as file:
        for line in file.readlines():
            match = PATTERN.match(line)
            switch_on = match.group(1) == 'on'
            x_from = int(match.group(2))
            x_to = int(match.group(3))
            y_from = int(match.group(4))
            y_to = int(match.group(5))
            z_from = int(match.group(6))
            z_to = int(match.group(7))

            output.append((switch_on, x_from, x_to, y_from, y_to, z_from, z_to))

    return output


class Box:
    def __init__(self, x1, x2, y1, y2, z1, z2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.z1 = z1
        self.z2 = z2

    def valid(self):
        return self.x1 <= self.x2 and self.y1 <= self.y2 and self.z1 <= self.z2

    def volume(self):
        return (self.x2 - self.x1 + 1) * (self.y2 - self.y1 + 1) * (self.z2 - self.z1 + 1)

    def overlap(self, other):
        return self.x1 <= other.x2 and self.x2 >= other.x1 \
            and self.y1 <= other.y2 and self.y2 >= other.y1 \
            and self.z1 <= other.z2 and self.z2 >= other.z1 \


    def remove_overlap(self, other):
        """
        >>> big = Box(1,3,1,3,1,3)
        >>> small = Box(2,2,2,2,2,2)
        >>> len(big.remove_overlap(small))
        26
        >>> sum(box.volume() for box in big.remove_overlap(small))
        26
        >>> len(small.remove_overlap(big))
        0
        """

        # Calculate the overlapping box
        ox1 = max(self.x1, other.x1)
        ox2 = min(self.x2, other.x2)
        oy1 = max(self.y1, other.y1)
        oy2 = min(self.y2, other.y2)
        oz1 = max(self.z1, other.z1)
        oz2 = min(self.z2, other.z2)

        remaining = []

        #  split this box into 27 boxes so we can leave out the overlap
        for rx1, rx2 in ((self.x1, ox1 - 1), (ox1, ox2), (ox2 + 1, self.x2)):
            for ry1, ry2 in ((self.y1, oy1 - 1), (oy1, oy2), (oy2 + 1, self.y2)):
                for rz1, rz2 in ((self.z1, oz1 - 1), (oz1, oz2), (oz2 + 1, self.z2)):
                    # skip the overlap
                    if rx1 == ox1 and ry1 == oy1 and rz1 == oz1:
                        continue

                    box = Box(rx1, rx2, ry1, ry2, rz1, rz2)

                    if not box.valid():
                        continue

                    remaining.append(box)

        return remaining

    def __str__(self):
        """
        >>> str(Box(1, 2, 3, 4, 5, 6))
        '<x=1..2, y=3..4, z=5..6>'
        """

        return '<x={x1}..{x2}, y={y1}..{y2}, z={z1}..{z2}>'.format(**self.__dict__)

    def __repr__(self):
        """
        >>> Box(1, 2, 3, 4, 5, 6)
        Box(1, 2, 3, 4, 5, 6)
        """

        return 'Box({x1}, {x2}, {y1}, {y2}, {z1}, {z2})'.format(**self.__dict__)


def part1(data):
    """
    >>> part1(read_input())
    644257
    """

    cubes = set()

    for step in data:
        switch_on, x_from, x_to, y_from, y_to, z_from, z_to = step

        x_from = max(x_from, -50)
        x_to = min(x_to, 50)
        y_from = max(y_from, -50)
        y_to = min(y_to, 50)
        z_from = max(z_from, -50)
        z_to = min(z_to, 50)

        for cube in product(range(x_from, x_to + 1), range(y_from, y_to + 1), range(z_from, z_to + 1)):
            if switch_on:
                cubes.add(cube)
            else:
                cubes.discard(cube)

    return len(cubes)


def part2(data):
    """
    >>> part2(read_input())
    1235484513229032
    """

    boxes = set()

    for step in data:
        switch_on, x_from, x_to, y_from, y_to, z_from, z_to = step

        box = Box(x_from, x_to, y_from, y_to, z_from, z_to)

        for other in boxes.copy():
            if box.overlap(other):
                boxes.remove(other)
                boxes.update(other.remove_overlap(box))

        if switch_on:
            boxes.add(box)

    return sum(box.volume() for box in boxes)


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
