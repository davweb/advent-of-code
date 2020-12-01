#!/usr/local/bin/python3

import itertools


def read_input():
    file = open('input/2017/day2-input.txt', 'r')
    return [[int(x) for x in row.split("\t")] for row in file]


def part1(data):
    """
    >>> part1([[5, 1, 9, 5], [7, 5, 3], [2, 4, 6, 8,]])
    18
    >>> part1(read_input())
    43074
    """
   
    return sum(max(row) - min(row) for row in data)


def part2(data):
    """
    >>> part2([[5, 9, 2, 8], [9, 4, 7, 3], [3, 8, 6, 5]])
    9
    >>> part2(read_input())
    280
    """

    checksum = 0
    
    for row in data:
        for (a,b) in itertools.permutations(row, 2):
            if a % b == 0:
                checksum += a // b
                break

    return checksum


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
