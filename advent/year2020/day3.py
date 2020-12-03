#!/usr/local/bin/python3

from math import prod

def read_input():
    file = open('input/2020/day3-input.txt', 'r')
    return [[c == '#' for c in line.strip()] for line in file.readlines()]


def count_trees(data, route):
    """
    >>> count_trees([
    ...     [False, False, True, True, False, False, False, False, False, False, False],
    ...     [True, False, False, False, True, False, False, False, True, False, False],
    ...     [False, True, False, False, False, False, True, False, False, True, False],
    ...     [False, False, True, False, True, False, False, False, True, False, True],
    ...     [False, True, False, False, False, True, True, False, False, True, False],
    ...     [False, False, True, False, True, True, False, False, False, False, False],
    ...     [False, True, False, True, False, True, False, False, False, False, True],
    ...     [False, True, False, False, False, False, False, False, False, False, True],
    ...     [True, False, True, True, False, False, False, True, False, False, False],
    ...     [True, False, False, False, True, True, False, False, False, False, True],
    ...     [False, True, False, False, True, False, False, False, True, False, True]
    ... ], (3, 1))
    7
    """

    dx, dy = route
    height = len(data)
    width = len(data[0])

    x = 0
    y = 0
    trees = 0

    while y < height:
        if data[y][x]:
            trees += 1
        
        x = (x + dx) % width
        y += dy

    return trees


def part1(data):
    """
    >>> part1(read_input())
    159
    """
    
    return count_trees(data, (3, 1))


def part2(data):
    """
    >>> part2(read_input())
    6419669520
    """
    
    routes = ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2))
    return prod(count_trees(data, route) for route in routes)


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
