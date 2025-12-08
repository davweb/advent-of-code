# -*- coding: utf-8 -*-

from itertools import combinations
from math import prod


def read_input(filename='input/2025/day8-input.txt'):
    with open(filename, encoding='utf8') as file:
        return [tuple(int(i) for i in line.split(',')) for line in file.readlines()]


def distance(pair):
    a, b = pair
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2


def part1(data):
    """
    >>> part1(read_input())
    52668
    """

    connections = sorted(combinations(data, 2), key=distance)
    circuits = [{c} for c in data]

    for a, b in connections[:1000]:
        found = []

        for circuit in circuits:
            if a in circuit or b in circuit:
                found.append(circuit)

                if len(found) > 1:
                    found[0].update(found[1])
                    circuits.remove(found[1])
                    break

    circuits.sort(key=len, reverse=True)
    return prod([len(c) for c in circuits][:3])


def part2(data):
    """
    >>> part2(read_input())
    01474050600
    """

    connections = sorted(combinations(data, 2), key=distance)
    circuits = [{c} for c in data]

    for a, b in connections:
        found = []

        for circuit in circuits:
            if a in circuit or b in circuit:
                found.append(circuit)

                if len(found) > 1:
                    found[0].update(found[1])
                    circuits.remove(found[1])

                    if len(circuits) == 1:
                        return a[0] * b[0]

                    break

    raise ValueError()


def main():
    print(part1(read_input()))
    print(part2(read_input()))


if __name__ == "__main__":
    main()
