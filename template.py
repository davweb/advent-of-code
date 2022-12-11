# -*- coding: utf-8 -*-

import re
from collections import defaultdict

PATTERN = re.compile(r'(\d+) <-> ((\d+, )*\d+)')

def read_input():
    with open('input/2021/day1-input.txt', encoding='utf8') as file:
        #return [int(line) for line in file.readlines()]
        #return file.read().split(",")
        return 0


def my_function(input_arg):
    """
    >>> my_function(12)
    12
    >>> my_function(14)
    14
    """

    return input_arg


def part1(data):
    """
    >>> part1(read_input())
    0
    """

    return data


def part2(data):
    """
    >>> part2(read_input())
    0
    """

    return 0


def main():
    print(part1(read_input()))
    print(part2(read_input()))


if __name__ == "__main__":
    main()
