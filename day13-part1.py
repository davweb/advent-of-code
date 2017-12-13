import re

PATTERN = re.compile("(\d+): (\d+)")

def load(filename):
    firewall = {}

    for line in file(filename):
        result = PATTERN.match(line)
        layer, depth = result.group(1, 2)
        layer = int(layer)
        firewall[layer] = int(depth)

    return firewall

def play(firewall):
    severity = sum(depth * range for (depth, range) in firewall.items() if depth % (range * 2 - 2) == 0)
    return severity

firewall = load('day13-input.txt')
print play(firewall)
