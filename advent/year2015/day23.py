# -*- coding: utf-8 -*-

import re

PATTERN = re.compile(r'([a-z]{3}) (a|b)?[, ]*([+-]\d+)?')


def read_input(filename='input/2015/day23-input.txt'):
    data = []

    with open(filename, encoding='utf8') as file:
        for line in file:
            if match := PATTERN.match(line):
                command, register, step = match.groups()
                if step is not None:
                    step = int(step)
                data.append((command, register, step))
            else:
                raise ValueError(line)

    return data


def run_code(data, a=0):
    pointer = 0
    registers = {'a': a, 'b': 0}

    while pointer < len(data):
        match data[pointer]:
            case 'hlf', register, _:
                registers[register] //= 2
                pointer += 1
            case 'tpl', register, _:
                registers[register] *= 3
                pointer += 1
            case 'inc', register, _:
                registers[register] += 1
                pointer += 1
            case 'jmp', _, step:
                pointer += step
            case 'jie', register, step:
                pointer += step if registers[register] % 2 == 0 else 1
            case 'jio', register, step:
                pointer += step if registers[register] == 1 else 1
            case line:
                raise ValueError(line)

    return registers['b']


def part1(data):
    """
    >>> part1(read_input())
    255
    """

    return run_code(data)


def part2(data):
    """
    >>> part2(read_input())
    334
    """

    return run_code(data, 1)


def main():
    print(part1(read_input()))
    print(part2(read_input()))


if __name__ == "__main__":
    main()
