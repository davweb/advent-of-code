#!/usr/local/bin/python3

INPUT = (245182, 790572)


def digits(n):
    """
    >>> digits(0)
    Traceback (most recent call last):
        ...
    ValueError: "0" is not a positive integer
    >>> digits(1)
    [1]
    >>> digits(12)
    [1, 2]
    >>> digits(333)
    [3, 3, 3]
    >>> digits(123456)
    [1, 2, 3, 4, 5, 6]
    """

    if n < 1:
        raise ValueError(f'"{n}" is not a positive integer')

    result = []

    while n > 0:
        digit = n % 10
        n //= 10
        result.append(digit)

    result.reverse()
    return result


def has_adjacent_digits(n):
    """
    >>> has_adjacent_digits(111111)
    True
    >>> has_adjacent_digits(123456)
    False
    >>> has_adjacent_digits(11111)
    True
    """

    last = None

    for digit in digits(n):
        if last == digit:
            return True
        last = digit

    return False


def has_never_decreasing_digits(n):
    """
    >>> has_never_decreasing_digits(111111)
    True
    >>> has_never_decreasing_digits(123456)
    True
    >>> has_never_decreasing_digits(123450)
    False
    """

    last = -1

    for digit in digits(n):
        if digit < last:
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

    for digit in digits(n):
        if last == digit:
            count += 1
        elif count == 2:
            return True
        else:
            count = 1

        last = digit

    return count == 2


def part1(data):
    """
    >>> part1(INPUT)
    1099
    """

    return sum(has_adjacent_digits(x) and has_never_decreasing_digits(x) for x in range(*data))


def part2(data):
    """
    >>> part2(INPUT)
    710
    """

    return sum(has_pair_of_digits(x) and has_never_decreasing_digits(x) for x in range(*data))


def main():
    print(part1(INPUT))
    print(part2(INPUT))


if __name__ == "__main__":
    main()
