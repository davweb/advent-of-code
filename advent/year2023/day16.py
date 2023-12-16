# -*- coding: utf-8 -*-

from enum import Enum
from collections import defaultdict


class Direction(Enum):
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)


def read_input(filename='input/2023/day16-input.txt'):
    grid = {}

    with open(filename, encoding='utf8') as file:
        for y, line in enumerate(file):
            for x, c in enumerate(line.strip()):
                grid[(x, y)] = c

    return grid


def bounds(grid):
    return max(x for x, _ in grid) + 1, max(y for _, y in grid) + 1


def move(location, direction):
    lx, ly = location
    dx, dy = direction.value
    return lx + dx, ly + dy


def reflect(grid, start_location, start_direction):
    beams = [(start_location, start_direction)]
    visits = defaultdict(set)

    width, height = bounds(grid)

    while beams:
        location, direction = beams.pop(0)
        x, y = location

        if not (0 <= x < width and 0 <= y < height):
            continue

        if direction in visits[location]:
            continue

        visits[location].add(direction)

        match grid[location], direction:
            # Carry straight on
            case ('.', _) | ('-', (Direction.LEFT | Direction.RIGHT)) | ('|', (Direction.UP | Direction.DOWN)):
                beams.append((move(location, direction), direction))
            # Split beams
            case '-', (Direction.UP | Direction.DOWN):
                beams.append((location, Direction.LEFT))
                beams.append((location, Direction.RIGHT))
            case '|', (Direction.LEFT | Direction.RIGHT):
                beams.append((location, Direction.UP))
                beams.append((location, Direction.DOWN))
            # Reflections
            case ('/', Direction.LEFT) | ('\\', Direction.RIGHT):
                beams.append((move(location, Direction.DOWN), Direction.DOWN))
            case ('/', Direction.RIGHT) | ('\\', Direction.LEFT):
                beams.append((move(location, Direction.UP), Direction.UP))
            case ('/', Direction.UP) | ('\\', Direction.DOWN):
                beams.append((move(location, Direction.RIGHT), Direction.RIGHT))
            case ('/', Direction.DOWN) | ('\\', Direction.UP):
                beams.append((move(location, Direction.LEFT), Direction.LEFT))

    return len(visits)


def part1(data):
    """
    >>> part1(read_input('input/2023/day16-sample.txt'))
    46
    >>> part1(read_input())
    6855
    """

    return reflect(data, (0, 0), Direction.RIGHT)


def part2(data):
    """
    >>> part2(read_input())
    7513
    """

    width, height = bounds(data)
    options = []

    for y in range(height):
        options.append(((0, y), Direction.RIGHT))
        options.append(((width - 1, y), Direction.LEFT))

    for x in range(width):
        options.append(((x, 0), Direction.DOWN))
        options.append(((x, height - 1), Direction.UP))

    return max(reflect(data, location, direction) for location, direction in options)


def main():
    print(part1(read_input()))
    print(part2(read_input()))


if __name__ == "__main__":
    main()
