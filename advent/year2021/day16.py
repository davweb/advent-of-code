# -*- coding: utf-8 -*-

from math import prod
from enum import IntEnum

HEX_MAP = {
    '0': (0, 0, 0, 0),
    '1': (0, 0, 0, 1),
    '2': (0, 0, 1, 0),
    '3': (0, 0, 1, 1),
    '4': (0, 1, 0, 0),
    '5': (0, 1, 0, 1),
    '6': (0, 1, 1, 0),
    '7': (0, 1, 1, 1),
    '8': (1, 0, 0, 0),
    '9': (1, 0, 0, 1),
    'A': (1, 0, 1, 0),
    'B': (1, 0, 1, 1),
    'C': (1, 1, 0, 0),
    'D': (1, 1, 0, 1),
    'E': (1, 1, 1, 0),
    'F': (1, 1, 1, 1)
}


class Type(IntEnum):
    SUM = 0
    PRODUCT = 1
    MIN = 2
    MAX = 3
    LITERAL = 4
    GREATER_THAN = 5
    LESS_THAN = 6
    EQUAL = 7


LENGTH_TOTAL = 0


def read_input():
    with open('input/2021/day16-input.txt', encoding='utf8') as file:
        return file.read().strip()


def hex_to_bits(string):
    """
    >>> hex_to_bits("")
    []
    >>> hex_to_bits("8A")
    [1, 0, 0, 0, 1, 0, 1, 0]
    """

    bits = []

    for c in string:
        bits.extend(HEX_MAP[c])

    return bits


def pop_n(input_list, n):
    """
    >>> sample = [1, 2, 3, 4]
    >>> pop_n(sample, 2)
    [1, 2]
    >>> sample
    [3, 4]
    """

    result = input_list[:n]
    del input_list[:n]
    return result


def bits_to_int(bits):
    """
    >>> bits_to_int((1, 0, 0))
    4
    """

    bits = list(bits)
    value = 0
    unit = 1

    while bits:
        bit = bits.pop()
        value += unit * bit
        unit *= 2

    return value


def parse(bits, count=None):
    """
    >>> parse(hex_to_bits('D2FE28'))
    [(6, 4, 2021)]
    >>> parse(hex_to_bits('38006F45291200'))
    [(1, 6, [(6, 4, 10), (2, 4, 20)])]
    >>> parse(hex_to_bits('EE00D40C823060'))
    [(7, 3, [(2, 4, 1), (4, 4, 2), (1, 4, 3)])]
    """

    result = []

    while bits and (count is None or count > 0):
        try:
            version = bits_to_int(pop_n(bits, 3))
            type_id = bits_to_int(pop_n(bits, 3))

            if type_id == Type.LITERAL:
                literal = []
                last_group = False

                while not last_group:
                    last_group = bits.pop(0) == 0
                    literal.extend(pop_n(bits, 4))

                value = bits_to_int(literal)
            else:
                length_type = bits.pop(0)

                if length_type == LENGTH_TOTAL:
                    total_length = bits_to_int(pop_n(bits, 15))
                    subpackets = pop_n(bits, total_length)
                    value = parse(subpackets)
                else:
                    total_length = None
                    packet_count = bits_to_int(pop_n(bits, 11))
                    value = parse(bits, count=packet_count)

            if value != []:
                result.append((version, type_id, value))
        except IndexError:
            break

        if count is not None:
            count -= 1

    return result


def sum_version(packets):
    total = 0

    for packet in packets:
        version, _, value = packet
        total += version

        if isinstance(value, list):
            total += sum_version(value)

    return total


def calculate(packet):
    match packet:
        case(_, Type.SUM, value):
            output = sum(calculate(sub) for sub in value)
        case(_, Type.PRODUCT, value):
            output = prod(calculate(sub) for sub in value)
        case(_, Type.MIN, value):
            output = min(calculate(sub) for sub in value)
        case(_, Type.MAX, value):
            output = max(calculate(sub) for sub in value)
        case(_, Type.LITERAL, value):
            return value
        case(_, Type.GREATER_THAN, value):
            first = calculate(value[0])
            second = calculate(value[1])
            output = int(first > second)
        case(_, Type.LESS_THAN, value):
            first = calculate(value[0])
            second = calculate(value[1])
            output = int(first < second)
        case(_, Type.EQUAL, value):
            first = calculate(value[0])
            second = calculate(value[1])
            output = int(first == second)
        case _:
            raise ValueError(packet)

    return output


def sum_packets(packets):
    total = 0

    for packet in packets:
        version, _, value = packet
        total += version

        if isinstance(value, list):
            total += sum_version(value)

    return total


def part1(data):
    """
    >>> part1(read_input())
    886
    """

    bits = hex_to_bits(data)
    packets = parse(bits)
    return sum_version(packets)


def part2(data):
    """
    >>> part2(read_input())
    184487454837
    """

    bits = hex_to_bits(data)
    packets = parse(bits)
    return calculate(packets[0])


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
