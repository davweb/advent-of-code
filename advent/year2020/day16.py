# -*- coding: utf-8 -*-

import re
from math import prod

RULE_PATTERN = re.compile(r"(.*): (\d+)-(\d+) or (\d+)-(\d+)")

def read_input():
    file = open("input/2020/day16-input.txt", "r")
    (rule_definitions, my_ticket_list, other_ticket_list) = file.read().split("\n\n")

    rules = {}

    for groups in RULE_PATTERN.findall(rule_definitions):
        rules[groups[0]] = ((int(groups[1]), int(groups[2])), (int(groups[3]), int(groups[4])))

    my_ticket = [int(i) for i in my_ticket_list.split("\n")[1].strip().split(",")]

    tickets = []

    for ticket in other_ticket_list.strip().split("\n")[1:]:
        tickets.append([int(i) for i in ticket.strip().split(",")])

    return rules, my_ticket, tickets


def error_rate(ticket, rules):
    rate = 0

    for field in ticket:
        valid = False

        for rule in rules.values():
            (from_a, to_a), (from_b, to_b) = rule

            if (from_a <= field <= to_a) or (from_b <= field <= to_b):
                valid = True
                break

        if not valid:
            rate += field

    return rate


def valid(ticket, rules):
    return error_rate(ticket, rules) == 0


def part1(data):
    """
    >>> part1(read_input())
    28882
    """

    rules, _, tickets = data
    return sum(error_rate(ticket, rules) for ticket in tickets)


def part2(data):
    """
    >>> part2(read_input())
    1429779530273
    """

    rules, my_ticket, tickets = data

    # Exclude bad tickets
    tickets = [ticket for ticket in tickets if valid(ticket, rules)]

    column_matches = {}

    # Assume every column is valid for field
    for rule_name in rules.keys():
        column_matches[rule_name] = set(range(0, len(my_ticket)))

    # Exclude the columns that don't match rule
    for ticket in tickets:
        for column, field in enumerate(ticket):
            for rule_name, ((from_a, to_a), (from_b, to_b)) in rules.items():
                if not ((from_a <= field <= to_a) or (from_b <= field <= to_b)):
                    column_matches[rule_name].remove(column)

    field_map = {}

    while sum(len(columns) for columns in column_matches.values()) > 0:
        # Find the first rule that maps to only one column
        rule_name, column = next(iter((rule, next(iter(columns))) for rule, columns in column_matches.items() if len(columns) == 1))
        
        # record the mapping found
        field_map[rule_name] = column

        # exclude that column from all the other lists
        for columns in column_matches.values():
            if column in columns:
                columns.remove(column)

    return prod(my_ticket[column] for name, column in field_map.items() if name.startswith("departure"))


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
