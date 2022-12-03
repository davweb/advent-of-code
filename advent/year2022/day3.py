# -*- coding: utf-8 -*-

from functools import reduce


def read_input():
    with open('input/2022/day3-input.txt', encoding='utf8') as file:
        return [line.strip() for line in file.readlines()]


def priority(char):
    """
    >>> priority('a')
    1
    >>> priority('z')
    26
    >>> priority('A')
    27
    >>> priority('Z')
    52
    """

    if len(char) != 1:
        raise ValueError()

    if 'a' <= char <= 'z':
        return ord(char) - 96

    if 'A' <= char <= 'Z':
        return ord(char) - 38

    raise ValueError()


def shared(rucksack):
    """
    >>> shared('vJrwpWtwJgWrhcsFMMfFFhFp')
    'p'
    >>> shared('jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL')
    'L'
    >>> shared('PmmdzqPrVvPwwTWBwg')
    'P'
    >>> shared('wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn')
    'v'
    >>> shared('ttgJtRGJQctTZtZT')
    't'
    >>> shared('CrZsJsPPZsGzwwsLwLmpwMDw')
    's'
    """

    middle = len(rucksack) // 2
    left = set(rucksack[0:middle])
    right = set(rucksack[middle:])
    both = left.intersection(right)

    if len(both) != 1:
        raise ValueError

    return both.pop()


def common(group):
    """
    >>> common(('vJrwpWtwJgWrhcsFMMfFFhFp', 'jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL', 'PmmdzqPrVvPwwTWBwg'))
    'r'
    """

    repeated = reduce(lambda a, b: a.intersection(set(b)), group[1:], set(group[0]))

    if len(repeated) != 1:
        raise ValueError

    return repeated.pop()


def transform(lines):
    i = 0

    while i < len(lines):
        yield (lines[i], lines[i + 1], lines[i + 2])
        i += 3


def part1(data):
    """
    >>> part1(read_input())
    7863
    """

    return sum(priority(shared(rucksack)) for rucksack in data)


def part2(data):
    """
    >>> part2(read_input())
    2488
    """

    return sum(priority(common(group)) for group in transform(data))


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
