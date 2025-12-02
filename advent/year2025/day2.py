# -*- coding: utf-8 -*-


def read_input(filename='input/2025/day2-input.txt'):
    with open(filename, encoding='utf8') as file:
        ranges = file.read().split(',')

        for min_max in ranges:
            yield [int(i) for i in min_max.split('-')]


def is_valid(num):
    """
    >>> is_valid(11)
    False
    >>> is_valid(12)
    True
    >>> is_valid(38593859)
    False
    """

    str_num = str(num)
    length = len(str_num)

    if length % 2 == 1:
        return True

    mid = length // 2
    return str_num[:mid] != str_num[mid:]


def is_still_valid(num):
    """
    >>> is_still_valid(11)
    False
    >>> is_still_valid(12)
    True
    >>> is_still_valid(38593859)
    False
    >>> is_still_valid(111)
    False
    """

    str_num = str(num)
    length = len(str_num)
    max_cut = length // 2

    for cut_size in range(1, max_cut + 1):
        if length % cut_size != 0:
            continue

        cuts = [str_num[i:i + cut_size] for i in range(0, length, cut_size)]

        if all(cuts[0] == c for c in cuts[1:]):
            return False

    return True


def part1(data):
    """
    >>> part1(read_input())
    40055209690
    """

    total = 0

    for (lower, upper) in data:
        total += sum(i for i in range(lower, upper + 1) if not is_valid(i))

    return total


def part2(data):
    """
    >>> part2(read_input())
    50857215650
    """

    total = 0

    for (lower, upper) in data:
        total += sum(i for i in range(lower, upper + 1) if not is_still_valid(i))

    return total


def main():
    print(part1(read_input()))
    print(part2(read_input()))


if __name__ == "__main__":
    main()
