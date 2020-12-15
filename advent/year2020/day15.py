# -*- coding: utf-8 -*-

INPUT = [16, 1, 0, 18, 12, 14, 19]


def play(start, rounds):
    """
    >>> play((0, 3, 6), 4)
    0
    >>> play((0, 3, 6), 5)
    3
    >>> play((0, 3, 6), 6)
    3
    >>> play((0, 3, 6), 10)
    0
    >>> play((0, 3, 6), 2020)
    436
    """

    numbers = {}
    round = len(start)

    for i, j in enumerate(start[:-1]):
        numbers[j] = i + 1

    last = start[-1]

    while round < rounds:
        index = numbers.get(last)
        numbers[last] = round
        last = 0 if index is None else round - index
        round += 1

    return last 


def part1(data):
    """
    >>> part1(INPUT)
    929
    """

    return play(data, 2020)


def part2(data):
    """
    >>> part2(INPUT)
    16671510
    """

    return play(data, 30000000)


def main():
    print(part1(INPUT))
    print(part2(INPUT))


if __name__ == "__main__":
    main()
