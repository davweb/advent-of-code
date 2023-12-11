# -*- coding: utf-8 -*-

from itertools import combinations


def read_input(filename='input/2023/day11-input.txt'):
    with open(filename, encoding='utf8') as file:
        data = []

        for line in file:
            data.append([('#' if c == '#' else 1) for c in line.strip()])

        return data


def expand_grid(data, factor):
    grid = []

    for row in data:
        if not any(c == '#' for c in row):
            grid.append([factor * c for c in row])
        else:
            grid.append(list(row))

    return grid


def bounds(a, b):
    ax, ay = a
    bx, by = b

    return (min(ax, bx), min(ay, by)), (max(ax, bx), max(ay, by))


def calculate_distances(data, factor):
    grid = expand_grid(data, factor)

    # transpose array
    grid = expand_grid(zip(*grid), factor)

    galaxies = []

    for y, row in enumerate(grid):
        for x, value in enumerate(row):
            if value == '#':
                galaxies.append((x, y))
                grid[y][x] = 1

    total = 0

    for a, b in combinations(galaxies, 2):
        (lower_x, lower_y), (upper_x, upper_y) = bounds(a, b)

        total += sum(grid[lower_y][x] for x in range(lower_x + 1, upper_x + 1))
        total += sum(grid[y][upper_x] for y in range(lower_y + 1, upper_y + 1))

    return total


def part1(data):
    """
    >>> part1(read_input())
    9329143
    """

    return calculate_distances(data, 2)


def part2(data):
    """
    >>> part2(read_input())
    710674907809
    """

    return calculate_distances(data, 1000000)


def main():
    print(part1(read_input()))
    print(part2(read_input()))


if __name__ == "__main__":
    main()
