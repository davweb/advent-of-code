#!/usr/local/bin/python3

from collections import defaultdict
from advent import taxicab_distance


def read_input():
    with open('input/2019/day3-input.txt', encoding='utf8') as file:
        return [line.split(',') for line in file]


def steps(start, instruction):
    """
    >>> list(steps((0, 0), "U3"))
    [(0, 1), (0, 2), (0, 3)]
    >>> list(steps((0, 0), "R3"))
    [(1, 0), (2, 0), (3, 0)]
    >>> list(steps((1, 1), "D4"))
    [(1, 0), (1, -1), (1, -2), (1, -3)]
    >>> list(steps((9, 3), "L1"))
    [(8, 3)]
    >>> list(steps((9, 9), "X1"))
    Traceback (most recent call last):
        ...
    ValueError: invalid direction "X"
    """

    (x, y) = start
    direction = instruction[0]
    distance = int(instruction[1:])

    if direction == "U":
        return ((x, i) for i in range(y + 1, y + distance + 1))
    if direction == "D":
        return ((x, i) for i in range(y - 1, y - distance - 1, -1))
    if direction == "R":
        return ((i, y) for i in range(x + 1, x + distance + 1))
    if direction == "L":
        return ((i, y) for i in range(x - 1, x - distance - 1, -1))

    raise ValueError(f'invalid direction "{direction}"')


def process_instructions(data):
    grid = {}
    location = (0, 0)
    length = 0

    for instruction in data:
        for step in steps(location, instruction):
            location = step
            length += 1

            if location not in grid:
                grid[location] = length

    return grid


def part1and2(data):
    """
    >>> part1and2(read_input())
    (266, 19242)
    """

    grid = defaultdict(int)
    length = defaultdict(int)

    for wire in data:
        wire_grid = process_instructions(wire)

        for location, value in wire_grid.items():
            grid[location] += 1
            length[location] += value

    min_dist = min(taxicab_distance((0, 0), item[0]) for item in grid.items() if item[1] == 2)
    min_length = min(length[item[0]] for item in grid.items() if item[1] == 2)

    return (min_dist, min_length)


def main():
    data = read_input()
    print(part1and2(data))


if __name__ == "__main__":
    main()
