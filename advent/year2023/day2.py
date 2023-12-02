# -*- coding: utf-8 -*-

import re
from math import prod

GAME_PATTERN = re.compile(r'Game \d+: (.*)')
TURN_PATTERN = re.compile(r'(\d+) (red|green|blue)')


def read_input(filename='input/2023/day2-input.txt'):
    with open(filename, encoding='utf8') as file:
        for line in file:
            result = GAME_PATTERN.match(line)
            turn_details = result.group(1).split('; ')
            turns = []

            for turn_detail in turn_details:
                turn = {}

                for m in TURN_PATTERN.finditer(turn_detail):
                    count = int(m.group(1))
                    colour = m.group(2)
                    turn[colour] = count

                turns.append(turn)

            yield turns


def valid_game(game):
    """
    >>> valid_game([{'red': 1}])
    True
    >>> valid_game([{'green': 20}])
    False
    """

    LIMITS = {'red': 12, 'green': 13, 'blue': 14}

    for turn in game:
        for colour, limit in LIMITS.items():
            if colour in turn and turn[colour] > limit:
                return False

    return True


def power(game):
    """
    >>> power([{'blue': 3, 'red': 4}, {'red': 1, 'green': 2, 'blue': 6}, {'green': 2}])
    48
    """

    minimum = {'red': 0, 'green': 0, 'blue': 0}

    for turn in game:
        for colour, current_minimum in minimum.items():
            if colour in turn and turn[colour] > current_minimum:
                minimum[colour] = turn[colour]

    return prod(minimum.values())


def part1(data):
    """
    >>> part1(read_input())
    2101
    """

    return sum(game_number for game_number, game in enumerate(data, start=1) if valid_game(game))


def part2(data):
    """
    >>> part2(read_input())
    58269
    """

    return sum(power(game) for game in data)


def main():
    print(part1(read_input()))
    print(part2(read_input()))


if __name__ == "__main__":
    main()
