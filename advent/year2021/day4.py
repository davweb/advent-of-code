# -*- coding: utf-8 -*-

import re

PATTERN = re.compile(r'\n*(\d+) +(\d+) +(\d+) +(\d+) +(\d+)' * 5)


class BingoCard:
    def __init__(self, values):
        self.values = set()
        self.rows = [set() for _ in range(5)]
        self.columns = [set() for _ in range(5)]

        for i, value in enumerate(values):
            self.values.add(value)
            self.rows[i // 5].add(value)
            self.columns[i % 5].add(value)

    def play(self, value):
        self.values.discard(value)

        for row in self.rows:
            row.discard(value)

        for column in self.columns:
            column.discard(value)

    def is_winner(self):
        """
        >>> card = BingoCard(range(1,26))
        >>> card
         1  2  3  4  5
         6  7  8  9 10
        11 12 13 14 15
        16 17 18 19 20
        21 22 23 24 25
        >>> card.play(1)
        >>> card.play(2)
        >>> card.play(4)
        >>> card.play(3)
        >>> card.is_winner()
        False
        >>> card.play(5)
        >>> card.is_winner()
        True
        >>> expected = sum(range(6,26))
        >>> card.remaining() == expected
        True
        """

        return any(len(line) == 0 for line in self.rows + self.columns)

    def __repr__(self):
        # autopep8: off
        return '\n'.join(' '.join(f'{cell:2d}' for cell in row) for row in self.rows)
        # autopep8: on

    def remaining(self):
        return sum(self.values)


def read_input():
    with open('input/2021/day4-input.txt', encoding='utf8') as file:
        move_list = file.readline()
        card_numbers = file.read()

    moves = [int(move) for move in move_list.strip().split(',')]
    matches = PATTERN.findall(card_numbers)
    cards = [BingoCard(int(value) for value in match) for match in matches]
    return moves, cards


def part1(data):
    """
    >>> part1(read_input())
    32844
    """

    moves, cards = data

    for move in moves:
        for card in cards:
            card.play(move)

            if card.is_winner():
                return move * card.remaining()

    raise ValueError()


def part2(data):
    """
    >>> part2(read_input())
    4920
    """

    moves, cards = data

    for move in moves:
        for card in list(cards):
            card.play(move)

            if card.is_winner():
                if len(cards) == 1:
                    return move * card.remaining()

                cards.remove(card)

    raise ValueError()


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
