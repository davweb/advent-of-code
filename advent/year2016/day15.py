# -*- coding: utf-8 -*-

import re

PATTERN = re.compile(r'Disc #(\d+) has (\d+) positions; at time=0, it is at position (\d+)')

def read_input():
    output = []

    with open('input/2016/day16-input.txt', encoding='utf8') as file:
        while match:= PATTERN.match(file.readline()):
            output.append([int(x) for x in match.groups()])

    return output


class Disc:
    def __init__(self, disc_id, size, start):
        self.disc_id = disc_id
        self.size = size
        self.position = start

    def tick(self):
        self.position = (self.position + 1) % self.size

    def ready_to_drop(self):
        return (self.position + self.disc_id) % self.size == 0

    def __repr__(self):
        return f'Disc({self.disc_id}, {self.size}, {self.position})'


def find_drop(discs):
    time = 0

    while not all(disc.ready_to_drop() for disc in discs):
        for disc in discs:
            disc.tick()

        time += 1

    return time


def part1(data):
    """
    >>> part1(read_input())
    122318
    """

    discs = [Disc(disc_id, size, start) for disc_id, size, start in data]
    return find_drop(discs)


def part2(data):
    """
    >>> part2(read_input())
    3208583
    """

    discs = [Disc(disc_id, size, start) for disc_id, size, start in data]

    next_disc_id = max(disc.disc_id for disc in discs) + 1
    discs.append(Disc(next_disc_id, 11, 0))

    return find_drop(discs)


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
