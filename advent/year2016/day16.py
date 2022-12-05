# -*- coding: utf-8 -*-

INPUT = '10001001100000001'


def dragon(data):
    """
    >>> dragon('1')
    '100'
    >>> dragon('0')
    '001'
    >>> dragon('11111')
    '11111000000'
    >>> dragon('111100001010')
    '1111000010100101011110000'
    """

    mirror = ''.join('1' if c == '0' else '0' for c in data[::-1])
    return f'{data}0{mirror}'


def checksum(data):
    """
    >>> checksum('110010110100')
    '100'
    """

    checksum = data

    while True:
        pairs = [checksum[i:i + 2] for i in range(0, len(checksum), 2)]
        checksum = ''.join('1' if pair[0] == pair[1] else '0' for pair in pairs)

        if len(checksum) % 2 == 1:
            break

    return checksum


def fill(input, size):
    """
    >>> fill('10000', 20)
    '01100'
    """

    while len(input) < size:
        input = dragon(input)

    return checksum(input[0:size])


def part1(data):
    """
    >>> part1(INPUT)
    '10101001010100001'
    """

    return fill(data, 272)


def part2(data):
    """
    >>> part2(INPUT)
    '10100001110101001'
    """

    return fill(data, 35651584)


def main():
    print(part1(INPUT))
    print(part2(INPUT))


if __name__ == "__main__":
    main()
