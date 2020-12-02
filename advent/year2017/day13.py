import re

PATTERN = re.compile("(\d+): (\d+)")


def read_input():
    firewall = {}
    file = open('input/2017/day13-input.txt', 'r')

    for line in file.readlines():
        result = PATTERN.match(line)
        layer, depth = result.group(1, 2)
        layer = int(layer)
        firewall[layer] = int(depth)

    return firewall


def part1(firewall):
    """
    >>> part1(read_input())
    2264
    """

    severity = sum(depth * range for (depth, range) in firewall.items() if depth % (range * 2 - 2) == 0)
    return severity


def clear(firewall, delay):
    for depth, range in firewall.items():
        turns = depth + delay
        position = turns % (range * 2 - 2)
        if position == 0:
            return False

    return True


def part2(firewall):
    """
    >>> part2(read_input())
    3875838
    """

    delay = 0

    while(not clear(firewall,delay)):
        delay += 1

    return delay


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
