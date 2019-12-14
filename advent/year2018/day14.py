#!/usr/local/bin/python3

from collections import defaultdict
from itertools import product
from functools import lru_cache

def part1(input):
    """
    >>> part1(5)
    '0124515891'
    >>> part1(18)
    '9251071085'
    >>> part1(2018)
    '5941429882'
    >>> part1(503761)
    '1044257397'
    """

    elves = [0, 1]
    recipes = [3, 7]
    
    while len(recipes) < input + 10:
        total = sum(recipes[elf] for elf in elves)
        recipes += [int(digit) for digit in str(total)]

        for i in range(0, len(elves)):
            elves[i] = (elves[i] + recipes[elves[i]] + 1) % len(recipes)

    return "".join(str(i) for i in recipes[input:input + 10])


def part2(input):
    """
    >>> part2("01245")
    5
    >>> part2("51589")
    9
    >>> part2("92510")
    18
    >>> part2("59414")
    2018
    >>> part2("503761")
    20185425
    """

    end = [int(i) for i in input]
    size = len(end)
    tail = [-1] * size
    elves = [0, 1]
    recipes = [3, 7]

    while True:
        # total = sum(recipes[elf] for elf in elves)
        total = recipes[elves[0]] + recipes[elves[1]]

        if total > 9:
            new_recipes = [1, total % 10]
        else:
            new_recipes = [total % 10]

        for recipe in new_recipes:
            recipes.append(recipe)
            tail.pop(0)
            tail.append(recipe)

            if tail == end:
                return len(recipes) - size

        # for i in range(0, len(elves)):
        #    elves[i] = (elves[i] + recipes[elves[i]] + 1) % len(recipes)
        no_of_recipes = len(recipes)
        elves[0] = (elves[0] + recipes[elves[0]] + 1) % no_of_recipes
        elves[1] = (elves[1] + recipes[elves[1]] + 1) % no_of_recipes


def main():
    print(part1(503761))
    print(part2("503761"))

    
if __name__ == "__main__":
    main()
    