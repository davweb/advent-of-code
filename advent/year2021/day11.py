# -*- coding: utf-8 -*-


def read_input():
    with open('input/2021/day11-input.txt', encoding='utf8') as file:
        return [[int(c) for c in line.strip()] for line in file.readlines()]


def valid(point):
    x, y = point
    return 0 <= x <= 9 and 0 <= y <= 9


def adjacent(point):
    x, y = point
    options = ((x - 1, y - 1), (x, y - 1), (x + 1, y - 1), (x - 1, y),
               (x + 1, y), (x - 1, y + 1), (x, y + 1), (x + 1, y + 1))
    return [point for point in options if valid(point)]


def take_turn(octopuses):
    for y, row in enumerate(octopuses):
        for x, value in enumerate(row):
            octopuses[y][x] = value + 1

    flashed = set()

    while True:
        flash = None

        for y, row in enumerate(octopuses):
            for x, value in enumerate(row):
                point = (x, y)

                if value > 9 and point not in flashed:
                    flash = point

        if flash is None:
            break

        flashed.add(flash)

        for near in adjacent(flash):
            x, y = near
            octopuses[y][x] += 1

    for y, row in enumerate(octopuses):
        for x, value in enumerate(row):
            octopuses[y][x] = 0 if value > 9 else value

    return len(flashed)


def part1(data):
    """
    >>> part1(read_input())
    1694
    """

    flashes = 0

    for _ in range(100):
        flashes += take_turn(data)

    return flashes


def part2(data):
    """
    >>> part2(read_input())
    346
    """

    step = 1

    while take_turn(data) != 100:
        step += 1

    return step


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
