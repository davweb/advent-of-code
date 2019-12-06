#!/usr/local/bin/python3

import itertools 
from collections import defaultdict
import re

PATTERN = re.compile(r"(\d+) <-> ((\d+, )*\d+)")

def read_input():
    file = open("input/day1-input.txt", "r")
    return [int(line) for line in file.readlines()]
    return file("input/day16-input.txt").read().split("",")

def my_function():
    """Calculate something

    >>> my_function(12)
    2
    >>> my_function(14)
    2
    """

def part1(data):
    for line in data:
        result = PATTERN.match(line)

def part2(data):
    pass

def main():
    part1("sample data")
    data = read_input()
    part1(data)
    part2(data)

if __name__ == "__main__":
    main()
