# -*- coding: utf-8 -*-

from advent import taxicab_distance


def read_input():
    with open('input/2020/day12-input.txt', encoding='utf8') as file:
        return [(line[0], int(line[1:])) for line in file.readlines()]


def part1(data):
    """
    >>> part1((('F', 10), ('N', 3), ('F', 7), ('R', 90), ('F', 11)))
    25
    >>> part1(read_input())
    1424
    """

    DIRECTIONS = ['N', 'E', 'S', 'W']

    east, north = (0, 0)
    current = 'E'

    for (direction, val) in data:

        if direction == 'R':
            index = DIRECTIONS.index(current)
            index += val // 90
            index %= 4
            current = DIRECTIONS[index]
            continue

        if direction == 'L':
            index = DIRECTIONS.index(current)
            index -= val // 90
            index %= 4
            current = DIRECTIONS[index]
            continue

        if direction == 'F':
            direction = current

        if direction == 'N':
            north += val

        elif direction == 'S':
            north -= val

        elif direction == 'E':
            east += val

        elif direction == 'W':
            east -= val

    return taxicab_distance((0, 0), (east, north))


def part2(data):
    """
    >>> part2((('F', 10), ('N', 3), ('F', 7), ('R', 90), ('F', 11)))
    286
    >>> part2(read_input())
    63447
    """

    east, north = (0, 0)
    waypoint_east, waypoint_north = (10, 1)

    for (direction, val) in data:

        if direction == 'R':
            for _ in range(0, val // 90):
                waypoint_east, waypoint_north = (waypoint_north, - waypoint_east)

        elif direction == 'L':
            for _ in range(0, val // 90):
                waypoint_east, waypoint_north = (- waypoint_north, waypoint_east)

        elif direction == 'F':
            east += waypoint_east * val
            north += waypoint_north * val

        elif direction == 'N':
            waypoint_north += val

        elif direction == 'S':
            waypoint_north -= val

        elif direction == 'E':
            waypoint_east += val

        elif direction == 'W':
            waypoint_east -= val

    return taxicab_distance((0, 0), (east, north))


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
