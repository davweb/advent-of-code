# -*- coding: utf-8 -*-

import re
from collections import Counter
from enum import IntEnum

PATTERN = re.compile(r'(\d+) <-> ((\d+, )*\d+)')


class Hand(IntEnum):
    FIVE_OF_A_KIND = 6
    FOUR_OF_A_KIND = 5
    FULL_HOUSE = 4
    THREE_OF_A_KIND = 3
    TWO_PAIR = 2
    ONE_PAIR = 1
    HIGH_CARD = 0


def read_input(filename='input/2023/day7-input.txt'):
    with open(filename, encoding='utf8') as file:
        for line in file:
            values = line.split()
            yield values[0], int(values[1])


def type_of_hand(hand, jokers=False):
    """
    >>> type_of_hand('AAAAA')
    <Hand.FIVE_OF_A_KIND: 6>
    >>> type_of_hand('12222')
    <Hand.FOUR_OF_A_KIND: 5>
    >>> type_of_hand('11222')
    <Hand.FULL_HOUSE: 4>
    >>> type_of_hand('11922')
    <Hand.TWO_PAIR: 2>
    >>> type_of_hand('AJKQ3')
    <Hand.HIGH_CARD: 0>
    """

    counts = Counter(hand)

    if jokers:
        joker_count = counts['J']
        counts.subtract({'J': joker_count})
    else:
        joker_count = 0

    mc = counts.most_common()
    first = mc[0][1]
    second = 0 if len(mc) == 1 else mc[1][1]

    first += joker_count

    if first > 5:
        second += first - 5
        first = 5

    match first, second:
        case 5, _:
            return Hand.FIVE_OF_A_KIND
        case 4, _:
            return Hand.FOUR_OF_A_KIND
        case 3, 2:
            return Hand.FULL_HOUSE
        case 3, _:
            return Hand.THREE_OF_A_KIND
        case 2, 2:
            return Hand.TWO_PAIR
        case 2, _:
            return Hand.ONE_PAIR
        case 1, _:
            return Hand.HIGH_CARD
        case _, _:
            raise ValueError(hand)


def hand_as_ints(hand, jokers=False):
    """
    >>> hand_as_ints('AKJ23')
    [14, 13, 11, 2, 3]
    >>> hand_as_ints('AKJ23', jokers=True)
    [14, 13, 1, 2, 3]
    """

    result = []

    for c in hand:
        match c:
            case 'A':
                i = 14
            case 'K':
                i = 13
            case 'Q':
                i = 12
            case 'J':
                i = 1 if jokers else 11
            case 'T':
                i = 10
            case _:
                i = int(c)

        result.append(i)

    return result


def score_hands_and_bids(data, jokers):
    hands_and_bids = list(data)

    def hand_key(hand_and_bid):
        hand = hand_and_bid[0]
        return type_of_hand(hand, jokers=jokers), hand_as_ints(hand, jokers=jokers)

    hands_and_bids.sort(key=hand_key)

    return sum((rank * bid) for (rank, (_, bid)) in enumerate(hands_and_bids, start=1))


def part1(data):
    """
    >>> part1((('32T3K', 765), ('T55J5', 684), ('KK677', 28), ('KTJJT', 220), ('QQQJA', 483)))
    6440
    >>> part1(read_input())
    245794640
    """

    return score_hands_and_bids(data, False)


def part2(data):
    """
    >>> part2((('32T3K', 765), ('T55J5', 684), ('KK677', 28), ('KTJJT', 220), ('QQQJA', 483)))
    5905
    >>> part2(read_input())
    247899149
    """

    return score_hands_and_bids(data, True)


def main():
    print(part1(read_input()))
    print(part2(read_input()))


if __name__ == "__main__":
    main()
