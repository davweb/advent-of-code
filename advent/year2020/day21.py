# -*- coding: utf-8 -*-

import re

PATTERN = re.compile(r"((\w+ )*)(\(contains (.*)\))?")

def read_input():
    file = open("input/2020/day21-input.txt", "r")
    data = []

    for line in file:
        match = PATTERN.match(line)
        ingredients = set(match.group(1).strip().split(' '))
        allergens = set(match.group(4).strip().split(', '))
        data.append((ingredients, allergens))

    return data


def part1(data):
    """
    >>> part1([
    ...     ({'trh', 'fvjkl', 'sbzzf', 'mxmxvkd'}, {'dairy'}),
    ...     ({'mxmxvkd', 'kfcds', 'sqjhc', 'nhms'}, {'dairy', 'fish'}),
    ...     ({'sqjhc', 'fvjkl'}, {'soy'}),
    ...     ({'sqjhc', 'mxmxvkd', 'sbzzf'}, {'fish'})
    ... ])
    5
    >>> part1(read_input())
    2436
    """

    allergen_map = {}
    all_ingredients = set()

    for (ingredients, allergens) in data:
        all_ingredients |= ingredients

        for allergen in allergens:
            if allergen in allergen_map:
                allergen_map[allergen] &= ingredients
            else:
                allergen_map[allergen] = set(ingredients)

    used_ingredients = set()
    
    for i in allergen_map.values():
        used_ingredients |= i

    unused_ingredients = all_ingredients - used_ingredients
    unused_count = sum(len(ingredients & unused_ingredients) for ingredients, _ in data)

    return unused_count


def part2(data):
    """
    >>> part2([
    ...     ({'trh', 'fvjkl', 'sbzzf', 'mxmxvkd'}, {'dairy'}),
    ...     ({'mxmxvkd', 'kfcds', 'sqjhc', 'nhms'}, {'dairy', 'fish'}),
    ...     ({'sqjhc', 'fvjkl'}, {'soy'}),
    ...     ({'sqjhc', 'mxmxvkd', 'sbzzf'}, {'fish'})
    ... ])
    'mxmxvkd,sqjhc,fvjkl'
    >>> part2(read_input())
    'dhfng,pgblcd,xhkdc,ghlzj,dstct,nqbnmzx,ntggc,znrzgs'
    """

    allergen_map = {}

    for (ingredients, allergens) in data:
        for allergen in allergens:
            if allergen in allergen_map:
                allergen_map[allergen] &= ingredients
            else:
                allergen_map[allergen] = set(ingredients)

    allergen_key = {}

    while sum(len(ingredients) for ingredients in allergen_map.values()) > 0:
        # Find the first rule that maps to only one ingredient
        allergen, ingredient = next(iter((allergen, next(iter(ingredients))) for allergen, ingredients in allergen_map.items() if len(ingredients) == 1))
        
        # record the mapping found
        allergen_key[allergen] = ingredient

        # exclude that column from all the other lists
        for ingredients in allergen_map.values():
            if ingredient in ingredients:
                ingredients.remove(ingredient)

    alergen_list = ",".join(ingredient for _, ingredient in sorted(allergen_key.items()))

    return alergen_list


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
