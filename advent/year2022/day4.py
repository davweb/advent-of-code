# -*- coding: utf-8 -*-

def read_input():
    output = []

    with open('input/2022/day4-input.txt', encoding='utf8') as file:
        for line in file:
            elves = [[int(x) for x in elf.split('-')] for elf in line.split(',')]
            output.append([set(range(elf[0], elf[1] + 1)) for elf in elves])

    return output


def part1(data):
    """
    >>> part1(read_input())
    657
    """

    return sum(1 for elf_a, elf_b in data if elf_a.issubset(elf_b) or elf_b.issubset(elf_a))


def part2(data):
    """
    >>> part2(read_input())
    938
    """

    return sum(1 for elf_a, elf_b in data if elf_a.intersection(elf_b))


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
