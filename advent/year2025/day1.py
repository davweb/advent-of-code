# -*- coding: utf-8 -*-


def read_input(filename='input/2025/day1-input.txt'):
    with open(filename, encoding='utf8') as file:
        return file.readlines()


def part1(data):
    """
    >>> part1(['L68', 'L30', 'R48', 'L5', 'R60', 'L55', 'L1', 'L99', 'R14', 'L82'])
    3
    >>> part1(read_input())
    995
    """

    value = 50
    count = 0

    for line in data:
        direction = 1 if line[0] == 'R' else -1
        clicks = int(line[1:])

        value += direction * clicks
        value %= 100

        if value == 0:
            count += 1

    return count


def part2(data):
    """
    >>> part2(['L50', 'R1'])
    1
    >>> part2(['L500', 'R1'])
    5
    >>> part2(['R500', 'L1'])
    5
    >>> part2(['L50', 'R100'])
    2
    >>> part2(['L50', 'R1', 'L1'])
    2
    >>> part2(['R50', 'L5', 'R6'])
    2
    >>> part2(['L68', 'L30', 'R48', 'L5', 'R60', 'L55', 'L1', 'L99', 'R14', 'L82'])
    6
    >>> part2(read_input())
    5847
    """

    value = 50
    count = 0

    for line in data:
        direction = 1 if line[0] == 'R' else -1
        clicks = int(line[1:])

        for _ in range(clicks):
            value += direction
            value %= 100
            if value == 0:
                count += 1

    return count


def main():
    print(part1(read_input()))
    print(part2(read_input()))


if __name__ == "__main__":
    main()
