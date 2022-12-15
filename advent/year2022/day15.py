# -*- coding: utf-8 -*-

import re
from advent import taxicab_distance, Range

PATTERN = re.compile(r'Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)')


def read_input(filename='input/2022/day15-input.txt'):
    output = []

    with open(filename, encoding='utf8') as file:
        for line in file:
            match = PATTERN.match(line)
            sensor = (int(match.group(1)), int(match.group(2)))
            beacon = (int(match.group(3)), int(match.group(4)))
            output.append((sensor, beacon))

    return output


def overlap_with_row(sensor, beacon, row):
    """
    >>> overlap_with_row((8,7), (2,10), 17)
    >>> overlap_with_row((8,7), (2,10), -3)
    >>> overlap_with_row((8,7), (2,10), 16)
    Range(8, 8)
    >>> overlap_with_row((8,7), (2,10), 1)
    Range(5, 11)
    >>> overlap_with_row((8,7), (2,10), 7)
    Range(-1, 17)
    """

    x = sensor[0]
    y_distance = taxicab_distance(sensor, (x, row))
    beacon_distance = taxicab_distance(sensor, beacon)
    overlap = beacon_distance - y_distance

    if overlap < 0:
        return None

    return Range(x - overlap, x + overlap)


def overlaps_with_row(data, y):
    overlaps = []

    for sensor, beacon in data:
        if overlap := overlap_with_row(sensor, beacon, y):
            overlaps.append(overlap)

    return Range.combine(overlaps)


def exclude_row(data , y):
    """
    >>> data = read_input(filename='input/2022/day15-test.txt')
    >>> exclude_row(data, 10)
    26
    """

    ranges = overlaps_with_row(data, y)
    row_beacons = set(beacon[0] for _, beacon in data if beacon[1] == y)
    return sum(range.size() for range in ranges) - len(row_beacons)


def find_beacon(data, max_value):
    """
    >>> data = read_input(filename='input/2022/day15-test.txt')
    >>> find_beacon(data, 20)
    (14, 11)
    """

    for row in range(0, max_value + 1):
        overlap = overlaps_with_row(data, row)

        if len(overlap) == 1:
            continue

        if len(overlap) == 2:
            x = overlap[0].upper + 1

            if x == overlap[1].lower - 1:
                return x, row

        raise ValueError('Too many gaps')

    raise ValueError('Beacon not found')


def part1(data):
    """
    >>> part1(read_input())
    4985193
    """

    return exclude_row(data, 2000000)


def part2(data):
    """
    >>> part2(read_input())
    11583882601918
    """

    x, y = find_beacon(data, 4000000)
    return x * 4000000 + y


def main():
    print(part1(read_input()))
    print(part2(read_input()))


if __name__ == "__main__":
    main()
