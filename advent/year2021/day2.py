# -*- coding: utf-8 -*-

import re


PATTERN = re.compile(r"(up|down|forward) (\d+)")


def read_input():
    file = open("input/2021/day2-input.txt", "r")
    data = []

    for line in file:
        result = PATTERN.match(line)
        direction, distance = result.group(1, 2)
        data.append((direction, int(distance)))

    return data


def part1(data):
    """
    >>> part1(read_input())
    1427868
    """

    horizontal = 0
    vertical = 0

    for (direction, distance) in data:
        if direction == "forward":
            horizontal += distance
        elif direction == "up":
            vertical -= distance
        elif direction == "down":
            vertical += distance
        else:
            raise ValueError(direction)

    return horizontal * vertical


def part2(data):
    """
    >>> part2(read_input())
    1568138742
    """

    horizontal = 0
    vertical = 0
    aim = 0

    for (direction, distance) in data:
        if direction == "forward":
            horizontal += distance
            vertical += aim * distance
        elif direction == "up":
            aim -= distance
        elif direction == "down":
            aim += distance
        else:
            raise ValueError(direction)

    return horizontal * vertical


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
