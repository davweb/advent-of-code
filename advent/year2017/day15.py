from itertools import islice

INPUT_A = 512
INPUT_B = 191

GENERATOR_A = 16807
GENERATOR_B = 48271

DIVISOR = 2147483647
MASK = 2 ** 16 - 1


def generate(value, factor, matcher=None):
    """"
    >>> a = generate(65, GENERATOR_A)
    >>> next(a)
    1092455
    >>> next(a)
    1181022009
    >>> next(a)
    245556042
    >>> next(a)
    1744312007
    >>> next(a)
    1352636452
    >>> a = generate(65, GENERATOR_A, 4)
    >>> next(a)
    1352636452
    >>> next(a)
    1992081072
    >>> next(a)
    530830436
    >>> next(a)
    1980017072
    >>> next(a)
    740335192
    """

    while True:
        value = value * factor % DIVISOR
        if matcher is None or value % matcher == 0:
            yield value


def pairs(a, b, count):
    return zip(islice(a, count), islice(b, count))


def match(pair):
    return pair[0] & MASK == pair[1] & MASK


def part1():
    """
    >>> part1()
    567
    """

    a = generate(INPUT_A, GENERATOR_A)
    b = generate(INPUT_B, GENERATOR_B)
    return sum(match(pair) for pair in pairs(a, b,  40000000))


def part2():
    """
    >>> part2()
    323
    """

    a = generate(INPUT_A, GENERATOR_A, 4)
    b = generate(INPUT_B, GENERATOR_B, 8)
    return sum(match(pair) for pair in pairs(a, b, 5000000))


def main():
    print(part1())
    print(part2())


if __name__ == "__main__":
    main()