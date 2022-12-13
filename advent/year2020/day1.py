# -*- coding: utf-8 -*-

import itertools
from math import prod


def read_input():
    with open('input/2020/day1-input.txt', encoding='utf8') as file:
        return [int(line) for line in file]


def search(data, size):
    for t in itertools.combinations(data, size):
        if sum(t) == 2020:
            return prod(t)

    raise ValueError()


def part1(data):
    """
    >>> part1(read_input())
    252724
    """
    return search(data, 2)


def part2(data):
    """
    >>> part2(read_input())
    276912720
    """
    return search(data, 3)


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
