# -*- coding: utf-8 -*-

import re
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
    >>> part1(read_input())
    1848
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


def calculate(start_a):
    """
    >>> calculate(0)
    1848
    >>> calculate(1)
    22157688
    """

    a = 0
    b = 10551260 if start_a == 1 else 860

    for d in range(1, b + 1):
        if b % d == 0:
            a += d

    return a


def part2():
    """
    >>> part2()
    22157688
    """

    return calculate(1)


def main():
    data = read_input()
    print(part1(data))
    print(part2())


if __name__ == "__main__":
    main()
