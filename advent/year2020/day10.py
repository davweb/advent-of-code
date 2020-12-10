from collections import defaultdict


def read_input():
    file = open('input/2020/day10-input.txt', 'r')
    return tidy([int(line.strip()) for line in file.readlines()])


def tidy(adapters):
    """Add the start and end values and sort the list"""

    target = max(adapters) + 3
    adapters.append(target)
    return sorted(adapters)


def part1(adapters):
    """
    >>> part1(tidy([16, 10, 15, 5, 1, 11, 7, 19, 6, 12, 4]))
    35
    >>> part1(tidy([28, 33, 18, 42, 31, 14, 46, 20, 48, 47, 24, 23, 49, 45, 19, 38, 39, 11, 1, 32, 25, 35, 8, 17, 7, 9, 4, 2, 34, 10, 3]))
    220
    >>> part1(read_input())
    2775
    """
 
    current = 0
    gaps = defaultdict(int)

    for adapter in adapters:
        gaps[adapter - current] += 1
        current = adapter

    return gaps[1] * gaps[3]




def part2(adapters):
    """
    >>> part2(tidy([16, 10, 15, 5, 1, 11, 7, 19, 6, 12, 4]))
    8
    >>> part2(tidy([28, 33, 18, 42, 31, 14, 46, 20, 48, 47, 24, 23, 49, 45, 19, 38, 39, 11, 1, 32, 25, 35, 8, 17, 7, 9, 4, 2, 34, 10, 3]))
    19208
    >>> part2(read_input())
    518344341716992
    """

    routes = {}
    routes[0] = 1
    adapters.insert(0,0)

    for adapter in adapters[1:]:
        routes[adapter] = sum(routes[parent] for parent in adapters if 1 <= adapter - parent <= 3)

    return routes[adapter]


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
