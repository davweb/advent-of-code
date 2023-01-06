# -*- coding: utf-8 -*-

INPUT = (3029, 2947)


def generate(location):
    """
    >>> generate((1, 1))
    20151125
    >>> generate((4, 5))
    6899651
    >>> generate((6, 6))
    27995004
    """

    x, y = (1, 1)
    value = 20151125

    while (x, y) != location:
        value = value * 252533 % 33554393

        if y == 1:
            x, y = 1, x + 1
        else:
            x, y = x + 1, y - 1

    return value


def part1(data):
    """
    >>> part1(INPUT)
    19980801
    """

    return generate(data)


def main():
    print(part1(INPUT))


if __name__ == "__main__":
    main()
