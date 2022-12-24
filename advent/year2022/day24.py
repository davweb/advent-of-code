# -*- coding: utf-8 -*-

from heapq import heappush, heappop
from advent import taxicab_distance


def read_input(filename='input/2022/day24-input.txt'):
    with open(filename, encoding='utf8') as file:
        top = file.readline().strip()
        width = len(top)
        entrance_x = top.index('.')
        entrance_y = 0
        row = 0
        blizzards = []

        while True:
            line = file.readline().strip()
            row += 1

            if '<' not in line:
                break

            for index, char in enumerate(line):
                if char in ('^', 'v', '>', '<'):
                    blizzards.append(((index, row), char))

        exit_x = line.index('.')
        exit_y = row
        height = row + 1

        return ((width, height), (entrance_x, entrance_y), (exit_x, exit_y), blizzards)


def blow_winds(size, blizzards):
    width, height = size

    new_blizzards = []

    for (x, y), direction in blizzards:
        match direction:
            case '<':
                x = x - 1
                if x == 0:
                    x = width - 2
            case '>':
                x = x + 1
                if x == width - 1:
                    x = 1
            case '^':
                y = y - 1
                if y == 0:
                    y = height - 2
            case 'v':
                y = y + 1
                if y == height - 1:
                    y = 1

        new_blizzards.append(((x, y), direction))

    return new_blizzards


def empty_spaces(size, entrance, escape, blizzards):
    width, height = size
    filled = set(location for location, _ in blizzards)
    unfilled = set([entrance, escape])

    for x in range(1, width - 1):
        for y in range(1, height - 1):
            if (x, y) not in filled:
                unfilled.add((x, y))

    return unfilled


def find_route(start_turn, start, finish, unfilled):
    queue = []
    heappush(queue, (taxicab_distance(start, finish), (start, )))
    best = len(unfilled) - 1

    seen = set()

    while queue:
        _, route = heappop(queue)
        turn = start_turn + len(route)

        if turn >= best:
            continue

        current = route[-1]

        if current == finish:
            best = min(best, turn)
            continue

        key = (turn, current)

        if key in seen:
            continue

        seen.add(key)

        x, y = current

        for option in ((x, y), (x - 1, y), (x + 1, y), (x, y + 1), (x, y - 1)):
            if option in unfilled[turn]:
                distance = taxicab_distance(option, finish)
                heappush(queue, (distance, route + (option,)))

    return best - 1


def unfilled_spaces(size, entrance, escape, blizzards, turns):
    unfilled = []

    for _ in range(turns):
        unfilled.append(empty_spaces(size, entrance, escape, blizzards))
        blizzards = blow_winds(size, blizzards)

    return unfilled


def part1(data):
    """
    >>> part1(read_input())
    290
    """

    size, entrance, escape, blizzards = data
    unfilled = unfilled_spaces(size, entrance, escape, blizzards, 1000)
    return find_route(0, entrance, escape, unfilled)


def part2(data):
    """
    >>> part2(read_input())
    842
    """
    size, entrance, escape, blizzards = data
    unfilled = unfilled_spaces(size, entrance, escape, blizzards, 1000)

    there = find_route(0, entrance, escape, unfilled)
    back = find_route(there, escape, entrance, unfilled)
    return find_route(back, entrance, escape, unfilled)


def main():
    print(part1(read_input()))
    print(part2(read_input()))


if __name__ == "__main__":
    main()
