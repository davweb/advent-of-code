# -*- coding: utf-8 -*-

import re
from enum import Enum

PATTERN = re.compile(r'([UDLR]) (\d+) \(#([a-z0-9]{6})\)')


def read_input(filename='input/2023/day18-input.txt'):
    with open(filename, encoding='utf8') as file:
        for line in file:
            result = PATTERN.match(line)
            yield result.group(1), int(result.group(2)), result.group(3)


class Direction(Enum):
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)


class Tile(Enum):
    EMPTY = 0
    WALL = 1
    COATING = 2


class Board:
    def __init__(self):
        self.horizontal = {}
        self.vertical = {}

    def add_horizontal_line(self, from_x, to_x, y, colour):
        if from_x > to_x:
            raise ValueError()

        if y not in self.horizontal:
            self.horizontal[y] = []

        self.horizontal[y].append((from_x, to_x, colour))

    def add_vertical_line(self, x, from_y, to_y, colour):
        if from_y > to_y:
            raise ValueError()

        if x not in self.vertical:
            self.vertical[x] = []

        self.vertical[x].append((from_y, to_y, colour))

    def add_line(self, start, end, colour):
        start_x, start_y = start
        end_x, end_y = end

        if start_y == end_y:
            start_x, end_x = min(start_x, end_x), max(start_x, end_x)
            self.add_horizontal_line(start_x, end_x, start_y, colour)
        elif start_x == end_x:
            start_y, end_y = min(start_y, end_y), max(start_y, end_y)
            self.add_vertical_line(start_x, start_y, end_y, colour)
        else:
            raise ValueError()

    def __getitem__(self, key):
        x, y = key

        if x in self.vertical:
            for from_y, to_y, colour in self.vertical[x]:
                if from_y <= y <= to_y:
                    return colour

        if y in self.horizontal:
            for from_x, to_x, colour in self.horizontal[y]:
                if from_x <= x <= to_x:
                    return colour

        return None

    def top_left(self):
        y = min(self.horizontal.keys())
        lines = sorted(self.horizontal[y])
        return lines[0][0], y

    def slice(self, y):
        slice_lines = []
        end = None

        for x, lines in self.vertical.items():
            for from_y, to_y, colour in lines:
                if from_y <= y <= to_y:
                    slice_lines.append((x, x, colour))
                    line_end = to_y - 1
                    end = line_end if end is None else min(line_end, end)

        if y in self.horizontal:
            slice_lines.extend(self.horizontal[y])
            end = y

        #  look for other parts of the hole in this range
        for i in range(y + 1, end + 1):
            if i in self.horizontal:
                end = i - 1
                break

        return sorted(slice_lines), end - y + 1

    def y_range(self):
        return min(self.horizontal.keys()), max(self.horizontal.keys())

    def neighbour_lines(self, location, filter_colour):
        lx, ly = location

        for x in range(lx - 1, lx + 2):
            if x in self.vertical:
                for from_y, to_y, colour in self.vertical[x]:
                    if (from_y <= ly - 1 <= to_y or from_y <= ly + 1 <= to_y) and colour == filter_colour:
                        yield True, from_y, to_y

        for y in range(ly - 1, ly + 2):
            if y in self.horizontal:
                for from_x, to_x, colour in self.horizontal[y]:
                    if (from_x <= lx - 1 <= to_x or from_x <= lx + 1 <= to_x) and colour == filter_colour:
                        yield False, from_x, to_x


def move(location, direction):
    lx, ly = location
    dx, dy = direction.value
    return lx + dx, ly + dy


def turn(direction, clockwise):
    output = None

    if clockwise:
        match direction:
            case Direction.UP:
                output = Direction.RIGHT
            case Direction.RIGHT:
                output = Direction.DOWN
            case Direction.DOWN:
                output = Direction.LEFT
            case Direction.LEFT:
                output = Direction.UP
    else:
        match direction:
            case Direction.UP:
                output = Direction.LEFT
            case Direction.LEFT:
                output = Direction.DOWN
            case Direction.DOWN:
                output = Direction.RIGHT
            case Direction.RIGHT:
                output = Direction.UP

    return output


def dig_hole(data):
    grid = Board()
    x, y = 0, 0

    for direction, count in data:

        match direction:
            case 'U':
                grid.add_vertical_line(x, y - count, y, Tile.WALL)
                y -= count
            case 'D':
                grid.add_vertical_line(x, y, y + count, Tile.WALL)
                y += count
            case 'L':
                grid.add_horizontal_line(x - count, x, y, Tile.WALL)
                x -= count
            case 'R':
                grid.add_horizontal_line(x, x + count, y, Tile.WALL)
                x += count

    if (x, y) != (0, 0):
        raise ValueError((x, y))

    return grid


def draw_outline(grid):
    """
    Draw an outline around the hole to make it easier to calculate the size
    """

    start_x, start_y = grid.top_left()
    start = (start_x, start_y - 1)

    location = start
    direction = Direction.RIGHT
    last_turn = location
    lines = None

    while location != start or lines is None:
        # Can we take a shortcut
        lines = list(grid.neighbour_lines(location, Tile.WALL))

        if len(lines) == 1:
            vertical, line_start, line_end = lines[0]
            lx, ly = location

            if vertical:
                if direction == Direction.UP and ly > line_start + 1:
                    location = lx, line_start + 1
                if direction == Direction.DOWN and ly < line_end - 1:
                    location = lx, line_end - 1
            else:
                if direction == Direction.LEFT and lx > line_start + 1:
                    location = line_start + 1, ly
                if direction == Direction.RIGHT and lx < line_end - 1:
                    location = line_end - 1, ly

        # Can we turn right
        next_direction = turn(direction, True)
        next_location = move(location, next_direction)

        if grid[next_location] != Tile.WALL:
            grid.add_line(last_turn, location, Tile.COATING)
            last_turn = next_location
            location = next_location
            direction = next_direction
            continue

       # Can we go straight on
        next_location = move(location, direction)
        if grid[next_location] != Tile.WALL:
            location = next_location
            continue

        #  Otherwise Turn Left
        grid.add_line(last_turn, location, Tile.COATING)
        direction = turn(direction, False)
        last_turn = location

    grid.add_line(last_turn, location, Tile.COATING)


def count_inside(grid):
    count = 0
    min_y, max_y = grid.y_range()
    y = min_y
    fill_start = None

    while y <= max_y:
        grid_slice, height = grid.slice(y)
        previous_colour = None

        for line in grid_slice:
            start_x, _, colour = line

            if previous_colour == Tile.COATING and colour == Tile.WALL:
                fill_start = start_x

            if previous_colour == Tile.WALL and colour == Tile.COATING:
                count += (start_x - fill_start) * height

            previous_colour = colour

        y += height

    return count


def hex_to_dig(value):
    """
    >>> hex_to_dig('70c710')
    ('R', 461937)
    >>> hex_to_dig('0dc571')
    ('D', 56407)
    """

    return 'RDLU'[int(value[-1])], int(value[:-1], 16)


def part1(data):
    """
    >>> part1(read_input())
    95356
    """

    grid = dig_hole((direction, count) for direction, count, _ in data)
    draw_outline(grid)
    return count_inside(grid)


def part2(data):
    """
    >>> part2(read_input())
    92291468914147
    """

    grid = dig_hole(hex_to_dig(hex) for _, _, hex in data)
    draw_outline(grid)
    return count_inside(grid)


def main():
    print(part1(read_input()))
    print(part2(read_input()))


if __name__ == "__main__":
    main()
