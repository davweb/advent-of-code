# -*- coding: utf-8 -*-

def read_input():
    with open('input/2016/day3-input.txt', encoding='utf8') as file:
        return [[int(x) for x in line.split()] for line in file.readlines()]


def transform_input(data):
    """
    >>> list(transform_input([(101, 201, 301), (102, 202, 303), (103, 203, 303)]))
    [[101, 102, 103], [201, 202, 203], [301, 303, 303]]
    """

    triangles = [[],[],[]]

    for row in data:
        for value, triangle in zip(row, triangles):
            triangle.append(value)

            if len(triangle) == 3:
                yield triangle.copy()
                triangle.clear()


def count_triangles(data):
    """
    >>> count_triangles([(3, 4, 5)])
    1
    >>> count_triangles([(5, 4, 3)])
    1
    >>> count_triangles([(1, 2, 4)])
    0
    """

    count = 0

    for triangle in data:
        triangle = sorted(triangle)
        if triangle[0] + triangle[1] > triangle[2]:
            count += 1

    return count


def part1(data):
    """
    >>> part1(read_input())
    983
    """

    return count_triangles(data)


def part2(data):
    """
    >>> part2(read_input())
    1836
    """

    return count_triangles(transform_input(data))


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
