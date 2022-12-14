# -*- coding: utf-8 -*-

import re
from itertools import combinations, chain, product


class Item:

    def __init__(self, name, cost, damage, armor):
        self.name = name
        self.cost = cost
        self.damage = damage
        self.armor = armor

    def __str__(self):
        return self.name

    def __repr__(self):
        return 'Item(\'{name}\', {cost}, {damage}, {armor})'.format(**self.__dict__)


WEAPONS = [
    Item('Dagger', 8, 4, 0),
    Item('Shortsword', 10, 5, 0),
    Item('Warhammer', 25, 6, 0),
    Item('Longsword', 40, 7, 0),
    Item('Greataxe', 74, 8, 0)
]

ARMOR = [
    Item('Leather', 13, 0, 1),
    Item('Chainmail', 31, 0, 2),
    Item('Splintmail', 53, 0, 3),
    Item('Bandedmail', 75, 0, 4),
    Item('Platemail', 102, 0, 5)
]

RINGS = [
    Item('Damage +1', 25, 1, 0),
    Item('Damage +2', 50, 2, 0),
    Item('Damage +3', 100, 3, 0),
    Item('Defense +1', 20, 0, 1),
    Item('Defense +2', 40, 0, 2),
    Item('Defense +3', 80, 0, 3)
]

PATTERN = re.compile(r'(.*): (\d+)')


def read_input():

    with open('input/2015/day21-input.txt', encoding='utf8') as file:

        for line in file:
            match = PATTERN.match(line)

            if match:
                name = match.group(1)

                if name == 'Hit Points':
                    hit_points = int(match.group(2))
                elif name == 'Damage':
                    damage = int(match.group(2))
                elif name == 'Armor':
                    armor = int(match.group(2))
                else:
                    raise ValueError(name)
            else:
                raise ValueError(line)

    return (hit_points, damage, armor)


def player_wins(player, boss):
    """
    >>> player_wins((8, 5, 5), (12, 7, 2))
    True
    >>> player_wins((8, 5, 5), (100, 7, 2))
    False
    """
    player_hp, player_damage, player_armor = player
    boss_hp, boss_damage, boss_armor = boss

    while True:
        boss_hp -= max(1, player_damage - boss_armor)
        if boss_hp <= 0:
            return True

        player_hp -= max(1, boss_damage - player_armor)
        if player_hp <= 0:
            return False


def possible_items():
    """
    >>> len(list(possible_items()))
    660
    """

    possible_weapons = ((weapon,) for weapon in WEAPONS)
    possible_armor = chain(
        ((armor,) for armor in ARMOR),
        [()]
    )
    possible_rings = chain(
        combinations(RINGS, 2),
        ((ring,) for ring in RINGS),
        [()]
    )

    for weapons, armor_items, rings in product(possible_weapons, possible_armor, possible_rings):
        items = weapons + armor_items + rings
        cost = sum(item.cost for item in items)
        damage = sum(item.damage for item in items)
        armor = sum(item.armor for item in items)
        yield cost, damage, armor


def part1(data):
    """
    >>> part1(read_input())
    121
    """

    cheapest = None

    for cost, damage, armor in possible_items():

        if player_wins((100, damage, armor), data):
            cheapest = cost if cheapest is None else min(cost, cheapest)

    return cheapest


def part2(data):
    """
    >>> part2(read_input())
    201
    """

    most_expensive = None

    for cost, damage, armor in possible_items():

        if not player_wins((100, damage, armor), data):
            most_expensive = cost if most_expensive is None else max(cost, most_expensive)

    return most_expensive


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
