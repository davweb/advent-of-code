# -*- coding: utf-8 -*-


from functools import cache


def read_input():
    with open("input/2021/day7-input.txt", "r") as file:
        return [int(crab) for crab in file.read().split(',')]


@cache
def fuel(start, end):
    """
    >>> fuel(16, 5)
    66
    >>> fuel(1, 5)
    10
    """

    return sum(range(1, abs(start - end) + 1))


def part1(data):
    """
    >>> part1([16,1,2,0,4,2,7,1,2,14])
    37
    >>> part1(read_input())
    352997
    """

    options = range(min(data), max(data) + 1)
    return min(sum(abs(option - crab) for crab in data) for option in options)


def part2(data):
    """
    >>> part2(read_input())
    101571302
    """

    options = range(min(data), max(data) + 1)
    return min(sum(fuel(option, crab) for crab in data) for option in options)


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
