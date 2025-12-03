# -*- coding: utf-8 -*-

from collections import defaultdict, namedtuple


def quantities(entry):
    quantity, name = entry.split(' ')
    return int(quantity), name


def read_input():
    Recipe = namedtuple('Recipe', ['quantity', 'ingredients'])
    recipes = {}

    with open('input/2019/day14-input.txt', encoding='utf-8') as file:
        for line in file.readlines():
            input_list, output = line.strip().split(' => ')
            output_quantity, output_name = quantities(output)
            ingredients = {}

            for input_entry in input_list.split(', '):
                input_quantity, input_name = quantities(input_entry)
                ingredients[input_name] = input_quantity

            recipes[output_name] = Recipe(output_quantity, ingredients)

    return recipes


def refine(recipes, target):
    complexity = {'ORE': -1}

    for makes, recipe in recipes.items():
        needs = set()
        queue = list(recipe.ingredients.keys())

        while len(queue) > 0:
            ingredient = queue.pop()

            if ingredient in needs or ingredient == 'ORE':
                continue

            needs.add(ingredient)
            needs_recipe = recipes[ingredient]
            queue += list(needs_recipe.ingredients.keys())

        complexity[makes] = len(needs)

    totals = defaultdict(int)
    totals['FUEL'] = target

    while True:
        if len(totals) == 1 and 'ORE' in totals:
            return totals['ORE']

        best_ingredient = sorted(totals.keys(), key=lambda i: complexity[i])[-1]
        recipe = recipes[best_ingredient]
        quantity_needed = totals[best_ingredient]
        multiplier = quantity_needed // recipe.quantity

        if quantity_needed % recipe.quantity != 0:
            multiplier += 1

        for i_name, i_quantity in recipe.ingredients.items():
            totals[i_name] += i_quantity * multiplier

        del totals[best_ingredient]


def part1(recipes):
    """
    >>> part1(read_input())
    198984
    """

    return refine(recipes, 1)


def part2(recipes):
    """
    >>> part2(read_input())
    7659732
    """

    target = 1000000000000
    lower = 0
    upper = 10000000000

    while upper - lower > 1:
        middle = (upper + lower) // 2

        if refine(recipes, middle) < target:
            lower = middle
        else:
            upper = middle

    return lower


def main():
    code = read_input()
    print(part1(code))
    print(part2(code))


if __name__ == "__main__":
    main()
