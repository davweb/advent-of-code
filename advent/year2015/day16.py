# -*- coding: utf-8 -*-

import re


PATTERN = re.compile(r"Sue (\d+): (\w+): (\d+), (\w+): (\d+), (\w+): (\d+)")

TAPE = {
    'children': 3,
    'cats': 7,
    'samoyeds': 2,
    'pomeranians': 3,
    'akitas': 0,
    'vizslas': 0,
    'goldfish': 5,
    'trees': 3,
    'cars': 2,
    'perfumes': 1
}


def read_input():
    results = []

    with open('input/2015/day16-input.txt', encoding='utf8') as file:
        for line in file:
            match = PATTERN.match(line)
            sue, name_one, count_one, name_two, count_two, name_three, count_three = match.group(1, 2, 3, 4, 5, 6, 7)
            results.append((
                int(sue),
                {
                    name_one: int(count_one),
                    name_two: int(count_two),
                    name_three: int(count_three)
                }
            ))

    return results


def part1(data):
    """
    >>> part1(read_input())
    213
    """

    for sue, measurements in data:
        if all(TAPE[key] == value for key, value in measurements.items()):
            return sue

    raise ValueError()


def part2(data):
    """
    >>> part2(read_input())
    323
    """

    for sue, measurements in data:
        value = measurements.pop('cats', None)

        if value is not None and value <= TAPE['cats']:
            continue

        value = measurements.pop('trees', None)

        if value is not None and value <= TAPE['trees']:
            continue

        value = measurements.pop('pomeranians', None)

        if value is not None and value >= TAPE['pomeranians']:
            continue

        value = measurements.pop('goldfish', None)

        if value is not None and value >= TAPE['goldfish']:
            continue

        if all(TAPE[key] == value for key, value in measurements.items()):
            return sue

    raise ValueError()


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
