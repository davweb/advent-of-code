# -*- coding: utf-8 -*-

def read_input():
    with open('input/2022/day6-input.txt', encoding='utf8') as file:
        return file.read().strip()


def all_different(value):
    return len(set(value)) == len(value)


def find_markers(value, size):
    """
    >>> find_markers('bvwbjplbgvbhsrlpgdmjqwftvncz', 4)
    5
    >>> find_markers('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', 4)
    10
    >>> find_markers('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', 14)
    29
    """

    buffer = value[0:size]
    queue = value[size:]
    count = size

    while not all_different(buffer):
        buffer = buffer[1:] + queue[0]
        queue = queue[1:]
        count += 1

    return count


def part1(data):
    """
    >>> part1(read_input())
    1155
    """

    return find_markers(data, 4)


def part2(data):
    """
    >>> part2(read_input())
    2789
    """

    return find_markers(data, 14)


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
