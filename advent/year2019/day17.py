# -*- coding: utf-8 -*-

from advent.year2019.intcode import IntCode


def read_input(filename='input/2019/day17-input.txt'):
    with open(filename, encoding='utf8') as file:
        return [int(i) for i in file.read().split(",")]


def create_map(data):
    map_ascii = IntCode(data, memory_size=3000).run()

    x = 0
    y = 0
    diagram = {}

    for c in map_ascii:
        match c:
            case 35:
                diagram[(x, y)] = '#'
                x += 1
            case 46:
                diagram[(x, y)] = '.'
                x += 1
            case 10:
                x = 0
                y += 1
            case 94:
                diagram[(x, y)] = '#'
                robot = (x, y)
                x += 1
            case other:
                raise ValueError(other)

    return diagram, robot


def neighbours(x, y):
    return [(x, y), (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]


def part1(data):
    """
    >>> part1(read_input())
    5788
    """

    diagram, _ = create_map(data)

    height = max(y for (_, y) in diagram)
    width = max(x for (x, _) in diagram)

    intersections = []

    for x in range(1, width - 1):
        for y in range(1, height - 1):
            if all(diagram[n] == '#' for n in neighbours(x, y)):
                intersections.append((x, y))

    return sum(x * y for (x, y) in intersections)


def part2(data):
    """
    >>> part2(read_input())
    0
    """

    _, _ = create_map(data)
    return 0


def main():
    print(part1(read_input()))
    print(part2(read_input()))


if __name__ == "__main__":
    main()
