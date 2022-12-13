# -*- coding: utf-8 -*-

from collections import defaultdict


def read_input():
    with open('input/2021/day12-input.txt', encoding='utf8') as file:
        return [line.strip().split('-') for line in file.readlines()]


def make_routes(connections):
    routes = defaultdict(set)

    for from_cave, to_cave in connections:
        routes[from_cave].add(to_cave)
        routes[to_cave].add(from_cave)

    return routes


def is_small_cave(cave):
    return cave.lower() == cave


def cave_not_in_path(small_cave, path):
    return small_cave not in path


def allow_one_cave_twice(small_cave, path):
    if small_cave not in path:
        return True

    cave_count = defaultdict(int)

    for cave in path:
        if is_small_cave(cave):
            cave_count[cave] += 1

            if cave_count[cave] > 1:
                return False

    return True


def find_paths(routes, can_be_added, cave=None, path=None, paths=None):
    """
    >>> connections = [
    ...    ['start', 'A'],
    ...    ['start', 'b'],
    ...    ['A', 'c'],
    ...    ['A', 'b'],
    ...    ['b', 'd'],
    ...    ['A', 'end'],
    ...    ['b', 'end'],
    ... ]
    >>> routes = make_routes(connections)
    >>> len(find_paths(routes, cave_not_in_path))
    10
    >>> len(find_paths(routes, allow_one_cave_twice))
    36
    """

    if cave is None:
        cave = 'start'

    if path is None:
        path = []

    if paths is None:
        paths = []

    if cave == 'start' and cave in path:
        return paths

    if is_small_cave(cave) and not can_be_added(cave, path):
        return paths

    path = path + [cave]

    if cave == 'end':
        paths.append(path)
        return paths

    adjacent_caves = routes[cave]

    for next_cave in adjacent_caves:
        find_paths(routes, can_be_added, next_cave, path, paths)

    return paths


def part1(data):
    """
    >>> part1(read_input())
    5457
    """

    routes = make_routes(data)
    return len(find_paths(routes, cave_not_in_path))


def part2(data):
    """
    >>> part2(read_input())
    128506
    """

    routes = make_routes(data)
    return len(find_paths(routes, allow_one_cave_twice))


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
