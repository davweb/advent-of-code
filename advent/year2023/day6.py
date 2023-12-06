# -*- coding: utf-8 -*-

import re
from math import prod

PATTERN = re.compile(r'Time:\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\nDistance:\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)')


def read_input(filename='input/2023/day6-input.txt'):
    with open(filename, encoding='utf8') as file:
        content = file.read()
        match = PATTERN.match(content)

        for i in range(1, 5):
            yield int(match.group(i)), int(match.group(i + 4))


def is_win(time, distance, hold):
    return (time - hold) * hold > distance


def binary_search(lower, upper, test_function):
    while upper - lower > 1:
        middle = (upper + lower) // 2

        if test_function(middle):
            lower = middle
        else:
            upper = middle

    return lower


def win_count(time, distance):
    """
    >>> win_count(7, 9)
    4
    >>> win_count(15, 40)
    8
    >>> win_count(71530, 940200)
    71503
    """

    middle = time // 2
    lower_bound = binary_search(0, middle, lambda hold: not is_win(time, distance, hold))
    upper_bound = binary_search(middle, time, lambda hold: is_win(time, distance, hold))

    return upper_bound - lower_bound


def part1(data):
    """
    >>> part1(read_input())
    449820
    """

    return prod(win_count(time, distance) for time, distance in data)


def part2(data):
    """
    >>> part2(read_input())
    42250895
    """

    data = list(data)
    time = int(''.join(str(t) for t, _ in data))
    distance = int(''.join(str(d) for _, d in data))

    return win_count(time, distance)


def main():
    print(part1(read_input()))
    print(part2(read_input()))


if __name__ == "__main__":
    main()
