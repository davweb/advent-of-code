# -*- coding: utf-8 -*-

import re
from collections import defaultdict

PATTERN = re.compile(r"(\d+) <-> ((\d+, )*\d+)")

def read_input():
    file = open("input/2020/day13-input.txt", "r")
    
    depart = int(file.readline())
    buses = [int(bus) if bus != 'x' else None for bus in file.readline().split(',')]
    return (depart, buses)


def cadence(a, b, required_gap):
    """
    For the pair of numbers determine when they first repeat with the required gap
    and the period that it will repeat.

    >>> cadence(67, 7, 1)
    (335, 336, 469)
    >>> cadence(67, 7, 2)
    (201, 203, 469)
    >>> cadence(1789, 37, 1)
    (30413, 30414, 66193)
    >>> cadence(17, 13, 21)
    Traceback (most recent call last):
    ...
    ValueError: Did not find matching gap
    """

    for i in range(b, a * b, b):
        if i % a == required_gap:
            return (i - required_gap, i, a * b)

    raise ValueError("Did not find matching gap")


def solve(target, gap):
    """
    >>> solve((67, 7, 59, 61), (1, 1, 1))
    754018
    >>> solve((1789, 37, 47, 1889), (1, 1, 1))
    1202161486
    >>> solve((67, 7, 59, 61), (2, 1, 1)) 
    779210
    """


    progress_delta = 100000000000000 // 10000
    progress = progress_delta


    count = len(target) - 1
    first, second, delta = [None] * count, [None] * count, [None] * count

    # Calculate the repeating pairs for each number and its successor    
    for i in range(0, count):
        first[i], second[i], delta[i] = cadence(target[i], target[i + 1], gap[i])   

    # Keep incrementing the repeating pairs until we finally have match 
    while any(first[i + 1] - second[i] != 0 for i in range(0, count - 1)):
        for i in range(0, count - 1):
            diff = first[i + 1] - second[i] 

            if diff > 0:
                remainder = diff % delta[i]

                if remainder == 0:
                    step = diff
                else:
                    step = (diff - remainder) + delta[i]
                
                first[i] += step
                second[i] += step

        for i in range(1, count):
            diff = second[i - 1] - first[i]

            if diff > 0:
                remainder = diff % delta[i]

                if remainder == 0:
                    step = diff
                else:
                    step = (diff - remainder) + delta[i]
                
                first[i] += step
                second[i] += step
        
        if first[0] > progress:
            print(first[0])
            progress += progress_delta



    return first[0]


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
