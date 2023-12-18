# -*- coding: utf-8 -*-

from heapq import heappop, heappush
from enum import Enum
from functools import total_ordering
from advent import taxicab_distance


@total_ordering
class Direction(Enum):
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)

    def __lt__(self, other):
        return self.value < other.value


def read_input(filename='input/2023/day17-input.txt'):
    grid = {}

    with open(filename, encoding='utf8') as file:
        for y, line in enumerate(file):
            for x, i in enumerate(line.strip()):
                grid[(x, y)] = int(i)

    return grid


def move(location, direction):
    lx, ly = location
    dx, dy = direction.value
    return lx + dx, ly + dy


def opposite(direction):
    match direction:
        case Direction.LEFT:
            return Direction.RIGHT
        case Direction.RIGHT:
            return Direction.LEFT
        case Direction.UP:
            return Direction.DOWN
        case Direction.DOWN:
            return Direction.UP
        case None:
            return None
        case _:
            raise ValueError(direction)


def shortest_route(grid, straight_limit=3, turn_limit=0):
    """
    >>> shortest_route(read_input('input/2023/day17-sample.txt'), 3, 0)
    102
    >>> shortest_route(read_input('input/2023/day17-sample.txt'), straight_limit = 10, turn_limit = 4)
    94
    """

    end = (max(x for x, _ in grid), max(y for _, y in grid))
    best = None
    queue = []
    heappush(queue, (0, 0, (0, 0), Direction.DOWN, 0))
    heappush(queue, (0, 0, (0, 0), Direction.RIGHT, 0))
    seen = {}

    while queue:
        _, heat_loss, location, direction, direction_count = heappop(queue)

        if best is not None and heat_loss >= best:
            continue

        if location == end:
            if direction_count >= turn_limit and (best is None or heat_loss < best):
                best = heat_loss
            continue

        current_step = (location, direction, direction_count)

        if current_step in seen and seen[current_step] <= heat_loss:
            continue

        seen[current_step] = heat_loss

        for next_direction in Direction:

            if next_direction == direction:
                if direction_count >= straight_limit:
                    continue

                next_direction_count = direction_count + 1
            elif next_direction == opposite(direction):
                continue
            else:
                if direction_count < turn_limit:
                    continue
                next_direction_count = 1

            next_location = move(location, next_direction)

            if next_location not in grid:
                continue

            heappush(queue, (taxicab_distance(next_location, end), heat_loss + grid[next_location],
                             next_location, next_direction, next_direction_count))

    return best


def part1(data):
    """
    # >>> part1(read_input())
    # 1246
    """

    return shortest_route(data)


def part2(data):
    """
    # >>> part2(read_input())
    # 1389
    """

    return shortest_route(data, straight_limit=10, turn_limit=4)


def main():
    print(part1(read_input()))
    print(part2(read_input()))


if __name__ == "__main__":
    main()
