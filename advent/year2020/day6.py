from itertools import chain
from functools import reduce

def read_input():
    file = open('input/2020/day6-input.txt', 'r')
    groups = []
    group = []

    for line in chain(file, ['']):
        line = line.strip()

        if line == '':
            groups.append(group)
            group = []
        else:
            group.append(set(line.strip()))

    return groups


def part1(groups):
    """
    >>> part1([[set('abc')], [set('a'), set('b'), set('c')], [set('ab'), set('ac')], [set('a'), set('a'), set('a'), set('a')], [set('b')]])
    11
    >>> part1(read_input())
    6680
    """
 
    return sum(len(reduce(set.union, group)) for group in groups)


def part2(groups):
    """
    >>> part2(read_input())
    3117
    """

    return sum(len(reduce(set.intersection, group)) for group in groups)


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
