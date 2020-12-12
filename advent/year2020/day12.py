# -*- coding: utf-8 -*-

from advent import taxicab_distance


def read_input():
    file = open("input/2020/day12-input.txt", "r")
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

    for (dir, val) in data:

        if dir == 'R':
            index = DIRECTIONS.index(current)
            index += val // 90
            index %= 4
            current = DIRECTIONS[index]
            continue

        if dir == 'L':
            index = DIRECTIONS.index(current)
            index -= val // 90
            index %= 4
            current = DIRECTIONS[index]
            continue

        if dir == 'F':
            dir = current

        if dir == 'N':
            north += val

        elif dir == 'S':
            north -= val
            
        elif dir == 'E':
            east += val

        elif dir == 'W':
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

    for (dir, val) in data:

        if dir == 'R':
            for _ in range(0, val // 90):
                waypoint_east, waypoint_north = (waypoint_north, - waypoint_east)

        elif dir == 'L':
            for _ in range(0, val // 90):
                waypoint_east, waypoint_north = (- waypoint_north, waypoint_east)
                
        elif dir == 'F':
            east += waypoint_east * val
            north += waypoint_north * val

        elif dir == 'N':
            waypoint_north += val

        elif dir == 'S':
            waypoint_north -= val

        elif dir == 'E':
            waypoint_east += val

        elif dir == 'W':
            waypoint_east -= val

    return taxicab_distance((0, 0), (east, north))


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
