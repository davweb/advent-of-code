#!/usr/local/bin/python3

from collections import defaultdict
from advent import bounds
from advent.year2019.intcode import IntCode

DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]


def read_input():
    with open('input/2019/day11-input.txt', encoding='utf-8') as file:
        return [int(code) for code in file.read().split(',')]


def paint(code, painted=None):
    if painted is None:
        painted = []

    hull = defaultdict(int)

    for point in painted:
        hull[point] = 1

    robot = IntCode(code)

    direction = 0
    point = (0, 0)

    while True:
        input_value = [hull[point]]

        paint_result = robot.execute(input_value)

        if paint_result is None:
            break

        turn = robot.execute()
        hull[point] = paint_result

        if turn == 0:
            turn = -1

        direction = (direction + turn) % len(DIRECTIONS)
        move = DIRECTIONS[direction]
        point = (point[0] + move[0], point[1] + move[1])

    return hull


def part1(code):
    """
    >>> part1(read_input())
    1747
    """

    return len(paint(code))


def part2(code):
    """
    >>> from advent import md5
    >>> md5(part2(read_input()))
    '02f9c4484ef489931028014595e96565'
    """

    hull = paint(code, [(0, 0)])

    points = [point for point, value in hull.items() if value]

    (left, top), (right, bottom) = bounds(points)
    output = []

    for y in range(top, bottom + 1):
        line = []

        for x in range(left, right + 1):
            if (x, y) in points:
                line.append("█")
            else:
                line.append(" ")

        output.append("".join(line))

    return "\n".join(output)


def main():
    code = read_input()
    print(part1(code))
    print(part2(code))


if __name__ == "__main__":
    main()
