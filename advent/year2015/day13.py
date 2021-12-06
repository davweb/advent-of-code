# -*- coding: utf-8 -*-

import re
from itertools import permutations

PATTERN = re.compile(r"(\w+) would (lose|gain) (\d+) happiness units by sitting next to (\w+).")


def read_input():
    results = []

    with open('input/2015/day13-input.txt') as file:
        for line in file.readlines():
            match = PATTERN.match(line)
            name, difference, score, other = match.group(1, 2, 3, 4)
            score = int(score)

            if difference == 'lose':
                score = -score

            results.append((name, other, score))

    return results


def looped_permutations(iterable):
    # Since table is a loop we don't need all permutations
    # Fix first diner and rotate all the others

    source = list(iterable)

    for permutation in permutations(source[1:]):
        yield [source[0]] + list(permutation)


def adjacent(one, two, items):
    """
    >>> adjacent(1, 2, [1, 2, 3, 4])
    True
    >>> adjacent(2, 1, [1, 2, 3, 4])
    True
    >>> adjacent(1, 3, [1, 2, 3, 4])
    False
    >>> adjacent(4, 2, [1, 2, 3, 4])
    False
    >>> adjacent(1, 4, [1, 2, 3, 4])
    True
    >>> adjacent(4, 1, [1, 2, 3, 4])
    True
    """

    one_index = items.index(one)
    two_index = items.index(two)
    end_index = len(items) - 1

    if one_index == two_index - 1:
        return True

    if one_index == two_index + 1:
        return True

    if one_index == 0 and two_index == end_index:
        return True

    if one_index == end_index and two_index == 0:
        return True

    return False


def calculate_happiness(rules, add_me):
    names = set()

    for name, other, _ in rules:
        names.add(name)
        names.add(other)

    if add_me:
        names.add("Me")

    # Assume change is > 0
    max_happiness = 0

    for table in looped_permutations(names):
        happiness = sum(score for name, other, score in rules if adjacent(name, other, table))
        max_happiness = max(happiness, max_happiness)

    return max_happiness


def part1(data):
    """
    >>> part1(read_input())
    664
    """

    return calculate_happiness(data, False)


def part2(data):
    """
    >>> part2(read_input())
    640
    """

    return calculate_happiness(data, True)


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
