from itertools import islice, izip

DIVISOR = 2147483647
MASK = 2 ** 16 - 1

def generate(value, factor, matcher=None):
    while True:
        value = value * factor % DIVISOR
        if matcher is None or value % matcher == 0:
            yield value

def pairs(a, b, count):
    return izip(islice(a, count), islice(b, count))

def match(pair):
    return pair[0] & MASK == pair[1] & MASK

def part1():
    a = generate(512, 16807)
    b = generate(191, 48271)
    print sum(match(pair) for pair in pairs(a,b,40000000))

def part2():
    a = generate(512, 16807, 4)
    b = generate(191, 48271, 8)
    print sum(match(pair) for pair in pairs(a,b,5000000))

if __name__ == "__main__":
    part1()
    part2()