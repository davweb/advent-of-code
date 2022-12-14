# -*- coding: utf-8 -*-

import re
from functools import cache

NOT_PATTERN = re.compile(r"NOT ([a-z]{1,2}|\d+) -> ([a-z]{1,2})")
OR_PATTERN = re.compile(r"([a-z]{1,2}|\d+) OR ([a-z]{1,2}|\d+) -> ([a-z]{1,2})")
AND_PATTERN = re.compile(r"([a-z]{1,2}|\d+) AND ([a-z]{1,2}|\d+) -> ([a-z]{1,2})")
LSHIFT_PATTERN = re.compile(r"([a-z]{1,2}) LSHIFT (\d+) -> ([a-z]{1,2})")
RSHIFT_PATTERN = re.compile(r"([a-z]{1,2}) RSHIFT (\d+) -> ([a-z]{1,2})")
NUMBER_PATTERN = re.compile(r"([a-z]{1,2}|\d+) -> ([a-z]{1,2})")


def read_input():
    with open('input/2015/day7-input.txt', encoding='utf8') as file:
        return [line.strip() for line in file]


def process(data):
    """
    >>> process(['NOT b -> a', '1 -> b'])
    -2
    """

    wires = {}

    @cache
    def get_value(key):
        try:
            return int(key)
        except ValueError:
            return wires[key]()

    for instruction in data:
        match = NUMBER_PATTERN.fullmatch(instruction)
        if match:
            value, result = match.group(1, 2)
            wires[result] = lambda value=value: get_value(value)
            continue

        match = NOT_PATTERN.fullmatch(instruction)
        if match:
            other, result = match.group(1, 2)
            wires[result] = lambda other=other: ~get_value(other)
            continue

        match = OR_PATTERN.fullmatch(instruction)
        if match:
            left, right, result = match.group(1, 2, 3)
            wires[result] = lambda left=left, right=right: get_value(left) | get_value(right)
            continue

        match = AND_PATTERN.fullmatch(instruction)
        if match:
            left, right, result = match.group(1, 2, 3)
            wires[result] = lambda left=left, right=right: get_value(left) & get_value(right)
            continue

        match = LSHIFT_PATTERN.fullmatch(instruction)
        if match:
            other, places, result = match.group(1, 2, 3)
            wires[result] = lambda other=other, places=places: get_value(other) << int(places)
            continue

        match = RSHIFT_PATTERN.fullmatch(instruction)
        if match:
            other, places, result = match.group(1, 2, 3)
            wires[result] = lambda other=other, places=places: get_value(other) >> int(places)
            continue

        raise ValueError(instruction)

    return get_value('a')


def part1(data):
    """
    >>> part1(read_input())
    3176
    """

    return process(data)


def part2(data):
    """
    >>> part2(read_input())
    14710
    """

    override = part1(data)
    data.append(f'{override} -> b')
    return process(data)


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
