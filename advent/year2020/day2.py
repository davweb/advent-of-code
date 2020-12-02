#!/usr/local/bin/python3

import re

PATTERN = re.compile("^(\d+)-(\d+) (\w): (.*)")


def read_input():
    file = open('input/2020/day2-input.txt', 'r')
    return file.readlines()


def valid_sled_password(line):
    """
    >>> valid_sled_password("1-3 a: abcde")
    True
    >>> valid_sled_password("1-3 b: cdefg")
    False
    >>> valid_sled_password("2-9 c: ccccccccc")
    True
    >>> valid_sled_password("Fail")
    Traceback (most recent call last):
    ...
    ValueError: Invalid input 'Fail'
    """

    match = PATTERN.match(line)

    if not match:
        raise ValueError("Invalid input '{}'".format(line))

    lower = int(match.group(1))
    upper = int(match.group(2))
    (letter, password) = match.group(3, 4)

    count = password.count(letter)

    return lower <= count <= upper


def valid_toboggan_password(line):
    """
    >>> valid_toboggan_password("1-3 a: abcde")
    True
    >>> valid_toboggan_password("1-3 b: cdefg")
    False
    >>> valid_toboggan_password("2-9 c: ccccccccc")
    False
    >>> valid_toboggan_password("Fail")
    Traceback (most recent call last):
    ...
    ValueError: Invalid input 'Fail'
    """

    match = PATTERN.match(line)

    if not match:
        raise ValueError("Invalid input '{}'".format(line))

    firstIndex = int(match.group(1)) - 1
    secondIndex = int(match.group(2)) - 1
    (letter, password) = match.group(3, 4)

    firstMatch = password[firstIndex] == letter
    secondMatch = password[secondIndex] == letter
    
    return firstMatch != secondMatch


def part1(data):
    """
    >>> part1(read_input())
    622
    """
    
    return sum(valid_sled_password(line) for line in data)


def part2(data):
    """
    >>> part2(read_input())
    263
    """
    
    return sum(valid_toboggan_password(line) for line in data)


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
