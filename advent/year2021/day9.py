# -*- coding: utf-8 -*-

from math import prod


def read_input():
    with open('input/2021/day9-input.txt', encoding='utf8') as file:
        return [[int(height) for height in line.strip()] for line in file]


def find_low_points(data):
    for x, row in enumerate(data):
        for y, height in enumerate(row):

            if x > 0 and data[x - 1][y] <= height:
                continue

            if x < 99 and data[x + 1][y] <= height:
                continue

            if y > 0 and row[y - 1] <= height:
                continue

            if y < 99 and row[y + 1] <= height:
                continue

            yield (x, y)


def find_basin(data, point, found=None):
    if found is None:
        found = set()

    if point in found:
        return found

    x, y = point

    if data[x][y] == 9:
        return found

    found.add(point)

    if x > 0:
        find_basin(data, (x - 1, y), found)

    if x < 99:
        find_basin(data, (x + 1, y), found)

    if y > 0:
        find_basin(data, (x, y - 1), found)

    if y < 99:
        find_basin(data, (x, y + 1), found)

    return found


def part1(data):
    """
    >>> part1(read_input())
    456
    """

    return sum(data[x][y] + 1 for x, y in find_low_points(data))


def part2(data):
    """
    >>> part2(read_input())
    1047744
    """

    basins = [find_basin(data, point) for point in find_low_points(data)]
    sizes = [len(basin) for basin in basins]
    return prod(sorted(sizes)[:-4:-1])


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
