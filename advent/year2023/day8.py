# -*- coding: utf-8 -*-

import re
from math import lcm

PATTERN = re.compile(r'(\w+) = \((\w+), (\w+)\)')


def read_input(filename='input/2023/day8-input.txt'):
    with open(filename, encoding='utf8') as file:
        directions = file.readline().strip()
        file.readline()
        nodes = []

        for line in file:
            result = PATTERN.match(line)
            nodes.append(result.groups((1, 2, 3)))

        return directions, nodes


def calculate_steps(directions, nodes, start=None):
    """
    >>> part1(('LLR',[('AAA', 'BBB', 'BBB'), ('BBB' ,'AAA', 'ZZZ'), ('ZZZ', 'ZZZ', 'ZZZ')]))
    6
    >>> part1(('RL', [('AAA', 'BBB', 'CCC'), ('BBB', 'DDD', 'EEE'), ('CCC', 'ZZZ', 'GGG'), ('DDD', 'DDD', 'DDD'), \\
    ...    ('EEE', 'EEE', 'EEE'), ('GGG', 'GGG', 'GGG'), ('ZZZ', 'ZZZ', 'ZZZ')]))
    2
    """

    if start is None:
        start = 'AAA'

        def not_finished(node):
            return node != 'ZZZ'
    else:
        def not_finished(node):
            return not node.endswith('Z')

    left_turns = {}
    right_turns = {}

    for node, left, right in nodes:
        left_turns[node] = left
        right_turns[node] = right

    node = start
    steps = 0

    while not_finished(node):
        if directions[steps % len(directions)] == 'L':
            node = left_turns[node]
        else:
            node = right_turns[node]
        steps += 1

    return steps


def part1(data):
    """
    >>> part1(read_input())
    19199
    """

    directions, nodes = data
    return calculate_steps(directions, nodes)


def part2(data):
    """
    >>> part2(read_input())
    13663968099527
    """

    directions, nodes = data
    ghosts = (node[0] for node in nodes if node[0].endswith('A'))
    steps = (calculate_steps(directions, nodes, ghost) for ghost in ghosts)
    return lcm(*steps)


def main():
    print(part1(read_input()))
    print(part2(read_input()))


if __name__ == "__main__":
    main()
