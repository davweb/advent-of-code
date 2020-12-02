import re
from collections import defaultdict

PATTERN = re.compile(r"(\d+) <-> ((\d+, )*\d+)")

def read_input():
    graph = defaultdict(set)
    file = open('input/2017/day12-input.txt', 'r')

    for line in file.readlines():
        result = PATTERN.match(line)
        source, targets = result.group(1, 2)
        source = int(source)
        targets = [int(target) for target in targets.split(", ")]

        for target in targets:
            graph[source].add(target)
            graph[target].add(source)

    return graph

def find(graph, node, seen=None):
    if seen is None:
        seen = set()
    seen.add(node)
    
    for target in graph[node]:
        if target not in seen:
            find(graph, target, seen)
            
    return seen

def part1(graph):
    """
    >>> part1(read_input())
    130
    """

    return len(find(graph, 0))

def part2(graph):
    """
    >>> part2(read_input())
    189
    """

    nodes = set(graph.keys())
    count = 0

    while (len(nodes) > 0):
        count += 1
        root = nodes.pop()
        found = find(graph, root)
        nodes -= found

    return count


def main():
    graph = read_input()
    print(part1(graph))
    print(part2(graph))


if __name__ == "__main__":
    main()
