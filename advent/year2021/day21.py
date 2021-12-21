# -*- coding: utf-8 -*-

from itertools import cycle, product
from collections import Counter

INPUT = [2, 10]
DIRAC_DICE = Counter(sum(dice) for dice in product(range(1, 4), range(1, 4), range(1, 4))).items()


def deterministic_dice():
    """
    >>> d = deterministic_dice()
    >>> next(d)
    (1, 2, 3)
    >>> next(d)
    (4, 5, 6)
    """

    dice = cycle(range(1, 101))
    while True:
        yield (next(dice), next(dice), next(dice))


def part1(data):
    """
    >>> part1(INPUT)
    571032
    """

    locations = data.copy()
    scores = [0, 0]
    rolls = 0
    dice = deterministic_dice()
    player = 0

    while all(score < 1000 for score in scores):
        rolls += 3
        move = sum(next(dice))
        new_location = locations[player] + move

        while new_location > 10:
            new_location -= 10

        locations[player] = new_location
        scores[player] += new_location
        player = 1 - player

    return rolls * min(scores)


def part2(data):
    """
    >>> part2(INPUT)
    49975322685009
    """

    wins = [0, 0]
    queue = [(1, data.copy(), (0, 0), 0)]

    while queue:
        universes, locations, scores, player = queue.pop()

        for move, combinations in DIRAC_DICE:
            new_location = locations[player] + move

            while new_location > 10:
                new_location -= 10

            if player == 0:
                new_locations = (new_location, locations[1])
                new_scores = (scores[0] + new_location, scores[1])
            else:
                new_locations = (locations[0], new_location)
                new_scores = (scores[0], scores[1] + new_location)

            new_universes = universes * combinations

            if new_scores[player] >= 21:
                wins[player] += new_universes
            else:
                queue.append((new_universes, new_locations, new_scores, 1 - player))

    return max(wins)


def main():
    print(part1(INPUT))
    print(part2(INPUT))


if __name__ == "__main__":
    main()
