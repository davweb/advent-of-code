# -*- coding: utf-8 -*-

import re
from collections import Counter

PATTERN = re.compile(r'(\S+)-(\d+)\[(\w+)\]')
OFFSET = ord('a')


def read_input():
    data = []

    with open('input/2016/day4-input.txt', encoding='utf8') as file:
        for line in file.readlines():
            match = PATTERN.match(line)
            data.append((match.group(1), int(match.group(2)), match.group(3)))

    return data


def calculate_checksum(name):
    """
    >>> calculate_checksum('aaaaa-bbb-z-y-x')
    'abxyz'
    >>> calculate_checksum('a-b-c-d-e-f-g-h')
    'abcde'
    """

    counter = Counter(sorted(c for c in name if c != '-'))
    return ''.join(c for c, _ in counter.most_common(5))


def rotate_letter(letter, delta):
    """
    >>> rotate_letter('a', 4)
    'e'
    >>> rotate_letter('z', 3)
    'c'
    >>> rotate_letter('-', 3)
    ' '
    """

    if letter == '-':
        return ' '

    return chr((ord(letter) - OFFSET + delta) % 26 + OFFSET)


def decrypt(name, sector):
    """
    >>> decrypt('qzmt-zixmtkozy-ivhz', 343)
    'very encrypted name'
    """

    return ''.join(rotate_letter(c, sector) for c in name)


def part1(data):
    """
    >>> part1(read_input())
    173787
    """

    total = 0

    for name, sector, checksum in data:
        if calculate_checksum(name) == checksum:
            total += sector

    return total


def part2(data):
    """
    >>> part2(read_input())
    548
    """

    for name, sector, _ in data:
        if decrypt(name, sector) == 'northpole object storage':
            return sector

    raise ValueError('Did not find room')


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
