# -*- coding: utf-8 -*-

from collections import deque


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

    return count_bits(x * x + 3 * x + 2 * x * y + y + y * y + seed) % 2 == 1


def moves(location, seed):
    (x, y) = location

    for (nx, ny) in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
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


def part1():
    """
    >>> part1()
    86
    """

    return find_route((31, 39), 1364)


def part2():
    """
    >>> part2()
    127
    """

    return count_locations(1364)


def main():
    print(part1())
    print(part2())


if __name__ == "__main__":
    main()
