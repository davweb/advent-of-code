# -*- coding: utf-8 -*-

from copy import deepcopy


def read_input(filename='input/2023/day22-input.txt'):
    bricks = []

    with open(filename, encoding='utf8') as file:
        for line in file:
            start, end = line.strip().split('~')
            bricks.append([tuple(int(i) for i in start.split(',')), tuple(int(i) for i in end.split(','))])

    return bricks


def at_bottom(brick):
    start, end = brick
    return start[2] == 1 or end[2] == 1


def down(brick):
    start, end = brick
    sx, sy, sz = start
    ex, ey, ez = end

    z = min(sz, ez) - 1

    for x in range(sx, ex + 1):
        for y in range(sy, ey + 1):
            yield (x, y, z)


def up(brick):
    start, end = brick
    sx, sy, sz = start
    ex, ey, ez = end

    z = max(sz, ez) + 1

    for x in range(sx, ex + 1):
        for y in range(sy, ey + 1):
            yield (x, y, z)


def cubes(brick):
    start, end = brick
    sx, sy, sz = start
    ex, ey, ez = end

    for x in range(sx, ex + 1):
        for y in range(sy, ey + 1):
            for z in range(sz, ez + 1):
                yield x, y, z


def make_grid(bricks):
    grid = {}

    for brick_id, brick in enumerate(bricks):
        for location in cubes(brick):
            grid[location] = brick_id

    return grid


def drop_bricks(bricks):
    bricks = deepcopy(bricks)
    grid = make_grid(bricks)

    moved = True
    dropped = set()

    while moved:
        moved = False

        for brick_id, brick in enumerate(bricks):
            if at_bottom(brick):
                continue

            if all(location not in grid for location in down(brick)):
                moved = True
                dropped.add(brick_id)

                for location in cubes(brick):
                    del grid[location]

                brick[0] = (brick[0][0], brick[0][1], brick[0][2] - 1)
                brick[1] = (brick[1][0], brick[1][1], brick[1][2] - 1)

                for location in cubes(brick):
                    grid[location] = brick_id

    return bricks, len(dropped)


def find_candidates(bricks):
    grid = make_grid(bricks)

    disintegrate = 0

    for brick in bricks:
        supporting = set()

        for location in up(brick):
            if location in grid:
                supporting.add(grid[location])

        can_disintegrate = True

        for supported_id in supporting:
            supported = bricks[supported_id]
            supported_by = set()

            for location in down(supported):
                if location in grid:
                    supported_by.add(grid[location])

            if len(supported_by) == 1:
                can_disintegrate = False
                break

        if can_disintegrate:
            disintegrate += 1

    return disintegrate


def part1(data):
    """
    >>> part1(read_input())
    475
    """

    bricks, _ = drop_bricks(data)
    return find_candidates(bricks)


def part2(data):
    """
    >>> part2(read_input())
    79144
    """

    bricks, _ = drop_bricks(data)
    would_fall = 0

    for candidate in range(len(bricks)):
        _, drop_count = drop_bricks(bricks[0:candidate] + bricks[candidate + 1:])
        would_fall += drop_count

    return would_fall


def main():
    print(part1(read_input()))
    print(part2(read_input()))


if __name__ == "__main__":
    main()
