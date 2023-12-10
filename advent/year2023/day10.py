# -*- coding: utf-8 -*-
#  pylint: disable=line-too-long,too-many-return-statements

from enum import Enum


class Direction(Enum):
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)


def read_input(filename='input/2023/day10-input.txt'):
    with open(filename, encoding='utf8') as file:
        return parse_grid(file.read())


def parse_grid(text):
    grid = {}

    for y, line in enumerate(text.strip().split('\n')):
        for x, c in enumerate(line.strip()):
            grid[(x, y)] = c

    return grid


def legal_moves(pipe):
    """
    >>> legal_moves('-')
    (<Direction.LEFT: (-1, 0)>, <Direction.RIGHT: (1, 0)>)
    """

    match pipe:
        case '-' | '=':
            return (Direction.LEFT, Direction.RIGHT)
        case '|' | '!':
            return (Direction.UP, Direction.DOWN)
        case 'L':
            return (Direction.UP, Direction.RIGHT)
        case 'J':
            return (Direction.LEFT, Direction.UP)
        case '7':
            return (Direction.LEFT, Direction.DOWN)
        case 'F':
            return (Direction.DOWN, Direction.RIGHT)
        case 'S':
            return (Direction.LEFT, Direction.RIGHT, Direction.UP, Direction.DOWN)
        case '.' | ' ':
            return ()
        case _:
            raise ValueError(pipe)


def neighbours(location):
    x, y = location
    return ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1))


def opposite_direction(direction):
    match direction:
        case Direction.UP:
            return Direction.DOWN
        case Direction.DOWN:
            return Direction.UP
        case Direction.LEFT:
            return Direction.RIGHT
        case Direction.RIGHT:
            return Direction.LEFT
        case _:
            raise ValueError(direction)


def next_locations(location, pipe):
    x, y = location

    for direction in legal_moves(pipe):
        dx, dy = direction.value
        yield (x + dx, y + dy), opposite_direction(direction)


def expand_grid(grid):
    """Double the size of the grid to move between pipes"""

    new_grid = {}

    for location, pipe in grid.items():
        x, y = location
        nx, ny = 2 * x, 2 * y
        new_grid[(nx, ny)] = pipe

        match pipe:
            case '-':
                new_grid[(nx + 1, ny)] = '='
                new_grid[(nx - 1, ny)] = '='
            case '|':
                new_grid[(nx, ny + 1)] = '!'
                new_grid[(nx, ny - 1)] = '!'
            case 'F':
                new_grid[(nx + 1, ny)] = '='
                new_grid[(nx, ny + 1)] = '!'
            case 'J':
                new_grid[(nx - 1, ny)] = '='
                new_grid[(nx, ny - 1)] = '!'
            case 'L':
                new_grid[(nx + 1, ny)] = '='
                new_grid[(nx, ny - 1)] = '!'
            case '7':
                new_grid[(nx - 1, ny)] = '='
                new_grid[(nx, ny + 1)] = '!'

    height = max(y for (_, y) in new_grid)
    width = max(x for (x, _) in new_grid)

    for y in range(height):
        for x in range(width):
            location = (x, y)
            if location not in new_grid:
                new_grid[location] = ' '

    return new_grid


def is_enclosed(tile, grid):
    visited = set()
    queue = [tile]

    while queue:
        location = queue.pop()
        if location in visited:
            continue

        visited.add(location)

        for neighbour in neighbours(location):
            if neighbour not in grid:
                return False

            if grid[neighbour] in (' ', '.'):
                queue.append(neighbour)

    return True


def part1(grid):
    """
    >>> part1(read_input())
    6800
    """

    start = [location for location, value in grid.items() if value == 'S'][0]

    queue = []
    distances = {}
    furthest = 0

    queue.append((start, 0))

    while queue:
        location, distance = queue.pop(0)

        if location in distances and distances[location] <= distance:
            continue

        distances[location] = distance
        furthest = max(furthest, distance)
        distance += 1

        pipe = grid[location]

        for next_location, incoming_direction in next_locations(location, pipe):
            if incoming_direction in legal_moves(grid[next_location]):
                queue.append((next_location, distance))

    return furthest


def part2(data):
    """
    >>> example = "..........\\n.S------7.\\n.|F----7|.\\n.||....||.\\n.||....||.\\n.|L-7F-J|.\\n.|..||..|.\\n.L--JL--J.\\n.........."
    >>> part2(parse_grid(example))
    4
    >>> example2 = '.F----7F7F7F7F-7....\\n.|F--7||||||||FJ....\\n.||.FJ||||||||L7....\\nFJL7L7LJLJ||LJ.L-7..\\nL--J.L7...LJS7F-7L7.\\n....F-J..F7FJ|L7L7L7\\n....L7.F7||L7|.L7L7|\\n.....|FJLJ|FJ|F7|.LJ\\n....FJL-7.||.||||...\\n....L---J.LJ.LJLJ...\\n'
    >>> part2(parse_grid(example2))
    8
    >>> example3 = "FF7FSF7F7F7F7F7F---7\\nL|LJ||||||||||||F--J\\nFL-7LJLJ||||||LJL-77\\nF--JF--7||LJLJ7F7FJ-\\nL---JF-JLJ.||-FJLJJ7\\n|F|F-JF---7F7-L7L|7|\\n|FFJF7L7F-JF7|JL---7\\n7-L-JL7||F7|L7F-7F7|\\nL.L7LFJ|||||FJL7||LJ\\nL7JLJL-JLJLJL--JLJ.L\\n"
    >>> part2(parse_grid(example3))
    10
    >>> part2(read_input())
    483
    """

    # double the size of the grid so we can move between pipes
    grid = expand_grid(data)

    #  Traverse the grid to find the loop
    start = [location for location, value in grid.items() if value == 'S'][0]
    queue = []
    visited = set()
    queue.append(start)

    while queue:
        location = queue.pop(0)

        if location in visited:
            continue

        visited.add(location)
        pipe = grid[location]

        for next_location, incoming_direction in next_locations(location, pipe):
            if next_location not in grid:
                continue
            if incoming_direction in legal_moves(grid[next_location]):
                queue.append(next_location)

    # Convert any pipe not part of the loop in to empty space
    for location, pipe in grid.items():
        if pipe not in (' ', '.') and location not in visited:
            # original pipes get a . new pipes a space
            if pipe in ('!', '='):
                grid[location] = ' '
            else:
                grid[location] = '.'

    #  We'll only check for tiles in the original grid
    tiles = [location for location, pipe in grid.items() if pipe == '.']

    return sum(is_enclosed(tile, grid) for tile in tiles)


def main():
    print(part1(read_input()))
    print(part2(read_input()))


if __name__ == "__main__":
    main()
