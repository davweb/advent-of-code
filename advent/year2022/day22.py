# -*- coding: utf-8 -*-
# pylint: disable=too-many-branches,too-many-statements

import re

GRID_PATTERN = re.compile(r'[ .#]+')
DIRECTIONS_PATTERN = re.compile(r'([LR]|\d+)')

RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3


def read_input(filename='input/2022/day22-input.txt'):
    grid = []
    width = None
    directions = None

    with open(filename, encoding='utf8') as file:
        while match := GRID_PATTERN.match(file.readline()):
            line = match.group(0)
            if width is None:
                width = len(line)

            row = list(line)
            while len(row) < width:
                row.append(' ')
            grid.append(row)

        directions = DIRECTIONS_PATTERN.findall(file.readline())

        for index, direction in enumerate(directions):
            if direction not in ('L', 'R'):
                directions[index] = int(direction)

    return (grid, directions)


def next_location(x, y, facing, grid):
    """
    >>> grid, _ = read_input()

    Moves that don't change face
    >>> next_location(55, 0, RIGHT, grid)
    (56, 0, 0)
    >>> next_location(99, 0, RIGHT, grid)
    (100, 0, 0)

    E -> B
    >>> next_location(149, 10, RIGHT, grid)
    (99, 139, 2)
    >>> next_location(99, 130, RIGHT, grid)
    (149, 19, 2)
    >>> next_location(99, 149, RIGHT, grid)
    (149, 0, 2)
    >>> next_location(149, 0, RIGHT, grid)
    (99, 149, 2)

    F -> E
    >>> next_location(49, 175, RIGHT, grid)
    (75, 149, 3)
    >>> next_location(75, 149, DOWN, grid)
    (49, 175, 2)

    F -> A
    >>> next_location(0, 169, LEFT, grid)
    (69, 0, 1)
    >>> next_location(69, 0, UP, grid)
    (0, 169, 0)

    A -> D
    >>> next_location(50, 44, LEFT, grid)
    (0, 105, 0)
    >>> next_location(0, 105, LEFT, grid)
    (50, 44, 0)

    C -> D
    >>> next_location(50, 89, LEFT, grid)
    (39, 100, 1)
    >>> next_location(39, 100, UP, grid)
    (50, 89, 0)

    A -> D
    >>> next_location(50, 13, LEFT, grid)
    (0, 136, 0)
    >>> next_location(0, 136, LEFT, grid)
    (50, 13, 0)

    C -> B
    >>> next_location(99, 60, RIGHT, grid)
    (110, 49, 3)
    >>> next_location(110, 49, DOWN, grid)
    (99, 60, 2)

    F -> B
    >>> next_location(19, 199, DOWN, grid)
    (119, 0, 1)
    >>> next_location(119, 0, UP, grid)
    (19, 199, 3)
    """

    width = len(grid[0])
    height = len(grid)

    next_x, next_y, next_facing = x, y, facing

    while True:
        if next_facing == UP:
            next_y = next_y - 1
        elif next_facing == RIGHT:
            next_x = next_x + 1
        elif next_facing == DOWN:
            next_y = next_y + 1
        elif next_facing == LEFT:
            next_x = next_x - 1
        else:
            raise ValueError()

        if next_x < 0:
            if 0 <= next_y <= 49:
                next_x, next_y = 0, 149 - next_y
                next_facing = RIGHT
            elif 50 <= next_y <= 99:
                next_x = next_y - 50
                next_y = 100
                next_facing = DOWN
            elif 100 <= next_y <= 149:
                next_x = 50
                next_y = 149 - next_y
                next_facing = RIGHT
            elif 150 <= next_y <= 199:
                next_x = next_y - 100
                next_y = 0
                next_facing = DOWN
            else:
                raise ValueError()

        elif next_x == width:
            if 0 <= next_y <= 49:
                next_x = 100
                next_y = 149 - next_y
                next_facing = LEFT
            elif 50 <= next_y <= 99:
                next_x = next_y + 50
                next_y = 49
                next_facing = UP
            elif 100 <= next_y <= 149:
                next_x = 149
                next_y = 149 - next_y
                next_facing = LEFT
            elif 150 <= next_y <= 199:
                next_x = next_y - 100
                next_y = 149
                next_facing = UP
            else:
                raise ValueError()

        elif next_y < 0:
            if 0 <= next_x <= 49:
                next_x, next_y = 50, 50 + next_x
                next_facing = RIGHT
            elif 50 <= next_x <= 99:
                next_x, next_y = 0, next_x + 100
                next_facing = RIGHT
            elif 100 <= next_x <= 149:
                next_x = next_x - 100
                next_y = 199
                next_facing = UP
            else:
                raise ValueError()

        elif next_y == height:
            if 0 <= next_x <= 49:
                next_x = next_x + 100
                next_y = 0
                next_facing = DOWN
            elif 50 <= next_x <= 99:
                next_x, next_y = 50, next_x + 100
                next_facing = LEFT
            elif 100 <= next_x <= 149:
                next_x, next_y = 100, next_x - 50
                next_facing = LEFT
            else:
                raise ValueError()

        if grid[next_y][next_x] != ' ':
            break

    return next_x, next_y, next_facing


def next_step(x, y, facing, grid):
    width = len(grid[0])
    height = len(grid)

    next_x, next_y = x, y

    while True:
        if facing == UP:
            next_y = next_y - 1
        elif facing == RIGHT:
            next_x = next_x + 1
        elif facing == DOWN:
            next_y = next_y + 1
        elif facing == LEFT:
            next_x = next_x - 1
        else:
            raise ValueError()

        if next_x < 0:
            next_x = width - 1
        if next_x == width:
            next_x = 0
        if next_y < 0:
            next_y = height - 1
        if next_y == height:
            next_y = 0

        if grid[next_y][next_x] != ' ':
            break

    return next_x, next_y, facing


def walk(data, next_move):
    grid, instructions = data

    facing = RIGHT
    x = 0
    y = 0

    while grid[y][x] != '.':
        x += 1

    while instructions:
        distance = instructions.pop(0)

        for _ in range(distance):
            next_x, next_y, next_facing = next_move(x, y, facing, grid)

            if grid[next_y][next_x] == '#':
                break

            x, y, facing = next_x, next_y, next_facing

        if instructions:
            turn = instructions.pop(0)
            facing = (facing + (1 if turn == 'R' else -1)) % 4

    return (y + 1) * 1000 + (x + 1) * 4 + facing


def part1(data):
    """
    >>> part1(read_input('input/2022/day22-test.txt'))
    6032
    >>> part1(read_input())
    77318
    """

    return walk(data, next_step)


def part2(data):
    """
    >>> part2(read_input())
    126017
    """

    return walk(data, next_location)


def main():
    print(part1(read_input()))
    print(part2(read_input()))


if __name__ == "__main__":
    main()
