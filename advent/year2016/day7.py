# -*- coding: utf-8 -*-


def read_input():
    with open('input/2016/day7-input.txt', encoding='utf8') as file:
        return [line.strip() for line in file.readlines()]


def supports_tls(address):
    """
    >>> supports_tls('abba[mnop]qrst')
    True
    >>> supports_tls('ioxxoj[asdfgh]zxcvbn')
    True
    >>> supports_tls('aaaa[qwer]tyui')
    False
    >>> supports_tls('abcd[bddb]xyyx')
    False
    """

    result = False
    a = None
    b = None
    c = None
    bracket = 0

    for d in address:
        if d == '[':
            bracket += 1
        elif d == ']':
            bracket -= 1
        elif a == d and b == c and a != b:
            if bracket > 0:
                return False

            result = True

        a, b, c = b, c, d

    return result


def supports_ssl(address):
    """
    >>> supports_ssl('aba[bab]xyz')
    True
    >>> supports_ssl('aaa[kek]eke')
    True
    >>> supports_ssl('zazbz[bzb]cdb')
    True
    >>> supports_ssl('xyx[xyx]xyx')
    False
    """

    a = None
    b = None
    bracket = 0
    accessors = set()
    blocks = set()

    for c in address:
        if c == '[':
            bracket += 1
        elif c == ']':
            bracket -= 1
        elif a == c and a != b:
            if bracket > 0:
                blocks.add((b, a))
            else:
                accessors.add((a, b))

        a, b = b, c

    return True if accessors.intersection(blocks) else False


def part1(data):
    """
    >>> part1(read_input())
    115
    """

    return sum(1 for address in data if supports_tls(address))


def part2(data):
    """
    >>> part2(read_input())
    231
    """

    return sum(1 for address in data if supports_ssl(address))


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
