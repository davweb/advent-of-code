# -*- coding: utf-8 -*-

import re
from collections import defaultdict
from advent.year2018.opcodes import addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr

INSTRUCTION_PATTERN = re.compile(
    r"Before: \[(\d+), (\d+), (\d+), (\d+)\]\n"
    r"(\d+) (\d+) (\d+) (\d+)\n"
    r"After:  \[(\d+), (\d+), (\d+), (\d+)\]")


def read_input():
    file = open('input/2018/day16-input.txt', 'r')
    text = file.read()
    
    (samples, listing) = text.split("\n\n\n\n")

    instructions = []

    for groups in INSTRUCTION_PATTERN.findall(samples):
        values = [int(group) for group in groups]

        before_registers = values[0:4]
        instruction = values[4:8]
        after_registers = values[8:]

        instructions.append((before_registers, instruction, after_registers))

    code = []

    for line in listing.strip().split("\n"):
        instruction = [int(i) for i in line.strip().split(" ")]
        code.append(instruction)

    return (instructions, code)


def op_matches(before, after, a, b, c):
    """
    >>> len(op_matches([3, 2, 1, 1], [3, 2, 2, 1], 2, 1, 2))
    3
    """
    
    ops = [addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr]
    matches = []

    for op in ops:
        copy = list(before)
        op(copy, a, b, c)

        if copy == after:
            matches.append(op)

    return matches


def part1(data):
    """
    >>> part1(read_input())
    529
    """

    count = 0

    for (before, instruction, after) in data[0]:
        (_, a, b, c) = instruction
        
        if len(op_matches(before, after, a, b, c)) >= 3:
            count += 1
    
    return count


def part2(data):
    """
    >>> part2(read_input())
    573
    """

    samples, code = data
    match_map = defaultdict(set)

    for (before, instruction, after) in samples:
        (op_id, a, b, c) = instruction
        matches = op_matches(before, after, a, b, c)

        for match in matches:
            match_map[op_id].add(match)

    op_map = {}

    while sum(len(matches) for matches in match_map.values()) > 0:
        # Find the first id that maps to only one function
        op_id, op = next(iter((key, next(iter(matches))) for key, matches in match_map.items() if len(matches) == 1))
        
        # record the mapping found
        op_map[op_id] = op

        # exclude that operation from all the other lists
        for matches in match_map.values():
            if op in matches:
                matches.remove(op)

    registers = [0, 0, 0, 0]

    for instruction in code:
        op_id, a, b, c = instruction
        op_map[op_id](registers, a, b, c)

    return registers[0]


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
