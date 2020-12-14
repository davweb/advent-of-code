# -*- coding: utf-8 -*-

import re
from collections import defaultdict

PATTERN = re.compile(r"(\d+) <-> ((\d+, )*\d+)")

def read_input():
    file = open("input/2020/day1-input.txt", "r")
    
    #return [int(line) for line in file.readlines()]
    return file.read().split(",")


def my_function():
    """Calculate something

    x>>> my_function(12)
    2
    x>>> my_function(14)
    2
    """

def part1(data):
    """
    >>> part1(read_input())
    0
    """

    return 0


def part2(data):
    """
    >>> part2(read_input())
    0
    """

    return 0


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
