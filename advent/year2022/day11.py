# -*- coding: utf-8 -*-

import re
import math

PATTERN = re.compile(r"""
    Monkey\ (\d+):\s+
    Starting\ items:\ (\d+[0-9 ,]*\d+)\s+
    Operation:\ new\ =\ old\ ([*+])\ (\w+|\d+)\s+
    Test:\ divisible\ by\ (\d+)\s+
        If\ true:\ throw\ to\ monkey\ (\d+)\s+
        If\ false:\ throw\ to\ monkey\ (\d+)\s+""", re.VERBOSE)


class Monkey:
    all = {}
    test_divisor = None

    def calculate_test_divisor():
        test_values = [monkey.test_value for monkey in Monkey.all.values()]
        return math.lcm(*test_values)

    def __init__(self, monkey_id, items, action, action_value, test_value, test_true, test_false):
        self.monkey_id = monkey_id
        self.items = items
        self.action = action
        self.action_value = action_value
        self.test_value = test_value
        self.test_true = test_true
        self.test_false = test_false
        self.inspections = 0

        Monkey.all[monkey_id] = self
        Monkey.test_divisor = Monkey.calculate_test_divisor()

    def __repr__(self):
        return f"Monkey({self.monkey_id}, {self.items}, '{self.action}', {self.action_value}, {self.test_value}, {self.test_true}, {self.test_false})"

    def __lt__(self, other):
        if self.inspections == other.inspections:
            return self.monkey_id < other.monkey_id
        else:
            return self.inspections < other.inspections

    def inspect(self, worry_divider=None):
        for item in self.items:
            self.inspections += 1
            if self.action == '*':
                item *= self.action_value
            elif self.action == '+':
                item += self.action_value
            elif self.action == '**':
                item **= self.action_value
            else:
                raise ValueError(self.action)

            if worry_divider is not None:
                item //= worry_divider

            item %= Monkey.test_divisor

            if item % self.test_value == 0:
                next_monkey = self.test_true
            else:
                next_monkey = self.test_false

            Monkey.all[next_monkey].items.append(item)

        self.items = []


def read_input(filename='input/2022/day11-input.txt'):
    monkeys = []

    with open(filename, encoding='utf8') as file:
        for match in PATTERN.findall(file.read()):
            monkey_id, items, action, action_value, test_value, test_true, test_false = match
            monkey_id = int(monkey_id)
            items = [int(value) for value in items.split(', ')]

            if action_value == 'old':
                action = '**'
                action_value = 2
            else:
                action_value = int(action_value)
            test_value = int(test_value)
            test_true = int(test_true)
            test_false = int(test_false)
            monkeys.append(Monkey(monkey_id, items, action, action_value, test_value, test_true, test_false))

    return monkeys


def solve(monkeys, turns, worry_divider=None):
    """
    >>> monkeys = read_input('input/2022/day11-test.txt')
    >>> solve(monkeys, 20, 3)
    10605
    >>> monkeys = read_input('input/2022/day11-test.txt')
    >>> solve(monkeys, 10000)
    2713310158
    """

    for _ in range(turns):
        for monkey in monkeys:
            monkey.inspect(worry_divider)

    monkeys = sorted(monkeys, reverse=True)
    return monkeys[0].inspections * monkeys[1].inspections


def part1(monkeys):
    """
    >>> part1(read_input())
    90294
    """

    return solve(monkeys, 20, 3)


def part2(monkeys):
    """
    >>> part2(read_input())
    18170818354
    """

    return solve(monkeys, 10000)


def main():
    print(part1(read_input()))
    print(part2(read_input()))


if __name__ == "__main__":
    main()
