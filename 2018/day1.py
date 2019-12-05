#!/usr/local/bin/python3

import collections
import itertools

def read_input():
    file = open('input/day1-input.txt', 'r')
    return [int(line) for line in file.readlines()]

def calculate_frequency(data):
    """For example, if the device displays frequency changes of +1, -2, +3, +1, then
    starting from a frequency of zero, the following changes would occur:

    Current frequency  0, change of +1; resulting frequency  1.
    Current frequency  1, change of -2; resulting frequency -1.
    Current frequency -1, change of +3; resulting frequency  2.
    Current frequency  2, change of +1; resulting frequency  3.
    In this example, the resulting frequency is 3.

    Here are other example situations:

    >>> calculate_frequency([+1, +1, +1])
    3
    >>> calculate_frequency([+1, +1, -2])
    0
    >>> calculate_frequency([-1, -2, -3])
    -6
    """

    return sum(data)

def find_repeat(data):
    """You notice that the device repeats the same frequency change list over and
    over. To calibrate the device, you need to find the first frequency it
    reaches twice.

    >>> find_repeat([+1, -1])
    0
    >>> find_repeat([+3, +3, +4, -2, -4])
    10
    >>> find_repeat([-6, +3, +8, +5, -6])
    5
    >>> find_repeat([+7, +7, -2, -7, -4])
    14
    """ 

    count = collections.defaultdict(int)
    value = 0

    for increment in itertools.cycle(data):
        count[value] += 1

        if count[value] == 2:
            return value

        value += increment



def part1(data):
    total = calculate_frequency(data)
    print(total);

def part2(data):
    print(find_repeat(data))

def main():
    data = read_input()
    part1(data)
    part2(data)

if __name__ == "__main__":
    main()
