import re
from collections import defaultdict

PATTERN = re.compile("(\d+) <-> ((\d+, )*\d+)")

def load(filename):
    graph = defaultdict(set)

    for line in file(filename):
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

graph = load('day12-input.txt')
zero_group_size = len(find(graph,0))

nodes = set(graph.keys())
count = 0

while (len(nodes) > 0):
    count += 1
    root = nodes.pop()
    found = find(graph,root)
    nodes -= found

print zero_group_size, count
