#!/usr/local/bin/python3

from collections import defaultdict

def read_input():
    with open("input/2018/day8-input.txt", "r") as file:
        data = file.read()
        return [int(x) for x in data.split(' ')]

def part1(data):
    """
    >>> part1(read_input())
    37439
    """

    data = data.copy()

    queue = [True]
    metadata = 0

    while data:
        is_node = queue.pop(0)

        if is_node:
            child_count = data.pop(0)
            metadata_count = data.pop(0)

            for _ in range(0, metadata_count):
                queue.insert(0, False);

            for _ in range(0, child_count):
                queue.insert(0, True)
        else:
            metadata += data.pop(0)
    
    return metadata


def node_value(data):
    """
    >>> node_value([0, 1, 7])
    (7, 3)
    >>> node_value([0, 3, 1, 0, 5])
    (6, 5)
    >>> node_value([1, 1, 0, 1, 8, 1])
    (8, 6)
    >>> node_value([1, 4, 0, 1, 8, 1, 1, 0, 9])
    (16, 9)
    """

    child_count = data[0]
    metadata_count = data[1]
    index = 2
    children = []
    value = 0

    for _ in range(0, child_count):
        (child_value, child_length) = node_value(data[index:])
        children.append(child_value)
        index += child_length

    for m in data[index:index + metadata_count]:
        if m == 0:
            continue
        
        if children:
            try:
                value += children[m - 1]
            except IndexError:
                pass
        else:
            value += m

    index += metadata_count
    return (value, index)



def part2(data):
    """
    >>> part2(read_input())
    20815
    """
    return node_value(data)[0]

def main():
    data = read_input()
    print(part1(data))
    print(part2(data))

if __name__ == "__main__":
    main()
    