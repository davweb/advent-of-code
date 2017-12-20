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

def vector_add(x,y):
    return tuple(a + b for a,b in zip(x,y))

def part1(filename):
    min_size = None
    min_index = None

    for index, (p, v, a) in enumerate(read_input(filename)):
        for _ in range(10000):
            v = vector_add(v, a)
            p = vector_add(p, v)

        size = sum(abs(x) for x in p)
        if min_size is None or size < min_size:
            min_size, min_index = size, index

    return min_index


def part2():
    pass

def main():
    print part1("day20-input.txt")
    part2()

if __name__ == "__main__":
    main()
