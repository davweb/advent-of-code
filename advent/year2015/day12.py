# -*- coding: utf-8 -*-

import json


def read_input():
    with open('input/2015/day12-input.txt', encoding='utf8') as file:
        return json.loads(file.read())


def sum_json(json_value):

    if isinstance(json_value, int):
        return json_value

    if isinstance(json_value, list):
        return sum(sum_json(item) for item in json_value)

    if isinstance(json_value, dict):
        return sum(sum_json(item) for item in json_value.values())

    return 0


def sum_json_no_red(json_value):

    if isinstance(json_value, int):
        return json_value

    if isinstance(json_value, list):
        return sum(sum_json_no_red(item) for item in json_value)

    if isinstance(json_value, dict):
        if 'red' in json_value.values():
            return 0
        return sum(sum_json_no_red(item) for item in json_value.values())

    return 0


def part1(data):
    """
    >>> part1(read_input())
    191164
    """

    return sum_json(data)


def part2(data):
    """
    >>> part2(read_input())
    87842
    """

    return sum_json_no_red(data)


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
