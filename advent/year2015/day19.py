# -*- coding: utf-8 -*-

import re
from collections import deque
from random import shuffle

PATTERN = re.compile(r'(\w+) => (\w+)')


def read_input():

    with open('input/2015/day19-input.txt', encoding='utf-8') as file:
        substitutions = []

        while True:
            line = file.readline()
            match = PATTERN.match(line)

            if match:
                substitutions.append(match.group(1, 2))
            else:
                break

        formula = file.readline()
        return (substitutions, formula)


def find_all(needle, haystack):
    index = 0

    while True:
        index = haystack.find(needle, index)

        if index == -1:
            return

        yield index
        index += len(needle)


def part1(data):
    """
    >>> part1(read_input())
    509
    """

    molecules = set()

    substitutions, formula = data

    for before, after in substitutions:
        for index in find_all(before, formula):
            new_molecule = formula[:index] + after + formula[index + len(before):]
            molecules.add(new_molecule)

    return len(molecules)


def reverse_engineer(substitutions, start_molecule):
    """
    >>> reverse_engineer([('e', 'H'), ('e', 'O'), ('H', 'HO'), ('H', 'OH'), ('O', 'HH')], 'HOH')
    3
    >>> reverse_engineer([('e', 'H'), ('e', 'O'), ('H', 'HO'), ('H', 'OH'), ('O', 'HH')], 'HOHOHO')
    6
    """

    seen = {}
    best = None
    queue = deque()
    queue.append((start_molecule, 0))
    shortest = len(start_molecule)

    while queue:
        molecule, steps = queue.pop()

        if best is not None and steps > best:
            continue

        previous_steps = seen.get(molecule, None)
        if previous_steps is not None and previous_steps <= steps:
            continue

        seen[molecule] = steps

        if shortest is None or len(molecule) < shortest:
            shortest = len(molecule)

        if molecule == 'e':
            if best is None or steps < best:
                best = steps
                # print("best so far", best)

            continue

        shuffle(substitutions)

        for before, after in substitutions:
            hits = list(find_all(after, molecule))
            hits.reverse()

            for index in hits:
                new_molecule = molecule[:index] + before + molecule[index + len(after):]

                if 'e' in molecule and len(molecule) > 1:
                    continue

                queue.append((new_molecule, steps + 1))

    return best


def part2(data):
    """
    # >>> part2(read_input())
    # 195
    """

    substitutions, formula = data
    return reverse_engineer(substitutions, formula)


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
