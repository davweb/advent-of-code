# -*- coding: utf-8 -*-

import re
import itertools

MASK_PATTERN = re.compile(r"mask = ([01X]+)")
MEM_PATTERN = re.compile(r"mem\[(\d+)\] = (\d+)")


def read_input():
    data = []
    with open('input/2020/day14-input.txt', encoding='utf-8') as file:
        for line in file:
            match = MASK_PATTERN.match(line)

            if match:
                data.append(("mask", match.group(1)))
                continue

            match = MEM_PATTERN.match(line)

            if match:
                data.append(("mem", (int(match.group(1)), int(match.group(2)))))
                continue

            raise ValueError(f"Did not match line '{line}'")

    return data


def mask(value, source):
    """
    >>> mask(11, "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X")
    73
    >>> mask(101, "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X")
    101
    >>> mask(0, "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X")
    64
    >>> mask(0, "1XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    34359738368
    """
    source = list(source)
    source.reverse()

    for i, c in enumerate(source):
        if c == 'X':
            continue

        bit = 2 ** i

        if c == '1':
            value |= bit
        else:
            value &= ~bit

    return value


def floating_mask(value, source):
    """
    >>> floating_mask(42, "000000000000000000000000000000X1001X")
    [26, 27, 58, 59]
    >>> floating_mask(26, "00000000000000000000000000000000X0XX")
    [16, 17, 18, 19, 24, 25, 26, 27]
    """
    source = list(source)
    source.reverse()
    masks = []

    for i, c in enumerate(source):
        bit = 2 ** i

        def set_bit(x, bit=bit):
            return x | bit

        def unset_bit(x, bit=bit):
            return x & ~bit

        if c == '1':
            value = set_bit(value)
        elif c == 'X':
            masks.append((set_bit, unset_bit))

    values = []

    for floaters in itertools.product(*masks):
        x = value

        for f in floaters:
            x = f(x)

        values.append(x)

    return sorted(values)


def part1(data):
    """
    >>> part1(read_input())
    5875750429995
    """

    bitmask = None
    mem = {}

    for (kind, value) in data:
        if kind == 'mask':
            bitmask = value
        else:
            mem[value[0]] = mask(value[1], bitmask)

    return sum(mem.values())


def part2(data):
    """
    >>> part2(read_input())
    5272149590143
    """

    bitmask = None
    mem = {}

    for (kind, value) in data:
        if kind == 'mask':
            bitmask = value
        else:
            for addr in floating_mask(value[0], bitmask):
                mem[addr] = value[1]

    return sum(mem.values())


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
