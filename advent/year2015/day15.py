# -*- coding: utf-8 -*-

import re


PATTERN = re.compile(r"(\w+): capacity (-?\d+), durability (-?\d+), flavor (-?\d+), texture (-?\d+), calories (-?\d+)")


def read_input():
    results = []

    with open('input/2015/day15-input.txt') as file:
        for line in file.readlines():
            match = PATTERN.match(line)
            name, capacity, durability, flavor, texture, calories, = match.group(1, 2, 3, 4, 5, 6)
            results.append((name, int(capacity), int(durability), int(flavor), int(texture), int(calories)))

    return results


def options(count, total):
    if count == 1:
        return [[total]]

    results = []

    for i in range(0, total + 1):
        for j in options(count - 1, total - i):
            results.append([i] + j)

    return results


def bake(cookies, calorie_target=None):
    """
    >>> bake([('Butterscotch', -1, -2, 6, 3, 8), ('Cinnamon', 2, 3, -2, -1, 3)])
    62842880
    """

    cookie_count = len(cookies)
    best_cookie = 0

    for weights in options(cookie_count, 100):
        capacity = 0
        durability = 0
        flavor = 0
        texture = 0
        calories = 0

        for i, cookie in enumerate(cookies):
            capacity += cookie[1] * weights[i]
            durability += cookie[2] * weights[i]
            flavor += cookie[3] * weights[i]
            texture += cookie[4] * weights[i]
            calories += cookie[5] * weights[i]

        if capacity <= 0 or durability <= 0 or flavor <= 0 or texture <= 0:
            continue

        if calorie_target is not None and calories != calorie_target:
            continue

        score = capacity * durability * flavor * texture
        best_cookie = max(best_cookie, score)

    return best_cookie


def part1(data):
    """
    >>> part1(read_input())
    13882464
    """

    return bake(data)


def part2(data):
    """
    >>> part2(read_input())
    11171160
    """

    return bake(data, calorie_target=500)


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
