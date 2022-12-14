# -*- coding: utf-8 -*-


def read_input():
    with open('input/2015/day17-input.txt', encoding='utf8') as file:
        return [int(line) for line in file]


def pour(pots, remaining, path=None, matches=None):
    """
    >>> pour([20, 15, 10, 5, 5], 25)
    [[15, 5, 5], [15, 10], [20, 5], [20, 5]]
    """

    if path is None:
        path = []

    if matches is None:
        matches = []

    if len(pots) == 0:
        return matches

    pot = pots[0]
    pots = pots[1:]

    pour(pots, remaining, path, matches)

    path = path + [pot]

    if pot == remaining:
        matches.append(path)
    elif pot < remaining:
        pour(pots, remaining - pot, path, matches)

    return matches


def part1(data):
    """
    >>> part1(read_input())
    1638
    """

    return len(pour(data, 150))


def part2(data):
    """
    >>> part2(read_input())
    17
    """

    combinations = pour(data, 150)
    shortest = min(len(combination) for combination in combinations)
    return sum(1 for combination in combinations if len(combination) == shortest)


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
