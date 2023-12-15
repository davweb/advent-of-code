# -*- coding: utf-8 -*-

from collections import OrderedDict
from functools import reduce


def read_input(filename='input/2023/day15-input.txt'):
    with open(filename, encoding='utf8') as file:
        return file.read().strip().split(",")


def holiday_hash(value):
    """
    >>> holiday_hash('rn=1')
    30
    >>> holiday_hash('cm-')
    253
    """

    return reduce(lambda x, y: ((x + ord(y)) * 17) % 256, value, 0)


def part1(data):
    """
    >>> part1(read_input())
    505379
    """

    return sum(holiday_hash(value) for value in data)


def part2(data):
    """
    >>> part2(('rn=1', 'cm-', 'qp=3', 'cm=2', 'qp-', 'pc=4', 'ot=9', 'ab=5', 'pc-', 'pc=6', 'ot=7'))
    145
    >>> part2(read_input())
    263211
    """

    boxes = [OrderedDict() for _ in range(256)]

    for instruction in data:
        if instruction.endswith('-'):
            label = instruction[:-1]
            box = boxes[holiday_hash(label)]
            if label in box:
                del box[label]
        else:
            label, value = instruction.split('=')
            box = boxes[holiday_hash(label)]
            box[label] = int(value)

    return sum(box_no * slot * focal_length for box_no, box in enumerate(boxes, start=1)
               for slot, focal_length in enumerate(box.values(), start=1))


def main():
    print(part1(read_input()))
    print(part2(read_input()))


if __name__ == "__main__":
    main()
