# -*- coding: utf-8 -*-

from advent import md5

INPUT = 'cxdnnyjw'


def find_password(value):
    """
    >>> find_password('abc')
    '18f47a30'
    """

    password = ''
    index = 0

    while True:
        hash_value = md5(value + str(index))
        index += 1

        if hash_value.startswith('00000'):
            password += hash_value[5]

            if len(password) == 8:
                break

    return password


def find_other_password(value):
    """
    >>> find_other_password('abc')
    '05ace8e3'
    """

    password = [None] * 8
    index = 0

    while True:
        hash_value = md5(value + str(index))
        index += 1

        if hash_value.startswith('00000') and hash_value[5].isdigit():
            place = int(hash_value[5])

            if place < 8 and password[place] is None:
                password[place] = hash_value[6]

                if all(x is not None for x in password):
                    break

    return ''.join(password)


def part1(data):
    """
    >>> part1(INPUT)
    'f77a0e6e'
    """

    return find_password(data)


def part2(data):
    """
    >>> part2(INPUT)
    '999828ec'
    """

    return find_other_password(data)


def main():
    print(part1(INPUT))
    print(part2(INPUT))


if __name__ == "__main__":
    main()
