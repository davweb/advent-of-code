# -*- coding: utf-8 -*-

import re
from enum import Enum
import numpy

PATTERN_RECT = re.compile(r'rect (\d+)x(\d+)')
PATTERN_ROW = re.compile(r'rotate row y=(\d+) by (\d+)')
PATTERN_COLUMN = re.compile(r'rotate column x=(\d+) by (\d+)')


class Instruction(Enum):
    FILL = 1
    ROW = 2
    COLUMN = 3


def read_input():
    results = []

    with open('input/2016/day8-input.txt', encoding='utf8') as file:
        for line in file.readlines():
            if match := PATTERN_RECT.match(line):
                instruction = Instruction.FILL
            elif match := PATTERN_ROW.match(line):
                instruction = Instruction.ROW
            elif match := PATTERN_COLUMN.match(line):
                instruction = Instruction.COLUMN
            else:
                raise ValueError(f'Did not match line: {line}')

            results.append((instruction, int(match.group(1)), int(match.group(2))))

    return results


class Screen:
    """
    >>> screen = Screen()
    >>> screen.fill(5, 3)
    >>> screen.rotate_column(3, 2)
    >>> screen.rotate_row(2, 5)
    >>> screen.fill(4, 4)
    >>> screen.count()
    np.int64(24)
    """

    def __init__(self):
        self.width = 50
        self.height = 6
        self.pixels = numpy.full((self.width, self.height), False)

    def fill(self, right, bottom):
        self.pixels[0:right, 0:bottom] = True

    def rotate_column(self, x, movement):
        rotated = numpy.roll(self.pixels[x, :], movement)
        self.pixels[x, :] = rotated

    def rotate_row(self, y, movement):
        rotated = numpy.roll(self.pixels[:, y], movement)
        self.pixels[:, y] = rotated

    def count(self):
        return numpy.count_nonzero(self.pixels)

    def __str__(self):
        output = ''

        for y in range(0, self.height):
            for x in range(0, self.width):
                output += '█' if self.pixels[x, y] else '·'
            output += '\n'

        return output.strip()


def part1and2(data):
    """
    >>> print(part1and2(read_input()))
    123
    ·██··████·███··█··█·███··████·███····██·███···███·
    █··█·█····█··█·█··█·█··█····█·█··█····█·█··█·█····
    █··█·███··███··█··█·█··█···█··███·····█·█··█·█····
    ████·█····█··█·█··█·███···█···█··█····█·███···██··
    █··█·█····█··█·█··█·█····█····█··█·█··█·█·······█·
    █··█·█····███···██··█····████·███···██··█····███··
    """

    screen = Screen()

    for instruction, a, b in data:
        if instruction == Instruction.FILL:
            screen.fill(a, b)
        elif instruction == Instruction.ROW:
            screen.rotate_row(a, b)
        elif instruction == Instruction.COLUMN:
            screen.rotate_column(a, b)

    return f'{screen.count()}\n{screen}'


def main():
    data = read_input()
    print(part1and2(data))


if __name__ == "__main__":
    main()
