#!/usr/local/bin/python3

from intcode import IntCode

def read_input():
    return [int(code) for code in open('input/day5-input.txt', 'r').read().split(',')]


        

def part1(data):
    print(IntCode(data, [1]).execute())

def part2(data):
    print(IntCode(data, [5]).execute())


def main():
    data = read_input()
    part1(data)
    part2(data)

if __name__ == "__main__":
    main()
