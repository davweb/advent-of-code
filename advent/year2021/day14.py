# -*- coding: utf-8 -*-

import re
from collections import Counter
from functools import cache

PATTERN = re.compile(r'([A-Z]{2}) -> ([A-Z])')


def read_input():

    with open('input/2021/day14-input.txt') as file:
        formula = file.readline().strip()

        # # blank line
        file.readline()

        substitutions = {}

        for line in file.readlines():
            match = PATTERN.match(line)

            if match:
                substitutions[match.group(1)] = match.group(2)
            else:
                raise ValueError(line)

    return (substitutions, formula)


def process(formula, substitutions):
    new_formula = ''
    previous = None

    for i in formula:
        if previous is not None:
            pair = previous + i

            if pair in substitutions:
                new_formula += substitutions[pair]

        new_formula += i
        previous = i

    return new_formula


def split(formula):
    """
    >>> split('CNNCB')
    ('CNN', 'NCB')
    >>> split('NNCB')
    ('NNC', 'CB')
    >>> split('NCB')
    ('NC', 'CB')
    """

    left = formula[:len(formula) // 2 + 1]
    right = formula[len(left) - 1:]

    return left, right


def smart_process(formula, substitutions, rounds):
    """
    >>> substitutions = dict((
    ...     ('CH', 'B'), ('HH', 'N'), ('CB', 'H'), ('NH', 'C'), ('HB', 'C'), ('HC', 'B'), ('HN', 'C'), ('NN', 'C'),
    ...     ('BH', 'H'), ('NC', 'B'), ('NB', 'B'), ('BN', 'B'), ('BB', 'N'), ('BC', 'B'), ('CC', 'N'), ('CN', 'C')
    ... ))
    >>> sorted(smart_process('NNCB', substitutions, 0).items())
    [('B', 1), ('C', 1), ('N', 2)]
    >>> sorted(smart_process('NNCB', substitutions, 1).items())
    [('B', 2), ('C', 2), ('H', 1), ('N', 2)]
    >>> sorted(smart_process('NNCB', substitutions, 2).items())
    [('B', 6), ('C', 4), ('H', 1), ('N', 2)]
    """

    @cache
    def recursive_process(formula, rounds):
        if rounds == 0:
            return Counter(formula)

        if len(formula) > 2:
            left, right = split(formula)
        else:
            new_element = substitutions[formula]
            left = formula[0] + new_element
            right = new_element + formula[1]
            rounds -= 1

        count = recursive_process(left, rounds) + recursive_process(right, rounds)
        count.subtract(right[0])
        return count

    return recursive_process(formula, rounds)


def most_minus_least(counts):
    least = None
    most = 0

    for count in counts.values():
        least = count if least is None else min(count, least)
        most = max(count, most)

    return most - least


def part1(data):
    """
    >>> part1(read_input())
    2797
    """

    substitutions, formula = data

    for _ in range(10):
        formula = process(formula, substitutions)

    counter = Counter(formula)
    return most_minus_least(counter)


def part2(data):
    """
    # >>> part2(read_input())
    # 2926813379532
    """

    substitutions, formula = data
    counter = smart_process(formula, substitutions, 40)
    return most_minus_least(counter)


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
