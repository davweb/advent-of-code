# -*- coding: utf-8 -*-

def read_input(filename='input/2018/day25-input.txt'):
    points = []

    with open(filename, encoding='utf8') as file:
        for line in file:
            points.append(tuple(int(n) for n in line.split(',')))

    return points


def manhattan_distance(a, b):
    """
    >>> manhattan_distance((-1, -5, 6, -1), (-8, 4, -5, 1))
    29
    """

    return sum(abs(x - y) for x, y in zip(a, b))


def in_constellation(star, constellation):
    return any(manhattan_distance(member, star) <= 3 for member in constellation)


def part1(data):
    """
    >>> part1(read_input('input/2018/day25-test.txt'))
    3
    >>> part1(read_input())
    386
    """

    constellations = 0
    stars = set(data)
    matches = {}

    while stars:
        if not matches:
            constellation = {stars.pop()}
            constellations += 1
        else:
            constellation.update(matches)
            stars.difference_update(matches)

        matches = {star for star in stars if in_constellation(star, constellation)}

    return constellations


def main():
    print(part1(read_input()))


if __name__ == "__main__":
    main()
