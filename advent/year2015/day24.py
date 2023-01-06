# -*- coding: utf-8 -*-

from itertools import combinations
import math


def read_input(filename='input/2015/day24-input.txt'):
    with open(filename, encoding='utf8') as file:
        return tuple(int(line) for line in file)


def solve(data, groups):
    target = sum(data) // groups

    size = 1
    candidates = None

    while not candidates:
        size += 1
        candidates = [c for c in combinations(data, size) if sum(c) == target]

    quantum = sorted(math.prod(c) for c in candidates)
    return quantum[0]


def part1(data):
    """
    >>> part1(read_input())
    11846773891
    """

    return solve(data, 3)


def part2(data):
    """
    >>> part2(read_input())
    80393059
    """

    return solve(data, 4)


def main():
    print(part1(read_input()))
    print(part2(read_input()))


if __name__ == "__main__":
    main()
