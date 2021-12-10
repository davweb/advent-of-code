# -*- coding: utf-8 -*-

from itertools import product
from functools import cache


def read_input():
    results = []

    with open('input/2015/day18-input.txt') as file:
        return [line.strip() for line in file.readlines()]


@cache
def adjacent_cells(point):
    x, y = point

    return frozenset([(x - 1, y - 1), (x, y - 1), (x + 1, y - 1), (x - 1, y),
                      (x + 1, y), (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)])


def lights(data, fixed=None):
    board = set()

    for y, row in enumerate(data):
        for x, light in enumerate(row):
            if light == '#':
                board.add((x, y))

    for _ in range(100):
        new_board = set() if fixed is None else fixed.copy()

        for point in product(range(100), range(100)):
            lit = point in board
            adjacent_lit = len(board & adjacent_cells(point))

            if lit and 2 <= adjacent_lit <= 3:
                new_board.add(point)

            if not lit and adjacent_lit == 3:
                new_board.add(point)

        board = new_board

    return len(board)


def part1(data):
    """
    >>> part1(read_input())
    768
    """

    return lights(data)


def part2(data):
    """
    >>> part2(read_input())
    781
    """

    return lights(data, set(((0, 0), (0, 99), (99, 0), (99, 99))))


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
