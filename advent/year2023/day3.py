# -*- coding: utf-8 -*-

import numpy


def read_input(filename='input/2023/day3-input.txt'):
    with open(filename, encoding='utf8') as file:
        data = []

        for line in file:
            data.append(list(line.strip()))

        grid = numpy.array(data)
        return numpy.transpose(grid)


def adjacent(index, grid):
    x, y = index
    width, height = numpy.shape(grid)

    for nx, ny in ((x - 1, y - 1), (x - 1, y), (x - 1, y + 1), (x, y - 1),
                   (x, y + 1), (x + 1, y - 1), (x + 1, y), (x + 1, y + 1)):
        if 0 <= nx < width and 0 <= ny < height:
            yield nx, ny


def adjacent_to_symbol(index, grid):
    for nearby in adjacent(index, grid):
        c = grid[nearby]
        if c != '.' and not c.isdigit():
            return True

    return False


def find_numbers(grid):
    width, height = numpy.shape(grid)
    numbers = []

    for y in range(height):
        digits = None

        for x in range(width):
            c = grid[x, y]
            if c.isdigit():
                if digits is None:
                    start_x = x
                    digits = c
                else:
                    digits += c
            elif digits is not None:
                numbers.append((set((dx, y) for dx in range(start_x, x)), int(digits)))
                digits = None

        if digits is not None:
            numbers.append((set((dx, y) for dx in range(start_x, x)), int(digits)))

    return numbers


def part1(grid):
    """
    >>> part1(read_input())
    559667
    """

    total = 0

    for (indexes, value) in find_numbers(grid):
        if any(adjacent_to_symbol(index, grid) for index in indexes):
            total += value

    return total


def part2(grid):
    """
    >>> part2(read_input())
    86841457
    """

    numbers = find_numbers(grid)
    total = 0

    for index in numpy.ndindex(grid.shape):
        if grid[index] == '*':
            ratio = 1
            count = 0
            adjacent_cells = set(adjacent(index, grid))

            for (indexes, value) in numbers:
                if adjacent_cells & indexes:
                    ratio *= value
                    count += 1

            if count == 2:
                total += ratio

    return total


def main():
    print(part1(read_input()))
    print(part2(read_input()))


if __name__ == "__main__":
    main()
