# -*- coding: utf-8 -*-


def read_input(filename='input/2023/day1-input.txt'):
    with open(filename, encoding='utf8') as file:
        return file.readlines()


DIGITS = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']


def part1(data):
    """
    >>> part1(read_input())
    55123
    """

    total = 0

    for line in data:
        first = None

        for c in line:
            if c.isdigit():
                n = int(c)
                if first is None:
                    first = n

        total += first * 10 + n

    return total


def part2(data):
    """
    >>> part2(read_input())
    55260
    """

    total = 0

    for line in data:
        first = None
        n = None

        for i, c in enumerate(line):
            for value, text in enumerate(DIGITS):
                if line[i - len(text) + 1:i + 1] == text:
                    n = value

            if c.isdigit():
                n = int(c)

            if first is None:
                first = n

        total += first * 10 + n

    return total


def main():
    print(part1(read_input()))
    print(part2(read_input()))


if __name__ == "__main__":
    main()
