# -*- coding: utf-8 -*-
# pylint: disable=too-many-arguments,line-too-long

import re

GROUP_PATTERN = re.compile(
    r'(\d+) units each with (\d+) hit points.*with an attack that does (\d+) (\w+) damage at initiative (\d+)')
WEAK_PATTERN = re.compile(r'weak to ([a-z, ]+)')
IMMUNE_PATTERN = re.compile(r'immune to ([a-z, ]+)')


def read_input(filename='input/2018/day24-input.txt'):
    armies = [[], []]
    index = 0

    with open(filename, encoding='utf8') as file:
        for line in file:
            if match := GROUP_PATTERN.match(line):
                units, hit_points, damage, attack_type, initiative = match.groups()
                if match := WEAK_PATTERN.search(line):
                    weaknesses = tuple(match.group(1).split(', '))
                else:
                    weaknesses = []
                if match := IMMUNE_PATTERN.search(line):
                    immunities = tuple(match.group(1).split(', '))
                else:
                    immunities = []
                group = Group(
                    int(units),
                    int(hit_points),
                    int(initiative),
                    int(damage),
                    attack_type,
                    weaknesses,
                    immunities)
                armies[index].append(group)
            elif line.strip() == 'Infection:':
                index += 1
            elif line.strip() not in ('', 'Immune System:'):
                raise ValueError(line)

    return armies


class Group:
    def __init__(self, units, hit_points, initiative, damage, attack_type, weaknesses, immunities):
        self.units = units
        self.hit_points = hit_points
        self.initiative = initiative
        self.damage = damage
        self.attack_type = attack_type
        self.weaknesses = weaknesses
        self.immunities = immunities

    def effective_power(self):
        return self.units * self.damage

    def potential_damage(self, other):
        damage = self.effective_power()

        if self.attack_type in other.weaknesses:
            damage *= 2

        if self.attack_type in other.immunities:
            damage = 0

        return damage

    def target_selection_value(self, other):
        return (self.potential_damage(other), other.effective_power(), other.initiative)

    def select_target(self, army):
        target = sorted(army, key=self.target_selection_value, reverse=True)[0]
        return target if self.potential_damage(target) else None

    def attack(self, other):
        potential_units = self.potential_damage(other) // other.hit_points
        potential_units = min(potential_units, other.units)
        other.units -= potential_units
        return potential_units > 0

    def boost(self, boost):
        return Group(
            self.units,
            self.hit_points,
            self.initiative,
            self.damage + boost,
            self.attack_type,
            self.weaknesses,
            self.immunities)

    def copy(self):
        return self.boost(0)

    def __repr__(self):
        return f"Group(units={self.units}, hit_points={self.hit_points}, initiative={self.initiative}, damage={self.damage}, attack_type='{self.attack_type}', weaknesses={self.weaknesses}, immunities={self.immunities})"


def sort_by_effective_power(army):
    army = (group for group in army if group.units > 0)
    return sorted(army, key=lambda g: (g.effective_power(), g.initiative), reverse=True)


def fight(armies):
    """
    >>> fight(read_input(filename='input/2018/day24-test.txt'))
    (5216, False)
    >>> armies = read_input(filename='input/2018/day24-test.txt')
    >>> armies[0] = [group.boost(1570) for group in armies[0]]
    >>> fight(armies)
    (51, True)
    """

    armies = [sort_by_effective_power(army) for army in armies]

    while all(len(army) > 0 for army in armies):
        targets = [set(armies[1]), set(armies[0])]
        attacks = []

        for army, target_list in zip(armies, targets):
            for group in army:
                target = group.select_target(target_list)

                if target is not None:
                    attacks.append((group.initiative, group, target))
                    target_list.remove(target)

                    if len(target_list) == 0:
                        break

        attacked = False

        for _, attacker, defender in sorted(attacks, reverse=True):
            if attacker.attack(defender):
                attacked = True

        if not attacked:
            return None, False

        armies = [sort_by_effective_power(army) for army in armies]

    win = len(armies[0]) > 0
    remaining = sum(sum(a.units for a in army) for army in armies)
    return remaining, win


def part1(data):
    """
    >>> part1(read_input())
    16325
    """

    return fight(data)[0]


def part2(data):
    """
    >>> part2(read_input())
    6787
    """

    low = 1
    high = 10000
    winning_score = None

    while high - low > 1:
        boost = low + (high - low) // 2

        immune = [group.boost(boost) for group in data[0]]
        infection = [group.copy() for group in data[1]]
        armies = [immune, infection]

        remaining, win = fight(armies)

        if win:
            high = boost
            winning_score = remaining
        else:
            low = boost

    return winning_score


def main():
    print(part1(read_input()))
    print(part2(read_input()))


if __name__ == "__main__":
    main()
