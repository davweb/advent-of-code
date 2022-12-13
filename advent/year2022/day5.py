# -*- coding: utf-8 -*-

import re

STACK_PATTERN = re.compile(r'^(\[[A-Z]\]|   )' + r' (\[[A-Z]\]|   )' * 8)
MOVE_PATTERN = re.compile(r'move (\d+) from (\d+) to (\d+)')


def read_input():

    with open('input/2022/day5-input.txt', encoding='utf8') as file:
        piles = []

        while match := STACK_PATTERN.match(file.readline()):
            piles.append([x[1] for x in match.groups()])

        stacks = []

        for stack in zip(*piles[::-1]):
            stack = list(stack)
            while stack[-1] == ' ':
                stack.pop()
            stacks.append(stack)

        #  Skip blank line
        file.readline()

        moves = []

        while match := MOVE_PATTERN.match(file.readline()):
            moves.append([int(x) for x in match.groups()])

    return (stacks, moves)


def part1(data):
    """
    >>> part1(read_input())
    'FWSHSPJWM'
    """

    (stacks, moves) = data

    for number, source, dest in moves:
        for _ in range(number):
            stacks[dest - 1].append(stacks[source - 1].pop())

    return ''.join(stack[-1] for stack in stacks)


def part2(data):
    """
    >>> part2(read_input())
    'PWPWHGFZS'
    """

    (stacks, moves) = data

    for number, source, dest in moves:
        stacks[dest - 1].extend(stacks[source - 1][-number:])
        del stacks[source - 1][-number:]

    return ''.join(stack[-1] for stack in stacks)


def main():
    print(part1(read_input()))
    print(part2(read_input()))


if __name__ == "__main__":
    main()
