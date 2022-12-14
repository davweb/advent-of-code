import itertools
import math


def read_input():
    with open('input/2015/day2-input.txt', encoding='utf8') as file:
        return [[int(side) for side in line.split('x')] for line in file]


def wrapping(lengths):
    """
    >>> wrapping([2, 3, 4])
    58
    >>> wrapping([1, 1, 10])
    43
    """

    sides = [(x * y) for x, y in itertools.combinations(lengths, 2)]
    return 2 * sum(sides) + min(sides)


def ribbon(lengths):
    """
    >>> ribbon([2, 3, 4])
    34
    >>> ribbon([1, 1, 10])
    14
    """

    sides = [(x + y) for x, y in itertools.combinations(lengths, 2)]
    return 2 * min(sides) + math.prod(lengths)


def part1(data):
    """
    >>> part1(read_input())
    1598415
    """
    return sum(wrapping(parcel) for parcel in data)


def part2(data):
    """
    >>> part2(read_input())
    3812909
    """
    return sum(ribbon(parcel) for parcel in data)


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
