# -*- coding: utf-8 -*-


def read_input():
    file = open("input/2021/day3-input.txt", "r")
    return [line.strip() for line in file.readlines()]


def most_common(data, index):
    """
    >>> most_common(['111', '110', '100', '000'], 0)
    '1'
    >>> most_common(['111', '110', '100', '000'], 1)
    >>> most_common(['111', '110', '100', '000'], 2)
    '0'
    """
    middle = len(data) / 2
    ones = [number[index] for number in data].count('1')

    if ones > middle:
        common = '1'
    elif ones < middle:
        common = '0'
    else:
        # None means 1 and 0 most equally common
        common = None

    return common


def binary_string_to_int(string):
    """
    >>> binary_string_to_int('10111')
    23
    """

    digit = 1
    result = 0

    for c in string[::-1]:
        if c == '1':
            result += digit

        digit *= 2

    return result


def part1(data):
    """
    >>> part1([
    ...    '00100', '11110', '10110', '10111', '10101', '01111',
    ...    '00111', '11100', '10000', '11001', '00010', '01010'
    ... ])
    198
    >>> part1(read_input())
    2250414
    """

    count = [0 for _ in range(len(data[0]))]

    for string in data:
        for i, c in enumerate(string):
            if c == '1':
                count[i] += 1

    digit = 1
    middle = len(data) // 2
    gamma = 0
    epsilon = 0

    for tally in count[::-1]:
        if tally > middle:
            gamma += digit
        else:
            epsilon += digit

        digit *= 2

    return gamma * epsilon


def part2(data):
    """
    >>> part2([
    ...    '00100', '11110', '10110', '10111', '10101', '01111',
    ...    '00111', '11100', '10000', '11001', '00010', '01010'
    ... ])
    230
    >>> part2(read_input())
    6085575
    """

    oxygen = data
    index = 0

    while len(oxygen) > 1:
        common = most_common(oxygen, index)
        if common is None:
            common = '1'

        oxygen = [value for value in oxygen if value[index] == common]
        index += 1

    scrubber = data
    index = 0

    while len(scrubber) > 1:
        common = most_common(scrubber, index)
        if common == '0':
            match = '1'
        else:
            match = '0'

        scrubber = [value for value in scrubber if value[index] == match]
        index += 1

    return binary_string_to_int(oxygen[0]) * binary_string_to_int(scrubber[0])


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
