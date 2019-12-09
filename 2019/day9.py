#!/usr/local/bin/python3

from intcode import IntCode
import itertools

def read_input():
    return [int(code) for code in open('input/day9-input.txt', 'r').read().split(',')]

def part1(code):
    print(IntCode(code).execute([1]))

def part2(code):
    print(IntCode(code).execute([2]))


def main():
    code = read_input()
    part1(code)
    part2(code)

if __name__ == "__main__":
    main()
