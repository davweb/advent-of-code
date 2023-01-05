# -*- coding: utf-8 -*-

from advent.year2016 import run_assembunny


def read_input():
    with open('input/2016/day25-input.txt', encoding='utf8') as file:
        return [line.strip().split() for line in file.readlines()]


def part1(data):
    """
    >>> part1(read_input())
    175
    """

    a = 0

    while run_assembunny(lines=data, a=a) != [0, 1, 0, 1, 0, 1, 0, 1, 0, 1]:
        a += 1

    return a


def main():
    print(part1(read_input()))


if __name__ == "__main__":
    main()
