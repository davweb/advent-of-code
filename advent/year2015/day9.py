# -*- coding: utf-8 -*-

import re
from collections import defaultdict


PATTERN = re.compile(r"(\w+) to (\w+) = (\d+)")


def read_input():
    file = open("input/2015/day9-input.txt", "r")
    data = []

    for line in file:
        result = PATTERN.match(line)
        from_name, to_name, distance = result.group(1, 2, 3)
        data.append((from_name, to_name, int(distance)))

    return data


def determine_distance(data, operator):
    """
    >>> determine_distance([
    ...     ('London', 'Dublin', 464),
    ...     ('London', 'Belfast', 518),
    ...     ('Dublin', 'Belfast', 141)
    ... ], min)
    605
    """

    places = set()
    distances = defaultdict(dict)

    for (from_name, to_name, distance) in data:
        places.add(from_name)
        places.add(to_name)
        distances[from_name][to_name] = distance
        distances[to_name][from_name] = distance

    def calculate_distance(current_distance, location, remaining_places):
        if len(remaining_places) == 0:
            return current_distance

        routes = []

        for next_place in remaining_places:
            try:
                if location is None:
                    next_hop = 0
                else:
                    next_hop = distances[location][next_place]

                next_distance = calculate_distance(
                    current_distance + next_hop,
                    next_place,
                    remaining_places.difference([next_place])
                )

                if next_distance is not None:
                    routes.append(next_distance)

            except KeyError:
                # We end up here if there's no route from location to next_place
                pass

        if len(routes) == 0:
            return None
        else:
            return operator(routes)

    return calculate_distance(0, None, places)


def part1(data):
    """
    >>> part1(read_input())
    117
    """

    return determine_distance(data, min)


def part2(data):
    """
    >>> part2(read_input())
    909
    """

    return determine_distance(data, max)


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
