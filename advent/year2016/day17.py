# -*- coding: utf-8 -*-

from collections import deque
from advent import md5

INPUT = 'pvhmgsws'


def doors(route):
    """
    >>> list(doors('hijkl'))
    [('U', 0, -1), ('D', 0, 1), ('L', -1, 0)]
    """

    DIRECTIONS = (('U', 0, -1), ('D', 0, 1), ('L', -1, 0), ('R', 1, 0))

    hash_value = md5(route)
    door_states = (door in ('b', 'c', 'd', 'e', 'f') for door in hash_value[:4])

    for door_open, direction in zip(door_states, DIRECTIONS):
        if door_open:
            yield direction


def find_routes(value):
    """
    >>> shortest, longest = find_routes('ihgpwlah')
    >>> shortest
    'DDRRRD'
    >>> len(longest)
    370
    >>> shortest, longest = find_routes('kglvqrro')
    >>> shortest
    'DDUDRLRRUDRD'
    >>> len(longest)
    492
    >>> shortest, longest = find_routes('ulqzkmiv')
    >>> shortest
    'DRURDRUDDLLDLUURRDULRLDUUDDDRR'
    >>> len(longest)
    830
    """

    shortest = None
    longest = None
    queue = deque([((0, 0), '')])

    while queue:
        (location, route) = queue.popleft()

        if location == (3, 3):
            if shortest is None or len(shortest) > len(route):
                shortest = route

            if longest is None or len(shortest) < len(route):
                longest = route

            continue

        for direction, dx, dy in doors(value + route):
            dx += location[0]
            dy += location[1]

            if dx < 0 or dx > 3 or dy < 0 or dy > 3:
                continue

            queue.append(((dx, dy), route + direction))

    return (shortest, longest)


def part1and2():
    """
    >>> part1and2()
    DRRDRLDURD
    618
    """

    shortest, longest = find_routes(INPUT)
    print(shortest)
    print(len(longest))


def main():
    part1and2()


if __name__ == "__main__":
    main()
