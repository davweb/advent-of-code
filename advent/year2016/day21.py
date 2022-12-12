# -*- coding: utf-8 -*-

import re

ROTATE = re.compile(r'rotate based on position of letter ([a-z])')
MOVE = re.compile(r'move position (\d+) to position (\d+)')
SWAP = re.compile(r'swap position (\d+) with position (\d+)')
SWAP_LETTER = re.compile(r'swap letter ([a-z]) with letter ([a-z])')
ROTATE_LEFT = re.compile('rotate left (\\d+) steps?')
ROTATE_RIGHT = re.compile('rotate right (\\d+) steps?')
REVERSE = re.compile('reverse positions (\\d+) through (\\d+)')


def read_input():
    with open('input/2016/day21-input.txt', encoding='utf8') as file:
        # return [int(line) for line in file.readlines()]
        # return file.read().split(",")
        return [line.strip() for line in file]


def rotate_right(value, amount):
    for _ in range(amount):
        value = value[-1] + value[:-1]

    return value


def rotate_left(value, amount):
    for _ in range(amount):
        value = value[1:] + value[0]

    return value


def swap(value, first, second):
    """
    >>> swap('abcde', 1, 3)
    'adcbe'
    >>> swap('abcde', 0, 4)
    'ebcda'
    >>> swap('ab', 0, 1)
    'ba'
    >>> swap('dfcaehbg', 1, 2)
    'dcfaehbg'
    """

    first, second = min(first, second), max(first, second)
    return value[:first] + value[second] + value[first + 1:second] + value[first] + value[second + 1:]


def reverse_part(value, first, second):
    """
    >>> reverse_part('abcdef', 0, 2)
    'cbadef'
    >>> reverse_part('abcdef', 3, 5)
    'abcfed'
    >>> reverse_part('abcdef', 1, 4)
    'aedcbf'
    """

    first, second = min(first, second), max(first, second)
    return value[:first] + value[second:None if first == 0 else first - 1:-1] + value[second + 1:]


def move(value, start, end):
    letter = value[start]
    value = value[:start] + value[start + 1:]
    return value[:end] + letter + value[end:]


def scramble(instructions, password):
    for instruction in instructions:

        if match := ROTATE_LEFT.match(instruction):
            amount = int(match.group(1))
            password = rotate_left(password, amount)

        elif match := ROTATE_RIGHT.match(instruction):
            amount = int(match.group(1))
            password = rotate_right(password, amount)

        elif match := ROTATE.match(instruction):
            key = match.group(1)
            amount = password.index(key) + 1
            if amount >= 5:
                amount += 1

            password = rotate_right(password, amount)

        elif match := MOVE.match(instruction):
            start = int(match.group(1))
            end = int(match.group(2))
            password = move(password, start, end)

        elif match := SWAP.match(instruction):
            first = int(match.group(1))
            second = int(match.group(2))
            password = swap(password, first, second)

        elif match := SWAP_LETTER.match(instruction):
            first = match.group(1)
            second = match.group(2)
            password = swap(password, password.index(first), password.index(second))

        elif match := REVERSE.match(instruction):
            first = int(match.group(1))
            second = int(match.group(2))
            password = reverse_part(password, first, second)

        else:
            raise ValueError(f'"{instruction}"')

    return password


def unscramble(instructions, password):
    """
    >>> instructions = []
    >>> instructions.append('rotate based on position of letter f')
    >>> password = 'abcdefgh'
    >>> scrambled = scramble(instructions, password)
    >>> unscramble(instructions, scrambled) == password
    True
    """

    if len(password) != 8:
        raise ValueError

    # As password is length 8 we can work out how to undo rotate based on letter
    indexes = list(range(0, 8))
    moves = [index + (1 if index < 4 else 2) for index in indexes]
    destinations = [(index + move) % 8 for index, move in zip(indexes, moves)]
    undo = dict((destination, (destination - index) % 8) for destination, index in zip(destinations, indexes))

    for instruction in instructions[::-1]:

        if match := ROTATE_LEFT.match(instruction):
            amount = int(match.group(1))
            password = rotate_right(password, amount)

        elif match := ROTATE_RIGHT.match(instruction):
            amount = int(match.group(1))
            password = rotate_left(password, amount)

        elif match := ROTATE.match(instruction):
            key = match.group(1)
            index = password.index(key)
            amount = undo[index]
            password = rotate_left(password, amount)

        elif match := MOVE.match(instruction):
            start = int(match.group(1))
            end = int(match.group(2))
            password = move(password, end, start)

        elif match := SWAP.match(instruction):
            first = int(match.group(1))
            second = int(match.group(2))
            password = swap(password, first, second)

        elif match := SWAP_LETTER.match(instruction):
            first = match.group(1)
            second = match.group(2)
            password = swap(password, password.index(first), password.index(second))

        elif match := REVERSE.match(instruction):
            first = int(match.group(1))
            second = int(match.group(2))
            password = reverse_part(password, first, second)

        else:
            raise ValueError(f'"{instruction}"')

    return password


def part1(data):
    """
    >>> part1(read_input())
    'ghfacdbe'
    """

    return scramble(data, 'abcdefgh')


def part2(data):
    """
    >>> part2(read_input())
    'fhgcdaeb'
    """

    return unscramble(data, 'fbgdceah')


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
