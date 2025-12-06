# -*- coding: utf-8 -*-

import operator
from functools import reduce


def read_input(filename='input/2025/day6-input.txt'):
    lines = []
    operators = None

    with open(filename, encoding='utf8') as file:
        lines = file.read().split("\n")

    indexes = range(len(lines) - 1)
    rows = [[''] for _ in indexes]

    for i in range(len(lines[0])):
        if all(lines[j][i] == ' ' for j in indexes):
            for j in indexes:
                rows[j].append('')
        else:
            for j in indexes:
                rows[j][-1] += lines[j][i]

    operators = (operator.mul if op_char == '*' else operator.add for op_char in lines[-1].split())
    return zip(*rows), operators


def part1(data):
    """
    >>> part1(read_input())
    6378679666679
    """

    columns, operators = data
    numbers = ((int(i) for i in column) for column in columns)
    return sum(reduce(op, nums) for nums, op in zip(numbers, operators))


def part2(data):
    """
    >>> part2(read_input())
    11494432585168
    """

    columns, operators = data
    numbers = ((int(''.join(c)) for c in zip(*column)) for column in columns)
    return sum(reduce(op, nums) for nums, op in zip(numbers, operators))


def main():
    print(part1(read_input()))
    print(part2(read_input()))


if __name__ == "__main__":
    main()
