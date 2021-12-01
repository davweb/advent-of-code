#!/usr/local/bin/python3


def read_input():
    file = open('input/2015/day1-input.txt', 'r')
    return file.read()


def part1(data):
    """
    >>> part1("(())")
    0
    >>> part1("()()")
    0
    >>> part1("(((")
    3
    >>> part1("(()(()(")
    3
    >>> part1(read_input())
    280
    """

    floor = 0

    for move in data:
        floor += 1 if move == '(' else -1

    return floor


def part2(data):
    """
    >>> part2(read_input())
    1797
    """

    floor = 0

    for (count, move) in enumerate(data):
        floor += 1 if move == '(' else -1
        if floor < 0:
            return count + 1

    return Exception("Never entered basement")


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
