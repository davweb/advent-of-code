#!/usr/local/bin/python3

from advent.year2019.intcode import IntCode

def read_input():
    return [int(code) for code in open('input/2019/day5-input.txt', 'r').read().split(',')]


def part1(data):
    """
    >>> part1(read_input())
    12234644
    """

    return IntCode(data, [1]).run()[-1]


def part2(data):
    """
    >>> part2(read_input())
    3508186
    """

    return IntCode(data).execute([5])


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))

if __name__ == "__main__":
    main()
