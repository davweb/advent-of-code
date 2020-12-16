# -*- coding: utf-8 -*-

import re
from collections import defaultdict

PATTERN = re.compile(r"(\d+) <-> ((\d+, )*\d+)")

def read_input():
    file = open("input/2020/day13-input.txt", "r")
    
    depart = int(file.readline())
    buses = [int(bus) if bus != 'x' else None for bus in file.readline().split(',')]
    return (depart, buses)


def cadence(a, b, required_gap, start):
    """
    For the pair of numbers determine when they first repeat with the required gap
    and the period that it will repeat, starting at the given value

    >>> cadence(67, 7, 1, 0)
    (335, 469)
    >>> cadence(67, 7, 2, 0)
    (201, 469)
    >>> cadence(1789, 37, 1, 0)
    (30413, 66193)
    >>> cadence(17, 13, 21, 0)
    (187, 221)
    """

    value = start
    first = None

    while True:
        if (value + required_gap) % b == 0:
            if first is None:
                first = value
            else:
                return (first, value - first)
        value += a


def solve(targets, gaps):
    """
    >>> solve((2, 5, 7, 97), (1, 1, 1))
    3974
    >>> solve((67, 7, 59, 61), (1, 1, 1))
    754018
    >>> solve((1789, 37, 47, 1889), (1, 1, 1))
    1202161486
    >>> solve((67, 7, 59, 61), (2, 1, 1)) 
    779210
    """

    targets = list(targets)
    gaps = list(gaps)

    # We can solve by solving for a pair of numbers and then matching that solution to the next number
    start = 0
    total_gap = 0
    loop = targets.pop(0)

    while len(targets) > 0:
        total_gap += gaps.pop(0)
        (start, loop) = cadence(loop, targets.pop(0), total_gap, start)

    return start


def part1(data):
    """
    >>> part1((939, [7, 13, 59, 31,19]))
    295
    >>> part1(read_input())
    4938
    """

    (depart, buses) = data
    best_bus = None
    shortest_wait = None

    for bus in buses:
        if bus is None:
            continue

        wait = bus - depart % bus

        if shortest_wait is None or wait < shortest_wait:
            shortest_wait = wait
            best_bus = bus

    return shortest_wait * best_bus


def part2(data):
    """
    >>> part2((0, [17, None, 13, 19]))
    3417
    >>> part2(read_input())
    230903629977901
    """
 
    buses = data[1]

    targets = [buses[0]]
    gaps = []
    gap = 1

    for bus in buses[1:]:
        if bus is None:
            gap += 1
        else:
            targets.append(bus)
            gaps.append(gap)
            gap = 1   

    return solve(targets, gaps)


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
