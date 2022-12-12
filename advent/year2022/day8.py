# -*- coding: utf-8 -*-

import numpy


def read_input():
    with open('input/2022/day8-input.txt', encoding='utf8') as file:
        return [[int(tree) for tree in line.strip()] for line in file.readlines()]


def count_trees(data):
    """
    >>> count_trees([[3, 0, 3, 7, 3], [2, 5, 5, 1, 2], [6, 5, 3, 3, 2], [3, 3, 5, 4, 9], [3, 5, 3, 9, 0]])
    21
    """

    trees = numpy.array(data)
    visible = 0

    for (x, y) in numpy.ndindex(trees.shape):
        height = trees[x, y]

        if all(tree < height for tree in trees[0:x, y]) \
                or all(tree < height for tree in trees[x + 1:, y]) \
                or all(tree < height for tree in trees[x, 0:y]) \
                or all(tree < height for tree in trees[x, y + 1:]):
            visible += 1

    return visible


def count_visible(height, trees):
    """
    >>> count_visible(5, [])
    0
    >>> count_visible(5, [5, 6, 7])
    1
    >>> count_visible(7, [5, 6, 7])
    3
    >>> count_visible(6, [5, 6, 7])
    2
    """

    visible = 0

    for tree in trees:
        visible += 1

        if tree >= height:
            break

    return visible


def scenic_score(data):
    """
    >>> scenic_score([[3, 0, 3, 7, 3], [2, 5, 5, 1, 2], [6, 5, 3, 3, 2], [3, 3, 5, 4, 9], [3, 5, 3, 9, 0]])
    8
    """

    best = -1

    trees = numpy.array(data)

    for (x, y) in numpy.ndindex(trees.shape):
        height = trees[x, y]

        #  0 - 1 = -1 which confuses the slices
        #  but score will be 0 so fine to skip
        if x == 0 or y == 0:
            continue

        score = count_visible(height, trees[x, y - 1::-1]) \
            * count_visible(height, trees[x, y + 1:]) \
            * count_visible(height, trees[x - 1::-1, y]) \
            * count_visible(height, trees[x + 1:, y])

        best = max(best, score)

    return best


def part1(data):
    """
    >>> part1(read_input())
    1719
    """

    return count_trees(data)


def part2(data):
    """
    >>> part2(read_input())
    590824
    """

    return scenic_score(data)


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
