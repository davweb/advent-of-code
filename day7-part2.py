import re
from collections import Counter

pattern = re.compile("([a-z]+) \((\d+)\)( -> ([a-z, ]+))?")
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

    for name, value in map.iteritems():
        if value == single:
            return name
    
    raise AssertionError("Should find match in the map") 

def children_weights(name):
    return dict((child, total_weight(child)) for child in children[name])


def calculate_correct_weight(name):
    parent = parents[name]
    sibling_weights = children_weights(parent)
    wrong_weight = sibling_weights[name]
    right_weight = filter(lambda x: x[0] != name, sibling_weights.items()).pop()[1]
    return weights[name] - wrong_weight + right_weight

def find(name):
    child_weights = children_weights(name)
    odd = odd_one_out(child_weights)

    if odd is None:
        return calculate_correct_weight(name)

    return find(odd)

for line in file("day7-input.txt"):
    result = pattern.match(line)
    name, weight, supporting = result.group(1, 2, 4)
    weights[name] = int(weight)

    if supporting is not None:
        childlist = supporting.split(', ')
        children[name] = childlist
        for child in childlist:
            parents[child] = name

root = (set(weights.keys()) - set(parents.keys())).pop()
print find(root)
