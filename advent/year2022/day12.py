# -*- coding: utf-8 -*-

from collections import deque

DIRECTIONS = ((1, 0), (0, -1), (0, 1), (-1, 0))


def height(char):
    if char == 'S':
        return 1
    if char == 'E':
        return 26
    if 'a' <= char <= 'z':
        return ord(char) - ord('a') + 1
    raise ValueError(char)


def parse_map(text):
    output = []
    start = None
    end = None
    for x, line in enumerate(text.strip().split('\n')):
        line = line.strip()
        output.append([height(c) for c in line])

        for y, char in enumerate(line):
            if char == 'S':
                start = (x, y)
            if char == 'E':
                end = (x, y)

    return (output, start, end)


def read_input():
    with open('input/2022/day12-input.txt', encoding='utf8') as file:
        return parse_map(file.read())


def steps_uphill(grid, location):
    x, y = location
    max_height = grid[x][y] + 1

    for dx, dy in DIRECTIONS:
        nx = x + dx
        ny = y + dy

        if nx < 0 or nx >= len(grid) or ny < 0 or ny >= len(grid[0]):
            continue

        if grid[nx][ny] > max_height:
            continue

        yield (nx, ny)


def steps_downhill(grid, location):
    x, y = location
    min_height = grid[x][y] - 1

    for dx, dy in DIRECTIONS:
        nx = x + dx
        ny = y + dy

        if nx < 0 or nx >= len(grid) or ny < 0 or ny >= len(grid[0]):
            continue

        if grid[nx][ny] < min_height:
            continue

        yield (nx, ny)


def find_route(grid, start, next_locations, at_end):
    shortest = None
    history = {}
    queue = deque(((start, 0),))

    while queue:
        location, distance = queue.popleft()

        if location in history and history[location] <= distance:
            continue

        history[location] = distance

        if at_end(location):
            if shortest is None or shortest > distance:
                shortest = distance
            continue

        for next_location in next_locations(grid, location):
            queue.append((next_location, distance + 1))

    return shortest


def find_route_uphill(grid, start, end):
    """
    >>> grid, start, end = parse_map('Sabqponm\\nabcryxxl\\naccszExk\\nacctuvwj\\nabdefghi')
    >>> find_route_uphill(grid, start, end)
    31
    """

    return find_route(grid, start, steps_uphill, lambda l: l == end)


def find_route_downhill(grid, end):
    """
    >>> grid, _, end = parse_map('Sabqponm\\nabcryxxl\\naccszExk\\nacctuvwj\\nabdefghi')
    >>> find_route_downhill(grid, end)
    29
    """

    return find_route(grid, end, steps_downhill, lambda l: grid[l[0]][l[1]] == 1)


def part1(data):
    """
    >>> part1(read_input())
    504
    """

    return find_route_uphill(*data)


def part2(data):
    """
    >>> part2(read_input())
    500
    """

    grid, _, end = data
    return find_route_downhill(grid, end)


def main():
    print(part1(read_input()))
    print(part2(read_input()))


if __name__ == "__main__":
    main()
