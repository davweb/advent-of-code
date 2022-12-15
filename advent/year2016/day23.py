# -*- coding: utf-8 -*-

from advent.year2016 import run_assembunny


def read_input():
    with open('input/2016/day23-input.txt', encoding='utf8') as file:
        return [line.strip().split() for line in file.readlines()]


def part1(data):
    """
    >>> part1(read_input())
    12516
    """

    return run_assembunny(lines=data, a=7)


def part2(data):
    """
    >>> part2(read_input())
    479009076
    """

    return run_assembunny(lines=data, a=12)


def main():
    print(part1(read_input()))
    print(part2(read_input()))


if __name__ == "__main__":
    main()
