# -*- coding: utf-8 -*-


def read_input():
    with open('input/2022/day1-input.txt', encoding='utf8') as file:
        result = []
        group = []

        for line in file.readlines():
            if line == '\n':
                result.append(group)
                group = []
            else:
                group.append(int(line))

    return result


def part1(data):
    """
    >>> part1(read_input())
    75501
    """

    return max(sum(group) for group in data)


def part2(data):
    """
    >>> part2(read_input())
    215594
    """

    return sum(sorted(sum(group) for group in data)[-3:])


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
