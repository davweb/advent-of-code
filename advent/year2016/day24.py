# -*- coding: utf-8 -*-

from heapq import heappop, heappush
from itertools import product, combinations
import numpy
from advent import taxicab_distance

ROCK = -2
SPACE = -1


def read_input(filename='input/2016/day24-input.txt'):
    with open(filename, encoding='utf8') as file:
        maze_string = [line.strip() for line in file]

    width = len(maze_string[0])
    height = len(maze_string)

    maze = numpy.zeros((width, height), numpy.int16)

    for x, y in product(range(width), range(height)):
        match maze_string[y][x]:
            case '.':
                value = SPACE
            case '#':
                value = ROCK
            case num:
                value = int(num)

        maze[x, y] = value

    return maze


def neighbours(location):
    x, y = location
    return ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1))


def exits(location, maze):
    """
    >>> maze = read_input('input/2016/day24-input.txt')
    >>> len(exits((1, 9), maze))
    3
    >>> len(exits((1, 1), maze))
    1
    >>> len(exits((2, 41), maze))
    2
    """

    return [neighbour for neighbour in neighbours(location) if maze[neighbour] != ROCK]


def routes(location, maze):
    """
    >>> maze = read_input('input/2016/day24-input.txt')
    >>> routes((1, 1), maze)
    [((3, 1), 2)]
    >>> routes((3, 1), maze)
    [((1, 7), 8)]
    >>> routes((1, 7), maze)
    [((3, 1), 8), ((1, 9), 2)]
    """

    routes_found = []

    for neighbour in exits(location, maze):
        previous = location
        length = 0

        while True:
            length += 1
            moves = exits(neighbour, maze)

            if maze[neighbour] != SPACE or len(moves) > 2:
                routes_found.append((neighbour, length))
                break

            if len(moves) == 1:
                break

            previous, neighbour = neighbour, moves[1] if moves[0] == previous else moves[0]

    return routes_found


def find(needle, maze):
    return numpy.unravel_index(numpy.flatnonzero(maze == needle)[0], maze.shape)


def shortest_route(start, end, maze):
    route_cache = {}
    best = None
    queue = []
    heappush(queue, (0, 0, (start,)))
    seen = {}

    while queue:
        _, steps, current_route = heappop(queue)

        if best is not None and steps >= best:
            continue

        location = current_route[-1]

        if location in seen and seen[location] <= steps:
            continue

        seen[location] = steps

        if location == end:
            if best is None or steps < best:
                best = steps
            continue

        next_steps = route_cache.get(location, None)

        if next_steps is None:
            next_steps = routes(location, maze)
            route_cache[location] = next_steps

        for neighbour, length in next_steps:
            if neighbour not in current_route:
                next_route = current_route + (neighbour,)
                priority = taxicab_distance(neighbour, end)
                heappush(queue, (priority, steps + length, next_route))

    return best


def remove_element(needle, haystack):
    return tuple(item for item in haystack if item != needle)


def all_destinations(maze):
    return tuple(numpy.extract(maze >= 0, maze))


def calculate_distances(maze):
    destinations = all_destinations(maze)
    distances = {}

    for start, end in combinations(destinations, 2):
        start_location = find(start, maze)
        end_location = find(end, maze)
        distance = shortest_route(start_location, end_location, maze)
        distances[(start, end)] = distance
        distances[(end, start)] = distance

    return distances


def calculate_path(maze, return_home=False):
    distances = calculate_distances(maze)
    destinations = all_destinations(maze)

    best = None
    queue = []
    heappush(queue, (0, 0, 0, remove_element(0, destinations)))

    while queue:
        _, steps, current, destinations_to_visit = heappop(queue)

        if best is not None and steps >= best:
            continue

        if len(destinations_to_visit) == 0:
            if return_home:
                steps += distances[(current, 0)]
            if best is None or steps < best:
                best = steps
            continue

        for next_entry in destinations_to_visit:
            distance = distances[(current, next_entry)]
            priority = len(destinations_to_visit)
            heappush(queue, (priority, steps + distance, next_entry, remove_element(next_entry, destinations_to_visit)))

    return best


def part1(maze):
    """
    >>> part1(read_input('input/2016/day24-test.txt'))
    14
    >>> part1(read_input())
    456
    """

    return calculate_path(maze)


def part2(maze):
    """
    >>> part2(read_input())
    704
    """

    return calculate_path(maze, return_home=True)


def main():
    print(part1(read_input('input/2016/day24-input.txt')))
    print(part2(read_input()))


if __name__ == "__main__":
    main()
