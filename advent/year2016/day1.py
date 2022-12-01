# -*- coding: utf-8 -*-

def read_input():
    with open('input/2016/day1-input.txt', encoding='utf8') as file:
        directions = []

        for instruction in file.read().split(', '):
            directions.append((instruction[0], int(instruction[1:])))

    return directions


def moves(data):
    """
    >>> list(moves((('R', 5), ('R', 3), ('L', 2))))
    [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (5, -1), (5, -2), (5, -3), (6, -3), (7, -3)]
    """

    moves = ((0, 1), (1, 0), (0, -1), (-1, 0))
    direction = 0
    x, y = 0, 0

    for (turn, distance) in data:
        direction += -1 if turn == 'L' else 1
        direction %= 4
        move = moves[direction]

        for _ in range(distance):
            x += move[0]
            y += move[1]
            yield (x, y)


def part1(data):
    """
    >>> part1(read_input())
    287
    """

    (x, y) = list(moves(data))[-1]
    return abs(x) + abs(y)


def part2(data):
    """
    >>> part2(read_input())
    133
    """

    visited = set()

    for location in moves(data):

        if location in visited:
            (x, y) = location
            return abs(x) + abs(y)

        visited.add(location)

    raise ValueError('Did not visit a location twice')


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
