#!/usr/local/bin/python3

from collections import defaultdict

def has_adjacent_digits(n):
    """
    >>> has_adjacent_digits(111111)
    True
    >>> has_adjacent_digits(123456)
    False
    >>> has_adjacent_digits(11111)
    Traceback (most recent call last):
        ...
    ValueError: not a six digit number '11111'
    """

    s = str(n)

    if len(s) != 6:
        raise ValueError("not a six digit number '{}'".format(s))

    return s[0] == s[1] or s[1] == s[2] or s[2] == s[3] or s[3] == s[4] or s[4] == s[5]

def has_never_decreasing_digits(n):
    """
    >>> has_never_decreasing_digits(111111)
    True
    >>> has_never_decreasing_digits(123456)
    True
    >>> has_never_decreasing_digits(123450)
    False
    """

    last = None

    while n > 0:
        digit = n % 10
        n //= 10

        if last != None and last < digit:
            return False

        last = digit

    return True

def has_pair_of_digits(n):
    """
    >>> has_pair_of_digits(112233)
    True
    >>> has_pair_of_digits(123444)
    False
    >>> has_pair_of_digits(111122)
    True
    >>> has_pair_of_digits(221111)
    True
    >>> has_pair_of_digits(112211)
    True
    """

    last = None
    count = 0

    while n > 0:
        digit = n % 10
        n //= 10

        if last == digit:
            count += 1
        elif count == 2:
            return True
        else:
            count = 1

        last = digit

    return count == 2

def part1(data):
    print(len([x for x in data if has_adjacent_digits(x) and has_never_decreasing_digits(x)]))

def part2(data):
    print(len([x for x in data if has_pair_of_digits(x) and has_never_decreasing_digits(x)]))

def main():
    input = (245182, 790572)
    part1(range(*input))
    part2(range(*input))

if __name__ == "__main__":
    main()
