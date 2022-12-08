# -*- coding: utf-8 -*-

from collections import deque
import numpy

INPUT = 3014603


def next_index(array, current):
    while True:
        current += 1

        if current == array.size:
            current = 0

        if array[current]:
            return current


def elf_elephant_party(size):
    """
    >>> elf_elephant_party(5)
    3
    """

    ring = numpy.full(size, True)
    player = 0

    while True:
        loser = next_index(ring, player)

        if loser == player:
            return player + 1

        ring[loser] = False
        player = next_index(ring, loser)


def second_elf_party(size):
    """
    >>> second_elf_party(5)
    2
    """

    ring = deque(range(1, size + 1))

    while (players := len(ring)) > 1:
        move = (players + 1) // 2 - 1
        ring.rotate(move)
        ring.pop()
        ring.rotate(- move - 1)


    return ring.pop()

def part1(data):
    """
    # >>> part1(INPUT)
    # 1834903
    """

    return elf_elephant_party(data)


def part2(data):
    """
    # >>> part2(INPUT)
    # 1420280
    """

    return second_elf_party(data)


def main():
    print(part1(INPUT))
    print(part2(INPUT))


if __name__ == "__main__":
    main()
