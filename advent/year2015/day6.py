# -*- coding: utf-8 -*-

import re
from collections import defaultdict


PATTERN = re.compile(r"(toggle|turn on|turn off) (\d+),(\d+) through (\d+),(\d+)")


def read_input():
    data = []

    with open('input/2015/day6-input.txt', encoding='utf8') as file:
        for line in file:
            result = PATTERN.match(line)
            action, from_x, from_y, to_x, to_y = result.group(1, 2, 3, 4, 5)
            data.append((action, int(from_x), int(from_y), int(to_x), int(to_y)))

    return data


def part1(data):
    """
    >>> part1(read_input())
    543903
    """

    grid = set()

    for (action, from_x, from_y, to_x, to_y) in data:
        for x in range(from_x, to_x + 1):
            for y in range(from_y, to_y + 1):
                cell = x + y * 1000

                if action == "turn on":
                    grid.add(cell)
                elif action == "turn off":
                    grid.discard(cell)
                elif cell in grid:
                    grid.remove(cell)
                else:
                    grid.add(cell)

    return len(grid)


def part2(data):
    """
    >>> part2(read_input())
    14687245
    """

    grid = defaultdict(int)

    for (action, from_x, from_y, to_x, to_y) in data:
        for x in range(from_x, to_x + 1):
            for y in range(from_y, to_y + 1):
                cell = (x, y)

                if action == "turn on":
                    grid[cell] += 1
                elif action == "turn off":
                    grid[cell] = max(0, grid[cell] - 1)
                else:
                    grid[cell] += 2

    return sum(grid.values())


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
