#!/usr/local/bin/python3

from collections import defaultdict
import re

PATTERN = re.compile(r"Step (\w) must be finished before step (\w) can begin.")

def read_input():
    file = open("input/2018/day7-input.txt", "r")
    
    pre_reqs = defaultdict(set)

    for line in file.readlines():
        match = PATTERN.match(line)
        (first, second) = (match.group(1), match.group(2))

        pre_reqs[second].add(first)
        # Make sure all steps have an entry in the map even if they have no dependencies
        pre_reqs[first]

    return pre_reqs

def part1(pre_reqs):
    """
    >>> part1(read_input())
    'FHICMRTXYDBOAJNPWQGVZUEKLS'
    """

    pre_reqs = pre_reqs.copy()
    order = []

    while pre_reqs:
        next = min(step for step in pre_reqs.keys() if len(pre_reqs[step] - set(order)) == 0)
        order.append(next)
        del pre_reqs[next]

    return "".join(order)

def time_to_complete(step):
    """
    >>> time_to_complete("A")
    61
    >>> time_to_complete("Z")
    86
    """

    return ord(step) - 4

def part2(pre_reqs):
    """
    >>> part2(read_input())
    946
    """

    remaining = dict((step, time_to_complete(step)) for step in pre_reqs.keys())
    minutes = 0
    done = set()

    while sum(remaining.values()):
        minutes += 1
        available = sorted(step for step in remaining.keys() if len(pre_reqs[step] - done) == 0)
        
        for task in available[:5]:
            todo = remaining[task] - 1

            if todo == 0:
                del remaining[task]
                done.add(task)
            else:
                remaining[task] = todo

    return minutes

def main():
    data = read_input()
    print(part1(data))
    print(part2(data))

if __name__ == "__main__":
    main()
    