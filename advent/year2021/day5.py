# -*- coding: utf-8 -*-

import re
from collections import defaultdict

PATTERN = re.compile(r"(\d+),(\d+) -> (\d+),(\d+)")


def read_input():
    data = []

    with open('input/2021/day5-input.txt', encoding='utf8') as file:
        for line in file:
            result = PATTERN.match(line)
            x1, y1, x2, y2 = result.group(1, 2, 3, 4)
            data.append(((int(x1), int(y1)), (int(x2), int(y2))))

    return data


def inclusive_range(start, end):
    if start > end:
        start, end = end, start

    return range(start, end + 1)


def part1(data):
    """
    >>> part1([
    ...     ((0, 9), (5, 9)),
    ...     ((8, 0), (0, 8)),
    ...     ((9, 4), (3, 4)),
    ...     ((2, 2), (2, 1)),
    ...     ((7, 0), (7, 4)),
    ...     ((6, 4), (2, 0)),
    ...     ((0, 9), (2, 9)),
    ...     ((3, 4), (1, 4)),
    ...     ((0, 0), (8, 8)),
    ...     ((5, 5), (8, 2))
    ... ])
    5
    >>> part1(read_input())
    6397
    """

    count = defaultdict(int)

    for (x1, y1), (x2, y2) in data:
        if x1 == x2:
            for y in inclusive_range(y1, y2):
                count[(x1, y)] += 1

        elif y1 == y2:
            for x in inclusive_range(x1, x2):
                count[(x, y1)] += 1

    return sum(1 for value in count.values() if value > 1)


def part2(data):
    """
    >>> part2([
    ...     ((0, 9), (5, 9)),
    ...     ((8, 0), (0, 8)),
    ...     ((9, 4), (3, 4)),
    ...     ((2, 2), (2, 1)),
    ...     ((7, 0), (7, 4)),
    ...     ((6, 4), (2, 0)),
    ...     ((0, 9), (2, 9)),
    ...     ((3, 4), (1, 4)),
    ...     ((0, 0), (8, 8)),
    ...     ((5, 5), (8, 2))
    ... ])
    12
    >>> part2(read_input())
    22335
    """

    count = defaultdict(int)

    for (x1, y1), (x2, y2) in data:
        if x1 == x2:
            for y in inclusive_range(y1, y2):
                count[(x1, y)] += 1

        elif y1 == y2:
            for x in inclusive_range(x1, x2):
                count[(x, y1)] += 1

        elif abs(x1 - x2) == abs(y1 - y2):
            dx = 1 if x1 < x2 else -1
            dy = 1 if y1 < y2 else -1
            x = x1 - dx
            y = y1 - dy

            while x != x2:
                x += dx
                y += dy
                count[(x, y)] += 1

        else:
            raise ValueError(((x1, y1), (x2, y2)))

    return sum(1 for value in count.values() if value > 1)


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
