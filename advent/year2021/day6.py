# -*- coding: utf-8 -*-

from functools import cache


def read_input():
    with open('input/2021/day6-input.txt', encoding='utf8') as file:
        return [int(fish) for fish in file.read().split(',')]


def one_day(fishes):
    """
    >>> one_day([3, 4, 3, 1, 2])
    [2, 3, 2, 0, 1]
    >>> one_day([2, 3, 2, 0, 1])
    [1, 2, 1, 6, 0, 8]
    """

    result = []
    new_fish = 0

    for fish in fishes:
        if fish == 0:
            result.append(6)
            new_fish += 1
        else:
            result.append(fish - 1)

    return result + [8] * new_fish


@cache
def number_of_fish(days, value=8):
    """
    >>> number_of_fish(1)
    1
    >>> number_of_fish(8)
    1
    >>> number_of_fish(9)
    2
    >>> number_of_fish(15)
    2
    >>> number_of_fish(16)
    3
    >>> number_of_fish(18)
    4
    >>> number_of_fish(25)
    7
    >>> number_of_fish(47)
    38
    >>> number_of_fish(48)
    48
    """

    result = 1

    while days > 0:
        days -= 1

        if value == 0:
            result += number_of_fish(days)
            value = 6
        else:
            value -= 1

    return result


def total_fish(fishes, days):
    """
    >>> total_fish([4], 3)
    1
    >>> total_fish([4], 8)
    2
    >>> total_fish([4], 15)
    4
    >>> total_fish([2, 3, 4], 15)
    12
    >>> total_fish([2, 3, 4], 17)
    13
    >>> total_fish([2, 3, 4], 18)
    14
    >>> total_fish([2, 3, 4], 19)
    17
    >>> total_fish([2, 3, 4], 20)
    19
    >>> total_fish([2, 3, 4], 49)
    227
    """

    return sum(number_of_fish(days, fish) for fish in fishes)


def part1(data):
    """
    >>> part1([3, 4, 3, 1, 2])
    5934
    >>> part1(read_input())
    393019
    """

    fish = data

    for _ in range(80):
        fish = one_day(fish)

    return len(fish)


def part2(data):
    """
    >>> part2([3, 4, 3, 1, 2])
    26984457539
    >>> part2(read_input())
    1757714216975
    """

    return total_fish(data, 256)


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
