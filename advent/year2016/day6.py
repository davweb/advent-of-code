# -*- coding: utf-8 -*-

from collections import Counter


def read_input():
    with open('input/2016/day6-input.txt', encoding='utf8') as file:
        return [line.strip() for line in file.readlines()]


def count_letters(data):
    counters = []

    for _ in range(len(data[0])):
        counters.append(Counter())

    for line in data:
        for c, counter in zip(line, counters):
            counter.update(c)

    return counters


def part1(data):
    """
    >>> part1(read_input())
    'gyvwpxaz'
    """

    return ''.join(counter.most_common(1)[0][0] for counter in count_letters(data))


def part2(data):
    """
    >>> part2(read_input())
    'jucfoary'
    """

    return ''.join(counter.most_common()[-1][0] for counter in count_letters(data))


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
