# -*- coding: utf-8 -*-

from advent import Span


def read_input():
    output = []
    with open('input/2016/day20-input.txt', encoding='utf8') as file:
        for line in file.readlines():
            (lower, upper) = line.strip().split('-')
            output.append((int(lower), int(upper)))

    return output


def part1(data):
    """
    >>> part1(read_input())
    14975795
    """

    minimum = 0

    for lower, upper in sorted(data):
        if lower <= minimum <= upper:
            minimum = upper + 1

    return minimum


def part2(data):
    """
    >>> part2(read_input())
    101
    """

    ranges = Span.combine(Span(lower, upper) for lower, upper in data)
    return 4294967296 - sum(len(span) for span in ranges)


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
