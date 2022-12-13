# -*- coding: utf-8 -*-

from ast import literal_eval
from functools import cmp_to_key
from itertools import zip_longest


def read_input():
    with open('input/2022/day13-input.txt', encoding='utf8') as file:
        return [literal_eval(line) for line in file if line.strip()]


def cmp(a, b):
    if a == b:
        return 0

    if a < b:
        return -1

    return 1


def compare(a, b):
    """
    >>> compare([1,1,3,1,1], [1,1,5,1,1])
    -1
    >>> compare([[1],[2,3,4]], [[1],4])
    -1
    >>> compare([9], [[8,7,6]])
    1
    >>> compare([[4,4],4,4], [[4,4],4,4,4])
    -1
    >>> compare([7,7,7,7], [7,7,7])
    1
    >>> compare([], [3])
    -1
    >>> compare([[[]]], [[]])
    1
    >>> compare([1,[2,[3,[4,[5,6,7]]]],8,9], [1,[2,[3,[4,[5,6,0]]]],8,9])
    1
    >>> compare(1,1)
    0
    >>> compare([1,2,3],[1,2,3])
    0
    """

    if isinstance(a, int) and isinstance(b, int):
        return cmp(a, b)

    if isinstance(a, list) and isinstance(b, list):
        for ea, eb in zip_longest(a, b):
            if ea is None:
                return -1
            if eb is None:
                return 1
            if c := compare(ea, eb):
                return c

        return 0

    if isinstance(a, int):
        a = [a]
    else:
        b = [b]

    return compare(a, b)


def part1(data):
    """
    >>> part1(read_input())
    6369
    """

    result = 0
    data = iter(data)

    for (index, a) in enumerate(data, start=1):
        b = next(data)

        if compare(a, b) == -1:
            result += index

    return result


def part2(data):
    """
    >>> part2(read_input())
    25800
    """

    FIRST_MARKER = [[2]]
    SECOND_MARKER = [[6]]
    signals = [FIRST_MARKER, SECOND_MARKER]
    signals.extend(data)
    signals.sort(key=cmp_to_key(compare))

    return (signals.index(FIRST_MARKER) + 1) * (signals.index(SECOND_MARKER) + 1)


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
