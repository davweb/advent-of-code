# -*- coding: utf-8 -*-

from array import array
from collections import deque


def read_input():
    rows = []

    with open('input/2021/day15-input.txt', encoding='utf8') as file:
        for line in file.readlines():
            rows.append([int(c) for c in line.strip()])

    return rows


def search(board):
    max_y = len(board)
    max_x = len(board[0])

    bottom = max_y - 1
    right = max_x - 1

    best = []

    board = array('i', (cell for row in board for cell in row))
    best = array('i', (-1 for _ in range(max_x * max_y)))

    best[0] = 0
    moves = deque((((0, 1), 0), ((1, 0), 0)))

    # Do a simple route to get an initial upper bound for the risk
    best_route = sum(board[x] for x in range(max_x)) + sum(board[right + y * max_x] for y in range(1, max_y))

    while moves:
        location, total_risk = moves.pop()
        x, y = location
        index = y * max_x + x

        total_risk += board[index]

        if total_risk > best_route:
            continue

        previous_best = best[index]

        if previous_best != -1 and previous_best <= total_risk:
            continue

        best[index] = total_risk

        if x == right and y == bottom and total_risk < best_route:
            best_route = total_risk

        # Prioritize heading for the corner
        if x < y:

            if x < right:
                moves.append(((x + 1, y), total_risk))

            if y < right:
                moves.appendleft(((x, y + 1), total_risk))

        else:

            if y < right:
                moves.append(((x, y + 1), total_risk))

            if x < right:
                moves.appendleft(((x + 1, y), total_risk))

        # Going "backwards" is less likely to get to the exit so put those moves at the head of the list
        # so they get tried later
        if x > 0:
            moves.appendleft(((x - 1, y), total_risk))

        if y > 0:
            moves.appendleft(((x, y - 1), total_risk))

    return best[bottom * max_x + right]


def part1(data):
    """
    >>> part1(read_input())
    687
    """

    return search(data)


def part2(data):
    """
    # Commenting out as this takes ~20 minutes to run
    # >>> part2(read_input())
    # 2957
    """

    board = []

    for my in range(5):
        for old_row in data:
            new_row = []

            for mx in range(5):
                for value in old_row:
                    new_value = value + mx + my

                    while new_value >= 10:
                        new_value -= 9

                    new_row.append(new_value)

            board.append(new_row)

    return search(board)


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
