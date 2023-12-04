# -*- coding: utf-8 -*-

import re
from functools import cache

CARD_PATTERN = re.compile(r'Card +\d+: (.*) \| (.*)')


def read_input(filename='input/2023/day4-input.txt'):
    with open(filename, encoding='utf8') as file:
        for line in file:
            result = CARD_PATTERN.match(line)
            winners = set(int(card) for card in result.group(1).split())
            numbers = set(int(card) for card in result.group(2).split())
            yield winners, numbers


def card_matches(cards):
    for winners, numbers in cards:
        yield len(winners & numbers)


def part1(data):
    """
    >>> part1(read_input())
    18619
    """

    return sum(2 ** (matches - 1) for matches in card_matches(data) if matches > 0)


def part2(data):
    """
    >>> part2(read_input())
    8063216
    """

    match_counts = list(card_matches(data))

    @cache
    def card_count(card_number):
        matches = match_counts[card_number - 1]
        copies_won = range(card_number + 1, card_number + 1 + matches)
        return matches + sum(card_count(copy_card) for copy_card in copies_won)

    return len(match_counts) + sum(card_count(card_number) for card_number in range(1, 1 + len(match_counts)))


def main():
    print(part1(read_input()))
    print(part2(read_input()))


if __name__ == "__main__":
    main()
