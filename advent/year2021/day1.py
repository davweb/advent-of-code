# -*- coding: utf-8 -*-

def read_input():
    with open('input/2021/day1-input.txt', encoding='utf8') as file:
        return [int(line) for line in file.readlines()]


def part1(data):
    """
    >>> part1([199, 200, 208, 210, 200, 207, 240, 269, 260, 263])
    7
    >>> part1(read_input())
    1581
    """
    previous = data[0]
    count = 0

    for value in data[1:]:
        if value > previous:
            count += 1

        previous = value

    return count


def part2(data):
    """
    >>> part2([199, 200, 208, 210, 200, 207, 240, 269, 260, 263])
    5
    >>> part2(read_input())
    1618
    """
    count = 0

    for i in range(1, len(data) - 2):
        previous = sum(data[i - 1:i + 2])
        value = sum(data[i:i + 3])

        if value > previous:
            count += 1

    return count


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
