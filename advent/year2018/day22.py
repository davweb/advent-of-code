# -*- coding: utf-8 -*-

from enum import Enum

DEPTH = 5616
TARGET = (10, 785)
PADDING = 20

class Type(Enum):
    ROCKY = 0
    WET = 1
    NARROW = 2

class Tool(Enum):
    NEITHER = 0
    TORCH = 1
    CLIMBING_GEAR = 2

BANNED_TOOL = {
    Type.ROCKY: Tool.NEITHER,
    Type.WET: Tool.TORCH,
    Type.NARROW: Tool.CLIMBING_GEAR
}

def calculate_map(depth, target, padding = 0):
    geologic_index = {}
    erosion_level = {}
    region_map = {}

    for y in range(target[1] + 1 + padding):
        for x in range(target[0] + 1 + padding):

            if (x, y) == (0, 0):
                index = 0
            elif (x, y) == target:
                index = 0
            elif y == 0:
                index = x * 16807
            elif x == 0:
                index = y * 48271
            else:
                index = erosion_level[(x - 1, y)] * erosion_level[(x, y - 1)]

          
            geologic_index[(x, y)] = index
            
            level = (index + depth) % 20183
            erosion_level[(x, y)] = level

            region_map[(x, y)] = Type(level % 3)

    return region_map


def part1(depth, target):
    """
    >>> part1(510, (10, 10))
    114
    >>> part1(DEPTH, TARGET)
    8681
    """

    region_map = calculate_map(depth, target)

    return sum(region.value for region in region_map.values())


def adjacents(location, max_x, max_y):
    x, y = location

    if y > 0:
        yield (x, y - 1)
        
    if x > 0:
        yield (x - 1, y)

    if x < max_x:
        yield (x + 1, y)
    
    if y < max_y:
        yield (x, y + 1)


def part2(depth, target):
    """
    >>> part2(510, (10, 10))
    45
    >>> part2(DEPTH, TARGET)
    1070
    """

    padding = 50
    region_map = calculate_map(depth, target, padding)
    max_x = target[0] + padding
    max_y = target[1] + padding

    queue = []
    location = (0, 0)
    tool = Tool.TORCH
    queue = [(location, tool)]
    time = {(location, tool): 0}

    while queue:
        pair = queue.pop(0)
        (location, tool) = pair
        location_type = region_map[location]
        location_time = time[pair]

        for option in adjacents(location, max_x, max_y):
            option_type = region_map[option]

            if tool == BANNED_TOOL[option_type]:
                continue

            option_time = location_time + 1
            new_pair = (option, tool)

            if new_pair not in time or time[new_pair] > option_time:
                time[new_pair] = option_time
                queue.append(new_pair)

        for option in Tool:
            if option == tool or option == BANNED_TOOL[location_type]:
                continue

            option_time = location_time + 7
            new_pair = (location, option)

            if new_pair not in time or time[new_pair] > option_time:
                time[new_pair] = option_time
                queue.append(new_pair)
    
    return time[(target, Tool.TORCH)]


def main():
    print(part1(DEPTH, TARGET))
    print(part2(DEPTH, TARGET))


if __name__ == "__main__":
    main()
