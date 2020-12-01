#!/usr/local/bin/python3

def read_input():
    file = open('input/2017/day6-input.txt', 'r')
    return [int(bank) for bank in file.read().split()]


def fullest_bank(banks):
    """
    >>> fullest_bank([2, 4, 1, 2])
    1
    >>> fullest_bank([3, 1, 2, 3])
    0
    """

    return banks.index(max(banks))


def redistribute(banks, i):
    """
    >>> bank = [2, 4, 1, 2]
    >>> redistribute(bank, 1)
    >>> bank
    [3, 1, 2, 3]
    >>> bank = [3, 1, 2, 3]
    >>> redistribute(bank, 0)
    >>> bank
    [0, 2, 3, 4]
    """

    redist = banks[i]
    banks[i] = 0

    while redist > 0:
        i = i + 1
        if i == len(banks):
            i = 0
        banks[i] += 1
        redist -= 1


def part1(banks):
    """
    >>> part1(read_input())
    7864
    """
   
    prev = set()
    count = 0

    while tuple(banks) not in prev:
        prev.add(tuple(banks))
        count += 1
        i = fullest_bank(banks)
        redistribute(banks, i)

    return count


def part2(banks):
    """
    >>> part2(read_input())
    1695
    """
   
    prev = {}
    count = 0

    while tuple(banks) not in prev:
        prev[tuple(banks)] = count
        count += 1
        i = fullest_bank(banks)
        redistribute(banks, i)

    return count - prev[tuple(banks)]


def main():
    print(part1(read_input()))
    print(part2(read_input()))


if __name__ == "__main__":
    main()
