import itertools 
from collections import defaultdict
import re
import advent

PATTERN = re.compile(r"p=<(-?\d+),(-?\d+),(-?\d+)>, v=<(-?\d+),(-?\d+),(-?\d+)>, a=<(-?\d+),(-?\d+),(-?\d+)>")

def read_input(filename):
    for line in file(filename):
        result = PATTERN.match(line)
        values = [int(v) for v in result.groups()]
        yield values[0:3], values[3:6], values[6:9]

def load_particles(filename):
    return dict(enumerate(read_input(filename)))

def vector_add(x,y):
    return tuple(a + b for a,b in zip(x,y))

def same_sign(v,a):
    return a == 0 or ((v > 0) == (a > 0))

def same_direction(v,a):
    return all(same_sign(a,b) for a,b in zip(v,a))

def manhattan_distance(p):
    return sum(abs(x) for x in p)

def part1(filename):
    min_size = None
    slowest = set()

    particles = load_particles(filename)

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

def part2(filename, turns):
    particles = load_particles(filename)

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
    print part1("day20-input.txt")
    print part2("day20-input.txt", 500)

if __name__ == "__main__":
    main()
