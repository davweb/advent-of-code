#!/usr/local/bin/python3

import re
from collections import Counter

PATTERN = re.compile("([a-z]+) \((\d+)\)( -> ([a-z, ]+))?")

def read_input():
    file = open('input/2017/day7-input.txt', 'r')
    data = []

    for line in file:
        result = PATTERN.match(line)
        name, weight, supporting = result.group(1, 2, 4)
        supporting = [] if supporting is None else supporting.split(', ')
        data.append((name, int(weight), supporting))
    
    return data


def part1(data):
    """
    >>> part1(read_input())
    'fbgguv'
    """
   
    supported = set()
    names = set()

    for (name, weight, supporting) in data:
        names.add(name)
        supported.update(supporting)

    return (names - supported).pop()


def part2(data):
    """
    >>> part2(read_input())
    1864
    """

    children = {}
    parents = {}
    weights = {}

    def total_weight(name):
        w = weights[name] 
        if name in children:
            w += sum(total_weight(child) for child in children[name])
        return w


    def odd_one_out(map):
        singles = [value for (value,count) in Counter(map.values()).items() if count == 1]

        if len(singles) != 1:
            return None

        single = singles.pop()

        for name, value in map.items():
            if value == single:
                return name
        
        raise AssertionError("Should find match in the map") 


    def children_weights(name):
        return dict((child, total_weight(child)) for child in children[name])


    def calculate_correct_weight(name):
        parent = parents[name]
        sibling_weights = children_weights(parent)
        wrong_weight = sibling_weights[name]
        right_weight = next(filter(lambda x: x[0] != name, sibling_weights.items()))[1]
        return weights[name] - wrong_weight + right_weight


    def find(name):
        child_weights = children_weights(name)
        odd = odd_one_out(child_weights)

        if odd is None:
            return calculate_correct_weight(name)

        return find(odd)


    for (name, weight, supporting) in data:
        weights[name] = int(weight)
        children[name] = supporting
        for child in supporting:
            parents[child] = name

    root = (set(weights.keys()) - set(parents.keys())).pop()
    return find(root)


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
