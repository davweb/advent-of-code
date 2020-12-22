# -*- coding: utf-8 -*-

import re
from advent import taxicab_distance
          
PATTERN = re.compile(r"pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)")

def read_input():
    file = open("input/2018/day23-input.txt", "r")
    text = file.read()

    nanobots = []

    for groups in PATTERN.findall(text):
        x = int(groups[0])
        y = int(groups[1])
        z = int(groups[2])
        r = int(groups[3])
        nanobots.append(((x, y, z), r))

    return nanobots

def distance(a, b):
    """
    >>> distance((0, 0, 0), (1, 3, 1))
    5
    >>> distance((1, 3, 1), (0, 0, 0))
    5
    >>> distance((1, 3, 1), (1, 3, 1))
    0
    >>> distance((1, 3, 1), (-1, -3, -2))
    11
    """

    return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])

def part1(nanobots):
    """
    >>> part1([
    ...     ((0, 0, 0), 4),
    ...     ((1, 0, 0), 1),
    ...     ((4, 0, 0), 3),
    ...     ((0, 2, 0), 1),
    ...     ((0, 5, 0), 3),
    ...     ((0, 0, 3), 1),
    ...     ((1, 1, 1), 1),
    ...     ((1, 1, 2), 1),
    ...     ((1, 3, 1), 1)
    ... ])
    7
    >>> part1(read_input())
    588
    """

    strongest_range = max(range for (_, range) in nanobots)
    strongest_location = next(location for (location, range) in nanobots if range == strongest_range)
    return sum(1 for (location, _) in nanobots if distance(strongest_location, location) <= strongest_range)


def part2(nanobots):
    """
    >>> part2([
    ...     ((10, 12, 12), 2),
    ...     ((12, 14, 12), 2),
    ...     ((16, 12, 12), 4),
    ...     ((14, 14, 14), 6),
    ...     ((50, 50, 50), 200),
    ...     ((10, 10, 10), 5)
    ... ])
    36

    # >>> part2(read_input())
    # 0
    """

    count = {}

    for bot in nanobots:
        ((x, y, z), bot_range) = bot

        for dx in range(-bot_range, bot_range + 1):
            yrange = bot_range - abs(dx)
                
            for dy in range(-yrange, yrange + 1):
                zrange = bot_range - abs(dx) - abs(dy)

                for dz in range(-zrange, zrange + 1):
                    location = (x + dx, y + dy, z + dz)

                    if location in count:
                        count[location] += 1
                    else:
                        count[location] = 1

    max_count = max(count.values())
    options = [location for (location, location_count) in count.items() if location_count == max_count]
    return min(distance((0, 0, 0), location) for location in options)


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
