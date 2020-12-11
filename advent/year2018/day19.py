# -*- coding: utf-8 -*-

import re
from collections import defaultdict
import advent.year2018.opcodes as opcodes

POINTER_PATTERN = re.compile(r"#ip (\d)")
INSTRUCTION_PATTERN = re.compile(r"([a-z]{4}) (\d+) (\d+) (\d+)")



def read_input():
    file = open('input/2018/day19-input.txt', 'r')
    text = file.read()
    
    match = POINTER_PATTERN.match(text)
    register = int(match.group(1))

    instructions = []

    for groups in INSTRUCTION_PATTERN.findall(text):
        instructions.append([groups[0]] + [int(i) for i in groups[1:4]])

    return (register, instructions)


def part1(data):
    """
    >>> part1((0, [['seti', 5, 0, 1], ['seti', 6, 0, 2], ['addi', 0, 1, 0], ['addr', 1, 2, 3], ['setr', 1, 0, 0], ['seti', 8, 0, 4], ['seti', 9, 0, 5]]))
    6
    """

    (ip, instructions) = data

    registers = [0, 0, 0, 0, 0, 0]
    pointer = 0 

    while 0 <= pointer < len(instructions):
        registers[ip] = pointer
        op, a, b, c = instructions[registers[ip]]
        getattr(opcodes, op)(registers, a, b, c)
        pointer = registers[ip] 
        pointer += 1

    return registers[0]


def part2(data):
    """
    >>> part2(read_input())
    0
    """

    (ip, instructions) = data

    registers = [1, 0, 0, 0, 0, 0]
    pointer = 0 

    while 0 <= pointer < len(instructions):
        registers[ip] = pointer
        op, a, b, c = instructions[registers[ip]]
        getattr(opcodes, op)(registers, a, b, c)
        pointer = registers[ip] 
        pointer += 1
        print(registers)

    return registers[0]


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
