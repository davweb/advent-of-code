# -*- coding: utf-8 -*-

from collections import Counter
from enum import Enum


class Direction(Enum):
    NORTH = 0
    SOUTH = 1
    WEST = 2
    EAST = 3


DIRECTIONS = tuple(Direction)


def read_input(filename='input/2022/day23-input.txt'):
    elves = set()

    with open(filename, encoding='utf8') as file:
        for y, row in enumerate(file):
            for x, char in enumerate(row):
                if char == '#':
                    elves.add((x, y))

    return elves


def is_free(elf, elves, direction):
    """
    >>> is_free((0, 0), ((0, 0), (1, 1)), Direction.NORTH)
    True
    >>> is_free((0, 0), ((0, 0), (1, 1)), Direction.SOUTH)
    False
    >>> is_free((0, 0), ((0, 0), (1, 1)), Direction.WEST)
    True
    >>> is_free((0, 0), ((0, 0), (1, 1)), Direction.EAST)
    False
    """

    x, y = elf

    match direction:
        case Direction.NORTH:
            check = ((x - 1, y - 1), (x, y - 1), (x + 1, y - 1))
        case Direction.SOUTH:
            check = ((x - 1, y + 1), (x, y + 1), (x + 1, y + 1))
        case Direction.WEST:
            check = ((x - 1, y - 1), (x - 1, y), (x - 1, y + 1))
        case Direction.EAST:
            check = ((x + 1, y - 1), (x + 1, y), (x + 1, y + 1))

    return not any(possible in elves for possible in check)


def move(elf, elves, turn):
    """
    >>> move((0, 0), ((0, 0), (1, 1)), 0)
    (0, -1)
    >>> move((0, 0), ((0, 0), (1, 1)), 1)
    (-1, 0)
    """

    free = []

    for index in range(4):
        index = (index + turn) % 4
        direction = DIRECTIONS[index]
        free.append((direction, is_free(elf, elves, direction)))

    if all(space_is_free for _, space_is_free in free):
        return None

    for direction, space_is_free in free:
        if space_is_free:
            x, y = elf

            match direction:
                case Direction.NORTH:
                    return (x, y - 1)
                case Direction.SOUTH:
                    return (x, y + 1)
                case Direction.WEST:
                    return (x - 1, y)
                case Direction.EAST:
                    return (x + 1, y)

    return None


def process(elves, turn):
    moves = [(elf, move(elf, elves, turn)) for elf in elves]
    counts = Counter(move for _, move in moves)

    if counts[None] == len(elves):
        return False

    for elf, possible in moves:
        if possible is not None and counts[possible] == 1:
            elves.remove(elf)
            elves.add(possible)

    return True


def bounding_rectangle(elves):
    x, y = next(iter(elves))
    top = y
    left = x
    bottom = y
    right = x

    for elf in elves:
        x, y = elf
        top = min(top, y)
        left = min(left, x)
        bottom = max(bottom, y)
        right = max(right, x)

    return ((top, left), (bottom + 1, right + 1))


def empty_tiles(elves):
    (top, left), (bottom, right) = bounding_rectangle(elves)
    area = (bottom - top) * (right - left)
    return area - len(elves)


def part1(elves):
    """
    >>> part1(read_input('input/2022/day23-test.txt'))
    110
    >>> part1(read_input())
    3947
    """

    for turn in range(10):
        process(elves, turn)

    return empty_tiles(elves)


def part2(elves):
    """
    >>> part2(read_input('input/2022/day23-test.txt'))
    20
    >>> part2(read_input())
    1012
    """

    turn = 0

    while process(elves, turn):
        turn += 1

    return turn + 1


def main():
    print(part1(read_input()))
    print(part2(read_input()))


if __name__ == "__main__":
    main()
