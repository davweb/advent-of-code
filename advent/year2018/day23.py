# -*- coding: utf-8 -*-

import re
from collections import defaultdict

PATTERN = re.compile(r"pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)")


def read_input():
    with open('input/2018/day23-input.txt', encoding='utf8') as file:
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


def options(location, delta):
    x, y, z = location
    dx, dy, dz = delta

    for nx in (x + dx, x - dx):
        for ny in (y + dy, y - dy):
            for nz in (z + dz, z - dz):
                yield (nx, ny, nz)


def overlapping(bot_one, bot_two):
    journey = distance(bot_one[0], bot_two[0])
    return journey <= bot_one[1] + bot_two[1]


def surface(radius):
    for dx in range(radius):
        for dy in range(radius - dx):
            yield dx, dy, radius - dx - dy


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


def part2_every_location(nanobots):
    """
    >>> part2_every_location([
    ...     ((10, 12, 12), 2),
    ...     ((12, 14, 12), 2),
    ...     ((16, 12, 12), 4),
    ...     ((14, 14, 14), 6),
    ...     ((50, 50, 50), 200),
    ...     ((10, 10, 10), 5)
    ... ])
    36
    """

    count = defaultdict(int)

    for bot in nanobots:
        ((x, y, z), bot_range) = bot

        for dx in range(-bot_range, bot_range + 1):
            yrange = bot_range - abs(dx)

            for dy in range(-yrange, yrange + 1):
                zrange = bot_range - abs(dx) - abs(dy)

                for dz in range(-zrange, zrange + 1):
                    location = (x + dx, y + dy, z + dz)
                    count[location] += 1

    max_count = max(count.values())
    location_options = [location for (location, location_count) in count.items() if location_count == max_count]
    return min(distance((0, 0, 0), location) for location in location_options)


def part2_by_surface(nanobots):
    """
    >>> part2_by_surface([
    ...     ((10, 12, 12), 2),
    ...     ((12, 14, 12), 2),
    ...     ((16, 12, 12), 4),
    ...     ((14, 14, 14), 6),
    ...     ((50, 50, 50), 200),
    ...     ((10, 10, 10), 5)
    ... ])
    36
    """

    max_count = 0
    min_distance = None

    for bot_location, bot_range in nanobots:
        for delta in surface(bot_range):
            for location in options(bot_location, delta):
                count = 0

                for other, other_range in nanobots:
                    if distance(location, other) <= other_range:
                        count += 1

                if count >= max_count:
                    max_count = count
                    home_distance = distance(location, (0, 0, 0))

                    if min_distance is None or min_distance > home_distance:
                        min_distance = home_distance

    return home_distance


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
    0
    >>> part2(read_input())
    0
    """

    max_count = 0

    for bot in nanobots:
        count = sum(overlapping(bot, other) for other in nanobots)
        max_count = max(max_count, count)

    return 0


def main():
    data = read_input()
    print(part1(data))
    #  print(part2(data))


if __name__ == "__main__":
    main()
