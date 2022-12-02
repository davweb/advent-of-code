# -*- coding: utf-8 -*-

from enum import Enum

class State(Enum):
    NORMAL = 1
    READING_LENGTH = 2
    READING_MULTIPLE = 3
    READING_SECTION = 4

def read_input():
    with open('input/2016/day9-input.txt', encoding='utf8') as file:
        return file.read().strip()


def decode(value):
    """
    >>> decode("ADVENT")
    'ADVENT'
    >>> decode("A(1x5)BC")
    'ABBBBBC'
    >>> decode("(3x3)XYZ")
    'XYZXYZXYZ'
    >>> decode("A(2x2)BCD(2x2)EFG")
    'ABCBCDEFEFG'
    >>> decode("(6x1)(1x3)A")
    '(1x3)A'
    >>> decode("X(8x2)(3x3)ABCY")
    'X(3x3)ABC(3x3)ABCY'
    """

    output = ''
    state = State.NORMAL
    length = None
    multiple = None
    section = ''

    for char in value:
        match state, char:
            case State.READING_SECTION, c:
                section += c

                if len(section) == length:
                    output += section * multiple
                    state = State.NORMAL

            case State.NORMAL, '(':
                state = State.READING_LENGTH
                length = ''

            case State.NORMAL, c:
                output += c

            case State.READING_LENGTH, 'x':
                state = State.READING_MULTIPLE
                length = int(length)
                multiple = ''

            case State.READING_LENGTH, c:
                length += c

            case State.READING_MULTIPLE, ')':
                state = State.READING_SECTION
                multiple = int(multiple)
                section = ''

            case State.READING_MULTIPLE, c:
                multiple += c

    return output



def extract(value):
    """
    >>> extract('(3x3)XYZ')
    9
    >>> extract('X(8x2)(3x3)ABCY')
    20
    >>> extract('(27x12)(20x12)(13x14)(7x10)(1x12)A')
    241920
    >>> extract('(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN')
    445
    """

    result = 0
    state = State.NORMAL
    length = ''
    multiple = ''
    size = len(value)
    i = 0

    while i < size:
        char = value[i]

        match state, char:
            case State.NORMAL, '(':
                state = State.READING_LENGTH
                length = ''

            case State.NORMAL, c:
                result += 1

            case State.READING_LENGTH, 'x':
                state = State.READING_MULTIPLE
                length = int(length)
                multiple = ''

            case State.READING_LENGTH, c:
                length += c

            case State.READING_MULTIPLE, ')':
                state = State.NORMAL
                multiple = int(multiple)
                result += multiple * extract(value[i + 1:i + 1 + length])
                i += length

            case State.READING_MULTIPLE, c:
                multiple += c

        i += 1

    return result


def part1(data):
    """
    >>> part1(read_input())
    70186
    """

    return len(decode(data))


def part2(data):
    """
    >>> part2(read_input())
    10915059201
    """

    return extract(data)


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
