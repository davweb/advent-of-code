# -*- coding: utf-8 -*-

from enum import Enum
from itertools import cycle


class Direction(Enum):
    NORTH = 1
    WEST = 2
    SOUTH = 3
    EAST = 4


def read_input(filename='input/2023/day14-input.txt'):
    with open(filename, encoding='utf8') as file:
        return make_grid(file.read())


def make_grid(text):
    grid = []

    for line in text.strip().split('\n'):
        grid.append(list(line))

    return grid


def calculate_load(grid):
    """
    >>> calculate_load(make_grid('OOOO.#.O..\\nOO..#....#\\nOO..O##..O\\nO..#.OO...\\n........#.\\n..#....#.#\\n" + \\
    ...     "..O..#.O.O\\n..O.......\\n#....###..\\n#....#....\\n'))
    136
    """

    total = 0
    height = len(grid)

    for y, row in enumerate(grid):
        value = height - y
        total += sum(value for c in row if c == 'O')

    return total


def neighbour(location, direction, width, height):
    x, y = location

    match direction:
        case Direction.NORTH:
            return None if y == 0 else (x, y - 1)
        case Direction.EAST:
            return None if x + 1 == width else (x + 1, y)
        case Direction.SOUTH:
            return None if y + 1 == height else (x, y + 1)
        case Direction.WEST:
            return None if x == 0 else (x - 1, y)
        case _:
            raise ValueError(direction)


def make_snapshot(grid):
    return ''.join(''.join(c for c in row) for row in grid)


def roll(grid, direction):
    height = len(grid)
    width = len(grid[0])

    rocks = []

    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c == 'O':
                rocks.append((x, y))

    moved = True

    while moved:
        moved = False
        next_rocks = []

        for location in rocks:
            next_location = neighbour(location, direction, width, height)

            if next_location is None:
                continue

            nx, ny = next_location

            match grid[ny][nx]:
                case '#':
                    continue
                case '.':
                    x, y = location
                    grid[y][x] = '.'
                    grid[ny][nx] = 'O'
                    moved = True
                    next_rocks.append(next_location)
                case 'O':
                    next_rocks.append(location)

        rocks = next_rocks


def part1(grid):
    """
    >>> part1(read_input())
    108955
    """

    roll(grid, Direction.NORTH)
    return calculate_load(grid)


def part2(grid):
    """
    >>> part2(read_input())
    106689
    """

    max_count = 4000000000
    count = 0
    seen = set()
    cycle_first_count = None
    cycle_first_snapshot = None
    directions = cycle(Direction)

    while count < max_count:
        roll(grid, next(directions))
        count += 1

        snapshot = make_snapshot(grid)

        if snapshot == cycle_first_snapshot:
            period = count - cycle_first_count
            remaining = max_count - count
            count = max_count - remaining % period
        elif snapshot in seen and cycle_first_snapshot is None:
            cycle_first_count = count
            cycle_first_snapshot = snapshot
        else:
            seen.add(snapshot)

    return calculate_load(grid)


def main():
    print(part1(read_input()))
    print(part2(read_input()))


if __name__ == "__main__":
    main()
