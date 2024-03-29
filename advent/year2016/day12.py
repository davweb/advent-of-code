# -*- coding: utf-8 -*-

from advent.year2016 import run_assembunny


def read_input():
    with open('input/2016/day12-input.txt', encoding='utf8') as file:
        return [line.strip().split() for line in file.readlines()]


def part1(data):
    """
    >>> part1(read_input())
    318009
    """

    return run_assembunny(data)


def part2(data):
    """
    >>> part2(read_input())
    9227663
    """

    return run_assembunny(data, c=1)


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
