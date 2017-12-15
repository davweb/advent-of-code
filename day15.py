from itertools import islice

DIVISOR = 2147483647
MASK = 2 ** 16 - 1

def generate(value, factor, matcher=None):
    while True:
        value = value * factor % DIVISOR
        if matcher is None or value % matcher == 0:
            yield value

def pairs(a, b, count):
    return zip(islice(a, count), islice(b, count))

def match(pair):
    return pair[0] & MASK == pair[1] & MASK

a = generate(512, 16807)
b = generate(191, 48271)
print sum(match(pair) for pair in pairs(a,b,40000000))

a = generate(512, 16807, 4)
b = generate(191, 48271, 8)
print sum(match(pair) for pair in pairs(a,b,5000000))

