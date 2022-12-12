# -*- coding: utf-8 -*-

from enum import Enum


class Hand(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


def read_input():
    with open('input/2022/day2-input.txt', encoding='utf8') as file:
        return [line.strip().split(' ') for line in file.readlines()]


def score_round(opponent, me):
    """
    >>> score_round(Hand.ROCK, Hand.PAPER)
    8
    >>> score_round(Hand.PAPER, Hand.ROCK)
    1
    >>> score_round(Hand.SCISSORS, Hand.SCISSORS)
    6
    """

    score = 0

    match me:
        case Hand.ROCK:
            score += 1
        case Hand.PAPER:
            score += 2
        case Hand.SCISSORS:
            score += 3

    match opponent, me:
        case [Hand.ROCK, Hand.PAPER] | [Hand.PAPER, Hand.SCISSORS] | [Hand.SCISSORS, Hand.ROCK]:
            score += 6
        case [play, response] if play == response:
            score += 3

    return score


def parse_opponent(opponent):
    match opponent:
        case 'A':
            return Hand.ROCK
        case 'B':
            return Hand.PAPER
        case 'C':
            return Hand.SCISSORS
        case _:
            raise ValueError()


def part1(data):
    """
    >>> part1([('A', 'Y'), ('B', 'X'), ('C', 'Z')])
    15
    >>> part1(read_input())
    13268
    """

    score = 0

    for a, b in data:
        opponent = parse_opponent(a)

        match b:
            case 'X':
                me = Hand.ROCK
            case 'Y':
                me = Hand.PAPER
            case 'Z':
                me = Hand.SCISSORS

        score += score_round(opponent, me)

    return score


def part2(data):
    """
    >>> part2(read_input())
    15508
    """

    score = 0

    for a, b in data:
        opponent = parse_opponent(a)

        match b, opponent:
            case 'X', Hand.ROCK:
                me = Hand.SCISSORS
            case 'X', Hand.PAPER:
                me = Hand.ROCK
            case 'X', Hand.SCISSORS:
                me = Hand.PAPER
            case 'Z', Hand.ROCK:
                me = Hand.PAPER
            case 'Z', Hand.PAPER:
                me = Hand.SCISSORS
            case 'Z', Hand.SCISSORS:
                me = Hand.ROCK
            case 'Y', play:
                me = play
            case _:
                raise ValueError()

        score += score_round(opponent, me)

    return score


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
