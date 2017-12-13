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
    layers = firewall.keys()
    max_depth = max(layers)
    scanners = dict((layer, (0, True)) for layer in layers)
    depth = 0
    severity = 0

    while depth <= max_depth:
        if depth in scanners:
            position, up = scanners[depth]
            if position == 0:
                range = firewall[depth]
                severity += depth * range 

        for layer in layers:
            position, up = scanners[layer]
            
            if up:
                position += 1
                if position == firewall[layer]:
                    position -= 2
                    up = False
            else:
                position -=1
                if position < 0:
                    position = 1
                    up = True

            scanners[layer] = (position,up)
        depth += 1

    return severity

firewall = load('day13-input.txt')
print play(firewall)
