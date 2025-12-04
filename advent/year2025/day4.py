# -*- coding: utf-8 -*-

def read_input(filename='input/2025/day4-input.txt'):
    grid = set()

    with open(filename, encoding='utf8') as file:
        for y, line in enumerate(file.readlines()):
            for x, c in enumerate(line.strip()):
                if c == '@':
                    grid.add((x, y))

    return grid


def neighbours(location):
    x, y = location
    return (
        (x - 1, y - 1), (x - 1, y), (x - 1, y + 1),
        (x, y - 1), (x, y + 1),
        (x + 1, y - 1), (x + 1, y), (x + 1, y + 1)
    )


def part1(grid):
    """
    >>> part1(read_input())
    1569
    """

    return sum(sum(n in grid for n in neighbours(cell)) < 4 for cell in grid)


def part2(grid):
    """
    >>> part2(read_input())
    9280
    """

    total = 0
    last_total = None

    while last_total != total:
        last_total = total

        for cell in list(grid):
            if sum(n in grid for n in neighbours(cell)) < 4:
                total += 1
                grid.remove(cell)

    return total


def main():
    print(part1(read_input()))
    print(part2(read_input()))


if __name__ == "__main__":
    main()
