#!/usr/local/bin/python3

from advent.year2019.intcode import IntCode
from collections import defaultdict
from advent import bounds, md5

DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]

def read_input():
    return [int(code) for code in open('input/2019/day11-input.txt', 'r').read().split(',')]

def paint(code, painted = []):
    hull = defaultdict(int)

    for point in painted:
        hull[point] = 1

    robot =  IntCode(code)

    direction = 0
    point = (0,0)

    while True:
        input = [hull[point]]
        
        paint = robot.execute(input)

        if paint is None:
            break

        turn = robot.execute()
        hull[point] = paint

        if turn == 0:
            turn = -1

        direction = (direction + turn) % len(DIRECTIONS)
        move = DIRECTIONS[direction]
        point = (point[0] + move[0], point[1] + move[1])

    return(hull)

def part1(code):
    """
    >>> part1(read_input())
    1747
    """

    return len(paint(code))


def part2(code):
    """
    >>> md5(part2(read_input()))
    '02f9c4484ef489931028014595e96565'
    """

    hull = paint(code, [(0,0)])
    
    points = [point for point in hull.keys() if hull[point]]

    (left, top), (right, bottom) = bounds(points)
    output = []

    for y in range(top, bottom + 1):
        line = []

        for x in range(left, right + 1):
            if (x,y) in points:
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
