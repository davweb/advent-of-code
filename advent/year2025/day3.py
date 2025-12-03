# -*- coding: utf-8 -*-

def read_input(filename='input/2025/day3-input.txt'):
    with open(filename, encoding='utf8') as file:
        for line in file.readlines():
            yield [int(c) for c in line.strip()]


def joltage(bank, level):
    if level == -1:
        return 0

    last = len(bank) - level
    max_value = -1
    max_index = 0

    for index, value in enumerate(bank[:last]):
        if value > max_value:
            max_value = value
            max_index = index

            if max_value == 9:
                break

    return (10 ** level) * max_value + joltage(bank[max_index + 1:], level - 1)


def part1(data):
    """
    >>> part1([
    >>>     [9, 8, 7, 6, 5, 4, 3, 2, 1, 1, 1, 1, 1, 1, 1],
    >>>     [8, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9],
    >>>     [2, 3, 4, 2, 3, 4, 2, 3, 4, 2, 3, 4, 2, 7, 8],
    >>>     [8, 1, 8, 1, 8, 1, 9, 1, 1, 1, 1, 2, 1, 1, 1]])
    357
    >>> part1(read_input())
    17324
    """

    return sum(joltage(bank, 1) for bank in data)


def part2(data):
    """
    >>> part2(read_input())
    171846613143331
    """

    return sum(joltage(bank, 11) for bank in data)


def main():
    print(part1(read_input()))
    print(part2(read_input()))


if __name__ == "__main__":
    main()
