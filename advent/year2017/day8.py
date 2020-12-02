import re
from collections import defaultdict

PATTERN = re.compile("([a-z]+) (inc|dec) (-?\d+) if ([a-z]+) ([<>=!]+) (-?\d+)")

def read_input():
    file = open('input/2017/day8-input.txt', 'r')
    data = []

    for line in file:
        result = PATTERN.match(line)
        target, op, amount, source, comparison, value = result.group(1, 2, 3, 4, 5, 6)
        data.append((target, op, int(amount), source, comparison, int(value)))

    return data


def part1and2(data):
    """
    >>> part1and2([['b', 'inc1', 5, 'a', '>', 1], ['a', 'inc', 1, 'b', '<', 5], ['c', 'dec', -10, 'a', '>=', 1], ['c', 'inc', -20, 'c', '==', 10]])
    (1, 10)
    >>> part1and2(read_input())
    (4647, 5590)
    """

    values = defaultdict(int)
    maxval = None

    for (target, op, amount, source, comparison, value) in data:
        current = values[source]

        if comparison == "==":
            result = current == value
        elif comparison == "!=":
            result = current != value
        elif comparison == ">":
            result = current > value
        elif comparison == "<":
            result = current < value
        elif comparison == ">=":
            result = current >= value
        elif comparison == "<=":
            result = current <= value
        else:
            raise ValueError("Unknown comparison '%s'" % comparison)

        if result:
            old = values[target]
            
            if op == "inc":
                old += amount
            elif op == "dec":
                old -= amount    
            else:
                raise ValueError("Unknown operator: %s" % op)

            values[target] = old
            if maxval is None or maxval < old:
                maxval = old

    return (max(values.values())), maxval


def main():
    data = read_input()
    print(part1and2(data))


if __name__ == "__main__":
    main()
