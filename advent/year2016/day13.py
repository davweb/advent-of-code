# -*- coding: utf-8 -*-

import re
from collections import deque

PATTERN = re.compile(r'(\d+) <-> ((\d+, )*\d+)')

def read_input():
    with open('input/2021/day1-input.txt', encoding='utf8') as file:
        #return [int(line) for line in file.readlines()]
        #return file.read().split(",")
        return 0


def count_bits(num):
    """
    >>> count_bits(0)
    0
    >>> count_bits(2)
    1
    >>> count_bits(7)
    3
    >>> count_bits(8)
    1
    """

    count = 0

    while num > 0:
        count += num % 2
        num //= 2

    return count


def is_wall(x, y, seed):
    """
    >>> is_wall(0, 0, 10)
    False
    >>> is_wall(3, 0, 10)
    True
    >>> is_wall(7, 0, 10)
    False
    >>> is_wall(9, 1, 10)
    True
    """

    return count_bits(x*x + 3*x + 2*x*y + y + y*y + seed) % 2 == 1


def moves(location, seed):
    (x, y) = location

    for (nx, ny) in ((x - 1 , y), (x + 1 , y), (x, y - 1), (x, y + 1)):
        if nx < 0 or ny < 0:
            continue

        if is_wall(nx, ny, seed):
            continue

        yield (nx, ny)


def find_route(destination, seed):
    """
    >>> find_route((7, 4), 10)
    11
    """

    shortest = None
    queue = deque([((1, 1), ())])

    while queue:
        location, route = queue.popleft()
        route = route + (location, )

        if shortest and shortest < len(route):
            continue

        if location == destination:
            shortest = len(route)
            continue

        for move in moves(location, seed):
            if move in route:
                continue

            queue.append((move, route))

    return shortest - 1


def count_locations(seed):
    """
    >>> find_route((7, 4), 10)
    11
    """

    visited = set()
    queue = deque([((1, 1), ())])

    while queue:
        location, route = queue.popleft()
        route = route + (location, )

        if len(route) > 51:
            continue

        visited.add(location)

        for move in moves(location, seed):
            if move in route:
                continue

            queue.append((move, route))

    return len(visited)


def part1(data):
    """
    >>> part1(read_input())
    86
    """

    return find_route((31, 39), 1364)


def part2(data):
    """
    >>> part2(read_input())
    127
    """

    return count_locations(1364)


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
