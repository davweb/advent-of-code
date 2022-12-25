# -*- coding: utf-8 -*-


def read_input():
    with open('input/2022/day25-input.txt', encoding='utf8') as file:
        return [line.strip() for line in file]


SNAFU_VALUE = {
    '=': -2,
    '-': -1,
    '0': 0,
    '1': 1,
    '2': 2
}


def snafu_to_decimal(snafu):
    """
    >>> snafu_to_decimal('1=-0-2')
    1747
    >>> snafu_to_decimal('12111')
    906
    >>> snafu_to_decimal('2=0=')
    198
    >>> snafu_to_decimal('20012')
    1257
    """

    power = 1
    decimal = 0

    while snafu:
        digit = snafu[-1]
        snafu = snafu[:-1]
        decimal += power * SNAFU_VALUE[digit]
        power *= 5

    return decimal


def decimal_to_snafu(decimal):
    """
    >>> decimal_to_snafu(1747)
    '1=-0-2'
    >>> decimal_to_snafu(906)
    '12111'
    >>> decimal_to_snafu(198)
    '2=0='
    >>> decimal_to_snafu(1257)
    '20012'
    >>> decimal_to_snafu(4890)
    '2=-1=0'
    """

    power = 1
    half = 0

    while decimal > 2 * power:
        half += 2 * power
        power *= 5

    snafu = ''

    while power > 0:

        if decimal > power + half:
            snafu += '2'
            decimal -= 2 * power
        elif decimal > half:
            snafu += '1'
            decimal -= power
        elif decimal < -(power + half):
            snafu += '='
            decimal += 2 * power
        elif decimal < -half:
            snafu += '-'
            decimal += power
        elif snafu != '':
            snafu += '0'

        power = power // 5
        half -= 2 * power

    return snafu


def part1(data):
    """
    >>> part1(read_input())
    '2-00=12=21-0=01--000'
    """

    return decimal_to_snafu(sum(snafu_to_decimal(snafu) for snafu in data))


def main():
    print(part1(read_input()))


if __name__ == "__main__":
    main()
