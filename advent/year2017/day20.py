from collections import defaultdict
import re

PATTERN = re.compile(r"p=<(-?\d+),(-?\d+),(-?\d+)>, v=<(-?\d+),(-?\d+),(-?\d+)>, a=<(-?\d+),(-?\d+),(-?\d+)>")


def read_input():
    data = []
    index = 0

    for line in open('input/2017/day20-input.txt', 'r'):
        result = PATTERN.match(line)
        values = [int(v) for v in result.groups()]
        data.append((index, (values[0:3], values[3:6], values[6:9])))
        index += 1

    return dict(data)

def vector_add(x,y):
    return tuple(a + b for a,b in zip(x,y))


def same_sign(v,a):
    return a == 0 or ((v > 0) == (a > 0))


def same_direction(v,a):
    return all(same_sign(a,b) for a,b in zip(v,a))


def manhattan_distance(p):
    return sum(abs(x) for x in p)


def part1(particles):
    """
    >>> part1(read_input())
    457
    """

    min_size = None
    slowest = set()

    for index, (p, v, a) in particles.items():
        size = manhattan_distance(a)
        if size == min_size:
            slowest.add(index)
        if min_size is None or size < min_size:
            min_size = size
            slowest = set([index])

    min_steps = None
    min_index = None

    for index in slowest:
        p, v, a = particles[index]

        while not same_direction(v, a):
            v = vector_add(v, a)
            p = vector_add(p, v)

        steps = manhattan_distance(p)

        if min_steps is None or steps < min_steps:
            min_steps = steps
            min_index = index

    return min_index


def part2(particles):
    """
    >>> part2(read_input())
    448
    """

    turns = 500

    for _ in range(0, turns):
        positions = defaultdict(set)

        for index, (p, v, a) in particles.items():
            v = vector_add(v, a)
            p = vector_add(p, v)
            particles[index] = (p, v, a)
            positions[p].add(index)

        for indexes in positions.values():
            if len(indexes) > 1:
                for index in indexes:
                    del particles[index]

    return len(particles)


def main():
    print(part1(read_input()))
    print(part2(read_input()))


if __name__ == "__main__":
    main()
