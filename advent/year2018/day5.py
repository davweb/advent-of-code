#!/usr/local/bin/python3

import string

def read_input():
    file = open('input/2018/day5-input.txt', 'r')
    return file.read()

def reduce(polymer):
    while True:
        before_len = len(polymer)

        for lower in string.ascii_lowercase:
            upper = lower.upper()
            polymer = polymer.replace(lower + upper,'')
            polymer = polymer.replace(upper + lower,'')

        if len(polymer) == before_len:
            break

    return before_len

def part1(polymer):
    """
    >>> part1(read_input())
    11264
    """
    return reduce(polymer)

def part2(polymer):
    """
    >>> part2(read_input())
    4552
    """
    min_length = len(polymer) + 1
    
    for lower in string.ascii_lowercase:
        upper = lower.upper()
        optimized = polymer.replace(lower,'').replace(upper, '')
        length = reduce(optimized)

        if length < min_length:
            min_length = length

    return min_length

def main():
    data = read_input()
    print(part1(data))
    print(part2(data))

if __name__ == "__main__":
    main()
