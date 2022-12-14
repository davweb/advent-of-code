# -*- coding: utf-8 -*-

import numpy as np


SAND_START = (500, 0)


def read_input():
    with open('input/2022/day14-input.txt', encoding='utf8') as file:
        return [[[int(i) for i in pair.split(',')] for pair in line.split(' -> ')] for line in file]


def build_map(data, with_floor=False):
    height = 0
    width = SAND_START[0] + 1

    for line in data:
        for x, y in line:
            width = max(width, x + 1)
            height = max(height, y + 1)

    if with_floor:
        height += 2
        width *= 2

    grid = np.full((width, height), False)

    if with_floor:
        grid[0:width, height - 1] = True

    for line in data:
        start = line[0]

        for end in line[1:]:
            x_range, y_range = zip(start, end)
            grid[min(x_range):max(x_range) + 1, min(y_range):max(y_range) + 1] = True
            start = end

    return grid


def drop_sand(grid):
    _, height = np.shape(grid)
    x, y = SAND_START

    while y + 1 < height:
        if not grid[x, y + 1]:
            y += 1
        elif not grid[x - 1, y + 1]:
            x, y = (x - 1, y + 1)
        elif not grid[x + 1, y + 1]:
            x, y = (x + 1, y + 1)
        else:
            grid[x, y] = True
            return (x, y)

    return None


def part1(data):
    """
    >>> part1(read_input())
    625
    """

    grid = build_map(data)
    count = 0

    while drop_sand(grid):
        count += 1

    return count


def part2(data):
    """
    >>> part2(read_input())
    25193
    """

    grid = build_map(data, True)
    count = 0

    while not grid[SAND_START]:
        drop_sand(grid)
        count += 1

    return count


def main():
    print(part1(read_input()))
    print(part2(read_input()))


if __name__ == "__main__":
    main()
