#!/usr/local/bin/python3

from advent.year2019.intcode import IntCode

def read_input():
    return [int(code) for code in open('input/2019/day9-input.txt', 'r').read().split(',')]


def part1(code):
    """
    >>> part1(read_input())
    2350741403
    """

    return IntCode(code).execute([1])


def part2(code):
    """
    >>> part2(read_input())
    53088
    """

    return IntCode(code).execute([2])


def main():
    code = read_input()
    print(part1(code))
    print(part2(code))

if __name__ == "__main__":
    main()
