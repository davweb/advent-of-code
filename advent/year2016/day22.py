# -*- coding: utf-8 -*-
# pylint: disable=too-many-locals

import re
from heapq import heappush, heappop
from itertools import combinations
import numpy
from advent import taxicab_distance

PATTERN = re.compile(r'/dev/grid/node-x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T\s+(\d+)T\s+\d+%')


def read_input(filename='input/2016/day22-input.txt'):
    output = []

    with open(filename, encoding='utf8') as file:

        for line in file:
            if match := PATTERN.match(line):
                output.append([int(g) for g in match.groups()])

    return output


def sort_key(end, current, zero):
    return (
        taxicab_distance(current, end),
        taxicab_distance(current, zero),
        taxicab_distance(end, zero)
    )


def neighbours(location, width, height):
    x, y = location

    for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
        if 0 <= nx < width and 0 <= ny < height:
            yield (nx, ny)


def part1(data):
    """
    >>> part1(read_input())
    860
    """

    count = 0

    for a, b in combinations(data, 2):
        (a_used, a_avail) = a[3:5]
        (b_used, b_avail) = b[3:5]

        if 0 < a_used <= b_avail or 0 < b_used < a_avail:
            count += 1

    return count


def part2(data):
    """
    >>> data = read_input('input/2016/day22-test.txt')
    >>> part2(data)
    7
    >>> part2(read_input())
    200
    """

    width = max(node[0] for node in data) + 1
    height = max(node[1] for node in data) + 1

    size = numpy.zeros((width, height), numpy.int16)
    used = numpy.zeros((width, height), numpy.int16)

    for x, y, node_size, node_used, _ in data:
        size[x, y] = node_size
        used[x, y] = node_used

    start = (width - 1, 0)
    end = (0, 0)

    zero = numpy.unravel_index(numpy.flatnonzero(used == 0)[0], used.shape)

    queue = []

    # Count is used so we never to try compare numpy arrays
    count = 0
    best = None
    seen = {}

    heappush(queue, (sort_key(end, start, zero), 0, count, start, zero, used))

    while len(queue) > 0:
        _, steps, _, current, zero, grid = heappop(queue)

        if best is not None and steps >= best:
            continue

        key = (current, zero)

        if key in seen and seen[key] <= steps:
            continue

        seen[key] = steps

        if current == end:
            if best is None or steps < best:
                best = steps

        steps += 1

        for next_zero in neighbours(zero, width, height):
            if size[zero] >= grid[next_zero]:

                next_grid = numpy.array(grid)
                next_grid[zero] = grid[next_zero]
                next_grid[next_zero] = 0

                next_current = zero if next_zero == current else current

                sort_value = sort_key(end, next_current, next_zero)

                heappush(queue, (sort_value, steps, count, next_current, next_zero, next_grid))
                count += 1

    return best


def main():
    print(part1(read_input()))
    print(part2(read_input()))


if __name__ == "__main__":
    main()
