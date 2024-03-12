# -*- coding: utf-8 -*-


from math import prod
from operator import lt, gt
import re
from copy import deepcopy

WORKFLOW_PATTERN = re.compile(r'([a-z]+)\{(.*)\}')
PART_PATTERN = re.compile(r'\{x=(\d+),m=(\d+),a=(\d+),s=(\d+)\}')


def read_input(filename='input/2023/day19-input.txt'):
    with open(filename, encoding='utf8') as file:
        workflows = {}
        parts = []

        for line in file:
            match = WORKFLOW_PATTERN.match(line)

            if match:
                workflows[match.group(1)] = match.group(2).split(',')
                continue

            match = PART_PATTERN.match(line)

            if match:
                parts.append([int(i) for i in match.group(1, 2, 3, 4)])
                continue

        return workflows, parts


def part1(data):
    """
    >>> part1(read_input())
    406934
    """

    workflows, parts = data
    total = 0

    for part in parts:
        workflow = list(workflows['in'])

        while True:
            step = workflow.pop(0)

            if step == 'A':
                total += sum(part)
                break

            if step == 'R':
                break

            if ':' not in step:
                workflow = list(workflows[step])
                continue

            instruction, destination = step.split(':')

            variable = part['xmas'.index(instruction[0])]
            operator = lt if instruction[1] == '<' else gt
            value = int(instruction[2:])

            if operator(variable, value):
                workflow = [destination]

    return total


def part2(data):
    """
    >>> part2(read_input())
    131192538505367
    """

    workflows, _ = data

    total = 0
    queue = [(workflows['in'], [[1, 4000] for _ in range(4)])]

    while queue:
        workflow, ranges = queue.pop()
        step = workflow.pop(0)

        if step == 'A':
            total += prod(high - low + 1 for low, high in ranges)
            continue

        if step == 'R':
            continue

        if ':' not in step:
            queue.append((workflows[step], ranges))
            continue

        instruction, destination = step.split(':')

        index = 'xmas'.index(instruction[0])
        operator = instruction[1]
        value = int(instruction[2:])

        if operator == '<':
            if ranges[index][0] < value:
                new_ranges = deepcopy(ranges)
                new_ranges[index][1] = min(value - 1, new_ranges[index][1])
                queue.append(([destination], new_ranges))

            ranges[index][0] = value
        else:
            if ranges[index][1] > value:
                new_ranges = deepcopy(ranges)
                new_ranges[index][0] = max(value + 1, new_ranges[index][0])
                queue.append(([destination], new_ranges))

            ranges[index][1] = value

        if ranges[index][0] <= ranges[index][1]:
            queue.append((workflow, ranges))

    return total


def main():
    print(part1(read_input()))
    print(part2(read_input()))


if __name__ == "__main__":
    main()
