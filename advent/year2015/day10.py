# -*- coding: utf-8 -*-

import csv

INPUT = '3113322113'


def read_elements():
    """
    Elements of the sequence
    http://www.nathanieljohnston.com/2010/10/a-derivation-of-conways-degree-71-look-and-say-polynomial/
    """

    elements = {}

    with open('input/2015/day10-elements.txt', encoding='utf8') as csvfile:
        element_reader = csv.reader(csvfile)

        for line in element_reader:
            element_id, pattern, length, next_elements = line

            element = {
                'id': int(element_id),
                'pattern': pattern,
                'length': int(length),
                'next': [int(next_id) for next_id in next_elements.split(',')]
            }

            elements[element['id']] = element

    return elements


ELEMENTS = read_elements()


def look_and_say(string, iterations):
    """
    >>> look_and_say('1', 5)
    '312211'
    >>> look_and_say('132', 4)
    '11131221232112'
    >>> look_and_say('132', 5)
    '31131122111213122112'
    """

    for _ in range(iterations):
        result = ''
        previous = None
        count = 0

        for c in string:
            if previous is not None and previous != c:
                result = f'{result}{count}{previous}'
                count = 0

            previous = c
            count += 1

        string = f'{result}{count}{previous}'

    return string


def deconstruct(string):
    """
    >>> deconstruct('')
    []
    >>> deconstruct('3')
    [62]
    >>> deconstruct('321121112')
    [92, 1]
    >>> deconstruct('132112211213322113')
    [43]
    """

    if string == '':
        return []

    for element in ELEMENTS.values():
        element_id = element['id']
        pattern = element['pattern']

        if string.startswith(pattern):
            remainder = string[len(pattern):]
            children = deconstruct(remainder)

            if children is not None:
                return [element_id] + children

    return None


def calculate_length(element_id, iterations):
    element = ELEMENTS[element_id]

    if iterations == 0:
        return element['length']

    return sum(calculate_length(next_id, iterations - 1) for next_id in element['next'])


def recursive_look_and_say(string, iterations):
    """
    >>> recursive_look_and_say("3", 0)
    1
    >>> recursive_look_and_say("3", 1)
    2
    >>> recursive_look_and_say("3", 2)
    4
    >>> recursive_look_and_say("132", 2)
    8
    >>> recursive_look_and_say("1323", 2)
    12
    >>> recursive_look_and_say('132', 4)
    14
    >>> recursive_look_and_say('132', 5)
    20
    """

    element_ids = deconstruct(string)
    return sum(calculate_length(element_id, iterations) for element_id in element_ids)


def part1(data):
    """
    >>> part1(INPUT)
    329356
    """

    return len(look_and_say(data, 40))


def part2(data):
    """
    >>> part2(INPUT)
    4666278
    """

    return recursive_look_and_say(data, 50)


def main():
    print(part1(INPUT))
    print(part2(INPUT))


if __name__ == "__main__":
    main()
