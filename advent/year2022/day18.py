# -*- coding: utf-8 -*-

from collections import deque
import numpy

AIR = 0
LAVA = 1
WATER = 2


def read_input():
    with open('input/2022/day18-input.txt', encoding='utf8') as file:
        return [[int(edge) for edge in line.split(',')] for line in file]


def adjacent(cube, model):
    x, y, z = cube
    width, height, depth = numpy.shape(model)

    for nx, ny, nz in ((x + 1, y, z), (x, y + 1, z), (x, y, z + 1), (x - 1, y, z), (x, y - 1, z), (x, y, z - 1)):
        if 0 <= nx < width and 0 <= ny < height and 0 <= nz < depth:
            yield nx, ny, nz


def create_model(cubes):
    shape = []

    for axis in range(3):
        min_value = min(cube[axis] for cube in cubes)
        offset = 2 - min_value

        for cube in cubes:
            cube[axis] += offset

        max_value = max(cube[axis] for cube in cubes) + 2
        shape.append(max_value + 1)

    model = numpy.full(shape, AIR)

    for cube in cubes:
        model[*cube] = LAVA

    return model


def count_faces(model, next_to):
    area = 0

    for cube in numpy.argwhere(model == LAVA):
        area += sum(1 for next_cube in adjacent(cube, model) if model[next_cube] == next_to)

    return area


def part1(cubes):
    """
    >>> part1([[1,1,1], [2,1,1]])
    10
    >>> sample = [[2,2,2], [1,2,2], [3,2,2], [2,1,2], [2,3,2], [2,2,1], [2,2,3], \\
    ...     [2,2,4], [2,2,6], [1,2,5], [3,2,5], [2,1,5], [2,3,5]]
    >>> part1(sample)
    64
    >>> part1(read_input())
    3636
    """

    model = create_model(cubes)
    return count_faces(model, AIR)


def part2(cubes):
    """
    >>> part2([[1,1,1], [2,1,1]])
    10
    >>> sample = [[2,2,2], [1,2,2], [3,2,2], [2,1,2], [2,3,2], [2,2,1], [2,2,3], \\
    ...     [2,2,4], [2,2,6], [1,2,5], [3,2,5], [2,1,5], [2,3,5]]
    >>> part2(sample)
    58
    >>> part2(read_input())
    2102
    """

    model = create_model(cubes)

    queue = deque()
    queue.append((0, 0, 0))

    while queue:
        cube = queue.pop()
        contents = model[cube]

        if contents == AIR:
            model[cube] = WATER
            queue.extend(adjacent(cube, model))

    return count_faces(model, WATER)


def main():
    print(part1(read_input()))
    print(part2(read_input()))


if __name__ == "__main__":
    main()
