# -*- coding: utf-8 -*-
# pylint: disable=too-many-locals

import re

SEEDS_PATTERN = re.compile(r'seeds:(( \d+)+)')
MAP_PATTERN = re.compile(r'(\w+)-to-(\w+) map:\n((\d+ \d+ \d+\n)+)', re.MULTILINE)


def read_input(filename='input/2023/day5-input.txt'):
    with open(filename, encoding='utf8') as file:
        content = file.read()

        match = SEEDS_PATTERN.match(content)
        seeds = [int(i) for i in match.group(1).split()]

        mappings = []

        for match in MAP_PATTERN.finditer(content):
            source_name = match.group(1)
            destination_name = match.group(2)
            ranges = [[int(i) for i in line.split()] for line in match.group(3).strip().split('\n')]
            mappings.append((source_name, destination_name, ranges))

        return seeds, mappings


def part1(data):
    """
    >>> part1(read_input())
    389056265
    """

    seeds, mappings = data
    lowest = None
    lookup = {}

    for (source_name, destination_name, ranges) in mappings:
        lookup[source_name] = (destination_name, ranges)

    for value in seeds:
        source_name = 'seed'

        while source_name != 'location':
            source_name, ranges = lookup[source_name]

            for destination_start, source_start, length in ranges:
                if source_start <= value < source_start + length:
                    value = destination_start + value - source_start
                    break

        lowest = value if lowest is None else min(lowest, value)

    return lowest


def part2(data):
    """
    >>> part2(read_input())
    137516820
    """

    seeds, mappings = data
    lowest = None
    lookup = {}

    for (source_name, destination_name, ranges) in mappings:
        lookup[source_name] = (destination_name, ranges)

    queue = []

    while seeds:
        item_start = seeds.pop(0)
        item_length = seeds.pop(0)
        queue.append(('seed', item_start, item_start + item_length))

    while queue:
        source_name, item_start, item_end = queue.pop(0)

        if source_name == 'location':
            lowest = item_start if lowest is None else min(lowest, item_start)
            continue

        destination_name, ranges = lookup[source_name]
        queued = False

        for destination_start, source_start, range_length in ranges:
            source_end = source_start + range_length

            # item fits in range
            if source_start <= item_start and source_end >= item_end:
                new_item_start = destination_start + item_start - source_start
                new_item_end = new_item_start + (item_end - item_start)
                queue.append((destination_name, new_item_start, new_item_end))
                queued = True
                break

            #  item overlaps range on lower end
            if item_start < source_start < item_end:
                queue.append((source_name, item_start, source_start))
                queue.append((source_name, source_start, item_end))
                queued = True
                break

            # item overlaps range on upper end
            if item_start < source_end <= item_end:
                queue.append((destination_name, item_start, source_end))
                queue.append((source_name, source_end, item_end))
                queued = True
                break

        # If we didn't overlap any of the mapping ranges values are unchanged
        if not queued:
            queue.append((destination_name, item_start, item_length))

    return lowest


def main():
    print(part1(read_input()))
    print(part2(read_input()))


if __name__ == "__main__":
    main()
