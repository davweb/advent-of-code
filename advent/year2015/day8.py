# -*- coding: utf-8 -*-

import re

ESCAPE_PATTERN = re.compile(r'(\\(x[0-9a-f]{2}|\\|"))')


def read_input():
    file = open("input/2015/day8-input.txt", "r")
    return [line.strip() for line in file.readlines()]


def storage_size(string):
    """
    >>> storage_size(r'""')
    0
    >>> storage_size(r'"abc"')
    3
    >>> storage_size(r'"aaa\\"aaa"')
    7
    >>> storage_size(r'"\\x27"')
    1
    >>> storage_size('"tltuvwhveau\\x43b\\"ymxjlcgiymcynwt"')
    29
    """

    return len(string) - 2 - sum(len(match[0]) - 1 for match in ESCAPE_PATTERN.findall(string))


def escaped_size(string):
    """
    >>> escaped_size(r'""')
    6
    >>> escaped_size(r'"abc"')
    9
    >>> escaped_size(r'"aaa\\"aaa"')
    16
    >>> escaped_size(r'"\\x27"')
    11
    """

    return len(string) + 2 + string.count('"') + string.count('\\')


def part1(data):
    """
    >>> part1(read_input())
    1350
    """

    return sum(len(string) - storage_size(string) for string in data)


def part2(data):
    """
    >>> part2(read_input())
    2085
    """

    return sum(escaped_size(string) - len(string) for string in data)


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
